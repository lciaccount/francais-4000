from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
idx=ROOT/'index.html'
s=idx.read_text(encoding='utf8')
sents=json.load(open(ROOT/'sentences-4000.json',encoding='utf8'))
extra=json.load(open(ROOT/'extra-words-4000.json',encoding='utf8'))
# Replace sentence corpus.
blob=json.dumps(sents,ensure_ascii=False,separators=(',',':'))
s=re.sub(r'const SENTENCES=\[.*?\];\nconst CATEGORIES=', 'const SENTENCES='+blob+';\nconst CATEGORIES=', s, count=1, flags=re.S)
# Insert / replace extra dictionary.
extra_blob=json.dumps(extra,ensure_ascii=False,separators=(',',':'))
if 'const EXTRA_WORDS_4000=' in s:
    s=re.sub(r'const EXTRA_WORDS_4000=\{.*?\};', 'const EXTRA_WORDS_4000='+extra_blob+';', s, count=1, flags=re.S)
else:
    s=s.replace('const EXTRA_LEMMA_WORDS=', 'const EXTRA_WORDS_4000='+extra_blob+';\nconst EXTRA_LEMMA_WORDS=',1)
# Clickable word index follows rendering rules.
comp={"week-end","rendez-vous","petit-déjeuner","après-midi","wi-fi","centre-ville","pique-nique","grand-père","grand-mère","grands-parents","beau-père","belle-mère","beau-frère","belle-sœur","petit-fils","petite-fille","micro-ondes","non-fumeur","sèche-cheveux","coffre-fort","e-mails","dix-huit","peut-être"}
pat=re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+)?(?:-[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+)*")
def norm(w):
    x=w.lower().replace('’',"'")
    m=re.match(r"^(?:l|d|j|t|c|m|n|s|qu)'(.+)$",x)
    if m: x=m.group(1)
    return x.strip("-'")
click=set()
for sent in sents:
    for m in pat.finditer(sent['fr']):
        raw=m.group(0); key=norm(raw)
        if '-' in raw and key not in comp:
            click.update(norm(x) for x in raw.split('-') if norm(x))
        elif key:
            click.add(key)
word_index={w:i+1 for i,w in enumerate(sorted(click))}
s=re.sub(r'const BUILTIN_WORD_INDEX=\{.*?\};','const BUILTIN_WORD_INDEX='+json.dumps(word_index,ensure_ascii=False,separators=(',',':'))+';',s,count=1,flags=re.S)
# Add peut-être as lexical compound.
s=re.sub(r'const COMPOUND_WORDS=new Set\(\[(.*?)\]\);', lambda m:'const COMPOUND_WORDS=new Set(['+ (m.group(1)+',"peut-être"' if '"peut-être"' not in m.group(1) else m.group(1)) +']);', s, count=1, flags=re.S)
# Dictionary lookups include new synchronized entries.
s=s.replace("const key=normWord(raw),base=WORDS[key]||LEMMA_WORDS[key]||EXTRA_LEMMA_WORDS[key]||null", "const key=normWord(raw),base=WORDS[key]||EXTRA_WORDS_4000[key]||LEMMA_WORDS[key]||EXTRA_LEMMA_WORDS[key]||null")
s=s.replace("const exists=WORDS[key]||LEMMA_WORDS[key]||EXTRA_LEMMA_WORDS[key]||DICT_OVERRIDES[key];", "const exists=WORDS[key]||EXTRA_WORDS_4000[key]||LEMMA_WORDS[key]||EXTRA_LEMMA_WORDS[key]||DICT_OVERRIDES[key];")
# UI/counts: preserve layout and behavior, make totals dynamic where possible.
s=s.replace('法语2000句','法语4000句').replace('日常法语 2000 句','日常法语 4000 句').replace('日常法语2000句','日常法语4000句')
s=s.replace('/ 2000','/ 4000')
s=s.replace('max="2000"','max="4000"')
s=s.replace("const STORE_KEY='fr2000-v2';","const STORE_KEY='fr4000-v1';")
s=s.replace("function renderProgress(){const n=progress.studied.size,p=(n/20).toFixed(1);$('#progressCount').textContent=String(n);$('#progressPct').textContent=`${p}%`;$('#headerProgress').title=`已学 ${n} / 2000（${p}%） · 收藏 ${progress.favorites.size} · 已掌握 ${progress.mastered.size}`;}",
"function renderProgress(){const n=progress.studied.size,p=(n/SENTENCES.length*100).toFixed(1);$('#progressCount').textContent=String(n);$('#progressPct').textContent=`${p}%`;$('#headerProgress').title=`已学 ${n} / ${SENTENCES.length}（${p}%） · 收藏 ${progress.favorites.size} · 已掌握 ${progress.mastered.size}`;}")
s=s.replace('`在 2000 句中找到 ${arr.length} 条`','`在 ${SENTENCES.length} 句中找到 ${arr.length} 条`')
s=s.replace('artist:`日常法语 2000 句 · #${id}`','artist:`日常法语 4000 句 · #${id}`')
s=s.replace('Math.min(2000,Number($(\'#rangeStart\').value)||1)',"Math.min(SENTENCES.length,Number($('#rangeStart').value)||1)")
s=s.replace('Math.min(2000,Number($(\'#rangeEnd\').value)||1)',"Math.min(SENTENCES.length,Number($('#rangeEnd').value)||1)")
s=s.replace("const next=Math.max(1,Math.min(2000,id+delta));", "const next=Math.max(1,Math.min(SENTENCES.length,id+delta));")
s=s.replace("id=arr.length?arr[0].id:(state.cat*100+1);", "id=arr.length?arr[0].id:(SENTENCES.find(s=>s.category===state.cat)?.id||1);")
# Any remaining literal human-facing total.
s=s.replace('在 2000 句中','在 4000 句中')
# New asset cache tag.
s=re.sub(r'\?v=(?:frtrim\d+|fronly\d+|neural\d+|fr4000v\d+)', '?v=fr4000v3', s)
idx.write_text(s,encoding='utf8')
# web manifest
mf=ROOT/'manifest.webmanifest'; t=mf.read_text(encoding='utf8').replace('2000','4000'); mf.write_text(t,encoding='utf8')
# service worker cache
sw=ROOT/'sw.js'; t=sw.read_text(encoding='utf8'); t=re.sub(r"const CACHE='[^']+';","const CACHE='fr4000-v13-fonts-offline-20260924';",t,count=1); sw.write_text(t,encoding='utf8')
# voice manifest: audio intentionally not bundled; local generator enables slots after successful build.
vm=ROOT/'audio'/'voice-manifest.json'
manifest={
  'version':'fr4000-v3-source','locale':'fr-FR','availableSlots':[],
  'voices':[{'slot':1,'shortName':'fr-FR-HenriNeural','label':'Henri · 法国法语男声'},{'slot':2,'shortName':'fr-FR-EloiseNeural','label':'Eloise · 法国法语女声'},{'slot':3,'shortName':'fr-FR-DeniseNeural','label':'Denise · 法国法语女声'}],
  'sentenceRate':'-4%','wordRate':'-14%','sentenceCount':len(sents),'wordCount':len(word_index),
  'silenceTrim':{'version':'fr4000-v3','edgeThresholdDb':-50,'edgeGuardMs':0,'maxSentencePauseMs':80,'note':'local builder removes leading/trailing silence and shortens overlong internal sentence pauses'}
}
vm.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('updated index; sentences',len(sents),'words',len(word_index))
