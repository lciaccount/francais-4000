#!/usr/bin/env python3
"""Actual media playback tests for fine-grained speed and cold-load recovery."""
from test_swipe_auto_lock import (
    settings, ROOT, PREFIX, Handler, ready, enter, card_id,
    ThreadingHTTPServer, Thread, partial, Path, tempfile, sync_playwright,
)

INIT = '''
Element.prototype.requestFullscreen=undefined;
window.audioEvents=[];window.createdAudio=0;window.playCalls=[];window.denyNext=false;
window.perElementPolicy=false;window.allowedElement=null;
const NativeAudio=window.Audio;
window.Audio=function(...args){
  const a=new NativeAudio(...args),id=++createdAudio;
  a.addEventListener('playing',()=>audioEvents.push({src:a.src,rate:a.playbackRate,id}));
  return a;
};
const nativePlay=HTMLMediaElement.prototype.play;
HTMLMediaElement.prototype.play=function(){
  playCalls.push(this.src);
  if(denyNext){denyNext=false;return Promise.reject(new DOMException('Test autoplay policy','NotAllowedError'));}
  if(perElementPolicy&&this!==allowedElement)return Promise.reject(new DOMException('New media element has no gesture authorization','NotAllowedError'));
  return nativePlay.call(this);
};
'''


def speed_tests(browser, base, shots):
    context = browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
    context.add_init_script(INIT)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    ready(page, base)
    enter(page)
    expected = [f'{(50+i*5)/100:.2f}' for i in range(31)]
    assert page.locator('#swipeSpeed option').evaluate_all('els=>els.map(el=>el.value)') == expected
    page.wait_for_function('state.audio && state.audio.currentTime>0')
    page.evaluate('window.originalPlayer=state.audio')
    for rate in ['0.50','0.55','0.75','1.05','1.35','1.95','2.00']:
        page.locator('#swipeSpeed').select_option(rate)
        assert page.evaluate('state.audio===originalPlayer')
        assert page.evaluate('state.audio.playbackRate') == float(rate)
        assert float(page.locator('#speed').input_value()) == float(rate)
        assert page.locator('#speedValue').inner_text() == rate+'×'
    page.locator('#swipePause').click()
    page.locator('#swipeSpeed').select_option('0.85')
    assert page.evaluate('state.mode===null')
    page.locator('#swipePause').click()
    page.wait_for_function('state.audio && state.audio.playbackRate===.85')
    page.locator('#swipeSpeed').select_option('0.75')
    assert page.locator('#swipeSpeed').input_value() == '0.75'
    page.locator('#swipeSpeed').select_option('0.85')
    assert page.locator('#swipeSpeed').input_value() == '0.85'
    page.locator('#swipeSpeed').select_option('0.75')
    page.locator('#swipeSpeed').select_option('1.15')
    assert page.locator('#swipeSlow').count() == 0
    page.locator('#swipeLock').click()
    assert page.locator('#swipeSpeed').is_hidden()
    assert page.locator('.swipeSpeedLabel').evaluate('el=>el.inert')
    page.locator('#swipeLock').click()
    page.locator('#swipeExit').click()
    page.reload(wait_until='networkidle')
    enter(page)
    assert page.locator('#swipeSpeed').input_value() == '1.15'
    page.wait_for_function('state.audio && state.audio.playbackRate===1.15')
    page.locator('#swipeKind').select_option('letter')
    page.wait_for_function('state.audio && state.audio.currentTime>0')
    assert page.evaluate('state.audio.playbackRate') == 1.15
    page.locator('#swipeKind').select_option('sound')
    page.wait_for_function('state.audio && state.audio.currentTime>0')
    page.locator('#swipeSpeed').select_option('0.65')
    assert page.evaluate('state.audio.playbackRate') == .65
    page.locator('#swipeExample').click()
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/phonetics/si.mp3")&&e.rate===.65)')
    for width,height in [(320,568),(390,844),(844,390),(1280,900)]:
        page.set_viewport_size({'width':width,'height':height})
        assert page.locator('#swipeStudy').evaluate('el=>el.scrollWidth<=el.clientWidth+1 && el.scrollHeight<=el.clientHeight+1')
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(shots/'speed-mobile.png'))
    assert not errors, errors
    context.close()
    print('PASS: 31 exact speed options, in-place updates, pause/slow/lock, persistence, letters/IPA/examples and responsive layout',flush=True)


