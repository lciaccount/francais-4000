const CACHE='fr4000-v13-fonts-offline-20260924';
const ASSETS=['./','./index.html','./learning-data-4000.js','./pronunciation-data-4000.js','./phonetics-data.js','./phonetics-sources.js','./phonetics.js','./phonetics.css','./swipe-study.js','./swipe-study.css','./audio/phonetics/manifest.json','./manifest.webmanifest','./icon-192.png','./icon-512.png','./audio/voice-manifest.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
// Retain already-downloaded sentence audio when updating the application shell.
self.addEventListener('activate',e=>{e.waitUntil((async()=>{
  const current=await caches.open(CACHE);
  for(const key of await caches.keys()){
    if(key===CACHE||!/^fr(?:2000|4000)-/.test(key))continue;
    const old=await caches.open(key);
    for(const request of await old.keys()){
      if(new URL(request.url).pathname.includes('/audio/')&&/\.mp3(?:\?|$)/.test(request.url)&&!(await current.match(request))){
        const response=await old.match(request);
        if(response?.status===200)await current.put(request,response);
      }
    }
    await caches.delete(key);
  }
  await self.clients.claim();
})());});

async function rangedAudio(request,response){
  const range=request.headers.get('range');
  if(!range||response.status!==200||!new URL(request.url).pathname.endsWith('.mp3'))return response;
  const match=range.match(/^bytes=(\d*)-(\d*)$/);
  if(!match||(!match[1]&&!match[2]))return response;
  const bytes=await response.arrayBuffer(),size=bytes.byteLength;
  const start=match[1]?Number(match[1]):Math.max(0,size-Number(match[2]));
  const end=match[1]&&match[2]?Math.min(Number(match[2]),size-1):size-1;
  if(start>end||start>=size)return new Response(null,{status:416,headers:{'Content-Range':`bytes */${size}`}});
  const headers=new Headers(response.headers);
  headers.set('Content-Range',`bytes ${start}-${end}/${size}`);
  headers.set('Content-Length',String(end-start+1));
  headers.set('Accept-Ranges','bytes');
  return new Response(bytes.slice(start,end+1),{status:206,statusText:'Partial Content',headers});
}

self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  // Keep third-party requests outside this app's offline cache.
  if(new URL(e.request.url).origin!==self.location.origin)return;
  e.respondWith((async()=>{
    const cache=await caches.open(CACHE),hit=await cache.match(e.request);
    if(hit)return rangedAudio(e.request,hit);
    try{
      // Cache a complete MP3 even when Safari/Chrome initially requests a range.
      let request=e.request;
      if(request.headers.has('range')&&new URL(request.url).pathname.endsWith('.mp3')){
        const headers=new Headers(request.headers);headers.delete('range');headers.delete('if-range');
        request=new Request(request,{headers});
      }
      const response=await fetch(request);
      // Cache writes must never turn a successful first download into a playback error.
      if(response.status===200){
        try{const saving=cache.put(e.request,response.clone()).catch(()=>{});e.waitUntil(saving);}catch{}
      }
      return rangedAudio(e.request,response);
    }catch{
      return e.request.mode==='navigate'?(await cache.match('./index.html'))||Response.error():Response.error();
    }
  })());
});

