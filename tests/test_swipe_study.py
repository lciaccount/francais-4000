#!/usr/bin/env python3
"""Chromium integration tests for the immersive swipe study mode.

Uses real MP3 playback, real mobile touch input, independent browser storage and
the GitHub Pages subpath. No app/user data or audio files are modified.
"""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
from threading import Thread

from playwright.sync_api import sync_playwright
from test_phonetics import Handler, ROOT, PREFIX

INIT = '''
window.audioEvents=[];
const NativeAudio=window.Audio;
window.Audio=function(...args){
  const audio=new NativeAudio(...args);
  audio.addEventListener('playing',()=>audioEvents.push({src:audio.src,rate:audio.playbackRate}));
  return audio;
};
'''


def ready(page, base):
    page.goto(base, wait_until='networkidle')
    page.locator('#voiceMode').select_option('builtin-1', force=True)
    page.locator('#singleRepeat').select_option('1', force=True)
    page.locator('#gap').select_option('50', force=True)


def enter(page):
    page.locator('#swipeEnter').click()
    page.wait_for_function('state.mode === "swipe"')


def card_id(page):
    return page.locator('#swipeCard').get_attribute('data-id')


def touch(page, start, end):
    cdp = page.context.new_cdp_session(page)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': start[0], 'y': start[1]}]})
    for i in range(1, 8):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{
            'x': start[0] + (end[0] - start[0]) * i / 7,
            'y': start[1] + (end[1] - start[1]) * i / 7}]})
        page.wait_for_timeout(25)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    cdp.detach()
    page.wait_for_timeout(250)


