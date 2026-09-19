#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:-$HOME/french-2000-upload}"
VENV="${HOME}/.cache/french2000-edge-tts-venv"
PYGEN="${HOME}/.cache/french2000-neural-v5-generator.py"

if [ ! -f "$PROJECT/index.html" ]; then
  echo "错误：没有找到 $PROJECT/index.html"
  echo "用法：bash build-french-2000-neural-v5.sh ~/french-2000-upload"
  exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "正在安装 python3-venv…"
  sudo apt-get update
  sudo apt-get install -y python3-venv
fi

mkdir -p "$(dirname "$VENV")"
if [ ! -x "$VENV/bin/python" ]; then
  echo "创建专用 Python 环境…"
  python3 -m venv "$VENV"
fi

echo "安装/更新 edge-tts…"
"$VENV/bin/python" -m pip install -q --upgrade pip edge-tts

cat > "$PYGEN" <<'PY'
from __future__ import annotations
import asyncio
import json
import os
import random
import re
import shutil
import sys
import time
import zipfile
from pathlib import Path

try:
    import edge_tts
except Exception as e:
    raise SystemExit(f"无法导入 edge-tts: {e}")

PROJECT = Path(sys.argv[1]).expanduser().resolve()
INDEX = PROJECT / "index.html"
TMP_AUDIO = PROJECT / ".audio-neural-v5-building"
FINAL_AUDIO = PROJECT / "audio"
OUT_ZIP = Path.home() / "french-2000-fr-only-v5.zip"

# v5 全部改成 fr-FR 单语神经音色。
# 不再使用 Vivienne/Remy Multilingual，避免短词或外来词被多语种模型按英语读。
VOICES = [
    (1, "fr-FR-HenriNeural", "Henri · 法国法语男声"),
    (2, "fr-FR-EloiseNeural", "Eloise · 法国法语女声"),
    (3, "fr-FR-DeniseNeural", "Denise · 法国法语女声"),
]
SENT_RATE = os.environ.get("FRENCH_SENT_RATE", "-4%")
WORD_RATE = os.environ.get("FRENCH_WORD_RATE", "-14%")
CONCURRENCY = int(os.environ.get("TTS_CONCURRENCY", "5"))
MAX_RETRIES = int(os.environ.get("TTS_MAX_RETRIES", "8"))
MIN_BYTES = 600
REBUILD_ALL = os.environ.get("FRENCH_REBUILD_ALL", "0") == "1"

html = INDEX.read_text(encoding="utf-8")
ms = re.search(r"const SENTENCES=(\[.*?\]);\nconst CATEGORIES=", html, re.S)
if not ms:
    raise SystemExit("无法从 index.html 读取 SENTENCES 数据。")
sentences = json.loads(ms.group(1))

mw = re.search(r"const BUILTIN_WORD_INDEX=(\{.*?\});", html, re.S)
if not mw:
    raise SystemExit("无法从 index.html 读取 BUILTIN_WORD_INDEX。")
word_index = json.loads(mw.group(1))
words = sorted(word_index.items(), key=lambda kv: kv[1])

print(f"读取到 {len(sentences)} 个句子、{len(words)} 个可点击词条。")
print("v5 将使用 3 个法国法语单语神经音色：")
for _, voice, label in VOICES:
    print(f"  {label}: {voice}")
print(f"句子语速 {SENT_RATE}；单词语速 {WORD_RATE}；并发数 {CONCURRENCY}")

TMP_AUDIO.mkdir(parents=True, exist_ok=True)
for n, _, _ in VOICES:
    (TMP_AUDIO / f"v{n}" / "sent").mkdir(parents=True, exist_ok=True)
    (TMP_AUDIO / f"v{n}" / "word").mkdir(parents=True, exist_ok=True)

def valid_file(p: Path) -> bool:
    try:
        return p.is_file() and p.stat().st_size >= MIN_BYTES
    except OSError:
        return False

