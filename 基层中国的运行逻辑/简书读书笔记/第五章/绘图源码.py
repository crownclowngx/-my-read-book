"""第五章简书读后感：四张依据原书和注明资料自绘的中文图。"""
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
 text(d,65,h-69,'《基层中国的运行逻辑》第五章读后感 · 自绘 · 2026-10-25',25)
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

im,d=canvas('县委书记的日常：事务与角色','依据原书对纪录片《书记》的归纳；四类事务不表示时间占比。',1430)
card(d,(65,220,695,490),'开会与见人',['听取情况、研究工作','协调企业问题、接待来访'],BLUE,FILLS[0])
card(d,(745,220,1375,490),'应酬与其他事务',['片中饮酒、接待等交往','参加活动、处理现场求助'],TEAL,FILLS[1])
text(d,65,545,'理解这些场景，还要看两个角度',36,b=True)
card(d,(65,625,695,1090),'作为“官”',['组织与协调的影响力','上级、程序和资源的约束','公共职责与结果责任'],BLUE,FILLS[0])
card(d,(745,625,1375,1090),'作为“人”',['利益、声誉与工作目标','情绪、精力与交往需要','合理激励与行为约束'],PURPLE,FILLS[2])
para(d,80,1150,'日常活动提供观察线索；工作的评价还要看实际结果、履职程序与权力监督。',1280,32,line=53)
im.save(OUT/'01-县委书记的日常与角色.png')

im,d=canvas('维稳、招商、借债：三项任务怎样联系','依据原书第一节第二小节整理；共同条件用于分析，不表示必然因果。',1510)
card(d,(65,225,1375,460),'维稳：回应诉求与防范风险',['观察：信访、社会治安、安全生产','追问：问题如何核实、怎样妥善解决？'],BLUE,FILLS[0])
card(d,(65,500,1375,735),'招商：发展产业与培育财力',['观察：企业、就业、税源与公共投入','追问：项目适合当地吗，投入和长期责任是什么？'],TEAL,FILLS[1])
card(d,(65,775,1375,1010),'借债：资金安排与未来偿还',['观察：债务主体、预算约束、成本与期限','追问：谁依法承担责任，未来靠什么偿还？'],PURPLE,FILLS[2])
text(d,80,1070,'三项工作都需要核对的条件',36,b=True)
para(d,80,1140,'可用财力与人员时间  ·  部门协作与法定程序\n当期任务与长期影响  ·  公共服务与风险承担',1280,33,INK,line=63)
para(d,80,1305,'政府债务、平台企业债务与隐性债务需要分别辨认。本图不提供融资操作流程。',1280,27,line=44)
im.save(OUT/'02-三项挑战的联系.png')

im,d=canvas('县与乡镇：先比较工作位置，再讨论压力','依据原书第二节第一小节概括；具体安排因地区和时期而异。',1640)
text(d,95,220,'县：较完整的统筹范围',36,BLUE,True)
text(d,780,220,'乡镇：更接近落实现场',36,TEAL,True)
for y,title,left,right in [
 (310,'功能',['通过部门体系组织任务','协调县域内不同单位'],['承接具体任务、组织落实','内部机构与人员较有限']),
 (650,'压力',['统筹财政与公共支出','考虑招商和产业布局'],['现场工作、应急与配合','承接条件取决于具体地方']),
 (990,'工作方式',['部门与乡镇之间的统筹','专业分工与综合协调'],['多头对接与入户走访','沟通、核实和现场组织'])]:
 text(d,65,y-33,title,30,b=True)
 card(d,(65,y+25,695,y+280),left[0],[left[1]],BLUE,FILLS[0],30)
 card(d,(745,y+25,1375,y+280),right[0],[right[1]],TEAL,FILLS[1],30)
para(d,80,1365,'乡镇执行包含具体判断与协调；村委会具有自治组织性质。\n比较工作责任的结构，不等于给个人辛苦程度作统一排序。',1280,29,line=49)
im.save(OUT/'03-县与乡镇的差别.png')
imgs=[Image.open(x) for x in sorted(OUT.glob('*.png'))]
thumbs=[]
for im in imgs:
 im.thumbnail((480,580));thumbs.append(im.copy())
proof=Image.new('RGB',(1440,580),'#dde5e8')
for i,im in enumerate(thumbs):proof.paste(im,(i*480,0))
proof.save(ROOT/'配图核对.png')
print('3 figures complete')
