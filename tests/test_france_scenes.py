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
                 'bourgogne', 'normandie', 'pantheon', 'champs-elysees'):
        assert (ROOT / 'backgrounds' / f'{name}.webp').stat().st_size > 10000
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
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='domcontentloaded')
            page.locator('#sceneOpen').tap()
            assert page.locator('#sceneDialog').is_visible()
            assert page.locator('.sceneChoice').count() == 11
            page.locator('[data-scene="louvre"]').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'louvre'
            assert page.locator('.sceneLine').count() == 2
            for name in ('eiffel', 'soleil', 'fleur', 'louvre', 'versailles', 'cote-azur',
                         'bourgogne', 'normandie', 'pantheon', 'champs-elysees'):
                page.locator(f'[data-scene="{name}"]').tap()
                assert page.locator('.sceneLine').count() == 2
            page.locator('[data-scene="louvre"]').tap()
            assert '卢浮宫从前是一座王宫' in page.locator('.sceneChinese').first.inner_text()
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
            page.locator('[data-scene="none"]').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'none'
            page.locator('#sceneClose').tap()
            assert page.locator('#sceneBanner').is_hidden()
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            assert page.evaluate('''async()=>{
              const c=await caches.open('fr4000-v17-france-scenes-20260930');
              return !!(await c.match('./france-scenes.js'))
                && !!(await c.match('./backgrounds/louvre.webp'));
            }''')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {engine}: ten French scenes, bilingual reading, lookup, explanation, persistence, offline assets')


if __name__ == '__main__':
    main()
