"""第一章读后感配图。Pillow绘制概念图，保留原书历史地图。"""
from pathlib import Path
import sys, math, shutil, json
sys.path.insert(0, r'C:\Users\crown\.cache\tooling\book-ocr')
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80';BLUE='#276CB0';PURPLE='#7852A1';GRID='#D8E2E6'
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def txt(d,x,y,s,n=29,c=INK,b=False):
    d.text((x,y),s,font=font(n,b),fill=c)
def centered(d,box,s,n=30,c=INK,b=False):
    l,t,r,bt=box;bb=d.textbbox((0,0),s,font=font(n,b))
    assert bb[2]-bb[0]<=r-l-16,(s,box)
    d.text(((l+r-bb[2]+bb[0])/2,(t+bt-bb[3]-bb[1])/2),s,font=font(n,b),fill=c)
def wrap(d,s,width,n,b=False):
    lines=[];buf=''
    for ch in s:
        if d.textlength(buf+ch,font=font(n,b))>width:
            lines.append(buf);buf=ch
        else:buf+=ch
    if buf:lines.append(buf)
    return lines
def para(d,x,y,s,width,n=28,c=MUTED,gap=44,b=False):
    ss=wrap(d,s,width,n,b)
    for i,line in enumerate(ss):txt(d,x,y+i*gap,line,n,c,b)
    return y+len(ss)*gap
def card(d,box,title,body='',c=TEAL,fill='#E5F2F0',title_n=31,body_n=28):
    l,t,r,b=box;d.rounded_rectangle(box,18,fill=fill,outline=c,width=3)
    end=para(d,l+24,t+20,title,r-l-48,title_n,c,42,True)
    if body:end=para(d,l+24,end+16,body,r-l-48,body_n,INK,43)
    assert end<b-12,(title,end,b)
def arrow(d,a,b,c=TEAL,dashed=False):
    x1,y1=a;x2,y2=b;dist=math.hypot(x2-x1,y2-y1)
    if dashed:
        for v in range(0,int(dist)-12,23):
            q=min(v+12,dist-12)
            d.line((x1+(x2-x1)*v/dist,y1+(y2-y1)*v/dist,x1+(x2-x1)*q/dist,y1+(y2-y1)*q/dist),fill=c,width=4)
    else:d.line((a,b),fill=c,width=5)
    ang=math.atan2(y2-y1,x2-x1);L=17
    d.polygon([b,(x2-L*math.cos(ang-.5),y2-L*math.sin(ang-.5)),(x2-L*math.cos(ang+.5),y2-L*math.sin(ang+.5))],fill=c)
def canvas(title,sub,h=1100):
    im=Image.new('RGB',(1440,h),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1440,12),fill=TEAL);txt(d,58,40,title,42,b=True)
    para(d,60,108,sub,1320,27)
    d.line((60,h-87,1380,h-87),fill=GRID,width=2)
    txt(d,60,h-64,'《基层中国的运行逻辑》第一章读后感 · 依据原书自绘 · 2026-10-22',23,MUTED)
    return im,d

# 01：垂直管理与属地管理分别示意，明确关系图例。
im,d=canvas('条与块：先分清两种管理关系','同一职能的纵向联系，可能是领导关系，也可能是业务指导。',1100)
for box in [(60,200,700,820),(740,200,1380,820)]:d.rounded_rectangle(box,20,fill='white',outline=GRID,width=2)
txt(d,92,230,'垂直管理示意',33,TEAL,True);txt(d,770,230,'属地管理示意',33,BLUE,True)
card(d,(195,330,565,445),'上级主管部门',c=TEAL)
card(d,(195,595,565,710),'本级主管部门',c=TEAL)
arrow(d,(380,460),(380,580));txt(d,410,503,'领导',29,TEAL)
card(d,(1055,330,1350,445),'上级业务部门',c=PURPLE,fill='#F0EAF7',title_n=29)
card(d,(1055,595,1350,710),'本级业务部门',c=BLUE,fill='#E8F0FA',title_n=29)
card(d,(770,595,1000,710),'本级政府',c=BLUE,fill='#E8F0FA',title_n=29)
arrow(d,(1202,460),(1202,580),PURPLE,True);txt(d,1231,503,'指导',28,PURPLE)
arrow(d,(1012,654),(1042,654),BLUE);txt(d,943,744,'领导 →',28,BLUE)
txt(d,130,754,'专业系统内的直接领导',28,MUTED)
txt(d,92,870,'实线：图示中的领导关系',28,TEAL)
txt(d,770,870,'虚线：业务指导关系',28,PURPLE)
para(d,92,925,'概念示意。具体机构的管理体制与事项权限，需要依据实际规定判断。',1250,27)
im.save(OUT/'01-条与块.png')

