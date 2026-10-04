"""Generate the Korean page-by-page comparison and PNG delivery package."""
from pathlib import Path
import json, shutil, zipfile, html
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent.parent
DOCS=ROOT/'docs'; OUT=ROOT/'output'; TMP=ROOT/'tmp/pdfs'
TMP.mkdir(parents=True,exist_ok=True)
pages=json.loads((DOCS/'pages.json').read_text(encoding='utf8'))
manifest=json.loads((DOCS/'screens/manifest.json').read_text(encoding='utf8'))
screens={s['id']:s for s in manifest}
url='https://leejinho970715-star.github.io/CRM/'
asis={
'home':'조회 범위와 미활동 기준, 고객 추천과 영업 요약을 제공하는 진입 화면.',
'customers':'고객 조건 검색과 넓은 고객 목록, 상세 항목 및 등록·수정 기능을 제공.',
'nonprofits':'일반 고객 정보에 설립·예산 관련 정보와 알림 조건이 함께 배치됨.',
'news':'영리·비영리 뉴스 조회와 고객 연결 조건이 있는 목록 구조.',
'contacts':'연락처 목록의 여러 열과 행 안의 편집 요소가 함께 표시됨.',
'upload':'고객 파일 선택과 열 매핑, 데이터 반영을 위한 업로드 화면.',
'activity':'좌측 고객 목록, 고객 요약 표, 좁고 긴 기본 정보 폼과 큰 내용 입력란이 병렬 배치됨. 처리 결과·다음 행동·품목·첨부·등록 버튼은 화면 아래로 이어짐.',
'tasks':'업무 등록과 기한·상태별 조회를 제공하는 업무 관리 화면.',
'leads':'유입 문의의 고객 정보, 배정 담당자와 진행 상태를 조회·관리.',
'quotes':'고객·담당자·제품 조건과 견적 관련 활동 내역을 목록으로 표시.',
'marketing':'대상 고객과 마케팅 활동 정보, 내용 및 리드 관련 값을 입력.',
'yearly':'기간·담당자·활동 조건에 따른 영업 집계와 상세 목록을 제공.',
'activity-detail':'활동 유형과 업체별 영업 내역, 관련 금액을 조회.',
'ai':'영업 기록에 기반한 추천·분석 정보를 확인하는 전용 영역.',
'work-report':'담당자와 기간에 따른 활동 내역 및 업무일지를 작성·조회.',
'custom-reports':'보고 대상·그룹·집계 기준을 선택해 사용자 보고서를 구성.',
'ssl-master':'SSL 품목·공급사·갱신 관련 기준 정보를 각각 관리.',
'ssl-purchase':'발주 정보와 품목의 수량·단가·세액 등을 입력.',
'ssl-delivery':'출고와 설치 정보, 고객·도메인·인증서 관련 항목을 관리.',
'ssl-expiration':'인증서 만료 정보와 갱신 대상, 알림 조건을 조회.',
'forecast-add':'고객·제품·라이선스·교육비·예정일·이월 정보를 등록.',
'forecast-status':'월별 계약 예상 내역과 이월·달성 관련 표가 반복되는 구조.',
'other-add':'기타 계약의 고객·금액·계약 일정과 이월 정보를 등록.',
'other-status':'기타 계약의 월별 예상·이월·달성 현황을 조회.',
'admin':'계정·권한·조직·기준정보·운영 설정으로 이어지는 관리자 메뉴.',
'members':'회원과 담당 업무, 재직 여부 및 관련 설정을 관리.',
'transfer':'고객 선택과 기존·변경 담당자를 지정하는 담당자 이관 기능.',
'permissions':'역할별 페이지 접근 대상을 선택·관리하는 권한 설정.',
'departments':'부서 목록과 소속 정보를 관리하고 신규 부서를 등록.',
'department-add':'부서의 기본 정보를 입력하는 별도 신규 등록 화면.',
'goals':'사원별 월 목표와 연간 목표 값을 관리하는 표 중심 화면.',
'manage-items':'관리 항목과 해당 선택값을 등록·관리.',
'institutions':'고객 분류에 사용하는 기관유형의 선택 항목을 관리.',
'acquisition':'소스출처와 인입경로 등 유입 분류 정보를 관리.',
'commercial-news':'뉴스 수집·사용·순서·키워드 관련 기준을 관리.',
'nonprofit-keywords':'비영리 관련 뉴스 수집 키워드와 사용 상태를 관리.',
'products':'제품 품목과 코드, 사용 여부를 관리.',
'product-options':'품목에 연결된 옵션과 옵션 코드를 관리.',
'options-upload':'품목옵션 데이터를 파일로 일괄등록.',
'marketing-types':'마케팅 활동의 유형과 사용 여부를 관리.',
'work-settings':'업무일지 표시 대상과 선보고 수신 대상 설정.',
'system':'브랜드·로그인 이미지와 운영 알림 관련 값을 설정.',
'migration':'원본 화면을 열지 않았음. 기존 배치와 실제 실행 규칙은 확인하지 않음.',
'login':'브랜드 영역과 인증 입력, 계정 찾기·가입 경로를 제공하는 로그인 화면.'}

