#!/usr/bin/env python
"""One-off reconstruction of the Nikkei 225 and Hang Seng change logs (2009+).

    python scripts/build_asia_changelogs.py [--cache DIR]

Writes data/membership/sources/n225_changes.csv and hsi_changes.csv in the
format every other change log uses (date, action in|out, symbol, name), which
scripts/build_membership.py then turns into membership spells. Neither index
publishes a free machine-readable history, so both are rebuilt from Wikipedia
and checked by the index-size replay in tests/test_membership.py.

Hang Seng
    The change table in https://zh.wikipedia.org/wiki/恒生指數 lists every
    constituent change with its effective date and the index size after it.
    Company names are mapped to HKEX codes by HSI_CODES below (hand-maintained;
    every mapping is checked against the size column by the replay test).

Nikkei 225
    The constituent list in https://ja.wikipedia.org/wiki/日経平均株価 was parsed
    at every revision since 2008-10. Only revisions listing 222-228 names are
    used (vandalism and half-finished edits list far more or fewer). Each name
    is mapped to a TSE code: from the list itself where it carries codes
    (2019+), else from N225_CODES (hand-maintained, sourced from each company's
    article infobox). A change must persist 14 days to count. Changes edited
    within 45 days before / 30 days after a periodic review are dated to the
    review's effective date (first business day of October; from 2022 also of
    April); other changes, mergers and delistings, keep the edit date and are
    marked "approximate".
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SOURCES = ROOT / "data" / "membership" / "sources"
UA = {"User-Agent": "trading-autoresearch membership builder (ivo.lasek@gmail.com)"}
START = pd.Timestamp("2009-01-01")

# ---------------------------------------------------------------------------
# Hang Seng
# ---------------------------------------------------------------------------

HSI_PAGE = "https://zh.wikipedia.org/wiki/%E6%81%92%E7%94%9F%E6%8C%87%E6%95%B8"

#: zh-Wikipedia company name -> HKEX code, for every name in the change table
#: from 2009 on. Renames that keep the code (香港電燈 -> 電能實業, 長江實業 ->
#: 長和) map both names to the same code and so produce no change.
HSI_CODES = {
    "裕元工業": "0551", "華潤電力": "0836", "華潤置地": "1109", "百麗國際": "1880",
    "中煤能源": "1898", "香港電燈": "0006", "電能實業": "0006", "富士康國際": "2038",
    "友邦保險": "1299", "恒安國際": "1044", "中國旺旺": "0151", "康師傅控股": "0322",
    "金沙中國": "1928", "昆侖能源": "0135", "中國鋁業": "2600", "聯想集團": "0992",
    "思捷環球": "0330", "銀河娛樂": "0027", "蒙牛乳業": "2319", "中遠太平洋": "1199",
    "領匯房產基金": "0823", "長江實業": "0001", "長和": "0001", "和記黃埔": "0013",
    "長實地產": "1113", "華潤啤酒": "0291", "長江基建": "1038", "瑞聲科技": "2018",
    "利豐": "0494", "吉利汽車": "0175", "萬洲國際": "0288", "九龍倉置業": "1997",
    "國泰航空": "0293", "碧桂園": "2007", "舜宇光學科技": "2382", "九龍倉集團": "0004",
    "石藥集團": "1093", "東亞銀行": "0023", "招商局港口": "0144", "中國生物製藥": "1177",
    "申洲國際": "2313", "創科實業": "0669", "信和置業": "0083", "中國神華": "1088",
    "阿里巴巴": "9988", "小米集團": "1810", "藥明生物": "2269", "太古股份公司'A'": "0019",
    "百威亞太": "1876", "安踏體育": "2020", "美團": "3690", "阿里健康": "0241",
    "龍湖集團": "0960", "海底撈": "6862", "信義光能": "0968", "比亞迪股份": "1211",
    "碧桂園服務": "6098", "交通銀行": "3328", "信義玻璃": "0868", "李寧集團": "2331",
    "招商銀行": "3968", "新奧能源": "2688", "京東集團": "9618", "網易": "9999",
    "農夫山泉": "9633", "東方海外國際": "0316", "中升控股": "0881", "中芯國際": "0981",
    "中國宏橋": "1378", "周大福": "1929", "翰森製藥": "3692", "百度集團": "9888",
    "華潤萬象生活": "1209", "海爾智家": "6690", "紫金礦業": "2899", "京東健康": "6618",
    "攜程集團": "9961", "國藥控股": "1099", "理想汽車": "2015", "藥明康德": "2359",
    "比亞迪電子": "0285", "新世界發展": "0017", "快手": "1024", "新東方": "9901",
    "美的集團": "0300", "中通快遞": "2057", "中國電信": "0728", "京東物流": "2618",
    "泡泡瑪特": "9992", "信達生物": "1801", "恒生銀行": "0011", "寧德時代": "3750",
    "洛陽鉬業": "3993", "老鋪黃金": "6181", "极兔速递": "1519", "極兔速遞": "1519",
    "百濟神州": "6160",
}


def _tables(url: str) -> list[pd.DataFrame]:
    html = requests.get(url, headers=UA, timeout=60).text
    # a few zh tables carry malformed span attributes ("3`"); normalize them
    html = re.sub(r'(colspan|rowspan)="(\d+)[^"]*"', r'\1="\2"', html)
    return pd.read_html(io.StringIO(html))


def _zh_date(s: str) -> pd.Timestamp:
    y, m, d = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s.strip()).groups()
    return pd.Timestamp(int(y), int(m), int(d))


def hsi_events() -> tuple[list[dict], list[tuple[str, int]]]:
    """(events, [(date, size after the change)]) from the zh change table."""
    table = next(t for t in _tables(HSI_PAGE)
                 if {"日期", "剔除", "加入", "成份股數量"} <= set(map(str, t.columns)))
    events, sizes = [], []
    for r in table.itertuples(index=False):
        date = _zh_date(str(r[0]))
        if date < START:
            continue
        sizes.append((date.strftime("%Y-%m-%d"), int(r[3])))
        for action, cell in (("out", r[1]), ("in", r[2])):
            if pd.isna(cell):
                continue
            for name in str(cell).split():
                code = HSI_CODES.get(name)
                if code is None:
                    raise KeyError(f"HSI: no code for {name!r} ({date.date()}); add it to HSI_CODES")
                events.append({"date": date, "action": action, "symbol": f"{code}.HK", "name": name})
    # a rename that keeps the code (out X / in X on one date) is not a change
    df = pd.DataFrame(events)
    key = df.groupby(["date", "symbol"])["action"].transform(lambda a: set(a) == {"in", "out"})
    return df[~key].to_dict("records"), sizes


# ---------------------------------------------------------------------------
# Nikkei 225
# ---------------------------------------------------------------------------

JA_API = "https://ja.wikipedia.org/w/api.php"
N225_TITLE = "日経平均株価"

#: ja-Wikipedia link target -> TSE code, for names listed without a code
#: (the list carried no codes before 2019). Sourced from each company's
#: article infobox; names whose article now redirects to a merged successor
#: are pinned to the code the listed company itself traded under.
N225_CODES = {
    "明治製菓": "2202", "明治乳業": "2261", "アサヒビール": "2502", "宝酒造": "2531",
    "東洋紡績": "3101", "日清紡績": "3105", "三菱レイヨン": "3404", "王子製紙": "3861",
    "三菱製紙": "3864", "北越製紙": "3865", "北越紀州製紙": "3865", "日本製紙グループ本社": "3893",
    "日本曹達": "4041", "東亞合成": "4045", "電気化学工業": "4061", "新日鉱ホールディングス": "5016",
    "新日本石油": "5001", "旭硝子": "5201", "日東紡績": "3110", "日東紡": "3110",
    "新日本製鐵": "5401", "新日鉄住金": "5401", "住友金属工業": "5405", "古河機械金属": "5715",
    "日本軽金属": "5701", "東洋製罐": "5901", "ミネベア": "6479", "東芝": "6502",
    "富士電機ホールディングス": "6504", "明電舎": "6508", "三洋電機": "6764", "ミツミ電機": "6767",
    "クラリオン": "6796", "松下電工": "6991", "パナソニック電工": "6991",
    "スズキ (自動車メーカー)": "7269", "富士重工業": "7270",
    "コニカミノルタホールディングス": "4902", "シチズンホールディングス": "7762",
    "国際石油開発帝石ホールディングス": "1605", "熊谷組": "1861", "ユニー": "8270",
    "ユニーグループ・ホールディングス": "8270", "ユニーファミリーマート・ホールディングス": "8028",
    "横浜銀行": "8332", "みずほ信託銀行": "8404", "住友信託銀行": "8403",
    "中央三井トラスト・ホールディングス": "8309", "新光証券": "8606", "みずほ証券": "8606",
    "損害保険ジャパン": "8755", "三井住友海上グループホールディングス": "8725",
    "平和不動産": "8803", "東急不動産": "8815", "全日本空輸": "9202", "東京電力": "9501",
    "東京瓦斯": "9531", "大阪瓦斯": "9532", "東京ドーム (企業)": "9681",
    "CSKホールディングス": "9737", "CSK_(企業)": "9737", "CSK (企業)": "9737",
    "ヤフー株式会社": "4689", "Yahoo! JAPAN": "4689", "コナミ": "9766",
    "マルハニチロホールディングス": "1334", "JXホールディングス": "5020",
    "NKSJホールディングス": "8630", "損保ジャパン日本興亜ホールディングス": "8630",
    "大日本スクリーン製造": "7735", "第一生命保険": "8750", "日新製鋼ホールディングス": "5413",
}
#: Names whose code changed while the name did not: (name, code before, switch date, code after).
N225_CODE_SWITCH = {"日新製鋼": ("5407", pd.Timestamp("2012-10-01"), "5413")}
#: Link targets that were never constituents (mis-linked or mis-listed names).
N225_IGNORE = {"NI帝人商事"}

_SEC = re.compile(r"^==\s*(?:225銘柄一覧|構成銘柄一覧)\s*==\s*$", re.M)
_LINK = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]")
_ROW = re.compile(r"^\|\s*(\d{3}[0-9A-Z])\s*\|\|(.*)$", re.M)


def n225_revisions(cache: Path | None) -> list[dict]:
    """Every revision of the ja article since 2008-10, oldest first."""
    if cache and (cache / "n225_revisions.json").exists():
        return json.loads((cache / "n225_revisions.json").read_text())
    ids, cont = [], {}
    while True:
        r = requests.get(JA_API, params=dict(
            action="query", prop="revisions", titles=N225_TITLE, rvlimit=500,
            rvprop="ids|timestamp", rvdir="newer", rvstart="2008-10-01T00:00:00Z",
            format="json", formatversion=2, **cont), headers=UA, timeout=60).json()
        ids += [rv["revid"] for rv in r["query"]["pages"][0]["revisions"]]
        if "continue" not in r:
            break
        cont = r["continue"]
    revs = []
    for i in range(0, len(ids), 50):
        r = requests.get(JA_API, params=dict(
            action="query", prop="revisions", revids="|".join(map(str, ids[i:i + 50])),
            rvprop="ids|timestamp|content", rvslots="main", format="json", formatversion=2),
            headers=UA, timeout=120).json()
        for p in r["query"]["pages"]:
            for rv in p["revisions"]:
                revs.append({"ts": rv["timestamp"], "content": rv["slots"]["main"].get("content", "")})
        time.sleep(1)
    revs.sort(key=lambda r: r["ts"])
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
        (cache / "n225_revisions.json").write_text(json.dumps(revs, ensure_ascii=False))
    return revs


def n225_members(text: str) -> dict[str, str | None]:
    """{link target: code or None} from one revision's constituent section."""
    m = _SEC.search(text)
    if not m:
        return {}
    rest = text[m.end():]
    nxt = re.search(r"^==[^=].*==\s*$", rest, re.M)
    sec = rest[: nxt.start()] if nxt else rest
    out: dict[str, str | None] = {}
    for row in _ROW.finditer(sec):
        link = _LINK.search(row.group(2))
        name = link.group(1).strip() if link else row.group(2).split("||")[0].strip()
        out[name] = row.group(1)
    if out:
        return out
    for line in sec.splitlines():
        s = line.strip()
        if s.startswith("*"):
            link = _LINK.search(s)
            if link:
                out[link.group(1).strip()] = None
    return out


