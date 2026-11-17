#!/usr/bin/env python3
"""Validate the five Turkish content-only drafts without a Windows installation.

The default checks are standard-library only. --schema additionally checks the
pinned original v1 schemas and the same in-memory Turkish extension as Studio;
install tests/requirements.txt first. This does not replace linguistic review or
an actual import/export in every Studio/Android version.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SONGS = {
    "adini-meze-etmem": (46, "7a8598fb77d93a4ee508d3eb67567058c3ef006e8fb811a383dab92c42bded9c"),
    "baba": (63, "0e1dde4564c6c7f328a2d47b44176ce10e0647583307f5bf080e982914a890a6"),
    "bu-gece": (53, "e3fd36023d8c00869cdb6af84d9207da2e3a3a92323e89d4075b254dd3a970be"),
    "desene-gunaydin": (39, "734a610a59a54d5ab55bdb9b2a73d49ab0b4e4ec372e58c1b908a749838f5b35"),
    "dondum-o-yollardan": (39, "029ec6f381aabea05008f0b1211d7c16f88537435fc4f2967eb10c1575b5f8f0"),
}
PERSONS = ["ben (من)", "sen (تو)", "o (او)", "biz (ما)", "siz (شما)", "onlar (آن‌ها)"]
NUMBERS = ["bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on"]
FORBIDDEN = {"media", "startMs", "endMs", "audio", "audioPath", "audioBase64", "coverPath", "base64", "dataUrl", "encryptionKey", "signature"}
CONTRACTIONS = {
    "farkeder": "fark eder", "içicem": "içeceğim", "affedicem": "affedeceğim",
    "sabredicem": "sabredeceğim", "durucam": "duracağım", "ölücez": "öleceğiz",
    "sarılıca’m": "sarılacağım", "gidicem": "gideceğim", "dönücem": "döneceğim",
    "güvenememki": "güvenemem", "desene": "de",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def turkish_lower(s: str) -> str:
    return unicodedata.normalize("NFC", s.translate(str.maketrans({"I": "ı", "İ": "i"})).lower())


def surface(s: str) -> str:
    return turkish_lower(s.strip('.,!?;:"“”()'))


def normalized_sentence(s: str) -> str:
    return " ".join(re.findall(r"[^\W_]+", turkish_lower(s), re.UNICODE))


def scan_forbidden(obj, where="$") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            require(key not in FORBIDDEN, f"{where}.{key}: forbidden in content-only draft")
            scan_forbidden(value, f"{where}.{key}")
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            scan_forbidden(value, f"{where}[{i}]")
    elif isinstance(obj, str):
        require(not re.match(r"^data:(?:audio|image)/", obj.strip(), re.I), f"{where}: embedded media")


def unique(items, label: str) -> None:
    require(len(items) == len(set(items)), f"duplicate {label}")


def validate_table(table, label: str) -> None:
    cols, rows = table["columns"], table["rows"]
    require(1 <= len(cols) <= 8 and 1 <= len(rows) <= 100, f"{label}: invalid dimensions")
    for i, row in enumerate(rows):
        require(len(row) == len(cols), f"{label} row {i}: cells do not match columns")
        for cell in row:
            if isinstance(cell, dict):
                require(bool(cell.get("fa")) and bool(cell.get("en")), f"{label}: incomplete bilingual cell")
            else:
                require(isinstance(cell, str) and bool(cell.strip()), f"{label}: empty cell")


def column_values(word, column_en):
    for table in word.get("tables", []):
        if not table.get("titleEn", "").startswith("Six-person conjugation:"):
            continue
        for idx, column in enumerate(table["columns"]):
            if column_en in column["en"]:
                return [row[idx] for row in table["rows"]]
    raise AssertionError(f"{word['lemma']}: missing conjugation column {column_en!r}")


def expect_column(words, lemma, label, expected):
    word = next((w for w in words if w["lemma"] == lemma), None)
    require(word is not None, f"missing verb {lemma}")
    actual = column_values(word, label)
    require(actual == expected, f"{lemma} / {label}: {actual!r} != {expected!r}")


def validate_draft(slug, expected_lines, expected_hash):
    path = ROOT / "tr" / "ayaz-erdogan" / slug / f"{slug}.rddraft.json"
    data = path.read_bytes()
    require(len(data) < 4 * 1024 * 1024 and not data.startswith(b"\xef\xbb\xbf"), "size or UTF-8 BOM")
    draft = json.loads(data.decode("utf-8", errors="strict"), object_pairs_hook=no_duplicate_keys,
                       parse_constant=lambda s: (_ for _ in ()).throw(ValueError(f"invalid JSON constant {s}")))
    require(draft["songId"] == slug and draft["targetLanguage"] == "tr" and draft["locale"] == "tr-TR", "identity/language")
    require("level" not in draft, "a level was not supplied")
    require(draft["sources"]["lyrics"]["rightsStatus"] == "unverified", "lyric rights must not be presumed")
    scan_forbidden(draft)
    lines = draft["lyrics"]
    require(len(lines) == expected_lines, "unexpected line count")
    require([line["id"] for line in lines] == [f"line-{i}" for i in range(1, len(lines) + 1)], "line IDs/order")
    content_hash = hashlib.sha256("\n".join(line["text"] for line in lines).encode("utf-8")).hexdigest()
    require(content_hash == expected_hash, "lyric sequence changed; review against the supplied text and update the fingerprint")
    for line in lines:
        require(not re.match(r"^\s*\[.*(?:verse|giriş|nakarat|chorus|bridge|köprü).*$", line["text"], re.I), "section label in lyrics")
        require("you might also like" not in line["text"].lower(), "unrelated recommendation in lyrics")
        require(" ".join(t["surface"] for t in line["tokens"]) == line["text"], f"{line['id']}: token reconstruction")
        require(bool(line["translationFa"]) and bool(line["translationEn"]), f"{line['id']}: missing translation")
    line_ids = {line["id"] for line in lines}
    lyric_texts = [normalized_sentence(line["text"]) for line in lines]
    words = draft["vocabulary"]
    unique([w["lexemeId"] for w in words], "lexemeId")
    by_id = {w["lexemeId"]: w for w in words}
    require(set(NUMBERS).issubset({w["lemma"] for w in words}), "vocabulary must teach 1–10")
    for word in words:
        require(re.fullmatch(r"tr:[a-z0-9]+(?:-[a-z0-9]+)*", word["lexemeId"]) is not None, "bad lexemeId")
        require(word["normalizedKey"] == unicodedata.normalize("NFC", word["lemma"]).lower().strip(), f"{word['lemma']}: normalizedKey")
        example = word["example"]
        require(all(example.get(key, "").strip() for key in ("text", "translationFa", "translationEn")), f"{word['lemma']}: incomplete example")
        candidate = normalized_sentence(example["text"])
        require(candidate and not any(f" {candidate} " in f" {line} " for line in lyric_texts), f"{word['lemma']}: example copied from lyrics")
        for i, table in enumerate(word.get("tables", [])):
            validate_table(table, f"{word['lemma']} table {i}")
        if word.get("partEn") == "verb":
            tables = [t for t in word.get("tables", []) if t.get("titleEn", "").startswith("Six-person conjugation:")]
            require(tables and tables[0]["columns"][1]["en"] == "Positive aorist", f"{word['lemma']}: missing positive simple present")
            require(all(len(t["rows"]) == 6 and [row[0] for row in t["rows"]] == PERSONS for t in tables), f"{word['lemma']}: six persons")
    for line in lines:
        for token in line["tokens"]:
            require(bool(token.get("translationFa")) and bool(token.get("translationEn")), f"{line['id']}: token translation")
            ident = token.get("lexemeId")
            if not ident:
                continue
            require(ident in by_id, f"{line['id']}: dangling {ident}")
            word = by_id[ident]
            if word.get("partEn") != "verb":
                continue
            analysis = next((t for t in word["tables"] if t["titleEn"].startswith("Lyric form analysis:")), None)
            require(analysis is not None, f"{word['lemma']}: missing form analysis")
            token_form = surface(token["surface"])
            row = next((r for r in analysis["rows"] if surface(r[0]) == token_form), None)
            require(row is not None, f"{word['lemma']}: missing analysis for {token_form}")
            if row[1]["en"].startswith("Nonfinite"):
                continue
            expected = CONTRACTIONS.get(token_form, token_form)
            conjugated = []
            for table in word["tables"]:
                if table["titleEn"].startswith("Six-person conjugation:"):
                    conjugated.extend(surface(v) for r in table["rows"] for v in r[1:] if isinstance(v, str))
            require(any(v == expected or v.endswith(" " + expected) for v in conjugated),
                    f"{word['lemma']}: lyric form {token_form!r} missing from person table")
    for section in ("grammar", "idioms", "sentences", "questions"):
        unique([item["id"] for item in draft[section]], f"{section} id")
        for item in draft[section]:
            if item.get("lineId"):
                require(item["lineId"] in line_ids, f"{section}: dangling lineId")
            for table in item.get("tables", []):
                validate_table(table, f"{section} {item['id']}")
            if section == "grammar":
                candidate = normalized_sentence(item["example"]["text"])
                require(candidate not in lyric_texts, f"grammar example {item['id']} copies lyric line")
            if section == "sentences":
                candidate = normalized_sentence(item["text"])
                require(candidate not in lyric_texts, f"practice sentence {item['id']} copies lyric line")
    for table in draft["vocabularyTables"]:
        validate_table(table, "vocabularyTables")
    numbers = next(t for t in draft["vocabularyTables"] if t["titleEn"] == "Numbers one to ten and lyric numbers")
    require([row[1] for row in numbers["rows"][:10]] == NUMBERS, "number table should contain one through ten")
    qs = draft["questions"]
    require(Counter(q["type"] for q in qs) == {"choice": 4, "match": 4, "order": 4, "typing": 4}, "quiz types")
    for q in qs:
        for ref in q.get("relatedLexemeIds", []):
            require(ref in by_id, f"{q['id']}: dangling related lexeme")
        if q["type"] == "choice":
            ids = [o["id"] for o in q["options"]]
            unique(ids, f"{q['id']} options")
            require(q["correctId"] in ids, f"{q['id']}: missing correct option")
        elif q["type"] == "match":
            ids = [p["id"] for p in q["pairs"]]
            unique(ids, f"{q['id']} pairs")
            require(set(q.get("meaningOrder", ids)) == set(ids), f"{q['id']}: meaningOrder")
            require(all(p["lexemeId"] in by_id for p in q["pairs"]), f"{q['id']}: dangling match lexeme")
        elif q["type"] == "order":
            ids = [p["id"] for p in q["chunks"]]
            unique(ids, f"{q['id']} chunks")
            require(set(q.get("presentationOrder", ids)) == set(ids), f"{q['id']}: presentationOrder")
        elif q["type"] == "typing":
            require("___" in q["context"] and all(a.strip() for a in q["accepted"]), f"{q['id']}: typing gap/answer")
    # Target the error-prone forms that cannot be checked from shape alone.
    if slug == "adini-meze-etmem":
        expect_column(words, "unutmak", "Unutamam", ["unutamam", "unutamazsın", "unutamaz", "unutamayız", "unutamazsınız", "unutamazlar"])
        expect_column(words, "açmak", "Açtıysan", ["açtıysam", "açtıysan", "açtıysa", "açtıysak", "açtıysanız", "açtılarsa"])
    elif slug == "baba":
        expect_column(words, "tutmak", "tutmazsan", ["tutmazsam", "tutmazsan", "tutmazsa", "tutmazsak", "tutmazsanız", "tutmazlarsa"])
        expect_column(words, "sarılmak", "sarılıca’m", ["sarılacağım", "sarılacaksın", "sarılacak", "sarılacağız", "sarılacaksınız", "sarılacaklar"])
    elif slug == "bu-gece":
        expect_column(words, "durulmak", "Durulurdu", ["durulurdum", "durulurdun", "durulurdu", "durulurduk", "durulurdunuz", "durulurlardı"])
        expect_column(words, "güvenmek", "güvenememki", ["güvenemem", "güvenemezsin", "güvenemez", "güvenemeyiz", "güvenemezsiniz", "güvenemezler"])
    elif slug == "desene-gunaydin":
        expect_column(words, "olmak", "olsaydın", ["olsaydım", "olsaydın", "olsaydı", "olsaydık", "olsaydınız", "olsaydılar"])
        require(next(t for t in lines[31]["tokens"] if t["surface"] == "Sende")["translationFa"] == "نزد تو", "locative sende")
    elif slug == "dondum-o-yollardan":
        expect_column(words, "kaybolmak", "kaybolmuştum", ["kaybolmuştum", "kaybolmuştun", "kaybolmuştu", "kaybolmuştuk", "kaybolmuştunuz", "kaybolmuşlardı"])
        expect_column(words, "kalmak", "kalamazdın", ["kalamazdım", "kalamazdın", "kalamazdı", "kalamazdık", "kalamazdınız", "kalamazlardı"])
    return draft


def validate_schema(drafts):
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
    except ImportError as exc:
        raise RuntimeError("--schema needs: python3 -m pip install -r tests/requirements.txt") from exc
    directory = ROOT / "tests" / "contracts" / "v1"
    draft_schema = json.loads((directory / "draft.schema.json").read_text(encoding="utf-8"))
    lesson_schema = json.loads((directory / "lesson.schema.json").read_text(encoding="utf-8"))
    extended = copy.deepcopy(lesson_schema)
    extended["$defs"]["language"]["enum"].append("tr")
    for name in ("locale", "lexemeId"):
        extended["$defs"][name]["pattern"] = extended["$defs"][name]["pattern"].replace("(?:en|es|ko)", "(?:en|es|ko|tr)")

    def make_validator(lesson):
        registry = Registry().with_resource("urn:reedance:lesson:v1", Resource.from_contents(lesson))
        return Draft202012Validator(draft_schema, registry=registry, format_checker=FormatChecker())

    original, widened = make_validator(lesson_schema), make_validator(extended)

    def validation_only_relabel(value, key=None):
        # A throwaway validation copy demonstrates that the original schema's
        # language restriction is the only difference. Never write this copy.
        if isinstance(value, dict):
            return {k: validation_only_relabel(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [validation_only_relabel(v) for v in value]
        if key == "targetLanguage" and value == "tr":
            return "en"
        if key == "locale" and value == "tr-TR":
            return "en-GB"
        if isinstance(value, str) and value.startswith("tr:"):
            return "en:" + value[3:]
        return value

    for slug, draft in drafts.items():
        errors = list(widened.iter_errors(draft))
        require(not errors, f"{slug}: extended schema errors: {[(list(e.path), e.message) for e in errors[:3]]}")
        require(not original.is_valid(draft), f"{slug}: original v1 unexpectedly accepted tr")
        control_errors = list(original.iter_errors(validation_only_relabel(draft)))
        require(not control_errors, f"{slug}: non-language original-schema errors: {[(list(e.path), e.message) for e in control_errors[:3]]}")
        print(f"  {slug}: extended schema OK; original v1 rejects tr as expected")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", action="store_true", help="also check pinned JSON schemas (requires jsonschema)")
    args = parser.parse_args()
    try:
        drafts = {}
        for slug, (count, digest) in SONGS.items():
            drafts[slug] = validate_draft(slug, count, digest)
            print(f"{slug}: content/reference checks OK")
        if args.schema:
            validate_schema(drafts)
    except (AssertionError, KeyError, ValueError, OSError, RuntimeError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1
    print("All five drafts passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
