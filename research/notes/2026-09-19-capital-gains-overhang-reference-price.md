---
title: "Prospect theory, mental accounting, and momentum — the capital gains overhang"
authors: Grinblatt, Han
year: 2005 (JFE); working-paper version NBER w8734, 2002
venue: Journal of Financial Economics (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2004.10.006
citations: 825 (Crossref is-referenced-by-count, checked 2026-09-19); 211 (OpenAlex, checked 2026-09-19); Semantic Scholar's DOI endpoint returns "not found" for this DOI. Per the session-7 rule on lone low counts, the OpenAlex figure is the outlier here, not the Crossref one — it disagrees with both the venue and the two independent extensions below.
sample_period: July 1962 – December 1996, weekly; the cross-sectional regressions begin July 1967 because the reference price consumes five prior years
markets: US only — NYSE and AMEX ordinary common shares (NASDAQ excluded for dealer double-counting of volume)
tier: B
validation_overlap: false
published_post_2018: false
---

Read **in full** in two versions: the published JFE article from Bing Han's Rotman faculty page
(`www-2.rotman.utoronto.ca/facbios/file/momentum_JFE.pdf`, JFE 78(2), 311–339 — the faculty-page
channel the README recommends, first try) and the NBER working paper w8734 (*The Disposition
Effect and Momentum*, January 2002), whose empirical section is more discursive and is the source
of several construction details quoted below. Where the two differ in wording the published
version governs.

This note opens a mechanism with **zero prior coverage in this folder**: a grep across all 109
notes returned nothing for `capital gain`, `overhang`, `disposition`, or `reference price`. It is
the first of three notes from 2026-09-19 (see *Related*); it supplies the base construction, and
the other two modify it.

## Mechanism

The disposition effect — investors sell winners too readily and hold losers too long — is one of
the most replicated facts in household finance. Shefrin–Statman named it; it has been observed in
experimental markets and in real stock, futures, options and housing markets, and in many
countries. This paper asks what it does to **prices** rather than to portfolios.

Model an asset with two investor types. Rational investors demand the asset in proportion to the
gap between fundamental value `F` and price `P`. Disposition investors' demand carries an extra
term in `(R − P)`, where `R` is a reference price standing in for their cost basis: when the price
is above their basis they are more eager to sell, when below it they hold on. Market clearing
makes the equilibrium price a **convex combination of the fundamental value and the reference
price**, `P = wF + (1−w)R` with `0 < w < 1`.

Two consequences follow, and they are the whole paper:

1. **Underreaction.** Holding the reference price fixed, the price moves only `w` of the way
   toward any news about fundamental value. Even when `F` follows a random walk and is therefore
   unforecastable, `P` is not.
2. **Predictable convergence.** The gap `P − R` closes over time as the reference price updates
   toward the price. The expected return is proportional to the *current* gap:
   `E[(P_t − P_{t−1})/P_{t−1}] = (1−w)·ν_{t−1}·(P_{t−1} − R_{t−1})/P_{t−1}`, with `ν` the turnover
   rate controlling how fast the reference price catches up.

So the predictor is not the past return. It is **the percentage by which today's price exceeds
the aggregate cost basis of the people holding the stock** — the *capital gains overhang*. Past
returns predict returns only to the extent that they proxy for this gap, which is the paper's
central and most aggressive claim.

The authors' own intuition is a horse race between a fundamental-value horse and a slower
reference-price horse. The gap between them is not largest at the start (the leader has not had
time to pull ahead) or at the end (the follower catches up, and the leader's speed is not
persistent); it is largest **somewhere in the middle**. That is the paper's account of why return
continuation is an intermediate-horizon phenomenon rather than a short- or long-horizon one — an
economic story for a fact this lab's `price-trend` work has always taken as given.

## Construction recipe

**The reference price.** Estimate, for each past date, the fraction of shares bought then and
still held now, and weight that date's price by it. Under the assumption that every outstanding
share is equally likely to trade on any date (shares are symmetric, with no memory of their own
history), the fraction of shares bought at `t−n` and untraded since is

```
w_{t−n} = V_{t−n} · Π_{i=1..n−1} [1 − V_{t−n+i}]
```

where `V` is the **turnover ratio** (period share volume ÷ shares outstanding). The reference
price truncates the history at five years and renormalises:

```
R_t = (1/k) · Σ_{n=1..260} { V_{t−n} · Π_{i=1..n−1}[1 − V_{t−n+i}] } · P_{t−n}
k   = Σ_{n=1..260} { V_{t−n} · Π_{i=1..n−1}[1 − V_{t−n+i}] }
```

Read the terms as probabilities: `V_{t−n}` is the chance the share traded at `t−n`, each
bracketed factor is the chance it did not trade at a later date, and the product is the chance
the share's basis *is* the price at `t−n`. The sum is an expected cost basis. Weights decay
**geometrically** with age, so distant prices matter very little; the five-year cutoff is
admittedly arbitrary and is there to make the estimate comparable across the sample.

**The signal.**

```
g_{t−1} = (P_{t−2} − R_{t−1}) / P_{t−2}
```

Theory calls for `P_{t−1}`; the market price is deliberately lagged one extra period to keep
bid-ask bounce out of the regressor. The authors state that results are *stronger* without the
lag and decline to report them for that reason — an unusually clean piece of methodological
self-discipline, and one this repo's own short-horizon work should imitate.

**The test.** Weekly Fama–MacBeth cross-sectional regressions of the week's return on

```
r = a0 + a1·r_{−4:−1} + a2·r_{−52:−5} + a3·r_{−156:−53} + a4·V̄_{−52:−1} + a5·log(mktcap) + a6·g
```

— i.e. the overhang enters alongside short-, intermediate- and long-horizon past returns, average
trailing turnover, and size. The paper's result is about `a2` and `a6` jointly, not `a6` alone.

**Calibration worth keeping.** With constant turnover `V` per period the implied average holding
period is `1/V` periods. The authors note that a constant *weekly* turnover of 1% — roughly their
sample mean — implies an average holding period of about two years. That number is the right way
to choose a decay rate when actual turnover levels are unavailable (see *Implementability*).

**What the signal is made of.** Regressing `g` cross-sectionally on past returns over three
horizons, past turnover over the same three horizons, and size explains about **59%** of its
variation — so roughly two fifths is something else. The signs are interpretable and they are the
construction's whole point: `g` is **increasing in past returns** and **decreasing in past
turnover**, and the turnover effect is strongest at the intermediate horizon. Controlling for past
returns, *a low-volume winner has a larger overhang than a high-volume winner, and a high-volume
loser has a larger capital loss.* Volume is what makes this different from momentum: it decides
**how much of the old basis has been washed out of the register**.

## Robustness evidence (qualitative only)

- **The headline claim.** With `g` in the regression, the intermediate-horizon past-return
  coefficient is no longer significant, while `g` itself is strongly related to future returns
  with the sign the model predicts. The authors' abstract states it plainly: controlling for this
  variable, past returns have no predictability for the cross-section of returns.
- **Subperiod stability.** The sample is split at the early-1980s change in market structure — two
  halves that differ in average returns, liquidity, trading costs and the strength of the size
  effect. The overhang coefficients in the two halves differ by about one standard error and are
  individually significant in both. This is the strongest robustness row in the paper.
- **Size.** Signs and significance are reported (not tabulated) as not drastically altered within
  size quintiles.
- **Truncation.** Using three or seven years of history instead of five leaves the regressions
  about the same.
- **Functional form.** Alternative gain definitions — dividing by `R` instead of `P`, or lagging
  the reference price an extra period — are also significantly related to future returns and also
  knock out intermediate-horizon past returns.
- **Not a volume × return interaction.** Adding the three turnover × past-return interaction
  terms (the Lee–Swaminathan high-volume-loser channel) leaves the overhang coefficient and its
  t-statistic almost unchanged, and those interactions on their own do *not* subsume momentum.
- **Not merely a cross-sectional liquidity difference.** Rebuilding the reference price with each
  firm's *trailing-year average* turnover in place of each period's actual turnover still produces
  a significant coefficient and still removes past returns' predictive power — but in a horse race
  the actual-turnover version subsumes the average-turnover one. **The time series of a stock's own
  volume carries incremental information beyond its liquidity level.** This is the single most
  useful robustness result in the paper for this repo (see below).
- **A conditional structure, not a constant.** The relation is reported as absent in January and
  strongest in December, which the authors attribute to tax-loss selling temporarily switching off
  the disposition demand. Recorded as a *mechanism* — a seasonal modulation of the same parameter —
  not as a calendar rule to trade.
- **Independent extension.** Riley–Summers–Duxbury (2020, *Management Science*; own note) rebuild
  the baseline `g` on daily data over a sample extending two decades past the original and report
  it as a working predictor before adding their own variants. An (2016, *RFS*; own note) likewise
  reproduces the baseline overhang effect before decomposing it. Neither is a hostile replication,
  but both are independent implementations by other authors on longer samples.
- **The adversarial test, and it does not go the paper's way.** Birru (2015, *RFS* 28(7),
  1849–1873, `10.1093/rfs/hhv007`; 61 citations Semantic Scholar / 106 OpenAlex, checked
  2026-09-19) uses investor-level data around stock splits, where inattentive investors fail to
  split-adjust their reference point. **This source is recorded as not read** — closed in OpenAlex
  with `any_repository_has_fulltext: false`, and `academic.oup.com` returned 403 to the PDF URL its
  own index advertises — so only its published abstract is used, verbatim: *"the magnitude is small
  relative to momentum, and momentum remains robustly present among this sample of stocks void of
  the disposition effect. The results suggest that the disposition effect may slow the
  incorporation of news, but not to the extent that it alone explains momentum."* Treat
  Grinblatt–Han's *subsumption* claim as contested and its *predictor* claim as intact.
