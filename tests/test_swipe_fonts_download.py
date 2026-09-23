#!/usr/bin/env python3
"""Large-screen font preferences and real service-worker sentence downloads."""
import time
from test_swipe_auto_lock import *


class DownloadHandler(Handler):
    requests = []
    fail = ''
    delay = 0

    def do_GET(self):
        if '/sent/' in self.path:
            type(self).requests.append(self.path)
            time.sleep(type(self).delay)
            if type(self).fail and type(self).fail in self.path:
                self.send_error(503)
                return
        try:
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError):
            pass


def panel(page):
    page.locator('#swipeTools').evaluate('el=>el.open=true')


def download(page, start, end):
    panel(page)
    page.locator('#swipeDownloadStart').fill(str(start))
    page.locator('#swipeDownloadEnd').fill(str(end))
    page.locator('#swipeDownload').click()


def status(page, text):
    page.wait_for_function('text=>document.querySelector("#swipeDownloadStatus").textContent.includes(text)',arg=text,timeout=30000)


def cached(page, start, end):
    return page.evaluate('''async ([start,end]) => {
      const cache=await caches.open('fr4000-v13-fonts-offline-20260924');
      let count=0;
      for(let id=start;id<=end;id++) for(let v=1;v<=3;v++) {
        const r=await cache.match(`./audio/v${v}/sent/${String(id).padStart(4,'0')}.mp3?v=fr4000v3`);
        if(r?.status===200 && (await r.arrayBuffer()).byteLength>0) count++;
      }
      return count;
    }''',[start,end])


