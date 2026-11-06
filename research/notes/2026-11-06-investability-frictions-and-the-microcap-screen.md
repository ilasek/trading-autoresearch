---
title: "What You See is Not What You Get: The Costs of Trading Market Anomalies"
authors: Patton, Weller
year: 2020
venue: Journal of Financial Economics 137(2), 515–549 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2020.02.012 · full text read from https://public.econ.duke.edu/~ap172/Patton_Weller_MF_28nov18.pdf
citations: 78 (Crossref `is-referenced-by-count`, checked 2026-11-06)
sample_period: January 1970 – December 2016, with a July 1993 – December 2016 subsample (post-Jegadeesh–Titman)
markets: US — CRSP common stocks and all US domestic equity mutual funds
tier: A — tier-1 venue, full text read, a 47-year sample, a method whose whole subject is implementation cost, and an explicit placebo (the value-weighted market) run against its own headline
validation_overlap: false (sample ends 2016-12)
published_post_2018: true (JFE 2020; the working-paper version read here is dated November 2018)
read: full text, author-hosted working paper (3.6 MB PDF → 220 KB of clean text, 908 instances of `" the "`, zero `( )` dropout, title line verified)
---

## Access

`public.econ.duke.edu/~ap172/<Author1>_<Author2>_MF_28nov18.pdf` served the complete working
paper on the first try. This is the 2026-09-18 faculty-page lesson again, with one reusable
specific: the filename encodes **both surnames plus a date**, not a title slug, so the path is
guessable from a search result but not from the title alone. The published JFE version is closed;
nothing below depends on it, and the working paper carries the full method, all tables and the
appendices.

**Note on the DOI.** The citation count above is for the published article. A DOI guessed from
the JFE pattern for this paper resolved to a *different* JFE article of the same volume year — the
2026-10-07 "never guess a legacy Elsevier DOI" lesson holding for a *modern* Elsevier DOI too. The
correct DOI came from a search result and was then confirmed against Crossref by title.

## Mechanism

This note is not about an anomaly. It is about **what the choice of investable universe does to a
measured cross-sectional effect**, and it is the first source in this folder that treats the
universe restriction as a *priced constraint* rather than as a sample-selection footnote.

The paper's framing is the useful part. A screen that removes names from the opportunity set is
not a transaction cost; it is a **shadow cost** — "analogous to the shadow price on a constraint on
which stocks can be included in a portfolio." It is invisible to every cost model that prices
*trades*, because it prices *trades that were never available*. This repo's cost model (per-name
liquidity tiers plus statutory taxes, protocol v3) is entirely of the trade-pricing kind, so this
shadow cost is structurally outside it and will never show up in a trial's reported cost figure.

The reason the screen bites on *returns* rather than merely on breadth is the interaction the
authors name explicitly: the highest returns to the characteristics studied are earned in the
smallest names, and those names are simultaneously the ones too small to absorb real money. So the
screen is not a random thinning of the cross-section — it is **correlated with the effect being
measured**, and it removes the part of the cross-section where the effect lives. The authors
attribute the concentration itself to limits to arbitrage: effects survive in the "dusty corners"
precisely because arbitrageurs cannot work there.

The method is worth recording independently of the universe result, because it is a general
technique this folder has no other instance of. Rather than model costs from microstructure, the
authors **extend Fama–MacBeth regressions to run on two sets of assets at once** — stock portfolios
and mutual funds — with separate cross-sectional slopes for each, and read the implementation cost
off the *difference in slopes* on the same factor exposures. That is an "all-in" cost estimate: it
requires no parametric microstructure model and no commitment to a particular factor trading
strategy, and it prices everything that separates a paper portfolio from a real one, the universe
restriction included.

## Construction recipe

The construction that matters here is the **screen**, not a strategy.

- **Microcap definition** (followed from Fama–French 2008 and Hou–Xue–Zhang): a stock whose market
  capitalisation is below the **20th percentile of NYSE market capitalisation**. Note the
  percentile is taken on **NYSE names only** and then applied to the whole cross-section, which is
  what makes it a severe screen on *count* and a mild one on *value*.
