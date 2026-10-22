"""第十章四张自绘概念图；Pillow + 微软雅黑。原书界面图单独复制。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,json,shutil
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80';BLUE='#276CB0';PURPLE='#7852A1';RED='#B34F4F';GRID='#D8E2E6'
checks=[]
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def text(d,x,y,s,n=27,c=INK,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def wrap(d,s,n,width,b=False):
 result=[];line=''
 for ch in s:
  if ch=='\n':result.append(line);line='';continue
  if d.textlength(line+ch,font=font(n,b))>width:result.append(line);line=ch
  else:line+=ch
 if line:result.append(line)
 return result
def canvas(title,sub,h):
 im=Image.new('RGB',(1400,h),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1400,12),fill=TEAL);text(d,60,40,title,42,b=True)
 text(d,62,111,sub,25,MUTED)
 d.line((60,h-80,1340,h-80),fill=GRID,width=2)
 text(d,60,h-57,'《AI工程》第十章读书笔记 · 自绘学习示意 · 2026-10-22',23,MUTED)
 return im,d
def card(d,rect,title,body=(),c=TEAL,fill='#E5F2F0',n=27):
 x,y,r,b=rect;d.rounded_rectangle(rect,18,fill=fill,outline=c,width=3)
 ts=wrap(d,title,30,r-x-40,True);yy=y+15
 for line in ts:text(d,x+20,yy,line,30,c,True);yy+=42
 yy+=12
 for s in body:
  for line in wrap(d,s,n,r-x-40):text(d,x+20,yy,line,n);yy+=40
 assert yy<=b-7,(title,yy,b)
 checks.append(dict(title=title,box=rect,textBottom=yy))
def arrow(d,a,b,c=TEAL,w=5):
 d.line((a,b),fill=c,width=w);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=17
 d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=c)
def label(d,y,s):text(d,70,y,s,30,b=True)
def save(im,name):im.save(OUT/name)

im,d=canvas('从模型调用到完整应用','先说明新增能力，再检查它引入的成本、边界与失败方式。',1470)
for top,bottom in [(185,410),(445,675),(710,940),(975,1315)]:
 d.rounded_rectangle((55,top,1345,bottom),16,fill='white',outline=GRID,width=2)
label(d,200,'1  最简调用：把问题交给模型')
card(d,(95,260,375,390),'用户查询',[],n=25)
card(d,(560,260,840,390),'模型生成',[],BLUE,'#E8F0FA')
card(d,(1025,260,1305,390),'返回响应',[],n=25)
arrow(d,(375,325),(540,325));arrow(d,(840,325),(1005,325))
label(d,460,'2  增强上下文：提供当前任务需要的依据')
card(d,(95,520,415,655),'问题与条件',['身份、日期、逐晚费用'],n=24)
card(d,(540,520,860,655),'有效资料与工具',['来源、版本、读取权限'],BLUE,'#E8F0FA',24)
card(d,(985,520,1305,655),'模型生成',['形成带依据的回答'],n=24)
arrow(d,(415,587),(520,587));arrow(d,(860,587),(965,587))
label(d,725,'3  加入防护：识别风险，并安排失败处理')
card(d,(95,785,415,920),'输入与资料边界',['敏感字段、访问范围'],n=24)
card(d,(540,785,860,920),'模型与工具建议',['保留任务条件与来源'],BLUE,'#E8F0FA',24)
card(d,(985,785,1305,920),'输出核查',['质量、安全与后续策略'],PURPLE,'#F0EAF7',24)
arrow(d,(415,852),(520,852));arrow(d,(860,852),(965,852))
label(d,990,'4  完成任务：保存状态，允许追问、循环与受控写入')
for x,title,body,c,fill in [
 (95,'任务状态',['问题、条件','当前进度'],TEAL,'#E5F2F0'),
 (410,'检索与生成',['取得依据','提出响应或动作'],BLUE,'#E8F0FA'),
 (725,'核验与执行',['权限、参数','校核后创建草稿'],PURPLE,'#F0EAF7'),
 (1040,'结果与下一步',['核对真实状态','完成或继续'],TEAL,'#E5F2F0')]:
 card(d,(x,1055,x+265,1240),title,body,c,fill,24)
 if x<1040:arrow(d,(x+265,1145),(x+295,1145),c)
text(d,95,1262,'条件不足时追问；未完成时进入下一轮；重试与循环都需要结束条件。',26,MUTED)
text(d,70,1340,'路由选择处理路径，网关统一模型接入，缓存复用有效结果；位置按需求设计。',26,MUTED)
save(im,'01-架构演进.png')

im,d=canvas('一次任务怎样留下可核查的记录','先关联步骤与版本，再用必要证据定位问题。',1230)
card(d,(65,185,1335,355),'任务 T-01：核对住宿金额并创建草稿',[
 '明确用户范围、必要条件和完成标准；以同一任务标识关联各步骤。',
 '示例：逐晚金额尚未齐备时，先追问；此时不直接确定可报金额。'],n=27)
for x,title,body,c,fill in [
 (65,'1 检索',['索引与制度版本','来源 / 读取状态'],TEAL,'#E5F2F0'),
 (395,'2 生成',['模型与提示词版本','结论 / 引用'],BLUE,'#E8F0FA'),
 (725,'3 核查',['规则与检查版本','通过 / 追问 / 转接'],PURPLE,'#F0EAF7'),
 (1055,'4 工具',['工具与业务标识','实际写入状态'],TEAL,'#E5F2F0')]:
 card(d,(x,460,x+280,670),title,body,c,fill,25)
 if x<1055:arrow(d,(x+280,560),(x+310,560),c)
arrow(d,(700,355),(700,430))
card(d,(65,775,1335,985),'记录与调查',[
 '各步骤关联任务、版本、状态、耗时；必要时保存受控证据引用。',
 '金额有误：查有效制度与逐晚条件。草稿未出现：查工具执行与业务状态。',
 '采集内容按定位需要设计，并控制访问与保留范围。'],BLUE,'#E8F0FA',27)
for x in [205,535,865,1195]:arrow(d,(x,670),(x,750),BLUE)
text(d,65,1030,'指标观察整体变化；日志记录事件；追踪关联一次任务经过的步骤。',29,b=True)
text(d,65,1085,'示例标识不代表真实系统，图中不展示未经运行的耗时或性能成绩。',26,MUTED)
save(im,'02-任务追踪.png')

im,d=canvas('从用户行为到可以使用的反馈','观察行为，提出多种解释，再结合任务证据核查。',1160)
for x,title in [(65,'观察到什么'),(475,'可能意味着什么'),(885,'还需检查什么')]:text(d,x+15,190,title,31,TEAL,True)
for y,act,why,evidence in [
 (260,'重新生成',['对当前答案不满意','也可能想比较表达'],['后续采用哪一版','是否继续纠错']),
 (490,'连续追问',['复杂任务正在推进','也可能反复误解'],['条件是否逐渐补齐','最终任务是否完成']),
 (720,'修改金额或条件',['纠正事实与条件','也可能记错了制度'],['有效制度与适用范围','逐晚费用及版本'])]:
 card(d,(65,y,405,y+180),act,[],n=26)
 card(d,(475,y,815,y+180),'候选解释',why,BLUE,'#E8F0FA',25)
 card(d,(885,y,1335,y+180),'核查证据',evidence,PURPLE,'#F0EAF7',25)
 arrow(d,(405,y+90),(455,y+90));arrow(d,(815,y+90),(865,y+90))
text(d,65,970,'表达偏好、事实正确性与工具完成状态，需要分别判断。',31,b=True)
text(d,65,1025,'同一行为允许多种原因；信号的含义取决于任务与上下文。',27,MUTED)
save(im,'03-反馈解释.png')

im,d=canvas('展示与反馈如何相互强化','用户只能选择已展示的内容，选择数据也受到展示机制影响。',1180)
card(d,(90,210,610,420),'1 展示倾向',['某类肯定回答更常出现','其他答案获得的展示机会较少'],n=28)
card(d,(790,210,1310,420),'2 用户选择',['更多展示带来更多选择机会','选择同时受任务与界面影响'],BLUE,'#E8F0FA',28)
card(d,(790,675,1310,885),'3 收集反馈',['点赞或采用进入反馈数据','若忽略曝光条件，容易误读'],PURPLE,'#F0EAF7',28)
card(d,(90,675,610,885),'4 更新策略',['强化已有的展示倾向','下一轮继续影响可见选项'],RED,'#F8ECEA',28)
arrow(d,(610,315),(765,315));arrow(d,(1050,420),(1050,650),BLUE)
arrow(d,(790,780),(635,780),PURPLE)
d.line(((90,780),(65,780),(65,315)),fill=RED,width=5)
arrow(d,(65,315),(90,315),RED)
text(d,285,505,'“更常被选择”需要结合展示机会解释',32,b=True)
text(d,308,562,'“用户更喜欢”还需与事实依据分别核查',28,MUTED)
text(d,90,970,'降低误读：记录展示条件，检查位置与样本偏差，核查业务正确性。',28,b=True)
text(d,90,1025,'此图说明可能的反馈路径，不代表已经完成因果实验。',27,MUTED)
save(im,'05-反馈循环.png')

shutil.copy2(ROOT.parent.parent/'第十章：AI工程架构与用户反馈/img/图10-19.png',OUT/'04-流程中的反馈.png')
thumbs=[]
for p in sorted(OUT.glob('*.png')):
 im=Image.open(p).convert('RGB');im.thumbnail((460,490))
 tile=Image.new('RGB',(480,535),'white');tile.paste(im,((480-im.width)//2,35))
 text(ImageDraw.Draw(tile),12,5,p.stem,17)
 thumbs.append(tile)
sheet=Image.new('RGB',(1440,1070),'#D8E2E6')
for i,t in enumerate(thumbs):sheet.paste(t,((i%3)*480,(i//3)*535))
sheet.save(ROOT/'配图核对.png')
(ROOT/'绘图布局核对.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('Created',len(thumbs),'figures;',len(checks),'text boxes checked')