def labels(page):
    fields=page.get('filters',[])+page.get('extra',[])
    for g in page.get('sections',[]):fields+=g.get('fields',[])
    for g in page.get('groups',[])+page.get('form',[]):fields+=g.get('fields',[])
    vals=list(dict.fromkeys(f.get('label','') for f in fields if f.get('label')))
    if page['id']=='activity':vals=['거래처명·코드','사업자번호','담당자','상세 필터','고객사 담당자','입력자','활동 유형·상세 유형','활동일','제목·내용','처리 결과','다음 행동·기한','품목','첨부파일']
    return vals

comparison=[dict(id=p['id'],title=p['title'],group=p['group'],source=p['source'],as_is=asis[p['id']],to_be=p['improvement'],preserved=labels(p),proposed=p.get('proposed',False),url=url+'#'+p['id']) for p in pages]
(DOCS/'comparison-data.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2),encoding='utf8')
markdown='# CRM 리뉴얼 · As-is / To-be\n\n2026-10-05 · 44개 화면 · Pretendard / White & Neutral / Calm Density / Thin Border / Bento\n\n기존 화면 구조 관찰과 구현한 시안의 비교입니다. 운영 기능의 실행 결과나 측정된 사용성 개선율을 의미하지 않습니다.\n\n'
for p in comparison:
    markdown+=f"## {p['title']}\n\n- As-is: {p['as_is']}\n- To-be: {p['to_be']}\n- 주요 유지 항목: {', '.join(p['preserved']) or '기존 관리 대상과 조회·등록·수정 흐름'}\n- [시안 보기]({p['url']})\n\n"
(DOCS/'AS-IS-TO-BE.md').write_text(markdown,encoding='utf8')

for name in ['Regular','Bold']:
    pdfmetrics.registerFont(TTFont('Pretendard'+name,str(OUT/'pdf/fonts'/('Pretendard-'+name+'.ttf'))))
W,H=595.28,841.89; M=36; CW=W-2*M
INK='#282a30'; MUTED='#747984'; LINE='#e5e6e9'; BLUE='#4263cd'
styles={k:ParagraphStyle(k,fontName='Pretendard'+('Bold' if k=='bold' else 'Regular'),fontSize=s,leading=l,textColor=HexColor(INK),wordWrap='CJK') for k,s,l in [('body',10,16),('small',8,12),('bold',11,17)]}
pdf=OUT/'pdf/CRM-Renewal-As-Is-To-Be.pdf'; pdf.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1)
c.setTitle('IONE CRM 리뉴얼 — As-is / To-be');c.setAuthor('CRM Design');c.setSubject('44개 페이지의 개선 방향과 공통 디자인 시스템')
def text(txt,x,y,size=10,color=INK,bold=False):
    c.setFont('Pretendard'+('Bold' if bold else 'Regular'),size);c.setFillColor(HexColor(color));c.drawString(x,y,txt)
def para(txt,x,y,width,style='body'):
    p=Paragraph(html.escape(txt),styles[style]);pw,ph=p.wrap(width,700);p.drawOn(c,x,y-ph);return ph