- **Implementation of the screen**: drop the smallest-size portfolios from double sorts of
  size × value, size × beta, size × prior return, and size × Amihud illiquidity. So the screen is
  applied inside each sort, leaving the rest of the characteristic spread intact.
- **The structural fact to carry, and it is the single most transferable number in the paper**:
  this exclusion removes **about a fifth of the portfolios but only about 3% of total market
  capitalisation**. A capitalisation-based screen is therefore enormously asymmetric between the two
  things it removes — most of the *names*, almost none of the *value*.
- **Weighting**: the microcap-exclusion tables are reported **value-weighted only**, deliberately,
  "because we are interested in downweighting tiny stocks to reflect the investable universe." The
  paper reports both equal- and value-weighted results elsewhere, and the equal-weighted estimates
  of the gap are uniformly the larger ones.
- **Placebo**: the same exclusion applied to replicating the value-weighted market changes the
  result by at most a few basis points. A universe screen should move a characteristic premium and
  *not* move the market, and the authors check that it does not.

## Robustness evidence (qualitative only)

- **The screen moves the measured premium in the expected direction, and does not close the gap.**
  Excluding microcaps lowers the measured compensation to both the value and the prior-return
  characteristics. The reduction is real and statistically visible, but the gap between the
  non-microcap stock portfolios and the funds remains large and statistically robust. So the
  universe restriction is **part** of the explanation for why paper effects are not realised, not
  the whole of it.
- **Decomposition shares** (these are shares of a gap, not returns, and are recorded here for that
  reason): the narrowing of the investable universe accounts for roughly **one third** of the
  implementation gap for the value characteristic and roughly **one sixth** for the prior-return
  characteristic. The ordering is the robust part — the universe screen explains about twice as
  much of value's shortfall as of momentum's.
- **Asymmetry across characteristics is stable across subsamples for value and roughly halves for
  momentum** in the later subsample. The authors read this as echoing Fama–French (2012) and
  Israel–Moskowitz (2013), both of which this folder already holds.
- **Long-only is not an escape, and this is the result most directly aimed at this lab.** The
  authors run long-only versions of the factors as well as long-short tilts, and conclude that
  "the implementation costs of 'long only' versions of standard factors are significant and
  comparable to short-side costs." About half of the all-in cost of the value and prior-return
  factors traces to the inability to short — which means **the other half survives in a long-only
  book**. Dropping the short leg removes roughly half of a cost, not the cost.
- **Methodology honesty**: the authors address omitted-strategy bias directly by splitting funds on
  the R² of their own factor regressions, cite Oster (2017) on coefficient stability as the relevant
  diagnostic, and report where their estimates are only marginally significant rather than rounding
  them up.
- **Single market.** US only, stocks and US domestic equity funds. The multi-market rubric row is
  open for this source, and the companion note on the illiquidity premium
  (`2026-11-06-illiquidity-premium-and-where-the-size-screen-sits.md`) is where the 45-country
  evidence on the same screen sits.

## Implementability here

**State the protocol and the panel: this is about protocol v3 on the v2 panel.**

1. **This repo's panel is a far more aggressive screen than the one measured here, and in the same
   direction.** The microcap screen studied is "below the 20th NYSE percentile". This lab's panel is
   the ever-members of **nine large-cap national indices** — a screen that sits well above that
   threshold and removes not merely microcaps but most of the small- and mid-cap cross-section. So
   the one-third / one-sixth decomposition shares above are a **lower bound** on what this panel's
   construction does to a measured characteristic premium, not an estimate of it. Any claim in this
   folder of the form "the effect is attenuated on a large-cap panel" now has a source and a
   direction, and the honest version of the claim is that the attenuation is **larger here than
   anything this paper measured**.
