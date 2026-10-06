"""Build a local UX review. Observational diagrams never impersonate screenshots.

This report intentionally stays in output/: the supplied original screenshot
contains operating CRM information and is not a public deployment asset.
"""
from pathlib import Path
import html
import json
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
pages = json.loads((ROOT / 'docs/pages.json').read_text(encoding='utf-8'))
comparison = {p['id']: p for p in json.loads((ROOT / 'docs/comparison-data.json').read_text(encoding='utf-8'))}
screens = {s['id']: ROOT / 'docs/screens' / (s['filename'] + '.png') for s in json.loads((ROOT / 'docs/screens/manifest.json').read_text(encoding='utf-8'))}
screens['activity'] = screens['activity-original']  # First implemented activity view, with its original standalone chrome.
inventory = json.loads((ROOT / 'output/crm-page-inventory.json').read_text(encoding='utf-8'))
original_activity = Path('C:/Users/tlscj/AppData/Local/Temp/codex-clipboard-f59bf958-e776-407b-bb1d-10e83a6150e7.png')
source_images = {s['id']: ROOT / 'output/captures-v5/as-is' / s['filename'] for s in json.loads((ROOT / 'output/captures-v5/as-is/manifest.json').read_text(encoding='utf8'))}
source_images['login'] = ROOT / 'output/original-login.jpg'
PUBLIC = '--public' in sys.argv
tab_screens = json.loads((ROOT/'docs/screens/tabs/manifest.json').read_text(encoding='utf8'))
source_tabs = json.loads((ROOT/'output/captures-v5/as-is-tabs/manifest.json').read_text(encoding='utf8'))
source_tab_lookup = {(s['route'],s['key']): ROOT/'output/captures-v5/as-is-tabs'/s['filename'] for s in source_tabs}
appendix = []
tab_intents = {
 'activity': '같은 고객의 기록·이력·견적과 예상 계약으로 이어지는 동작을 구분합니다. 포캐스팅은 별도 등록 화면으로 연결됩니다. AI/OCR와 실제 견적 산출은 서비스 연결 과제입니다.',
 'activity-original': '처음 만든 단독 시안의 네 탭도 빠짐없이 캡처했습니다. 각 작업의 입력 맥락을 고객 요약 아래에 유지합니다.',
 'home': '오늘·이번 주·완료를 전환해 확인할 업무 범위를 바꿉니다. 같은 카드 안의 탭과 목록을 연결해 현재 범위를 식별하도록 구성했습니다.',
 'tasks': '업무의 상태와 보기 방식을 별도 그룹으로 구분합니다. 목록은 비교, 보드는 진행 단계, 달력은 기한을 살펴보도록 설계했습니다. 5개 상태와 3개 보기의 15개 조합을 포함합니다.',
 'news': '전체 기사와 관심 기사를 같은 콘텐츠 카드 안에서 전환합니다. 관심 기사 캡처는 저장된 항목이 없는 빈 상태도 그대로 보여줍니다.',
 'ssl-master': '품목·공급사·갱신주기를 한 기준정보 카드 안에서 구분합니다. 현재 선택한 관리 대상을 탭의 밑줄로 표시합니다.',
 'forecast-status': '전체·이월·달성 현황을 구분해 계약 일정과 성과를 서로 다른 보기에서 확인하도록 구성했습니다.',
 'other-status': '기타계약에도 같은 전체·이월·달성 현황 구조를 적용해 영업 계약과 동일한 탐색 규칙을 사용합니다.',
 'customers': '원본 회사정보·영업활동 탭의 맥락을 상세 패널에서 함께 확인하도록 묶었습니다. 고객사 담당자는 별도 컨택 관리에서 조회합니다.',
 'nonprofits': '기관의 기본 정보와 설립·예산 항목을 상세 패널에 묶었습니다. 담당자·영업활동은 해당 관리 화면으로 연결하는 방향입니다.',
 'marketing': '상시 입력 폼을 목록에서 분리하고 필요할 때 등록창을 엽니다. 모든 입력 항목이 보이도록 상단·하단 스크롤 위치를 각각 캡처했습니다.',
 'permissions': '원본의 CRM·관리자 영역 구분을 통합 권한 목록과 조건으로 확인하는 시안입니다. 실제 접근 권한은 변경하지 않았습니다.'
}
for s in tab_screens:
    route = 'activity' if s['route']=='activity-original' else s['route']
    key = s['id'].split('--')[-1]
    src = source_tab_lookup.get((route,key))
    if s['route']=='marketing': src=source_tab_lookup.get(('marketing','register'))
    appendix.append(dict(route=route,title=s['title'],tab=s['tab'],to=ROOT/'docs/screens/tabs'/(s['filename']+'.png'),before=src,
                         before_label='원본 내부 화면' if src else '원본 페이지 · 대응 탭은 별도 구성',intent=tab_intents.get(s['route'],tab_intents[route])))
tab_lookup = {(s['route'],s['id'].split('--')[-1]): ROOT/'docs/screens/tabs'/(s['filename']+'.png') for s in tab_screens}
for route in ['customers','nonprofits']:
    for key,dest in [('companyTabButton',tab_lookup[(route,'detail')]),('contactTabButton',screens['contacts']),('activityTabButton',tab_lookup[('activity','history')])]:
        s=next(s for s in source_tabs if s['route']==route and s['key']==key)
        appendix.append(dict(route=route,title=next(p['title'] for p in pages if p['id']==route),tab='원본 '+s['tab']+' → 연결 화면',to=dest,before=source_tab_lookup[(route,key)],before_label='원본 내부 탭',intent=tab_intents[route]))
for route,key,dest in [('marketing','history',screens['marketing']),('permissions','member',screens['permissions'])]:
    s=next(s for s in source_tabs if s['route']==route and s['key']==key)
    appendix.append(dict(route=route,title=next(p['title'] for p in pages if p['id']==route),tab='원본 '+s['tab']+' → 연결 화면',to=dest,before=source_tab_lookup[(route,key)],before_label='원본 내부 탭',intent=tab_intents[route]))
TOTAL_PAGES = 50 + len(appendix) + 2
if PUBLIC:
    source_images = {}
    for a in appendix: a['before']=None; a['before_label']='관찰한 구성 관계 도식 · 원본 캡처 비공개'

