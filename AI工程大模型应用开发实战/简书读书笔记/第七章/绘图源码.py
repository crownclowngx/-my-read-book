"""生成第七章七张中文概念图。Pillow与Windows微软雅黑字体。"""
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
 txt(d,60,h-58,'《AI工程》第七章读书笔记 · 自绘学习示意 · 2026-10-19',23,MUTED)
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

im,d=canvas('先定位失败 再选择适配方式','参考原书7.2：任务定义与评估先行，修改以后重新检查改善与退步。',1130)
card(d,(65,190,1335,350),'保存具体失败及其依据',['问题、资料版本、检索结果、模型输出和评分规则'],TEAL,n=28)
for x,r,title,body,c,fill in [
 (65,460,'信息缺失或过期',['核对来源和有效版本','改进检索与上下文','需要时使用RAG'],BLUE,'#E8F0FA'),
 (500,895,'资料正确仍答不好',['检查指令与代表性示例','比较输出约束和模型','必要时评估微调'],PURPLE,'#F0EAF7'),
 (935,1335,'涉及权限与动作',['核验用户与操作对象','由系统实施访问控制','检查真实执行结果'],TEAL,'#E5F2F0')]:
 card(d,(x,450,r,680),title,body,c,fill,24)
 arrow(d,((x+r)//2,350),((x+r)//2,430),c)
 arrow(d,((x+r)//2,680),((x+r)//2,790),c)
card(d,(65,810,1335,990),'在相同任务上比较 再决定采用或继续试验',['RAG与微调可以结合；任务、资料和部署要求共同约束选择。'],TEAL,n=28)
save(im,'01-微调选择.png')

im,d=canvas('推理与训练分别要保存什么','组成示意；框大小不代表内存比例，具体开销随模型与实现变化。',1160)
card(d,(65,190,675,385),'推理',['模型权重','激活值、KV缓存与临时缓冲'],BLUE,'#E8F0FA',27)
card(d,(725,190,1335,385),'训练',['模型权重、激活值','梯度、优化器状态及临时缓冲'],TEAL,'#E5F2F0',27)
card(d,(65,475,675,715),'模型总参数量',['决定基座权重的存储规模','每个数值的位宽也影响内存','长上下文与并发影响缓存'],BLUE,'#E8F0FA',26)
card(d,(725,475,1335,715),'可训练参数量',['影响梯度和优化器状态','冻结权重仍可能参与计算','激活值不按同一比例缩小'],PURPLE,'#F0EAF7',26)
arrow(d,(370,385),(370,455),BLUE);arrow(d,(1030,385),(1030,455))
card(d,(65,825,1335,995),'估算条件需要记录',['参数量与数值格式、序列长度、微批次、累积步数、检查点和分片方式。'],TEAL,n=27)
save(im,'02-内存组成.png')

im,d=canvas('位数相同 范围和精度仍可能不同','参考原书7.3.3：指数影响范围，有效数影响精度。',1080)
rows=[('FP32',1,8,23,230),('FP16',1,5,10,420),('BF16',1,8,7,610)]
for label,sign,ex,fr,y in rows:
 txt(d,65,y+28,label,34,b=True);x=260
 for count,c,name in [(sign,RED,'符号'),(ex,BLUE,'指数'),(fr,TEAL,'有效数')]:
  width=count*31;d.rectangle((x,y,x+width,y+84),fill=c)
  if count>1:txt(d,x+12,y+23,str(count)+'位',27,'white',True)
  x+=width
 txt(d,260,y+104,f'符号 {sign}位  /  指数 {ex}位  /  有效数存储 {fr}位',26,MUTED)
txt(d,65,820,'同为16位：BF16范围较广，FP16有效数存储位较多。',30,b=True)
txt(d,65,880,'有效数存储位不含正规数的隐含首位；格式选择还需结合模型和硬件。',25,MUTED)
save(im,'03-数值表示.png')

im,d=canvas('LoRA学习低秩权重增量','采用W为n×m、A为n×r、B为r×m的记号；原始W保持冻结。',1130)
card(d,(65,195,460,400),'原始权重 W',['维度 n × m','保留预训练参数'],BLUE,'#E8F0FA',27)
card(d,(540,195,895,400),'可训练矩阵 A',['维度 n × r','更新其中的参数'],TEAL,'#E5F2F0',25)
card(d,(975,195,1335,400),'可训练矩阵 B',['维度 r × m','更新其中的参数'],TEAL,'#E5F2F0',25)
txt(d,917,275,'×',35,b=True)
arrow(d,(720,400),(720,490));arrow(d,(1155,400),(1155,490))
card(d,(540,510,1335,675),'低秩增量 ΔW = AB',['结果维度 n × m；秩r控制更新空间与参数量'],PURPLE,'#F0EAF7',26)
arrow(d,(260,400),(260,775),BLUE);arrow(d,(940,675),(940,775),PURPLE)
card(d,(65,795,1335,980),'合并后的权重 W′ = W + (α / r) × AB',['可训练参数量为nr + rm；基座权重nm仍然需要存储与使用。'],TEAL,n=28)
save(im,'04-LoRA更新.png')

im,d=canvas('一套基座 多个任务适配器','参考原书图7-12：适配器分离便于共享与切换，部署效率需要测量。',1090)
card(d,(65,195,1335,365),'兼容的基座模型 W',['模型、分词器、聊天模板与适配器的来源版本需要对应。'],BLUE,'#E8F0FA',28)
card(d,(65,485,675,685),'任务适配器 A',['制度问答：解释条款与条件','加载相应低秩更新'],TEAL,n=27)
card(d,(725,485,1335,685),'任务适配器 B',['材料整理：汇总缺项与草稿','加载相应低秩更新'],PURPLE,'#F0EAF7',27)
arrow(d,(370,365),(370,465));arrow(d,(1030,365),(1030,465),PURPLE)
card(d,(65,815,1335,965),'两种部署安排',['预先合并为完整模型，或保留基座与适配器分离；核对质量、内存与延迟。'],TEAL,n=27)
save(im,'05-多适配器部署.png')

im,d=canvas('模型合并的三种基本思路','参考原书7.4.2与图7-14；符号表达组合方式，不代表实际训练结果。',1160)
for y,title,body,c,fill in [
 (195,'求和与插值',['对应的参数按权重组合','需要检查参数对应关系与任务效果'],TEAL,'#E5F2F0'),
 (470,'层堆叠',['选择、复制并组合不同层','可能改变深度，通常需要继续训练'],BLUE,'#E8F0FA'),
 (745,'拼接',['保留并连接各组成部分','维度和参数量增加，继续评估资源代价'],PURPLE,'#F0EAF7')]:
 card(d,(65,y,675,y+200),title,body,c,fill,26)
 arrow(d,(695,y+100),(795,y+100),c)
 x=845
 if y==195:
  for j in range(3):d.rectangle((x,y+22+j*53,x+435,y+58+j*53),fill=c)
 elif y==470:
  for j in range(5):d.rectangle((x,y+12+j*35,x+435,y+36+j*35),fill=BLUE if j<3 else TEAL)
 else:
  for j in range(3):
   d.rectangle((x,y+22+j*53,x+235,y+58+j*53),fill=BLUE)
   d.rectangle((x+245,y+22+j*53,x+435,y+58+j*53),fill=TEAL)
save(im,'06-模型合并.png')

im,d=canvas('让每次微调对应一个可检查的问题','延续第四章的评估过程；开发材料和独立保留材料承担不同职责。',1190)
card(d,(65,190,610,400),'定义目标与保留能力',['记录重复失败与正确处理方式','建立提示词和RAG基线'],TEAL,n=26)
card(d,(790,190,1335,400),'准备数据与训练设置',['检查来源、近似样本与切分','记录模型、模板和配置版本'],BLUE,'#E8F0FA',26)
card(d,(790,515,1335,725),'开发与分组回归',['检查目标行为与其他任务','比较训练、验证和任务结果'],PURPLE,'#F0EAF7',26)
card(d,(65,515,610,725),'独立检验与采用决定',['使用未参与调参的材料','综合质量、费用与部署条件'],TEAL,n=26)
arrow(d,(610,295),(770,295));arrow(d,(1060,400),(1060,495),BLUE)
arrow(d,(790,620),(630,620),PURPLE)
card(d,(65,850,1335,1025),'保留记录 发现问题后继续迭代',['开发集可以反复使用；保留集若参与调参，就不再保持原来的独立性。'],BLUE,'#E8F0FA',27)
save(im,'07-微调验证.png')