def n225_review_dates(years) -> list[pd.Timestamp]:
    out = []
    for y in years:
        months = (4, 10) if y >= 2022 else (10,)
        for mth in months:
            out.append(pd.bdate_range(pd.Timestamp(y, mth, 1), periods=1)[0])
    return out


_MARKS = "＊△▲↓"


def n225_year_table(text: str) -> list[dict]:
    """The article's year-by-year change table: [{year, action, name, marker}].

    `marker` is one of ＊ (merger), △ (delisting), ▲ (special-attention
    designation), ↓ (demotion) — an extraordinary change — or "" for a change
    made at a periodic review."""
    i = text.find("構成銘柄除外")
    if i < 0:
        return []
    sec = text[i: text.find("|}", i)]
    out = []
    for row in re.finditer(r"^\|[^\n]*?(\d{4})年\s*\|\|(.*?)\|\|(.*)$", sec, re.M):
        year = int(row.group(1))
        for action, cell in (("out", row.group(2)), ("in", row.group(3))):
            for item in re.split(r"、", cell):
                item = item.strip()
                if not item:
                    continue
                marker = item[0] if item[0] in _MARKS else ""
                link = _LINK.search(item)
                name = link.group(1).strip() if link else item.lstrip(_MARKS).strip()
                out.append({"year": year, "action": action, "name": name, "marker": marker})
    return out


