"""Export captured pixels to PNG without rescaling, and package every view."""
from pathlib import Path
import json, zipfile, shutil
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'output/captures-v55'
DEST = ROOT / 'docs/screens'
DEST.mkdir(parents=True, exist_ok=True)
(DEST / 'tabs').mkdir(exist_ok=True)
base = json.loads((RAW / 'to-be/manifest.json').read_text(encoding='utf8'))
tabs = json.loads((RAW / 'tabs/manifest.json').read_text(encoding='utf8'))
assert len(base) == 45 and len(tabs) == 42
manifest = []
pending=set()
for items, source, target, prefix in [(base, RAW/'to-be', DEST, ''), (tabs, RAW/'tabs', DEST/'tabs', 'tabs/')]:
    for item in items:
        origin = source/(item['filename']+'.jpg')
        assert origin.exists(), origin
        item['review_status'] = 'fixed-header position needs recapture' if item['filename'] in pending else 'captured'
        result = target / (item['filename']+'.png')
        with Image.open(origin) as im:
            im.save(result, format='PNG', optimize=True)
            with Image.open(result) as decoded:
                assert decoded.size == im.size and decoded.tobytes() == im.tobytes()
            item['pixels'] = {'width': im.width, 'height': im.height}
            item['capture_format'] = 'native JPEG screenshot; unchanged pixels exported as PNG'
        manifest.append({**item, 'file': prefix+result.name})
    (target/'manifest.json').write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf8')
(DEST/'all-views.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')
lines = ['# IONE CRM v5.5 - capture index', '', '45 page images + 42 tab, detail and form images = 87 PNGs.',
         'Captured at a 1920px browser width; native screenshot pixels retained without enlargement.',
         'PNG conversion adds no resolution or lost detail to the browser JPEG capture.', '', '| Page / View | Image |', '| --- | --- |']
for s in manifest:
    lines.append(f"| {s['title']} / {s.get('tab', 'Default page')} | [{s['file']}]({s['file']}) |")
(DEST/'CAPTURE-INDEX.md').write_text('\n'.join(lines)+'\n', encoding='utf8')
archive = ROOT/'output/CRM-리뉴얼-v5.5-전체페이지-탭포함-PNG.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for s in manifest:
        z.write(DEST/s['file'], 'CRM-PNG/'+s['file'])
    z.writestr('CRM-PNG/manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    z.write(ROOT/'docs/CAPTURE-QUALITY-v5.md', 'CRM-PNG/CAPTURE-QUALITY-v5.md')
    z.writestr('CRM-PNG/README.txt', 'IONE CRM v5.5 · 2026-10-06\n기본 페이지 45장 + 탭·상세·등록창 42장 = 총 87장\n네이비 메인 + 본문 색상 보조 버튼·텍스트 + 흰색 CTA 텍스트. 호버 시 좌우 선 추가 없음.\n회사·사용자 프로필 아이콘, 고객 선택선 제거, 카드 텍스트 정렬과 관리자 아이콘과 의미별 라벨 아이콘을 반영했습니다.\n업무함 5개 상태 × 목록·보드·달력의 15개 조합 포함\n영업활동 등록·이력·AI 견적서·포캐스팅 연결 및 단독 시안의 4개 탭 포함\n1920px 브라우저에서 촬영. 캡처 원본 화소 유지, 확대 없음.\n브라우저 JPEG 캡처를 같은 화소의 PNG로 내보냈습니다.\n등록창은 내부 스크롤 때문에 상단/하단을 별도 캡처했습니다.\n가상 고객 및 user_1~3만 사용한 UI 시안입니다.\nhttps://leejinho970715-star.github.io/CRM/?v=5.5\n')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and len([n for n in z.namelist() if n.endswith('.png')]) == 87
shutil.copy2(archive, ROOT/'docs/CRM-PNG.zip')
print(f'Exported 87 PNGs, identical decoded pixels. ZIP: {archive.stat().st_size/1024/1024:.1f} MB')
