from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0, r'C:\Users\crown\.cache\tooling\book-preview')
import markdown,base64,re,json,html
ROOT=Path(__file__).resolve().parent
files=sorted(ROOT.glob('0[123]-*.md'));records=[];articles=[]
for i,p in enumerate(files):
 md=p.read_text(encoding='utf-8-sig').strip();title=md.splitlines()[0][2:];body=md.split('\n',1)[1].strip()
 assert body.count('```')%2==0
 imgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',body);assert len(imgs)==[2,3,3][i]
 for path in imgs:
  f=ROOT/path;Image.open(f).verify();body=body.replace('('+path+')','(data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()+')')
 rendered=markdown.markdown(body,extensions=['tables','fenced_code'])
 articles.append(f'<article id="a{i}"><div class="controls"><button onclick="copy({i},true)">复制标题</button><button onclick="copy({i},false)">复制Markdown正文</button></div><h1>{html.escape(title)}</h1>{rendered}</article>')
 records.append(dict(file=p.name,title=title,body=md.split('\n',1)[1].strip(),chinese_characters=len(re.findall('[\u4e00-\u9fff]',md)),images=imgs))
css='''*{box-sizing:border-box}body{margin:0;background:#f1f5f7;color:#203e49;font:18px/1.9 "Microsoft YaHei",sans-serif}header{background:#173b48;color:white;padding:30px max(24px,calc((100vw - 960px)/2))}header h1{font-size:29px;margin:0}header p{font-size:15px}nav a{color:white;margin-right:24px}main{max-width:1050px;margin:24px auto;padding:0 20px}article{background:white;padding:40px 54px;margin-bottom:32px;border-radius:12px}h1{font-size:28px;line-height:1.5}h2{font-size:24px;border-left:5px solid #087f80;padding-left:14px;margin-top:36px}h3{font-size:21px;margin-top:30px}h4{font-size:19px}img{max-width:100%;height:auto;display:block;margin:25px auto}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.65;margin:22px 0}td,th{border:1px solid #ccdce0;padding:10px;text-align:left}th{background:#e8f2f2}blockquote{border-left:4px solid #aac9cb;padding:4px 18px;background:#f4f8f9;font-size:15px}a{color:#087f80}button{background:#087f80;color:white;border:0;border-radius:6px;padding:9px 15px;margin-right:10px;cursor:pointer;font:15px "Microsoft YaHei"}.controls{border-bottom:1px solid #d8e2e6;padding-bottom:20px}pre{overflow-x:auto;background:#f1f5f7;padding:16px;font-size:15px}@media(max-width:700px){article{padding:22px}body{font-size:17px}h1{font-size:24px}table{font-size:13px}}'''
data=json.dumps(records,ensure_ascii=False).replace('</','<\\/')
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第九章简书读书笔记 阅读与复制</title><style>'+css+'</style><header><h1>第九章简书读书笔记</h1><p>三篇文章 · 原书顺序 · 八张自绘图 · 本地阅读副本</p><nav>'+''.join(f'<a href="#a{i}">第{i+1}篇</a>' for i in range(3))+'</nav></header><main>'+''.join(articles)+'</main><script>const notes='+data+'; async function copy(i,title){await navigator.clipboard.writeText(title?notes[i].title:notes[i].body);}</script></html>'
(ROOT/'阅读预览与复制.html').write_text(page,encoding='utf-8')
(ROOT/'待上传内容.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
assert 0.8+199*0.02==4.78
assert 2*8*4096*32*8*128*2==4*1024**3
(ROOT/'本地核对.json').write_text(json.dumps([dict(file=r['file'],chinese_characters=r['chinese_characters'],images=len(r['images']),fences=r['body'].count('```'),result='PASS') for r in records],ensure_ascii=False,indent=2),encoding='utf-8')
print([(r['file'],r['chinese_characters'],len(r['images'])) for r in records])

