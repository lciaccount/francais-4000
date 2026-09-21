#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:-$PWD}"
VENV="${HOME}/.cache/french4000-edge-tts-venv"
PYGEN="${HOME}/.cache/french4000-neural-generator.py"

if [ ! -f "$PROJECT/index.html" ]; then
  echo "错误：没有找到 $PROJECT/index.html"
  echo "用法：bash build-french-4000-neural.sh /path/to/french-4000-project"
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then echo "错误：需要 python3。"; exit 1; fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "错误：需要 ffmpeg，用于裁掉每段音频首尾静音。"
  echo "Ubuntu/WSL: sudo apt-get update && sudo apt-get install -y ffmpeg"
  exit 1
fi
if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "错误：需要 python3-venv。Ubuntu/WSL 可安装：sudo apt-get install -y python3-venv"
  exit 1
fi
mkdir -p "$(dirname "$VENV")"
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install -q --upgrade pip edge-tts

cat > "$PYGEN" <<'PY'
from __future__ import annotations
import asyncio, json, os, random, re, subprocess, sys, time
from pathlib import Path
import edge_tts

PROJECT=Path(sys.argv[1]).expanduser().resolve()
INDEX=PROJECT/'index.html'
AUDIO=PROJECT/'audio'
VOICES=[
 (1,'fr-FR-HenriNeural','Henri · 法国法语男声'),
 (2,'fr-FR-EloiseNeural','Eloise · 法国法语女声'),
 (3,'fr-FR-DeniseNeural','Denise · 法国法语女声'),
]
SENT_RATE=os.environ.get('FRENCH_SENT_RATE','-4%')
WORD_RATE=os.environ.get('FRENCH_WORD_RATE','-14%')
CONCURRENCY=max(1,int(os.environ.get('TTS_CONCURRENCY','5')))
MAX_RETRIES=max(1,int(os.environ.get('TTS_MAX_RETRIES','8')))
THRESHOLD=os.environ.get('FRENCH_SILENCE_THRESHOLD','-50dB')
MAX_SENT_PAUSE=max(0.10,min(1.0,float(os.environ.get('FRENCH_MAX_SENT_PAUSE','0.30'))))
MIN_BYTES=500

html=INDEX.read_text(encoding='utf-8')
ms=re.search(r'const SENTENCES=(\[.*?\]);\nconst CATEGORIES=',html,re.S)
mw=re.search(r'const BUILTIN_WORD_INDEX=(\{.*?\});',html,re.S)
if not ms or not mw: raise SystemExit('无法读取 index.html 中的语料/词条索引。')
sentences=json.loads(ms.group(1)); word_index=json.loads(mw.group(1))
if len(sentences)!=4000: raise SystemExit(f'句子数异常：{len(sentences)}，应为 4000。')
words=sorted(word_index.items(),key=lambda kv:kv[1])

def valid(p:Path):
 try: return p.is_file() and p.stat().st_size>=MIN_BYTES
 except OSError: return False

async def check_voices():
    voices={x.get('ShortName'):x for x in await edge_tts.list_voices()}
    for _,name,_ in VOICES:
        if name not in voices: raise SystemExit(f'Edge TTS 当前找不到音色：{name}')
        if voices[name].get('Locale')!='fr-FR': raise SystemExit(f'拒绝使用非 fr-FR 音色：{name} / {voices[name].get("Locale")}')
asyncio.run(check_voices())

jobs=[]
for slot,voice,_ in VOICES:
    for s in sentences:
        jobs.append((s['fr'],voice,SENT_RATE,AUDIO/f'v{slot}'/'sent'/f"{int(s['id']):04d}.mp3"))
    for word,idx in words:
        jobs.append((word,voice,WORD_RATE,AUDIO/f'v{slot}'/'word'/f'{int(idx):04d}.mp3'))
for *_,dst in jobs: dst.parent.mkdir(parents=True,exist_ok=True)

# 所有音频都完全裁掉首尾静音；句子还会把过长的句中静音压缩到自然短停顿。
edge_trim=(f'silenceremove=start_periods=1:start_duration=0:start_threshold={THRESHOLD},'
           'areverse,'
           f'silenceremove=start_periods=1:start_duration=0:start_threshold={THRESHOLD},'
           'areverse')
