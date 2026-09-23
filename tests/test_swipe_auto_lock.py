#!/usr/bin/env python3
"""Swipe auto-advance/range and gesture-only lock integration tests."""
from test_swipe_study import (
    INIT, ROOT, PREFIX, Handler, ready, enter, card_id, touch,
    ThreadingHTTPServer, Thread, partial, Path, tempfile, sync_playwright,
)

MOCK_SPEECH = '''
window.speechCalls=[];
speechSynthesis.speak=u=>speechCalls.push(u);
speechSynthesis.cancel=()=>{};
'''


def settings(page, repeats=2, start=1, end=2, loop=False, auto=True, ranged=True):
    page.locator('#swipeAutoSettings').evaluate('el=>el.open=true')
    page.locator('#swipeAuto').set_checked(auto)
    page.locator('#swipeRepeats').fill(str(repeats))
    page.locator('#swipeRange').set_checked(ranged)
    if ranged:
        page.locator('#swipeRangeStart').fill(str(start))
        page.locator('#swipeRangeEnd').fill(str(end))
    page.locator('#swipeRangeLoop').set_checked(loop)
    page.locator('#swipeAutoForm button[type=submit]').click()


def finish(page, next_calls=1):
    count = page.evaluate('speechCalls.length')
    page.evaluate('speechCalls.at(-1).onend()')
    if next_calls:
        page.wait_for_function('n=>speechCalls.length>=n', arg=count + next_calls)
    else:
        page.wait_for_timeout(150)


def real_audio(browser, base):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    context.add_init_script(INIT + 'Element.prototype.requestFullscreen=undefined;')
    page = context.new_page()
    ready(page, base)
    enter(page)
    # Apply is an explicit restart; count only its subsequent real playing events.
    page.locator('#swipePause').click()
    page.evaluate('audioEvents=[]')
    settings(page, repeats=2)
    page.locator('#swipeLock').click()
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("本轮已完成")', timeout=25000)
    events = page.evaluate(r'audioEvents.map(e=>e.src.match(/sent\/(\d+)\.mp3/)?.[1]).filter(Boolean)')
    assert events == ['0001', '0001', '0002', '0002'], events
    assert card_id(page) == '2'
    assert page.evaluate('state.mode===null && state.audio===null')
    assert page.locator('#swipeLock').inner_text() == '解锁'
    page.locator('#swipeLock').click()
    page.locator('#swipeExit').click()
    print('PASS: real MP3s play exactly twice per sentence, auto-advance while locked, stop at range end', flush=True)
    page.wait_for_function('navigator.serviceWorker.controller!==null')
    context.set_offline(True)
    page.reload(wait_until='networkidle')
    enter(page)
    page.locator('#swipePause').click()
    settings(page, repeats=1)
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("本轮已完成")', timeout=15000)
    assert card_id(page) == '2'
    assert page.locator('#swipeLock').inner_text() == '锁定'
    assert page.evaluate('audioEvents.some(e=>e.src.includes("/sent/0001.mp3")) && audioEvents.some(e=>e.src.includes("/sent/0002.mp3"))')
    print('PASS: offline reload retains range/repeat preferences and plays cached sentence range automatically', flush=True)
    context.close()


