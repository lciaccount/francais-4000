#!/usr/bin/env python3
"""Compact homepage and movable shortcut regression."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            engine = os.environ.get('FR_TEST_ENGINE', 'chromium')
            options = {'headless': True}
            if engine == 'chromium':
                options['args'] = ['--no-sandbox']
            if engine == 'webkit' and os.environ.get('FR_WEBKIT_EXECUTABLE'):
                options['executable_path'] = os.environ['FR_WEBKIT_EXECUTABLE']
            browser = getattr(p, engine).launch(**options)
            desktop = browser.new_context(viewport={'width': 1440, 'height': 900}, service_workers='block')
            page = desktop.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='domcontentloaded')
            page.locator('#sceneOpen').click()
            page.locator('.sceneChoice[data-scene="eiffel"]').click()
            page.locator('.sceneApplyBtn').click()
            page.locator('#sceneClose').click()
            assert page.locator('#advancedControls').get_attribute('open') is None
            assert page.locator('#sceneBanner').bounding_box()['height'] <= 90
            first_y = page.locator('.sentence').first.bounding_box()['y']
            assert first_y < 550, f'desktop first sentence too low: {first_y}'
            page.set_viewport_size({'width': 2048, 'height': 1080})
            assert page.locator('.sentence').first.bounding_box()['y'] < 600
            page.locator('#advancedControls summary').click()
            assert page.locator('#rangeBtn').is_visible()
            page.locator('#advancedControls summary').click()
            shortcut = page.locator('#locatePlayingBtn')
            assert shortcut.is_enabled()
            original = shortcut.bounding_box()
            page.mouse.move(original['x'] + original['width'] / 2, original['y'] + original['height'] / 2)
            page.mouse.down()
            page.mouse.move(original['x'] - 140, original['y'] - 90, steps=7)
            page.mouse.up()
            moved = shortcut.bounding_box()
            assert moved['x'] < original['x'] - 80 and moved['y'] < original['y'] - 40
            assert '当前没有正在播放' not in page.locator('#status').inner_text()
            assert page.evaluate("!!localStorage.getItem('fr4000-locate-position')")
            page.reload(wait_until='domcontentloaded')
            restored = page.locator('#locatePlayingBtn').bounding_box()
            assert abs(restored['x'] - moved['x']) < 3 and abs(restored['y'] - moved['y']) < 3
            desktop.close()

            mobile = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, service_workers='block')
            phone = mobile.new_page()
            phone.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='domcontentloaded')
            phone.wait_for_selector('.sentenceActions [data-swipe-sentence]')
            actions = phone.locator('.sentenceActions').first
            rows = [actions.locator(selector).bounding_box()['y'] for selector in
                    ('.sentencePlayBtn', '.favBtn', '.masterBtn', '.detailsBtn', '[data-swipe-sentence]')]
            assert len({round(y) for y in rows}) == 2, rows
            assert rows[0] == rows[1] == rows[2] and rows[3] == rows[4], rows
            phone.set_viewport_size({'width': 320, 'height': 568})
            actions = phone.locator('.sentenceActions').first
            rows = [actions.locator(selector).bounding_box()['y'] for selector in
                    ('.sentencePlayBtn', '.favBtn', '.masterBtn', '.detailsBtn', '[data-swipe-sentence]')]
            assert len({round(y) for y in rows}) == 2, rows
            assert phone.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
    print('PASS: desktop first-screen density, expanded settings, draggable shortcut persistence, two-row mobile actions')


if __name__ == '__main__':
    main()