sentence_trim=(f'silenceremove=start_periods=1:start_duration=0:start_threshold={THRESHOLD},'
               f'silenceremove=stop_periods=-1:stop_duration={MAX_SENT_PAUSE:.3f}:'
               f'stop_threshold={THRESHOLD}:stop_silence=0,'
               'areverse,'
               f'silenceremove=start_periods=1:start_duration=0:start_threshold={THRESHOLD},'
               'areverse')

def trim(raw:Path,dst:Path):
    part=dst.with_name(dst.stem+'.trim.tmp.mp3')
    af=sentence_trim if dst.parent.name=='sent' else edge_trim
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',af,
         '-map_metadata','-1','-ar','24000','-ac','1','-b:a','48k',str(part)]
    p=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if p.returncode or not valid(part):
        part.unlink(missing_ok=True)
        raise RuntimeError((p.stderr or 'ffmpeg 输出异常').strip())
    part.replace(dst)

queue=asyncio.Queue()
for j in jobs:
    if not valid(j[3]): queue.put_nowait(j)
TOTAL=len(jobs); already=TOTAL-queue.qsize(); done=already; failed=[]; lock=asyncio.Lock(); start=time.time()
print(f'4000 句 + {len(words)} 个点读词条 × 3 音色 = {TOTAL} 个 MP3')
print(f'音色严格固定为 fr-FR：{", ".join(v for _,v,_ in VOICES)}')
print(f'首尾静音会完全裁掉；句中静音最长保留约 {MAX_SENT_PAUSE*1000:.0f}ms。')
print(f'已有 {already} 个有效文件；需生成 {TOTAL-already} 个。支持断点续跑。')

async def synth(text,voice,rate,dst):
    raw=dst.with_name(dst.stem+'.raw.tmp.mp3')
    for attempt in range(1,MAX_RETRIES+1):
        try:
            raw.unlink(missing_ok=True)
            await edge_tts.Communicate(text=text,voice=voice,rate=rate).save(str(raw))
            if not valid(raw): raise RuntimeError('TTS 输出文件过小')
            await asyncio.to_thread(trim,raw,dst)
            raw.unlink(missing_ok=True)
            return
        except Exception:
            raw.unlink(missing_ok=True)
            if attempt==MAX_RETRIES: raise
            await asyncio.sleep(min(30,1.6**attempt)+random.random())

async def worker():
    global done
    while True:
        try: text,voice,rate,dst=queue.get_nowait()
        except asyncio.QueueEmpty: return
        try:
            await synth(text,voice,rate,dst)
            async with lock:
                done+=1
                if done%25==0 or done==TOTAL:
                    elapsed=max(time.time()-start,1); speed=max(done-already,1)/elapsed; eta=max(TOTAL-done,0)/speed
                    print(f'[{done}/{TOTAL}] {done/TOTAL*100:5.1f}%  预计剩余 {eta/60:5.1f} 分钟',flush=True)
        except Exception as e:
            async with lock:
                failed.append((str(dst),voice,text,repr(e)))
                print(f'失败：{dst} | {voice} | {text!r} | {e}',file=sys.stderr,flush=True)
        finally: queue.task_done()

async def main(): await asyncio.gather(*(worker() for _ in range(CONCURRENCY)))
asyncio.run(main())
if failed:
    log=PROJECT/'audio-build-failures.txt'; log.write_text('\n'.join('\t'.join(x) for x in failed),encoding='utf-8')
    raise SystemExit(f'{len(failed)} 个音频最终失败，记录在 {log}；重新运行即可续跑。')
missing=[str(dst) for *_,dst in jobs if not valid(dst)]
if missing: raise SystemExit(f'仍有 {len(missing)} 个缺失音频，请重新运行。')

manifest={
 'version':'fr4000-v2','locale':'fr-FR','availableSlots':[1,2,3],
 'voices':[{'slot':n,'shortName':v,'label':label} for n,v,label in VOICES],
 'sentenceRate':SENT_RATE,'wordRate':WORD_RATE,'sentenceCount':len(sentences),'wordCount':len(words),
 'silenceTrim':{'version':'fr4000-v2','edgeThresholdDb':THRESHOLD,'edgeGuardMs':0,
                'maxSentencePauseMs':round(MAX_SENT_PAUSE*1000),
                'note':'leading/trailing silence removed; overlong internal sentence pauses shortened'}
}
(AUDIO/'voice-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(PROJECT/'audio-build-failures.txt').unlink(missing_ok=True)
print(f'完成：{TOTAL} 个 MP3；voice-manifest.json 已启用 3 路内置音色。')
PY

exec "$VENV/bin/python" "$PYGEN" "$PROJECT"