def recovery_tests(browser, base):
    context = browser.new_context(viewport={'width':1280,'height':900}, service_workers='block')
    context.add_init_script(INIT)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    ready(page, base)
    page.locator('#voiceMode').select_option('builtin-cycle')
    enter(page)
    page.wait_for_function('state.audio && state.audio.currentTime>0')
    # Model Safari's per-element authorization; this is not a real iOS browser test.
    page.evaluate('allowedElement=state.audio;perElementPolicy=true')
    page.locator('#swipePause').click()
    page.locator('#swipeSpeed').select_option('1.25')
    requests = {}
    def transient(route):
        src = route.request.url
        requests[src] = requests.get(src,0)+1
        if requests[src] == 1: route.abort()
        else: route.continue_()
    page.route('**/sent/002*.mp3?*',transient)
    page.evaluate('audioEvents=[]')
    settings(page,repeats=3,start=21,end=22)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("本轮已完成")',timeout=45000)
    played = page.evaluate(r'audioEvents.map(e=>e.src.match(/audio\/(v\d)\/sent\/(\d+)\.mp3/).slice(1))')
    assert played == [[f'v{v}',f'{s:04d}'] for s in [21,22] for v in [1,2,3]], played
    assert len(requests)==6 and all(n==2 for n in requests.values()),requests
    assert page.evaluate('new Set(audioEvents.map(e=>e.id)).size')==1
    assert all(e['rate']==1.25 for e in page.evaluate('audioEvents'))
    page.unroute('**/sent/002*.mp3?*')
    print('PASS: every cold voice recovers on the SAME voice; exact 3-repeat sequence and shared player under simulated per-element authorization',flush=True)

    failed=[]
    page.route('**/sent/0040.mp3?*',lambda r:(failed.append(r.request.url),r.abort()))
    settings(page,repeats=3,start=40,end=40)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("未能播放")')
    assert len(failed)==3 and all('/v1/' in src for src in failed),failed
    page.wait_for_timeout(1100)
    assert len(failed)==3 and page.evaluate('state.mode===null')
    page.unroute('**/sent/0040.mp3?*')
    page.evaluate('audioEvents=[]')
    page.locator('#swipePause').click()
    page.wait_for_function('audioEvents.length>0')
    assert '/v1/sent/0040.mp3' in page.evaluate('audioEvents[0].src')
    page.locator('#swipePause').click()
    print('PASS: persistent failure has bounded retries; manual continue retains the failed voice, with no phantom completed repeat',flush=True)

    # Autoplay denial needs a gesture, not network retries or a misleading network error.
    page.evaluate('denyNext=true;playCalls=[]')
    settings(page,repeats=2,start=41,end=41)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("浏览器阻止")')
    page.wait_for_timeout(1100)
    assert page.evaluate('playCalls.length')==1
    page.locator('#swipePause').click()
    page.wait_for_function('state.audio && state.audio.currentTime>0')
    assert '/v1/sent/0041.mp3' in page.evaluate('state.audio.src')
    print('PASS: permission denial is distinguished from load failure and manual authorization retries the same voice',flush=True)

    # Stop, skip and exit must cancel pending retry timers.
    attempts=[]
    page.route('**/sent/0042.mp3?*',lambda r:(attempts.append(r.request.url),r.abort()))
    settings(page,start=42,end=43)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("重试")')
    page.evaluate('SwipeStudy.step(1)')
    n=len(attempts)
    page.wait_for_timeout(1200)
    assert len(attempts)==n and card_id(page)=='43'
    assert '/0043.mp3' in page.evaluate('state.audio.src')
    settings(page,start=42,end=43)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("重试")')
    page.locator('#swipeExit').click()
    n=len(attempts)
    page.wait_for_timeout(1200)
    assert len(attempts)==n and page.evaluate('state.audio===null && state.mode===null')
    assert not errors,errors
    context.close()
    print('PASS: switching and exiting during recovery cancels stale retries without overlapping audio',flush=True)


