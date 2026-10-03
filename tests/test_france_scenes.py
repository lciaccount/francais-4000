#!/usr/bin/env python3
"""French illustrated backgrounds and cultural reading regression."""
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    for name in ('eiffel', 'soleil', 'fleur', 'louvre', 'versailles', 'cote-azur',
                 'bourgogne', 'normandie', 'pantheon', 'champs-elysees',
                 'mont-saint-michel', 'provence', 'chambord', 'strasbourg',
                 'bretagne', 'lyon', 'histoire-france'):
        assert (ROOT / 'backgrounds' / f'{name}.webp').stat().st_size > 10000
    for name in ('eiffel', 'fleur', 'louvre', 'versailles', 'cote-azur',
                 'bourgogne', 'normandie', 'pantheon', 'champs-elysees',
                 'mont-saint-michel', 'provence', 'chambord', 'strasbourg',
                 'bretagne', 'lyon'):
        assert (ROOT / 'backgrounds' / 'photos' / f'{name}.webp').stat().st_size > 10000
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    engine = os.environ.get('FR_TEST_ENGINE', 'chromium')
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if engine == 'chromium':
                options['args'] = ['--no-sandbox']
            if engine == 'webkit' and os.environ.get('FR_WEBKIT_EXECUTABLE'):
                options['executable_path'] = os.environ['FR_WEBKIT_EXECUTABLE']
            browser = getattr(p, engine).launch(**options)
            context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error.stack or error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='domcontentloaded')
            assert not errors, errors
            page.evaluate('''() => {window.__sceneSpeech=[]; window.speakOnce=(text,lang,onend)=>{window.__sceneSpeech.push({text,lang});window.__sceneSpeechDone=onend;};}''')
            page.locator('#sceneOpen').tap()
            assert page.locator('#sceneDialog').is_visible()
            assert '背景选择' in page.locator('#sceneOpen').inner_text()
            assert page.locator('.sceneChoice').count() == 31
            assert page.locator('.sceneChoice[data-scene="soleil"]').count() == 0
            assert page.locator('#sceneOpacityControls').is_visible()
            assert page.locator('#sceneAutoOpacity').is_checked()
            assert page.locator('#homeOpacity').is_visible()
            assert page.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--scene-veil").trim()') == '.34'
            page.locator('#sceneAutoOpacity').uncheck()
            page.locator('#sceneVisibility').fill('80')
            assert page.locator('#sceneVisibilityValue').inner_text() == '80%'
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-veil")') == '0.2'
            assert abs(float(page.evaluate('document.documentElement.style.getPropertyValue("--scene-swipe-veil")')) - .56) < .001
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-surface")') == '89%'
            assert page.locator('#homeOpacity [data-opacity-summary]').inner_text() == '80%'
            page.locator('#sceneAutoOpacity').check()
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-veil")') == ''
            page.locator('.sceneChoice[data-scene="louvre"]').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'none'
            assert page.locator('.sceneApplyBtn').inner_text() == '选定该背景'
            page.locator('.sceneApplyBtn').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            assert 'louvre.webp' in page.evaluate('getComputedStyle(document.body).backgroundImage')
            page.wait_for_timeout(250)  # Card background has a short CSS transition.
            assert page.evaluate('''() => [...document.querySelectorAll('.sentence')].some(el =>
              getComputedStyle(el).backgroundColor.includes('0.94'))''')
            assert page.locator('.sceneLine').count() == 20
            assert page.locator('.sceneHero').bounding_box()['height'] >= 205
            assert page.evaluate('getComputedStyle(document.querySelector(".sceneLine")).backgroundColor') == 'rgb(255, 255, 255)'
            for name in ('eiffel', 'fleur', 'louvre', 'versailles', 'cote-azur',
                         'bourgogne', 'normandie', 'pantheon', 'champs-elysees',
                         'mont-saint-michel', 'provence', 'chambord', 'strasbourg',
                         'bretagne', 'lyon'):
                page.locator(f'.sceneChoice[data-scene="{name}"]').tap()
                assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
                assert page.locator('.sceneLine').count() == 20
                assert page.locator('.sceneIpa').count() == 20
                assert all(text.startswith('/') and text.endswith('/') and len(text) > 5
                           for text in page.locator('.sceneIpa').all_inner_texts())
                page.locator('.sceneZoomBtn').tap()
                assert page.locator('#sceneZoomImage').get_attribute('src').endswith(f'{name}.webp')
                page.locator('#sceneZoomClose').tap()
            page.locator('.sceneChoice[data-scene="louvre"]').tap()
            page.locator('#sceneClose').tap()
            page.locator('#homeOpacity summary').tap()
            page.locator('#homeOpacity [data-opacity-auto]').uncheck()
            page.locator('#homeOpacity [data-opacity-visibility]').fill('70')
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-veil")') == '0.3'
            assert page.locator('#homeOpacity [data-opacity-summary]').inner_text() == '70%'
            page.locator('#swipeEnter').tap()
            assert page.locator('#swipeStudy').is_visible()
            assert page.locator('#swipeOpacity').is_visible()
            assert 'louvre.webp' in page.evaluate('getComputedStyle(document.querySelector("#swipeStudy")).backgroundImage')
            page.locator('#swipeOpacity summary').tap()
            assert page.locator('#swipeOpacity').evaluate('el=>el.open')
            panel = page.locator('#swipeOpacity .sceneOpacityControls').bounding_box()
            assert panel['x'] >= 10 and panel['x'] + panel['width'] <= 390, panel
            assert not page.locator('#swipeOpacity [data-opacity-auto]').is_checked()
            assert page.locator('#swipeOpacity [data-opacity-value]').inner_text() == '70%', page.locator('#swipeOpacity').inner_text()
            page.locator('#swipeOpacity [data-opacity-visibility]').fill('55')
            assert page.locator('#homeOpacity [data-opacity-summary]').inner_text() == '55%'
            page.locator('#swipeLock').tap()
            assert page.locator('#swipeOpacity').is_hidden()
            page.locator('#swipeLock').tap()
            page.locator('#swipeExit').tap()
            page.locator('#homeOpacity [data-opacity-auto]').check()
            page.locator('#historyOpen').tap()
            assert page.locator('.sceneHistoryChoice').count() == 16
            assert page.locator('#sceneOpacityControls').is_hidden()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            assert page.locator('.sceneLine').count() >= 20
            assert '瓦卢瓦王朝与百年战争' in page.locator('.sceneHistoryChoice').all_inner_texts()[9]
            assert page.locator('.sceneIpa').count() == page.locator('.sceneLine').count()
            assert all(len(text) > 5 for text in page.locator('.sceneIpa').all_inner_texts())
            assert page.locator('.sceneSource a').count() >= 1
            page.locator('[data-history="4"]').tap()
            page.locator('.sceneLine [data-word="Mérovingiens"]').first.tap()
            assert '墨洛温王朝' in page.locator('#dictMeanings').inner_text()
            page.locator('#dictClose').tap()
            page.evaluate('window.__sceneSpeech=[]')
            history_total = 0
            for stage in range(1, 17):
                page.locator(f'[data-history="{stage}"]').tap()
                count = page.locator('.sceneLine').count()
                assert count >= 20
                assert page.locator('.sceneIpa').count() == count
                history_total += count
            assert history_total == 343
            assert '第 16 / 16 阶段' in page.locator('.sceneHistoryNote').inner_text()
            assert page.locator('.sceneLine').count() >= 20
            page.locator('.sceneZoomBtn').tap()
            assert page.locator('#sceneZoom').is_visible()
            assert page.locator('#sceneZoomImage').get_attribute('src').endswith('histoire-france.webp')
            page.locator('#sceneZoomIn').tap()
            page.locator('#sceneZoomIn').tap()
            assert page.locator('#sceneZoomScale').inner_text() == '200%'
            assert page.locator('.sceneZoomViewport').evaluate('el=>el.scrollWidth>el.clientWidth')
            page.locator('#sceneZoomReset').tap()
            assert page.locator('#sceneZoomScale').inner_text() == '100%'
            page.keyboard.press('Escape')
            assert page.locator('#sceneZoom').is_hidden()
            page.locator('.sceneZoomBtn').tap()
            page.locator('#sceneZoomClose').tap()
            assert page.locator('#sceneZoom').is_hidden()
            page.locator('#sceneClose').tap()
            page.locator('#peopleOpen').tap()
            assert page.locator('.scenePersonChoice').count() == 32
            assert page.locator('#sceneOpacityControls').is_hidden()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            for person in page.locator('.scenePersonChoice').all():
                person.tap()
                person_id = person.get_attribute('data-person')
                expected = 24 if person_id == 'louis-xiv' else 21 if person_id == 'napoleon' else 20
                assert page.locator('.sceneLine').count() == expected
                assert all(len(text) > 5 for text in page.locator('.sceneIpa').all_inner_texts())
            page.locator('[data-person="louis-xiv"]').tap()
            page.locator('.sceneZoomBtn').tap()
            assert page.locator('#sceneZoomImage').get_attribute('src').endswith('soleil.webp')
            page.locator('#sceneZoomClose').tap()
            page.locator('[data-person="olympe-gouges"]').tap()
            assert page.locator('.sceneLine').count() == 20
            assert page.locator('.sceneIpa').count() == 20
            assert all(len(text) > 5 for text in page.locator('.sceneIpa').all_inner_texts())
            assert '1791' in page.locator('.sceneChinese').nth(1).inner_text()
            page.locator('.sceneLine [data-word="Déclaration"]').first.tap()
            assert page.locator('#dictionary').is_visible()
            page.locator('#dictClose').tap()
            page.locator('[data-person="napoleon"]').tap()
            assert page.locator('.sceneLine').count() == 21
            page.locator('.sceneLine').first.locator('[data-action="play-fr"]').tap()
            assert page.locator('.sceneLine').first.locator('[data-action="play-fr"]').get_attribute('aria-pressed') == 'true'
            page.locator('.sceneLine').first.locator('[data-action="play-fr"]').tap()
            page.locator('.sceneZoomBtn').tap()
            assert page.locator('#sceneZoomImage').get_attribute('src').endswith('histoire-france.webp')
            page.locator('#sceneZoomClose').tap()
            page.locator('#sceneClose').tap()
            page.locator('#sceneOpen').tap()
            page.evaluate('window.__sceneSpeech=[]')
            assert '卢浮宫从前是一座王宫' in page.locator('.sceneChinese').first.inner_text()
            assert page.locator('.sceneSource a').count() == 2
            page.locator('.sceneLine').first.locator('[data-action="play-fr"]').tap()
            assert page.locator('.sceneLine').first.locator('[data-action="play-fr"]').get_attribute('aria-pressed') == 'true'
            assert '循环朗读中' in page.locator('#status').inner_text()
            page.evaluate('window.__sceneSpeechDone()')
            page.wait_for_function('window.__sceneSpeech.length >= 2')
            assert page.evaluate('window.__sceneSpeech[0].text === window.__sceneSpeech[1].text')
            page.locator('.sceneLine').first.locator('[data-action="play-fr"]').tap()
            assert page.locator('.sceneLine').first.locator('[data-action="play-fr"]').get_attribute('aria-pressed') == 'false'
            page.locator('[data-action="play-all"]').tap()
            assert page.locator('[data-action="play-all"]').get_attribute('aria-pressed') == 'true'
            page.locator('[data-action="stop"]').tap()
            assert page.locator('[data-action="play-all"]').get_attribute('aria-pressed') == 'false'
            page.locator('.sceneLine').first.locator('[data-action="explain"]').tap()
            assert page.locator('.sceneExplanation').first.is_visible()
            page.locator('.sceneLine').first.locator('[data-word="Louvre"]').tap()
            assert page.locator('#dictionary').is_visible()
            assert '卢浮宫从前' in page.locator('#dictContext').inner_text()
            assert page.locator('#dictLoopBtn').is_visible()
            page.locator('#dictClose').tap()
            page.locator('#sceneClose').tap()
            assert page.locator('#sceneDialog').is_hidden()
            assert page.locator('#sceneBanner').is_visible()
            page.reload(wait_until='domcontentloaded')
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            page.locator('#sceneOpen').tap()
            for name in ('eiffel', 'fleur', 'louvre', 'versailles', 'cote-azur',
                         'bourgogne', 'normandie', 'pantheon', 'champs-elysees',
                         'mont-saint-michel', 'provence', 'chambord', 'strasbourg',
                         'bretagne', 'lyon'):
                page.locator(f'.sceneChoice[data-scene="photo-{name}"]').tap()
                assert page.locator('.sceneLine').count() == 20
                assert '实拍摄影' in page.locator('.sceneSource').inner_text()
                assert page.locator('.sceneSource a').count() >= 3
                page.locator('.sceneZoomBtn').tap()
                assert page.locator('#sceneZoomImage').get_attribute('src').endswith(f'photos/{name}.webp')
                page.locator('#sceneZoomClose').tap()
            page.locator('.sceneChoice[data-scene="photo-louvre"]').tap()
            page.locator('.sceneApplyBtn').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'photo-louvre'
            page.locator('#sceneAutoOpacity').uncheck()
            page.locator('#sceneVisibility').fill('75')
            page.reload(wait_until='domcontentloaded')
            assert page.evaluate('document.documentElement.dataset.scene') == 'photo-louvre'
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-veil")') == '0.25'
            assert page.locator('#homeOpacity [data-opacity-summary]').inner_text() == '75%'
            page.locator('#sceneOpen').tap()
            assert not page.locator('#sceneAutoOpacity').is_checked()
            assert page.locator('#sceneVisibilityValue').inner_text() == '75%'
            page.locator('#sceneAutoOpacity').check()
            page.locator('.sceneChoice[data-scene="none"]').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'none'
            page.locator('#sceneClose').tap()
            assert page.locator('#sceneBanner').is_hidden()
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            assert page.evaluate('''async()=>{
              const c=await caches.open('fr4000-v25-history32-photos15-20261003');
              return !!(await c.match('./france-scenes.js'))
                && !!(await c.match('./france-scenes-more.js'))
                && !!(await c.match('./france-scenes-deeper.js'))
                && !!(await c.match('./theme-monochrome.css'))
                && !!(await c.match('./eiffel-mark.svg'))
                && !!(await c.match('./france-history.js'))
                && !!(await c.match('./france-history-expanded.js'))
                && !!(await c.match('./france-history-deep.js'))
                && !!(await c.match('./france-people.js'))
                && !!(await c.match('./france-people-expanded.js'))
                && !!(await c.match('./france-people-additional.js'))
                && !!(await c.match('./france-people-deep.js'))
                && !!(await c.match('./france-photos.js'))
                && !!(await c.match('./france-scenes-ipa.js'))
                && !!(await c.match('./backgrounds/histoire-france.webp'))
                && !!(await c.match('./backgrounds/lyon.webp'))
                && !!(await c.match('./backgrounds/louvre.webp'))
                && !!(await c.match('./backgrounds/photos/eiffel.webp'))
                && !!(await c.match('./backgrounds/photos/louvre.webp'))
                && !!(await c.match('./backgrounds/photos/versailles.webp'))
                && !!(await c.match('./backgrounds/photos/mont-saint-michel.webp'))
                && !!(await c.match('./backgrounds/photos/fleur.webp'))
                && !!(await c.match('./backgrounds/photos/lyon.webp'));
            }''')
            desktop = browser.new_context(viewport={'width': 1365, 'height': 900})
            desk = desktop.new_page()
            desk.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='domcontentloaded')
            desk.locator('#sceneOpen').click()
            desk.locator('.sceneChoice[data-scene="chambord"]').click()
            assert desk.evaluate('document.documentElement.dataset.scene') == 'none'
            desk.locator('.sceneApplyBtn').click()
            art = desk.locator('.sceneArtwork').bounding_box()
            reading = desk.locator('.sceneReading').bounding_box()
            assert art['x'] + art['width'] < reading['x']
            assert desk.locator('.sceneHero').bounding_box()['height'] >= 300
            desk.locator('.sceneSheet').evaluate('(el) => {el.scrollTop = 600}')
            assert desk.locator('.sceneArtwork').bounding_box()['y'] >= 0
            assert desk.locator('.sceneFooter').bounding_box()['y'] >= 0
            assert not errors, errors
            desktop.close()
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {engine}: 15 illustrated and 15 photographic backgrounds, 16 deep history stages and 32 people, zoom, IPA, playback, lookup, opacity, persistence, offline assets')


if __name__ == '__main__':
    main()