# Each tuple is: focus, observed structure, implemented change, intended benefit.
# Benefits are hypotheses, not measured task-time or error-rate outcomes.
changes = {
'activity': [
 ('입력 순서', '좁은 기본 정보 칸에 제목·결과·후속 업무·품목·첨부가 길게 이어짐.', '기본 정보 → 활동 내용 → 처리 결과·다음 행동으로 구분. 첨부는 상담 내용 가까이 배치.', '관련 항목을 함께 찾고, 상담 기록에서 후속 업무로 자연스럽게 이어서 작성하도록 설계.'),
 ('고객·저장 맥락', '고객 정보 표와 하단 등록 버튼으로 대상 고객·완료 동작을 확인.', '회사 아이콘으로 고객 요약 표시. 선택선 대신 배경으로 구분하고 저장 버튼 분리.', '작성 대상과 다음 동작을 계속 확인하도록 설계. 탭의 카드 내부 배치는 기존 구조를 유지한 부분.')],
'home': [
 ('실행 우선 요약', '오늘의 업무·고객 관리·최근 활동·지표·지도·추천이 세로로 이어짐.', '업무·영업·계약 요약을 상단에 모으고 관련 목록·실행 영역으로 연결.', '첫 화면에서 무엇부터 확인할지 판단하고 실제 처리 화면으로 이어지도록 설계.'),
 ('정보 위계', '영업 요약과 고객 추천 등 여러 정보를 한 진입 화면에서 확인.', '카드별 위계·입체 장식 정리. 바로가기 제목·설명 시작점과 화살표 위치 통일.', '업무 정보의 읽는 순서를 명확하게 하고 장식이 데이터와 경쟁하지 않도록 조절.')],
'customers': [
 ('목록과 상세', '많은 고객 정보 열과 상세·등록·수정 경로를 제공.', '핵심 열을 우선 표시하고 추가 열 선택·상세 패널로 정보 분리.', '목록에서는 고객을 비교하고 상세에서는 한 고객의 맥락을 확인하도록 설계.'),
 ('후속 업무 연결', '검색 조건, 고객 정보와 관련 영업활동을 각각 확인.', '기본·상세 필터를 유지하고 상세에 정보·이력·수정·활동 기록을 묶음.', '고객을 찾은 뒤 정보를 다시 탐색하는 부담을 줄이려는 구성.')],
'nonprofits': [
 ('설립·예산 정보', '고객 정보와 설립·예산·알림 관련 항목을 함께 관리.', '설립 단계·예산 편성 시기·알림 주기를 독립된 입력 묶음으로 배치.', '기관별 영업 시점에 필요한 항목을 빠뜨리지 않고 함께 확인하도록 설계.'),
 ('목록의 우선순위', '기관 정보와 여러 관리 조건을 목록에서 조회.', '설립·예산 관련 핵심 열을 먼저 비교하고 나머지는 상세로 연결.', '기관의 현재 상황과 담당 업무를 같은 맥락에서 판단하도록 설계.')],
'news': [
 ('기사와 고객', '영리·비영리 뉴스 조회 및 고객 연결 조건을 제공.', '기사에 연계 고객과 기회 유형을 함께 배치.', '뉴스의 영업 의미를 파악하는 데 필요한 고객 맥락을 같은 화면에서 제공.'),
 ('관심과 후속 업무', '기사 목록을 조회하고 고객 연결 내용을 확인.', '관심 기사와 후속 업무로 이어지는 동작을 기사 가까이에 배치.', '정보 확인이 고객 접촉 준비로 이어지도록 설계. 수집·발송은 서버 연결 대상.')],
'contacts': [
 ('편집 영역', '넓은 연락처 목록의 행 안에 여러 편집 요소가 함께 있음.', '핵심 연락 정보를 목록에 남기고 편집은 상세 패널로 이동.', '비교와 편집의 목적을 구분해 목록의 읽기 흐름을 유지하도록 설계.'),
 ('담당자 맥락', '소속·연락처·재직 관련 항목을 여러 열에서 확인.', '소속·연락·이직·퇴사 정보와 메일 후속 동작을 연결.', '잘못된 연락 대상이나 오래된 소속 정보가 있는지 함께 확인하도록 설계.')],
'upload': [
 ('진행 단계', '파일 선택·열 매핑·데이터 반영으로 업로드를 진행.', '파일 → 항목 → 검증 → 결과의 네 단계로 표시.', '현재 단계와 다음에 필요한 작업을 알아볼 수 있도록 설계.'),
 ('반영 전 확인', '업로드 파일과 매핑할 항목을 지정하는 구조.', '반영 전에 필수값·오류 행의 샘플 검증 결과를 표시.', '잘못된 자료를 확인할 기회를 제공. 실제 서버 검증과 반영 규칙은 별도 연결 필요.')],
'tasks': [
 ('업무의 기한', '업무 등록과 기한·상태별 목록 조회를 제공.', '기한 경과·오늘·예정·완료로 구분하고 보기 방식을 별도 그룹으로 배치.', '업무 상태와 표시 방식을 혼동하지 않고 처리 대상을 좁히도록 설계.'),
 ('조회와 등록', '새 업무 등록 영역과 업무 목록이 함께 표시됨.', '필요할 때 등록 폼을 열고 목록·보드·달력으로 같은 업무를 확인.', '목록을 확인할 공간을 확보하면서 사용 목적에 맞는 보기 방식을 제공.')],
'leads': [
 ('응답 우선순위', '문의 고객·배정 담당자·진행 상태를 목록에서 관리.', '문의·배정·우선순위·응답기한을 같은 행에서 비교.', '어떤 문의에 먼저 응답할지 판단할 정보를 가까이 배치.'),
 ('첫 연락 연결', '문의 내용과 고객 정보·연락처를 확인.', '리드 상세에서 문의를 확인하고 첫 연락 업무를 생성하는 경로 제공.', '문의 확인 이후의 다음 동작을 명확하게 제시. 실제 업무 저장은 서버 연결 대상.')],
'quotes': [
 ('견적 비교', '고객·담당자·제품 조건과 견적 활동을 목록으로 조회.', '금액·제품·상태 요약을 먼저 표시하고 조건과 상세를 연결.', '견적의 핵심 차이를 목록에서 판단하고 필요한 상담 맥락으로 이동하도록 설계.'),
 ('상세 맥락', '견적 내역에 상담·금액·첨부 관련 정보가 함께 있음.', '상세에서 상담 내용·금액·첨부를 함께 확인.', '견적 수치만 보고 판단하지 않도록 관련 설명과 자료를 가까이 배치.')],
'marketing': [
 ('입력 묶음', '대상 고객·마케팅 활동·내용·리드 관련 값을 입력.', '대상 고객 / 활동 정보 / 내용·리드의 세 묶음으로 구분.', '누구에게 무엇을 했고 어떤 반응이 있었는지 순서대로 작성하도록 설계.'),
 ('대상 구분', '고객과 마케팅 유형·리드 항목을 함께 지정.', '기존·신규 대상을 구분하고 단계·점수를 활동 맥락에 연결.', '대상 선택과 결과 기록의 관계를 명확하게 보여주도록 설계.')],
'yearly': [
 ('집계의 기준', '기간·담당자·활동 조건에 따른 집계와 상세 목록을 제공.', '조건·요약·추이·목록을 같은 조회 기준으로 표시.', '보고 있는 수치가 어떤 조건에서 나온 것인지 함께 이해하도록 설계.'),
 ('요약과 원본', '영업 집계 및 상세 활동 내역을 조회.', '요약 수치에서 추이와 관련 활동 목록을 이어서 확인.', '큰 흐름을 파악한 뒤 상세 내역을 확인하는 검토 순서를 지원.')],
'activity-detail': [
 ('조회 범위', '활동 유형·업체별 영업 내역과 관련 금액을 조회.', '활동 유형·거래처·상태 조건으로 좁힌 목록을 제공.', '찾고 있는 활동의 조건과 조회 결과를 가까이 배치.'),
 ('상담과 금액', '활동 내용과 관련 금액 항목을 확인.', '상세 상담·라이선스·교육비·총액을 연결해 확인.', '활동의 의미와 금액을 같은 맥락에서 판단하도록 설계.')],
'ai': [
 ('추천의 맥락', '영업 기록을 바탕으로 추천·분석을 확인하는 전용 영역.', '추천 고객과 기록 근거를 함께 보여주는 전용 화면으로 정리.', '추천을 그대로 따르기 전에 왜 제시됐는지 확인할 수 있도록 설계.'),
 ('후속 업무', '추천·분석 정보를 조회.', '우선 고객 확인에서 후속 업무 준비로 이어지는 동작 제공.', '분석 확인 이후의 실행 경로를 명확하게 표시. 실제 AI 생성·품질 검증은 별도 대상.')],
'work-report': [
 ('기록과 보고', '활동 내역과 여러 보고 항목을 작성·조회.', '담당자별 활동 내역과 일지 메모를 함께 표시.', '기록을 참고하며 보고를 작성하도록 정보 사이의 거리를 줄이려는 구성.'),
 ('선보고 초안', '일지·이슈·미수행 등 보고 항목과 선보고 경로를 제공.', '조회한 활동과 메모를 바탕으로 선보고 초안을 구성.', '보고를 작성할 출발점을 제공. 초안은 검토 대상이며 실제 메시지 발송은 연결되지 않음.')],
'custom-reports': [
 ('구성과 결과', '보고 대상·그룹·집계 기준을 선택해 보고서를 구성.', '구성 패널과 샘플 집계 결과를 나란히 제공.', '조건을 바꾸었을 때 결과가 어떻게 달라지는지 알아보도록 설계.'),
 ('반복 보고', '선택한 기준에 따라 보고서를 생성·조회.', '월별 교차 표와 저장한 보고서 불러오기 제공.', '반복해서 쓰는 구성의 재사용을 지원. 실제 집계·저장 규칙은 서버 연결 필요.')],
'ssl-master': [
 ('기준정보의 구분', 'SSL 품목·공급사·갱신 관련 기준정보를 관리.', '같은 관리 카드 안에서 품목·공급사·갱신주기를 탭으로 구분.', '관리 대상이 달라도 조회·등록 동작의 위치를 일관되게 제공.'),
 ('공통 관리 동작', '대상별 기준정보 항목을 각각 관리.', '동일한 목록·상태·등록 규칙을 반복 사용.', '관리 대상마다 조작 방식을 다시 익히는 부담을 줄이려는 구성.')],
'ssl-purchase': [
 ('발주와 품목', '발주 정보와 품목별 수량·단가·세액을 입력.', '발주 기본 정보와 품목별 발주를 하나의 폼 안에서 구분.', '한 발주에 속하는 정보임을 유지하면서 작성 순서를 명확하게 표시.'),
 ('합계 확인', '품목별 금액과 발주 합계 관련 항목을 관리.', '수량·단가·부가세와 합계를 같은 입력 흐름에서 확인.', '입력한 값과 총액의 관계를 확인하도록 설계. 실제 세금·반올림 규칙은 별도 확정 필요.')],
'ssl-delivery': [
 ('출고 맥락', '출고·설치·고객·도메인·인증서 정보를 관리.', '고객 목록에서 설치·출고·도메인·인증서 상세로 연결.', '한 고객의 인증서와 처리 상태를 함께 알아보도록 설계.'),
 ('핵심 열', '인증서 관련 여러 항목을 목록과 입력 영역에서 확인.', '주요 일정·상태를 목록에서 비교하고 나머지는 상세에서 확인.', '비교할 정보와 개별 확인 정보를 구분해 넓은 표의 부담을 줄이려는 구성.')],
'ssl-expiration': [
 ('갱신 우선순위', '만료 정보·갱신 대상·알림 조건을 조회.', '만료일·잔여일·알림 구간을 먼저 표시.', '어떤 인증서를 먼저 확인할지 판단할 정보를 우선 제공.'),
 ('확인에서 갱신', '만료·갱신·알림 관련 항목을 관리.', '확인 상태와 갱신 폼을 목록의 상세 흐름에 연결.', '만료 확인 이후의 조치로 이어지도록 설계. 알림 발송과 실갱신은 연결 대상.')],
'forecast-add': [
 ('계약 입력 순서', '고객·제품·비용·예정일·이월 항목을 등록.', '고객·계약 / 금액·일정 / 이월 관리로 입력을 묶음.', '어떤 계약인지, 얼마인지, 언제인지 순서대로 기록하도록 설계.'),
 ('금액과 이월', '라이선스·교육비 및 이월 관련 값을 입력.', '라이선스+교육비 합계를 표시하고 이월 정보를 별도 묶음으로 구분.', '금액 구성과 이월 사유를 서로 다른 판단 정보로 확인하도록 설계.')],
'forecast-status': [
 ('월별 반복', '월별 예상 계약·이월·달성 관련 표가 반복됨.', '하나의 목록과 기간 필터, 전체·이월·달성 탭으로 통합.', '여러 표를 오가며 비교하는 대신 같은 구조에서 조건을 바꿔 확인하도록 설계.'),
 ('비교 기준', '월별 계약 및 이월·달성 항목을 확인.', '같은 열과 조회 조건으로 계약 상태를 비교.', '기간과 상태에 따른 결과의 차이를 이해하도록 기준을 일관되게 제공.')],
'other-add': [
 ('일관된 입력', '기타 계약의 고객·금액·일정·이월 정보를 등록.', '포캐스팅과 같은 고객·계약 / 금액·일정 / 이월 입력 규칙 적용.', '계약 종류가 바뀌어도 작성 방식을 다시 익히지 않도록 설계.'),
 ('정보 묶음', '계약 관련 여러 항목을 한 등록 화면에서 입력.', '기본 정보와 금액·일정·이월을 의미별로 분리.', '관련 항목을 함께 찾고 작성 상태를 확인하도록 설계.')],
'other-status': [
 ('현황 비교', '기타 계약의 월별 예상·이월·달성을 조회.', '기간·상태 조건과 통합 목록으로 비교.', '다른 계약 현황 화면과 같은 방식으로 조회하도록 설계.'),
 ('공통 상태 표시', '계약 일정과 진행 관련 값을 확인.', '일반 포캐스팅과 같은 탭·열·상태 라벨 규칙 사용.', '동일한 상태를 화면마다 다르게 해석하지 않도록 일관된 표현 제공.')],
'admin': [
 ('관리 목적별 탐색', '계정·권한·조직·기준정보·운영 설정 메뉴를 제공.', '계정·조직 / 기준정보 / 운영 설정으로 관리 메뉴를 분류.', '하려는 관리 업무의 목적을 기준으로 메뉴를 찾도록 설계.'),
 ('공통 화면 틀', '여러 관리 기능으로 이동하는 관리자 진입 화면.', '관리 항목·요약 카드에 기능별 아이콘 적용. 좌측 메뉴와 같은 아이콘 사용.', '일반 업무에서 관리 업무로 이동해도 조작 위치를 예측하도록 설계.')],
'members': [
 ('회원 맥락', '회원 정보·담당 업무·재직 여부와 설정을 관리.', '회원 정보·담당 업무·재직 상태를 하나의 목록과 상세에 통합.', '누가 어떤 업무를 맡고 있는지 함께 확인하도록 설계.'),
 ('상세 설정', '회원 관련 여러 관리 항목을 확인·수정.', '업무별 설정을 상세 패널에서 제공.', '목록의 비교 흐름을 유지하면서 필요한 계정 설정에 접근하도록 설계.')],
'transfer': [
 ('변경 전후 확인', '고객을 선택하고 기존·변경 담당자를 지정.', '대상 고객과 현재·새 담당자를 같은 화면에서 비교.', '변경 대상과 방향을 알아보고 잘못된 이관을 예방하려는 구성.'),
 ('조건과 대상', '고객 선택 조건 및 담당자 이관 기능을 제공.', '검색·선택한 고객 목록과 담당자 지정 흐름을 연결.', '선택 범위를 확인하고 다음 입력으로 이어지도록 설계. 실제 이관은 수행하지 않음.')],
'permissions': [
 ('설정 맥락', '역할별로 접근할 페이지를 선택·관리.', '역할 선택과 해당 페이지 목록을 같은 설정 흐름으로 배치.', '어떤 역할의 권한을 편집 중인지 계속 확인하도록 설계.'),
 ('선택 상태', '페이지 접근 대상의 선택 상태를 관리.', '페이지 목록의 선택 상태와 저장 동작을 공통 패턴으로 제공.', '설정 범위와 변경 동작을 명확하게 표시. 실제 권한 정책은 서버 단계에서 검증 필요.')],
'departments': [
 ('조직 비교', '부서 목록과 소속 정보를 관리.', '부서와 소속 인원을 같은 표에서 비교.', '부서별 인원 맥락을 함께 확인하도록 설계.'),
 ('목록 공간', '부서 조회와 신규 등록 경로를 제공.', '조회는 목록에 집중하고 등록 폼은 필요할 때 열기.', '조회와 등록의 목적에 따라 화면을 사용할 수 있도록 설계.')],
'department-add': [
 ('등록 범위', '부서 기본 정보를 입력하는 별도 등록 화면.', '부서 정보만 남긴 공통 폼 구조로 정리.', '짧은 등록 작업에 필요한 입력과 완료 동작을 명확하게 제공.'),
 ('등록 이후', '부서 신규 등록 경로를 제공.', '등록 후 부서 관리 목록으로 이어지는 흐름 제공.', '입력 완료 이후 어디서 결과를 확인할지 알 수 있도록 설계.')],
'goals': [
 ('기간과 담당자', '사원별 월 목표·연간 목표를 표에서 관리.', '연도 전환과 사원별 월 목표 입력을 같은 표에 배치.', '어느 기간·담당자의 목표인지 확인하며 입력하도록 설계.'),
 ('합계 확인', '월 목표와 연간 목표 관련 값을 관리.', '월별 값의 연간 합계를 샘플 계산으로 표시.', '개별 입력과 전체 목표의 관계를 확인하도록 설계. 서버 계산 규칙은 별도 확정 필요.')],
'manage-items': [
 ('항목과 선택값', '관리 항목과 해당 선택값을 등록·관리.', '항목 이름과 선택값을 한 입력 화면에서 연결.', '선택값이 어느 관리 항목에 속하는지 알아보도록 설계.'),
 ('관리 방식', '여러 관리 항목의 등록·관리 경로를 제공.', '공통 목록·입력 규칙으로 항목 관리를 정리.', '반복 관리 작업에서 입력 위치와 동작을 예측하도록 설계.')],
'institutions': [
 ('분류의 사용 맥락', '고객 분류에 쓰는 기관유형 항목을 관리.', '기관유형과 사용 고객사 수·상태를 함께 표시.', '분류 항목의 사용 맥락을 확인하도록 설계. 실제 영향 범위는 서버 데이터로 검증 필요.'),
 ('공통 관리 패턴', '기관유형 선택 항목을 등록·관리.', '목록·상세·등록을 기준정보 공통 규칙으로 구성.', '다른 기준정보 관리 화면과 같은 방식으로 작업하도록 설계.')],
'acquisition': [
 ('분류 관계', '소스출처·인입경로 등 유입 분류 정보를 관리.', '소스출처와 인입경로의 상위 관계를 표시.', '이름만 보고 분류하는 대신 어느 경로에 속하는지 함께 이해하도록 설계.'),
 ('등록 맥락', '유입 관련 선택 항목을 등록·관리.', '상위 분류·항목명·유형·사용 상태를 하나의 입력 묶음으로 정리.', '분류 관계를 확인하며 새 항목을 작성하도록 설계.')],
'commercial-news': [
 ('수집과 노출', '뉴스 수집 사용·순서·키워드 기준을 관리.', '수집 사용·노출 순서·키워드를 같은 관리 목록으로 정리.', '수집 여부와 표시 순서가 서로 다른 설정임을 알아보도록 설계.'),
 ('설정 위치', '뉴스 관련 기준정보를 등록·관리.', '검색·목록·등록을 공통 관리 패턴으로 구성.', '일반 기준정보 관리와 같은 조작 위치를 유지. 실제 수집 동작은 연결 대상.')],
'nonprofit-keywords': [
 ('업무 관련 키워드', '비영리 뉴스 수집 키워드와 사용 상태를 관리.', '기관 설립·예산 관련 키워드와 수집 상태를 함께 확인.', '어떤 영업 정보에 연결되는 키워드인지 이해하도록 설계.'),
 ('관리 방식', '키워드를 등록하고 사용 여부를 관리.', '영리 뉴스와 동일한 목록·등록·상태 규칙 사용.', '뉴스 종류가 달라도 관리 방식을 일관되게 제공.')],
'products': [
 ('품목과 옵션', '품목명·코드·사용 여부를 관리.', '품목명·코드·활성 상태와 옵션 수를 함께 비교.', '품목을 식별하고 연결된 옵션의 존재를 알아보도록 설계.'),
 ('기준정보 입력', '제품 품목의 등록·관리 경로를 제공.', '품목 정보 입력과 상태를 공통 상세·폼 패턴으로 정리.', '다른 기준정보와 동일한 작성 규칙을 제공.')],
'product-options': [
 ('소속 품목', '품목에 연결된 옵션과 옵션 코드를 관리.', '제품별 옵션·코드·활성 상태를 연결해 표시.', '옵션이 어느 품목에 속하는지 확인하고 선택하도록 설계.'),
 ('관리 흐름', '품목옵션의 등록·관리 경로를 제공.', '품목 선택과 옵션 정보 입력을 공통 관리 폼으로 정리.', '상위 품목을 확인하며 옵션을 작성하도록 설계.')],
'options-upload': [
 ('등록 단계', '품목옵션 파일로 일괄등록.', '파일 선택 → 항목 확인 → 검증 → 결과의 단계로 표시.', '현재 단계와 반영 전에 확인할 내용을 알아보도록 설계.'),
 ('반영 전 검증', '파일 기반 옵션 등록 경로를 제공.', '필수값·오류 행·반영 결과를 샘플 검증 화면에서 구분.', '자료를 확인하고 수정할 기회를 제공. 실제 서버 검증·일괄 반영은 별도 연결 필요.')],
'marketing-types': [
 ('사용 상태', '마케팅 활동유형과 사용 여부를 관리.', '활동유형 이름·상태·등록 정보를 같은 목록에서 확인.', '새 유형을 추가하기 전에 기존 항목과 사용 상태를 비교하도록 설계.'),
 ('입력 일관성', '활동유형 등록·수정 경로를 제공.', '기준정보 공통 목록·등록·수정 패턴을 재사용.', '유형 관리마다 다른 방식으로 조작하는 부담을 줄이려는 구성.')],
'work-settings': [
 ('대상의 구분', '업무일지 표시 대상·선보고 수신 대상을 설정.', '표시 대상과 수신 대상의 설정 영역을 분리.', '누가 화면에 표시되고 누가 보고를 받는지 구분하도록 설계.'),
 ('선택과 완료', '대상 관련 여러 운영 설정을 관리.', '각 대상 선택 상태와 저장 동작을 같은 규칙으로 제공.', '설정 대상과 완료 동작을 명확하게 표시. 실제 수신·발송 설정은 변경하지 않음.')],
'system': [
 ('브랜드와 운영', '브랜드·로그인 이미지·운영 알림 값을 설정.', '브랜드 이미지와 알림 수신 정보를 별도 묶음으로 구분.', '화면 외형과 알림 운영이 서로 다른 설정임을 알아보도록 설계.'),
 ('이미지 확인', '브랜드 및 로그인 관련 이미지 설정을 제공.', '로고·로그인 이미지 미리보기를 입력 가까이에 배치.', '선택한 이미지의 용도를 확인하도록 설계. 운영 파일 업로드·설정 반영은 수행하지 않음.')],
'migration': [
 ('별도 제안', '원본을 열지 않아 기존 배치·실행 규칙을 확인하지 않음.', '샘플 중복·필수값 검증을 보여주는 별도 제안 시안.', '확인하지 않은 원본에 대한 개선 효과를 주장하지 않고 제안 범위를 명확하게 표시.'),
 ('확인 후 연결', '운영 데이터 이동의 규칙과 예외는 미확인.', '검증 결과와 처리 단계를 예시로 제공.', '실제 마이그레이션 설계 전에 자료·중복·권한 규칙을 확인할 출발점을 제공.')],
'login': [
 ('인증 입력', '브랜드와 아이디·비밀번호, 계정 찾기·가입 경로를 제공.', '브랜드 소개와 인증 영역을 구분하고 입력에 지속 레이블 적용.', '입력 중에도 각 칸의 의미를 확인하고 인증 작업에 집중하도록 설계.'),
 ('보조 경로', '아이디 저장·비밀번호 찾기·회원가입을 제공.', '인증 버튼과 보조 경로의 우선순위를 구분.', '로그인에 필요한 동작과 계정 문제 해결 경로를 알아보도록 설계. 실제 인증은 연결되지 않음.')]
}
assert set(changes) == {p['id'] for p in pages}
ordered = sorted(pages, key=lambda p: 0 if p['id'] == 'activity' else 1)
for name in ['Regular', 'Bold']:
    pdfmetrics.registerFont(TTFont('PR' + name, str(OUT / 'fonts' / ('Pretendard-' + name + '.ttf'))))