# 旧 v4 的 v3 本来就是 DeniseNeural，可安全复用，默认少生成约 1/3 音频。
# 如需强制全部重做：FRENCH_REBUILD_ALL=1 bash build-french-2000-neural-v5.sh ...
if not REBUILD_ALL and FINAL_AUDIO.exists() and "Denise" in html:
    reused = 0
    for src in (FINAL_AUDIO / "v3").rglob("*.mp3") if (FINAL_AUDIO / "v3").exists() else []:
        if not valid_file(src):
            continue
        rel = src.relative_to(FINAL_AUDIO / "v3")
        dst = TMP_AUDIO / "v3" / rel
        if not valid_file(dst):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            reused += 1
    if reused:
        print(f"已复用旧版 Denise 音频 {reused} 个；Henri/Eloise 会重新生成。")

async def validate_voices():
    try:
        available = {v.get("ShortName"): v for v in await edge_tts.list_voices()}
    except Exception as e:
        print(f"提示：暂时无法预先读取在线音色列表，将直接尝试生成：{e}")
        return
    missing = [voice for _, voice, _ in VOICES if voice not in available]
    if missing:
        raise SystemExit("Edge TTS 当前未返回这些音色：" + ", ".join(missing))
    wrong_locale = [voice for _, voice, _ in VOICES if available[voice].get("Locale") != "fr-FR"]
    if wrong_locale:
        raise SystemExit("音色区域校验失败（必须全部为 fr-FR）：" + ", ".join(wrong_locale))

asyncio.run(validate_voices())

jobs = []
for n, voice, _ in VOICES:
    for sent in sentences:
        dst = TMP_AUDIO / f"v{n}" / "sent" / f"{int(sent['id']):04d}.mp3"
        jobs.append((str(sent["fr"]), voice, SENT_RATE, dst))
    for word, idx in words:
        dst = TMP_AUDIO / f"v{n}" / "word" / f"{int(idx):04d}.mp3"
        jobs.append((str(word), voice, WORD_RATE, dst))

TOTAL = len(jobs)
already = sum(valid_file(j[3]) for j in jobs)
print(f"总计 {TOTAL} 个 MP3；已存在且有效 {already} 个；本次需要 {TOTAL-already} 个。")
print("支持断点续跑；中断后重新运行同一脚本即可。\n")

queue: asyncio.Queue = asyncio.Queue()
for j in jobs:
    if not valid_file(j[3]):
        queue.put_nowait(j)

completed = already
failed = []
lock = asyncio.Lock()
start = time.time()

async def synth_one(text: str, voice: str, rate: str, dst: Path):
    part = dst.with_suffix(".mp3.part")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            part.unlink(missing_ok=True)
            comm = edge_tts.Communicate(text=text, voice=voice, rate=rate)
            await comm.save(str(part))
            if not valid_file(part):
                raise RuntimeError(f"生成文件过小 ({part.stat().st_size if part.exists() else 0} bytes)")
            part.replace(dst)
            return
        except Exception:
            part.unlink(missing_ok=True)
            if attempt >= MAX_RETRIES:
                raise
            await asyncio.sleep(min(30, 1.6 ** attempt) + random.random() * 1.5)

async def worker(worker_id: int):
    global completed
    while True:
        try:
            text, voice, rate, dst = queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        try:
            await synth_one(text, voice, rate, dst)
            async with lock:
                completed += 1
                if completed % 25 == 0 or completed == TOTAL:
                    elapsed = max(time.time() - start, 1)
                    newly = max(completed - already, 1)
                    speed = newly / elapsed
                    remain = max(TOTAL - completed, 0)
                    eta = remain / speed if speed else 0
                    print(f"[{completed}/{TOTAL}] {completed/TOTAL*100:5.1f}%  预计剩余 {eta/60:5.1f} 分钟", flush=True)
        except Exception as e:
            async with lock:
                failed.append((str(dst), text, voice, repr(e)))
                print(f"\n失败：{dst.name} | {voice} | {text!r} | {e}", file=sys.stderr, flush=True)
        finally:
            queue.task_done()

async def main():
    workers = [asyncio.create_task(worker(i)) for i in range(max(1, CONCURRENCY))]
    await asyncio.gather(*workers)

