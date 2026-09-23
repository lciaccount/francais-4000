#!/usr/bin/env python3
"""Build only the alphabet/IPA assets; never regenerate the 4000 sentences.

Requires edge-tts, curl and ffmpeg. Run with --check for an offline inventory audit.
Commons metadata and attribution are pinned in phonetics-sources.js after the first
build. --refresh-sources explicitly fetches new metadata. Audio derivatives retain
their source licenses; this does not relicense the rest of the application.
"""
import argparse
import asyncio
import html
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.parse

ROOT = Path(__file__).resolve().parent
VOICES = ['fr-FR-HenriNeural', 'fr-FR-EloiseNeural', 'fr-FR-DeniseNeural']
TRIM = ('silenceremove=start_periods=1:start_duration=0:start_threshold=-50dB,'
        'areverse,silenceremove=start_periods=1:start_duration=0:start_threshold=-50dB,areverse')


def payload(path):
    return json.loads(path.read_text(encoding='utf-8').split(' = ', 1)[1].strip().removesuffix(';'))


def curl(url):
    return subprocess.check_output(['curl', '-fLsS', '--retry', '3', '--max-time', '60', url])


def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value)).strip()


def sources(data, refresh=False):
    path = ROOT / 'phonetics-sources.js'
    if path.exists() and not refresh:
        return payload(path)
    result = {}
    sounds = data['sounds']
    for start in range(0, len(sounds), 8):
        batch = sounds[start:start + 8]
        query = urllib.parse.urlencode(dict(action='query', format='json', prop='imageinfo',
            iiprop='url|extmetadata|sha1', titles='|'.join('File:' + s['file'] for s in batch)))
        pages = json.loads(curl('https://commons.wikimedia.org/w/api.php?' + query))['query']['pages']
        by_title = {p['title']: p for p in pages.values()}
        for sound in batch:
            page = by_title['File:' + sound['file']]
            if not page.get('imageinfo'):
                raise RuntimeError('Missing source: ' + sound['file'])
            info = page['imageinfo'][0]
            meta = info['extmetadata']
            license_name = plain(meta.get('LicenseShortName', {}).get('value', ''))
            if not license_name.startswith(('CC BY', 'CC0', 'Public domain')):
                raise RuntimeError('Review license before distributing: ' + sound['file'] + ' ' + license_name)
            author = plain(meta.get('Artist', {}).get('value', ''))
            if not author:
                # Older IPA recordings predate the machine-readable Artist field.
                # These explicit credits have been checked against their file pages.
                if sound['group'] in ('consonant', 'glide'):
                    author = 'Peter Isotalo (User:Karmosin / User:Peter Isotalo)'
                elif sound['file'] == 'Fr-un-fr BE.ogg':
                    author = 'User:Moyogo'
            if not author:
                raise RuntimeError('Review author before distributing: ' + sound['file'])
            result[sound['id']] = dict(title=page['title'], author=author,
                license=license_name, licenseUrl=meta.get('LicenseUrl', {}).get('value', ''),
                page=info['descriptionurl'], url=info['url'].split('?')[0], sha1=info['sha1'],
                changes='Converted to mono 24 kHz MP3; leading/trailing silence trimmed; no added padding.')
            if sound['id'] == 'e-open':
                # Pin the checked 2005 recording, not the replacement by Terfili.
                result[sound['id']].update(author='Denelson83 (2005 recording)',
                    url='https://upload.wikimedia.org/wikipedia/commons/archive/7/71/20110514201025%21Open-mid_front_unrounded_vowel.ogg',
                    sha1='2072ac51e95391966ef83de9f5c579d774e30df9')
    path.write_text('window.PHONETICS_SOURCES = ' + json.dumps(result, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    return result


def convert(raw, dest):
    subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(raw), '-af', TRIM, '-map_metadata', '-1', '-ar', '24000', '-ac', '1',
        '-b:a', '64k', str(dest)], check=True)


