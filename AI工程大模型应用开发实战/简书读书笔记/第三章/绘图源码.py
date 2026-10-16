"""生成第三章读书笔记的八张中文PNG，运行时需要Pillow和微软雅黑字体。"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img'; OUT.mkdir(exist_ok=True)
FONT=Path('C:/Windows/Fonts/msyh.ttc')
BOLD=Path('C:/Windows/Fonts/msyhbd.ttc')
INK='#173B48'; MUTED='#526A75'; TEAL='#087F80'; BLUE='#276CB0'; PURPLE='#7852A1'
BG='#F5F8FA'; GRID='#D8E2E6'; RED='#B34F4F'

def font(n,b=False):return ImageFont.truetype(str(BOLD if b else FONT),n)
def text(d,xy,s,n=29,color=INK,b=False,anchor=None):
    d.text(xy,s,font=font(n,b),fill=color,anchor=anchor)
def lines(d,x,y,ss,n=28,gap=44,color=INK):
    for i,s in enumerate(ss):text(d,(x,y+i*gap),s,n,color)
def base(title,sub,h=1000):
    im=Image.new('RGB',(1400,h),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1400,12),fill=TEAL)
    text(d,(58,42),title,43,b=True);text(d,(60,108),sub,26,MUTED)
    d.line((60,h-83,1340,h-83),fill=GRID,width=2)
    text(d,(60,h-58),'《AI工程》第三章读书笔记 · 自绘学习示意 · 2026-10-16',23,MUTED)
    return im,d
def card(d,rect,title,body=(),color=TEAL,fill='#E5F2F0',n=28):
    d.rounded_rectangle(rect,18,fill=fill,outline=color,width=3)
    x,y,r,b=rect;text(d,(x+24,y+20),title,31,color,True)
    lines(d,x+24,y+79,body,n,43)
def arrow(d,a,b,c=TEAL):
    d.line([a,b],fill=c,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);ll=17
    d.polygon([b,(b[0]-ll*math.cos(ang-.5),b[1]-ll*math.sin(ang-.5)),(b[0]-ll*math.cos(ang+.5),b[1]-ll*math.sin(ang+.5))],fill=c)
def center(d,x,y,s,n=29,c=INK,b=False):text(d,(x,y),s,n,c,b,'mm')
def save(im,name):im.save(OUT/name)

im,d=base('熵与交叉熵：数据的不确定性与预测的代价','位置示例假定各区域等概率；下面的模型预测示例只使用“上、下”两个结果。',1050)
for x,k,label in [(130,2,'两个等概率位置'),(820,4,'四个等概率位置')]:
    y=255;w=260;d.rectangle((x,y,x+w,y+w),outline=TEAL,width=4)
    d.line((x,y+w//2,x+w,y+w//2),fill=TEAL,width=3)
    if k==4:d.line((x+w//2,y,x+w//2,y+w),fill=TEAL,width=3)
    for j,(dx,dy) in enumerate([(w/2,w/4),(w/2,3*w/4)] if k==2 else [(w/4,w/4),(3*w/4,w/4),(w/4,3*w/4),(3*w/4,3*w/4)]):
        center(d,x+dx,y+dy,str(j+1),38)
    text(d,(x,y-55),label,30,b=True)
    text(d,(x,y+w+25),f'H(P) = {1 if k==2 else 2} 比特',30)
card(d,(70,665,650,895),'真实分布 P：上、下各占一半',['模型 Q：0.5 / 0.5','平均交叉熵 = 1 比特'],TEAL)
card(d,(725,665,1330,895),'同一真实分布，模型预测改变',['模型 Q：0.9 / 0.1','平均交叉熵 ≈ 1.737 比特'],BLUE,'#E8F0FA')
center(d,700,625,'H(P, Q) = H(P) + D_KL(P || Q)',32,PURPLE,True)
save(im,'01-熵与交叉熵.png')

im,d=base('语言建模指标：先统一单位，再比较结果','不同分母和不同计算条件，会改变数值的含义。',1050)
card(d,(345,195,1055,370),'同一份文本的总预测代价（比特）',['逐个真实token的负对数概率相加'],TEAL)
for x,title,body in [(60,'平均交叉熵',['总比特数 / token数','单位：比特/token']),(500,'BPC',['总比特数 / 字符数','单位：比特/字符']),(940,'BPB',['总比特数 / 字节数','单位：比特/字节'])]:
    card(d,(x,465,x+400,665),title,body,BLUE,'#E8F0FA',27)
    arrow(d,(700,370),(x+200,465))
card(d,(60,735,460,865),'困惑度 PPL',['2 ^ 平均交叉熵'],PURPLE,'#F0EAF7')
arrow(d,(260,665),(260,735),PURPLE)
lines(d,535,745,['比较前确认：数据、分词、文本处理、编码','以及上下文窗口、步长和对数单位。','这些指标不等于业务问题的正确概率。'],27,44)
save(im,'02-语言建模指标.png')

im,d=base('与参考数据比较：表达接近与事实一致需要区分','假设制度：住宿上限500元/晚，超出部分自行承担。',1080)
card(d,(65,190,1335,345),'参考答案',['住宿报销上限为500元，超出部分自行承担。'],TEAL)
card(d,(65,395,680,595),'响应甲：换一种有效表达',['每晚最高报销500元，','其余费用由本人支付。'],BLUE,'#E8F0FA')
card(d,(730,395,1335,595),'响应乙：只改关键数字',['住宿报销上限为650元，','超出部分自行承担。'],RED,'#F8ECEA')
for y,title,body in [(660,'精确匹配','关注是否一致；需要定义规范化规则'),(750,'词汇相似度','关注表面重叠；关键数字错误也可能很相似'),(840,'语义相似度','关注含义接近；仍需检查条件、否定和事实')]:
    text(d,(90,y),title,30,TEAL,True);text(d,(365,y),body,28)
text(d,(90,935),'这里只解释方法关注点，没有虚构任何指标实测分数。',25,MUTED)
save(im,'03-参考数据与相似度.png')

im,d=base('嵌入与余弦相似度：先理解几何关系','左侧是自编二维向量；真实文本嵌入通常维度更高。',1020)
origin=(250,635);a=(630,635);b=(440,306);c=(250,255)
d.line((135,635,730,635),fill=GRID,width=2);d.line((250,735,250,190),fill=GRID,width=2)
arrow(d,origin,a,TEAL);arrow(d,origin,b,BLUE);arrow(d,origin,c,PURPLE)
text(d,(465,670),'A = (1, 0)',28,TEAL,True)
text(d,(385,245),'B ≈ (0.5, 0.866)',27,BLUE,True)
text(d,(85,195),'C = (0, 1)',27,PURPLE,True)
d.arc((170,555,330,715),300,360,fill=BLUE,width=4);text(d,(342,566),'60°',29,BLUE)
card(d,(800,255,1325,505),'非零向量的余弦相似度',['(A · B) / (||A|| × ||B||)','A与B：cos 60° = 0.5','A与C：cos 90° = 0'],BLUE,'#E8F0FA',26)
card(d,(800,555,1325,785),'使用边界',['相同维度不代表同一向量空间','相似度不等于正确概率','零向量的余弦没有定义'],PURPLE,'#F0EAF7',25)
text(d,(90,855),'嵌入表示 → 相似度计算 → 在目标任务上验证是否有效',31,b=True)
save(im,'04-嵌入与余弦相似度.png')

im,d=base('多次尝试：至少成功一次，与全部成功','下方两行是假设结果，展示事件定义，不是模型测量。',1000)
for y,label,states,summary in [(255,'情境一',[True,False,False],'至少一次成功：是     三次全部成功：否'),(505,'情境二',[True,True,True],'至少一次成功：是     三次全部成功：是')]:
    text(d,(65,y+36),label,30,b=True)
    for j,s in enumerate(states):
        x=285+j*325;d.rounded_rectangle((x,y,x+260,y+115),18,fill='#E5F2F0' if s else '#F8ECEA',outline=TEAL if s else RED,width=3)
        center(d,x+130,y+57,'成功' if s else '失败',35,TEAL if s else RED,True)
    center(d,790,y+163,summary,28)
card(d,(65,775,1335,905),'独立且每次成功率固定为0.8时的数学例子',['三次至少成功一次：1 − 0.2³ = 99.2%      三次全部成功：0.8³ = 51.2%'],BLUE,'#E8F0FA',27)
save(im,'05-多次尝试与持续成功.png')

im,d=base('AI裁判：输入、评判条件与复核路径','裁判系统由模型和评估设置共同构成。',1050)
card(d,(65,230,460,480),'待评材料',['问题与候选回答','任务相关资料','参考答案（可选）'],TEAL,n=27)
card(d,(590,230,1000,480),'AI裁判',['模型版本与采样参数','提示词、规则和示例','输入顺序与输出解析'],BLUE,'#E8F0FA',26)
arrow(d,(460,355),(590,355))
card(d,(1070,230,1340,480),'评估结果',['类别 / 分数','依据片段','问题说明'],PURPLE,'#F0EAF7',26)
arrow(d,(1000,355),(1070,355))
card(d,(590,650,1000,855),'人工与规则复核',['核对证据和类别边界','分析误判与无法判定','保留版本和判断记录'],TEAL,n=26)
arrow(d,(1205,480),(1000,715),PURPLE)
lines(d,85,685,['生成解释有助于审查，','解释本身也需要验证。','输入中的指令不获得执行权。'],26,49)
save(im,'06-AI裁判流程.png')

im,d=base('验证AI裁判：三个问题分别回答','这是结合近期研究提出的学习验证方案，不是已执行实验。',1020)
cols=[(60,'重复性',['保持输入与设置相同','重复评估相同答案','记录判断是否变化'],TEAL,'#E5F2F0'),(505,'顺序影响',['保持候选内容相同','交换A与B的位置','核对偏好是否随之改变'],BLUE,'#E8F0FA'),(950,'准确性',['人工确认资料与结论','加入金额错误、条件遗漏','检查裁判能否发现错误'],PURPLE,'#F0EAF7')]
for x,title,ss,color,fill in cols:card(d,(x,245,x+390,610),title,ss,color,fill,25)
card(d,(160,730,1240,880),'综合解释',['稳定不代表准确；顺序影响小也不代表能发现关键事实错误。'],TEAL,n=28)
for x,*_ in cols:arrow(d,(x+195,610),(700,730))
save(im,'07-验证AI裁判.png')

im,d=base('比较评估：从比较信号到实际选型','模型排名概括相对表现，应用验收判断是否达到使用要求。',1100)
rows=[(195,'同题比较','问题、资料、模型设置和运行条件'),(365,'记录对局','匿名候选、评估者、胜负 / 平局与理由'),(535,'汇总排名','胜率口径、评分算法、样本覆盖与不确定性'),(705,'作出应用选择','任务达标情况 + 成本 + 延迟 + 维护条件')]
for j,(y,title,body) in enumerate(rows):
    col=TEAL if j%2==0 else BLUE;fill='#E5F2F0' if j%2==0 else '#E8F0FA'
    card(d,(155,y,1245,y+125),title,[body],col,fill,28)
    if j:arrow(d,(700,rows[j-1][0]+125),(700,y))
text(d,(160,918),'同时保留：版本、时间、工具、重试与资源预算。',29,b=True)
save(im,'08-比较评估与排名.png')

if __name__=='__main__':
    for p in sorted(OUT.glob('*.png')):
        with Image.open(p) as im:print(p.name,im.size)
