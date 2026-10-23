"""第二章读后感：三张自绘概念图与一张原书图。使用Pillow及微软雅黑。"""
from pathlib import Path
import math, shutil, json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'img'
OUT.mkdir(exist_ok=True)
BG='#F5F8FA'; INK='#173B48'; MUTED='#526A75'; TEAL='#087F80'
BLUE='#276CB0'; PURPLE='#7852A1'; GRID='#D8E2E6'

def font(n, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc', n)

def text(d,x,y,s,n=32,c=INK,b=False):
    d.text((x,y),s,font=font(n,b),fill=c)

def paragraph(d,x,y,s,w,n=31,c=MUTED,b=False,line=48):
    rows=[]; buf=''
    for ch in s:
        if d.textlength(buf+ch,font=font(n,b))>w:
            rows.append(buf);buf=ch
        else:buf+=ch
    if buf:rows.append(buf)
    for i,row in enumerate(rows):text(d,x,y+i*line,row,n,c,b)
    return y+len(rows)*line

def canvas(title,sub,h):
    im=Image.new('RGB',(1440,h),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1440,12),fill=TEAL)
    text(d,65,43,title,44,b=True)
    paragraph(d,68,119,sub,1304,29)
    d.line((65,h-94,1375,h-94),fill=GRID,width=2)
    text(d,65,h-70,'《基层中国的运行逻辑》第二章读后感 · 自绘 · 2026-10-23',25)
    return im,d

def card(d,box,title,body,color,fill,title_size=36):
    l,t,r,b=box;d.rounded_rectangle(box,20,fill=fill,outline=color,width=3)
    y=paragraph(d,l+28,t+24,title,r-l-56,title_size,color,True,line=52)
    y=paragraph(d,l+28,y+18,body,r-l-56,31,INK,line=48)
    assert y<b-18,(title,y,b)

def arrow(d,a,b,color=TEAL):
    d.line((a,b),fill=color,width=5)
    ang=math.atan2(b[1]-a[1],b[0]-a[0]);size=17
    d.polygon([b,(b[0]-size*math.cos(ang-.5),b[1]-size*math.sin(ang-.5)),(b[0]-size*math.cos(ang+.5),b[1]-size*math.sin(ang+.5))],fill=color)

# 保留原书图像像素与2024年统计背景，不重写为当前数量。
source=ROOT.parent.parent/'第二章 等级制是行政资源分配的主要方式/img/图2-2.png'
shutil.copy2(source,OUT/'01-中国城市的等级.png')

im,d=canvas('读懂一个职位，分清四件事','四个观察角度互相联系，需要结合具体机构、岗位与制度判断。',1110)
card(d,(65,220,695,520),'机构级别','这个机构在组织体系中处于什么位置？先确认机构，再判断所属岗位。',BLUE,'#E8F0FA')
card(d,(745,220,1375,520),'领导职务及其层次','担任什么领导岗位？承担哪些领导职责？完整任职信息是判断依据。',TEAL,'#E5F2F0')
card(d,(65,565,695,865),'个人职级','与领导职务并行的晋升序列。职级本身不具有领导职责。',PURPLE,'#F0EAF7')
card(d,(745,565,1375,865),'实际职责与权限','对一项具体事项能决定什么？继续看岗位分工、授权和适用制度。',BLUE,'#E8F0FA')
paragraph(d,80,908,'依据原书第二节及《公务员职务与职级并行规定》概括；这是概念比较，不是四级晋升阶梯。',1280,29)
im.save(OUT/'02-机构职务职级与职责.png')

im,d=canvas('西气东输：一个项目怎样逐步落地','依据原书第四节的历史案例，按九个环节梳理；不代表所有项目的统一程序。',1710)
steps=['基层单位提出想法','向主管领导汇报','主管领导实地视察','向中央领导报告','中央领导作出批示','有关部委调研论证','中央开会审批','成立领导小组推进','项目实施']
for i,label in enumerate(steps):
    y=215+i*137
    color=[BLUE,TEAL,PURPLE][i//3]
    d.rounded_rectangle((220,y,1220,y+100),18,fill='white',outline=color,width=3)
    d.ellipse((247,y+21,305,y+79),fill=color)
    text(d,264,y+26,str(i+1),30,'white',True)
    text(d,340,y+25,label,36,INK,True)
    if i<8:arrow(d,(720,y+107),(720,y+130),color)
paragraph(d,95,1487,'推进中仍需协调：项目论证、资源支持、地方需求与管网利益。获得认可后，还要落实实施条件。',1250,30)
im.save(OUT/'03-西气东输项目推进.png')

im,d=canvas('昆山：地方探索怎样获得正式认可','按原书案例的关键节点整理，观察横向合作、地方行动与上层认可。',1490)
timeline=[
 ('1981','横向合作','与上海企业合作建设生产基地，在合作中扩大地方发展机会。',BLUE,'#E8F0FA'),
 ('1985','自费工业新区','地方先行组织建设，通过实际发展逐步展现可行性。',TEAL,'#E5F2F0'),
 ('1988','专家与媒体推动','专家考察与公开报道扩大影响，使地方探索获得更多关注。',PURPLE,'#F0EAF7'),
 ('1992','正式获批','开发区取得国家级资格，地方探索与正式制度进一步衔接。',BLUE,'#E8F0FA')]
for i,(year,title,body,c,fill) in enumerate(timeline):
    y=215+i*268
    text(d,78,y+25,year,43,c,True)
    d.ellipse((248,y+37,270,y+59),fill=c)
    if i<3:d.line((259,y+62,259,y+302),fill=GRID,width=5)
    card(d,(315,y,1360,y+225),title,body,c,fill)
paragraph(d,80,1310,'历史案例用于理解探索与认可的互动；具体做法需放回当时的改革环境。',1290,29)
im.save(OUT/'04-昆山探索与认可.png')

sheet=Image.new('RGB',(1440,1480),GRID)
for i,p in enumerate(sorted(OUT.glob('*.png'))):
    im=Image.open(p).convert('RGB');im.thumbnail((670,665))
    x=i%2*720;y=i//2*740
    sheet.paste(im,(x+(720-im.width)//2,y+55))
    ImageDraw.Draw(sheet).text((x+18,y+12),p.name,font=font(24),fill=INK)
sheet.save(ROOT/'配图核对.png')
print(json.dumps({'images':[p.name for p in sorted(OUT.glob('*.png'))]},ensure_ascii=True))
