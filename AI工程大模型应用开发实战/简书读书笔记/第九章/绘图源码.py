from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'img';OUT.mkdir(exist_ok=True)
W=1500;BG='#F5F8FA';INK='#173B48';MUTED='#526A75';TEAL='#087F80';BLUE='#276CB0';PURPLE='#7852A1';RED='#AD5252';GRID='#D8E2E6'
checks=[]
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def text(d,x,y,s,n=28,c=INK,b=False):
 box=d.textbbox((x,y),s,font=font(n,b));assert box[2]<W-30,(s,box)
 d.text((x,y),s,font=font(n,b),fill=c);checks.append((s,box))
def lines(d,x,y,ss,n=28,gap=47,c=INK):
 for i,s in enumerate(ss):text(d,x,y+i*gap,s,n,c)
def canvas(title,sub,h=1020):
 im=Image.new('RGB',(W,h),BG);d=ImageDraw.Draw(im);d.rectangle((0,0,W,12),fill=TEAL)
 text(d,60,40,title,43,b=True);text(d,62,112,sub,26,MUTED)
 d.line((60,h-83,W-60,h-83),fill=GRID,width=2);text(d,60,h-59,'《AI工程》第九章读书笔记 · 自绘学习示意 · 2026-10-21',23,MUTED)
 return im,d
def card(d,box,title,body=(),c=TEAL,fill='#E5F2F0',n=27):
 x,y,r,b=box;d.rounded_rectangle(box,18,fill=fill,outline=c,width=3);text(d,x+22,y+18,title,31,c,True)
 for i,s in enumerate(body):
  bb=d.textbbox((x+22,y+76+i*46),s,font=font(n));assert bb[2]<r-12 and bb[3]<b-8,(s,box,bb)
  text(d,x+22,y+76+i*46,s,n)
def arrow(d,a,b,c=TEAL):
 d.line((a,b),fill=c,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=18
 d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=c)
def save(im,name):im.save(OUT/name)

im,d=canvas('用户等待，需要明确计时边界','从提交问题到完整答案；阶段宽度为示意，不代表真实耗时。',1000)
for box,title,body,c,fill in [((60,230,320,405),'应用准备',['网络、检索、工具'],PURPLE,'#F0EAF7'),((355,230,565,405),'排队',['等待资源'],BLUE,'#E8F0FA'),((600,230,890,405),'预填充',['处理输入与状态'],TEAL,'#E5F2F0'),((935,230,1440,405),'解码',['逐步生成后续token'],BLUE,'#E8F0FA')]:card(d,box,title,body,c,fill,26)
for a,b in [((322,315),(347,315)),((568,315),(592,315)),((894,315),(927,315))]:arrow(d,a,b)
d.line((912,185,912,440),fill=RED,width=3);text(d,775,180,'首个token',27,RED,True)
card(d,(60,495,725,690),'客户端TTFT',['可包含网络、排队和预填充','检索是否计入，取决于测量起点'],PURPLE,'#F0EAF7',27)
card(d,(775,495,1440,690),'用户首个可见输出',['内部token可能是工具调用或中间步骤','需要另外记录端到端任务耗时'],BLUE,'#E8F0FA',27)
text(d,80,755,'简化关系：耗时 ≈ TTFT + (N − 1) × TPOT',34,TEAL,True)
text(d,80,820,'N为输出token总数；比较之前先统一起点、终点与实际输出长度。',28,MUTED)
save(im,'01-请求时间线.png')

im,d=canvas('内存层次：容量、带宽和数据路径','访问位置不同，容量与带宽也不同；图形面积不表示实际容量。',1040)
card(d,(95,205,725,375),'GPU片上SRAM',['较近、访问快；容量有限'],TEAL,'#E5F2F0',28)
card(d,(95,440,725,610),'GPU设备内存',['存放权重、KV缓存等；可为HBM或GDDR'],BLUE,'#E8F0FA',26)
card(d,(95,675,725,845),'CPU主机内存',['容量和访问路径取决于系统配置'],PURPLE,'#F0EAF7',27)
for y in [375,610]:arrow(d,(410,y+53),(410,y+8))
card(d,(805,205,1405,480),'容量回答：能否放下？',['权重 + 缓存 + 激活 + 运行时开销','并发与上下文长度都会影响需求'],TEAL,'#E5F2F0',26)
card(d,(805,550,1405,845),'带宽回答：搬运多快？',['计算单元反复读取所需数据','减少搬运与提高复用可能更有效','移到主机内存后还要考虑传输'],BLUE,'#E8F0FA',26)
text(d,95,892,'选择硬件时，同时检查容量、带宽、计算能力、功耗与软件支持。',28,MUTED)
save(im,'02-内存层次.png')

