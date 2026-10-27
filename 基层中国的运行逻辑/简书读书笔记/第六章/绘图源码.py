"""第六章简书读后感：三张依据原书和注明资料自绘的中文图。"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80'
BLUE='#276CB0';PURPLE='#7852A1';GRID='#D8E2E6'
COLORS=[BLUE,TEAL,PURPLE,'#A15B27']
FILLS=['#E8F0FA','#E5F2F0','#F0EAF7','#FAF0E5']

def font(n,bold=False):
 return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',n)

def text(d,x,y,s,n=32,c=INK,b=False):
 d.text((x,y),s,font=font(n,b),fill=c)

def para(d,x,y,s,w,n=32,c=MUTED,b=False,line=51):
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
 d.rectangle((0,0,1440,12),fill=TEAL)
 text(d,65,43,title,44,b=True)
 para(d,68,120,sub,1300,29,line=46)
 d.line((65,h-94,1375,h-94),fill=GRID,width=2)
 text(d,65,h-69,'《基层中国的运行逻辑》第六章读后感 · 自绘 · 2026-10-26',25)
 return im,d

def card(d,box,title,lines,color,fill,n=32):
 l,t,r,b=box;d.rounded_rectangle(box,22,fill=fill,outline=color,width=3)
 y=para(d,l+30,t+22,title,r-l-60,37,color,True,line=57)
 for s in lines:
  y+=14;y=para(d,l+30,y,s,r-l-60,n,INK,line=50)
 assert y<=b-20,(title,y,b)

def arrow(d,p,q,color=TEAL):
 import math
 d.line((p,q),fill=color,width=5)
 a=math.atan2(q[1]-p[1],q[0]-p[0]);l=18
 d.polygon([q,(q[0]-l*math.cos(a-.5),q[1]-l*math.sin(a-.5)),(q[0]-l*math.cos(a+.5),q[1]-l*math.sin(a+.5))],fill=color)

im,d=canvas('晋升路径：先看组织空间，再比较个人经历','依据原书设定整理；三个年限不表示全国实际晋升时长的平均值。',1680)
card(d,(65,225,1375,535),'乡镇：作者设定的较顺利路径',['试用 → 普通科员 → 副乡长 → 乡长','再任乡党委书记或部门负责人 → 副处级','作者设定累计约15年'],BLUE,FILLS[0],33)
card(d,(65,580,1375,940),'乡镇：经过多个“隐性台阶”的路径',['副乡长 → 党委委员 → 副书记等同层次岗位','再经历正科级相关职务 → 副处级','作者估计可能约25年；分工和实权可先于级别变化'],TEAL,FILLS[1],33)
card(d,(65,985,1375,1295),'中央部委：作者设置的对照路径',['试用 → 副主任科员 → 主任科员 → 副处级','沿用原书名称与条件，不直接等同于现行任职路线','作者设定累计约7年'],PURPLE,FILLS[2],33)
text(d,80,1360,'现实比较要分别看',34,b=True)
para(d,80,1420,'领导职务与具体分工   ·   职级和待遇变化\n机构职位结构   ·   实际选拔机会与个人条件',1275,31,INK,line=54)
im.save(OUT/'01-晋升路径与组织空间.png')

im,d=canvas('考核变化：原书地方样本的前后比较','依据表6-1重排；前→后指十八大前后两个阶段，各栏分别计数。',1210)
xs=[65,285,650,1015,1375];heads=['对象','一级指标数量','减分事项','一票否决事项']
for j,h in enumerate(heads):
 d.rounded_rectangle((xs[j]+5,235,xs[j+1]-5,360),15,fill=FILLS[min(j,2)])
 text(d,xs[j]+28,277,h,34,b=True)
rows=[('市','6 → 8','5 → 5','5 → 5'),('县','6 → 15','5 → 20','5 → 7'),('乡','6 → 13','5 → 15','4 → 7')]
for i,row in enumerate(rows):
 y=385+i*160
 d.rounded_rectangle((65,y,1375,y+140),15,fill='white',outline=GRID,width=2)
 for j,t in enumerate(row):text(d,xs[j]+38,y+45,t,42,COLORS[min(j,2)],True)
text(d,80,925,'怎样读这张图',35,b=True)
para(d,80,990,'县、乡的部分要求明显增加；各栏目变化并不完全相同。\n这是原书选择的地方比较，不能据此画出全国逐年变化趋势。',1270,30,INK,line=51)
im.save(OUT/'02-原书样本中的考核变化.png')

im,d=canvas('数字考核：解决了什么，还要继续问什么','前两列依据原书兴安案例；第三列为本文的延伸思考。',1510)
cols=[(65,460),(505,900),(945,1375)]
for (l,r),h,c in zip(cols,['原有难题','案例中的回应','继续追问'],[BLUE,TEAL,PURPLE]):text(d,l+15,235,h,36,c,True)
data=[
 ('评价主体较单一',['信息主要来自上级与同事'],'群众评价',['办事群众通过\n二维码反馈'],'谁能参与评价？',['不同岗位接触群众的机会是否相同？']),
 ('评分缺少区分度',['普遍高分难以说明差异'],'稀缺荣誉币',['让评价者在有限资源中作出取舍'],'差异说明什么？',['分数差异能否\n反映真实贡献？']),
 ('量化内容存在偏重',['重要但难记录的工作可能被遗漏'],'结合多维记录',['工分、奖惩、错情等信息一起观察'],'组织是否更好？',['长期工作与团队合作怎样获得认可？'])]
for i,row in enumerate(data):
 y=330+i*315
 for j,((l,r),c,f) in enumerate(zip(cols,[BLUE,TEAL,PURPLE],FILLS[:3])):
  card(d,(l,y,r,y+280),row[j*2],row[j*2+1],c,f,30)
text(d,80,1325,'信息更丰富，还需要合理的规则、复核和激励。',33,b=True)
im.save(OUT/'03-数字考核的回应与追问.png')

proof=Image.new('RGB',(1440,600),'#DDE5E8')
for i,p in enumerate(sorted(OUT.glob('*.png'))):
 im=Image.open(p);im.thumbnail((480,600));proof.paste(im,(i*480,0))
proof.save(ROOT/'配图核对.png')
print('3 figures complete')

