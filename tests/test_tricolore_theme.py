#!/usr/bin/env python3
"""Tricolour theme selection, decoration, layouts and offline shell."""
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
            page.locator('#themeBtn').tap()
            assert page.evaluate('document.documentElement.dataset.theme') == 'dark'
            page.locator('#themeBtn').tap()
            assert page.evaluate('document.documentElement.dataset.theme') == 'tricolore'
            assert page.locator('#themeColorMeta').get_attribute('content') == '#f7f6f2'
            assert page.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--accent").trim()') == '#284660'
            assert page.locator('#themeBtn').inner_text() == '⚜ 三色'
            assert page.evaluate('parseFloat(getComputedStyle(document.querySelector(".topbar"),"::before").width) <= 60')
            assert page.evaluate('getComputedStyle(document.querySelector(".brand h1"),"::after").maskImage.includes("fleur-de-lys.svg")')
            assert page.evaluate('getComputedStyle(document.querySelector(".sentence"),"::after").maskImage === "none"')
            assert page.evaluate('''()=>{const s=getComputedStyle(document.querySelector('.mobileNav .mStop'));return s.backgroundColor==='rgb(40, 70, 96)';}''')
            for width, height in [(320, 568), (390, 844), (844, 390), (1280, 900)]:
                page.set_viewport_size({'width': width, 'height': height})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, height)
            page.set_viewport_size({'width': 390, 'height': 844})
            page.reload(wait_until='networkidle')
            assert page.evaluate('document.documentElement.dataset.theme') == 'tricolore'
            page.locator('[data-study-view="phonetics"]').tap()
            assert page.locator('.phonTile').count() == 26
            assert page.evaluate('getComputedStyle(document.querySelector(".phoneticsHead h2"),"::before").maskImage.includes("fleur-de-lys.svg")')
            page.locator('#swipeEnter').tap()
            assert page.locator('#swipeStudy').is_visible()
            assert page.evaluate('getComputedStyle(document.querySelector(".swipeHeader h2"),"::after").maskImage.includes("fleur-de-lys.svg")')
            assert page.evaluate('getComputedStyle(document.querySelector(".swipeStage"),"::before").maskImage === "none"')
            assert page.evaluate('document.querySelector("#swipeStudy").scrollWidth <= innerWidth')
            page.locator('#swipeExit').tap()
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            assert page.evaluate('''async()=>{const c=await caches.open('fr4000-v18-scene-ipa-loop-20261001');return !!(await c.match('./theme-tricolore.css'))&&!!(await c.match('./fleur-de-lys.svg'));}''')
            page.locator('#themeBtn').tap()
            assert page.evaluate('document.documentElement.dataset.theme') == 'light'
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
    print(f'PASS {engine}: restrained three-colour theme, sparse fleur motifs, persistence, responsive layouts and offline assets')


if __name__ == '__main__':
    main()
