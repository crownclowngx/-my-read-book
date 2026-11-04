"""第一章读后感：三张概念图、一张原书图及离线阅读页。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil,base64,re,json,html as html_module

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img'; OUT.mkdir(exist_ok=True)
BG='#F5F8FA'; INK='#173B48'; MUTED='#526A75'; TEAL='#087F80'
COLORS=['#276CB0',TEAL,'#7852A1','#A15B27']
FILLS=['#E8F0FA','#E5F2F0','#F0EAF7','#FAF0E5']
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def text(d,x,y,s,n=32,c=INK,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def para(d,x,y,s,w,n=32,c=INK,b=False,line=51):
 rows=[];buf=''
 for ch in s:
  if ch=='\n':rows.append(buf);buf='';continue
  if d.textlength(buf+ch,font=font(n,b))>w:rows.append(buf);buf=ch
  else:buf+=ch
 if buf:rows.append(buf)
 for i,row in enumerate(rows):text(d,x,y+i*line,row,n,c,b)
 return y+len(rows)*line
def canvas(title,sub,h):
 im=Image.new('RGB',(1440,h),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1440,12),fill=TEAL); text(d,65,42,title,44,b=True)
 para(d,68,120,sub,1300,29,MUTED,line=47)
 d.line((65,h-94,1375,h-94),fill='#D8E2E6',width=2)
 text(d,65,h-68,'《“十五五”经济发展的思考》第一章 · 依据原书自绘 · 2026-10-29',25)
 return im,d
def card(d,box,title,body,i,n=32):
 l,t,r,b=box;d.rounded_rectangle(box,22,fill=FILLS[i],outline=COLORS[i],width=3)
 y=para(d,l+30,t+22,title,r-l-60,36,COLORS[i],True,line=56)
 y=para(d,l+30,y+18,body,r-l-60,n,line=53)
 assert y<=b-20,(title,y,b)

source=ROOT.parent.parent/'第一章 扩消费、稳增长、稳预期与结构性改革'/'img'/'图1-4.png'
shutil.copy2(source,OUT/'01-增长阶段原书图.png')

im,d=canvas('消费不足：沿原书辨认四个原因','关注不同家庭的消费能力、风险与收益来源；四个方面相互交叉。',1290)
items=[('01 基本公共服务','教育、医疗、住房与养老\n影响实际负担和生活保障。'),('02 城市化水平和质量','人口集聚与服务供给衔接；\n就业、定居和权益需要匹配。'),('03 收入分配结构','不同群体的收入与需求不同；\n平均数之外还要看分布。'),('04 财富与收益分配','资产由谁持有，收益流向哪里，\n影响积累与家庭可用收入。')]
for i,(title,body) in enumerate(items):
 x=65+(i%2)*680;y=240+(i//2)*350
 card(d,(x,y,x+630,y+295),title,body,i,31)
d.rounded_rectangle((65,985,1375,1125),20,fill='#E3ECEF')
para(d,100,1015,'共同追问：谁能形成持续需求，哪些条件仍限制消费能力？',1220,35,b=True,line=56)
im.save(OUT/'02-消费不足的四个原因.png')

im,d=canvas('两个改革方向，回到家庭的生活条件','依据原书关于两项改革的论证整理；以下为可能作用路径，不是效果测量。',1450)
card(d,(65,240,1375,555),'方向一 提高低收入群体的基本公共服务水平','保障性住房、教育、医疗、社保与养老\n关注：覆盖谁，怎样减轻负担，长期保障由谁支持？',0,33)
card(d,(65,605,1375,920),'方向二 推动城乡要素双向顺畅流动','人员、土地、资金流动与都市圈中小城镇发展\n关注：就业是否匹配，家庭能否定居，服务能否接续？',1,33)
d.rounded_rectangle((65,980,1375,1200),22,fill=FILLS[2],outline=COLORS[2],width=3)
para(d,100,1010,'连接到家庭：实际负担、风险与预期、就业和发展机会',1220,35,COLORS[2],True,line=57)
para(d,100,1090,'这些条件的改善，可能为消费能力提供更稳定的支撑。',1220,32,line=53)
para(d,80,1245,'实现程度取决于资金、人员、设施、办理条件及当地人口与产业情况。',1280,28,MUTED,line=47)
im.save(OUT/'03-改革方向与家庭生活.png')

im,d=canvas('高质量发展的三支柱','按原书顺序：需求侧、要素侧、产业侧。三者相互支持。',1470)
for i,(y,title,body) in enumerate([
 (235,'需求侧 发展型服务消费','扩大消费能力与需求，改善准入、开放、供给质量和可及性。'),
 (535,'要素侧 公共服务与人力资本','促进城乡融合，支持健康、教育、保障及劳动力合理流动。'),
 (835,'产业侧 公平竞争与转型升级','保护产权，推动创新与效率提升，支持有序进入和退出。')]):
 card(d,(65,y,1375,y+250),title,body,i,33)
para(d,80,1150,'两台发动机：企业家与地方主要领导者',1280,36,TEAL,True,line=58)
para(d,80,1220,'推进改革需要主动性，也需要稳定可信的规则与具体执行条件。',1280,31,line=53)
im.save(OUT/'04-高质量发展的三支柱.png')

ims=[]
for f in sorted(OUT.glob('*.png')):
 a=Image.open(f);a.thumbnail((360,480));ims.append(a.copy())
proof=Image.new('RGB',(1440,500),'#DEE7EB')
for i,a in enumerate(ims):proof.paste(a,(360*i,10))
proof.save(ROOT/'配图核对.png')
article=ROOT/'01-扩消费稳增长稳预期与结构性改革.md'
md=article.read_text(encoding='utf-8')
try:
 import markdown
 html=markdown.markdown(md,extensions=['tables','fenced_code'])
except ImportError:
 def inline(s):
  s=html_module.escape(s)
  s=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',r'<img alt="\1" src="\2">',s)
  s=re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
  return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
 blocks=[]
 for block in md.strip().split('\n\n'):
  if block.startswith('#'):
   match=re.match(r'^(#{1,6}) (.*)',block);level=len(match[1]);blocks.append(f'<h{level}>'+inline(match[2])+f'</h{level}>')
  elif block.startswith('> '):blocks.append('<blockquote><p>'+inline(block[2:])+'</p></blockquote>')
  elif block.startswith('- '):blocks.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines())+'</ul>')
  else:blocks.append('<p>'+inline(block)+'</p>')
 html='\n'.join(blocks)
for f in OUT.glob('*.png'):
 html=html.replace('img/'+f.name,'data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode())
title,body=md.split('\n',1)
controls='<div><button onclick="navigator.clipboard.writeText(document.getElementById(\'copy-title\').value)">复制标题</button> <button onclick="navigator.clipboard.writeText(document.getElementById(\'copy-body\').value)">复制Markdown正文</button></div>'
controls+='<textarea hidden id="copy-title">'+html_module.escape(title.removeprefix('# '))+'</textarea><textarea hidden id="copy-body">'+html_module.escape(body.strip())+'</textarea>'
page='<!doctype html><meta charset="utf-8"><title>第一章读后感</title><style>body{max-width:820px;margin:40px auto;padding:0 22px;font:18px/1.95 "Microsoft YaHei",sans-serif;color:#243b48}img{max-width:100%;height:auto}h1{font-size:29px}h2{margin-top:2.4em;font-size:25px}h3{font-size:21px}blockquote{border-left:4px solid #087f80;padding-left:18px;color:#526a75}a{color:#276cb0}button{padding:9px 16px;font:16px sans-serif;cursor:pointer}</style>'+controls+html
(ROOT/'阅读预览与复制.html').write_text(page,encoding='utf-8')
print(json.dumps({'characters':len(md),'images':[x.name for x in OUT.glob('*.png')]},ensure_ascii=False))