def ready(path):
    return path.exists() and path.stat().st_size > 700


def all_paths(data):
    for sound in data['sounds']:
        yield ROOT / 'audio' / 'phonetics' / 'ipa' / (sound['id'] + '.mp3')
    for slot in range(1, 4):
        for item in data['letters']:
            yield ROOT / 'audio' / f'v{slot}' / 'alphabet' / (item['id'] + '.mp3')
        for item in data['examples'].values():
            yield ROOT / 'audio' / f'v{slot}' / 'phonetics' / (item['id'] + '.mp3')


async def build(data, refresh=False, tts_only=False):
    import edge_tts
    metadata = sources(data, refresh)
    with tempfile.TemporaryDirectory(prefix='fr4000-phonetics-') as temp:
        temp = Path(temp)
        for sound in ([] if tts_only else data['sounds']):
            dest = ROOT / 'audio' / 'phonetics' / 'ipa' / (sound['id'] + '.mp3')
            if ready(dest):
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            raw = temp / (sound['id'] + '.ogg')
            content = curl(metadata[sound['id']]['url'])
            if hashlib.sha1(content).hexdigest() != metadata[sound['id']]['sha1']:
                raise RuntimeError('Source recording changed; review --refresh-sources: ' + sound['file'])
            raw.write_bytes(content)
            convert(raw, dest)
            print('IPA', sound['symbol'], flush=True)
        semaphore = asyncio.Semaphore(4)

        async def generate(slot, kind, key, text):
            dest = ROOT / 'audio' / f'v{slot}' / kind / (key + '.mp3')
            if ready(dest):
                return
            async with semaphore:
                dest.parent.mkdir(parents=True, exist_ok=True)
                raw = temp / f'{slot}-{kind}-{key}.mp3'
                output = temp / f'{slot}-{kind}-{key}-trim.mp3'
                for attempt in range(5):
                    try:
                        await edge_tts.Communicate(text, VOICES[slot - 1], rate='-10%').save(str(raw))
                        convert(raw, output)
                        if not ready(output):
                            raise RuntimeError('Audio too short: ' + str(dest))
                        output.replace(dest)
                        print(slot, kind, key, flush=True)
                        return
                    except Exception:
                        if attempt == 4:
                            raise
                        await asyncio.sleep(1 + attempt * 2)
        jobs = []
        for slot in range(1, 4):
            jobs.extend(generate(slot, 'alphabet', x['id'], x['name']) for x in data['letters'])
            jobs.extend(generate(slot, 'phonetics', x['id'], word) for word, x in data['examples'].items())
        await asyncio.gather(*jobs)
    paths = list(all_paths(data))
    missing = [str(p.relative_to(ROOT)) for p in paths if not ready(p)]
    if missing:
        if tts_only:
            print('TTS ready; reference audio still pending:', len(missing), flush=True)
            return
        raise RuntimeError('Missing audio: ' + ', '.join(missing))
    # The service worker uses this exact list for an explicit full offline download.
    manifest = dict(version=data['version'], assets=['./' + p.relative_to(ROOT).as_posix() for p in paths])
    (ROOT / 'audio' / 'phonetics' / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Ready:', len(paths), 'audio assets', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--refresh-sources', action='store_true')
    parser.add_argument('--tts-only', action='store_true', help='Build neural letters/examples while reference downloads are pending')
    args = parser.parse_args()
    data = payload(ROOT / 'phonetics-data.js')
    assert len(data['letters']) == 26 and len(data['sounds']) == 37
    assert len({x['id'] for x in data['sounds']}) == 37
    if args.check:
        paths = list(all_paths(data))
        missing = [p.relative_to(ROOT).as_posix() for p in paths if not ready(p)]
        print(json.dumps(dict(expected=len(paths), missing=missing), ensure_ascii=False))
        raise SystemExit(bool(missing))
    asyncio.run(build(data, args.refresh_sources, args.tts_only))