- **Two rubric rows fail, which is why this is tier B and not tier A.** (i) **Single market.** All
  evidence is US, NYSE+AMEX, with NASDAQ excluded. A peer-reviewed international study exists —
  Zheng, Li & Li (2024), *Journal of Financial Research* 47(1), 211–242, `10.1111/jfir.12341` —
  but it is **not read** (the publisher is closed and the conference mirror `efmaefm.org` fails TLS
  verification through this environment's proxy even with the CA bundle, an eighth distinct refusal
  mode), and its sample period is unverified, so the multi-market row stays open and nothing here
  rests on it. (ii) **Costs are not modeled at all** — the paper contains no transaction-cost
  analysis; it is a Fama–MacBeth regression paper, and the word appears only in a description of
  market history. Also worth recording: **the overhang is absent from Hou–Xue–Zhang's
  *Replicating Anomalies*** — a grep of the full text for `overhang` returns zero across its 452
  anomalies — so the largest replication study in the literature offers this signal neither support
  nor refutation.

## Implementability here

**The blocking constraint, and the way around it.** The weights need **turnover**, i.e. share
volume ÷ shares outstanding. This repo has `aux["volume"]` as a share count and **no shares
outstanding**, so turnover *levels* are unavailable and cross-sectional differences in the decay
rate cannot be recovered. What *is* available is each name's volume path relative to its own
history. Two constructions follow, and they form a designed pair:

