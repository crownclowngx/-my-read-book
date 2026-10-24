"""第四章简书读后感：四张依据原书和注明资料自绘的中文图。"""
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
 text(d,65,h-69,'《基层中国的运行逻辑》第四章读后感 · 自绘 · 2026-10-24',25)
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

im,d=canvas('同在基层，组织性质与工作关系各有区别','先分清机构，再看由什么身份的人承担哪些具体事务。',1490)
card(d,(65,220,1375,450),'街道办事处',[
 '机构性质：不设区的市、市辖区政府的派出机关。',
 '主要观察：行政职责、上级交办事项与部门协作。'],BLUE,FILLS[0])
card(d,(65,485,1375,715),'乡镇政府',[
 '机构性质：乡、民族乡、镇这一级地方政府。',
 '主要观察：本级人大、法定职责与具体工作安排。'],TEAL,FILLS[1])
card(d,(65,750,1375,980),'社区居民委员会',[
 '机构性质：基层群众性自治组织。',
 '主要观察：社区公共事务、居民参与及协助政府工作。'],PURPLE,FILLS[2])
card(d,(65,1020,1375,1255),'街道与居委会怎样联系？',[
 '街道给予指导、支持和帮助；居委会协助开展工作。',
 '协助任务还需要相应经费、条件与工作保障。'],TEAL,'#FFFFFF',30)
para(d,80,1280,'依据原书第一节及2025年修订的城市居民委员会组织法概括。具体权限与人员身份需分别确认。',1280,27,line=43)
im.save(OUT/'01-街道乡镇与自治组织.png')

im,d=canvas('级别与实权：四种岗位的取舍','依据原书图4-3重绘；类别用于分析，具体处境还要看岗位和地方条件。',1330)
# 纵轴向上级别较高，横轴向右实权较大；保留原书象限编号。
arrow(d,(720,1080),(720,222),INK);arrow(d,(90,650),(1350,650),INK)
text(d,744,207,'级别较高',27);text(d,1193,663,'实权较大',27)
text(d,83,663,'实权较小',27);text(d,744,1060,'级别较低',27)
card(d,(80,290,665,600),'Ⅱ类：实权小、级别高',[
 '竞争相对少，“实惠”较少',
 '作者框架：压力相对小'],TEAL,FILLS[1],30)
card(d,(775,290,1360,600),'Ⅰ类：实权大、级别高',[
 '竞争较多，“实惠”较多',
 '作者框架：压力相对小'],BLUE,FILLS[0],30)
card(d,(80,725,665,1035),'Ⅲ类：实权小、级别低',[
 '竞争相对少，“实惠”较少',
 '作者框架：压力相对大'],PURPLE,FILLS[2],30)
card(d,(775,725,1360,1035),'Ⅳ类：实权大、级别低',[
 '竞争较多，“实惠”较多',
 '作者框架：压力相对大'],COLORS[3],FILLS[3],30)
para(d,80,1125,'“实惠”沿用原书用语；图示并非测量结果，也不代表同一单位每个岗位的实际工作压力。',1280,28,line=45)
im.save(OUT/'02-四类岗位分析.png')

im,d=canvas('乡镇公务员流动：先看清两个分母','北方某县2011—2021年招录；统计截至2021年。依据原书表4-6、图4-5。',1430)
card(d,(65,215,1375,445),'第一层：319名招录者',[
 '120人离开原录用乡镇，占319人的37.6%。',
 '其余199人未计入离开者，占62.4%。'],BLUE,FILLS[0])
card(d,(65,465,1375,650),'第二层：仅观察已经离开的120人',[
 '下列去向的分母均为120人，不能换用319人。'],TEAL,FILLS[1])
data=[('市直机关',68),('县直机关',29),('市直以上机关',16),('辞职',7)]
for i,(label,n) in enumerate(data):
 y=710+i*112
 text(d,85,y,label,31,b=True)
 d.rounded_rectangle((400,y+7,1110,y+51),12,fill=GRID)
 d.rounded_rectangle((400,y+7,400+710*n/120,y+51),12,fill=COLORS[i])
 text(d,1140,y,f'{n}人 / {n/120:.1%}',29,c=COLORS[i],b=True)
para(d,80,1188,'这里的“离开”包含不同流动方式，不等于全部晋升。不同入职批次观察时长不同，也不能视为全国年度流动率。',1280,29,line=47)
im.save(OUT/'03-乡镇公务员流动.png')

im,d=canvas('村级治理：组织职责与人员兼任分别看','依据原书第四节、2025年村委会组织法修改及农村基层干部廉洁履职规定概括。',1530)
card(d,(240,220,1200,400),'村党组织',[
 '领导和支持村委会履职，支持和保障村民自治。'],BLUE,FILLS[0])
arrow(d,(720,410),(720,478));text(d,760,421,'领导和支持',29,c=TEAL)
card(d,(240,490,1200,670),'村民委员会',[
 '办理公共事务和公益事业，依相应程序开展工作。'],TEAL,FILLS[1])
arrow(d,(390,835),(390,682),BLUE);text(d,80,733,'依法决定相关事项',28,c=BLUE)
arrow(d,(1050,835),(1050,682),PURPLE);text(d,1075,733,'履行村务监督',28,c=PURPLE)
card(d,(65,850,690,1120),'村民会议或代表会议',[
 '依照法律规定和相应权限，',
 '讨论决定有关重大事项。'],BLUE,FILLS[0],30)
card(d,(750,850,1375,1120),'村务监督机构',[
 '参与民主理财，',
 '监督村务公开等制度落实。'],PURPLE,FILLS[2],30)
card(d,(65,1170,1375,1360),'“一肩挑”是人员依法兼任',[
 '兼任不合并组织职责，重大事项仍需依适用程序办理。'],TEAL,'#FFFFFF',30)
im.save(OUT/'04-村级治理与监督.png')

sheet=Image.new('RGB',(1440,1600),GRID)
for i,p in enumerate(sorted(OUT.glob('*.png'))):
 q=Image.open(p).convert('RGB');q.thumbnail((680,720));x=i%2*720;y=i//2*800
 sheet.paste(q,(x+(720-q.width)//2,y+55))
 ImageDraw.Draw(sheet).text((x+15,y+15),p.name,font=font(24),fill=INK)
sheet.save(ROOT/'配图核对.png')
print(json.dumps({'images':[p.name for p in sorted(OUT.glob('*.png'))]},ensure_ascii=True))