def controlled_tests(browser, base, shots):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    context.add_init_script(MOCK_SPEECH + 'Element.prototype.requestFullscreen=undefined;')
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    ready(page, base)
    page.locator('#voiceMode').select_option('system', force=True)
    page.locator('#gap').select_option('0', force=True)
    enter(page)
    settings(page, repeats=3, start=201, end=202)
    assert card_id(page) == '201' and page.locator('#swipeCounter').inner_text() == '1 / 2'
    assert '201–202' in page.locator('#swipeScopeLabel').inner_text()
    assert page.locator('#swipeAllLabel').is_hidden()
    finish(page)
    assert '第 2/3' in page.locator('#swipePlayState').inner_text()
    page.locator('#swipePause').click()
    page.locator('#swipePause').click()
    assert '第 2/3' in page.locator('#swipePlayState').inner_text()
    finish(page)
    assert card_id(page) == '201'
    finish(page)
    assert card_id(page) == '202'
    page.evaluate('window.staleSpeech=speechCalls.at(-1)')
    page.evaluate('SwipeStudy.step(-1)')
    n = page.evaluate('speechCalls.length')
    page.evaluate('staleSpeech.onend()')
    page.wait_for_timeout(150)
    assert page.evaluate('speechCalls.length') == n and card_id(page) == '201'
    assert '第 1/3' in page.locator('#swipePlayState').inner_text()
    print('PASS: global sentence ID range overrides category, pause preserves completed count, swipe resets count and invalidates old completion', flush=True)

    settings(page, repeats=1, start=201, end=202, loop=True)
    finish(page); assert card_id(page) == '202'
    finish(page); assert card_id(page) == '201'
    settings(page, repeats=1, start=4000, end=4000, loop=True)
    finish(page); assert card_id(page) == '4000'
    assert page.locator('#swipeCounter').inner_text() == '1 / 1'
    settings(page, repeats=1, start=4000, end=4000)
    finish(page, 0)
    assert page.evaluate('state.mode===null')
    page.locator('#swipePause').click()
    assert page.evaluate('state.mode==="swipe"')
    print('PASS: loop wraps only within range, single-sentence range and #4000 boundary, completed item can restart', flush=True)

    for repeats, start, end in [(0, 1, 2), (1.5, 1, 2), (101, 1, 2), (2, 0, 2), (2, 1, 4001), (2, 4, 2)]:
        n = page.evaluate('speechCalls.length')
        settings(page, repeats, start, end)
        assert page.locator('#swipeAutoError').is_visible()
        assert card_id(page) == '4000' and page.evaluate('speechCalls.length') == n
    settings(page, repeats=2, start=1, end=3, auto=False)
    for _ in range(4): finish(page)
    assert card_id(page) == '1'
    settings(page, repeats=1, ranged=False)
    assert page.locator('#swipeCounter').inner_text().endswith('/ 200')
    finish(page); assert card_id(page) == '2'
    print('PASS: invalid settings do not interrupt playback; auto-off keeps infinite loop; no range uses original filtered list', flush=True)

    # One repeat means the entire FR -> ZH -> FR sequence, not one utterance.
    page.evaluate('document.querySelector("#playPattern").value="fr-zh-fr"')
    settings(page, repeats=1, start=1, end=2)
    finish(page); assert card_id(page) == '1'
    assert page.evaluate('speechCalls.at(-1).lang') == 'zh-CN'
    finish(page); assert card_id(page) == '1'
    assert page.evaluate('speechCalls.at(-1).lang') == 'fr-FR'
    finish(page); assert card_id(page) == '2'
    page.evaluate('document.querySelector("#playPattern").value="fr"')

    # Cancelling during the inter-repeat gap must cancel the planned advance too.
    page.evaluate('document.querySelector("#gap").value="1000"')
    settings(page, repeats=1)
    finish(page, 0)
    page.locator('#swipePause').click()
    page.wait_for_timeout(1100)
    assert card_id(page) == '1'
    page.locator('#swipePause').click()
    page.wait_for_function('document.querySelector("#swipeCard").dataset.id==="2"')
    page.evaluate('document.querySelector("#gap").value="0"')
    print('PASS: full bilingual sequence counted once; pause cancels pending auto switch and resumes without extra repeat', flush=True)

    settings(page, repeats=2, start=1, end=3, auto=False)
    page.locator('#swipeDefaultDetails').check()
    page.locator('#swipeHideTranslation').check()
    page.locator('#swipeLock').click()
    assert page.locator('#swipeExit').is_hidden()
    assert page.locator('.swipeSettings').evaluate('el=>el.inert')
    n = page.evaluate('speechCalls.length')
    page.evaluate('''() => {
      for(const id of ['swipePause','swipeExit','swipeFavorite','swipeReveal','swipeDetails']) document.getElementById(id).click();
      SwipeStudy.step(1); SwipeStudy.close();
    }''')
    page.locator('#swipeCard').focus()
    for key in ['Space', 'Escape', 'ArrowDown', 'PageDown']:
        page.keyboard.press(key)
    assert card_id(page) == '1' and page.evaluate('speechCalls.length') == n
    assert page.locator('#swipeStudy').is_visible()
    assert page.locator('#swipeTranslation').is_hidden()
    assert page.locator('#swipeExplanation').is_visible()
    assert not page.evaluate('progress.favorites.has(1)')
    bounds = page.locator('#swipeExplanation').bounding_box()
    touch(page, (70, bounds['y'] + bounds['height'] - 20), (70, bounds['y'] + 20))
    assert card_id(page) == '2'  # Locked: even the explanation is a swipe surface.
    stage = page.locator('#swipeStage').bounding_box()
    touch(page, (60, stage['y'] + 40), (60, stage['y'] + 260))
    assert card_id(page) == '1'
    page.mouse.move(70, stage['y'] + 80)
    page.mouse.wheel(0, 160)
    page.wait_for_function('document.querySelector("#swipeCard").dataset.id==="2"')
    assert page.locator('#swipeLock').inner_text() == '解锁'
    page.screenshot(path=str(shots / 'locked-mobile.png'))
    page.keyboard.press('Tab')
    assert page.locator('#swipeLock').evaluate('el=>el===document.activeElement')
    page.locator('#swipeLock').click()
    assert page.locator('#swipeExit').is_visible()
    page.locator('#swipeReveal').click()
    assert page.locator('#swipeTranslation').is_visible()
    print('PASS: locked buttons/links/shortcuts are blocked, real touch works across details, explicit unlock restores controls', flush=True)

    settings(page, repeats=2, start=201, end=203, loop=True)
    page.locator('#swipeLock').click()
    finish(page); finish(page)
    assert card_id(page) == '202'
    page.locator('#swipeLock').click()
    page.locator('#swipeExit').click()
    page.reload(wait_until='networkidle')
    enter(page)
    assert '每句 2 遍' in page.locator('#swipeAutoSummary').inner_text()
    assert '201–203' in page.locator('#swipeScopeLabel').inner_text()
    assert page.locator('#swipeLock').inner_text() == '锁定'
    page.locator('#swipeKind').select_option('letter')
    assert page.locator('#swipeAutoSettings').is_hidden()
    for _ in range(3): finish(page)
    assert card_id(page) == 'a'
    page.locator('#swipeKind').select_option('sentence')
    page.locator('#swipeAutoSettings').evaluate('el=>el.open=true')
    for width, height in [(320,568), (390,844), (844,390), (1280,900)]:
        page.set_viewport_size({'width':width,'height':height})
        assert page.locator('#swipeStudy').evaluate('el=>el.scrollWidth<=el.clientWidth+1 && el.scrollHeight<=el.clientHeight+1'), (width,height)
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(shots / 'auto-settings-mobile.png'))
    assert not errors, errors
    print('PASS: auto works while locked, preferences persist but lock resets, letters unaffected, expanded settings fit small/landscape screens', flush=True)
    context.close()