W, H, M, GAP = 1440, 1400, 48, 24
CW = W - 2 * M
COL = (CW - GAP) / 2
INK, MUTED, BLUE, LINE, BG = '#18243A', '#576579', '#1A3C83', '#CAD2DE', '#F7F8FA'
pdf = ROOT/'docs/CRM-Renewal-As-Is-To-Be.pdf' if PUBLIC else OUT / 'CRM-UX-As-Is-To-Be-Review.pdf'
c = canvas.Canvas(str(pdf), pagesize=(W, H), pageCompression=1)
c.setTitle('IONE CRM - 페이지별 UX As-Is / To-Be 비교')
c.setAuthor('IONE CRM Renewal')
c.setSubject('현재 v5.5 구현과 기존 화면의 UX 비교. 사용성 개선율은 미측정.')
qa = []
layout_regions = []
layout_page = 0

def overlaps(a, b):
    return min(a[2], b[2])-max(a[0], b[0]) > 1 and min(a[3], b[3])-max(a[1], b[1]) > 1

def record_text(rect, value):
    if rect[0] < M-1 or rect[2] > W-M+1 or rect[1] < 19:
        raise ValueError(f'Page {layout_page}: text exceeds page margin: {value}')
    for kind, region, _ in layout_regions:
        if kind == 'image' and overlaps(rect, region):
            raise ValueError(f'Page {layout_page}: text overlaps an image: {value}')
        if kind == 'text' and overlaps(rect, region):
            raise ValueError(f'Page {layout_page}: text overlaps earlier text: {value}')
    layout_regions.append(('text', rect, value[:90]))

