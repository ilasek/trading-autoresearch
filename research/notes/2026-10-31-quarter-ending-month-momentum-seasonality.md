---
title: "The quarter-ending-month concentration of momentum profits — the one price-only construction on the quarter boundary"
authors: Sias (2007); Brown (SSRN working paper, no journal version found)
year: 2007; working paper
venue: Financial Analysts Journal (Tier 1–2, peer-reviewed practitioner journal); SSRN working paper (Tier 4 — unrefereed, uncited)
url: https://doi.org/10.2469/faj.v63.n2.4521 — https://doi.org/10.2139/ssrn.2481042
citations: Sias 70 (Semantic Scholar by DOI, checked 2026-10-31; Crossref `is-referenced-by-count` 41, same date; its own SSRN working-paper version, 10.2139/ssrn.894333, 10 on Crossref). Brown 0 (Crossref by DOI, checked 2026-10-31) — SSRN-only, no journal version located
sample_period: Sias approximately 1984–2004 — NOT verified against full text (the journal abstract says only "the past 20 years"; a secondary summary gives April 1984 – December 2004). Brown's sample is not verified
markets: US stocks only, both sources
tier: B (Sias); C (Brown)
validation_overlap: false
published_post_2018: false
---

**Access note, stated before anything is used.** Neither source was read in full, and this is the
weakest-evidenced note of tonight's four.