def mobile_tests(browser, base, shots):
    # Route-controlled failures/late responses must not bypass interception via SW.
    context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, service_workers='block')
    context.add_init_script(INIT + 'Element.prototype.requestFullscreen=undefined;')
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    ready(page, base)
    enter(page)
    assert page.locator('#swipeCounter').inner_text() == '1 / 200'
    assert page.locator('.app').evaluate('el=>el.inert')
    assert page.locator('#swipeStudy').evaluate('el=>Math.abs(el.getBoundingClientRect().height-innerHeight)<2')
    page.wait_for_function('audioEvents.filter(e=>e.src.includes("/sent/0001.mp3")).length >= 2', timeout=16000)
    assert page.evaluate('state.mode === "swipe"')
    assert page.locator('#singleRepeat').input_value() == '1'
    page.screenshot(path=str(shots / 'swipe-sentence-mobile.png'))
    print('PASS: fullscreen viewport + infinite current-sentence loop regardless of single-repeat setting', flush=True)

    touch(page, (190, 500), (190, 250))
    assert card_id(page) == '2', card_id(page)
    touch(page, (190, 250), (190, 500))
    assert card_id(page) == '1'
    touch(page, (100, 420), (290, 425))
    assert card_id(page) == '1'
    touch(page, (190, 420), (190, 400))
    assert card_id(page) == '1'
    print('PASS: native upward/downward touch navigation; horizontal/short gestures ignored', flush=True)

    page.locator('#swipeDefaultDetails').check()
    assert page.locator('#swipeExplanation').is_visible()
    bounds = page.locator('#swipeExplanation').bounding_box()
    start = (180, bounds['y'] + bounds['height'] - 35)
    end = (180, bounds['y'] + 35)
    touch(page, start, end)
    assert card_id(page) == '1'
    assert page.locator('#swipeExplanation').evaluate('el=>el.scrollTop>0')
    page.locator('#swipeExplanation').evaluate('el=>{el.scrollTop=el.scrollHeight;}')
    touch(page, start, end)
    assert card_id(page) == '2'
    assert page.locator('#swipeExplanation').is_visible()
    page.locator('#swipeDetails').click()
    assert page.locator('#swipeExplanation').is_hidden()
    page.evaluate('SwipeStudy.step(1)')
    assert page.locator('#swipeExplanation').is_visible()
    print('PASS: detail scrolling does not skip cards; a new boundary gesture changes card; default detail applied on each card', flush=True)

    page.locator('#swipeHideTranslation').check()
    assert page.locator('#swipeTranslation').is_hidden()
    page.locator('#swipeReveal').click()
    assert page.locator('#swipeTranslation').is_visible()
    page.evaluate('SwipeStudy.step(1)')
    assert page.locator('#swipeTranslation').is_hidden()
    current = int(card_id(page))
    page.locator('#swipeFavorite').click()
    page.locator('#swipeMastered').click()
    assert page.evaluate(f'progress.favorites.has({current}) && progress.mastered.has({current})')
    page.locator('#swipePause').click()
    assert page.evaluate('state.mode === null && state.audio === null')
    n = page.evaluate('audioEvents.length')
    page.wait_for_timeout(1000)
    assert page.evaluate('audioEvents.length') == n
    page.locator('#swipeSpeed').select_option('0.75')
    page.locator('#swipePause').click()
    page.wait_for_function('state.audio && state.audio.playbackRate === .75')
    print('PASS: recall/reveal, favorite/mastered persistence, pause cancellation and slow looping', flush=True)

    page.locator('#swipeKind').select_option('letter')
    assert page.locator('#swipeCounter').inner_text().endswith('/ 26')
    page.locator('#swipeDefaultDetails').uncheck()
    page.locator('#swipeSpeed').select_option('1.00')
    page.wait_for_function('audioEvents.filter(e=>e.src.includes("/alphabet/a.mp3")).length >= 3', timeout=10000)
    assert page.evaluate('state.mode === "swipe"')
    # Delay an old letter request, switch to the next one, then release the old response.
    held = []
    page.route('**/v1/alphabet/b.mp3', lambda route: held.append(route))
    page.evaluate('SwipeStudy.step(1)')
    page.wait_for_timeout(150)
    assert held, 'Previous audio request was not intercepted'
    page.evaluate('SwipeStudy.step(1)')
    assert card_id(page) == 'c'
    for route in held:
        route.continue_()
    page.wait_for_function('state.audio && state.audio.src.includes("/alphabet/c.mp3") && state.audio.currentTime > 0')
    assert not page.evaluate('audioEvents.some(e=>e.src.includes("/alphabet/b.mp3"))')
    page.unroute('**/v1/alphabet/b.mp3')
    print('PASS: letters loop; a late previous audio request cannot resume or overlap', flush=True)

    page.locator('#swipeVoice').select_option('builtin-cycle')
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/v3/alphabet/c.mp3"))', timeout=10000)
    page.locator('#swipeKind').select_option('sound')
    assert page.locator('#swipeCounter').inner_text().endswith('/ 37')
    page.wait_for_function('audioEvents.filter(e=>e.src.includes("/ipa/i.mp3")).length >= 2', timeout=10000)
    page.locator('#swipeExample').click()
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/phonetics/si.mp3"))', timeout=10000)
    page.wait_for_function('state.mode === "swipe" && state.audio && state.audio.src.includes("/ipa/i.mp3")')
    page.screenshot(path=str(shots / 'swipe-ipa-mobile.png'))
    print('PASS: three-voice cycle, fixed IPA reference loop, example preview then resume current sound', flush=True)

    page.route('**/ipa/y.mp3', lambda route: route.abort())
    page.evaluate('SwipeStudy.step(1)')
    page.wait_for_function('document.querySelector("#swipePlayState").textContent.includes("未能播放")')
    assert page.evaluate('state.mode === null')
    page.unroute('**/ipa/y.mp3')
    page.locator('#swipePause').click()
    page.wait_for_function('state.audio && state.audio.currentTime > 0')
    page.locator('#swipeDefaultDetails').check()
    page.locator('#swipeExit').click()
    assert page.locator('#swipeStudy').is_hidden()
    assert not page.locator('.app').evaluate('el=>el.inert')
    assert page.evaluate('state.audio === null && state.mode === null')
    page.reload(wait_until='networkidle')
    enter(page)
    assert page.locator('#swipeDefaultDetails').is_checked()
    assert page.locator('#swipeHideTranslation').is_checked()
    assert page.locator('#swipeExplanation').is_visible()
    page.locator('#swipeExit').click()
    print('PASS: audio errors pause with retry feedback, exit cleanup, preferences survive reload', flush=True)
    assert not errors, errors
    context.close()