asyncio.run(main())

if failed:
    fail_log = PROJECT / "neural-v5-failures.txt"
    fail_log.write_text("\n".join("\t".join(x) for x in failed), encoding="utf-8")
    print(f"\n有 {len(failed)} 个文件最终失败，已写入 {fail_log}")
    print("直接重新运行本脚本即可断点续跑。")
    raise SystemExit(2)

missing = [str(j[3]) for j in jobs if not valid_file(j[3])]
if missing:
    print(f"仍有 {len(missing)} 个缺失/无效文件。请重新运行。")
    raise SystemExit(3)

# 写入可检查的音色清单。
manifest = {
    "version": "fr-only-v5",
    "locale": "fr-FR",
    "availableSlots": [1, 2, 3],
    "voices": [{"slot": n, "shortName": voice, "label": label} for n, voice, label in VOICES],
    "sentenceRate": SENT_RATE,
    "wordRate": WORD_RATE,
    "sentenceCount": len(sentences),
    "wordCount": len(words),
}
(TMP_AUDIO / "voice-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("\n全部法语单语神经音频生成完成。正在替换旧 audio/ …")
if FINAL_AUDIO.exists():
    shutil.rmtree(FINAL_AUDIO)
TMP_AUDIO.rename(FINAL_AUDIO)

try:
    (PROJECT / "neural-v5-failures.txt").unlink(missing_ok=True)
except Exception:
    pass

final_count = sum(1 for p in FINAL_AUDIO.rglob("*.mp3") if valid_file(p))
if final_count != TOTAL:
    raise SystemExit(f"最终音频数量异常：{final_count}，期望 {TOTAL}")
print(f"最终音频数量：{final_count}")

# 兼容从旧 v4 index.html 直接运行脚本的情况：更新音色名称和缓存版本。
html = INDEX.read_text(encoding="utf-8")
html = html.replace("Vivienne · 神经女声", "Henri · 法国法语男声")
html = html.replace("Remy · 神经男声", "Eloise · 法国法语女声")
html = html.replace("Vivienne / Remy / Denise", "Henri / Eloise / Denise")
html = html.replace(">Vivienne</option>", ">Henri</option>")
html = html.replace(">Remy</option>", ">Eloise</option>")
html = re.sub(r"\?v=(?:neural\d+|fronly\d+)", "?v=fronly5", html)
INDEX.write_text(html, encoding="utf-8")

sw = PROJECT / "sw.js"
if sw.exists():
    sw_text = sw.read_text(encoding="utf-8")
    sw_text = re.sub(r"const CACHE='[^']+';", "const CACHE='fr2000-v5-20260919';", sw_text, count=1)
    sw.write_text(sw_text, encoding="utf-8")

print(f"正在打包：{OUT_ZIP}")
if OUT_ZIP.exists():
    OUT_ZIP.unlink()
root_name = "french-2000-main"
with zipfile.ZipFile(OUT_ZIP, "w", allowZip64=True) as z:
    for p in sorted(PROJECT.rglob("*")):
        rel = p.relative_to(PROJECT)
        if any(part == ".git" for part in rel.parts):
            continue
        if any(part.startswith(".audio-neural") for part in rel.parts):
            continue
        if p.is_dir():
            continue
        arc = str(Path(root_name) / rel)
        compress = zipfile.ZIP_STORED if p.suffix.lower() == ".mp3" else zipfile.ZIP_DEFLATED
        z.write(p, arcname=arc, compress_type=compress)

size_mb = OUT_ZIP.stat().st_size / 1024 / 1024
print("\n完成！")
print(f"上传包：{OUT_ZIP}")
print(f"大小：{size_mb:.1f} MB")
print("\n若要更新 GitHub：")
print(f"  cd {PROJECT}")
print('  git add -A')
print('  git commit -m "Fix mobile layout, French-only TTS, and dictionary meanings"')
print('  git push origin main')
PY

echo
exec "$VENV/bin/python" "$PYGEN" "$PROJECT"
