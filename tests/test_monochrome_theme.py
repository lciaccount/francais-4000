#!/usr/bin/env python3
"""Two-tone French theme, legible background reading, and offline shell."""
import os
from functools import partial
from http.server import ThreadingHTTPServer
from threading import Thread

from playwright.sync_api import sync_playwright

from test_phonetics import Handler, PREFIX, ROOT


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    engine = os.environ.get('FR_TEST_ENGINE', 'chromium')
    try:
        with sync_playwright() as playwright:
            options = {'headless': True}
            if engine == 'chromium':
                options['args'] = ['--no-sandbox']
            if engine == 'webkit' and os.environ.get('FR_WEBKIT_EXECUTABLE'):
                options['executable_path'] = os.environ['FR_WEBKIT_EXECUTABLE']
            browser = getattr(playwright, engine).launch(**options)
            context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
            context.add_init_script('Element.prototype.requestFullscreen=undefined;speechSynthesis.speak=()=>{};speechSynthesis.cancel=()=>{};')
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}{PREFIX}', wait_until='networkidle')
            assert page.evaluate('document.documentElement.dataset.theme') == 'light'
            assert page.locator('#themeBtn').inner_text() == '☼ 白色'
            assert page.evaluate('getComputedStyle(document.querySelector(".brand h1"),"::before").maskImage.includes("eiffel-mark.svg")')
            assert page.evaluate('getComputedStyle(document.querySelector(".brand h1"),"::after").maskImage.includes("fleur-de-lys.svg")')
            page.locator('#themeBtn').tap()
            assert page.evaluate('document.documentElement.dataset.theme') == 'dark'
            assert page.locator('#themeBtn').inner_text() == '☾ 黑色'
            assert page.locator('#themeColorMeta').get_attribute('content') == '#111111'
            page.locator('#sceneOpen').tap()
            page.locator('[data-scene="eiffel"]').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'none'
            page.locator('.sceneApplyBtn').tap()
            assert page.evaluate('document.documentElement.dataset.scene') == 'eiffel'
            assert page.evaluate('getComputedStyle(document.querySelector(".sceneLine")).backgroundColor') == 'rgb(29, 29, 29)'
            page.locator('#sceneClose').tap()
            assert page.evaluate('getComputedStyle(document.querySelector(".sentence")).backgroundColor') == 'rgb(29, 29, 29)'
            assert page.evaluate('getComputedStyle(document.body).backgroundImage.includes("eiffel.webp")')
            for width, height in [(320, 568), (390, 844), (844, 390), (1280, 900)]:
                page.set_viewport_size({'width': width, 'height': height})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, height)
            page.set_viewport_size({'width': 390, 'height': 844})
            page.reload(wait_until='networkidle')
            assert page.evaluate('document.documentElement.dataset.theme') == 'dark'
            assert page.evaluate('document.documentElement.dataset.scene') == 'eiffel'
            page.locator('#themeBtn').tap()
            assert page.evaluate('document.documentElement.dataset.theme') == 'light'
            assert page.locator('#themeColorMeta').get_attribute('content') == '#f7f7f5'
            page.wait_for_function('getComputedStyle(document.querySelector(".sentence")).backgroundColor === "rgb(255, 255, 255)"')
            page.locator('[data-study-view="phonetics"]').tap()
            assert page.locator('.phonTile').count() == 26
            assert page.evaluate('getComputedStyle(document.querySelector(".phoneticsHead h2"),"::before").maskImage.includes("fleur-de-lys.svg")')
            page.locator('#swipeEnter').tap()
            assert page.locator('#swipeStudy').is_visible()
            assert page.evaluate('getComputedStyle(document.querySelector(".swipeHeader h2"),"::after").maskImage.includes("fleur-de-lys.svg")')
            assert page.evaluate('document.querySelector("#swipeStudy").scrollWidth <= innerWidth')
            page.locator('#swipeExit').tap()
            page.evaluate("localStorage.setItem('fr4000-theme','tricolore')")
            page.reload(wait_until='networkidle')
            assert page.evaluate('document.documentElement.dataset.theme') == 'light'
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            assert page.evaluate('''async()=>{const c=await caches.open('fr4000-v24-history-photos-20261002');return !!(await c.match('./theme-monochrome.css'))&&!!(await c.match('./eiffel-mark.svg'))&&!!(await c.match('./fleur-de-lys.svg'));}''')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {engine}: two French monochrome themes, preview/apply, legible panels, persistence, responsive layout, offline assets')


if __name__ == '__main__':
    main()
