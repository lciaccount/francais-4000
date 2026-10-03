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
    for name in ('eiffel', 'louvre', 'versailles', 'mont-saint-michel'):
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
            assert page.locator('.sceneChoice').count() == 20
            assert page.locator('.sceneChoice[data-scene="soleil"]').count() == 0
            assert page.locator('#sceneOpacityControls').is_visible()
            assert page.locator('#sceneAutoOpacity').is_checked()
            assert page.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--scene-veil").trim()') == '.42'
            page.locator('#sceneAutoOpacity').uncheck()
            page.locator('#sceneVisibility').fill('80')
            assert page.locator('#sceneVisibilityValue').inner_text() == '80%'
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-veil")') == '0.2'
            page.locator('#sceneAutoOpacity').check()
            assert page.evaluate('document.documentElement.style.getPropertyValue("--scene-veil")') == ''
            page.locator('.sceneChoice[data-scene="louvre"]').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'none'
            assert page.locator('.sceneApplyBtn').inner_text() == '选定该背景'
            page.locator('.sceneApplyBtn').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
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
            page.locator('#historyOpen').tap()
            assert page.locator('#sceneChoices').is_hidden()
            assert page.locator('#sceneOpacityControls').is_hidden()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            assert page.locator('.sceneChapter').count() == 16
            assert page.locator('.sceneLine').count() == 183
            assert '瓦卢瓦王朝与百年战争' in page.locator('.sceneChapter').all_inner_texts()[9]
            assert page.locator('.sceneIpa').count() == 183
            assert all(len(text) > 5 for text in page.locator('.sceneIpa').all_inner_texts())
            assert page.locator('.sceneChapter a').count() == 16
            page.locator('.sceneLine [data-word="Mérovingiens"]').first.tap()
            assert '墨洛温王朝' in page.locator('#dictMeanings').inner_text()
            page.locator('#dictClose').tap()
            page.evaluate('window.__sceneSpeech=[]')
            assert page.locator('.sceneHistoryJump option').count() == 17
            page.locator('.sceneHistoryJump select').select_option('16')
            page.wait_for_timeout(500)
            chapter_y = page.locator('.sceneChapter[data-chapter="16"]').bounding_box()['y']
            assert chapter_y < 844, f'chapter y={chapter_y}, sheet scroll={page.locator(".sceneSheet").evaluate("el=>el.scrollTop")}'
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
            assert page.locator('.scenePersonChoice').count() == 17
            assert page.locator('#sceneOpacityControls').is_hidden()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            for person in page.locator('.scenePersonChoice').all():
                person.tap()
                person_id = person.get_attribute('data-person')
                expected = 16 if person_id == 'louis-xiv' else 13 if person_id == 'napoleon' else 12
                assert page.locator('.sceneLine').count() == expected
                assert all(len(text) > 5 for text in page.locator('.sceneIpa').all_inner_texts())
            page.locator('[data-person="louis-xiv"]').tap()
            page.locator('.sceneZoomBtn').tap()
            assert page.locator('#sceneZoomImage').get_attribute('src').endswith('soleil.webp')
            page.locator('#sceneZoomClose').tap()
            page.locator('[data-person="olympe-gouges"]').tap()
            assert page.locator('.sceneLine').count() == 12
            assert page.locator('.sceneIpa').count() == 12
            assert all(len(text) > 5 for text in page.locator('.sceneIpa').all_inner_texts())
            assert '1791' in page.locator('.sceneChinese').nth(1).inner_text()
            page.locator('.sceneLine [data-word="Déclaration"]').first.tap()
            assert page.locator('#dictionary').is_visible()
            page.locator('#dictClose').tap()
            page.locator('[data-person="napoleon"]').tap()
            assert page.locator('.sceneLine').count() == 13
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
            for name in ('eiffel', 'louvre', 'versailles', 'mont-saint-michel'):
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
              const c=await caches.open('fr4000-v24-history-photos-20261002');
              return !!(await c.match('./france-scenes.js'))
                && !!(await c.match('./france-scenes-more.js'))
                && !!(await c.match('./france-scenes-deeper.js'))
                && !!(await c.match('./theme-monochrome.css'))
                && !!(await c.match('./eiffel-mark.svg'))
                && !!(await c.match('./france-history.js'))
                && !!(await c.match('./france-history-expanded.js'))
                && !!(await c.match('./france-people.js'))
                && !!(await c.match('./france-people-expanded.js'))
                && !!(await c.match('./france-photos.js'))
                && !!(await c.match('./france-scenes-ipa.js'))
                && !!(await c.match('./backgrounds/histoire-france.webp'))
                && !!(await c.match('./backgrounds/lyon.webp'))
                && !!(await c.match('./backgrounds/louvre.webp'))
                && !!(await c.match('./backgrounds/photos/eiffel.webp'))
                && !!(await c.match('./backgrounds/photos/louvre.webp'))
                && !!(await c.match('./backgrounds/photos/versailles.webp'))
                && !!(await c.match('./backgrounds/photos/mont-saint-michel.webp'));
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
    print(f'PASS {engine}: 15 illustrated and 4 photographic backgrounds, 183-line history and 17 people, zoom, IPA, playback, lookup, opacity, persistence, offline assets')


if __name__ == '__main__':
    main()
