from pathlib import Path
import json, shutil
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent.parent
review=json.loads((ROOT/'output/pdf/CRM-UX-Review-Data.json').read_text(encoding='utf8'))
pages={p['id']:p for p in json.loads((ROOT/'docs/pages.json').read_text(encoding='utf8'))}
lines=['# CRM v5.6 · 페이지별 UX As-is / To-be', '',
       '2026-10-06 · 44개 페이지 · 88개 비교 항목 · 탭·상세 화면 별도 캡처 포함', '',
       '최종 시안의 페이지별 UX 변경과 개선 의도를 기존 화면과 비교합니다. 네이비 대표 버튼·페이지 번호, 본문 색상의 보조 텍스트, 회사·사용자 프로필과 의미별 라벨 아이콘을 반영했습니다. 기대 효과는 실제 사용 테스트로 검증할 설계 의도입니다.', '',
       '[102쪽 공개 비교 PDF](CRM-Renewal-As-Is-To-Be.pdf) · [87장 PNG ZIP](CRM-PNG.zip) · [전체 캡처 목차](screens/CAPTURE-INDEX.md)', '',
       '공개판의 AS-IS는 확인한 구성 관계의 도식이며 실제 원본의 배치·스타일을 재현한 이미지가 아닙니다. 로그인 후 실제 원본 캡처를 포함한 비교 PDF는 로컬 output/pdf에 별도로 제공합니다. 마이그레이션은 원본 미열람 제안입니다.', '']
for p in review:
    lines.extend(['## '+p['title'],'','| 개선 항목 | As-is | To-be | 개선 의도 |','| --- | --- | --- | --- |'])
    for ch in p['changes']:
        lines.append('| '+' | '.join(ch[k].replace('|','／') for k in ['focus','as_is','to_be','intent'])+' |')
    lines.extend(['',f"[리뉴얼 시안](https://leejinho970715-star.github.io/CRM/?v=5.6#{p['id']}) · [기존 페이지](https://ione119.co.kr{p['source']})",''])
(ROOT/'docs/AS-IS-TO-BE.md').write_text('\n'.join(lines),encoding='utf8')
shutil.copy2(ROOT/'output/pdf/CRM-UX-Review-Data.json',ROOT/'docs/ux-review-v5.json')
samples=['001','002','003','006','007','009','014','021','025','041','049','050','051','053','062','075','088','093','095','098','101','102']
sheet=Image.new('RGB',(5*340,5*360),'#e9edf2')
for i,n in enumerate(samples):
    path=ROOT/'tmp/pdfs'/('v5-review-'+n+'.png')
    if not path.exists(): raise FileNotFoundError(path)
    im=Image.open(path).convert('RGB');im.thumbnail((328,324))
    x=(i%5)*340;y=(i//5)*360
    sheet.paste(im,(x+(340-im.width)//2,y+23))
    ImageDraw.Draw(sheet).text((x+14,y+5),'Page '+n,fill='#18243a')
sheet.save(ROOT/'tmp/pdfs/v5-contact-sheet.png')
responsive=json.loads((ROOT/'docs/responsive-validation-v5.json').read_text(encoding='utf8'))
tabs=json.loads((ROOT/'docs/tab-validation-v5.json').read_text(encoding='utf8'))
activity=json.loads((ROOT/'docs/activity-responsive-v5.json').read_text(encoding='utf8'))
assert len(responsive)==352 and all(r['width']==r['viewport'] and not r['overflow'] and not r['textOverflow'] for r in responsive)
assert len(tabs)==68 and all(not r['overflow'] for r in tabs)
assert len(activity)==40 and all(not r['overflow'] for r in activity)
print('Markdown updated; contact sheet created. QA: 352 pages + 68 narrow tab views + 40 activity states.')
