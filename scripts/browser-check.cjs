// Verificação de navegador do oscoach: sem pageerror, total de tópicos, contagem por módulo, sem overflow no celular.
// Uso: BASE_URL=http://127.0.0.1:PORT [LANG_PREFIX=en/] node scripts/browser-check.cjs
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'/home/nmaldaner/projetos/timesmkt3/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const base=(process.env.BASE_URL||'http://127.0.0.1:8931')+'/'+(process.env.LANG_PREFIX||'');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../curso/_shared/manifest.json'),'utf8'));
const total=manifest.tracks.reduce((a,t)=>a+t.modules.reduce((b,m)=>b+m.topics,0),0);
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(page.url()+' '+e.message));
 await page.goto(base);await page.waitForTimeout(300);
 assert.equal(await page.evaluate(()=>INEMA.progress('curso').total),total,'total de tópicos');
 const urls=[''];
 for(const t of manifest.tracks){urls.push(`curso/trilha${t.n}/index.html`);for(const m of t.modules){
  await page.goto(base+m.href);
  const n=await page.locator('[data-inema-topic]').count();assert.equal(n,m.topics,`tópicos ${m.id}`);
  const toc=await page.locator('[data-inema-toc] a').count();assert.equal(toc,m.topics,`TOC ${m.id}`);
 }}
 for(const u of urls){await page.goto(base+u);}
 await page.setViewportSize({width:390,height:844});
 for(const u of ['','curso/trilha5/modulo-5-7.html','curso/trilha2/modulo-2-3.html']){await page.goto(base+u);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+u);}
 fs.mkdirSync(path.join(__dirname,'../.verificacao'),{recursive:true});
 await page.screenshot({path:path.join(__dirname,`../.verificacao/m57-${(process.env.LANG_PREFIX||'pt/').slice(0,2)}-mobile.png`),fullPage:false});
 assert.deepEqual(errors,[]);
 console.log(`OK ${process.env.LANG_PREFIX||'pt/'}: ${total} tópicos, 22 módulos conferidos (DOM+TOC), sem erro JS, sem overflow no celular.`);
 await browser.close();
})().catch(e=>{console.error('FALHOU',e.message);process.exit(1)});