def _n225_date(ts: pd.Timestamp, entries: list[dict], reviews: list[pd.Timestamp]):
    """Effective date for a change first seen in the list at edit time `ts`.

    The list is often edited late — sometimes months after a review took
    effect — so a change the year table records as periodic is dated to the
    latest review of that table year on or before ts + 45 days (editors also
    update at announcement, ~a month early). An extraordinary change, or one
    the table does not record, keeps the edit date and is approximate."""
    near = [e for e in entries if abs(e["year"] - ts.year) <= 1]
    if near:
        e = min(near, key=lambda e: abs(e["year"] - ts.year) - 0.5 * (e["year"] < ts.year))
        if not e["marker"]:
            year_reviews = [r for r in reviews if r.year == e["year"]]
            before = [r for r in year_reviews if r <= ts + pd.Timedelta(days=45)]
            return (before[-1] if before else year_reviews[0]), False
    return ts.normalize(), True


def n225_events(cache: Path | None) -> list[dict]:
    revs = n225_revisions(cache)
    table_code: dict[str, str] = {}
    snaps: list[tuple[pd.Timestamp, dict[str, str]]] = []
    parsed = [(pd.Timestamp(r["ts"]).tz_localize(None), n225_members(r["content"])) for r in revs]
    for _, m in parsed:
        for name, code in m.items():
            if code:
                table_code.setdefault(name, code)

    def code_for(name: str, when: pd.Timestamp) -> str | None:
        if name in N225_IGNORE:
            return None
        if name in N225_CODE_SWITCH:
            before, switch, after = N225_CODE_SWITCH[name]
            return before if when < switch else after
        return table_code.get(name) or N225_CODES.get(name)

    unknown: set[str] = set()
    for ts, m in parsed:
        if not 222 <= len(m) <= 228:
            continue
        codes: dict[str, str] = {}
        for name, code in m.items():
            c = code or code_for(name, ts)
            if c is None:
                if name not in N225_IGNORE:
                    unknown.add(name)
                continue
            codes.setdefault(c, name)
        snaps.append((ts, codes))
    if unknown:
        raise KeyError(f"N225: no code for {sorted(unknown)}; add them to N225_CODES")

    # A code's membership as a step function over revisions; keep only flips
    # that persist >= 14 days (drops vandalism and half-finished edits).
    all_codes = sorted(set().union(*(set(c) for _, c in snaps)))
    names: dict[str, str] = {}
    for _, c in snaps:
        names.update(c)
    reviews = n225_review_dates(range(2000, 2028))
    history = n225_year_table(revs[-1]["content"])
    table = {}
    for h in history:
        code = code_for(h["name"], pd.Timestamp(h["year"], 7, 1))
        if code:
            table.setdefault((code, h["action"]), []).append(h)
    raw: list[dict] = []
    for code in all_codes:
        state = None
        flips = []
        for ts, c in snaps:
            now = code in c
            if state is None:
                state = now
                continue
            if now != state:
                flips.append((ts, now))
                state = now
        # drop flip pairs that revert within 14 days
        kept: list[tuple[pd.Timestamp, bool]] = []
        for ts, now in flips:
            if kept and kept[-1][1] != now and (ts - kept[-1][0]).days < 14:
                kept.pop()
                continue
            kept.append((ts, now))
        for ts, now in kept:
            action = "in" if now else "out"
            date, approx = _n225_date(ts, table.get((code, action), []), reviews)
            raw.append({"code": code, "action": action, "ts": ts, "date": date, "approx": approx})

    # Nikkei replaces a delisted or merged name at once, with a name the year
    # table lists unmarked, as if it were a periodic change. A "periodic"
    # change edited well away from any review but within 10 days of an
    # extraordinary change of the opposite direction is that replacement: it
    # takes the extraordinary change's date.
    for e in raw:
        if e["approx"] or -45 <= (e["ts"] - e["date"]).days <= 30:
            continue
        pair = [x for x in raw if x["approx"] and x["action"] != e["action"]
                and abs((x["ts"] - e["ts"]).days) <= 10]
        if pair:
            e["date"], e["approx"] = pair[0]["date"], True
    events = []
    for e in raw:
        if e["date"] < START:
            continue
        events.append({
            "date": e["date"], "action": e["action"], "symbol": f"{e['code']}.T",
            "name": names[e["code"]] + (" (approximate)" if e["approx"] else ""),
        })
    return events


