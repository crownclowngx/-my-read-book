"""第六章读后感配图，采用前两章的Pillow与微软雅黑样式。"""
import sys
sys.path.insert(0,r'C:\Users\crown\AppData\Local\Temp\chapter1-ocr-libs')
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
 txt(d,60,h-58,'《AI工程》第六章读书笔记 · 自绘学习示意 · 2026-10-19',23,MUTED)
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

im,d=canvas('RAG：资料准备与本次查询','先组织可检索资料，再根据本次任务选择证据并生成回答。',1140)
txt(d,65,185,'资料准备 / 索引阶段',30,BLUE,True)
card(d,(65,245,430,445),'原始资料',['制度与来源','版本、生效范围'],BLUE,'#E8F0FA',27)
card(d,(515,245,880,445),'解析与分块',['保留必要条件','附加来源与元数据'],BLUE,'#E8F0FA',26)
card(d,(965,245,1335,445),'建立索引',['词项 / 嵌入向量','支持后续检索'],BLUE,'#E8F0FA',26)
arrow(d,(430,340),(495,340),BLUE);arrow(d,(880,340),(945,340),BLUE)
txt(d,65,520,'本次查询阶段',30,TEAL,True)
d.line([(1150,445),(1150,500),(700,500)],fill=BLUE,width=4);arrow(d,(700,500),(700,595),BLUE)
card(d,(65,615,430,850),'用户问题',['识别任务与条件','必要时追问或重写'],TEAL,n=26)
card(d,(515,615,880,850),'检索与筛选',['读取索引，选择片段','核验访问范围与版本','按需要合并、重排序'],TEAL,n=25)
card(d,(965,615,1335,850),'组织输入与生成',['问题 + 指令 + 证据','给出条件与可核查出处'],PURPLE,'#F0EAF7',25)
arrow(d,(430,730),(495,730));arrow(d,(880,730),(945,730))
txt(d,65,925,'分别检查：资料是否有效、证据是否充分、回答是否受证据支持。',29,b=True)
txt(d,65,980,'业务规则与权限由应用落实；本图不表示模型能自动识别所有问题。',25,MUTED)
save(im,'01-RAG信息流.png')

im,d=canvas('检索优化：先观察失败，再选择改动','四种优化按原书6.1.3顺序排列；示例均需在目标任务中验证。',1240)
rows=[
 (185,'分块：条件被拆开',['金额与人群、地点分离'],'保留语义边界',['按结构拆分并保留表头与来源']),
 (405,'排序：旧资料靠前',['先确认制度是否仍然有效'],'筛选并重排序',['使用生效范围、版本与相关性']),
 (625,'重写：问题含有指代',['用户只问：“那B市呢？”'],'补足已知语境',['恢复查询意图，缺少条件时追问']),
 (845,'块上下文：含义不清',['片段只剩“每晚最高600元”'],'补充可追溯上下文',['附加原文标题、章节与必要条件'])]
for y,title,body,solution,detail in rows:
 card(d,(65,y,625,y+175),title,body,RED,'#F8ECEA',26)
 card(d,(775,y,1335,y+175),solution,detail,TEAL,n=25)
 arrow(d,(625,y+90),(755,y+90))
txt(d,65,1085,'同题比较改善与退步，并记录费用、延迟及配置版本。',29,b=True)
save(im,'02-检索优化.png')

im,d=canvas('规划、执行与结果检查','目标、约束和完成条件先明确；每一步可以根据真实反馈调整。',1250)
card(d,(65,185,1335,360),'用户任务与应用约束',['例：准备报销草稿；限定资料范围、允许动作与完成状态。'],BLUE,'#E8F0FA',28)
arrow(d,(245,360),(245,445),BLUE)
card(d,(65,465,430,700),'生成计划',['选择下一步动作','识别依赖与缺失项','保留目标和约束'],TEAL,n=26)
card(d,(515,465,880,700),'验证计划',['工具是否可用？','参数和前提是否满足？','需要什么授权？'],PURPLE,'#F0EAF7',25)
card(d,(965,465,1335,700),'受控执行',['由应用调用工具','返回结果、状态或错误','写入操作核验权限'],BLUE,'#E8F0FA',25)
arrow(d,(430,580),(495,580));arrow(d,(880,580),(945,580),PURPLE)
arrow(d,(1150,700),(1150,795),BLUE)
card(d,(515,815,1335,1005),'检查结果与任务状态',['独立核对证据、金额及业务记录；判断继续、纠错或结束。','完成以验收条件为准，保留必要状态供后续处理。'],TEAL,n=25)
d.line([(515,900),(245,900)],fill=TEAL,width=4);arrow(d,(245,900),(245,720))
txt(d,65,1065,'计划不通过时先调整；工具失败时按规则处理；限制重试与总预算。',28,b=True)
save(im,'03-计划与执行.png')

im,d=canvas('记忆：保存、取回与更新各有职责','原书区分内部知识、短期记忆与长期记忆；应用另需管理信息来源和有效性。',1300)
card(d,(65,185,625,410),'模型内部知识',['由训练形成，所有任务可使用','更新通常涉及模型参数变化'],BLUE,'#E8F0FA',27)
card(d,(775,185,1335,410),'外部长期记忆',['制度、任务记录和必要历史','持久保存，按任务检索与更新'],PURPLE,'#F0EAF7',27)
arrow(d,(1055,410),(1055,485),PURPLE)
txt(d,850,447,'检索 / 选择',25,PURPLE)
card(d,(775,505,1335,725),'当前上下文 / 短期记忆',['任务、约束与当前关键证据','容量有限，需按用途组织'],TEAL,n=27)
arrow(d,(1055,725),(1055,795))
card(d,(775,815,1335,1015),'模型处理本次任务',['结合内部知识和当前上下文','生成回答、计划或工具请求'],BLUE,'#E8F0FA',26)
d.line([(345,410),(345,455),(35,455),(35,1045),(1055,1045)],fill=BLUE,width=4);arrow(d,(1055,1045),(1055,1015),BLUE)
card(d,(65,505,625,725),'信息管理规则',['保存什么、谁可访问、何时更新','摘要保留关键条件和来源'],RED,'#F8ECEA',26)
card(d,(65,815,625,1015),'任务状态示例',['已确认字段、来源和确认时间','待补材料、申请编号与实际状态'],TEAL,n=25)
txt(d,65,1080,'需要长期保留的结果，经规则核验后写回外部存储；临时内容按用途处理。',27,b=True)
txt(d,65,1130,'历史偏好、旧制度与当前事实分别核对，防止过期信息影响新任务。',26,MUTED)
save(im,'04-记忆与状态.png')

sheet=Image.new('RGB',(1400,1400),'white');d=ImageDraw.Draw(sheet)
for i,p in enumerate(sorted(OUT.glob('*.png'))):
 thumb=Image.open(p);thumb.thumbnail((680,630));x=i%2*700;y=i//2*700
 txt(d,x+10,y+10,p.name,22);sheet.paste(thumb,(x+10,y+55))
sheet.save(ROOT/'配图核对.png')
print('生成4张中文概念图及核对页')