def protect_text(rect, kind):
    for region_kind, region, value in layout_regions:
        if region_kind == 'text' and overlaps(rect, region):
            raise ValueError(f'Page {layout_page}: {kind} covers earlier text: {value}')

def text(value, x, y, size=18, color=INK, bold=False):
    font = 'PR' + ('Bold' if bold else 'Regular')
    ascent, descent = pdfmetrics.getAscentDescent(font, size)
    record_text((x, y+descent, x+pdfmetrics.stringWidth(value, font, size), y+ascent), value)
    c.setFont(font, size)
    c.setFillColor(HexColor(color))
    c.drawString(x, y, value)

def para(value, x, top, width, size=18, color=INK, bold=False, max_h=None):
    style = ParagraphStyle('p', fontName='PR' + ('Bold' if bold else 'Regular'), fontSize=size,
                           leading=size * 1.55, textColor=HexColor(color), wordWrap='CJK')
    p = Paragraph(html.escape(value).replace('\n', '<br/>'), style)
    _, height = p.wrap(width, H)
    if max_h is not None and height > max_h and size == 16:
        style.fontSize = 14
        style.leading = 21
        p = Paragraph(html.escape(value).replace('\n', '<br/>'), style)
        _, height = p.wrap(width, H)
    if max_h is not None and height > max_h:
        raise ValueError(f'Text exceeds box ({height:.1f} > {max_h}): {value}')
    record_text((x, top-height, x+width, top), value)
    p.drawOn(c, x, top - height)
    qa.append({'text': value[:70], 'height': round(height, 2), 'bottom': round(top-height, 2)})
    return height