def base(number,label):
    c.setFillColor(HexColor('#ffffff'));c.rect(0,0,W,H,fill=1,stroke=0)
    c.drawImage(str(ROOT/'assets/logo.png'),M,H-49,width=100,height=36.18,mask='auto')
    text('CRM / RENEWAL REVIEW',M+115,H-32,8,MUTED,True)
    text(label,M,26,8,MUTED);text(f'{number:02d}',W-M-16,26,8,MUTED)
    c.setStrokeColor(HexColor(LINE));c.line(M,45,W-M,45)
def card(x,y,w,h):
    c.setFillColor(HexColor('#fafafa'));c.setStrokeColor(HexColor(LINE));c.roundRect(x,y,w,h,10,fill=1,stroke=1)
def shot(id,x,y,w,h,crop=True):
    source=DOCS/'screens'/(screens[id]['filename']+'.png')
    im=Image.open(source)
    if crop:im=im.crop((0,0,im.width,min(im.height,int(im.width*h/w))));temp=TMP/(id+'.jpg');im.convert('RGB').save(temp,quality=95)
    else:temp=source
    c.drawImage(str(temp),x,y,width=w,height=h,preserveAspectRatio=True,anchor='n',mask='auto')

base(1,'DESIGN DIRECTION / 2026.10.05')
text('고객에서 활동,',M,735,32,bold=True);text('다음 행동까지.',M,687,32,bold=True)
text('IONE CRM 전체 리뉴얼',M,643,19,MUTED)
para('44개 화면의 개선 전·후 비교와 공통 UI 규칙. 첨부한 공식 로고, 전체 반응형 보완, 대시보드의 절제된 3D 카드 표현과 네 가지 상태 라벨 기준을 반영한 최신 시안입니다.',M,597,CW)
card(M,230,CW,285);shot('home',M+8,238,CW-16,269)
text('WHITE & NEUTRAL  /  CALM DENSITY  /  BENTO',M,190,10,BLUE,True)
para('Pretendard · 얇은 1px Border · 흰색 카드 · 중립 배경 · 절제된 파란 강조',M,164,CW)
para('본 문서는 화면 구조와 UI 시안의 비교입니다. 수치로 측정한 사용성 개선율은 포함하지 않습니다. 데이터·저장·계산은 로컬 샘플 동작이며 실제 CRM 서버와 연결되지 않습니다.',M,111,CW,'small');c.showPage()

base(2,'COMMON DESIGN SYSTEM')
text('전체 페이지를 묶는 5가지 규칙',M,754,24,bold=True)
rules=[('01  White / Neutral','배경 #F7F7F8, 카드 #FFFFFF, 본문 #282A30. 색상보다 제목·간격·그룹으로 정보의 우선순위를 표현합니다.'),('02  Calm Density','본문 14px, 필터·입력 높이 40px, 카드 간격 18px. 긴 목록은 표 안에서 스크롤하고 등록은 목적별 입력 묶음으로 구성합니다.'),('03  Thin Border / Status','공통 경계 #E5E6E9, 1px 테두리. 상태 라벨은 뉴트럴(대기·종료), 블루 그레이(진행), 세이지(완료), 샌드(조치 필요)의 네 가지 톤과 동일한 의미 사전을 사용합니다.'),('04  Bento Structure','요약·필터·목록·입력·다음 행동을 역할별 카드로 묶습니다. 같은 필드 이름과 핵심 기능을 유지하면서 읽는 순서를 정리합니다.'),('05  Pretendard / Brand','첨부한 DOUZONE 로고를 원본 그대로 사용합니다. 웹과 PDF에 Pretendard를 적용하고 사용자님 및 user_1~3 표기를 유지합니다.')]
y=705
for title,body in rules:
    card(M,y-100,CW,100);text(title,M+18,y-28,13,BLUE,True);para(body,M+18,y-47,CW-36);y-=116
para('확인 범위: 운영 CRM 42개 화면 및 로그인 화면을 읽기 전용으로 확인한 이전 분석과 사용자 첨부 화면을 바탕으로 작성. 데이터 마이그레이션은 원본을 열지 않은 제안 화면입니다. 운영 사이트의 등록·수정·발송·권한 변경은 수행하지 않았습니다.',M,101,CW,'small');c.showPage()

