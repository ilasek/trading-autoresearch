---
title: "The equal-weight tilt in managed portfolios"
authors: Hanke, Keswani, Quigley, Stolin, Zagonov
year: 2019
venue: "Economics Letters 182, 59–63 — venue tier 2 (peer-reviewed, Elsevier, but a short-paper outlet below the JF/JFE/RFS/JFQA/ManSci/JPM tier; four pages of text, tables referenced but compressed)"
url: https://doi.org/10.1016/j.econlet.2019.06.003 · accepted manuscript read in full at https://openaccess.city.ac.uk/id/eprint/22338/1/The%20equal-weight%20tilt%20in%20managed%20portfolios.pdf
citations: "6 (Crossref is-referenced-by-count, checked 2026-10-13). OpenAlex and Semantic Scholar were not spent on it — Semantic Scholar's title endpoint was already returning 429 this session and OpenAlex's daily budget is small (research/README.md). Six citations is low in absolute terms and the tier below reflects that"
sample_period: "factor returns tabulated 1980–2009; the mutual-fund panel is CRSP Mutual Fund Database funds assigned to broad US benchmarks by Petajisto's (2013) classification"
markets: US only — the S&P 500 universe for the factor, and 1,229 US mutual funds benchmarked against the S&P 500 (of 1,432 broad-benchmark funds) for the fund regressions
tier: "B — peer-reviewed, read in full, cost-aware in an unusually concrete way, and its central construction is so simple it cannot be the product of specification search; but a single market, a single index universe, one fund database, only six citations, and no replication located. Treat the *measurement* (how much of managed-fund return variation the tilt accounts for) as the finding and the venue as the discount"
validation_overlap: false
published_post_2018: true
---

## Access

Read in full as the **accepted manuscript** from City St George's institutional repository
(`openaccess.city.ac.uk`), 195 KB, `pdftotext -layout` into 35 KB of clean text, `( )`-dropout
check zero. **This is the second time this repository has served this folder a closed-journal
accepted manuscript** — `notes/2026-08-22-rebalancing-return-attribution-critique.md` came from
the same host — which makes it a confirmed-twice channel rather than a lucky hit. The published
version of record was not opened; the accepted manuscript carries the full argument, all section
structure and the reference list, and the tables are referenced in-text with their key numbers
restated in the prose, which is what is used below.

## Mechanism

The paper's object is the **tilt toward equal weights as a systematic factor**, and its
contribution is to argue that this tilt belongs in the list of things you strip out before
calling anything alpha. That list is the familiar one — market, size, value, momentum,
liquidity, beta, quality, profitability — and the argument for adding one more member is the
same argument that put each of the others there: *it is pervasive, it is cheaply obtainable
passively, and it explains fund returns.*

The factor is one line:

> **EMV = (return on the equal-weighted universe) − (return on the value-weighted universe)**,
> both over the same index membership.

The economic content is **not** a risk premium and the authors do not claim one. It is the
diversification return — the growth benefit that accrues to a diversified book rebalanced to
constant weights — and they cite the whole chain the folder already holds for it (Fernholz &
Shay 1982; Booth & Fama 1992; Plyakha, Uppal & Vilkov; Greene & Rakowski 2015; Banner et al.
2018), with the standard two-asset illustration: a 50/50 book of one asset that doubles then
halves and another that does the reverse returns zero if held and earns a positive
"diversification return" if rebalanced annually. They say out loud what that example depends
on: *"this example is characterized by a strong return reversal, raising valid questions about
its generalizability."*

Three mechanism-level results, all transferable:

1. **The tilt is not a corner case of active management; it is the default.** An active book
   is either more concentrated than the capitalisation-weighted market or more diversified than
   it, and *being more diversified than a cap-weighted index is, mechanically, a tilt toward
   equal weights.* So any manager who diversifies away from the market — deliberately or as a
   side effect of stock selection — picks up EMV exposure. Their fund regressions bear this out:
   the average fund's EMV loading is **about a quarter** (coefficient ≈ 0.246), i.e. *the average
   fund's diversification goes about a quarter of the way from cap weights toward equal weights.*
2. **The tilt is close to orthogonal to the standard factor set.** Regressing EMV on market,
   size, value, momentum, liquidity, beta, quality and profitability leaves **roughly 44% of its
   variation unexplained**. It is significantly related to most of them — it would be odd if a
   small-and-cheap tilt were not — but it is not a repackaging of any of them.