def box(x, y, width, height, fill='#FFFFFF', radius=12):
    protect_text((x, y, x+width, y+height), 'card')
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(LINE))
    c.roundRect(x, y, width, height, radius, fill=1, stroke=1)

def image_fit(source, x, bottom, width, height, align_top=True, forced_width=None):
    with Image.open(source) as im:
        iw, ih = im.size
    scale = min(width / iw, height / ih)
    if forced_width is not None:
        scale = forced_width / iw
    sw, sh = iw * scale, ih * scale
    assert sw <= width + .01 and sh <= height + .01
    y = bottom + height - sh if align_top else bottom + (height - sh) / 2
    protect_text((x+(width-sw)/2, y, x+(width+sw)/2, y+sh), 'image')
    layout_regions.append(('image', (x+(width-sw)/2, y, x+(width+sw)/2, y+sh), str(source)))
    c.drawImage(str(source), x + (width - sw) / 2, y, width=sw, height=sh, mask='auto')
    return sw, sh

def base(number, label):
    global layout_page
    layout_page = number
    layout_regions.clear()
    c.setFillColor(HexColor(BG)); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.drawImage(str(ROOT / 'assets/logo.png'), M, H-69, width=112, height=40.52, mask='auto')
    text('CRM / UX REVIEW', M+134, H-45, 14, MUTED, True)
    text('2026.10.06', W-M-105, H-45, 14, MUTED)
    c.setStrokeColor(HexColor(LINE)); c.line(M, 57, W-M, 57)
    text(label, M, 30, 12, MUTED)
    text(f'{number:02d} / {TOTAL_PAGES}', W-M-94, 30, 12, MUTED)