- **Sias (2007)** is paywalled at the publisher. `tandfonline.com`'s PDF endpoint returns HTTP 403;
  the CFA Institute landing page returns an HTTP-200 Cloudflare interstitial ("Just a moment…
  Enable JavaScript"); the SSRN working-paper version (`abstract_id=980678`) returns the documented
  403 on its delivery endpoint. What is recorded here comes from **the journal abstract read via
  RePEc** plus two practitioner summaries, and the sample period is explicitly unverified.
- **Brown** is an SSRN working paper with **zero** recorded citations and no located journal
  version; its content here is **second-hand from one practitioner review** of it. It is included
  only because it is the single source found that addresses the capitalisation and
  international-transferability questions this lab's admission criterion asks about, and it is
  flagged Tier C throughout. **Nothing in `SUMMARY.md` should rest on Brown alone.**

Per the folder's anti-lookahead rule, the abstract's headline figures (a per-month momentum return
in quarter-ending versus other months, over its sample) are **not** recorded. The qualitative form
— that the profits concentrate in quarter-ending months by a large multiple — is.

## Mechanism

This is the only source in tonight's set whose construction is **cross-sectional, price-only and
fully invested**, which is exactly the shape the lab's admission criterion asked for. The claim:

> A cross-sectional momentum sort's profits are concentrated in the **third month of each calendar
> quarter** (March, June, September, December), and are small in the other months — with January
> excluded, since the January effect is a separate and well-known object.

Two causes are proposed, and they are *different mechanisms with the same calendar footprint*,
which is the main reason to treat the vein as unidentified rather than merely untested:

1. **Window dressing.** Institutions buy past winners and sell past losers before a reporting date
   so the disclosed holdings list looks good. Because reporting is quarterly, the pressure lands in
   quarter-ending months and pushes winners up and losers down — i.e. it mechanically *adds* to a
   momentum sort in those months and not in others. Sias reports the pattern is stronger for stocks
   with high institutional trading, which is the cross-sectional prediction this story makes.
2. **Tax-loss selling.** Investors sell stocks carrying capital losses to realise them, which
   depresses loser returns. Sias reports the pattern is particularly strong in December, the
   natural tax month. Brown's working paper pushes this further and makes the tax channel primary:
   the profit comes mainly from the **loser leg**, is larger when more stocks carry losses, and —
   per the review — the losses that fuel it tend to arise from reversals earlier in the quarter.

**The two stories differ in three testable ways, and every difference matters here:**

| | Window dressing | Tax-loss selling |
|---|---|---|
| Which leg carries it | Both, winners up and losers down | Mainly the **loser** leg |
| Where in the cross-section | Stocks with heavy institutional trading | Per Brown, **larger-capitalisation** stocks — the review's reading is that investors prefer to realise losses in liquid names |
| Transferability | Reporting cycles are near-universal for institutions | **Depends on a specific national capital-gains regime**; the review notes explicitly that the results need not apply where tax law differs |

Note that Brown's capitalisation prediction is the **opposite** of the pumping literature's
(`notes/2026-10-31-quarter-end-marking-the-close.md`, where the effect is monotone *decreasing* in
capitalisation). That is not necessarily a contradiction — they are different mechanisms — but it
means a measured quarter-ending-month effect on a large-cap panel cannot be attributed to either
without a further test.

## Construction recipe

As far as it can be reconstructed from the abstract and summaries, with the gaps marked:

- **Signal**: a standard cross-sectional momentum sort. The formation lookback is **not verified**;
  the conventional Jegadeesh–Titman form the folder already has a note on is the natural default,
  and the folder's existing construction-mechanics notes supply the skip-month and overlapping-
  portfolio conventions.
- **Calendar conditioning**: an indicator for the **third month of a calendar quarter**, with
  **January excluded** from the comparison set so the January effect does not drive the contrast.
  This is a *month-of-quarter* index, not a day-of-month index — it is a far coarser object than the
  turn-of-month windows in `notes/2026-09-02-turn-of-month-payment-cycle.md`, and much cheaper to
  trade because the boundary is crossed four times a year rather than twelve.
- **Cross-sectional conditioning**: institutional trading intensity (Sias) or the presence of
  accrued capital losses (Brown). **Neither is computable here**: the first needs holdings or trade
  data, the second needs a per-holder cost basis. The price-only fallback — "names whose price is
  below its own trailing high" as a loss proxy — is a *different* signal and is not what either
  source tested.
- **Weighting / rebalance**: not verified. The literature's standard for this kind of claim is
  equal-weighted decile or tercile portfolios rebalanced monthly.
- **The honest version of the construction for a price-only lab**: a fully-invested long-only
  cross-sectional momentum book whose **tilt magnitude** is larger in the third month of each
  quarter and smaller otherwise. Never in cash — that is the whole point of using a cross-sectional
  rather than a timing form, per the lab's v3 arithmetic.

## Robustness evidence (qualitative only)

Weak, and weak in a specific way. Sias is in a refereed journal with a respectable citation count
for a short practitioner-facing article, and its author has a long track record in institutional
trading research — but it is a **single market**, a **single sample**, and the paper is a six-page
article rather than a full robustness study. There is **no replication** of the
quarter-ending-month concentration in the Hou–Xue–Zhang or Jensen–Kelly–Pedersen sense, and this
folder found no multi-market test of it. Brown is unrefereed and uncited.

Worse, the proposed cause is contradicted by better evidence inside tonight's own set:
**`notes/2026-10-31-tape-painting-buying-versus-selling.md` tests the window-dressing hypothesis
directly in institutional trade data and rejects it** — institutions are reported *not* to be more
likely to buy high-past-return stocks or sell low-past-return stocks at quarter- or year-end. That
is a Tier-A, trade-level rejection of the Tier-B, return-level source's primary explanation. The
tension is recorded, not resolved: it is possible that the return pattern is real and the cause is
the tax channel rather than window dressing, and it is possible that the return pattern is a
multiple-testing artefact of the calendar-anomaly literature the folder's own
`notes/2026-08-29-same-calendar-month-seasonality.md` warns about. Nothing in these two sources
separates those.

## Implementability here

**Verdict: the construction clears the criterion's shape test and fails on the lab's own measured
input. Do not spend a trial.** The reasoning is short and it is the most useful thing in this note.

1. **The criterion's three clauses.** (a) **passes** — a month-of-quarter effect is distinct from
   the month-boundary effect and the sources name a quarter-specific institutional reason.
   (b) **passes** — this is a genuinely cross-sectional, fully-invested construction, the only one
   in the vein. (c) **passes in the weak form only** — the *calendar* conditioner needs no outside
   data, but the *cross-sectional* conditioner both sources rely on (institutional trading
   intensity; accrued losses) is not computable here, so what remains implementable is the calendar
   conditioning applied to a plain momentum sort.
2. **And that is where it dies, on a number the lab already has.** A calendar conditioner can only
   concentrate content that exists. On this panel, under v2's own measurement,
   **12−1 momentum's region-matched cross-sectional rank IC is +0.0128 at t = +0.96** — a null
   (`experiments/learnings.md`, the v2 screen whose read-out also covers `rev1m`, `lowidio`,
   `seas`). Conditioning a null on a calendar indicator yields a null on a quarter of the
   observations, with a wider standard error. The `price-trend` family is also capped at 2 trials
   per session and is the legacy family the program explicitly de-prioritised.
3. **The required free screen, if anyone wants to reopen this.** It costs no trial and it is the
   whole question: **measure the cross-sectional rank IC of the momentum signal separately in
   third-months-of-quarter and in other months (January excluded), on train, region-matched.** If
   the third-month IC is not materially above the pooled +0.0128, the vein is closed on this panel
   and should be recorded as closed. This is the *identifying* version of the lab's 2026-10-09/10
   measurement, which conditioned a *residual-reversal* book on the month after a quarter-end — a
   different signal, a different window (after rather than in the boundary month) and a one-sided
   statistic.
4. **Two standing discounts from the sources themselves.** Brown's tax channel is tied to one
   nation's capital-gains rules, and this panel is nine indices across Europe, the US, Japan and
   Hong Kong, whose tax regimes differ — so even on its own terms the effect should be **diluted by
   construction** on a global panel, and a pooled null would be uninformative about the US piece.
   And per the review, most of the profit sits in the **loser leg**, which a long-only book cannot
   access: this is the same "only the cheap side of the residual is tradeable" problem the folder
   has recorded for `statistical-arbitrage`.
5. **A correction the lab owes itself, found while writing this note.** `SUMMARY.md`'s [2026-10-30]
   open question carries a standing discount — *"this lab has already measured same-calendar-month
   seasonality as significantly inverted on this panel (v2), so a source proposing the
   calendar-month version is re-testing a refutation"*. **That claim was withdrawn by the lab on
   2026-10-15**: `learnings.md` records the inverted reading as a *misaligned score*
   (`features.seasonal_same_month_return` published the month that had just ended rather than the
   month a book formed then would hold), and the properly aligned seasonal is a **region-matched
   null** (t +1.78), orthogonal to the misaligned version. So the correct discount on any
   calendar-seasonal source is **"the lab measured a null, not an inversion"** — weaker than the
   open question states, and it should be cited that way from now on. This note's verdict does not
   depend on which version is right; the momentum-IC argument in point 2 is the binding one.

## Related

- `notes/2026-10-31-tape-painting-buying-versus-selling.md` — the Tier-A trade-level rejection of
  this note's primary proposed mechanism. Read that note before treating window dressing as the
  explanation for anything.
- `notes/2026-10-31-quarter-end-marking-the-close.md` — the other quarter-boundary mechanism, with
  the opposite capitalisation gradient.
- `notes/2026-08-29-same-calendar-month-seasonality.md` — Heston–Sadka, and the multiple-testing
  warning that applies to every calendar-anomaly claim including this one.
- `notes/2026-09-02-turn-of-month-payment-cycle.md` — the month boundary; note that this note's
  object is a month-of-quarter index, four boundary crossings a year rather than twelve, which is
  the one respect in which it is cheaper than anything in that note.
- `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md` and
  `notes/2026-08-17-momentum-horizon-echo.md` — the momentum construction this conditioning would
  be applied to.
- `experiments/learnings.md` — the v2 cross-sectional IC read-out that supplies the +0.0128 / t
  +0.96 momentum null, and the 2026-10-15 correction to the inverted-seasonal entry.