3. **It explains managed-fund returns better than any factor except the market.** Two
   measurements, in the authors' own framing:
   - *Incremental over a one-factor market model:* adding EMV cuts average residual variance by
     **14.9%**, comparable to size (17.0%) and value (17.8%) and far above the other five
     (2.3%–9.9%).
   - *Leave-one-out of the full nine-factor model* — the comparison they call the more relevant
     one: dropping EMV raises the unexplained portion of variance by **7.85%**, more than any
     factor other than the market (momentum is next at 6.45%). EMV's `t`-statistic exceeds 30 in
     the nine-factor model.
   None of these are performance figures; they are explanatory-power statistics, which is why
   they are recorded here while the paper's return numbers are not.

One further mechanism, offered as a conjecture by the authors and worth keeping because it is
testable and because it predicts *where* the tilt comes from: a manager acting on **noisy
signals** will tilt toward equal weights automatically if signal precision is itself tilted that
way — and it is, in part because analyst coverage of a stock is "much less than proportional to
the stock's market value". That is the same mechanism as
`notes/2026-09-13-analyst-coverage-and-the-speed-of-bad-news.md`, arriving at a weighting
consequence rather than a momentum one.

## Construction recipe

1. **The factor.** Long the equal-weighted portfolio of an index's members, short the
   value-weighted portfolio of the same members, rebalanced on the index's own grid. The authors
   deliberately use the **S&P 500** universe rather than a broader one so that both legs are
   cheaply investable — the factor's claim to be a *performance-evaluation* control rests on its
   being obtainable at ETF cost, unlike momentum, which "requires expensive shorting of
   distressed stocks and high turnover costs".
2. **Why the short leg is nearly free in practice.** In an evaluation regression the short leg is
   offset by the market loading, so replicating an average fund's EMV exposure means holding
   `(β_MKT − β_EMV)` units of a cap-weighted index fund and `β_EMV` units of an equal-weighted
   index fund — two long positions, no shorting. The implementation cost of the tilt is the
   *difference in expense ratios between an equal-weight and a cap-weight index fund*, plus the
   equal-weight index's own turnover. That turnover is modest: the official quarterly-rebalanced
   S&P 500 equal-weight index's reported annual turnover sits in the **mid-20-percent range**
   (they cite Zeng & Luo 2013).
3. **The evaluation model.** `R_it − RF_t = α_i + β_MKT·MKT + β_SMB·SMB + β_HML·HML + β_UMD·UMD
   + β_LIQ·LIQ + β_BAB·BAB + β_QMJ·QMJ + β_PMU·PMU + β_EMV·EMV + e_it`, estimated fund by fund,
   with coefficients and `t`-statistics averaged across funds, and explanatory power reported
   both as the incremental R² over the market model and as the leave-one-out contribution to the
   full model's R².
4. **The conditioning variable, which the paper names but does not test.** The relative
   performance of a diversified rebalanced book against a cap-weighted one depends on **the
   diversification return minus the drift in market concentration** (Fernholz 1998; Hanke &
   Quigley 2014): when the market becomes more concentrated, that drift offsets and can overwhelm
   the diversification return. Their defence is only an asymptotic one — "the market cannot
   concentrate forever" — which is a statement about the long run and not about any sample.
5. **Persistence, which is the one piece of dynamics they report.** EMV's 12-month
   autocorrelation is the only one among the nine factors anywhere near conventional
   significance (p ≈ 0.054), from which they infer that funds' diversification returns are
   themselves persistent. One market, one sample, one lag — a lead, not a result.

## Robustness evidence (qualitative only)

- **Simplicity as a defence against the folder's own multiple-testing discount.** The authors
  invoke Harvey–Liu–Zhu explicitly: EMV has no parameters, no breakpoints, no rank bands, no
  skip month, no winsorisation. There is nothing in it to tune, so the
  `notes/2026-09-09-specification-curve-analysis.md` and
  `notes/2026-08-24-multiple-testing-haircut.md` discounts bite less hard here than on a sorted
  anomaly. That argument is sound and it is the main reason this note is Tier B rather than C.
- **What is not robust.** One country, one index, one fund database, one sample vintage. No
  international evidence, no subperiod table in the accepted manuscript, no replication located,
  and the fund results are net of management fees but gross of loads. The conclusion itself
  concedes the paper "does not investigate the reasons why so many actively managed funds have a
  significant EMV tilt".
- **The dependence their own illustration admits.** Their worked example works *because* it is
  built from a strong relative-price reversal, which is exactly the condition
  `notes/2026-08-22-rebalancing-return-attribution-critique.md` proves is **necessary** for
  rebalancing trades to have positive expected value. The paper does not test whether that
  condition holds in its sample; it assumes the diversification-return literature settled it.