def page_title(title, subtitle):
    text(title, M, H-120, 32, INK, True)
    text(subtitle, M, H-155, 16, MUTED)

base(1, 'OVERVIEW / v5.5 / PAGE UX COMPARISON')
text('화면을 정리한 이유까지,', M, 1220, 48, INK, True)
text('페이지별로 비교합니다.', M, 1150, 48, INK, True)
para('44개 페이지의 UX 비교 + 내부 탭·연결 화면 부록\nAS-IS / TO-BE / 변경 내용 / 개선 의도\n회사·사용자 아이콘 · 선택선 제거 · 정렬·OG 갱신', M, 1095, 650, 23, MUTED)
box(M, 620, 620, 310)
text('이 문서에서 비교하는 내용', M+24, 886, 23, BLUE, True)
para('① 기존 화면과 최종 시안의 페이지별 비교\n② 변경 내용과 개선 의도의 간략한 설명\n③ 내부 탭·상세 패널·등록창까지 포함한 부록\n\n고객 찾기, 상담 기록, 다음 행동 확인 등 실제 업무 흐름에 따라 달라진 부분을 정리합니다.', M+24, 850, 572, 20, max_h=212)
box(M, 292, 620, 298)
text('비교 이미지의 출처', M+24, 548, 23, BLUE, True)
para(('공개판: 원본은 관찰한 구성 관계의 도식으로 표시\n원본 캡처 포함 비교 PDF는 별도 로컬 파일로 제공\n' if PUBLIC else 'CRM 42개 화면: 로그인 후 실제 원본 전체 캡처\n로그인: 보관된 실제 원본 캡처\n')+'리뉴얼: 기본 45장 + 탭·상세·등록창 42장\n마이그레이션: 원본 미열람, 별도 제안\n\n1920px 브라우저 폭에서 촬영하고 원본 화소를 유지합니다. 캡처 JPEG를 확대 없이 PNG로 내보냈습니다. PDF 설명은 벡터 텍스트입니다.', M+24, 510, 572, 18, max_h=210)
image_fit(screens['activity'], 710, 260, 675, 830)
text('영업활동관리부터 시작하는 전체 44개 페이지 리뷰', M, 194, 22, INK, True)
para('실제 원본 화면과 일반 UX 원칙을 연결한 설계 설명입니다. 실제 사용자 업무시간·누락·오류의 개선 정도는 아직 측정하지 않았습니다.', M, 153, CW, 18, MUTED)
c.showPage()

base(2, 'UX CHANGES / FINAL REVIEW')
page_title('최종 시안에서 달라진 사용 경험', '페이지별 상세 비교에 앞서, 공통으로 정리한 동작과 정보 표현을 살펴봅니다.')
rules = [
 ('업무 흐름에 따른 정보 묶음', '조회 조건, 목록, 선택 대상, 입력 내용과 다음 행동을 구분합니다. 고객·상담·계약의 맥락을 화면에서 계속 확인하도록 구성했습니다.'),
 ('현재 작업과 보기 방식 구분', '내부 탭은 해당 콘텐츠 카드 안에 배치했습니다. 업무의 상태 조회와 목록·보드·달력 보기 방식은 별도 그룹으로 구분합니다.'),
 ('명확한 대표 행동', '조회·등록·저장과 선택된 페이지 번호는 네이비 배경과 흰 글자로 표시합니다. 보조 버튼·링크는 본문 색상으로 정리해 대표 행동을 식별하도록 했습니다.'),
 ('라벨의 실제 의미 표시', '유입경로는 웹·캠페인·직접 입력 아이콘, 우선순위는 위·등호·아래, 접촉·유효·전환은 전화·확인 방패·이동 화살표로 구분합니다. 모호한 빼기·시계 표시는 제거했습니다.'),
 ('프로필과 탐색 항목의 구분', '이름 첫 글자 대신 회사·사용자 아이콘을 사용합니다. 관리자 메뉴는 기능별 아이콘으로 구분하고, 선택된 고객은 좌측 선 없이 배경으로 표시합니다.'),
 ('정렬과 좁은 화면에서의 읽기', '바로가기 제목·설명의 시작점을 맞추고 버튼 간 간격을 확보했습니다. 좁은 화면은 카드·폼을 재배치하고 표는 내부 스크롤로 정보를 보존합니다.')
]
y = 1205
for title, body in rules:
    box(M, y-164, CW, 164)
    text(title, M+24, y-36, 23, BLUE, True)
    para(body, M+24, y-66, CW-48, 22, max_h=84)
    y -= 178
c.showPage()

base(3, 'EVIDENCE / HOW TO READ THIS DOCUMENT')
page_title('관찰, 설계 의도, 검증 결과를 구분합니다.', '비교표의 “개선 의도”는 기대하는 사용 경험이며, 측정된 성과를 뜻하지 않습니다.')
items = [
 ('01  직접 확인한 근거', '사용자 제공 영업활동 캡처, 새로 촬영한 42개 CRM 실제 화면과 이전 분석의 제목·필드·선택지·표·버튼 기록을 사용합니다. 등록·수정·발송·업로드·권한 변경은 수행하지 않았습니다.'),
 ('02  현재 구현에서 확인한 변경', 'docs/pages.json, 페이지별 비교 기록과 v5.5 전체 화면 캡처를 대조했습니다. 입력 묶음·조건·상세 패널·탭·샘플 계산·로컬 동작을 설명합니다. 실제 서버 규칙과 운영 기능 실행은 확인하지 않았습니다.'),
 ('03  일반 UX 원칙', '관련 항목의 그룹화, 현재 상태 표시, 기억보다 화면에서 알아보기, 공통 동작의 일관성을 근거로 개선 의도를 작성합니다. 일반 원칙이 이 CRM의 업무 시간 단축을 직접 증명하지는 않습니다.'),
 ('04  아직 검증할 부분', '실제 영업 담당자에게 같은 작업을 기존·리뉴얼 화면에서 수행하게 하고 완료 시간·누락·오선택을 비교해야 합니다. 품목 접기처럼 추가 클릭이 생기는 변경도 함께 확인해야 합니다.'),
 ('05  이미지의 차이', '42개 CRM 화면은 로그인 후 실제 원본을 새로 촬영했습니다. 로그인은 로그인된 상태에서 대시보드로 이동하므로 보관된 캡처를 사용합니다. 원본 미열람인 마이그레이션은 제안 화면으로 구분합니다. 원본 자료를 등록·수정·발송하지 않았습니다.')
]
y = 1206
for title, body in items:
    box(M, y-178, CW, 178)
    text(title, M+24, y-39, 25, BLUE, True)
    para(body, M+24, y-73, CW-48, 22, max_h=92)
    y -= 194
