---
title: "Enhanced Active Equity Strategies" + "20 Myths about Enhanced Active 120–20 Strategies"
authors: Jacobs, Levy
year: 2006, 2007
venue: Journal of Portfolio Management 32(2), 45–55 (venue tier 1 by `research/README.md`'s list) and Financial Analysts Journal 63(4), 19–26 (peer-reviewed practitioner-academic)
url: https://doi.org/10.3905/jpm.2006.628405 and https://doi.org/10.2469/faj.v63.n4.4746
citations: JPM 2006 — 29 (Crossref `is-referenced-by-count`, checked 2026-11-03); 38 (OpenAlex, same date). FAJ 2007 — 28 (Crossref, checked 2026-11-03). Semantic Scholar returned HTTP 429 to every DOI call this session (seventh consecutive session confirming the Crossref-first ordering). Both read in full from the authors' own firm's open article library, `jlem.com/documents/FG/jlem/articles/580177_EnhancedActive.pdf` and `.../580176_20MythsAboutEnhancedActiveStrategies.pdf`.
sample_period: none — both papers are analytical/expository. The only quantities are undated benchmark-weight facts about US equity indices and a hypothetical seven-security exhibit.
markets: US equity benchmarks used as illustration (S&P 500, Russell 1000, Russell 3000)
tier: B
validation_overlap: false
published_post_2018: false
---

First coverage in this folder of `enhanced active` / `130/30` / the attainable-underweight
arithmetic (greps across 255 prior notes: `enhanced active` **0**, `130/30` **0**,
`long-only portfolio optimization` **0**). Taken as the primary for the aim the
[2026-11-02] open-questions entry set: `program.md`'s own sentence *"say how the short leg's
absence is handled"* is a question the folder had never written a note about, and these two
papers are the literature that answers it at the level of portfolio weights rather than of
anomaly returns.

Two sources, one note: same two authors, same framework, the FAJ piece is the objection-by-
objection restatement of the JPM piece.

## Mechanism

**The whole constraint reduces to one inequality.** A long-only portfolio's weight in
security *i* satisfies `w_i >= 0`. Its *active* weight against a benchmark is `w_i - b_i`,
so the constraint is

```
w_i - b_i >= -b_i
```

i.e. **the maximum attainable underweight of any security equals that security's benchmark
weight**, achieved by holding none of it. Overweights have no corresponding bound (short of
a position cap). The constraint is therefore *asymmetric in the information it destroys*: a
long-only book can express an arbitrarily strong positive view and only a bounded negative
one, and the bound is set by the benchmark, not by the signal.

**Why that bound is tight in practice: benchmark concentration.** The papers' arithmetic is
that the bound is small for almost every name in a capitalisation-weighted index. About
**fifteen** securities in the S&P 500, the Russell 1000 and the Russell 3000 alike carry an
index weight above **1%**. Half the S&P 500 sits below **0.10%**, half the Russell 1000
below **0.03%**, and half the Russell 3000 below **0.01%**. So for the median name in a
broad index, "sell everything you hold of it" is a negative active weight of one basis
point — economically indistinguishable from neutral. Insight about overvaluation is, for
most of the cross-section, unexpressible.

**The second-order mechanism, and the one this folder had not written down: the constraint
also caps overweights.** Active weights sum to zero, so every overweight is funded by an
underweight. Jacobs and Levy state the consequence directly: *"not holding these stocks at
all frees only a minuscule amount of capital for overweighting attractive stocks. Instead,
much of the capital for these portfolios' overweighted positions comes from underweighting
an only slightly unattractive stock or a neutrally ranked stock."* Under a concentrated
benchmark the long-only book's implicit bet is therefore **not** "long the top, short the
bottom" but **"long the top, short the middle"** — the funding leg is drawn from names the
signal ranks near-neutral, because those are the only names with enough benchmark weight to
sell. The FAJ paper makes the same point as its Myth 2: a manager wanting a neutral industry
weight must offset overweights with underweights *inside* that industry, and if the
overvalued names there have insignificant benchmark weights the overweight itself becomes
infeasible.

**Why a small relaxation buys a lot.** Because the binding quantity is per-name capital, a
short sleeve equal to 20% of capital can be spread over the names where the bound bites: 80
names underweighted an extra **0.25%** each, or 40 names an extra **0.50%** each. The median
S&P 500 name goes from a 0.10% attainable underweight to 0.35% or 0.60%; the median Russell
3000 name from ~0.01% to 0.26% or 0.51%. The marginal value of the first units of shorting
capacity is high precisely because the long-only bound is near zero for most names — which
is the economic content of the 120–20 / 130–30 class.

**A structural asymmetry that travels with it.** The names that cannot be meaningfully
underweighted are the *small* ones, so the short book of a relaxed-constraint portfolio has
a lower average capitalisation than the benchmark, and the long book must be tilted the same
way to keep net capitalisation exposure neutral. Relaxing the constraint is therefore not a
pure information play; it comes bundled with a size exposure that has to be controlled
explicitly.

## Construction recipe

The papers' prescriptions, stated at the level that matters for construction:

1. **Measure everything as active weight against a stated benchmark.** The benchmark is not
   a performance convention here; it is the object that *defines* the feasible set, since
   `-b_i` is the floor.
2. **Optimise long and short holdings jointly, in one problem, together with the desired
   benchmark exposure.** Jacobs and Levy's Myth 3 is explicit that building a 120–20 as a
   100–0 long-only sleeve plus a separate 20–20 market-neutral sleeve "negates most of the
   advantages": the sleeves cannot see each other's exposures, so the combined book is not
   the optimum of the combined problem. The reusable form of this is a general one — *a
   two-sleeve construction is not the solution of the one-portfolio problem unless the
   sleeves share constraints.*
3. **Control the size and industry exposures of the net book, not of the legs.** The legs
   are individually unrepresentative by construction (previous paragraph); only the whole
   portfolio is comparable to the benchmark.
4. **Charge the relaxation.** The FAJ paper's Myth 8 prices it: a stock loan fee of about
   **50 bps per year on the short notional** (≈10 bps of capital for a 120–20), plus higher
   transaction costs on the larger gross position and a higher management fee. The paper's
   own position is that the strategy is worth it, but it does not pretend the relaxation is
   free, and its Myth 16 says the optimiser should weigh expected trading cost against
   expected active return name by name rather than cap turnover.

## Robustness evidence (qualitative only)

- The weight-bound result is **arithmetic, not empirical** — `w_i >= 0` implies
  `w_i - b_i >= -b_i` with no sample, no estimation and no decay. Nothing in it can fail to
  replicate. The benchmark-concentration facts are index-composition facts of the same kind:
  they vary with the index and over time, but the qualitative statement "the median
  constituent of a broad capitalisation-weighted index has a negligible weight" is stable
  across every such index studied.
- The **performance** claim — that relaxation raises attainable active return — is *not*
  established by these papers. The JPM article's Exhibit 3 is a hypothetical seven-security
  illustration, and for the empirical claim it defers to Clarke, de Silva and Sapra (2004),
  which it cites rather than reproduces. Treat the performance direction as a corollary of
  the arithmetic plus a cited third party, not as this paper's evidence.
- **Methodology-honesty flags, both pointing the same way.** The authors are principals of a
  firm that managed enhanced-active portfolios, and the FAJ paper is framed as the rebuttal
  of twenty objections to that product. The arithmetic is unaffected; the emphasis and the
  choice of which numbers to report are not disinterested. Citation counts are modest (29
  and 28 on Crossref) for papers this old, and neither appears in the replication literature
  (`Hou–Xue–Zhang`, `Jensen–Kelly–Pedersen`) because neither claims a cross-sectional
  anomaly. **Tier B, on venue plus arithmetic, with the performance claim discounted.**

## Implementability here

The lab is long-only with gross leverage ≤ 1.0, so the relaxation these papers sell is
unavailable and nothing here is a candidate. The value is diagnostic, and it comes with one
**correction that has to be made before any of their numbers are quoted in this repo.**

**The correction: their arithmetic is driven by benchmark *concentration*, and this lab's
benchmark is not concentrated.** Protocol v3 scores skill against the **equal-weight
eligible pool** (~1,400 stocks plus 42 ETFs), so every name's benchmark weight is
`1/N ≈ 0.07%`. Per name, that is the Russell 3000 case — the attainable underweight is
seven basis points. But the *aggregate* is completely different, and the difference inverts
the papers' conclusion:

- Excluding `k` of `N` equally weighted names frees exactly `k/N` of capital. A book holding
  20 names at 5% each has active weights `+4.93%` on 20 names and `-0.0714%` on 1,380 names;
  the underweights sum to **98.6%** and fund the overweights exactly. **A long-only book on
  an equal-weight pool can run a ~99% active position.** Jacobs and Levy's "not holding
  these stocks frees only a minuscule amount of capital" is a *capitalisation-weighted*
  statement and **does not transfer to this lab**; neither does their "long the top, short
  the middle" funding story, because here dropping the bottom genuinely does fund the top.
- **What does transfer is a resolution limit, not a capital limit.** Every excluded name
  receives exactly the same active weight, `-1/N`. The ranking is usable above the inclusion
  threshold and **quantised to one bit below it** (in or out). That is the precise sense in
  which the short leg's absence binds here, and it is a different statement from the one this
  folder has been carrying.

**The reusable rule, and it is sharper than the discount the folder already has.** A score is
reachable on this panel **iff its information is in identifying the best names**, and
unreachable **iff its information is in ordering the bad ones** — because the book cannot
distinguish bad from worse at all, at any weighting. This is a construction-level reason for
a shape the lab has now measured repeatedly ("real, large, significant, and structurally
unreachable": 5–10 day reversal, regional neutralisation, the whole `calendar` half of
`seasonality-calendar`, the ETF-versus-constituent asymmetry that "sits on the leg long-only
cannot reach").

**Three free screens follow, none of which costs a trial** (all on train/validation only,
never the holdout):

1. **Top-minus-pool versus pool-minus-bottom.** For any score the lab already has, compare
   the top band's mean excess over the equal-weight pool against the pool's mean excess over
   the bottom band. The first is the reachable half. This is the return-side screen the
   `2026-09-22-anomaly-profits-short-leg-asymmetry.md` note already proposed; this note
   supplies the *weights-side* reason it is the right screen.
2. **The one-bit truncation test, which is new.** Recompute the score's rank IC after
   collapsing everything below the book's inclusion threshold to a single value
   (`score_trunc = max(rank, threshold)`). If the IC largely survives, the score's content is
   in the top and the long-only constraint costs little. If the IC collapses, the score's
   content was in the ordering of names the book will never hold, and **no weighting scheme
   can recover it** — refuse the candidate before writing it rather than after measuring it.
   This is strictly more informative than (1), because a score can have a flat top and a
   steep bottom while still showing a spread.
3. **Check what the funding leg is.** Report, for any proposed book, the sum of underweights
   and which score band supplies it. On an equal-weight benchmark this should be the bottom
   of the ranking; if a construction ends up funding its overweights out of mid-ranked names
   (because of a position cap, a sector constraint or a turnover buffer), it has
   re-imported the cap-weighted pathology by accident.

**Two cautions.**

- **Do not import their magnitudes.** The 0.10% / 0.03% / 0.01% median weights are index
  facts about benchmarks this lab does not use, and the 0.35% / 0.60% augmented underweights
  describe a 120–20 structure it cannot run. The transferable content is the inequality and
  the resolution argument.
- **Their size asymmetry runs *against* this panel, and must be stated as a gradient.** The
  names they say "cannot be meaningfully underweighted" are small ones — exactly the names
  a point-in-time large-cap index-member panel excludes by construction. Per the
  [2026-11-02] documentation correction, the honest form is **"the gradient of this argument
  runs against this panel"**, not "the constraint does not bite here": the resolution limit
  in the previous paragraph is panel-independent, and only the *capitalisation* half of their
  story weakens.

## Related

- `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md` — Stambaugh–Yu–Yuan: the
  *return-side* version of the same problem (the short leg carries most of an anomaly's
  abnormal return). That note supplies the discount; this one supplies the mechanism in
  weights, and the equal-weight correction above says the discount's usual justification
  ("you cannot free capital") is not the one that applies here.
- `notes/2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` and
  `notes/2026-09-23-spanning-under-short-sales-and-costs.md` — why the unreachable leg is
  systematically the one with more mispricing, and the econometrics of testing spanning when
  short sales are constrained.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — carries the transfer
  coefficient `IR ≈ TC · IC · √BR` and explicitly flags that **Clarke, de Silva and Thorley
  (2002) was not read first-hand**. That is still true after this session: FAJ 58(5), 48–66,
  `10.2469/faj.v58.n5.2468`, **197 Crossref / 252 OpenAlex citations**, resolves as
  `oa_status: closed, any_repository_has_fulltext: false`, and no repository copy was found.
  Its companion, **Clarke, de Silva and Sapra (2004)**, *JPM* 31(1), 54–63 — the paper
  Jacobs and Levy cite for the empirical version of their claim — is likewise closed, and
  the only text obtained this session was the **CFA Digest editorial summary** (May 2005,
  pp. 63–65, read from `hillsdaleinv.com`). Flagged second-hand, not first-hand, and
  recorded here rather than given its own note for that reason: the summary states a
  transfer coefficient of **0.332** with the full constraint set imposed, rising to **0.678**
  when the long-only constraint alone is relaxed, versus 0.471 for the market-cap
  constraint and 0.42 for industry-plus-sector — i.e. **the long-only constraint is the
  single most expensive constraint in that exercise, roughly doubling TC when removed** —
  and that the gain is largely captured by modest shorting rather than requiring a full
  long–short book. Those numbers are the summariser's, from a tracking-error-relative
  S&P 500 exercise, and should not be quoted in this repo as a measured quantity or carried
  into a Sharpe-based gate; a session with access to the article should replace this
  paragraph with a first-hand note.
- `experiments/learnings.md` — the lab's own instances of the shape this note explains:
  "real, large, significant, and structurally unreachable" (2026-08-31, 2026-09-01), and the
  long-only market component that the five correlated family leads share.