im,d=canvas('推测解码：提出草稿，再由目标模型验证','字母表示候选token；只展示接受前缀的关系，不替代采样验证算法。',980)
text(d,70,225,'草稿提出',30,b=True)
for i,ch in enumerate(['A','B','C','D']):card(d,(325+i*230,205,500+i*230,330),ch,(),BLUE,'#E8F0FA')
text(d,70,415,'目标验证',30,b=True)
for i,ch in enumerate(['A  接受','B  接受','C  拒绝','D  不采用']):
 c=TEAL if i<2 else RED;card(d,(325+i*230,395,500+i*230,520),ch,(),c,'#E5F2F0' if i<2 else '#F8ECEA')
arrow(d,(790,340),(790,380))
text(d,70,605,'本轮推进',30,b=True)
for i,ch in enumerate(['A','B','R']):card(d,(325+i*230,585,500+i*230,710),ch,(),TEAL,'#E5F2F0')
text(d,1060,610,'R：修正或后续token',25,MUTED)
text(d,80,775,'收益取决于：草稿成本、接受长度、验证开销与当前负载。',29,TEAL,True)
text(d,80,830,'无损采样需使用正确的接受和修正机制；随机输出不必逐字相同。',27,MUTED)
save(im,'03-推测解码.png')

im,d=canvas('KV缓存：复用已有位置的键和值','常规未压缩KV张量的容量估算；不包含其他运行时开销。',1080)
card(d,(65,205,650,435),'已有位置',['K1、K2、…、Ks','V1、V2、…、Vs'],TEAL,'#E5F2F0',29)
card(d,(860,205,1435,435),'处理新位置',['计算新的键与值','复用旧状态，并按规则扩展缓存'],BLUE,'#E8F0FA',27)
arrow(d,(655,320),(840,320))
text(d,100,500,'KV字节数 ≈ 2 × B × S × L × Hkv × Dh × b',35,TEAL,True)
lines(d,100,575,['2：键和值       B：序列数       S：每条序列长度       L：层数','Hkv：KV头数       Dh：每头维度       b：每个元素的字节数'],28,55)
card(d,(65,725,1435,910),'假设算例',['B=8，S=4096，L=32，Hkv=8，Dh=128，b=2 → 约4GiB','改变KV头数或缓存精度会改变容量；不同长度应逐条计算后求和。'],PURPLE,'#F0EAF7',28)
text(d,80,945,'缓存保存计算状态，不是最终答案；架构、压缩和内存管理会影响实际占用。',26,MUTED)
save(im,'04-KV缓存.png')

im,d=canvas('内核融合：减少中间结果的反复搬运','概念示意；实际融合条件和性能依赖算子、编译器与目标硬件。',980)
text(d,70,200,'分别执行',31,b=True)
for box,title,body,c,fill in [((70,280,410,470),'内核A',['计算中间结果'],BLUE,'#E8F0FA'),((560,280,935,470),'设备内存',['写入，再读回'],PURPLE,'#F0EAF7'),((1080,280,1430,470),'内核B',['读取后继续计算'],BLUE,'#E8F0FA')]:card(d,box,title,body,c,fill,28)
arrow(d,(415,375),(540,375));arrow(d,(940,375),(1060,375))
text(d,70,555,'合适的融合实现',31,b=True)
card(d,(70,635,1430,825),'融合内核',['让部分中间数据留在更近的存储中，减少不必要的写回与读取。','不保证所有算子都能融合，也不保证每种负载都获得相同收益。'],TEAL,'#E5F2F0',28)
save(im,'05-内核融合.png')