- **The candidate.** Set `V_t = v̄ · vol_t / mean_{252}(vol_t)`, clipped into `(0, 1)`, with a
  single constant `v̄` shared across names. This keeps the within-name time variation in volume —
  the part the paper's Table III horse race shows carries incremental predictive power — and fixes
  only the level, which is the part this repo cannot observe. Choose `v̄` from the paper's own
  calibration rather than by search: an average holding period of about two years is `v̄ ≈ 1/504`
  per trading day. Pre-register it.
- **The control.** Set `V_t = v̄` for all `t`. Then the weights are exactly geometric and `R`
  collapses to an **EWMA of past prices with a fixed decay**, so `g = 1 − EWMA(P)/P` is a smooth
  distributed lag of past returns and nothing more. This is the paper's own average-turnover
  variant pushed one step further, and it is the right control precisely because it is the version
  that *should* look like trend. **If the candidate does not beat this control, the volume
  weighting did no work and the signal is trend in costume** — the same designed-pair logic that
  has twice caught trend in costume on this universe.

**Expect high overlap with trend, and screen for it before spending a trial.** The paper's own
decomposition says about 59% of the overhang's cross-sectional variation is past returns, turnover
and size. Run the standing free screen — rank correlation of the candidate's holdings against the
champion's and against the trailing total return — and read a high number as *predicted*, not as a
disqualification; the question is whether the residual two fifths earns anything. The sharper form
of the test is the paper's own: does the overhang **displace** trailing return in a joint ranking,
or merely ride along with it?