def system_and_cache_tests(browser, base):
    context=browser.new_context(service_workers='block')
    context.add_init_script('''Element.prototype.requestFullscreen=undefined;
      window.speechCalls=[];speechSynthesis.speak=u=>speechCalls.push(u);speechSynthesis.cancel=()=>{};''')
    page=context.new_page()
    ready(page,base)
    page.locator('#voiceMode').select_option('system',force=True)
    page.locator('#playPattern').select_option('fr-zh-fr',force=True)
    enter(page)
    page.locator('#swipeSpeed').select_option('1.35')
    assert page.evaluate('speechCalls.length')==1
    page.evaluate('speechCalls[0].onend()')
    page.wait_for_function('speechCalls.length===2')
    lang,rate=page.evaluate('[speechCalls[1].lang,speechCalls[1].rate]')
    assert lang=='zh-CN' and abs(rate-1.35)<1e-6,(lang,rate)  # Speech rate is a float32.
    page.locator('#swipeSpeed').select_option('1.65')
    page.evaluate('speechCalls[1].onend()')
    page.wait_for_function('speechCalls.length===3')
    lang,rate=page.evaluate('[speechCalls[2].lang,speechCalls[2].rate]')
    assert lang=='fr-FR' and abs(rate-1.65)<1e-6,(lang,rate)
    page.locator('#swipeExit').click()
    # Run the real worker handler with failed storage/lifetime operations. A valid
    # network response must still reach the media element on its FIRST request.
    assert page.evaluate('''async () => {
      const source=await (await fetch('./sw.js')).text();
      for(const failure of ['put-sync','put-async','waitUntil']){
        const listeners={};
        const worker={location:{origin:location.origin},addEventListener:(type,fn)=>listeners[type]=fn};
        const store={match:async()=>undefined,put:()=>{
          if(failure==='put-sync')throw new Error('storage unavailable');
          return failure==='put-async'?Promise.reject(new Error('quota exceeded')):Promise.resolve();
        }};
        let requestedRange='not fetched';
        const network=async request=>{
          requestedRange=request.headers.get('range');
          return new Response(new Uint8Array(100).fill(7),{headers:{'Content-Type':'audio/mpeg'}});
        };
        new Function('self','caches','fetch',source)(worker,{open:async()=>store},network);
        let result;
        listeners.fetch({request:new Request(new URL('./audio/v1/sent/0010.mp3',location.href),{headers:{Range:'bytes=0-49'}}),
          respondWith:p=>result=p,waitUntil:()=>{if(failure==='waitUntil')throw new DOMException('expired','InvalidStateError');}});
        const response=await result;
        const bytes=new Uint8Array(await response.arrayBuffer());
        if(response.status!==206||bytes.length!==50||bytes[0]!==7||requestedRange!==null)return false;
      }
      return true;
    }''')
    context.close()
    print('PASS: bilingual speech applies the selected rate to the next segment; failed cache writes cannot break cold range playback',flush=True)


def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}{PREFIX}'
    shots=Path(tempfile.mkdtemp(prefix='fr4000-speed-audio-'))
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            speed_tests(browser,base,shots)
            recovery_tests(browser,base)
            system_and_cache_tests(browser,base)
            browser.close()
    finally:server.shutdown()
    print('Screenshots:',shots)


if __name__=='__main__':main()