- **No cost charged on the active side.** Costs appear only as expense ratios of the two index
  products. Nothing in this paper prices the tilt under per-name liquidity tiers or transaction
  taxes.

## Implementability here

- **EMV is not constructible on this panel, and that is the first finding to record.** The short
  leg needs capitalisation weights; the panel has no share counts and no fundamentals. As in
  tonight's companion note: `dollar_volume` is a liquidity measure, not a size measure, and
  substituting it would rename the hypothesis rather than test it. So **the EW-vs-VW axis is
  closed here by data, not by evidence** — no candidate can be written on it, and a null on it
  would be uninformative.
- **The consequential reading is about the lab's own scoreboard, and it is sharp.** Under v3 the
  benchmark is the **equal-weight** eligible pool. The lab has therefore, by construction, set
  its null to the single tilt this paper measures as the most pervasive non-market exposure in
  professionally managed equity money. Three consequences:
  1. **Skill against the equal-weight pool is a strictly harder statistic than alpha against the
     cap-weighted market**, and harder by an amount this literature says is the largest single
     non-market factor contribution in managed-fund returns. A candidate scoring zero skill here
     would, on this evidence, still have carried a tilt that explains more of real funds' returns
     than momentum does. **This is a reason to read the lab's near-zero v3 skill numbers as a
     statement about the benchmark, not only about the signals.**
  2. **Any construction operator whose effect is "hold more names, more evenly" buys nothing
     measurable under v3**, because the benchmark already is that operator at its limit. The
     lab's de-concentration instinct (built under v1's Sharpe-versus-zero bar, and already
     flagged by `SUMMARY.md` #234 on different grounds) is now doubly suspect: #234 says
     anchoring compresses the measured difference; this note says the specific anchor the lab
     chose is the one portfolio that monopolises the diversification return. **Concentration, or
     a genuinely non-weight-like signal, is what can move the statistic.**
  3. **A candidate that is equal-weighted over a subset of the pool is, in factor terms, long
     EMV over its subset and short it over the complement.** Its measured skill is then mostly
     about *selection*, with the weighting channel netted out — which is the right way round,
     and worth saying because it means a selection signal is not disadvantaged by being equally
     weighted inside the book. Equal weighting inside a book is the *neutral* choice under this
     benchmark, not a bet.
- **The one testable residue, free and on the train split only.** The paper's conditioning
  variable is the drift in universe concentration. The lab cannot compute capitalisation
  concentration, but it *can* compute the concentration of its own benchmark's realised risk
  contributions, for which the folder already holds four measures
  (`notes/2026-10-06-absorption-ratio-eigenvalue-concentration.md`,
  `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`). Whether the
  eligible pool's effective breadth trends over the train split is a one-pass diagnostic, it
  belongs in the census pass `SUMMARY.md` already schedules, and it bounds how much of the
  pool's own return is a concentration drift rather than anything a candidate competes with.
- **Carry nothing numeric across.** 14.9%, 7.85% and 0.246 are properties of US mutual funds
  benchmarked to one index in one sample. They are recorded as evidence that the tilt is
  *pervasive and near-orthogonal*, which is a qualitative claim, and for nothing else.

## Related

- `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` — tonight's companion and
  this paper's own motivating citation; the source of the tilt-versus-rebalancing split.
- `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the adversarial algebra. This
  paper's worked example silently satisfies that paper's necessary condition and never says so.
- `notes/2026-08-21-diversification-return-and-rebalancing.md`,
  `notes/2026-08-22-excess-growth-and-return-decomposition.md` — the identity and its
  continuous-time form; the lab has already measured the latter's `γ*` as a null on this
  universe.
- `notes/2026-10-08-benchmark-portfolios-have-alpha-of-their-own.md` — the closest prior note in
  spirit: benchmarks are not neutral objects. That note is about index benchmarks having factor
  alpha; this one is about the *weighting scheme* of a benchmark being a factor in its own right.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — `1/N` against optimisation, a different
  question from `1/N` against capitalisation.
- `notes/2026-09-13-analyst-coverage-and-the-speed-of-bad-news.md` — the coverage-asymmetry
  mechanism the authors conjecture as the source of managers' tilt.
- `research/SUMMARY.md` candidate ideas #217 (what the pool's own maintenance costs), #234
  (anchoring compresses the measured statistic — same conclusion, independent route).