2. **The 3%-of-capitalisation fact resolves a confusion this folder has been at risk of.** It is
   tempting to argue that because a large-cap panel holds nearly all of the market's *value*, it
   holds nearly all of the measurable cross-sectional effect. This paper says the opposite and shows
   why: the names carrying the effect are the ones carrying almost none of the value. **Breadth in
   capitalisation terms is not breadth in signal terms**, and the v2 panel's ~1,000 eligible names
   are wide in count while being narrow in exactly the dimension that matters.
3. **The shadow-cost framing is the actionable import, and it is a warning about reading trial
   output.** A v3 trial reports a cost figure built from liquidity tiers and taxes. That figure
   prices the trades the candidate made. It does not and cannot price the names the panel never
   offered. So **a candidate that looks cheap in a trial's cost accounting may still be paying the
   larger of the two costs**, and the lab has no instrument that would show it. This is not a
   reason to change the cost model; it is a reason not to read a low reported cost as evidence that
   implementation is cheap on this panel.
4. **The long-only half-of-the-cost result cuts against an optimistic reading available in this
   folder.** `2026-11-03-which-leg-arbitrage-capital-trades.md` and the long-only vein
   (`#373`–`#380`) establish that the short leg carries most of the *profit*. It would be natural to
   infer that the long-only constraint at least buys cheapness in exchange. This paper measures that
   trade directly and the answer is that it buys **about half** of the cost reduction — long-only
   implementation costs remain significant and comparable to short-side costs. The two findings
   together are worse than either alone: a long-only book forgoes most of the profit and keeps about
   half of the cost.
5. **The method is not implementable here and should not be attempted.** The two-asset-set
   Fama–MacBeth comparison needs a panel of *fund* returns. This repo has none and cannot fetch any.
   Record the technique as a reading aid, not as a candidate.
6. **One free diagnostic does follow, and it is cheap.** The paper's placebo logic inverts into a
   screen on this repo's own panel: a candidate whose skill against the equal-weight eligible pool
   is driven by the *smallest eligible names* is a candidate whose measured edge lives in the part
   of the cross-section this panel barely represents and the next panel revision may remove. Ranking
   a candidate's active return contribution by the eligible names' own trailing dollar-volume tier —
   data a v3 trial already has — says whether that is the case, costs no trial, and is a property of
   the candidate rather than of the holdout.

**Known pitfalls.** (a) Do not import the decomposition shares as effect sizes; they are shares of
a gap measured on a US fund panel, and this folder's standing rule against importing performance
expectations applies to them. (b) The equal-weighted estimates are the larger ones throughout, and
this repo's benchmark pool is **equal-weight**, so the relevant comparison is the one that makes the
gap look worse, not better. (c) The paper's microcap screen and this panel's index screen are both
capitalisation screens but they are not the same object — the former is a percentile cut, the latter
is an index committee's rule, and
`2026-11-06-index-membership-is-not-an-information-free-selection.md` is the note on why that
difference matters.

## Related

- `2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — Hou–Xue–Zhang, whose microcap
  definition this paper adopts; the pessimistic half of the replication pair.
- `2026-09-02-anomalies-by-size-group.md` — Fama–French (2008), the source of both the 20th-NYSE-
  percentile convention and the 3%-of-capitalisation fact.
- `2026-09-06-long-side-share-of-anomaly-profits.md` — Israel–Moskowitz, cited here for the
  size-dependence of the value premium.
- `2026-11-03-no-short-constraint-cost-and-panel-breadth.md`,
  `2026-11-03-which-leg-arbitrage-capital-trades.md`,
  `2026-11-03-attainable-underweight-and-the-long-only-constraint.md` — the long-only vein that
  point 4 above sharpens.
- `2026-11-06-illiquidity-premium-and-where-the-size-screen-sits.md` — the multi-market evidence on
  the same screen, and where the threshold's location turns out to decide the answer.
- `2026-11-06-index-membership-is-not-an-information-free-selection.md` — what an index rule selects
  for, over and above size.
- `2026-10-08-benchmark-portfolios-have-alpha-of-their-own.md` — the companion point that the
  benchmark's own construction carries a tilt; under v3 the benchmark is the equal-weight eligible
  pool, so both notes bear on the same measured number.
