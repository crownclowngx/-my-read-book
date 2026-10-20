"""第八章读书笔记的五幅中文概念图，无模型成绩或实验曲线。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80';BLUE='#276CB0';PURPLE='#7852A1';GRID='#D8E2E6'
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def text(d,x,y,s,n=27,c=INK,b=False):
    assert d.textbbox((x,y),s,font=font(n,b))[2]<1370,(s,x,n)
    d.text((x,y),s,font=font(n,b),fill=c)
def canvas(title,sub,h=1080):
    im=Image.new('RGB',(1400,h),BG);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1400,12),fill=TEAL)
    text(d,60,40,title,42,b=True);text(d,62,111,sub,25,MUTED)
    d.line((60,h-82,1340,h-82),fill=GRID,width=2)
    text(d,60,h-58,'《AI工程》第八章读书笔记 · 自绘学习示意 · 2026-10-21',23,MUTED)
    return im,d
def card(d,rect,title,body,c=TEAL,fill='#E5F2F0',n=27):
    x,y,r,b=rect;d.rounded_rectangle(rect,18,fill=fill,outline=c,width=3)
    assert d.textlength(title,font=font(30,True))<r-x-44,title
    assert all(d.textlength(s,font=font(n))<r-x-44 for s in body),(title,body)
    assert y+76+max(0,len(body)-1)*44+n<b-12,(title,'height')
    text(d,x+22,y+18,title,30,c,True)
    for i,s in enumerate(body):text(d,x+22,y+76+i*44,s,n)
def arrow(d,a,b,c=TEAL):
    d.line((a,b),fill=c,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=18
    d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=c)

im,d=canvas('让一条样本有可核对的依据','参考8.1.1与8.1.4；以下制度、问题与金额为假设学习案例。',1150)
card(d,(60,180,1340,370),'任务条件与有效资料',['普通员工在A市住两晚，每晚700元；假定审批和凭证条件已满足。','制度R-2026第3条：每晚最高600元，超出自理。'],BLUE,'#E8F0FA',28)
arrow(d,(700,370),(700,425))
card(d,(60,445,675,685),'目标响应',['按第3条，两晚最多可报1200元。','超出的200元自理。'],TEAL,n=27)
card(d,(725,445,1340,685),'核对项目',['适用条件与依据是否正确？','金额、引用和超出部分是否完整？'],PURPLE,'#F0EAF7',26)
arrow(d,(360,685),(360,760));arrow(d,(1040,685),(1040,760),PURPLE)
card(d,(60,780,1340,990),'保留可追溯记录',['原始问题、资料版本、支持片段、目标响应、标注理由与复核记录。','缺少城市或每晚明细时，应重新判断目标行为，不能直接套用答案。'],TEAL,n=28)
im.save(OUT/'01-样本与标注依据.png')

im,d=canvas('检查问题类别 也检查期望行为','沿用前文五类问题；以下是覆盖检查示意，不表示数据条数或比例。',1050)
xs=[60,310,865,1340];top=190;rh=121
headers=['问题类别','示例情境','应检查的行为']
for j,h in enumerate(headers):
    d.rectangle((xs[j],top,xs[j+1],top+80),fill=TEAL)
    text(d,xs[j]+20,top+22,h,28,'white',True)
rows=[('常见问题','城市、身份与费用均明确','依条款回答并说明条件'),('专业术语','询问“实际合规金额”','结合制度解释术语'),('资料缺失','未提供适用制度','说明资料缺口，避免编造'),('版本冲突','两份制度的生效日期不同','核对日期及适用范围'),('中英混合','问句混有英文或业务简称','正确理解意图与必要条件')]
for i,row in enumerate(rows):
    y=top+80+i*rh
    for j,s in enumerate(row):
        d.rectangle((xs[j],y,xs[j+1],y+rh),fill='white' if i%2==0 else '#EAF2F4',outline=GRID,width=2)
        text(d,xs[j]+18,y+43,s,25)
text(d,60,920,'同一类别可以对应多种行为；还应交叉检查表达方式、长度与多轮交互。',27,b=True)
im.save(OUT/'02-数据覆盖度.png')

im,d=canvas('生成结果先进入候选区','参考8.2.3；数量扩展与质量确认分别进行，同源关系贯穿全过程。',1180)
card(d,(60,185,1340,370),'可信种子与明确缺口',['记录制度依据，说明本轮要补哪种场景，以及允许改变哪些条件。'],BLUE,'#E8F0FA',28)
arrow(d,(700,370),(700,425))
card(d,(60,445,675,685),'受控扩展',['改写表达、组合条件、生成多轮。','条件变化后，重新生成目标响应。'],TEAL,n=27)
card(d,(725,445,1340,685),'验证与复核',['规则校验、证据核查、人工抽查。','AI裁判也需要检查误判。'],PURPLE,'#F0EAF7',27)
arrow(d,(675,565),(705,565));arrow(d,(1040,685),(1040,760),PURPLE)
card(d,(60,780,1340,1010),'决定入库 或退回修订',['保留合格样本、种子来源、问题族、生成配置与验证依据。','未通过的样本可以修订或排除；入库后仍需用独立任务检验训练效果。'],TEAL,n=28)
im.save(OUT/'03-合成与验证.png')

im,d=canvas('教师输出经过核查 再用于学生训练','参考8.2.4；此图表达数据流，框大小不代表参数量或性能。',1100)
card(d,(60,200,445,450),'教师生成候选',['围绕任务产生响应','保留生成配置与来源'],BLUE,'#E8F0FA',26)
card(d,(505,200,890,450),'数据整理与验证',['核对依据与正确性','筛选合格的训练示例'],TEAL,n=26)
card(d,(950,200,1340,450),'训练学生模型',['按目标任务进行训练','记录模型与数据版本'],PURPLE,'#F0EAF7',26)
arrow(d,(445,325),(485,325),BLUE);arrow(d,(890,325),(930,325),TEAL)
arrow(d,(1140,450),(1140,550),PURPLE)
card(d,(60,570,1340,795),'独立检验能力和运行代价',['检查正常回答、必要追问、资料不足与版本冲突等行为。','比较质量、费用与延迟，再决定采用、回退或继续改进。'],TEAL,n=29)
text(d,60,870,'教师更强不代表每条样本都正确；使用合成数据的训练也不全属于蒸馏。',29,b=True)
text(d,60,930,'制度更新与访问控制，仍由资料管理和应用系统共同处理。',27,MUTED)
im.save(OUT/'04-模型蒸馏.png')

im,d=canvas('将候选材料整理成训练数据','参考8.3；先小规模试运行，保留原始数据，按成本与任务调整步骤。',1150)
cards=[(60,345,'检查',['来源、长度与分布','人工查看完整样本'],BLUE,'#E8F0FA'),(390,675,'去重',['定义重复单位','复核相似样本差异'],TEAL,'#E5F2F0'),(720,1005,'清理与过滤',['核对标签与依据','关注误删和分布变化'],PURPLE,'#F0EAF7'),(1050,1340,'格式化',['角色与对话模板','截断与损失掩码'],BLUE,'#E8F0FA')]
for x,r,title,body,c,fill in cards:card(d,(x,210,r,460),title,body,c,fill,23)
for a,b in [(345,390),(675,720),(1005,1050)]:arrow(d,(a+7,335),(b-13,335))
card(d,(60,570,1340,780),'贯穿全程的管理记录',['来源与资料版本、原始样本ID、问题族、标注与验证、处理规则及数据版本。','按评估目标分组切分，检查种子和派生样本是否跨越训练与独立测试。'],TEAL,n=28)
arrow(d,(1195,460),(1195,550),BLUE)
text(d,60,865,'训练文件可加载以后，还要检查模型实际看到的文本和预期学习的回答。',28,b=True)
text(d,60,935,'通过独立任务评价数据是否有用，发现问题后回到相应步骤修订。',28,MUTED)
im.save(OUT/'05-数据处理流程.png')

# Contact sheet for layout review.
thumbs=[]
for p in sorted(OUT.glob('*.png')):
    img=Image.open(p).convert('RGB');img.thumbnail((700,590));thumbs.append((p.name,img))
sheet=Image.new('RGB',(1400,3*640),'white');dd=ImageDraw.Draw(sheet)
for i,(name,img) in enumerate(thumbs):
    x=(i%2)*700;y=(i//2)*640;sheet.paste(img,(x,y+38));dd.text((x+12,y+5),name,font=font(22),fill=INK)
sheet.save(ROOT/'配图核对.png')
print('Generated five illustrations and contact sheet')