**Data-handling notes specific to this engine.**

- `volume` is **not forward-filled** and is NaN on foreign holidays. The principled fill is
  **zero** — no shares changed hands — which makes that day's weight zero and leaves the survival
  product `Π(1 − V)` untouched. This is one of the rare cases where the natural NaN policy is also
  the economically correct one; say so in the journal rather than leaving it to a default.
- `prices` are **USD-adjusted closes**, and the reference price is a weighted average of *the same*
  panel, so `g` is a ratio of two objects on one basis and is a genuine percentage. This is the
  opposite of the 2026-09-18 open/close trap — no imputation is needed — but the reason must be
  checked rather than assumed, since the weights come from a *different* panel (`volume`) whose
  units are native shares. A split changes the share count and the price on the same day, so the
  volume path is on a **native, unadjusted** basis while the price path is adjusted; the paper's
  own market data are split-adjusted throughout, and Riley et al. state they split-adjust prices
  explicitly. Here, an unadjusted volume spike at a split date will misplace weight onto that date.
  Treat it as a known, unfixable defect of the available panels and record it, rather than
  pretending the two panels agree.
- **Five years of history is a pool rule, and this repo's pool rule is already a known confounder.**
  Requiring 1260 prior trading days (Riley et al. relax it to three years) selects on **listing
  age**, which this folder has a note on and the lab has measured as a level effect, and interacts
  with the survivorship-biased constituent list. Whatever the verdict, the breadth comparison must
  be against a **breadth-matched** control or it measures the pool rule.
- **ETFs.** 42 of ~145 instruments are ETFs, whose share counts move through creation and
  redemption rather than through investors changing hands. Both the turnover denominator and the
  disposition story are ill-defined for them. The clean choice is to restrict the sort to single
  names and say so; the alternative — leaving them in — buys breadth at the cost of the mechanism.
- **Cost profile is favourable, unusually.** The reference price is a five-year weighted average,
  so `g` moves slowly and a book sorted on it should have low turnover against a 15 bps/side
  charge. The published tests are weekly, which is not what makes the signal work; a monthly
  rebalance is what Riley et al. use and is the right cadence here.
- **The tradeable side is the long side.** The prediction is that *high* overhang earns more, so a
  long-only book takes the high end. That is worth flagging because this folder's cost work records
  that most of a long-short momentum spread lives on the *short* leg; here the signed prediction
  puts the reachable leg on the side a long-only repo can hold.

**What this is not.** It is not the 52-week high. That signal is a *maximum* of the price path and
this lab has refuted it; the overhang is a *volume-weighted mean* of the path, is decreasing in
turnover, and has a different economic story. Do not treat the earlier refutation as covering this
construction — but do read Riley et al. (own note) first, because their composite reference point
re-introduces the 52-week high as one of its components and is therefore *partly* the refuted
object.

## Related

- `research/notes/2026-09-19-v-shaped-selling-propensity.md` — An (2016), which splits this
  signal into its gain and loss halves and argues the monotone form used here is the wrong
  functional form. **Read it before implementing this one**; it proposes the better candidate.
- `research/notes/2026-09-19-dynamic-reference-point-composite-cgo.md` — Riley–Summers–Duxbury
  (2020), which keeps these weights and replaces the price they are applied to.
- `research/notes/2026-09-01-max-lottery-extreme-positive-returns.md` — the other behavioural sort
  in this folder that is a functional of the past return *distribution* rather than its sum.
- `research/notes/2026-09-13-listing-age-as-a-level-effect.md` and
  `research/notes/2026-09-12-missing-data-and-complete-case-pools.md` — the five-year history
  requirement is exactly the pool rule those two notes are about.
- `experiments/learnings.md` — the 52-week-high refutation (a different functional of the same
  price path, see above), and the standing finding that dispersion and volatility *levels* are this
  universe's survivorship artifact.