# ---------------------------------------------------------------------------

def write_log(path: Path, header: str, events: list[dict]) -> None:
    df = pd.DataFrame(events).sort_values(["date", "action", "symbol"])
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    body = df[["date", "action", "symbol", "name"]].to_csv(index=False)
    path.write_text("".join(f"# {line}\n" for line in header.strip().splitlines()) + body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, default=None, help="cache dir for Wikipedia revisions")
    args = ap.parse_args()
    today = pd.Timestamp.today().strftime("%Y-%m-%d")

    events, sizes = hsi_events()
    write_log(SOURCES / "hsi_changes.csv", f"""
Hang Seng Index constituent changes from 2009 on, from the change table of
https://zh.wikipedia.org/wiki/恒生指數 (retrieved {today}); dates are the effective
dates listed there. Names mapped to HKEX codes by scripts/build_asia_changelogs.py
(HSI_CODES). Index size after each change (the table's 成份股數量 column), used by
the replay test: {json.dumps(sizes)}
""", events)
    print(f"hsi: {len(events)} events")

    events = n225_events(args.cache)
    write_log(SOURCES / "n225_changes.csv", f"""
Nikkei 225 constituent changes from 2009 on, reconstructed from the revision
history of https://ja.wikipedia.org/wiki/日経平均株価 (retrieved {today}): the
constituent list was parsed at every revision (only revisions listing 222-228
names), names mapped to TSE codes, and a change counted once it persisted 14
days. Changes edited within 45 days before / 30 days after a periodic review are
dated to its effective date (first business day of October; from 2022 also of
April); the rest (mergers, delistings, extraordinary replacements) carry the
edit date and are marked "approximate". Method: scripts/build_asia_changelogs.py.
""", events)
    print(f"n225: {len(events)} events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