def native_fullscreen_lock(browser, base):
    context = browser.new_context()
    context.add_init_script(MOCK_SPEECH)
    page = context.new_page()
    ready(page, base)
    page.locator('#voiceMode').select_option('system', force=True)
    enter(page)
    page.wait_for_function('document.fullscreenElement?.id==="swipeStudy"')
    page.locator('#swipeLock').click()
    page.evaluate('document.exitFullscreen()')
    page.wait_for_function('!document.fullscreenElement')
    assert page.locator('#swipeStudy').is_visible() and page.locator('#swipeLock').inner_text() == '解锁'
    page.locator('#swipeLock').click()
    page.locator('#swipeExit').click()
    assert page.locator('#swipeStudy').is_hidden()
    context.close()
    print('PASS: browser fullscreen exit cannot bypass UI lock; explicit unlock and exit remain available', flush=True)


def main():
    server = ThreadingHTTPServer(('127.0.0.1',0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}{PREFIX}'
    shots = Path(tempfile.mkdtemp(prefix='fr4000-auto-lock-'))
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            real_audio(browser, base)
            controlled_tests(browser, base, shots)
            native_fullscreen_lock(browser, base)
            browser.close()
    finally:
        server.shutdown()
    print('Screenshots:', shots)


if __name__ == '__main__':
    main()
