"""生成第五章六张中文概念图。Pillow与Windows微软雅黑字体。"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80';BLUE='#276CB0';PURPLE='#7852A1';RED='#B34F4F';GRID='#D8E2E6'
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def txt(d,x,y,s,n=27,c=INK,b=False):
 assert d.textbbox((x,y),s,font=font(n,b))[2]<1380,(s,x,n)
 d.text((x,y),s,font=font(n,b),fill=c)
def lines(d,x,y,ss,n=27,gap=44,c=INK):
 for i,s in enumerate(ss):txt(d,x,y+i*gap,s,n,c)
def canvas(title,sub,h=1120):
 im=Image.new('RGB',(1400,h),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1400,12),fill=TEAL);txt(d,60,40,title,42,b=True);txt(d,62,110,sub,26,MUTED)
 d.line((60,h-83,1340,h-83),fill=GRID,width=2)
 txt(d,60,h-58,'《AI工程》第五章读书笔记 · 自绘学习示意 · 2026-10-17',23,MUTED)
 return im,d
def card(d,rect,title,body=(),c=TEAL,fill='#E5F2F0',n=27):
 x,y,r,b=rect;d.rounded_rectangle(rect,18,fill=fill,outline=c,width=3)
 assert d.textlength(title,font=font(31,True))<r-x-48,title
 assert all(d.textlength(s,font=font(n))<r-x-48 for s in body),(title,body)
 assert y+79+max(0,len(body)-1)*43+n<b-10,(title,'height')
 txt(d,x+24,y+19,title,31,c,True);lines(d,x+24,y+79,body,n,43)
def arrow(d,a,b,c=TEAL):
 d.line((a,b),fill=c,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=18
 d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=c)
def save(im,name):im.save(OUT/name)

im,d=canvas('把知识库问答交代清楚','任务描述、示例与具体任务参考原书5.1；背景资料提供本次回答的依据。',1150)
for y,title,body,c,fill in [
 (185,'任务描述',['按提供的制度回答，给出条件和出处；资料不足时说明缺口。'],TEAL,'#E5F2F0'),
 (365,'完成任务的示例',['展示怎样引用条款，以及缺少适用制度时怎样回应。'],BLUE,'#E8F0FA'),
 (545,'本次背景资料',['制度[P1]：2026年版、普通员工、A市、每晚最高600元。'],PURPLE,'#F0EAF7'),
 (725,'本次具体任务',['用户条件：普通员工、A市、住宿一晚650元；询问条款上限。'],TEAL,'#E5F2F0')]:
 card(d,(65,y,1335,y+140),title,body,c,fill,29)
txt(d,65,930,'示例展示处理方式；资料提供事实依据；问题说明本次需求。',29,b=True)
txt(d,65,980,'上述制度仅为学习示例，真实报销还需核对完整条件。',26,MUTED)
save(im,'01-提示词组成.png')

im,d=canvas('上下文长度与上下文效率','概念示意：判断信息是否适用，再检查模型能否正确使用。',1100)
card(d,(65,200,675,435),'能容纳多少信息',['上下文窗口以token计量','本次输入还包括指令与历史','窗口变大，也要核对使用效果'],BLUE,'#E8F0FA',27)
card(d,(725,200,1335,435),'信息是否对任务有用',['相关条款与完整适用条件','来源、版本和必要例外','避免无关内容淹没关键信息'],TEAL,'#E5F2F0',27)
card(d,(65,535,1335,715),'知识库问答需要保留',['普通员工 + A市 + 当前有效制度 + 每晚计量 + 金额上限 + 必要例外'],PURPLE,'#F0EAF7',28)
arrow(d,(370,435),(370,510),BLUE);arrow(d,(1030,435),(1030,510))
card(d,(65,810,1335,955),'检查实际利用效果',['固定问题与依据，改变无关资料数量或依据位置，比较结论、条件和引用。'],TEAL,n=27)
save(im,'02-上下文效率.png')

im,d=canvas('将复杂问答拆成可检查的步骤','顺序由依赖关系决定；多次调用会增加费用、延迟和信息传递环节。',1150)
rows=[(195,'1  定位适用条款',['保留来源、版本和原始片段'],'检查资料是否适用'),(435,'2  核对用户条件',['识别人员、地点、时间与缺失项'],'检查条件是否完整'),(675,'3  形成带依据的回答',['给出结论、出处和必要的追问'],'检查结论是否受支持')]
for i,(y,title,body,check) in enumerate(rows):
 card(d,(65,y,835,y+160),title,body,TEAL,n=28)
 card(d,(925,y,1335,y+160),'步骤检查',[check],BLUE,'#E8F0FA',25)
 arrow(d,(835,y+80),(905,y+80))
 if i<2:arrow(d,(450,y+160),(450,y+218))
txt(d,65,945,'每一步继续携带原始依据，避免中间摘要遗漏关键条件。',29,b=True)
save(im,'03-任务拆解.png')

im,d=canvas('让提示词修改留下可比较的证据','学习流程示意；开发材料与独立保留材料承担不同职责。',1140)
card(d,(65,195,610,380),'观察具体失败',['保存问题、资料、输出与评分','区分条件遗漏、编造与误拒'],TEAL,n=26)
card(d,(790,195,1335,380),'提出有目的的修改',['调整规则、上下文或示例','记录预期改善与运行条件'],BLUE,'#E8F0FA',26)
card(d,(790,505,1335,690),'比较改善与退步',['固定模型、资料、工具与预算','逐组回归，必要时人工复核'],PURPLE,'#F0EAF7',26)
card(d,(65,505,610,690),'决定采用或继续试验',['保留版本、结果与变更原因','新失败进入后续开发材料'],TEAL,n=26)
arrow(d,(610,285),(770,285));arrow(d,(1060,380),(1060,485),BLUE)
arrow(d,(790,595),(630,595),PURPLE);arrow(d,(335,505),(335,400))
card(d,(65,815,1335,985),'独立检验',['参与过修改的题目属于开发材料。','另留未参与调优的代表性题目，检查提示词能否适用于新问题。'],BLUE,'#E8F0FA',28)
save(im,'04-提示词迭代.png')

im,d=canvas('资料提供依据 操作需要授权','知识库资料的业务权威，不等于改变任务或调用工具的权限。',1160)
card(d,(65,195,610,380),'用户任务与应用规则',['解释住宿制度，回答适用条件','用户身份由应用确认'],TEAL,n=26)
card(d,(790,195,1335,380),'检索资料与工具结果',['可能包含正确资料或干扰文字','按来源、用途和权限处理'],RED,'#F8ECEA',26)
card(d,(390,485,1010,660),'模型生成回答或操作请求',['依据资料作答，或提出工具参数','输出仍需检查'],BLUE,'#E8F0FA',26)
arrow(d,(335,380),(520,465));arrow(d,(1060,380),(880,465),RED)
card(d,(65,790,610,980),'回答检查',['条款是否支持结论？','是否泄露不应返回的信息？'],PURPLE,'#F0EAF7',26)
card(d,(790,790,1335,980),'执行前检查',['核验身份、对象、权限和业务状态','符合条件后，由受控服务执行'],TEAL,n=26)
arrow(d,(520,660),(335,770),PURPLE);arrow(d,(880,660),(1060,770))
save(im,'05-输入与权限边界.png')

im,d=canvas('分层防御与正常任务一起验证','模型、提示词和系统分别承担职责；保持应用有用性也需要检查。',1190)
card(d,(65,185,1335,345),'模型层面',['通过训练增强指令层级遵循；在目标任务与攻击样本中验证表现。'],BLUE,'#E8F0FA',28)
card(d,(65,400,1335,560),'提示词层面',['表达应用职责，区分任务指令与外部资料；检查干扰与边界请求。'],PURPLE,'#F0EAF7',28)
card(d,(65,615,1335,775),'系统层面',['最小必要访问、受限工具、隔离执行，以及身份、权限与业务状态检查。'],TEAL,n=28)
card(d,(65,865,675,1050),'攻击评估',['明确攻击目标与成功判据','记录违规与实际操作结果'],RED,'#F8ECEA',27)
card(d,(725,865,1335,1050),'正常任务评估',['保留正常请求与边界请求','检查误拒和任务可用性'],BLUE,'#E8F0FA',27)
save(im,'06-分层防御.png')
thumbs=[]
for p in sorted(OUT.glob('*.png')):
 im=Image.open(p);im.thumbnail((460,400));thumbs.append((p.name,im.copy()))
sheet=Image.new('RGB',(1400,900),'white');d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(thumbs):
 x=i%3*466;y=i//3*450;txt(d,x+6,y+6,name,19);sheet.paste(im,(x,y+40))
sheet.save(ROOT/'配图核对.png')
print('生成6张配图与核对页')
