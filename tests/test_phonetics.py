#!/usr/bin/env python3
"""Real Chromium smoke tests, including playback, mobile UI and offline MP3 ranges.

Install playwright and its Chromium browser, then run this from any directory.
--skip-offline is useful while audio is still being generated. Screenshots are
written to a fresh temporary directory, never into the project.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tempfile
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/francais-4000/'  # Exercise the same non-root URLs as GitHub Pages.
TRACK_AUDIO = '''
window.audioEvents = [];
const NativeAudio = window.Audio;
window.Audio = function(...args) {
  const audio = new NativeAudio(...args);
  audio.addEventListener('playing', () => window.audioEvents.push({src: audio.src, rate: audio.playbackRate}));
  return audio;
};
'''


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith(PREFIX):
            self.send_error(404)
            return
        self.path = '/' + self.path[len(PREFIX):]
        super().do_GET()

    def log_message(self, *_):
        pass


def open_lab(page):
    page.locator('[data-study-view="phonetics"]').click()
    assert page.locator('.phonTile').count() == 26
    page.locator('#voiceMode').select_option('builtin-1', force=True)
    page.locator('#singleRepeat').select_option('1', force=True)
    page.locator('#gap').select_option('0', force=True)


def wait_done(page):
    try:
        page.wait_for_function('state.mode === null', timeout=15000)
    except Exception:
        print('Playback diagnostic:', page.evaluate('''() => ({mode:state.mode, token:state.token,
          status:document.querySelector('#phoneticsPlayState')?.textContent,
          audio:state.audio && {src:state.audio.src,time:state.audio.currentTime,duration:state.audio.duration,
            paused:state.audio.paused,ended:state.audio.ended,ready:state.audio.readyState,network:state.audio.networkState},
          recent:window.audioEvents?.slice(-8)})'''), flush=True)
        raise


def events(page, since=0):
    return page.evaluate('window.audioEvents')[since:]


def exercise_playback(browser, base, shots):
    context = browser.new_context(viewport={'width': 1280, 'height': 1000}, service_workers='block')
    context.add_init_script(TRACK_AUDIO)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base, wait_until='networkidle')
    initial_progress = page.evaluate('[...progress.studied]')
    open_lab(page)
    page.screenshot(path=str(shots / 'desktop-alphabet.png'), full_page=True)
    page.locator('#singleRepeat').select_option('2')
    page.locator('[data-phon-key="letter-a"]').click()
    wait_done(page)
    assert len(events(page)) == 2, events(page)
    assert all('/v1/alphabet/a.mp3' in e['src'] for e in events(page))
    print('PASS: native MP3 playback, finite two-repeat loop', flush=True)

    n = len(events(page))
    page.locator('#voiceMode').select_option('builtin-cycle')
    page.locator('#singleRepeat').select_option('3')
    page.locator('[data-phon-key="letter-u"]').click()
    wait_done(page)
    assert [f'/v{i}/alphabet/u.mp3' in e['src'] for i, e in enumerate(events(page, n), 1)] == [True] * 3
    page.locator('#phoneticsSlow').click()
    page.wait_for_function('state.audio && state.audio.playbackRate === .75')
    wait_done(page)
    assert events(page)[-1]['rate'] == .75
    print('PASS: three-voice cycle, 0.75x slow playback', flush=True)

    page.locator('#voiceMode').select_option('builtin-2')
    page.locator('#singleRepeat').select_option('1')
    page.locator('#phoneticsExample').click()
    wait_done(page)
    assert '/v2/phonetics/tu.mp3' in events(page)[-1]['src']
    page.locator('[data-phon-tab="sounds"]').click()
    assert page.locator('.phonTile').count() == 37
    for group, count in [('oral', 12), ('nasal', 4), ('consonant', 18), ('glide', 3), ('all', 37)]:
        page.locator(f'[data-phon-group="{group}"]').click()
        assert page.locator('.phonTile').count() == count
    page.locator('[data-phon-key="sound-y"]').click()
    wait_done(page)
    assert '/audio/phonetics/ipa/y.mp3' in events(page)[-1]['src']
    print('PASS: 37 IPA entries, four groups, fixed-reference vs selected-example voice', flush=True)

    page.locator('#singleRepeat').select_option('inf')
    page.locator('[data-phon-key="sound-i"]').click()
    page.wait_for_function('state.audio && state.audio.currentTime > 0')
    page.locator('#phoneticsStop').click()
    n = len(events(page))
    page.wait_for_timeout(1400)
    assert len(events(page)) == n
    assert page.evaluate('state.audio === null && state.mode === null')
    page.locator('[data-phon-key="sound-i"]').click()
    page.locator('[data-study-view="sentences"]').click()
    n = len(events(page))
    page.wait_for_timeout(1000)
    assert len(events(page)) == n and page.locator('#sentencePanel').is_visible()
    assert page.evaluate('[...progress.studied]') == initial_progress
    print('PASS: stop cancels scheduled repeats; section switch stops audio; sentence progress unchanged', flush=True)

    page.locator('#singleRepeat').select_option('1')
    page.locator('.sentencePlayBtn').first.click()
    page.wait_for_function('state.audio && state.audio.currentTime > 0')
    wait_done(page)
    assert '/sent/0001.mp3' in events(page)[-1]['src']
    page.locator('.sentence .word').first.click()
    page.wait_for_function('state.mode === "word"')
    page.locator('#dictSlowBtn').click()
    page.wait_for_function('state.mode === "word-preview"')
    page.locator('#dictClose').click()
    assert page.evaluate('state.mode === null && state.audio === null')
    print('PASS: existing sentence playback and dictionary slow/close regression', flush=True)

    page.locator('[data-study-view="phonetics"]').click()
    page.locator('[data-phon-group="nasal"]').click()
    page.locator('#singleRepeat').select_option('1')
    page.locator('#speed').evaluate("el => {el.value='2'; el.dispatchEvent(new Event('input'));}")
    n = len(events(page))
    page.locator('#phoneticsSequence').click()
    wait_done(page)
    assert len(events(page, n)) == 4
    assert [e['src'].rsplit('/', 1)[-1] for e in events(page, n)] == ['in.mp3', 'un.mp3', 'an.mp3', 'on.mp3']
    print('PASS: ordered group playback finishes exactly once', flush=True)

    page.locator('[data-phon-group="oral"]').click()
    page.route('**/audio/phonetics/ipa/e.mp3', lambda route: route.abort())
    page.locator('[data-phon-key="sound-e"]').click()
    page.wait_for_function('document.querySelector("#phoneticsPlayState").textContent.includes("未能播放")')
    assert page.evaluate('state.mode === null')
    page.unroute('**/audio/phonetics/ipa/e.mp3')
    page.locator('[data-phon-key="sound-e"]').click()
    wait_done(page)
    print('PASS: missing IPA audio reports failure (never synthesizes a symbol)', flush=True)

    for width in [320, 390, 768, 1280]:
        page.set_viewport_size({'width': width, 'height': 844})
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), width
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('[data-phon-tab="letters"]').click()
    page.screenshot(path=str(shots / 'mobile-alphabet.png'), full_page=True)
    page.locator('[data-phon-key="letter-g"]').click()
    assert page.locator('#phoneticsDetail').get_attribute('aria-modal') == 'true'
    assert page.locator('#phoneticsClose').evaluate('(el) => el === document.activeElement')
    page.keyboard.press('Shift+Tab')
    assert page.locator('#phoneticsDetail').evaluate('(el) => el.contains(document.activeElement)')
    page.screenshot(path=str(shots / 'mobile-drawer.png'), full_page=True)
    page.keyboard.press('Escape')
    assert not page.locator('#phoneticsDetail').is_visible()
    assert page.locator('[data-phon-key="letter-g"]').evaluate('(el) => el === document.activeElement')
    assert page.evaluate('state.mode === null')
    page.locator('#themeBtn').click()
    page.screenshot(path=str(shots / 'mobile-dark.png'), full_page=True)
    assert not errors, errors
    print('PASS: 320/390/768/1280px layouts, mobile drawer focus/escape, light/dark; no JS errors', flush=True)
    context.close()


def exercise_offline(browser, base):
    context = browser.new_context(viewport={'width': 1280, 'height': 1000})
    context.add_init_script(TRACK_AUDIO)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    # Seed an old app cache and an unrelated cache before the new worker installs.
    page.goto(base + 'README.md')
    page.evaluate('''async () => {
      const old = await caches.open('fr4000-v11-swipe-speed-audio-20260923');
      const path = './audio/v1/sent/0001.mp3?v=fr4000v3';
      await old.put(path, await fetch(path));
      const other = await caches.open('unrelated-app-cache');
      await other.put('./keep-me', new Response('preserve'));
    }''')
    page.goto(base, wait_until='networkidle')
    page.wait_for_function('navigator.serviceWorker.controller !== null', timeout=30000)
    assert page.evaluate('''async () => (await caches.keys()).includes('unrelated-app-cache')''')
    assert page.evaluate('''async () => !!(await (await caches.open('fr4000-v12-large-screen-20260923')).match('./audio/v1/sent/0001.mp3?v=fr4000v3'))''')
    open_lab(page)
    page.locator('#phoneticsDownload').click()
    page.wait_for_function('document.querySelector("#phoneticsOffline").textContent.includes("232 个音频已缓存")', timeout=90000)
    print('PASS: cache upgrade preserves old audio; all 232 lab MP3s cached under a subpath', flush=True)
    context.set_offline(True)
    page.reload(wait_until='networkidle')
    open_lab(page)
    page.locator('[data-phon-key="letter-z"]').click()
    # Short clips can finish before a currentTime poll; retain real playing events.
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/alphabet/z.mp3"))')
    wait_done(page)
    page.locator('[data-phon-tab="sounds"]').click()
    page.locator('[data-phon-key="sound-hw"]').click()
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/ipa/hw.mp3"))')
    wait_done(page)
    page.locator('#phoneticsExample').click()
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/phonetics/huit.mp3"))')
    wait_done(page)
    ranges = page.evaluate('''async () => {
      const src = './audio/phonetics/ipa/y.mp3';
      const results=[];
      for(const range of ['bytes=0-49','bytes=-25','bytes=99999999-']) {
        const response=await fetch(src,{headers:{Range:range}});
        results.push([response.status,(await response.arrayBuffer()).byteLength]);
      }
      return results;
    }''')
    assert ranges == [[206, 50], [206, 25], [416, 0]], ranges
    assert not errors, errors
    print('PASS: offline reload, letter/IPA/example playback, MP3 byte and suffix ranges', flush=True)
    context.close()


def exercise_file(browser):
    page = browser.new_page(viewport={'width': 1280, 'height': 1000})
    page.add_init_script(TRACK_AUDIO)
    page.goto((ROOT / 'index.html').as_uri(), wait_until='networkidle')
    open_lab(page)
    page.locator('[data-phon-key="letter-z"]').click()
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/alphabet/z.mp3"))')
    wait_done(page)
    page.locator('[data-phon-tab="sounds"]').click()
    page.locator('[data-phon-key="sound-hw"]').click()
    page.wait_for_function('audioEvents.some(e=>e.src.includes("/ipa/hw.mp3"))')
    wait_done(page)
    print('PASS: file:// package can select builtin voices and play local letters/IPA', flush=True)
    page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-offline', action='store_true')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}{PREFIX}'
    shots = Path(tempfile.mkdtemp(prefix='fr4000-phonetics-tests-'))
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            exercise_playback(browser, base, shots)
            if not args.skip_offline:
                exercise_offline(browser, base)
                exercise_file(browser)
            browser.close()
    finally:
        server.shutdown()
    print('Screenshots:', shots)


if __name__ == '__main__':
    main()
