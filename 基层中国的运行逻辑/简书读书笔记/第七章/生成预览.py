from pathlib import Path
import sys,base64,re,json,html,hashlib
sys.path.insert(0,r'C:\Users\crown\.cache\tooling\book-preview')
from PIL import Image
import markdown
ROOT=Path(__file__).resolve().parent
p=ROOT/'01-基层治理的困境.md'
md=p.read_text(encoding='utf8').strip();title=md.splitlines()[0][2:];body=md.split('\n',1)[1].strip()
imgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',body)
assert len(imgs)==len(set(imgs))==4
assert len(re.findall(r'^## 第',body,re.M))==4
assert len(re.findall(r'^### [一二三四五六七八九十]+、',body,re.M))==12
assert len(re.findall(r'^#### [1-5]\. ',body,re.M))==5
embedded=body
for path in imgs:
 Image.open(ROOT/path).verify()
 embedded=embedded.replace('('+path+')','(data:image/png;base64,'+base64.b64encode((ROOT/path).read_bytes()).decode()+')')
rendered=markdown.markdown(embedded,extensions=['tables','fenced_code'])
css='''*{box-sizing:border-box}body{margin:0;background:#f1f5f7;color:#203e49;font:18px/1.95 "Microsoft YaHei",sans-serif}header{background:#173b48;color:white;padding:28px max(24px,calc((100vw - 960px)/2))}h1{font-size:28px;margin:0;line-height:1.6}main{max-width:1050px;margin:24px auto;padding:0 20px}article,.controls{background:white;padding:30px 48px;border-radius:12px;margin-bottom:24px}h2{font-size:25px;border-left:5px solid #087f80;padding-left:14px;margin-top:42px}h3{font-size:22px;margin-top:30px}h4{font-size:20px;margin-top:26px}img{max-width:100%;height:auto;display:block;margin:25px auto}blockquote{border-left:4px solid #aac9cb;padding:4px 18px;background:#f4f8f9;font-size:15px}a{color:#087f80}textarea,input{width:100%;font:14px/1.6 "Microsoft YaHei";padding:10px;border:1px solid #ccdce0}textarea{height:135px}em{color:#526a75;font-size:15px}@media(max-width:700px){article,.controls{padding:22px}body{font-size:17px}}'''
record=dict(file=p.name,title=title,body=body,images=imgs,chinese_characters=len(re.findall('[\u4e00-\u9fff]',md)))
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第七章读后感 阅读与复制</title><style>'+css+'</style><header><h1>'+html.escape(title)+'</h1><p>单篇完整读后感 · 原书四节十二小节 · 四张中文自绘图</p></header><main><div class="controls"><label>文章标题<input id="draft-title" aria-label="文章标题" readonly value="'+html.escape(title,quote=True)+'"></label><label>Markdown正文<textarea id="draft-body" aria-label="Markdown正文" readonly>'+html.escape(body)+'</textarea></label></div><article>'+rendered+'</article></main></html>'
(ROOT/'阅读预览与复制.html').write_text(page,encoding='utf8')
(ROOT/'待上传内容.json').write_text(json.dumps([record],ensure_ascii=False,indent=2),encoding='utf8')
checks=dict(file=p.name,chinese_characters=record['chinese_characters'],images=len(imgs),sections=4,subsections=12,subheadings=5,body_sha256=hashlib.sha256(body.encode()).hexdigest(),result='PASS')
(ROOT/'本地核对.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(checks,ensure_ascii=True))