# 02：原书图直接复制，不重绘历史边界。
source=ROOT.parent.parent/'第一章“条块结合”是中国国家治理的根本特征'/'img/图1-9.png'
shutil.copy2(source,OUT/'02-江南省拆分.png')

# 03：治理成本条件链，明确中介作用与代理风险。
im,d=canvas('皇权不下县：直接治理的成本','地域、交通、通信与信息条件，共同影响治理的组织方式。',1180)
card(d,(130,200,1310,350),'交通通信不便、地方差异较大','人口、土地与灾情等资料，取得、更新和传递都需要成本。',c=BLUE,fill='#E8F0FA')
arrow(d,(720,368),(720,408),BLUE)
card(d,(130,425,1310,575),'直接掌握情况与监督执行的成本较高','增加官员以后，仍需要解决信息核验、资源投入与代理问题。',c=PURPLE,fill='#F0EAF7')
arrow(d,(720,593),(720,633),PURPLE)
card(d,(130,650,1310,800),'更多借助乡绅等地方中介','利用地方知识与组织能力，也面临中介自身的利益和权力问题。')
card(d,(130,860,1310,1035),'需要区分两个边界','正式官僚机构设置到哪里，与国家通过赋役等方式影响到哪里。',c=BLUE,fill='#E8F0FA',title_n=30)
im.save(OUT/'03-治理成本.png')

# 04：理论框架简化，分支标注模型条件，保留动态调整问题。
im,d=canvas('内外冲突与制度选择','作者模型：治理目标的权衡，需要结合资源、信息与协调成本。',1330)
card(d,(115,195,1325,340),'分析条件','外部威胁的程度  ·  交通网络与通信技术  ·  可用资源',c=BLUE,fill='#E8F0FA')
arrow(d,(720,355),(720,394),BLUE)
card(d,(295,410,1145,550),'内部稳定与外部稳定的权衡','不同条件下，两类目标的相对紧迫性与实现成本发生变化。',c=PURPLE,fill='#F0EAF7',title_n=31,body_n=27)
arrow(d,(485,567),(365,638),TEAL);arrow(d,(955,567),(1075,638),BLUE)
card(d,(65,655,695,1005),'分权：更重地方信息与行动','作者模型中，侧重应对外部防御压力时，更依赖地方激励与及时判断。',c=TEAL,body_n=28)
card(d,(745,655,1375,1005),'集权：更重统一协调与控制','作者模型中，侧重维护内部稳定时，更依赖协调、监督与地方力量约束。',c=BLUE,fill='#E8F0FA',body_n=28)
txt(d,94,899,'激励 · 能力 · 因地制宜',29,TEAL,True)
txt(d,94,945,'划界侧重“山川形便”',27,MUTED)
txt(d,775,899,'监督 · 忠诚 · 统一执行',29,BLUE,True)
txt(d,775,945,'划界侧重“犬牙交错”',27,MUTED)
arrow(d,(365,1022),(520,1075),TEAL);arrow(d,(1075,1022),(920,1075),BLUE)
card(d,(160,1090,1280,1220),'条件变化后，重新评估制度与配套安排',c=PURPLE,fill='#F0EAF7',title_n=31)
im.save(OUT/'04-双均衡框架.png')

thumbs=[]
for p in sorted(OUT.glob('*.png')):
    a=Image.open(p).convert('RGB');a.thumbnail((650,610));t=Image.new('RGB',(700,670),'white');t.paste(a,((700-a.width)//2,45));ImageDraw.Draw(t).text((18,10),p.name,font=font(22),fill=INK);thumbs.append(t)
preview=Image.new('RGB',(1400,1340),'#D8E2E6')
for i,t in enumerate(thumbs):preview.paste(t,((i%2)*700,(i//2)*670))
preview.save(ROOT/'配图核对.png')
print(json.dumps({'images':[p.name for p in sorted(OUT.glob('*.png'))]},ensure_ascii=False))