text('참고 근거 / 문서와 웹에서 확인 가능한 원칙', M, 207, 22, INK, True)
refs = [('W3C · 텍스트 최소 대비', 'https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html'),
        ('NN/g · 폼 항목 그룹화', 'https://www.nngroup.com/articles/form-design-white-space/'),
        ('NN/g · 사용성의 기본 원칙', 'https://www.nngroup.com/articles/ten-usability-heuristics/')]
for i, (label, url) in enumerate(refs):
    y = 169-i*31
    text(label, M, y, 17, BLUE)
    text(url, M+280, y, 14, MUTED)
    c.linkURL(url, (M, y-5, W-M, y+19), relative=0)
c.showPage()

for n, subset in enumerate([ordered[:22], ordered[22:]], 4):
    base(n, 'CONTENTS / PAGE COMPARISON')
    page_title('페이지별 비교 목차', '영업활동관리를 우선 배치했습니다. 항목을 누르면 해당 비교 페이지로 이동합니다.')
    for i, p in enumerate(subset):
        y = 1203-i*46
        page_num = ordered.index(p)+6
        text(p['title'], M+12, y, 23, INK, True)
        text(p['group'], M+620, y, 17, MUTED)
        text(f'{page_num:02d}', W-M-38, y, 21, BLUE, True)
        c.linkRect('', p['id'], (M, y-11, W-M, y+31), relative=0, thickness=0)
        c.setStrokeColor(HexColor(LINE)); c.line(M, y-18, W-M, y-18)
    c.showPage()

def record_diagram(p, x, bottom, width, height):
    cp = comparison[p['id']]
    if p['id'] == 'migration':
        text('원본 미열람', x+22, bottom+height-54, 30, INK, True)
        para('운영 마이그레이션 화면은 확인하지 않았습니다.\n\n기존 배치와 실행 규칙에 대한 AS-IS 이미지나 개선 효과를 작성하지 않았습니다.', x+22, bottom+height-88, width-44, 23)
        return
    para('아래는 확인한 구성 관계의 도식입니다.\n원본의 위치·크기·스타일을 재현한 화면이 아닙니다.', x+20, bottom+height-16, width-40, 17, MUTED, max_h=62)
    cursor = bottom+height-101
    nodes = [('기존 화면의 역할', cp['as_is'])]
    filters = list(dict.fromkeys(f.get('label','') for f in p.get('filters',[])+p.get('extra',[]) if f.get('label')))
    if filters:
        nodes.append(('확인한 조회·검색 대상', ' · '.join(filters[:8]) + (' · …' if len(filters)>8 else '')))
    cols = [a['label'] if isinstance(a,dict) else str(a) for a in p.get('columns',[])]
    if cols:
        nodes.append(('유지한 관리 정보 / 대표 항목', ' · '.join(cols[:9]) + (' · …' if len(cols)>9 else '')))
    kept = cp['preserved']
    if kept and not cols:
        nodes.append(('유지한 입력·관리 대상', ' · '.join(kept[:9]) + (' · …' if len(kept)>9 else '')))
    nodes.append(('원본 확인 경로', p['source']))
    node_h = min(137, (height-136-(len(nodes)-1)*20)/len(nodes))
    for i, (label, body) in enumerate(nodes):
        box(x+20, cursor-node_h, width-40, node_h, '#F8FAFC', 8)
        text(label, x+36, cursor-31, 18, INK, True)
        para(body, x+36, cursor-48, width-72, 17 if label != '원본 확인 경로' else 14, max_h=node_h-55)
        cursor -= node_h+20
        if i < len(nodes)-1:
            c.setStrokeColor(HexColor(LINE)); c.line(x+width/2, cursor+20, x+width/2, cursor)
    para('출처: 기존 읽기 전용 화면 구조 기록과 페이지 대응 문서. 데이터 값은 이 도식에 포함하지 않았습니다.', x+22, bottom+52, width-44, 14, MUTED, max_h=47)

for idx, p in enumerate(ordered, 6):
    base(idx, p['group']+' / '+p['id'])
    c.bookmarkPage(p['id']); c.addOutlineEntry(p['title'], p['id'], 0, False)
    subtitle = '기존 구조와 현재 구현 시안의 비교 / 변경 내용과 개선 의도'
    if p['id']=='migration': subtitle = '원본 미열람 / 개선 전후의 효과 비교가 아닌 별도 제안'
    page_title(p['title'], subtitle)
    y, ch = 370, 838
    for x, head, note, active in [
        (M, 'AS-IS  /  개선 전', '원본 미열람' if p['id']=='migration' else '관찰한 구조의 도식 · 원본 캡처 비공개' if PUBLIC else '보관된 실제 원본 캡처' if p['id']=='login' else '로그인 후 실제 원본 전체 화면 캡처 · 2026.10.06', False),
        (M+COL+GAP, 'TO-BE  /  현재 리뉴얼 시안', '처음 구현한 단독 영업활동 시안 · v5.5' if p['id']=='activity' else 'v5.5 최종 화면 캡처', True)]:
        box(x, y, COL, ch)
        text(head, x+22, y+ch-36, 24, BLUE if active else INK, True)
        para(note, x+22, y+ch-52, COL-44, 15, MUTED, max_h=38)
        c.setStrokeColor(HexColor(LINE)); c.line(x, y+ch-84, x+COL, y+ch-84)
    image_area_h = ch-114
    if p['id'] in source_images:
        before = source_images[p['id']]
        after = screens[p['id']]
        with Image.open(before) as a, Image.open(after) as b:
            common_width = min(COL-32, image_area_h*a.width/a.height, image_area_h*b.width/b.height)
        image_fit(before, M+16, y+16, COL-32, image_area_h, forced_width=common_width)
        image_fit(after, M+COL+GAP+16, y+16, COL-32, image_area_h, forced_width=common_width)
    else:
        record_diagram(p, M+8, y+16, COL-16, image_area_h)
        image_fit(screens[p['id']], M+COL+GAP+16, y+16, COL-32, image_area_h)
    table_top = 344
    widths = [150, 358, 396, CW-904]
    heads = ['개선 항목', 'AS-IS / 기존', 'TO-BE / 변경 내용', '개선 의도 / 기대하는 경험']
    x = M
    for head, width in zip(heads, widths):
        para(head, x+12, table_top, width-24, 16, BLUE, True, 27)
        x += width
    row_top = table_top-38
    for row in changes[p['id']]:
        c.setFillColor(HexColor('#FFFFFF')); c.rect(M, row_top-86, CW, 86, fill=1, stroke=0)
        c.setStrokeColor(HexColor(LINE)); c.line(M, row_top, W-M, row_top)
        x = M
        for j, (value, width) in enumerate(zip(row, widths)):
            para(value, x+12, row_top-10, width-24, 16, INK if j!=3 else MUTED, j==0, max_h=76)
            x += width
        row_top -= 90
    kept = ' · '.join(comparison[p['id']]['preserved']) or '기존 화면의 관리 대상과 조회·등록 흐름'
    if len(kept)>150: kept=kept[:146]+' …'
    para('유지한 항목: '+kept, M, 116, CW, 13, MUTED, max_h=42)
    link = 'https://leejinho970715-star.github.io/CRM/?v=5.5#'+p['id']
    text('현재 웹 시안 열기  /  '+p['id'], M, 74, 13, BLUE)
    c.linkURL(link, (M, 68, M+500, 93), relative=0)
    text('일반 UX 원칙에 따른 설계 의도 · 실제 개선 성과 미측정', W-M-397, 74, 13, MUTED)
    c.showPage()

