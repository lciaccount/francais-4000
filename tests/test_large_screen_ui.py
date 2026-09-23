#!/usr/bin/env python3
"""Large-screen naming, simplified controls, first-entry hint and settings strip."""
from test_swipe_auto_lock import (
    MOCK_SPEECH, settings, ROOT, PREFIX, Handler, ready, enter, card_id, touch,
    ThreadingHTTPServer, Thread, partial, Path, tempfile, sync_playwright,
)


def exercise(browser, base, shots, reduced_motion=False):
    context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,
        reduced_motion='reduce' if reduced_motion else 'no-preference')
    context.add_init_script(MOCK_SPEECH+'Element.prototype.requestFullscreen=undefined;')
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    ready(page,base)
    page.locator('#voiceMode').select_option('system',force=True)
    assert '大屏滑动模式' in page.locator('#swipeEnter').inner_text()
    assert '大屏滑动模式' in page.locator('[data-swipe-sentence]').first.inner_text()
    page.evaluate('''() => {
      window.hintEvents=[];
      const el=document.querySelector('#swipeIntro');
      new MutationObserver(()=>hintEvents.push({hidden:el.hidden,time:performance.now()})).observe(el,{attributes:true,attributeFilter:['hidden']});
    }''')
    enter(page)
    assert page.locator('#swipeTitle').inner_text()=='大屏滑动模式'
    assert page.locator('#swipeIntro').is_visible()
    assert page.locator('#swipeIntro').evaluate('el=>getComputedStyle(el).pointerEvents')=='none'
    assert page.locator('.swipeActions button').evaluate_all('els=>els.map(el=>el.id)')==['swipePause','swipeDetails']
    assert page.locator('#swipeSlow,#swipePrev,#swipeNext').count()==0
    assert page.locator('#swipeSpeed option').count()==31
    page.wait_for_timeout(150)
    page.screenshot(path=str(shots/f'intro-{reduced_motion}.png'))
    # A gesture starting on the hint still reaches the underlying swipe surface.
    touch(page,(190,400),(190,210))
    assert card_id(page)=='2'
    page.wait_for_function('document.querySelector("#swipeIntro").hidden',timeout=2500)
    events=page.evaluate('hintEvents')
    assert len(events)==2 and events[0]['hidden'] is False and events[1]['hidden'] is True,events
    duration=events[1]['time']-events[0]['time']
    assert 1400<=duration<=1850,duration
    page.locator('#swipeExit').click()
    enter(page)
    assert page.locator('#swipeIntro').is_hidden()
    page.locator('#swipeExit').click()
    page.reload(wait_until='networkidle')
    enter(page)
    assert page.locator('#swipeIntro').is_hidden()
    print(f'PASS: renamed entries, exactly two footer buttons, 1500ms non-blocking first-entry hint persists across reload (reduced motion={reduced_motion})',flush=True)
    if reduced_motion:
        context.close()
        return

    strip=page.locator('#swipeAutoSummary')
    assert '手动切换' in strip.inner_text() and '当前列表' in strip.inner_text()
    assert page.locator('#swipeAutoForm').is_hidden()
    strip.click()
    assert page.locator('#swipeAutoForm').is_visible()
    strip.focus()
    page.keyboard.press('Space')
    assert page.locator('#swipeAutoForm').is_hidden()
    page.keyboard.press('Enter')
    assert page.locator('#swipeAutoForm').is_visible()
    settings(page,repeats=4,start=12,end=14,loop=True)
    assert page.locator('#swipeAutoForm').is_hidden()
    for text in ['自动切换','每句 4 遍','#12–14','区间循环']:
        assert text in strip.inner_text(),strip.inner_text()
    settings(page,repeats=2,start=21,end=22,loop=False)
    assert '末尾停止' in strip.inner_text() and '每句 2 遍' in strip.inner_text()
    settings(page,auto=False,ranged=False)
    assert '手动切换' in strip.inner_text()
    page.locator('#swipeAll').check()
    assert '全部 4000 句' in strip.inner_text()
    page.locator('#swipeLock').click()
    assert not strip.is_visible()
    page.locator('#swipeLock').click()
    assert strip.is_visible()
    for width,height in [(320,568),(390,844),(844,390),(1280,900)]:
        page.set_viewport_size({'width':width,'height':height})
        for expanded in [False,True]:
            if page.locator('#swipeAutoSettings').evaluate('el=>el.open')!=expanded:
                strip.click()
            assert page.locator('#swipeStudy').evaluate('el=>el.scrollWidth<=el.clientWidth+1 && el.scrollHeight<=el.clientHeight+1'),(width,height,expanded)
            assert strip.evaluate('el=>Math.abs(el.getBoundingClientRect().width-el.parentElement.clientWidth)<2')
    page.set_viewport_size({'width':390,'height':844})
    strip.click()
    page.screenshot(path=str(shots/'collapsed-mobile.png'))
    strip.click()
    page.screenshot(path=str(shots/'expanded-mobile.png'))
    page.locator('#swipeExit').click()
    page.locator('#themeBtn').click()
    enter(page)
    page.screenshot(path=str(shots/'dark-mobile.png'))
    page.locator('#swipeExit').click()
    # Early exit cancels the timer, and should not replay the hint next time.
    page.evaluate('''() => {const p=JSON.parse(localStorage.getItem('fr4000-swipe-v1'));p.introSeen=false;localStorage.setItem('fr4000-swipe-v1',JSON.stringify(p));}''')
    page.reload(wait_until='networkidle')
    enter(page)
    assert page.locator('#swipeIntro').is_visible()
    page.locator('#swipeExit').click()
    assert page.locator('#swipeIntro').is_hidden()
    enter(page)
    assert page.locator('#swipeIntro').is_hidden()
    page.locator('#swipeExit').click()
    page.locator('[data-study-view="phonetics"]').click()
    assert '大屏滑动模式' in page.locator('[data-swipe-phonetics]').inner_text()
    assert not errors,errors
    context.close()
    print('PASS: full-width settings strip summarizes active mode/range/repeats/end behavior, native keyboard disclosure, lock, screen sizes and early hint cleanup',flush=True)


def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}{PREFIX}'
    shots=Path(tempfile.mkdtemp(prefix='fr4000-large-screen-'))
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            exercise(browser,base,shots)
            exercise(browser,base,shots,reduced_motion=True)
            browser.close()
    finally:server.shutdown()
    print('Screenshots:',shots)


if __name__=='__main__':main()