def desktop_tests(browser, base, shots):
    context = browser.new_context(viewport={'width': 1280, 'height': 900})
    context.add_init_script(INIT + 'Element.prototype.requestFullscreen=()=>Promise.reject(new Error("blocked"));')
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    ready(page, base)
    page.locator('[data-swipe-sentence="3"]').click()
    assert card_id(page) == '3'
    page.keyboard.press('ArrowDown')
    assert card_id(page) == '4'
    page.keyboard.press('ArrowUp')
    assert card_id(page) == '3'
    page.keyboard.press('Space')
    assert page.evaluate('state.mode === null')
    page.keyboard.press('Space')
    assert page.evaluate('state.mode === "swipe"')
    page.mouse.move(450, 440)
    page.mouse.wheel(0, 160)
    page.wait_for_timeout(70)
    page.mouse.wheel(0, 400)
    page.wait_for_timeout(100)
    assert card_id(page) == '4'  # Inertia must not skip multiple entries.
    page.wait_for_timeout(300)
    page.mouse.wheel(0, -150)
    page.wait_for_timeout(100)
    assert card_id(page) == '3'
    page.screenshot(path=str(shots / 'swipe-desktop.png'))
    for _ in range(24):
        page.keyboard.press('Tab')
        assert page.locator('#swipeStudy').evaluate('el=>el.contains(document.activeElement)')
    page.keyboard.press('Escape')
    assert page.locator('#swipeStudy').is_hidden()
    print('PASS: context entry, keyboard/space/Escape, wheel inertia guard, focus trap, fullscreen-denied fallback', flush=True)

    page.locator('#searchInput').fill('4000')
    page.wait_for_function('document.querySelectorAll(".sentence").length === 1')
    enter(page)
    assert card_id(page) == '4000'
    assert page.locator('#swipeCounter').inner_text() == '1 / 1'
    page.evaluate('SwipeStudy.step(1); SwipeStudy.step(-1)')
    assert card_id(page) == '4000'  # Both directions stay inside a one-item list.
    page.locator('#swipeAll').check()
    assert page.locator('#swipeCounter').inner_text() == '4000 / 4000'
    page.locator('#swipeExit').click()
    page.locator('#searchInput').fill('definitely-no-sentence-xxx')
    page.wait_for_function('document.querySelectorAll(".sentence").length === 0')
    page.locator('#swipeEnter').click()
    assert page.locator('#swipeCounter').inner_text() == '0 / 0'
    assert page.locator('#swipePause').is_disabled()
    page.locator('#swipeAll').check()
    assert page.locator('#swipeCounter').inner_text().endswith('/ 4000')
    page.locator('#swipeExit').click()
    print('PASS: search/filter scope, first/last/empty lists, all-4000 switch', flush=True)

    page.locator('[data-study-view="phonetics"]').click()
    page.locator('[data-phon-tab="sounds"]').click()
    page.locator('[data-phon-group="nasal"]').click()
    page.locator('[data-phon-key="sound-on"]').click()
    page.locator('[data-swipe-phonetics]').click()
    assert card_id(page) == 'on'
    assert page.locator('#swipeCounter').inner_text() == '4 / 4'
    page.evaluate('SwipeStudy.step(-1)')
    assert card_id(page) == 'an'
    for width, height in [(320, 568), (390, 844), (844, 390), (1280, 900)]:
        page.set_viewport_size({'width': width, 'height': height})
        page.locator('#swipeDefaultDetails').check()
        assert page.locator('#swipeStudy').evaluate('el=>el.scrollWidth<=el.clientWidth+1 && el.scrollHeight<=el.clientHeight+1'), (width, height)
    page.locator('#swipeExit').click()
    page.locator('#themeBtn').click()
    page.locator('#swipeEnter').click()
    page.screenshot(path=str(shots / 'swipe-dark.png'))
    page.locator('#swipeExit').click()
    print('PASS: current IPA subgroup/selected sound, phone/landscape/desktop sizes, dark theme', flush=True)
    assert not errors, errors
    context.close()


