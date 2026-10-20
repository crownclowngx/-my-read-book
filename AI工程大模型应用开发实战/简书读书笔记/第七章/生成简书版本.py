from pathlib import Path
import re,json
root=Path(__file__).resolve().parent
out=root/'简书上传版本';out.mkdir(exist_ok=True)
diagrams={
'01-微调选择.png':'''记录任务、资料、输出与评分
             ↓
  ┌─ 信息缺失或过期 → 检查版本、检索和上下文
  ├─ 资料正确仍答不好 → 检查提示词、约束和模型
  │                    必要时评估微调
  └─ 涉及权限与动作 → 系统核验身份、对象与执行条件
             ↓
     同题比较改善与退步 → 决定采用或继续试验''',
'02-内存组成.png':'''推理：模型权重 + 激活值 + KV缓存 + 临时缓冲等
训练：模型权重 + 激活值 + 梯度 + 优化器状态等

模型总参数量 ── 影响基座权重的存储规模
可训练参数量 ── 影响梯度和优化器状态
序列长度、微批次等 ── 影响激活值及运行开销

减少可训练参数 ≠ 按相同比例减少全部内存''',
'03-数值表示.png':'''         符号      指数      有效数存储
FP32      1位       8位         23位
FP16      1位       5位         10位
BF16      1位       8位          7位

指数影响范围；有效数影响精度。
有效数存储位不含正规数的隐含首位。''',
'04-LoRA更新.png':'''原始权重 W：n × m，冻结
可训练 A：n × r    可训练 B：r × m
          └── 相乘 ──┘
          ΔW = AB：n × m
                ↓
       W′ = W + (α / r) × AB

可训练参数：nr + rm
基座权重：nm，仍需存储与参与计算''',
'05-多适配器部署.png':'''          同一兼容基座 W
          ↓           ↓
    任务适配器A       任务适配器B
    制度条款解释       材料与缺项整理

部署可以预先合并，也可以保留基座与适配器分离。
模型、分词器、模板和适配器版本需要对应。''',
'06-模型合并.png':'''求和与插值：对应参数按权重组合
             → 检查参数对应关系与任务效果

层堆叠：选择、复制并组合不同层
             → 检查新结构，通常需要继续训练

拼接：保留并连接组成部分
             → 维度和参数量增加，评估资源代价''',
'07-微调验证.png':'''明确失败与必须保留的能力
          ↓
准备训练数据，检查来源、切分与近似样本
          ↓
记录模型、模板和配置 → 训练与分组回归
          ↓
使用未参与调参的材料独立检验
          ↓
综合质量、费用与部署条件 → 采用、回退或继续试验

开发材料用于迭代；保留材料参与调参后，独立性会改变。'''
}
records=[]
for p in sorted(root.glob('0[123]-*.md')):
 s=p.read_text(encoding='utf-8')
 for name,text in diagrams.items():
  s=re.sub(r'!\[[^\]]*\]\(img/'+re.escape(name)+r'\)',lambda _: '```text\n'+text+'\n```',s)
 s=s.replace('配图自绘','结构图为文字示意').replace('配图为自绘','结构图为文字')
 s=s.replace('图1：自绘','图1：文字示意').replace('图2：自绘','图2：文字示意').replace('图3：自绘','图3：文字示意').replace('图4：自绘','图4：文字示意').replace('图5：自绘','图5：文字示意').replace('图6：自绘','图6：文字示意').replace('图7：自绘','图7：文字示意')
 s=s.replace('框的大小不代表实际内存比例；','本图只列出主要组成；').replace('两图为自绘示意','两图为文字示意').replace('四图为自绘概念图','四图为文字示意').replace('图为自绘概念图','图为文字示意')
 assert not re.search(r'!\[[^\]]*\]\(img/',s)
 assert s.count('```')%2==0
 (out/p.name).write_text(s,encoding='utf-8')
 records.append({'file':p.name,'title':s.splitlines()[0][2:],'body':s.split('\n',1)[1].strip(),'image_variant':'text_diagrams','chinese_characters':len(re.findall('[\u4e00-\u9fff]',s))})
(root/'待保存稿件.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print([(r['file'],len(r['body'])) for r in records])
