"""Compose the landing social preview from supplied brand assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
assets = ROOT / 'i-ONE/assets'
canvas = ImageOps.fit(Image.open(assets / 'hero-tech-background.webp').convert('RGB'), (1200, 630), method=Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(canvas)
fonts = ROOT / 'output/pdf/fonts'
bold = ImageFont.truetype(str(fonts / 'Pretendard-Bold.ttf'), 54)
body = ImageFont.truetype(str(fonts / 'Pretendard-Regular.ttf'), 21)

def paste(name, box):
    image = Image.open(assets / name).convert('RGBA')
    image.thumbnail(box[2:])
    canvas.paste(image, box[:2], image)

paste('company-logo.webp', (56, 40, 222, 64))
draw.line((303, 45, 303, 99), fill='#dfe5ee', width=1)
paste('ax-dx-logo.webp', (325, 39, 131, 63))
draw.text((58, 183), '비즈니스의 다음을', font=bold, fill='#272a33')
draw.text((58, 253), '연결합니다.', font=bold, fill='#1471ef')
draw.text((61, 354), '경영관리에서 협업, 그리고 AI까지.', font=body, fill='#666c76')
draw.rounded_rectangle((60, 424, 267, 478), radius=8, fill='#1471ef')
draw.text((83, 439), '아이원소프트뱅크', font=body, fill='white')
paste('hero-visual.webp', (530, 160, 645, 395))
draw.line((60, 555, 1140, 555), fill='#dfe5ee', width=1)
draw.text((61, 576), 'OmniEsol  ·  Amaranth10  ·  WEHAGO  ·  ONE AI  ·  비영리  ·  IFRS18', font=body, fill='#1471ef')
canvas.save(assets / 'og-landing.png', optimize=True)
for size, name in [(32,'favicon-32.png'), (180,'apple-touch-icon.png')]:
    icon=Image.new('RGBA',(size*4,size*4),(0,0,0,0))
    d=ImageDraw.Draw(icon)
    s=size*4
    d.rounded_rectangle((0,0,s,s),radius=s*.25,fill='#1471ef')
    d.ellipse((s*.22,s*.22,s*.78,s*.78),outline='white',width=round(s*.11))
    d.ellipse((s*.625,s*.14,s*.84,s*.355),fill='#00aaf0')
    icon.resize((size,size),Image.Resampling.LANCZOS).save(assets/name)
print('Created i-ONE/assets/og-landing.png (1200 × 630)')
