#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:-$PWD}"
INDEX="$PROJECT/index.html"
SW="$PROJECT/sw.js"

if [ ! -f "$INDEX" ]; then
  echo "错误：没有找到 $INDEX"
  exit 1
fi

python3 - "$INDEX" <<'PY'
from pathlib import Path
import re, sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")

m = re.search(r'(<select id="gap">)(.*?)(</select>)', s, re.S)
if not m:
    raise SystemExit('错误：没有找到 <select id="gap">')

body = m.group(2)

# 移除已有的 0 / 0.05 选项，避免重复；然后按 0, 0.05, 0.10... 插回最前面。
body = re.sub(r'<option value="0">0 秒</option>', '', body)
body = re.sub(r'<option value="50">0\.05 秒</option>', '', body)

body = '<option value="0">0 秒</option><option value="50">0.05 秒</option>' + body
s = s[:m.start()] + m.group(1) + body + m.group(3) + s[m.end():]

p.write_text(s, encoding="utf-8")
print("已添加：0 秒、0.05 秒")
PY

if [ -f "$SW" ]; then
  python3 - "$SW" <<'PY'
from pathlib import Path
import re, sys
p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
s=re.sub(r"const CACHE='[^']+';", "const CACHE='fr2000-v7-20260919';", s, count=1)
p.write_text(s, encoding="utf-8")
print("已升级 Service Worker 缓存版本：fr2000-v7-20260919")
PY
fi

echo
echo "检查结果："
grep -n '<select id="gap">' "$INDEX" || true
echo
echo "完成。"
