from pathlib import Path
import sys,re,json,html,base64
sys.path.insert(0,r'C:\Users\crown\.cache\tooling\book-preview')
import markdown
from PIL import Image
ROOT=Path(__file__).resolve().parent
files=sorted(ROOT.glob('0[123]-*.md'))
records=[];sections=[]
css='''*{box-sizing:border-box}body{margin:0;background:#f1f5f7;color:#203e49;font:18px/1.9 "Microsoft YaHei",sans-serif}header{background:#173b48;color:white;padding:30px max(24px,calc((100vw - 960px)/2))}header h1{font-size:29px;margin:0}header p{font-size:15px}nav a{color:white;margin-right:24px}main{max-width:1050px;margin:24px auto;padding:0 20px}article{background:white;padding:40px 54px;margin-bottom:32px;border-radius:12px}h1{font-size:28px;line-height:1.5}h2{font-size:24px;border-left:5px solid #087f80;padding-left:14px;margin-top:36px}h3{font-size:21px;margin-top:30px}h4{font-size:19px}img{max-width:100%;height:auto;display:block;margin:25px auto}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.65;margin:22px 0}td,th{border:1px solid #ccdce0;padding:10px;text-align:left}th{background:#e8f2f2}blockquote{border-left:4px solid #aac9cb;padding:4px 18px;background:#f4f8f9;font-size:15px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf3f5;padding:18px;font:15px/1.7 Consolas,"Microsoft YaHei",monospace}a{color:#087f80}button{background:#087f80;color:white;border:0;border-radius:6px;padding:9px 15px;margin:0 10px 12px 0;cursor:pointer;font:15px "Microsoft YaHei"}.controls{border-bottom:1px solid #d8e2e6;padding-bottom:10px}@media(max-width:700px){article{padding:22px}body{font-size:17px}h1{font-size:24px}table{font-size:13px}}'''
for i,p in enumerate(files):
    md=p.read_text(encoding='utf-8');title=md.splitlines()[0][2:];body=md.split('\n',1)[1].strip()
    assert body.count('```')%2==0
    images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',body)
    assert len(images)==[2,2,1][i]
    inline=body
    for path in images:
        f=ROOT/path;im=Image.open(f);im.verify()
        inline=inline.replace('('+path+')','(data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()+')')
    uploaded=ROOT/'简书上传版本'/p.name
    online=uploaded.read_text(encoding='utf-8').split('\n',1)[1].strip() if uploaded.exists() else None
    record=dict(file=p.name,title=title,body=body,online=online,chinese_characters=len(re.findall('[\u4e00-\u9fff]',md)),images=images)
    records.append(record)
    buttons=f'<button onclick="copy({i},\'title\')">复制标题</button><button onclick="copy({i},\'body\')">复制本地Markdown</button>'
    if online:buttons+=f'<button onclick="copy({i},\'online\')">复制简书图片版正文</button>'
    sections.append(f'<article id="a{i}"><div class="controls">{buttons}</div><h1>{html.escape(title)}</h1>'+markdown.markdown(inline,extensions=['tables','fenced_code'])+'</article>')
data=json.dumps(records,ensure_ascii=False).replace('</','<\\/')
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第八章简书读书笔记 阅读与复制</title><style>'+css+'</style><header><h1>第八章简书读书笔记</h1><p>数据策展 · 数据增强与合成 · 数据处理 | 五张自绘图 | 本地阅读副本</p><nav>'+''.join(f'<a href="#a{i}">第{i+1}篇</a>' for i in range(3))+'</nav></header><main>'+''.join(sections)+'</main><script>const notes='+data+'; async function copy(i,key){await navigator.clipboard.writeText(notes[i][key]);}</script></html>'
(ROOT/'阅读预览与复制.html').write_text(page,encoding='utf-8')
# Structural and arithmetic verification for the actual article examples.
assert min(700,600)+min(500,600)==1100
assert 2*min(700,600)==1200
assert 2*700-1200==200
code=re.findall(r'```json\n(.*?)\n```',files[2].read_text(encoding='utf-8'),re.S)
assert len(code)==1 and len(json.loads(code[0])['messages'])==3
assert not any('图片上传中' in r['body'] or '上传失败' in r['body'] for r in records)
(ROOT/'本地核对.json').write_text(json.dumps([dict(file=r['file'],chinese_characters=r['chinese_characters'],images=len(r['images']),fences_balanced=True) for r in records],ensure_ascii=False,indent=2),encoding='utf-8')
saved=ROOT/'简书保存记录.json'
if saved.exists():
    r=json.loads(saved.read_text(encoding='utf-8'))
    assert len(r['records'])==3 and len(r['imageMap'])==5 and r['published'] is False
    for item in r['records']:
        md=(ROOT/'简书上传版本'/item['name']).read_text(encoding='utf-8')
        assert md.splitlines()[0][2:]==item['title']
        assert md.split('\n',1)[1].strip()==item['body']
        assert all(item[k] for k in ['verifiedBody','verifiedTitle','savedIndicator','publishActionPresent'])
        assert '](img/' not in item['body']
    assert page.count('src="data:image/png;base64,')==5
    im=Image.open(ROOT/'简书草稿保存凭证.png');im.verify()
    print('平台三篇完整回读结果与本地副本一致；五张平台图片映射及保存凭证通过检查')
print('三篇正文、五张图片、代码围栏、JSON和金额示例检查通过')
