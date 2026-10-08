#pragma once
#include <pgmspace.h>

static const char INDEX_HTML[] PROGMEM = R"HTML(<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LED Kontrol</title>
<style>
:root{--bg:#f4f4f2;--fg:#1d1d1b;--card:#fff;--acc:#e8a33d;--mut:#7a7a74}
@media(prefers-color-scheme:dark){:root{--bg:#141413;--fg:#ecebe6;--card:#1f1f1d;--mut:#9a9a92}}
body{margin:0;font:16px system-ui,sans-serif;background:var(--bg);color:var(--fg);display:flex;justify-content:center}
main{width:100%;max-width:360px;padding:24px 16px}
.card{background:var(--card);border-radius:16px;padding:24px;box-shadow:0 1px 3px #0002}
h1{font-size:18px;margin:0 0 20px}
button{width:100%;height:96px;border:0;border-radius:12px;font-size:22px;font-weight:600;cursor:pointer;
background:#3a3a37;color:#fff;transition:background .2s}
button.on{background:var(--acc);color:#1d1d1b}
label{display:block;margin:24px 0 8px;color:var(--mut);font-size:14px}
input{width:100%;accent-color:var(--acc)}
small{display:block;margin-top:20px;color:var(--mut);font-size:12px}
</style></head><body><main><div class="card">
<h1>LED Şerit</h1>
<button id="b">…</button>
<label>Parlaklık <span id="v"></span>%</label>
<input id="s" type="range" min="1" max="100">
<small id="i"></small>
</div></main>
<script>
const b=document.getElementById('b'),s=document.getElementById('s'),v=document.getElementById('v'),i=document.getElementById('i');
function show(d){b.textContent=d.on?'AÇIK':'KAPALI';b.className=d.on?'on':'';
 if(document.activeElement!==s)s.value=d.brightness;v.textContent=d.brightness;
 i.textContent=d.ip+' · RSSI '+d.rssi+' dBm · '+Math.floor(d.uptime_s/60)+' dk';}
async function api(m,body){const r=await fetch('/api/state',{method:m,headers:{'Content-Type':'application/json'},
 body:body?JSON.stringify(body):undefined});show(await r.json());}
b.onclick=()=>api('POST',{toggle:true});
let t;s.oninput=()=>{v.textContent=s.value;clearTimeout(t);t=setTimeout(()=>api('POST',{brightness:+s.value,on:true}),120)};
api('GET');setInterval(()=>api('GET'),5000);
</script></body></html>)HTML";
