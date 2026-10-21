import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const {marked}=await import(pathToFileURL('C:/Users/crown/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js'));
let md=await fs.readFile(path.join(root,'04-简书完整文章.md'),'utf8');
const math=[
  '<mi>S</mi><mo>=</mo><mi>N</mi><mo>×</mo><mi>b</mi><mo>×</mo><mi>u</mi>',
  '<msub><mi>c</mi><mtext>success</mtext></msub><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mtext>inference</mtext></msub><mo>+</mo><msub><mi>C</mi><mtext>integration</mtext></msub><mo>+</mo><msub><mi>C</mi><mtext>review</mtext></msub><mo>+</mo><msub><mi>C</mi><mtext>rework</mtext></msub></mrow><msub><mi>N</mi><mtext>successful tasks</mtext></msub></mfrac>',
  '<msub><mi>C</mi><mtext>API</mtext></msub><mo>=</mo><mi>p</mi><mi>Q</mi><mo>,</mo><mspace width="2em"/><msub><mi>C</mi><mtext>private</mtext></msub><mo>=</mo><mi>F</mi><mo>+</mo><mi>v</mi><mi>Q</mi>',
  '<msup><mi>Q</mi><mo>*</mo></msup><mo>=</mo><mfrac><mi>F</mi><mrow><mi>p</mi><mo>−</mo><mi>v</mi></mrow></mfrac><mo>,</mo><mspace width="2em"/><mi>p</mi><mo>&gt;</mo><mi>v</mi>',
  '<mfrac><msub><mi>H</mi><mtext>new</mtext></msub><msub><mi>H</mi><mtext>old</mtext></msub></mfrac><mo>=</mo><mfrac><msub><mi>G</mi><mtext>demand</mtext></msub><msub><mi>G</mi><mtext>efficiency</mtext></msub></mfrac>'
];
let index=0;
md=md.replace(/\$\$[\s\S]*?\$\$/g,()=>`\n\nMATHPLACEHOLDER${index++}\n\n`);
if(index!==math.length)throw Error('公式数量不匹配');
for(const m of [...md.matchAll(/!\[[^\]]*\]\((img\/[^)]+)\)/g)]) {
  const bytes=await fs.readFile(path.join(root,m[1]));
  md=md.replace('('+m[1]+')','(data:image/png;base64,'+bytes.toString('base64')+')');
}
let body=marked.parse(md);
math.forEach((m,i)=>body=body.replace(`<p>MATHPLACEHOLDER${i}</p>`,`<div class="math"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block">${m}</math></div>`));
const css='*{box-sizing:border-box}body{margin:0;background:#eef3f7;color:#243549;font:18px/1.95 "Microsoft YaHei",sans-serif}main{max-width:1050px;margin:35px auto;background:white;padding:45px 65px}h1{font-size:32px;line-height:1.5}h2{font-size:25px;margin-top:44px;border-left:5px solid #087f8c;padding-left:14px}p{margin:20px 0}a{color:#087f8c}blockquote{border-left:4px solid #92b8be;background:#f3f7f8;margin:24px 0;padding:5px 22px;font-size:16px}img{display:block;max-width:100%;height:auto;margin:30px auto}table{border-collapse:collapse;width:100%;font-size:16px}td,th{border:1px solid #d1dde5;padding:12px;text-align:left}th{background:#eaf2f5}.math{overflow:auto;padding:20px 0;font-size:22px}em{color:#526578;font-size:16px}@media(max-width:700px){main{padding:24px;margin:0}body{font-size:17px}h1{font-size:26px}h2{font-size:22px}.math{font-size:18px}}';
await fs.writeFile(path.join(root,'完整图文预览.html'),'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DeepInfer 简书完整图文预览</title><style>'+css+'</style><main>'+body+'</main></html>','utf8');
console.log('已生成自包含预览：4张原图，5组原生MathML公式');
