---
title: "Lost in the multiverse: Methodological uncertainty in studying global equity returns" — read for how much of a country-level result is the research design, and specifically for what happens when the design is pinned at this lab's two settings
authors: Cakici, Fieberg, Neszveda, Piljak, Zaremba
year: 2026
venue: Journal of Banking and Finance (peer-reviewed field journal; not one of the rubric's named tier-1 outlets)
url: https://doi.org/10.1016/j.jbankfin.2026.107775
citations: 0 (Crossref `is-referenced-by-count`, checked 2026-11-02). The article is recent, so this is an age artefact and not a quality signal; it is nevertheless the reason the tier below is B rather than A. Semantic Scholar returned HTTP 429 on six spaced attempts and was not resolved; OpenAlex was not spent on a count.
sample_period: 1973-01 – 2022-12, monthly
markets: country equity markets, up to ~70 depending on data source; six alternative representations of a "country" — CRSP/Compustat aggregates, Datastream indices, MSCI indices, GFD indices, iShares single-country ETFs, and index futures
tier: B
validation_overlap: true
published_post_2018: true
read: full text of the version of record (CC BY), fetched from the University of Vaasa repository. **Access note:** the repository's advertised `osuva.uwasa.fi/bitstreams/<uuid>/download` path returned **HTTP 200 with a 353 KB HTML login page** ("Sisäänkirjautuminen"), while the DSpace REST path `osuva.uwasa.fi/server/api/core/bitstreams/<uuid>/content` served the genuine 3.97 MB PDF (→ 212 KB of clean text, 702 instances of `" the "`, zero `( )` dropout, no ASCII shift). The bitstream UUID came from `/server/api/core/bundles/<uuid>/bitstreams`.
---

## Mechanism

This is not a source of a mechanism. It is a source about **how much of any country-level
mechanism is an artefact of the choices made while measuring it**, and it is in this folder
because the session that opened the country-index vein needed something to grade that vein
against.

The design: take 15 return-predictive country characteristics from the literature, turn each
into a long-short country allocation strategy, and then vary **nine** methodological decisions —
data source, geographic scope, study period, hyperinflation treatment, number of portfolios,
portfolio weighting, rebalancing frequency, minimum portfolio size, and implementation lag. The
cross-product is **13,824 distinct research designs**, benchmarked against a systematic review of
52 published studies to establish which choices are the common ones. This is the
"nonstandard errors" / multiverse-analysis method applied to a literature whose cross-section is
small enough that design choices should bite harder than they do at the firm level.

The economically substantive finding — the one that is a claim about markets rather than about
method — is that **country-level return predictability is concentrated in small, illiquid,
partially segmented markets**, and that every design choice which raises the weight of such
markets raises measured performance while every choice which lowers it lowers measured
performance. The authors' own framing is that designs with broad, equal- or rank-weighted
exposure "may overstate the premia available in large, liquid, and directly investable markets."

## Construction recipe

Not a construction source, but two definitions are worth carrying because they are precise and
this folder had neither:

- **`StMom` (short-term momentum), the country-level signal that survives:** total return in the
  **previous month (t-1)**, sorted **High-minus-Low** — i.e. **continuation**, not reversal. The
  authors are explicit that at the country level this is momentum "rather than reversal", which
  is the opposite sign to the one-month effect in the stock cross-section.
- **`LtMom` (the baseline country momentum):** total return over months **t-12 to t-2**, the
  standard skip-a-month 12-1 construction.

The other 13 signals, for the record, are world-market beta, idiosyncratic volatility, sovereign
rating, 52-week high (price at t-1 over the max over t-12..t-2), moving average (price at t-1
over the mean over t-12..t-2), dividend yield, earnings-to-price, long-run reversal (return over
t-60..t-13, Low-minus-High), same-calendar-month seasonality over the past 20 years, market size,
issuance, and two further risk measures. Of these, only `StMom`, `LtMom`, `H52`, `MA`, `LtRev`
and `Seas` are computable from prices alone.

**Two tests beyond the design sweep.** A block bootstrap over the "mean of the means" across all
designs, resampling with replacement while preserving cross-sectional dependence across designs;
and an out-of-sample design-selection procedure that ranks implementations by past performance
and asks whether the historically best designs keep paying.

## Robustness evidence (qualitative only)

Everything below is a **cross-design contrast or elasticity**, which is what this source is for.
No dated performance level is recorded, and nothing from the post-2023 world appears — the sample
ends 2022-12.

- **Most country-level patterns are fragile.** Across the multiverse, most characteristics
  produce significant spread-portfolio profits in only a **modest minority of implementations,
  typically not above 15–20%** — and that includes the most prominent ones. Momentum, beta and
  idiosyncratic risk specifically "fail to confirm their significance across research designs".
- **Only four signals survive both the bootstrap and the out-of-sample design selection:**
  **sovereign rating, short-term momentum, dividend yield, and market size**, with market size the
  most reliable. Of those four, **only short-term momentum is computable from price alone** —
  sovereign rating and dividend yield need non-price data and market size needs capitalisation.
- **The single most influential decision is the data source, and the instrument this lab would
  actually trade is the worst one.** Representing countries by **ETFs or index futures** rather
  than by full-market index aggregates **reduces mean spread returns by roughly 0.13–0.16
  percentage points per month in the regression** (the ETF coefficient runs about −0.13 / −0.14 /
  −0.16 across the three specifications and is significant in all three), and the authors state
  the payoffs are **two to three times lower** than for CRSP/Compustat aggregates. Their
  explanation is coverage, not tracking error: futures and ETFs hold large liquid stocks, while
  the full-market aggregates include the small and micro-cap names that are "the primary source
  of return predictability."
- **The second most influential decision is geographic scope, and this lab is pinned at the worse
  end of that one too.** Restricting the sample to **developed markets** yields average spread
  returns **statistically indistinguishable from zero**, with roughly half the pooled Sharpe;
  including emerging markets roughly doubles both, and a non-developed-only sample raises them
  further. The regression coefficient on "developed only" is about −0.13 pp/month. **Honest
  caveat the paper states itself:** this scope effect is significant in **univariate** regressions
  and **vanishes in multivariate** ones, because data source and sample length already absorb it.
  So scope and data source are substantially the *same* finding seen twice, not two independent
  penalties to add together — do not stack them naively.
- **Weighting matters in the same direction.** Value-weighting "almost wipes out all gains";
  equal-weighting and rank-weighting raise them (incremental effects of roughly +0.05 and +0.06
  pp/month). Again the channel is exposure to small markets.
- **What does *not* matter:** hyperinflation treatment, minimum portfolio size, and the number of
  portfolios have little effect on the conclusions; finer sorts raise mean returns slightly but
  leave Sharpe ratios flat, because the extra spread is paid for in lost diversification.
- **The one geographic finding that points the other way, and it must not be suppressed:** while
  dividend yield and size patterns are strongest in samples including emerging and frontier
  markets, **"momentum effects prevail in developed countries."** So momentum is fragile overall
  at the country level, but its *localisation* runs toward exactly the markets this lab's panel
  contains, opposite to the other signals.
- **Methodological uncertainty is real but not catastrophic.** Nonstandard errors exceed standard
  errors by roughly 19%–59% depending on method — substantial, yet **lower** than the equivalent
  figure in stock, futures and cryptocurrency studies. ETF-based designs carry **higher**
  nonstandard errors than Compustat- or Datastream-based ones, so the ETF route is both
  lower-payoff and noisier.
- **The gaps.** **No transaction costs are modelled anywhere** — a grep of the full text returns
  zero mentions of transaction or trading costs — so every number is gross, and the near-zero
  developed-market result is a *pre-cost* near-zero. The study is also entirely **long-short**;
  no long-leg-only breakout is reported, which is the breakout a long-only lab most needs.
  Finally it is a single (very large) study, unreplicated, with no citation record yet. Hence
  Tier B despite an unusually honest design.

## Implementability here

This source implements nothing. Its use is as a **discount**, and the discount is specific and
large.

**This lab's panel sits at the intersection of the two most damaging design choices the paper
identifies.** The country-level instruments available here are **single-country ETFs** (the
data-source setting worth roughly −0.13 to −0.16 pp/month) drawn from **nine large-cap developed
national indices** (the scope setting worth roughly −0.13 pp/month univariate). Because the paper
shows those two are largely the same effect measured twice, the right reading is not "add them"
but "**this panel is the worst case for country-level cross-sectional predictability, and the
paper measured that case directly rather than leaving it to analogy.**" That is a materially
stronger statement than the folder's usual hedge that "a null on a large-cap panel would be
uninformative": here the literature has actually run the large-cap, ETF-instrument version and
found it near zero before costs.

**What survives the discount.** Exactly one thing, and it is the same thing
`2026-11-02-country-index-momentum-and-the-currency-component.md` arrives at independently:
**short-horizon country-index continuation.** `StMom` is one of only four signals robust to the
full multiverse plus a bootstrap plus out-of-sample design selection; it is the only one of the
four computable from prices; and the paper's own geographic result says momentum is the signal
whose country-level effect leans *developed*. Two independent sources with different samples,
different methods and 26 years between them converge on short-horizon index continuation and on
nothing else.

**What is refused, and should be recorded as an anti-candidate.** The 12-1 country momentum
book (`LtMom`), country-level beta and idiosyncratic-volatility books, and country value/size
books — the first three for failing the multiverse, the last because dividend yield, market size
and sovereign rating all need data this repo does not have and all localise to emerging and
frontier markets this panel excludes by construction. Also refused: any argument of the form
"country rotation is a fresh family, so the lab's `+0.06` gross ceiling does not apply to it."
This paper is the reason that argument fails — the fresh family was measured in the lab's own
instrument class and scope and came back near zero gross.

**One caution about using this note as a refusal.** The paper's unit is a **long-short spread**,
and `2026-11-02-country-index-momentum-and-the-currency-component.md` finds the country-index
effect lives almost entirely in the **long leg**. A long-short spread can be near zero while its
long half is not. Nothing here measures that, so this source cannot by itself refuse a long-only
construction — it can only refuse the spread. Say which one is being refused.

## Related

- `2026-11-02-country-index-momentum-and-the-currency-component.md` — the constructive half of
  the same session; agrees on short-horizon continuation and on value-weighting shrinking
  country effects, disagrees on the ETF instrument, and is the source of the long-leg caveat
  above.
- `2026-11-02-winner-loser-reversals-in-national-indices.md` — reaches the same
  small-market-localisation conclusion from a 1997 Tier-A source, 29 years earlier and by an
  entirely different route.
- `2026-11-01-reproduction-versus-replication-open-source.md`,
  `2026-11-01-weak-identification-of-t-stat-hurdles.md`,
  `2026-08-25-hierarchical-bayesian-factor-replication.md`,
  `2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` (Hou–Xue–Zhang) — the
  replication cluster, which `SUMMARY.md` records as
  **closed**. This note is not a fifth source in it: its unit is a *research design*, not a
  *factor*, and its subject is the country cross-section rather than the firm one. It does,
  however, corroborate `#359` from the lab's other side — no replication-rate or fragility
  estimate in this literature models transaction costs either.
- `experiments/learnings.md` — the ETF-sleeve entries. Those measured *static diversified
  sleeves* under v1 and are not in tension with this note, which is about cross-sectional
  country selection.