def fullscreen_offline_tests(browser, base):
    context = browser.new_context(viewport={'width': 1024, 'height': 800})
    context.add_init_script(INIT)
    page = context.new_page()
    ready(page, base)
    assert page.evaluate('''async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      let ended = 0;
      const audio = {duration:1,currentTime:.99,paused:false,pause(){this.paused=true;}};
      onAudioFinished(audio, () => ended++);
      audio.ontimeupdate(); await sleep(350);
      if(ended !== 0) return false; // Never cut even the final 10 ms.
      audio.currentTime=1; await sleep(650); // Also recover without timeupdate.
      if(ended !== 1 || !audio.paused || audioEndCleanups.has(audio)) return false;
      audio.paused=false;
      onAudioFinished(audio, () => ended++);
      audio.ontimeupdate(); audioEndCleanups.get(audio)(); await sleep(350);
      if(ended !== 1) return false; // Stop/skip cancels pending EOF recovery.
      onAudioFinished(audio, () => ended++);
      audio.ontimeupdate(); audio.onended(); await sleep(350);
      return ended === 2 && !audioEndCleanups.has(audio);
    }''')
    print('PASS: missing-ended recovery waits for the exact EOF; stop and native end cancel fallback without duplicate callbacks', flush=True)
    enter(page)
    page.wait_for_function('document.fullscreenElement?.id === "swipeStudy"')
    page.evaluate('document.exitFullscreen()')
    page.wait_for_function('document.querySelector("#swipeStudy").hidden')
    assert page.evaluate('state.mode === null')
    # Avoid requesting native fullscreen in the remaining independent cases.
    page.evaluate('Element.prototype.requestFullscreen = undefined')
    page.locator('[data-study-view="phonetics"]').click()
    page.wait_for_function('navigator.serviceWorker.controller !== null')
    page.locator('#phoneticsDownload').click()
    page.wait_for_function('document.querySelector("#phoneticsOffline").textContent.includes("232 个音频已缓存")', timeout=90000)
    context.set_offline(True)
    page.reload(wait_until='networkidle')
    page.evaluate('Element.prototype.requestFullscreen = undefined')
    enter(page)
    page.locator('#swipeKind').select_option('letter')
    page.wait_for_function('audioEvents.filter(e=>e.src.includes("/alphabet/a.mp3")).length>=2', timeout=10000)
    page.locator('#swipeKind').select_option('sound')
    page.wait_for_function('audioEvents.filter(e=>e.src.includes("/ipa/i.mp3")).length>=2', timeout=10000)
    # A synthetic visibility notification with a hidden document tests safe pause.
    page.evaluate('''() => {Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));}''')
    assert page.evaluate('state.mode === null')
    assert '后台' in page.locator('#swipePlayState').inner_text()
    page.evaluate('''() => {Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'));}''')
    assert page.evaluate('state.mode === null')
    page.locator('#swipePause').click()
    assert page.evaluate('state.mode === "swipe"')
    page.locator('#swipeExit').click()
    print('PASS: native fullscreen enter/exit, cached offline reload + letter/IPA loops, background pause/manual resume', flush=True)
    context.close()


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}{PREFIX}'
    shots = Path(tempfile.mkdtemp(prefix='fr4000-swipe-tests-'))
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            try:
                mobile_tests(browser, base, shots)
                desktop_tests(browser, base, shots)
                fullscreen_offline_tests(browser, base)
            except Exception:
                for context in browser.contexts:
                    for page in context.pages:
                        print('Playback diagnostic:', page.evaluate('''() => ({mode:state.mode,
                          status:document.querySelector('#swipePlayState')?.textContent,
                          audio:state.audio && {src:state.audio.src,time:state.audio.currentTime,duration:state.audio.duration,
                            paused:state.audio.paused,ended:state.audio.ended,ready:state.audio.readyState},
                          recent:window.audioEvents?.slice(-8)})'''), flush=True)
                raise
            browser.close()
    finally:
        server.shutdown()
    print('Screenshots:', shots)


if __name__ == '__main__':
    main()
