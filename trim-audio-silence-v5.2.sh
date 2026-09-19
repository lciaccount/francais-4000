#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:-$PWD}"
AUDIO="$PROJECT/audio"
TMP="$PROJECT/.audio-trim-v5.2"
OLD="$PROJECT/.audio-trim-v5.2-old"
INDEX="$PROJECT/index.html"
SW="$PROJECT/sw.js"

if [ ! -d "$AUDIO" ]; then
  echo "错误：没有找到 $AUDIO"
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "错误：未安装 ffmpeg。"
  echo "WSL/Ubuntu 可执行：sudo apt-get update && sudo apt-get install -y ffmpeg"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "错误：未找到 python3。"
  exit 1
fi

# 已处理过则直接退出，避免重复有损转码。
if [ -f "$AUDIO/voice-manifest.json" ]; then
  if python3 - "$AUDIO/voice-manifest.json" <<'PY'
import json, sys
try:
    d=json.load(open(sys.argv[1], encoding="utf-8"))
    ok=(d.get("silenceTrim") or {}).get("version")=="v5.2"
except Exception:
    ok=False
raise SystemExit(0 if ok else 1)
PY
  then
    echo "audio/ 已标记为 v5.2 静音裁剪版，无需重复处理。"
    exit 0
  fi
fi

rm -rf "$TMP"
mkdir -p "$TMP"

export PROJECT AUDIO TMP
export TRIM_CONCURRENCY="${TRIM_CONCURRENCY:-4}"

python3 <<'PY'
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

audio = Path(os.environ["AUDIO"]).resolve()
tmp = Path(os.environ["TMP"]).resolve()
workers = max(1, int(os.environ.get("TRIM_CONCURRENCY", "4")))

# 只裁掉文件“最前面/最后面”的静音，不动句子内部的自然停顿。
# 两端保留约 10 ms 保护垫，降低切掉爆破音/擦音起始的风险。
af = (
    "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-50dB,"
    "areverse,"
    "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-50dB,"
    "areverse,"
    "adelay=10:all=1,"
    "apad=pad_dur=0.01"
)

mp3s = sorted(audio.rglob("*.mp3"))
if not mp3s:
    raise SystemExit("没有找到 MP3。")

# 先复制非 MP3 文件。
for src in audio.rglob("*"):
    if not src.is_file() or src.suffix.lower() == ".mp3":
        continue
    rel = src.relative_to(audio)
    dst = tmp / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def one(src: Path):
    rel = src.relative_to(audio)
    dst = tmp / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    part = dst.with_name(dst.stem + ".tmp.mp3")
    cmd = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(src),
        "-af", af,
        "-map_metadata", "-1",
        "-ar", "24000", "-ac", "1", "-b:a", "48k",
        str(part),
    ]
    p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        try: part.unlink()
        except FileNotFoundError: pass
        return rel, False, (p.stderr or "").strip()
    if not part.is_file() or part.stat().st_size < 500:
        try: part.unlink()
        except FileNotFoundError: pass
        return rel, False, "输出文件异常或过小"
    part.replace(dst)
    return rel, True, ""

print(f"准备裁剪 {len(mp3s)} 个 MP3；并发 {workers}")
done = 0
failed = []
with ThreadPoolExecutor(max_workers=workers) as ex:
    futs = [ex.submit(one, p) for p in mp3s]
    for fut in as_completed(futs):
        rel, ok, err = fut.result()
        done += 1
        if not ok:
            failed.append((str(rel), err))
        if done % 100 == 0 or done == len(mp3s):
            print(f"[{done}/{len(mp3s)}] {done/len(mp3s)*100:5.1f}%", flush=True)

if failed:
    fail_path = Path(os.environ["PROJECT"]) / "audio-trim-v5.2-failures.txt"
    fail_path.write_text("\n".join(f"{p}\t{e}" for p,e in failed), encoding="utf-8")
    print(f"\n有 {len(failed)} 个文件处理失败：{fail_path}", file=sys.stderr)
    raise SystemExit(2)

out_count = sum(1 for p in tmp.rglob("*.mp3") if p.is_file() and p.stat().st_size >= 500)
if out_count != len(mp3s):
    raise SystemExit(f"输出数量异常：{out_count}，期望 {len(mp3s)}")

manifest = tmp / "voice-manifest.json"
if manifest.exists():
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    data["silenceTrim"] = {
        "version": "v5.2",
        "edgeThresholdDb": -50,
        "edgeGuardMs": 10,
        "note": "leading/trailing silence trimmed; internal pauses preserved"
    }
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"全部完成：{out_count} 个 MP3")
PY

# 完整处理成功后再一次性切换目录；失败时原 audio/ 不受影响。
rm -rf "$OLD"
mv "$AUDIO" "$OLD"
mv "$TMP" "$AUDIO"
rm -rf "$OLD"

# 修改音频 URL 缓存版本，避免手机继续播放旧缓存 MP3。
if [ -f "$INDEX" ]; then
  python3 - "$INDEX" <<'PY'
import re, sys
p=sys.argv[1]
s=open(p, encoding="utf-8").read()
s=re.sub(r"\?v=(?:neural\d+|fronly\d+|frtrim\d+)", "?v=frtrim6", s)
open(p,"w",encoding="utf-8").write(s)
PY
fi

# 同步升级 Service Worker 缓存名。
if [ -f "$SW" ]; then
  python3 - "$SW" <<'PY'
import re, sys
p=sys.argv[1]
s=open(p, encoding="utf-8").read()
s=re.sub(r"const CACHE='[^']+';", "const CACHE='fr2000-v6-20260919';", s, count=1)
open(p,"w",encoding="utf-8").write(s)
PY
fi

echo
echo "完成：已裁掉每个内置 MP3 两端静音，并保留约 10 ms 保护垫。"
echo "已把 index.html 音频缓存参数升级为 frtrim6，并升级 sw.js 缓存版本。"
echo
echo "建议检查："
echo "  find audio -type f -name '*.mp3' | wc -l"
echo "  grep -n 'frtrim6' index.html | head"
echo "  git status --short | head -40"