let phoneticsDownload=null;
const downloadPorts=new Set();
const notifyDownload=message=>downloadPorts.forEach(port=>port.postMessage(message));
async function cachePhonetics(){
  const cache=await caches.open(CACHE);
  let manifest=await cache.match('./audio/phonetics/manifest.json');
  if(!manifest){manifest=await fetch('./audio/phonetics/manifest.json');if(!manifest.ok)throw new Error('无法读取音频清单');await cache.put('./audio/phonetics/manifest.json',manifest.clone());}
  const {assets}=await manifest.json();
  let loaded=0,next=0;
  const failures=[];
  notifyDownload({loaded,total:assets.length});
  await Promise.all(Array.from({length:4},async()=>{
    while(next<assets.length){
      const path=assets[next++];
      try{
        if(!(await cache.match(path))){
          const response=await fetch(path,{signal:AbortSignal.timeout(25000)});
          if(response.status!==200)throw new Error('音频下载失败');
          await cache.put(path,response);
        }
        loaded++;
        notifyDownload({loaded,total:assets.length});
      }catch{failures.push(path);}
    }
  }));
  if(failures.length)throw new Error(`${failures.length} 个音频未能缓存（请检查网络或存储空间）`);
  notifyDownload({done:true,loaded,total:assets.length});
}
self.addEventListener('message',e=>{
  if(e.data?.type!=='CACHE_PHONETICS'||!e.ports[0])return;
  downloadPorts.add(e.ports[0]);
  if(!phoneticsDownload)phoneticsDownload=cachePhonetics().catch(error=>notifyDownload({error:error.message})).finally(()=>{downloadPorts.clear();phoneticsDownload=null;});
  e.waitUntil(phoneticsDownload);
});

// One bounded sentence download at a time; never disturb playback or lab downloads.
let sentenceDownload = null;
async function cacheSentenceRange(job) {
  const {start,end,port,controller} = job;
  const total = (end-start+1)*3;
  let loaded = 0, next = 0, failure = '';
  const send = extra => {try {port.postMessage({loaded,total,...extra});} catch { /* Page closed. */ }};
  port.onmessage = e => {if(e.data?.type==='CANCEL') controller.abort();};
  send({});
  try {
    const cache = await caches.open(CACHE);
    await Promise.all(Array.from({length:2}, async () => {
      while(next < total && !controller.signal.aborted) {
        const index = next++, slot = index%3+1, id = start+Math.floor(index/3);
        // Must match builtinAsset() exactly, including its audio revision.
        const path = `./audio/v${slot}/sent/${String(id).padStart(4,'0')}.mp3?v=fr4000v3`;
        const requestController = new AbortController();
        const abort = () => requestController.abort();
        controller.signal.addEventListener('abort',abort,{once:true});
        const timer = setTimeout(abort,25000);
        try {
          const hit = await cache.match(path);
          if(controller.signal.aborted) break;
          if(hit?.status !== 200) {
            const response = await fetch(path,{signal:requestController.signal});
            if(response.status !== 200 || !/^(audio\/|application\/octet-stream)/i.test(response.headers.get('content-type') || '')) throw new Error('音频响应无效');
            // Consume the entire body before persisting: no partial downloads in cache.
            const bytes = await response.arrayBuffer();
            if(controller.signal.aborted) break;
            if(!bytes.byteLength) throw new Error('音频为空');
            await cache.put(path,new Response(bytes,{status:200,headers:response.headers}));
          }
          loaded++;
          send({});
        } catch(error) {
          if(!controller.signal.aborted) {
            failure = error.name === 'QuotaExceededError' ? '存储空间不足，下载已停止' : '下载失败或超时，请检查网络与存储空间';
            controller.abort();
          }
        } finally {
          clearTimeout(timer); controller.signal.removeEventListener('abort',abort);
        }
      }
    }));
  } catch {failure = '无法使用离线缓存，请检查浏览器存储设置';}
  send(failure ? {error:failure} : controller.signal.aborted ? {cancelled:true} : {done:true});
  port.close();
}
self.addEventListener('message',e=>{
  if(e.data?.type!=='CACHE_SENTENCE_RANGE' || !e.ports[0]) return;
  const {start,end} = e.data, port = e.ports[0];
  if(!Number.isInteger(start) || !Number.isInteger(end) || start<1 || end>4000 || start>end) {
    port.postMessage({error:'句子区间无效'}); port.close(); return;
  }
  if(sentenceDownload) {port.postMessage({error:'另一个窗口正在下载句子音频，请稍后重试'}); port.close(); return;}
  const job = {start,end,port,controller:new AbortController()};
  sentenceDownload = job;
  e.waitUntil(cacheSentenceRange(job).finally(()=>{if(sentenceDownload===job) sentenceDownload=null;}));
});
