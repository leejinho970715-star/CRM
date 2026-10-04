from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parent.parent
fontdir=root/'output/pdf/fonts'
def font(size,bold=False):return ImageFont.truetype(str(fontdir/('Pretendard-Bold.ttf' if bold else 'Pretendard-Regular.ttf')),size)
im=Image.new('RGB',(1200,630),'#f7f7f8');d=ImageDraw.Draw(im)
d.rounded_rectangle((40,40,1160,590),radius=24,fill='white',outline='#e5e6e9',width=2)
d.rounded_rectangle((76,76,132,132),radius=15,fill='#4263cd')
d.line([(92,113),(104,102),(119,87)],fill='white',width=5)
for x,y in [(92,113),(104,102),(119,87)]:d.ellipse((x-4,y-4,x+4,y+4),fill='white')
d.text((149,88),'IONE WORKSPACE',font=font(23,True),fill='#282a30')
d.text((76,207),'IONE CRM',font=font(65,True),fill='#282a30')
d.text((79,306),'고객에서 활동,',font=font(29),fill='#747984')
d.text((79,350),'다음 행동까지.',font=font(29),fill='#747984')
d.rounded_rectangle((78,431,388,471),radius=9,fill='#f0f2fa')
d.text((94,438),'44개 화면 · CRM 리뉴얼 시안',font=font(19,True),fill='#4263cd')
d.text((79,518),'White / Neutral / Calm Density / Bento',font=font(15),fill='#747984')
shot=Image.open(root/'docs/screens/02-activity.png').convert('RGB')
shot=shot.crop((210,0,shot.width,min(shot.height,1050)))
shot.thumbnail((564,478))
d.rounded_rectangle((544,74,1125,554),radius=13,fill='#f7f7f8',outline='#e5e6e9',width=1)
im.paste(shot,(552,82))
im.save(root/'assets/og-image.png')
print('Created 1200x630 neutral OG image with Pretendard and the renewed activity page.')
