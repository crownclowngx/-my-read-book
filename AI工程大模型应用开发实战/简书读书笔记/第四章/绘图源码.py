"""生成第四章的六张中文概念图。需要Pillow及Windows微软雅黑字体。"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80';BLUE='#276CB0';PURPLE='#7852A1';RED='#B34F4F';GRID='#D8E2E6'
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def txt(d,x,y,s,n=27,c=INK,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def lines(d,x,y,ss,n=27,gap=44,c=INK):
 for i,s in enumerate(ss):txt(d,x,y+i*gap,s,n,c)
def canvas(title,sub,h=1040):
 im=Image.new('RGB',(1400,h),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1400,12),fill=TEAL);txt(d,60,40,title,42,b=True);txt(d,62,110,sub,26,MUTED)
 d.line((60,h-83,1340,h-83),fill=GRID,width=2)
 txt(d,60,h-58,'《AI工程》第四章读书笔记 · 自绘学习示意 · 2026-10-17',23,MUTED)
 return im,d
def card(d,rect,title,body=(),c=TEAL,fill='#E5F2F0',n=27):
 x,y,r,b=rect;d.rounded_rectangle(rect,18,fill=fill,outline=c,width=3)
 txt(d,x+24,y+19,title,31,c,True);lines(d,x+24,y+79,body,n,43)
def arrow(d,a,b,c=TEAL):
 d.line((a,b),fill=c,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=19
 d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=c)
def save(im,name):im.save(OUT/name)

im,d=canvas('从应用要求到评估维度','同一个知识库回答，需要多种证据共同检查。',1100)
card(d,(65,185,1335,340),'应用要求',['根据当前有效资料回答，条件完整，行为符合职责，使用代价可接受。'],n=29)
for rect,title,body,c,fill in [
 ((65,440,675,650),'领域特定能力',['能否理解术语、条件与任务？','证据：实际业务题与任务结果'],TEAL,'#E5F2F0'),
 ((725,440,1335,650),'生成能力',['结论是否有依据，内容是否安全？','证据：支持片段与风险检查'],BLUE,'#E8F0FA'),
 ((65,720,675,930),'指令遵循能力',['格式、内容限制与职责是否满足？','证据：规则检查与行为样本'],PURPLE,'#F0EAF7'),
 ((725,720,1335,930),'成本和延迟',['完成任务需要多少资源与时间？','证据：同一负载下的运行记录'],RED,'#F8ECEA')]:
 card(d,rect,title,body,c,fill,27)
arrow(d,(370,340),(370,420));arrow(d,(1030,340),(1030,420))
txt(d,65,965,'验收保留各维度结果与关键失败；硬性条件需要单独满足。',27,MUTED)
save(im,'01-评估维度.png')

im,d=canvas('事实核查：陈述需要对应证据','假设当前有效制度：A市住宿每晚最多报销600元，超出部分自理。',1120)
card(d,(65,180,1335,330),'待检查回答',['“所有员工在任何城市住宿都能报销600元。”'],n=31)
for x,title,body,c,fill in [(65,'金额',['600元','需要保留每晚这一单位'],TEAL,'#E5F2F0'),(505,'范围',['任何城市？','资料仅支持A市'],RED,'#F8ECEA'),(945,'人群',['所有员工？','给定片段不足以判断'],PURPLE,'#F0EAF7')]:
 card(d,(x,425,x+390,655),title,body,c,fill,27);arrow(d,(700,330),(x+195,405),c)
card(d,(65,745,1335,925),'核查顺序',['拆分陈述 → 找到支持片段 → 检查来源、版本和适用范围','分别记录：支持 / 矛盾 / 无法判定；保留缺失的条件'],BLUE,'#E8F0FA',29)
txt(d,65,975,'局部一致：是否符合给定资料       资料有效：是否适用于当前问题',28,MUTED)
save(im,'02-事实核查.png')

im,d=canvas('模型选择：约束、筛选、实验与监控','参考原书4.2.1；新证据可能促使此前的选择发生变化。',1130)
rows=[(185,'1  按硬属性排除','协议、数据边界、部署位置和资源条件',TEAL,'#E5F2F0'),(365,'2  用公开信息筛选','看任务覆盖、评估条件与成本，缩小候选范围',BLUE,'#E8F0FA'),(545,'3  用自己的任务实验','固定问题、资料、工具与预算，比较关键失败',PURPLE,'#F0EAF7'),(725,'4  持续观察与复评','监控用户任务与版本变化，补充真实失败',TEAL,'#E5F2F0')]
for y,title,body,c,fill in rows:
 card(d,(170,y,1230,y+135),title,[body],c,fill,28)
 if y<725:arrow(d,(700,y+135),(700,y+167))
txt(d,170,935,'每轮都同时考虑：模型质量、总成本、延迟与维护条件。',29,b=True)
txt(d,170,985,'根据新证据返回前面的步骤，保留调整原因与版本记录。',27,MUTED)
save(im,'03-模型选择.png')

im,d=canvas('模型属性与部署方式需要分别判断','开放程度影响可访问和可修改的内容；部署方式影响运行与数据条件。',1080)
txt(d,325,210,'自托管',34,TEAL,True);txt(d,865,210,'使用模型API',34,BLUE,True)
card(d,(255,295,735,505),'开放权重模型',['自行托管已有模型','核查许可、硬件与维护条件'],TEAL,'#E5F2F0',26)
card(d,(790,295,1335,505),'开放权重模型',['使用提供方或第三方服务','核查版本、数据与服务条件'],BLUE,'#E8F0FA',26)
card(d,(255,555,735,765),'专有模型',['通常无法自行部署','具体私有部署看提供方安排'],PURPLE,'#F0EAF7',26)
card(d,(790,555,1335,765),'专有模型',['通过提供方或授权渠道访问','核查能力、条款与版本策略'],BLUE,'#E8F0FA',26)
txt(d,65,375,'开放',31,TEAL,True);txt(d,65,420,'权重',31,TEAL,True)
txt(d,65,630,'专有',31,PURPLE,True);txt(d,65,675,'模型',31,PURPLE,True)
lines(d,255,840,['能下载权重，并不自动意味着训练数据公开或用途不受限制。','自托管现有模型，与从零训练模型的投入不同。'],28,47)
save(im,'04-模型与部署.png')

im,d=canvas('评估组件，也评估完整任务','知识库助手示意；先保存中间结果，再结合最终结果定位失败。',1090)
for x,title,body in [(65,'资料解析',['正文、表格和版本']),(505,'资料检索',['相关且有效的依据']),(945,'回答生成',['结论、条件和引用'])]:
 card(d,(x,235,x+390,430),title,body,n=27)
 if x<945:arrow(d,(x+390,330),(x+425,330))
for x,body in [(65,['正文是否遗漏？','版本是否识别正确？']),(505,['应取资料是否找到？','是否混入无效版本？']),(945,['给定正确资料后，','结论是否受到支持？'])]:
 card(d,(x,530,x+390,720),'组件检查',body,BLUE,'#E8F0FA',26);arrow(d,(x+195,430),(x+195,510),BLUE)
card(d,(65,810,1335,935),'端到端检查',['按真实输入条件，用户最终是否得到可用答案，或恰当的追问与转接？'],PURPLE,'#F0EAF7',28)
save(im,'05-组件评估.png')

im,d=canvas('让评估能够持续支持迭代','比较系统版本，也记录数据、评分规则和运行环境的变化。',1140)
card(d,(65,205,610,385),'固定任务与基线',['问题、资料、规则、模型和预算'],TEAL,n=26)
card(d,(790,205,1335,385),'运行并评分',['保存输出、中间结果、费用和耗时'],BLUE,'#E8F0FA',26)
arrow(d,(610,295),(770,295))
card(d,(790,505,1335,730),'复核具体失败',['系统错误？任务歧义？','评分误判？环境不一致？'],PURPLE,'#F0EAF7',27)
arrow(d,(1060,385),(1060,485),BLUE)
card(d,(65,505,610,730),'修改并进行回归比较',['检查改善与退步','补充新失败，保留独立测试材料'],TEAL,n=26)
arrow(d,(790,615),(630,615),PURPLE);arrow(d,(335,505),(335,405))
card(d,(65,845,1335,1010),'版本发生变化时',['记录变化；必要时用同一新规则重评旧输出，避免比较口径发生混淆。'],BLUE,'#E8F0FA',28)
save(im,'06-持续评估.png')
print('生成6张配图')
