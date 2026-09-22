#!/usr/bin/env python3
"""Build offline grammar, morphology, phrase and corpus-example data.

Build dependency (not needed by the web app):
    python -m pip install spacy fr-core-news-sm
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import spacy


ROOT = Path(__file__).resolve().parent
WORD_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+)?"
    r"(?:-[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+)*"
)
CLAUSE_RE = re.compile(r"(?<=[.!?;])\s+|\s*[,;:]\s*")

POS_ZH = {
    "NOUN": "名词", "PROPN": "专名", "VERB": "动词", "AUX": "助动词",
    "ADJ": "形容词", "ADV": "副词", "PRON": "代词", "DET": "限定词",
    "ADP": "介词", "CCONJ": "并列连词", "SCONJ": "从属连词",
    "INTJ": "感叹词", "NUM": "数词", "PART": "小品词",
}
MOOD_ZH = {"Ind": "直陈式", "Cnd": "条件式", "Imp": "祈使式", "Sub": "虚拟式"}
TENSE_ZH = {"Pres": "现在时", "Imp": "未完成过去时", "Fut": "简单将来时", "Past": "过去时"}
PERSON_ZH = {"1": "第一人称", "2": "第二人称", "3": "第三人称"}
NUMBER_ZH = {"Sing": "单数", "Plur": "复数"}
GENDER_ZH = {"Masc": "阳性", "Fem": "阴性"}

# Longer phrases must come first. Meanings are deliberately phrase meanings, not
# word-by-word glosses.
PHRASES = {
    "s'il vous plaît": "请（正式或礼貌用法）",
    "s'il te plaît": "请（对熟人）",
    "tout à l'heure": "刚才；待会儿（由语境决定）",
    "à tout à l'heure": "待会儿见",
    "est-ce que": "是否……；用于构成一般疑问句",
    "qu'est-ce que": "什么；用于询问事物",
    "il n'y a pas de quoi": "不用客气",
    "je vous en prie": "不客气；请",
    "comment allez-vous": "您好吗",
    "comment ça va": "你好吗；情况怎么样",
    "ça fait longtemps": "好久不见；已经很久了",
    "avoir besoin de": "需要……",
    "avoir mal à": "……疼",
    "tout de suite": "马上；立刻",
    "de temps en temps": "有时；偶尔",
    "en train de": "正在……",
    "près de": "靠近……",
    "loin de": "离……远",
    "à côté de": "在……旁边",
    "en face de": "在……对面",
    "au revoir": "再见",
    "à bientôt": "回头见；很快再见",
    "de rien": "不客气",
    "avec plaisir": "很乐意；不客气",
    "pas de problème": "没问题",
    "bien sûr": "当然",
    "excusez-moi": "对不起；打扰一下",
    "allez-y": "请去吧；请继续；您请",
    "je voudrais": "我想要……（礼貌表达）",
    "pourriez-vous": "您能否……（礼貌请求）",
    "pouvez-vous": "您能……吗",
    "puis-je": "我可以……吗",
    "ça marche": "可以；行得通；正常运行",
    "il faut": "需要；必须",
    "il y a": "有；……以前（与时间长度连用）",
    "avoir envie de": "想要做……",
    "prendre soin de": "照顾；保重",
    "faire attention": "注意；当心",
    "à pied": "步行",
    "en avance": "提前",
    "en retard": "迟到；晚点",
    "parce que": "因为",
    "même si": "即使",
    "afin de": "为了……",
}
PHRASE_PATTERNS = (
    (r"\b(?:j'ai|tu as|il a|elle a|on a|nous avons|vous avez|ils ont|elles ont) besoin de\b", "avoir besoin de：需要……"),
    (r"\b(?:j'ai|tu as|il a|elle a|on a|nous avons|vous avez|ils ont|elles ont) mal (?:au|à la|à l'|aux)\b", "avoir mal à：……疼"),
    (r"\b(?:j'ai|tu as|il a|elle a|on a|nous avons|vous avez|ils ont|elles ont) envie de\b", "avoir envie de：想要做……"),
    (r"\b(?:prends|prenez|prendre) soin de\b", "prendre soin de：照顾；保重"),
    (r"\b(?:vais|vas|va|allons|allez|vont)\s+[a-zà-öø-ÿœç'-]+(?:er|ir|re)\b", "aller + 不定式：近期将来，表示即将做某事"),
    (r"\b(?:viens|vient|venons|venez|viennent) de\s+[a-zà-öø-ÿœç'-]+(?:er|ir|re)\b", "venir de + 不定式：刚刚做了某事"),
)

FIXED_STARTS = (
    "bonjour", "bonsoir", "salut", "merci", "pardon", "bienvenue", "au revoir",
    "à bientôt", "à demain", "bonne journée", "bonne soirée", "bonne nuit",
    "bon courage", "bon appétit", "félicitations", "de rien", "avec plaisir",
    "au plaisir", "enchanté",
)
USAGE_POS = {"固定表达", "名词短语", "动词短语", "天气表达", "症状表达", "形容词/状态表达", "时间表达"}
SPLIT_FORMS = {
    "aidez": ("aider", "VERB", ["祈使式", "第二人称", "复数"]),
    "amusez": ("amuser", "VERB", ["祈使式", "第二人称", "复数"]),
    "devons": ("devoir", "AUX", ["直陈式", "现在时", "第一人称", "复数"]),
    "elle": ("elle", "PRON", ["第三人称", "单数", "阴性"]),
    "excusez": ("excuser", "VERB", ["祈使式", "第二人称", "复数"]),
    "montrez": ("montrer", "VERB", ["祈使式", "第二人称", "复数"]),
    "puis": ("pouvoir", "AUX", ["直陈式", "现在时", "第一人称", "单数"]),
    "reposez": ("reposer", "VERB", ["祈使式", "第二人称", "复数"]),
    "t": ("t", "PART", ["倒装连音 /t/"]),
}


def norm(text: str) -> str:
    value = text.lower().replace("’", "'")
    match = re.match(r"^(?:l|d|j|t|c|m|n|s|qu)'(.+)$", value)
    if match:
        value = match.group(1)
    return value.strip("-'")


def load_inline_json(html: str, name: str) -> dict:
    match = re.search(rf"^const {re.escape(name)}=(.*);$", html, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Cannot find inline constant {name}")
    return json.loads(match.group(1))


def morph_values(token, field: str) -> list[str]:
    return token.morph.get(field)


def localized_morph(token, mood_override: str = "") -> list[str]:
    values: list[str] = []
    mood = [mood_override] if mood_override else morph_values(token, "Mood")
    tense = morph_values(token, "Tense")
    person = morph_values(token, "Person")
    number = morph_values(token, "Number")
    gender = morph_values(token, "Gender")
    verb_form = morph_values(token, "VerbForm")
    if mood:
        values.append(MOOD_ZH.get(mood[0], mood[0]))
    if tense:
        values.append(TENSE_ZH.get(tense[0], tense[0]))
    if person:
        values.append(PERSON_ZH.get(person[0], person[0]))
    if number:
        values.append(NUMBER_ZH.get(number[0], number[0]))
    if gender:
        values.append(GENDER_ZH.get(gender[0], gender[0]))
    if "Inf" in verb_form:
        values.append("不定式")
    elif "Part" in verb_form:
        values.append("分词")
    return list(dict.fromkeys(values))


def dictionary_meaning(info: dict | None, pos: str) -> str:
    if not info:
        return ""
    groups = info.get("groups", [])
    lexical = [g for g in groups if g.get("pos") not in USAGE_POS]
    needles = {
        "VERB": "动词", "AUX": "动词", "NOUN": "名词", "PROPN": "名词",
        "ADJ": "形容", "ADV": "副词", "ADP": "介词", "PRON": "代词",
        "DET": "限定词", "CCONJ": "连词", "SCONJ": "连词", "INTJ": "感叹",
    }
    needle = needles.get(pos, "")
    chosen = next((g for g in lexical if needle and needle in g.get("pos", "")), None)
    chosen = chosen or (lexical[0] if lexical else (groups[0] if groups else None))
    meanings = chosen.get("meanings", []) if chosen else []
    return meanings[0] if meanings else ""


def contextual_meaning(info: dict | None, pos: str, key: str, sentence: str) -> str:
    """Select a concise sense from local French context before showing all senses."""
    low = sentence.lower().replace("’", "'")
    if key == "vol":
        return "盗窃；失窃事件" if re.search(r"signaler|déclaration|portefeuille|téléphone", low) else "航班；飞行"
    if key == "café":
        return "咖啡馆" if re.search(r"\b(?:au|dans le|près du) café\b", low) else "咖啡"
    if key == "carte":
        if "sur la carte" in low:
            return "地图"
        if re.search(r"carte bancaire|payer .* par carte|bloquer .* carte", low):
            return "银行卡；支付卡"
    if key == "temps":
        return "天气" if re.search(r"quel temps|le temps (?:est|change)", low) else "时间"
    if key == "marche":
        return "可以；行得通；正常运转" if "ça marche" in low else "步行；走路"
    if key == "poste":
        return "邮局" if re.search(r"(?:à|vers|trouver|où est) la poste", low) else "职位；岗位"
    if key == "puis" and pos == "AUX":
        return "可以（pouvoir 的第一人称单数倒装形式，用于 puis-je）"
    if key == "t":
        return "倒装疑问中的连音 /t/，不是独立词"
    if key == "porte":
        return "门"
    if key == "montre":
        return "手表" if pos == "NOUN" else "展示；指给看"
    return dictionary_meaning(info, pos)


def contextual_morph(token) -> list[str]:
    values = localized_morph(token)
    if token.pos_ in {"NOUN", "PROPN"}:
        determiner = next((child for child in token.children if child.dep_ == "det"), None)
        if determiner:
            genders = morph_values(determiner, "Gender")
            if genders:
                values = [v for v in values if v not in GENDER_ZH.values()]
                values.append(GENDER_ZH.get(genders[0], genders[0]))
    return list(dict.fromkeys(values))


def find_phrases(text: str) -> list[dict]:
    folded = text.lower().replace("’", "'")
    found = []
    for phrase, meaning in sorted(PHRASES.items(), key=lambda item: -len(item[0])):
        if phrase in folded:
            found.append({"text": phrase, "meaning": meaning})
    for pattern, meaning in PHRASE_PATTERNS:
        for match in re.finditer(pattern, folded, re.I):
            found.append({"text": text[match.start():match.end()], "meaning": meaning})
    # Remove phrases wholly contained in a longer match.
    return [p for p in found if not any(p["text"] != q["text"] and p["text"] in q["text"] for q in found)]


def finite_tokens(doc, original: str):
    question = "?" in original
    out = []
    for token in doc:
        if "Fin" not in morph_values(token, "VerbForm"):
            continue
        mood = (morph_values(token, "Mood") or [""])[0]
        # The small model often labels an inverted question as imperative.
        if mood == "Imp" and question:
            mood = "Ind"
        if not question and token.i == 0 and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿŒœÇç]+ez-(?:moi|nous|vous)\b", original, re.I):
            mood = "Imp"
        out.append((token, mood, (morph_values(token, "Tense") or [""])[0]))
    return out


def compound_construction(doc, finite):
    for i, (aux, mood, tense) in enumerate(finite):
        if aux.lemma_.lower() not in {"avoir", "être"}:
            continue
        for token in doc[aux.i + 1:min(len(doc), aux.i + 6)]:
            if token.is_punct:
                break
            if "Part" in morph_values(token, "VerbForm") and (morph_values(token, "Tense") or [""])[0] == "Past":
                label = "复合过去时（passé composé）" if tense == "Pres" else "复合时态"
                evidence = [{"words": [aux.text, token.text], "text": f"{aux.text} 是助动词，{token.text} 是过去分词，两者共同构成{label.replace('（passé composé）', '')}。"}]
                return label, evidence
    return None


def periphrastic_construction(doc, finite):
    for token, _, tense in finite:
        tail = [t for t in doc[token.i + 1:min(len(doc), token.i + 5)] if not t.is_punct]
        infinitive = next((t for t in tail if "Inf" in morph_values(t, "VerbForm")), None)
        if token.lemma_.lower() == "aller" and tense == "Pres" and infinitive:
            return "近期将来时（aller + 不定式）", [{"words": [token.text, infinitive.text], "text": f"{token.text} 是 aller 的现在时，{infinitive.text} 是不定式，整体表示即将发生的动作。"}]
        if token.lemma_.lower() == "venir" and tense == "Pres" and infinitive and any(t.lower_ == "de" for t in tail):
            return "近期过去时（venir de + 不定式）", [{"words": [token.text, infinitive.text], "text": f"{token.text} + de + {infinitive.text} 表示“刚刚做了……”。"}]
    return None


def tense_analysis(doc, original: str):
    finite = finite_tokens(doc, original)
    special = compound_construction(doc, finite) or periphrastic_construction(doc, finite)
    if special:
        return special[0], special[1], "high"
    labels, evidence = [], []
    for token, mood, tense in finite:
        if mood == "Imp":
            label = "祈使式"
        elif mood == "Cnd":
            label = "条件式现在时" if tense == "Pres" else "条件式"
        elif mood == "Sub":
            label = f"虚拟式{TENSE_ZH.get(tense, '')}"
        else:
            label = TENSE_ZH.get(tense, "直陈式")
        if label not in labels:
            labels.append(label)
        detail = "、".join(localized_morph(token, mood)) or "变位谓语"
        evidence.append({"words": [token.text], "text": f"{token.text}（原形 {token.lemma_}）：{detail}。"})
    if labels:
        joined = labels[0] if len(labels) == 1 else " + ".join(labels[:3])
        return joined, evidence[:4], "high"
    lowered = original.lower().replace("’", "'").strip()
    # The compact statistical model occasionally mistags very common short forms,
    # especially after a greeting or around hyphens. These transparent rules keep
    # those corpus-specific cases deterministic.
    aux_match = re.search(r"\b(j'ai|tu as|il a|elle a|on a|nous avons|vous avez|ils ont|elles ont|je suis|tu es|il est|elle est|on est|nous sommes|vous êtes|ils sont|elles sont)\b", lowered)
    participle = next((t for t in doc if "Part" in morph_values(t, "VerbForm") and (morph_values(t, "Tense") or [""])[0] == "Past"), None)
    if aux_match and participle:
        aux = aux_match.group(1)
        return "复合过去时（passé composé）", [{"words": [aux, participle.text], "text": f"{aux} 是助动词的变位，{participle.text} 是过去分词。"}], "high"
    if re.search(r"\b(?:aimerais|aimerait|pourrais|pourrait|voudrais|voudrait|devrais|devrait)\b", lowered):
        word = re.search(r"\b(?:aimerais|aimerait|pourrais|pourrait|voudrais|voudrait|devrais|devrait)\b", lowered).group(0)
        return "条件式现在时", [{"words": [word], "text": f"{word} 是条件式现在时形式，常用于愿望或礼貌表达。"}], "high"
    current_forms = r"puis|veux|veut|es|est|prie|habite|neige|monte|baisse|change|arrête|prends|dit|faut|ai|as|a|avons|avez|ont"
    current = re.search(rf"\b({current_forms})\b", lowered)
    if current:
        word = current.group(1)
        return "现在时", [{"words": [word], "text": f"{word} 是本句的现在时变位形式。"}], "high"
    if re.match(r"^comment\s+(?:aller|faire|obtenir|trouver|contacter)\b", lowered):
        verb = re.match(r"^comment\s+([a-zà-öø-ÿœç'-]+)", lowered).group(1)
        return "疑问省略句（comment + 不定式）", [{"words": [verb], "text": f"{verb} 使用不定式；这里是询问方法或路线的省略表达。"}], "high"
    command = re.match(r"^([a-zà-öø-ÿœç]+ez)(?:-(?:moi|nous|vous))?\b", lowered)
    if command and "?" not in original:
        word = command.group(1)
        return "祈使式", [{"words": [word], "text": f"{word} 位于句首且省略主语，在这里是 vous 形式的祈使式。"}], "high"
    if lowered.startswith(FIXED_STARTS):
        return "固定表达 / 省略句（无完整变位谓语）", [], "high"
    if len(list(WORD_RE.finditer(original))) <= 4:
        return "固定表达 / 省略句（无完整变位谓语）", [], "medium"
    return "省略句或固定搭配（未发现完整变位谓语）", [], "medium"


def structure_analysis(doc, original: str, tense_label: str):
    text = original.strip().rstrip(".!?")
    if "固定表达" in tense_label or "省略句" in tense_label:
        return "固定表达 / 省略结构", [{"text": text, "role": "固定表达或省略成分"}], []
    is_question = "?" in original
    is_imperative = "祈使式" in tense_label
    has_subordinate = any(t.dep_ in {"mark", "advcl", "ccomp", "xcomp"} for t in doc)
    if is_question and re.search(r"-(?:t-)?(?:vous|tu|il|elle|on|nous|ils|elles)\b", original, re.I):
        label = "疑问成分 + 谓语—主语倒装 + 补语"
    elif is_question:
        label = "疑问句（陈述语序或疑问词引导）"
    elif is_imperative:
        label = "祈使谓语 + 宾语 / 补语"
    elif has_subordinate:
        label = "主句 + 从句 / 不定式补语"
    else:
        label = "主语 + 变位谓语 + 宾语 / 补语"

    root = next((t for t in doc if t.dep_ == "ROOT" and t.pos_ in {"VERB", "AUX"}), None)
    root = root or next((item[0] for item in finite_tokens(doc, original)), None)
    subject = next((t for t in doc if t.dep_ in {"nsubj", "expl:subj", "csubj"} and (not root or t.head == root)), None)
    subject = subject or next((t for t in doc if t.dep_ in {"nsubj", "expl:subj", "csubj"}), None)
    parts = []
    if subject:
        subject_text = " ".join(t.text for t in subject.subtree).lstrip("-")
        subject_text = re.sub(r"\s+(?:n|ne)\s*['’]?$", "", subject_text, flags=re.I)
        parts.append({"text": subject_text, "role": "主语"})
    if root:
        parts.append({"text": root.text, "role": "核心谓语" if not is_imperative else "祈使谓语"})
        if root.dep_ == "cop" and root.head.pos_ in {"ADJ", "NOUN", "PROPN", "ADV"}:
            parts.append({"text": root.head.text, "role": "表语 / 核心说明"})
        complements = [t for t in root.children if t.dep_ in {"obj", "iobj", "obl", "xcomp", "ccomp", "advmod"}]
        for token in complements[:2]:
            phrase = " ".join(t.text for t in token.subtree)
            if phrase and not any(p["text"] == phrase for p in parts):
                parts.append({"text": phrase, "role": "宾语 / 补语 / 状语"})
    if not parts:
        clauses = [p.strip() for p in CLAUSE_RE.split(text) if p.strip()]
        parts = [{"text": part, "role": "主要分句" if i == 0 else "补充分句"} for i, part in enumerate(clauses[:3])]

    subparts = []
    for token in doc:
        if token.dep_ in {"ccomp", "advcl"}:
            phrase = " ".join(t.text for t in token.subtree)
            if phrase:
                subparts.append({"text": phrase, "role": "宾语从句" if token.dep_ == "ccomp" else "状语从句"})
    return label, parts[:5], subparts[:2]


def notes_for(doc, original: str, phrases: list[dict]) -> list[str]:
    low = original.lower().replace("’", "'")
    notes = []
    if re.search(r"\b(?:ne|n')\b.*\b(?:pas|plus|jamais|rien|personne)\b", low):
        notes.append("否定通常由 ne / n’ 与 pas、plus、jamais、rien 等词共同构成。")
    if "?" in original and re.search(r"-(?:t-)?(?:vous|tu|il|elle|on|nous|ils|elles)\b", low):
        notes.append("这里使用主谓倒装构成疑问；夹在两个元音之间的 -t- 只用于连音，没有独立词义。")
    if re.search(r"\b(?:que|qu')\b", low):
        notes.append("que / qu’ 可引导从句，补充说明主句中的内容。")
    if re.search(r"\b(?:pour|afin de)\s+", low):
        notes.append("pour / afin de + 不定式常表示目的，即“为了……”。")
    if any(t.dep_ == "xcomp" and t.pos_ == "VERB" for t in doc):
        notes.append("第二个动词使用不定式，补充说明意愿、能力、计划或动作内容。")
    if "vous" in low:
        notes.append("vous 可指“您”或“你们”；礼貌场景中通常译作“您”。")
    for phrase in phrases[:2]:
        notes.append(f"{phrase['text']} 是一个整体表达，意思是“{phrase['meaning']}”。")
    return list(dict.fromkeys(notes))[:5]


def voice_analysis(doc, tense_label: str):
    passive = [t for t in doc if "Pass" in morph_values(t, "Voice") or t.dep_ in {"aux:pass", "nsubj:pass"}]
    if passive:
        words = list(dict.fromkeys(t.text for t in passive))
        return "被动语态", words, "检测到被动形态或被动句法关系。"
    if "固定表达" in tense_label or "省略句" in tense_label:
        return "不适用", [], "固定表达或省略句没有需要判断主动、被动的完整谓语。"
    verbs = [t.text for t in doc if t.pos_ in {"VERB", "AUX"} and "Fin" in morph_values(t, "VerbForm")]
    return "主动 / 非被动结构", verbs[:3], "未检测到法语被动结构（être + 过去分词及相应句法关系）。"


def build():
    sentences = json.loads((ROOT / "sentences-4000.json").read_text(encoding="utf-8"))
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    dictionaries = {}
    for name in ("WORDS", "LEMMA_WORDS", "DICT_OVERRIDES", "EXTRA_WORDS_4000", "EXTRA_LEMMA_WORDS"):
        dictionaries.update(load_inline_json(html, name))
    dictionaries["sur"] = {"groups": [{"pos": "介词", "meanings": ["在……上；关于"]}], "ipa": "sˈyʁ"}
    dictionaries["t"] = {"groups": [{"pos": "连音", "meanings": ["倒装疑问中的连音 /t/，不是独立词，不单独朗读"]}], "ipa": "t"}

    nlp = spacy.load("fr_core_news_sm", disable=["ner"])
    docs = list(nlp.pipe((s["fr"] for s in sentences), batch_size=128))
    examples: dict[str, list[int]] = defaultdict(list)
    token_candidates: dict[str, list[dict]] = defaultdict(list)
    annotations = {}

    for sentence, doc in zip(sentences, docs):
        sid, original = sentence["id"], sentence["fr"]
        phrases = find_phrases(original)
        tense, evidence, confidence = tense_analysis(doc, original)
        structure, parts, subparts = structure_analysis(doc, original, tense)
        voice, voice_words, voice_text = voice_analysis(doc, tense)

        keywords = []
        seen = set()
        for match in WORD_RE.finditer(original):
            raw, key = match.group(0), norm(match.group(0))
            if key in seen:
                continue
            seen.add(key)
            overlapping = [t for t in doc if t.idx < match.end() and t.idx + len(t.text) > match.start() and not t.is_punct]
            token = next((t for t in overlapping if t.pos_ in {"VERB", "AUX"}), None)
            token = token or next((t for t in overlapping if t.pos_ in POS_ZH and t.pos_ not in {"DET", "PRON", "ADP", "PART"}), None)
            token = token or next((t for t in overlapping if t.pos_ in POS_ZH), None)
            if not token:
                continue
            lemma = token.lemma_.lower().replace("’", "'") if token.lemma_ else key
            info = dictionaries.get(key) or dictionaries.get(norm(lemma))
            meaning = contextual_meaning(info, token.pos_, key, original)
            metadata = {
                "lemma": lemma, "pos": token.pos_, "posLabel": POS_ZH.get(token.pos_, token.pos_),
                "morph": contextual_morph(token), "currentMeaning": meaning,
            }
            token_candidates[key].append(metadata)
            if len(examples[key]) < 6:
                examples[key].append(sid)
            if token.pos_ in {"NOUN", "PROPN", "VERB", "AUX", "ADJ", "ADV"} and meaning and len(keywords) < 5:
                keywords.append({"raw": raw, **metadata})

        summary = f"{structure}；{tense}。"
        annotations[str(sid)] = {
            "confidence": confidence, "summary": summary, "structure": structure,
            "parts": parts, "subparts": subparts, "tense": tense, "tenseEvidence": evidence,
            "voice": voice, "voiceWords": voice_words, "voiceText": voice_text,
            "notes": notes_for(doc, original, phrases), "phrases": phrases, "keywords": keywords,
        }

    lexicon = {}
    builtin_keys = set(load_inline_json(html, "BUILTIN_WORD_INDEX"))
    for key in sorted(builtin_keys - set(token_candidates)):
        if key not in SPLIT_FORMS:
            continue
        lemma, pos, morphology = SPLIT_FORMS[key]
        info = dictionaries.get(key) or dictionaries.get(norm(lemma))
        token_candidates[key].append({
            "lemma": lemma, "pos": pos, "posLabel": POS_ZH.get(pos, pos),
            "morph": morphology, "currentMeaning": contextual_meaning(info, pos, key, ""),
        })
        for sentence in sentences:
            pieces = [norm(part) for word in WORD_RE.findall(sentence["fr"]) for part in word.split("-")]
            if key in pieces and len(examples[key]) < 6:
                examples[key].append(sentence["id"])
    for key, candidates in token_candidates.items():
        # Prefer an analysis that occurs most often; break ties in favor of content words.
        encoded = Counter(json.dumps(c, ensure_ascii=False, sort_keys=True) for c in candidates)
        best = json.loads(encoded.most_common(1)[0][0])
        ids = examples[key]
        # Prefer short, easy-to-scan examples and spread duplicates across the corpus.
        ranked = sorted(ids, key=lambda sid: (len(sentences[sid - 1]["fr"]), sid))
        selected = []
        for sid in ranked:
            if sid not in selected:
                selected.append(sid)
            if len(selected) == 3:
                break
        best["examples"] = selected
        lexicon[key] = best

    data = {
        "version": "2026-09-22.1", "generator": "spaCy fr_core_news_sm + curated rules",
        "sentenceCount": len(sentences), "sentences": annotations, "lexicon": lexicon,
        "phraseCount": sum(len(a["phrases"]) for a in annotations.values()),
    }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (ROOT / "learning-data-4000.js").write_text(
        "/* Generated by build_learning_data.py; do not edit by hand. */\nwindow.LEARNING_DATA=" + payload + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {len(annotations)} sentence analyses, {len(lexicon)} lexicon forms, {data['phraseCount']} phrase matches")


if __name__ == "__main__":
    build()