def exercise(browser, base, shots):
    context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    context.add_init_script(INIT+MOCK_SPEECH+'Element.prototype.requestFullscreen=undefined;')
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    ready(page,base)
    page.locator('#voiceMode').select_option('system',force=True)
    page.wait_for_function('navigator.serviceWorker.controller!==null')
    enter(page)
    panel(page)
    def sizes():
        return page.evaluate("['.swipeMainText','.swipeTranslation','.swipeIPA'].map(s=>parseFloat(getComputedStyle(document.querySelector(s)).fontSize))")
    before=sizes()
    for key,value in [('fr',150),('zh',125),('ipa',80)]:
        page.locator('#swipeFont-'+key).fill(str(value))
    after=sizes()
    for old,new,ratio in zip(before,after,[1.5,1.25,.8]):
        assert abs(new/old-ratio)<.005,(before,after)
    assert page.locator('#swipeFontValue-fr').inner_text()=='150%'
    calls=page.evaluate('speechCalls.length')
    page.locator('#swipeFont-fr').fill('160')
    assert page.evaluate('speechCalls.length')==calls
    page.evaluate('SwipeStudy.step(1)')
    assert page.locator('#swipeFont-fr').input_value()=='160'
    page.locator('#swipeExit').click()
    page.reload(wait_until='networkidle')
    enter(page)
    panel(page)
    assert page.locator('#swipeFont-fr').input_value()=='160'
    assert page.locator('#swipeFont-zh').input_value()=='125'
    page.locator('#swipeFontReset').click()
    assert all(page.locator('#swipeFont-'+key).input_value()=='100' for key in ['fr','zh','ipa'])
    for kind in ['sentence','letter','sound']:
        page.locator('#swipeKind').select_option(kind)
        panel(page)
        page.locator('#swipeFontReset').click()
        original=sizes()[0]
        page.locator('#swipeFont-'+('ipa' if kind=='sound' else 'fr')).fill('160')
        assert abs(sizes()[0]/original-1.6)<.005,kind
        for key in ['fr','zh','ipa']: page.locator('#swipeFont-'+key).fill('160')
        for width,height in [(320,568),(390,844),(844,390)]:
            page.set_viewport_size({'width':width,'height':height})
            assert page.locator('#swipeStudy').evaluate('el=>el.scrollWidth<=el.clientWidth+1 && el.scrollHeight<=el.clientHeight+1'),(kind,width)
        assert page.locator('#swipeDownloadForm').is_hidden()==(kind!='sentence')
    page.set_viewport_size({'width':390,'height':844})
    page.locator('#swipeKind').select_option('sentence')
    panel(page)
    page.screenshot(path=str(shots/'fonts-download.png'))
    page.locator('#swipeLock').click()
    assert page.locator('#swipeToolsSummary').is_hidden()
    page.locator('#swipeLock').click()
    print('PASS: independent immediate font scaling, reset, persistence, no playback restart, letter/IPA scaling, lock and responsive layout',flush=True)

    download(page,0,2)
    status(page,'请输入')
    assert not DownloadHandler.requests
    settings(page,start=21,end=22)
    panel(page)
    page.locator('#swipeDownloadRange').click()
    assert page.locator('#swipeDownloadStart').input_value()=='21'
    assert page.locator('#swipeDownloadEnd').input_value()=='22'
    page.locator('#swipeDownload').click()
    status(page,'下载完成')
    assert cached(page,21,22)==6
    assert len(DownloadHandler.requests)==6,DownloadHandler.requests
    download(page,21,22)
    status(page,'下载完成')
    assert len(DownloadHandler.requests)==6,'Cached audio was downloaded again'
    print('PASS: invalid ranges rejected, learning-range shortcut, all six real MP3s cached, completed range skips network',flush=True)

    DownloadHandler.fail='/v2/sent/0031.mp3'
    download(page,31,32)
    status(page,'下载失败')
    kept=cached(page,31,32)
    assert kept<6
    DownloadHandler.fail=''
    download(page,31,32)
    status(page,'下载完成')
    assert cached(page,31,32)==6
    DownloadHandler.delay=.6
    download(page,41,48)
    page.wait_for_function('document.querySelector("#swipeDownloadProgress").value>=2')
    page.locator('#swipeDownloadCancel').click()
    status(page,'已取消')
    kept=cached(page,41,48)
    assert 2<=kept<24,kept
    DownloadHandler.delay=0
    download(page,41,48)
    status(page,'下载完成')
    assert cached(page,41,48)==24
    print('PASS: failed downloads report error, cancellation preserves completed files, retries fill missing files',flush=True)

    DownloadHandler.delay=.6
    download(page,71,78)
    page.wait_for_function('document.querySelector("#swipeDownloadProgress").value>=2')
    # An unrelated tab cannot replace the active interval or start duplicate work.
    busy=page.evaluate('''() => new Promise(resolve=>{
      const channel=new MessageChannel();
      channel.port1.onmessage=({data})=>{resolve(data.error);channel.port1.close();};
      navigator.serviceWorker.controller.postMessage({type:'CACHE_SENTENCE_RANGE',start:81,end:81},[channel.port2]);
    })''')
    assert '另一个窗口' in busy
    page.locator('#swipeExit').click()
    enter(page)
    panel(page)
    assert page.locator('#swipeDownload').is_disabled()
    page.reload(wait_until='networkidle')
    enter(page)
    DownloadHandler.delay=0
    download(page,71,78)
    status(page,'下载完成')
    assert cached(page,71,78)==24
    print('PASS: duplicate worker jobs rejected, exit/re-entry retains task, page reload cancels and supports resume',flush=True)

    worker=context.service_workers[0]
    worker.evaluate("() => {self.originalPut=Cache.prototype.put; Cache.prototype.put=function(){return Promise.reject(new DOMException('full','QuotaExceededError'));};}")
    download(page,51,51)
    status(page,'存储空间不足')
    worker.evaluate('() => {Cache.prototype.put=self.originalPut;}')
    assert cached(page,51,51)==0
    download(page,4000,4000)
    status(page,'下载完成')
    assert cached(page,4000,4000)==3
    print('PASS: storage quota failure never reports success, last corpus item downloads all three voices',flush=True)

    page.locator('#swipeExit').click()
    context.set_offline(True)
    page.reload(wait_until='networkidle')
    enter(page)
    page.locator('#swipeVoice').select_option('builtin-cycle')
    page.locator('#swipePause').click()
    page.evaluate('audioEvents=[]')
    settings(page,repeats=3,start=21,end=21)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("本轮已完成")',timeout=30000)
    voices=page.evaluate('audioEvents.map(e=>e.src.match(/audio\\/v(\\d)/)?.[1])')
    assert voices==['1','2','3'],voices
    panel(page)
    download(page,21,22)
    status(page,'下载完成')
    download(page,61,61)
    status(page,'下载失败')
    # Cached byte ranges are what Safari requests for audio.
    result=page.evaluate('''async()=>{const r=await fetch('./audio/v3/sent/0022.mp3?v=fr4000v3',{headers:{Range:'bytes=0-31'}});return [r.status,(await r.arrayBuffer()).byteLength];}''')
    assert result==[206,32],result
    assert not errors,errors
    context.close()
    print('PASS: offline reload and real sentence playback, already-cached range works offline, missing range fails honestly, MP3 range responses',flush=True)


def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(DownloadHandler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    shots=Path(tempfile.mkdtemp(prefix='fr4000-fonts-download-'))
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            exercise(browser,f'http://127.0.0.1:{server.server_port}{PREFIX}',shots)
            browser.close()
    finally:server.shutdown()
    print('Screenshots:',shots)


if __name__=='__main__':main()
