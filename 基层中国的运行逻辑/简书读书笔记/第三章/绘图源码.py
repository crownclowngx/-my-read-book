"""第三章读后感：三张自绘概念图与一张原书表。Pillow + 微软雅黑。"""
from pathlib import Path
import shutil,json
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80'
BLUE='#276CB0';PURPLE='#7852A1';GRID='#D8E2E6'

def font(n,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',n)

def text(d,x,y,s,n=32,c=INK,b=False):
    d.text((x,y),s,font=font(n,b),fill=c)

def para(d,x,y,s,w,n=32,c=MUTED,b=False,line=51):
    rows=[];buf=''
    for ch in s:
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
    text(d,65,h-69,'《基层中国的运行逻辑》第三章读后感 · 自绘 · 2026-10-23',25)
    return im,d

def card(d,box,title,lines,color,fill):
    l,t,r,b=box;d.rounded_rectangle(box,22,fill=fill,outline=color,width=3)
    y=para(d,l+32,t+22,title,r-l-64,37,color,True,line=57)
    for label,body in lines:
        y+=15
        y=para(d,l+32,y,label+body,r-l-64,32,INK,line=51)
    assert y<=b-20,(title,y,b)

im,d=canvas('县委书记：作用来自哪里，边界在哪里？','组织位置、作用方式和约束条件，需要放在同一幅图中理解。',1340)
card(d,(65,222,1375,458),'组织位置：主持党委全面工作',[
    ('角色：','组织常委会活动，协调成员工作。'),
    ('区分：','个人承担的职责，与集体决策的职责范围。')],BLUE,'#E8F0FA')
card(d,(65,494,1375,730),'作用方式：组织决策与协调资源',[
    ('直接职责：','依照职责和程序推进工作。'),
    ('协调影响：','跨部门沟通，争取其他主体支持。')],TEAL,'#E5F2F0')
card(d,(65,766,1375,1053),'约束条件：上级、分工、程序和监督',[
    ('组织边界：','行政层次、部门职责与不同管理关系。'),
    ('运行条件：','依照程序作决定，并承担责任、接受监督。')],PURPLE,'#F0EAF7')
para(d,80,1093,'依据原书第一节及地方党委工作条例概括；这是概念图，具体事项仍需核对相应权限与程序。',1280,29,line=47)
im.save(OUT/'01-县委书记的作用与边界.png')

im,d=canvas('常务、主持工作、代理：分别看什么？','名称提供线索，工作范围和相互关系还要看实际依据。',1420)
card(d,(65,222,1375,512),'常务副职',[
    ('常见情境：','按分工持续承担日常事务和有关业务。'),
    ('判断依据：','班子分工、职责安排与具体协调授权。')],BLUE,'#E8F0FA')
card(d,(65,550,1375,840),'主持工作的副职',[
    ('常见情境：','正职空缺等情况下，由副职承担相应工作。'),
    ('判断依据：','主持工作的具体安排、范围及期限。')],TEAL,'#E5F2F0')
card(d,(65,878,1375,1168),'代理职务',[
    ('常见情境：','依相应程序代理某项职务。'),
    ('判断依据：','任命依据、法定程序与实际职责。')],PURPLE,'#F0EAF7')
para(d,80,1200,'依据原书第三节整理。不能仅从“常务”或“主持”推导统一级别，以及所有其他成员的汇报关系。',1280,29,line=47)
im.save(OUT/'02-常务主持与代理.png')

im,d=canvas('判断职务含权量，逐项问三个问题','三个维度用于定性观察；比较时需要说明具体事项与地方条件。',1460)
card(d,(65,222,1375,512),'01 处在什么行政层次？',[
    ('先确认：','机构本身、所任领导职务与其他兼职。'),
    ('再区分：','个人配备、机构层次与实际职责。')],BLUE,'#E8F0FA')
card(d,(65,550,1375,840),'02 参与哪些人员事项？',[
    ('看对象：','人员与岗位的重要性、管理范围。'),
    ('看环节：','日常管理、提名、考察或任免。')],TEAL,'#E5F2F0')
card(d,(65,878,1375,1168),'03 对哪些预算与资源负责？',[
    ('看范围：','具体资源、预算事项与项目。'),
    ('看环节：','编制、审核、执行或监督。')],PURPLE,'#F0EAF7')
para(d,80,1202,'同级岗位仍可能有不同资源条件；岗位影响力、公共任务的重要性与个人贡献，需分别判断。',1280,29,line=47)
im.save(OUT/'03-职务含权量的三个维度.png')

shutil.copy2(ROOT.parent.parent/'第三章 基层首长的权力清单/img/表3-1.png',OUT/'04-原书县域职务层级.png')
sheet=Image.new('RGB',(1440,1510),GRID)
for i,p in enumerate(sorted(OUT.glob('*.png'))):
    im=Image.open(p).convert('RGB');im.thumbnail((670,670));x=i%2*720;y=i//2*750
    sheet.paste(im,(x+(720-im.width)//2,y+58))
    ImageDraw.Draw(sheet).text((x+16,y+13),p.name,font=font(24),fill=INK)
sheet.save(ROOT/'配图核对.png')
print(json.dumps({'images':[p.name for p in sorted(OUT.glob('*.png'))]},ensure_ascii=True))