ordered=sorted(comparison,key=lambda p:0 if p['id']=='activity' else 1)
for n,items in enumerate([ordered[:22],ordered[22:]],3):
    base(n,'PAGE INDEX');text('페이지별 비교 목차',M,754,24,bold=True)
    for i,p in enumerate(items):
        ypos=705-i*27;idx=ordered.index(p)+5
        text(p['title'],M,ypos,10);text(f'{idx:02d}',W-M-22,ypos,10,MUTED)
        c.linkURL(p['url'],(M,ypos-3,W-M,ypos+14),relative=0)
    c.showPage()

for idx,p in enumerate(ordered,5):
    base(idx,p['group']+' / '+p['id']);c.bookmarkPage(p['id']);c.addOutlineEntry(p['title'],p['id'],0,False)
    text(p['title'],M,751,23,bold=True);text('AS-IS → TO-BE'+(' / 제안 화면' if p['proposed'] else ''),M,723,9,BLUE,True)
    card(M,408,CW,291);shot(p['id'],M+5,413,CW-10,281)
    text('To-be 상단 미리보기 · 전체 화면은 PNG 및 웹 시안에서 확인',M,392,8,MUTED)
    half=(CW-14)/2
    card(M,180,half,194);card(M+half+14,180,half,194)
    text('AS-IS / 기존 구조',M+15,348,11,MUTED,True);para(p['as_is'],M+15,324,half-30)
    text('TO-BE / 개선 방향',M+half+29,348,11,BLUE,True);para(p['to_be']+'.',M+half+29,324,half-30)
    text('유지한 주요 입력·필터·관리 대상',M,152,11,bold=True)
    kept=' · '.join(p['preserved']) or '조회·등록·수정 흐름 및 해당 메뉴의 관리 대상'
    para(kept,M,131,CW,'small')
    text('전체 시안 열기 → '+p['id'],M,67,9,BLUE);c.linkURL(p['url'],(M,60,W-M,83),relative=0)
    c.showPage()

base(49,'IMPLEMENTATION & HANDOFF')
text('구현 범위와 다음 연결 단계',M,754,24,bold=True)
y=704
for title,body in [('현재 구현','44개 화면 및 단독 영업활동 시안, 첨부 로고, 공통 Pretendard 테마, 내용 너비에 따른 반응형 배치, 은은한 3D 대시보드, 공통 상태 라벨 가이드, 사용자 익명 표기, favicon·OG 및 전체 화면 PNG 패키지.'),('시안의 동작','검색·필터·탭·상세 패널·로컬 저장·샘플 계산을 제공하는 정적 UI입니다. 기존 기능에 대한 입력 구조를 보존했으며, 실제 서버 규칙·권한·예외 처리는 별도 구현이 필요합니다.'),('실서비스 연결','실제 API, 인증과 접근 권한, CRM 데이터 저장, 이메일·알림, 뉴스 수집, AI 생성, Excel 서버 처리와 데이터 마이그레이션은 실제 서비스와 연결되지 않습니다.'),('검증과 전달','320·390·600·820·1024·1280·1600px의 7개 폭에서 44개 화면을 확인했습니다. 넓은 표는 내부 스크롤로 유지합니다. 웹·PDF·PNG에 새 로고와 대시보드 입체 표현을 반영했습니다. 검증 기록은 VALIDATION.md에 있습니다.')]:
    card(M,y-130,CW,130);text(title,M+18,y-28,13,BLUE,True);para(body,M+18,y-51,CW-36);y-=147
c.save()
reader=PdfReader(str(pdf));assert len(reader.pages)==49
assert all(len(p.extract_text())>30 for p in reader.pages)
shutil.copyfile(pdf,DOCS/pdf.name)

archive=OUT/'CRM-리뉴얼-전체페이지-PNG.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for s in manifest:z.write(DOCS/'screens'/(s['filename']+'.png'),'CRM-PNG/'+s['filename']+'.png')
    z.writestr('CRM-PNG/README.txt','IONE CRM 리뉴얼 · 2026-10-05\n45장의 전체 화면 PNG\n01 영업활동 단독, 02 영업활동 통합, 이후 전체 CRM 44개 화면\nPretendard / White & Neutral / Calm Density / Thin Border / Bento\n샘플 데이터 UI 시안입니다.\n'+url)
    z.writestr('CRM-PNG/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
print(f'PDF: {pdf} ({len(reader.pages)} pages)\nPNG ZIP: {archive} ({len(manifest)} images)')