for n in range(2):
    base(50+n, 'CONTENTS / ALL TABS AND LINKED VIEWS')
    page_title('탭·상세·연결 화면 목차', '기본 화면만 캡처하지 않고, 내부 탭과 원본 탭의 연결 대상까지 비교합니다.')
    for i,a in enumerate(appendix[n*25:(n+1)*25]):
        y=1206-i*40
        para(a['title']+' / '+a['tab'], M+8, y, CW-90, 18, max_h=36)
        text(str(52+n*25+i), W-M-58, y-22, 18, BLUE, True)
        c.linkRect('', 'view-'+str(n*25+i), (M,y-36,W-M,y),relative=0,thickness=0)
        c.setStrokeColor(HexColor(LINE));c.line(M,y-37,W-M,y-37)
    c.showPage()

for i,a in enumerate(appendix):
    base(52+i, 'TAB VIEW / '+a['route'])
    c.bookmarkPage('view-'+str(i))
    page_title(a['title']+' / '+a['tab'], '내부 탭·상세·연결 화면의 실제 캡처 · 상태와 스크롤 위치를 파일명으로 구분')
    p=next(p for p in pages if p['id']==a['route'])
    before=a['before'] or source_images.get(a['route'])
    y,ch=352,866
    pending=False
    for x,label,note in [(M,'AS-IS / 기존 화면',a['before_label']), (M+COL+GAP,'TO-BE / 현재 시안',a['tab']+(' · 촬영 정렬 재점검 대기' if pending else ''))]:
        box(x,y,COL,ch)
        text(label,x+22,y+ch-36,24,BLUE if x>M else INK,True)
        para(note,x+22,y+ch-52,COL-44,15,MUTED,max_h=38)
    ih=ch-114
    if before:
        with Image.open(before) as b, Image.open(a['to']) as t:
            common=min(COL-32,ih*b.width/b.height,ih*t.width/t.height)
        image_fit(before,M+16,y+16,COL-32,ih,forced_width=common)
        image_fit(a['to'],M+COL+GAP+16,y+16,COL-32,ih,forced_width=common)
    else:
        record_diagram(p,M+8,y+16,COL-16,ih)
        image_fit(a['to'],M+COL+GAP+16,y+16,COL-32,ih)
    text('개선 내용 · 의도',M,302,24,INK,True)
    para(a['intent'],M,274,CW,23,max_h=112)
    para('왼쪽은 원본의 해당 탭 또는 대응 페이지, 오른쪽은 샘플 데이터 시안입니다. 같은 고객의 전후 데이터 비교나 기능 검증 결과를 의미하지 않습니다. 원본 탭이 없는 경우 새로 구성한 보기로 표시합니다.',M,146,CW,17,MUTED,max_h=62)
    text('화면별 개선 설명은 '+str(ordered.index(p)+6)+'쪽 · 변경의 기대 효과는 실제 작업으로 검증 필요',M,74,14,MUTED)
    c.showPage()

base(TOTAL_PAGES, 'VALIDATION / NEXT UX REVIEW')
page_title('실제 업무에서 검증할 다음 과제', '구현한 화면의 사용성 검증과 운영 연결 과제')
steps = [
 ('01  핵심 작업 시나리오 확인', '고객 조회·상담 등록·리드 배정·계약 현황 확인을 대표 작업으로 선정합니다. 업무별 필수값·상태 변경·다음 행동의 규칙을 실제 담당자와 확인합니다.'),
 ('02  영업활동에서 먼저 검토', '고객을 선택하고 상담 내용·처리 결과·다음 행동·기한을 기록하는 순서를 검토합니다. 선택 고객을 잘못 인식하거나 필수 항목을 놓치는 지점을 확인합니다.'),
 ('03  탐색과 라벨의 이해 확인', '리드의 유입경로·우선순위·상태를 구분해서 읽는지 확인합니다. 내부 탭과 보기 전환의 현재 위치, 저장·조회 버튼과 선택된 페이지 번호도 함께 검토합니다.'),
 ('04  반응형과 접근성 확인', '새 스타일 적용 후 320·390·600·820·1024·1280·1600·1920px에서 전체 화면의 가로 넘침을 확인했습니다. 상태 라벨 글자 대비는 모두 4.5:1 이상입니다. 정식 WCAG 감사를 완료한 결과는 아니며 키보드·스크린리더·오류 예외도 별도 검증이 필요합니다.'),
 ('05  실제 작업으로 검증', '같은 고객과 상담 시나리오로 고객 찾기 → 상담 입력 → 품목 선택 → 다음 행동·기한 입력 → 저장을 수행합니다. 순서 효과를 줄이도록 기존·리뉴얼 사용 순서를 바꾸어 완료 시간·누락·오선택을 비교합니다. 숙련자의 적응 부담과 품목 접기의 추가 클릭도 확인합니다.')
]
y = 1204
for title, body in steps:
    box(M, y-177, CW, 177)
    text(title, M+24, y-39, 25, BLUE, True)
    para(body, M+24, y-73, CW-48, 22, max_h=108)
    y -= 190
para('이 문서는 현재 시안의 설명과 디자인 방향 검토용입니다. 서버 저장·인증·발송·수집·권한·마이그레이션은 연결하지 않았으며 운영 CRM을 변경하지 않았습니다. 최신 수정본의 PNG 87장을 다시 촬영·정리했습니다. 고정 메뉴는 최상단 위치를 확인하고, PDF 설명·이미지·비교 카드의 영역이 겹치지 않는지 검사했습니다.', M, 163, CW, 17, MUTED, max_h=92)
c.save()
reader = PdfReader(str(pdf))
assert len(reader.pages) == TOTAL_PAGES
all_text = '\n'.join(page.extract_text() for page in reader.pages)
assert all(len(page.extract_text())>150 for page in reader.pages)
assert all(p['title'] in all_text for p in pages)
assert len(changes) == 44 and all(len(v)==2 for v in changes.values())
review = [dict(id=p['id'], title=p['title'], source=p['source'], image_kind='original-capture' if p['id'] in source_images else 'unobserved-proposal' if p['id']=='migration' else 'observed-structure-diagram', changes=[dict(focus=a, as_is=b, to_be=d, intent=e) for a,b,d,e in changes[p['id']]]) for p in ordered]
if not PUBLIC:
    (OUT/'CRM-UX-Review-Data.json').write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding='utf8')
    (OUT/'CRM-UX-Review-QA.json').write_text(json.dumps({'pages':len(reader.pages), 'reviewed_routes':len(review), 'comparisons':sum(len(p['changes']) for p in review), 'tab_appendix_pages':len(appendix), 'text_boxes':len(qa), 'min_text_bottom':min(q['bottom'] for q in qa), 'source_capture_routes':list(source_images), 'design_guide_content_included':False}, ensure_ascii=False, indent=2), encoding='utf8')
print(f'Created {pdf}\n{len(reader.pages)} pages; 44 routes; 88 comparison rows; checked {len(qa)} text boxes.')
