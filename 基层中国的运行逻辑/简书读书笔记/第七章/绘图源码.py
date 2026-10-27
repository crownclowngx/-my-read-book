"""第七章读后感配图。运行需要 Pillow 与 Windows 微软雅黑字体。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80'
BLUE='#276CB0';PURPLE='#7852A1';ORANGE='#A15B27';GRID='#D8E2E6'
FILLS=['#E8F0FA','#E5F2F0','#F0EAF7','#FAF0E5']

def font(n,bold=False):
 return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',n)
def text(d,x,y,s,n=34,c=INK,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def para(d,x,y,s,w,n=34,c=INK,b=False,line=54):
 rows=[];buf=''
 for ch in s:
  if ch=='\n':rows.append(buf);buf='';continue
  if d.textlength(buf+ch,font=font(n,b))>w:rows.append(buf);buf=ch
  else:buf+=ch
 if buf:rows.append(buf)
 for j,row in enumerate(rows):text(d,x,y+j*line,row,n,c,b)
 return y+len(rows)*line
def canvas(title,sub,h):
 im=Image.new('RGB',(1440,h),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1440,12),fill=TEAL);text(d,65,43,title,44,b=True)
 para(d,68,120,sub,1300,29,MUTED,line=46)
 d.line((65,h-94,1375,h-94),fill=GRID,width=2)
 text(d,65,h-69,'《基层中国的运行逻辑》第七章读后感 · 自绘 · 2026-10-27',25)
 return im,d
def card(d,box,title,lines,color,fill,n=34):
 l,t,r,b=box;d.rounded_rectangle(box,22,fill=fill,outline=color,width=3)
 y=para(d,l+28,t+20,title,r-l-56,38,color,True,line=58)
 for s in lines:y=para(d,l+28,y+12,s,r-l-56,n,INK,line=53)
 assert y<=b-15,(title,y,b)
def arrow(d,p,q,c=TEAL,width=5):
 d.line((p,q),fill=c,width=width);a=math.atan2(q[1]-p[1],q[0]-p[0]);l=19
 d.polygon([q,(q[0]-l*math.cos(a-.5),q[1]-l*math.sin(a-.5)),(q[0]-l*math.cos(a+.5),q[1]-l*math.sin(a+.5))],fill=c)

im,d=canvas('政企关系：联系紧密，还要看怎样互动','依据原书图7-1重绘；两个维度共同区分四种关系。',1570)
arrow(d,(720,1360),(720,255),MUTED);arrow(d,(85,780),(1375,780),MUTED)
text(d,755,250,'合法合规',32,TEAL,True);text(d,755,1330,'违法违规',32,ORANGE,True)
text(d,90,803,'政府较少干预',30,MUTED);text(d,1120,803,'政府较多干预',30,MUTED)
card(d,(110,350,650,700),'政企分治',['政府与企业各守其界','各自按规则开展活动'],BLUE,FILLS[0],34)
card(d,(790,350,1330,700),'政企合作',['双方持续协调与合作','互动遵守规则和程序'],TEAL,FILLS[1],34)
card(d,(110,895,650,1245),'政企伤害',['违规或失信造成损失','可能单方或相互伤害'],ORANGE,FILLS[3],34)
card(d,(790,895,1330,1245),'政企合谋',['通过违规方式交换利益','可能损害公共利益'],PURPLE,FILLS[2],34)
text(d,100,1410,'判断具体关系，需要项目、行为与制度证据。',32,b=True)
im.save(OUT/'01-政企关系的四种类型.png')

im,d=canvas('土地财政：产业、城市与收入怎样联系','依据原书图7-4及第二节论述整理；图中不表示必然盈利。',1660)
card(d,(65,225,1375,430),'公共投入：土地整理与基础设施',['园区、道路和公共设施需要前期投入，也有后续维护成本。'],BLUE,FILLS[0],34)
arrow(d,(390,450),(390,505));arrow(d,(1050,450),(1050,505))
card(d,(65,525,705,1060),'工业用地与产业发展',['较低的用地成本吸引企业','配套生产、服务和就业','经营活动形成相关税源','能否实现取决于实际经营'],TEAL,FILLS[1],35)
card(d,(750,525,1375,1060),'商住用地与城市发展',['产业与人口形成空间需求','土地出让形成出让收入','建设与交易涉及相关税收','收入受供求和市场影响'],PURPLE,FILLS[2],35)
arrow(d,(390,1080),(390,1160));arrow(d,(1050,1080),(1050,1160))
card(d,(65,1185,1375,1425),'地方财力与持续支出',['不同收入按预算制度管理；毛收入还需考虑相关成本。','后续建设和公共服务，不能只依赖土地收入持续增长的预期。'],BLUE,FILLS[0],34)
text(d,80,1495,'税收、土地出让收入与可支配收益，需要分别理解。',32,b=True)
im.save(OUT/'02-土地财政与地方建设.png')

im,d=canvas('地方债：形成机制与两类治理办法','依据原书第三节整理；不同地区的作用条件与程度存在差异。',1770)
card(d,(65,225,705,500),'地区竞争与发展动力',['争取产业、就业和税源','投资需求可能先于收入形成'],BLUE,FILLS[0],34)
card(d,(750,225,1375,500),'资源与信用动员',['土地、资产与融资条件','影响地方能够筹集多少资金'],TEAL,FILLS[1],34)
card(d,(65,550,705,825),'决策与权力约束',['谁决定项目和投资规模','预算与监督能否有效约束'],PURPLE,FILLS[2],34)
card(d,(750,550,1375,825),'资金参与方的利益',['平台、金融机构与中介','信息与责任是否清楚透明'],ORANGE,FILLS[3],34)
arrow(d,(720,855),(720,900));text(d,190,925,'共同影响借款规模、资金用途与风险承担',34,b=True)
card(d,(65,1040,705,1505),'短期化债：缓解集中压力',['协调偿还时间与融资成本','优化资产负债及项目运营','在适用规则下引入市场参与','争取时间，仍有未来责任'],TEAL,FILLS[1],34)
card(d,(750,1040,1375,1505),'长期限债：约束无序扩张',['调整政府职能和投资方式','完善决策程序与权力约束','公开债务与偿还责任信息','改善未来投入和经营质量'],BLUE,FILLS[0],34)
text(d,80,1590,'政府债务、隐性债务与平台企业债务，先分清范围。',32,b=True)
im.save(OUT/'03-地方债的成因与治理.png')

im,d=canvas('县域电商：把市场机会变成持续经营','依据原书第四节整理；交易、交付与本地就业需要一起观察。',2010)
stages=[
 ('产地生产','生产组织、日常管理与用工','食品安全','生产条件与信任'),
 ('分级与加工','规格、检验、包装与品控','标准化','稳定品质与预期'),
 ('线上经营','选品、内容、获客与客服','专业人才','运营能力与成本'),
 ('仓储与寄递','保鲜、冷链、时效与运输','物流成本','损耗与交付质量'),
 ('售后与反馈','处理争议、复购与改进','持续协作','质量与经营反馈')]
text(d,85,220,'经营环节',35,BLUE,True);text(d,960,220,'需要解决的问题',35,PURPLE,True)
for j,(title,desc,issue,sub) in enumerate(stages):
 y=295+j*250
 card(d,(65,y,875,y+190),title,[desc],BLUE,FILLS[0],33)
 card(d,(940,y,1375,y+190),issue,[sub],PURPLE,FILLS[2],32)
 if j<4:arrow(d,(470,y+203),(470,y+238))
 d.line((890,y+95,925,y+95),fill=GRID,width=4)
card(d,(65,1620,1375,1850),'公共服务提供共用支持',['基础设施、质量服务和人才培养，为经营创造条件。','具体岗位和收益留在哪里，需要回到本地参与环节判断。'],TEAL,FILLS[1],32)
im.save(OUT/'04-县域电商的经营与就业.png')

proof=Image.new('RGB',(1440,1020),'#DDE5E8')
for j,p in enumerate(sorted(OUT.glob('*.png'))):
 im=Image.open(p);im.thumbnail((720,510));proof.paste(im,(j%2*720+(720-im.width)//2,j//2*510))
proof.save(ROOT/'配图核对.png')
print('4 figures complete')
