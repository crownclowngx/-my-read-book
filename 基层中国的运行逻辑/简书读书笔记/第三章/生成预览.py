from pathlib import Path
import sys,base64,re,json,html,hashlib

sys.path.insert(0,r'C:\Users\crown\.cache\tooling\book-preview')
from PIL import Image
import markdown
ROOT=Path(__file__).resolve().parent
p=ROOT/'01-基层首长的权力清单.md'
md=p.read_text(encoding='utf-8').strip();title=md.splitlines()[0][2:];body=md.split('\n',1)[1].strip()
imgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',body)
assert len(imgs)==4 and len(set(imgs))==4
assert len(re.findall(r'^## 第',body,re.M))==4
for imagepath in imgs:
    f=ROOT/imagepath;Image.open(f).verify()
    body=body.replace('('+imagepath+')','(data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()+')')
rendered=markdown.markdown(body,extensions=['tables','fenced_code'])
css='''*{box-sizing:border-box}body{margin:0;background:#f1f5f7;color:#203e49;font:18px/1.95 "Microsoft YaHei",sans-serif}header{background:#173b48;color:white;padding:28px max(24px,calc((100vw - 960px)/2))}header h1{font-size:28px;margin:0;line-height:1.6}header p{font-size:15px}main{max-width:1050px;margin:24px auto;padding:0 20px}article{background:white;padding:40px 54px;border-radius:12px}h2{font-size:25px;border-left:5px solid #087f80;padding-left:14px;margin-top:42px}h3{font-size:22px;margin-top:30px}h4{font-size:20px}img{max-width:100%;height:auto;display:block;margin:25px auto}table{border-collapse:collapse;width:100%;font-size:16px;line-height:1.7;margin:24px 0}td,th{border:1px solid #ccdce0;padding:11px;text-align:left}th{background:#e8f2f2}blockquote{border-left:4px solid #aac9cb;padding:4px 18px;background:#f4f8f9;font-size:15px}a{color:#087f80}button{background:#087f80;color:white;border:0;border-radius:6px;padding:9px 15px;margin-right:10px;cursor:pointer;font:15px "Microsoft YaHei"}.controls{border-bottom:1px solid #d8e2e6;padding-bottom:20px}em{color:#526a75;font-size:15px}@media(max-width:700px){article{padding:22px}body{font-size:17px}table{font-size:13px}td,th{padding:7px}}'''
record=dict(file=p.name,title=title,body=md.split('\n',1)[1].strip(),images=imgs,chinese_characters=len(re.findall('[\u4e00-\u9fff]',md)))
data=json.dumps(record,ensure_ascii=False).replace('</','<\\/')
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第三章读后感 阅读与复制</title><style>'+css+'</style><header><h1>'+html.escape(title)+'</h1><p>单篇完整读后感 · 原书四节顺序 · 三张自绘图与一张原书图</p></header><main><article><div class="controls"><button onclick="copy(true)">复制标题</button><button onclick="copy(false)">复制Markdown正文</button></div>'+rendered+'</article></main><script>const note='+data+';async function copy(title){await navigator.clipboard.writeText(title?note.title:note.body);}</script></html>'
(ROOT/'阅读预览与复制.html').write_text(page,encoding='utf-8')
(ROOT/'待上传内容.json').write_text(json.dumps([record],ensure_ascii=False,indent=2),encoding='utf-8')
checks=dict(file=p.name,chinese_characters=record['chinese_characters'],images=len(imgs),sections=4,table_count=rendered.count('<table>'),source_sha256=hashlib.sha256(md.encode()).hexdigest(),result='PASS')
(ROOT/'本地核对.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))

