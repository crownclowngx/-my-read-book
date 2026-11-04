"""第八章读后感：三张自绘说明图和一张原书地图。"""
from pathlib import Path
import math,shutil
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80'
BLUE='#276CB0';PURPLE='#7852A1';GRID='#D8E2E6'
FILLS=['#E8F0FA','#E5F2F0','#F0EAF7','#FAF0E5']
def font(n,bold=False):
 return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',n)
def text(d,x,y,s,n=32,c=INK,b=False):d.text((x,y),s,font=font(n,b),fill=c)
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
 para(d,68,120,sub,1300,28,line=45)
 d.line((65,h-94,1375,h-94),fill=GRID,width=2)
 text(d,65,h-69,'《基层中国的运行逻辑》第八章读后感 · 依据原书自绘 · 2026-10-28',23)
 return im,d
def card(d,box,title,lines,color,fill,n=31):
 l,t,r,b=box;d.rounded_rectangle(box,22,fill=fill,outline=color,width=3)
 y=para(d,l+28,t+20,title,r-l-56,36,color,True,line=54)
 for s in lines:y=para(d,l+28,y+13,s,r-l-56,n,INK,line=49)
 assert y<=b-16,(title,y,b)
def arrow(d,p,q,color=TEAL,width=4):
 d.line((p,q),fill=color,width=width)
 a=math.atan2(q[1]-p[1],q[0]-p[0]);l=18
 d.polygon([q,(q[0]-l*math.cos(a-.5),q[1]-l*math.sin(a-.5)),(q[0]-l*math.cos(a+.5),q[1]-l*math.sin(a+.5))],fill=color)

im,d=canvas('城市化战略：活力与秩序之间的权衡','依据原书图8-3重绘。线条与位置为理论示意，没有使用经验测算数据。',1350)
arrow(d,(260,1020),(260,205),INK)
arrow(d,(260,1020),(1290,1020),INK)
text(d,70,245,'活力',36,b=True)
text(d,40,303,'（区域失衡）',29)
text(d,1110,1060,'秩序',36,b=True)
text(d,1040,1117,'（区域平衡）',29)
points=[(260+u,1020-90000/u) for u in range(120,801)]
d.line(points,fill=TEAL,width=6)
d.line(((260,420),(860,1020)),fill=PURPLE,width=4)
for u in (130,300,730):
 x,y=260+u,1020-90000/u
 d.ellipse((x-8,y-8,x+8,y+8),fill=INK)
text(d,465,225,'人口自由流动',34,TEAL,True)
arrow(d,(480,280),(399,330),TEAL,3)
text(d,880,823,'限制城市规模',34,TEAL,True)
text(d,840,510,'城市化政策',34,BLUE,True)
arrow(d,(865,565),(635,780),BLUE,3)
text(d,305,550,'成本最小化',32,PURPLE,True)
arrow(d,(395,602),(450,610),PURPLE,3)
d.arc((775,935,945,1105),180,225,fill=PURPLE,width=3)
text(d,750,965,'45°',28,PURPLE)
para(d,75,1180,'不同阶段、不同地区面对的约束不同，合适的政策组合也会变化。',1270,30,INK,line=47)
im.save(OUT/'01-活力与秩序的权衡.png')

im,d=canvas('怎样观察政商关系的“亲”与“清”','依据原书表8-1整理。百分比表示指标权重，不表示城市实际得分。',1460)
text(d,85,220,'亲近指数  60%',40,TEAL,True)
text(d,780,220,'清白指数  40%',40,PURPLE,True)
card(d,(65,300,695,550),'政府对企业的关心  10%',['观察例子：领导走访企业','与企业家座谈等'],TEAL,FILLS[1])
card(d,(65,590,695,890),'政府对企业的服务  40%',['基础设施、金融服务','市场中介、电子政务效率','以上四类各占10%'],TEAL,FILLS[1])
card(d,(65,930,695,1180),'企业税费负担  10%',['观察例子：企业相关税负','结合原书使用的数据口径'],TEAL,FILLS[1])
card(d,(745,300,1375,550),'政府廉洁度  10%',['通过评价体系选定的指标','观察廉洁程度'],PURPLE,FILLS[2])
card(d,(745,590,1375,890),'政府透明度  30%',['网络信息公开  15%','财政透明度  15%'],PURPLE,FILLS[2])
para(d,775,960,'先理解指标观察什么，\n再判断综合分数能说明什么。',560,31,INK,line=56)
para(d,80,1240,'这是原书采用的评价体系。比较不同报告、年份或样本时，需要核对指标和计算方法。',1280,29,line=47)
im.save(OUT/'02-亲近与清白的评价指标.png')

shutil.copy2(ROOT.parent.parent/'第八章 区域协同发展之路'/'img'/'图8-4.png',OUT/'03-城市政商关系地图-2019.png')

im,d=canvas('营商环境：五个角度看研究结果','依据原书对2017—2021年城市政商关系指数的分析归纳。',1720)
rows=[
 ('01  前列名单','排名前列的城市相对稳定','观察：改善自身条件与进入前列，各需要什么？',BLUE,FILLS[0]),
 ('02  行政级别','高级别城市总体上更有优势','观察：服务能力与资源、财政和组织条件的联系。',TEAL,FILLS[1]),
 ('03  省份差异','省级均值呈现不同分布','观察：省级概括之外，具体城市仍有差别。',PURPLE,FILLS[2]),
 ('04  区域比较','华东整体领先，区域表现各有差异','观察：用相同时期的指标检验笼统地域印象。',BLUE,FILLS[0]),
 ('05  影响因素','与经济、人口和产业等条件相关','观察：进一步追问机制与条件，区分相关与因果。',TEAL,FILLS[1]),
]
for i,(title,line1,line2,color,fill) in enumerate(rows):
 y=220+i*250
 card(d,(65,y,1375,y+215),title,[line1,line2],color,fill,30)
para(d,80,1500,'这些结果对应原书样本与时期，不是2026年新排名；图中没有绘制新的量化比较。',1280,28,line=45)
im.save(OUT/'04-营商环境的五个观察.png')
sheet=Image.new('RGB',(1440,700),'#DCE6EA')
for i,p in enumerate(sorted(OUT.glob('*.png'))):
 thumb=Image.open(p).convert('RGB');thumb.thumbnail((355,680));sheet.paste(thumb,(i*360,10))
sheet.save(ROOT/'配图核对.png')
print('3 drawn figures and 1 source map saved.')