im,d=canvas('批处理：进入条件与生成中的补位','前两行说明组批条件，第三行说明迭代调度；格子不是实测时间。',1100)
card(d,(65,195,1435,365),'静态批处理',['固定数量组成一批；在线场景要处理等满造成的等待。'],BLUE,'#E8F0FA',29)
card(d,(65,410,1435,580),'动态批处理',['数量达到上限，或最长等待窗口到达，即可执行当前批次。'],PURPLE,'#F0EAF7',29)
text(d,80,635,'连续批处理：请求完成后退出，新请求加入后续迭代',30,TEAL,True)
for j,row in enumerate([['A','B','C'],['A','D','C'],['E','D','C']]):
 text(d,100,705+j*78,f'迭代{j+1}',27)
 for i,ch in enumerate(row):
  x=350+i*210;y=695+j*78;d.rounded_rectangle((x,y,x+160,y+58),10,fill='#E5F2F0',outline=TEAL,width=2);text(d,x+65,y+9,ch,27,TEAL,True)
text(d,1040,724,'B完成 → D补位',27,MUTED);text(d,1040,803,'A完成 → E补位',27,MUTED)
text(d,80,965,'批次进入与退出是不同维度；比较实际调度行为及延迟、吞吐量。',28,MUTED)
save(im,'06-批处理.png')

im,d=canvas('前缀缓存：复用共享输入的计算状态','同一模型及兼容配置下的示意；具体匹配与隔离规则以服务实现为准。',1030)
card(d,(65,200,1435,370),'稳定前缀',['任务规则 + 经允许共享的制度版本 + 固定示例'],TEAL,'#E5F2F0',30)
for x,title,body in [(65,'请求A',['前缀 + 问题A']),(550,'请求B',['前缀 + 问题B']),(1035,'请求C',['前缀 + 问题C'])]:
 card(d,(x,480,x+400,655),title,body,BLUE,'#E8F0FA',28);arrow(d,(x+200,370),(x+200,460))
card(d,(65,750,1435,925),'复用之后仍需工作',['处理变化的后缀，并生成本次答案；不等于复用过去的完整答案。','没有命中、前缀变化或状态被淘汰时，需要重新处理相应内容。'],PURPLE,'#F0EAF7',28)
save(im,'07-前缀缓存.png')

im,d=canvas('并行方式：分别拆分什么？','请求分流、层内协作与跨阶段流动解决不同问题；通信成本需另行测量。',1180)
card(d,(65,195,1435,415),'副本并行：不同请求分流',['请求A → 完整副本1          请求B → 完整副本2','增加同时服务的能力；单条请求不自动得到更快的单步计算。'],TEAL,'#E5F2F0',28)
card(d,(65,470,1435,690),'张量并行：共同完成层内运算',['同一层的张量分片 → 设备1与设备2协作 → 聚合或继续计算','可以分摊模型和计算，但会引入设备间通信。'],BLUE,'#E8F0FA',28)
card(d,(65,745,1435,965),'流水线并行：不同设备承载不同阶段',['微批次 → 阶段1 / 设备1 → 阶段2 / 设备2 → 后续阶段','可部署更大的模型；需要考虑传输、阶段平衡和空闲气泡。'],PURPLE,'#F0EAF7',28)
text(d,80,1020,'一个模型副本也可以跨多卡；副本并行与模型并行可以组合。',28,MUTED)
save(im,'08-并行方式.png')

thumbs=[]
for p in sorted(OUT.glob('*.png')):
 im=Image.open(p).convert('RGB');im.thumbnail((650,520));thumbs.append(im)
sheet=Image.new('RGB',(1320,sum(max(t.height for t in thumbs[i:i+2])+16 for i in range(0,len(thumbs),2))),'#dce5e9');y=0
for i in range(0,len(thumbs),2):
 for j,t in enumerate(thumbs[i:i+2]):sheet.paste(t,(j*660+5,y))
 y+=max(t.height for t in thumbs[i:i+2])+16
sheet.save(ROOT/'配图核对.png')
(ROOT/'绘图布局核对.json').write_text(json.dumps(dict(images=8,text_checks=len(checks),result='PASS'),ensure_ascii=False,indent=2),encoding='utf-8')
print('8张中文配图已生成，文字边界检查通过')

