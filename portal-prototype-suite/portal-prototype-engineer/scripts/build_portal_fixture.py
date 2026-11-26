# Offline deterministic Portal acceptance fixture; not an autonomous designer.
import argparse, html, json, pathlib
p=argparse.ArgumentParser()
p.add_argument('--spec',required=True);p.add_argument('--output',required=True)
a=p.parse_args()
spec=json.loads(pathlib.Path(a.spec).read_text(encoding='utf-8'))
assert isinstance(spec['title'],str) and isinstance(spec['services'],list) and len(spec['services'])>0
services=[]
for obj in spec['services']:
 assert isinstance(obj['id'],str) and isinstance(obj['name'],str) and isinstance(obj['description'],str)
 services.append({k:html.escape(str(obj[k]),quote=True) for k in ('id','name','description')})
items=''.join(f'<article class="service-card" data-service="{o["id"]}"><h2>{o["name"]}</h2><p>{o["description"]}</p><button class="detail" data-id="{o["id"]}">查看详情</button></article>' for o in services)
name=html.escape(spec['title']);doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title><style>
:root{{--bg:#f5f7fb;--surface:#fff;--fg:#1c283c;--primary:#1554b4;--line:#d7deeb}}
[data-theme="dark"]{{--bg:#101827;--surface:#202c3f;--fg:#f2f5fa;--primary:#90baff;--line:#46566f}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,sans-serif}}
header{{background:var(--surface);border-bottom:1px solid var(--line);padding:18px max(24px,calc((100vw - 1100px)/2));display:flex;justify-content:space-between;gap:16px;align-items:center}}
nav{{display:flex;gap:12px;flex-wrap:wrap}}button{{font:inherit;cursor:pointer;border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:8px;padding:8px 13px}}button:focus-visible,input:focus-visible{{outline:3px solid var(--primary);outline-offset:2px}}.primary{{background:var(--primary);color:var(--bg);border-color:var(--primary)}}
main{{max-width:1100px;margin:32px auto;padding:0 24px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}}.service-card,.panel{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px}}h1{{font-size:30px;line-height:1.3}}h2{{font-size:19px}}.muted{{opacity:.8}}input{{width:100%;padding:10px;background:var(--surface);color:var(--fg);border:1px solid var(--line);border-radius:8px}}dialog{{background:var(--surface);color:var(--fg);border:1px solid var(--line);border-radius:12px;max-width:480px;width:calc(100% - 36px)}}dialog::backdrop{{background:#0008}}[hidden]{{display:none!important}}#notice{{min-height:24px}}
@media(max-width:600px){{header{{padding:12px 16px;flex-direction:column;align-items:flex-start}}main{{margin:18px auto;padding:0 16px}}h1{{font-size:24px}}}}
</style></head><body data-theme="light"><header><strong>{name}</strong><nav aria-label="主导航"><button data-route="home">首页</button><button data-route="catalog">服务目录</button><button data-route="account">个人中心</button><button id="theme">切换主题</button></nav></header>
<main><section id="home"><h1>发现适合您的企业服务</h1><p class="muted">从发现、了解，到收藏与管理，完成可演示的服务旅程。</p><button class="primary" data-route="catalog">浏览服务</button></section>
<section id="catalog" hidden><h1>服务目录</h1><label for="search">搜索服务</label><input id="search" placeholder="输入服务名称"><p id="count"></p><div class="grid" id="cards">{items}</div><p id="empty" hidden>暂无匹配服务</p></section>
<section id="account" hidden><h1>个人中心</h1><div class="panel"><h2>我的收藏</h2><ul id="saved"></ul><button id="reset">重置演示数据</button></div></section><p id="notice" role="status" aria-live="polite"></p></main>
<dialog id="detailDialog" aria-labelledby="detailTitle"><h2 id="detailTitle"></h2><p id="detailDesc"></p><button id="save">收藏服务</button><button id="close">关闭</button></dialog>
<script>const services={json.dumps(spec['services'],ensure_ascii=False).replace('</','<\\/')};let saved=[];let active=null;const byId=id=>document.getElementById(id);const notice=t=>byId('notice').textContent=t;
function route(name){{for(const id of ['home','catalog','account'])byId(id).hidden=id!==name;if(name==='account')renderSaved();if(name==='catalog')filter();notice('')}}
function filter(){{const q=byId('search').value.toLowerCase();let n=0;document.querySelectorAll('.service-card').forEach(c=>{{const match=c.textContent.toLowerCase().includes(q);c.hidden=!match;if(match)n++}});byId('count').textContent='共 '+n+' 项服务';byId('empty').hidden=n!==0}}
function renderSaved(){{byId('saved').innerHTML='';for(const id of saved){{const s=services.find(x=>x.id===id);const li=document.createElement('li');li.textContent=s.name;byId('saved').appendChild(li)}}if(!saved.length){{const li=document.createElement('li');li.textContent='尚未收藏服务';byId('saved').appendChild(li)}}}}
document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>route(b.dataset.route));document.querySelectorAll('.detail').forEach(b=>b.onclick=()=>{{active=services.find(x=>x.id===b.dataset.id);byId('detailTitle').textContent=active.name;byId('detailDesc').textContent=active.description;byId('detailDialog').showModal()}});
byId('close').onclick=()=>byId('detailDialog').close();byId('save').onclick=()=>{{if(!saved.includes(active.id))saved.push(active.id);byId('detailDialog').close();notice('已收藏：'+active.name)}};byId('search').oninput=filter;byId('reset').onclick=()=>{{saved=[];renderSaved();notice('演示数据已重置')}};byId('theme').onclick=()=>{{document.body.dataset.theme=document.body.dataset.theme==='light'?'dark':'light'}};route('home');</script></body></html>'''
path=pathlib.Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(doc,encoding='utf-8');print(json.dumps({'output':str(path),'services':len(services)},ensure_ascii=False))
