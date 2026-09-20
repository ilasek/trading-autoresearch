---
title: "Salience Theory and Stock Prices: Empirical Evidence"
authors: Cosemans, Frehen
year: 2021 (JFE 140(2), 460–483); read from the February 2017 working-paper version
venue: Journal of Financial Economics (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2020.12.012 — version read: https://www.cfr-cologne.de/download/kolloquium/2017/CosemansFrehen.pdf
citations: 159 (Semantic Scholar by DOI, checked 2026-09-20); 223 (Crossref is-referenced-by-count, checked 2026-09-20)
sample_period: 1926–2015 in the version read (CRSP daily); the published 2021 version's sample was not verified and may extend
markets: US only — NYSE, AMEX, NASDAQ
tier: A
validation_overlap: false in the version read (sample ends 2015); UNVERIFIED for the published version
published_post_2018: true
---

Read **in full**, in the authors' **February 2017 working-paper version** hosted on the Centre for
Financial Research Cologne's colloquium mirror. SSRN returned **403** (Cloudflare) and
ScienceDirect returned **403** to both the article and its `pdfft` endpoint, so the published JFE
article was **not read**. Its abstract was retrieved verbatim from RePEc and matches the
working-paper abstract in every claim. Construction details below are attributed to the version
read; the published version's sample may have been extended past 2015, which is why the
`validation_overlap` flag is recorded as unverified rather than false.

Second of three notes from 2026-09-20. Read `2026-09-20-salience-theory-choice-under-risk.md`
first for `σ`, `θ` and `δ`. **Read `2026-09-20-salience-international-replication.md` before
writing a candidate** — it is a hostile Tier-1 replication and it bears directly on whether this
mechanism can exist on a universe like this one.

## Mechanism

Investors form expectations about a stock's future return by looking at its recent daily returns —
but they do not weight those days equally. A day on which the stock's return **stood out against
what the rest of the market did that day** captures attention and is overweighted; an ordinary day
is underweighted. Salience is a property of a *day*, assessed for each stock separately, and the
comparison set is the cross-section on that same day.

The pricing prediction follows from which days get overweighted:

- A stock whose **salient days are its good ones** ("salient upside") has its expected return
  revised upward by salient thinkers, is bid above fundamental value, and therefore earns **lower**
  subsequent returns.
- A stock whose **salient days are its bad ones** ("salient downside") is pushed below fundamental
  value and earns **higher** subsequent returns.

So the predicted relation between the salience measure and next-period returns is **negative**, and
— this is the part that matters for a long-only lab — **the leg with the positive expected return
is the LOW-salience leg**, which is directly tradeable without a short.

Two structural features give the effect a route to prices rather than leaving it an individual
bias. First, salience as constructed depends only on the stock's return and the market's return, not
on any investor-specific quantity, so **the same stock is salient to everyone at once** — demand
distortions are correlated across investors and can move prices. Second, the mispricing persists
only where arbitrage is limited; the paper predicts and reports a stronger effect where limits to
arbitrage are greater.

**Why this is not short-term reversal, in the authors' own framing.** Reversal theories say
investors overreact to *past returns*. Salience theory says investors misperceive *which* past
returns to attend to, conditional on using past returns at all. The measure is explicitly defined
as the **difference between the salience-weighted and the equally-weighted** past daily return, so
the level of the past month's return is differenced out by construction. The discriminating
prediction is sharp: **two stocks with the same one-month return can have very different salience
values**, depending on whether their best and worst days landed on flat market days or on days when
the whole market moved the same way. A big up-day when the market is flat is salient; the same
up-day when the market rallies hard is not.

**Why this is not attention (Barber–Odean), also in the authors' framing, and the two theories
disagree in sign.** The attention hypothesis says retail investors are net buyers of
attention-grabbing stocks — both good and bad news grab attention, so both ends become overpriced
and subsequently reverse. Salience theory says attention is drawn to salient *states*, not salient
*stocks*, so a stock with an attention-grabbing **downside** becomes **under**priced and earns
**higher** returns. Opposite signs on the same stocks: a genuine identifying test rather than a
robustness check.

## Construction recipe

Everything below is computable from a panel of daily closes and needs no other data.

**1. State space.** For stock `i` in month `t`, the states are the **daily returns over the past
month**. Each realised day is one state with known probability `π_s = 1/S_t`, `S_t` = number of
trading days in the month. Require a minimum of **15 daily observations** in the month or drop the
name for that month.

**2. Salience of each day.** With `r_is` the stock's return on day `s` and `r̄_s` the **average
return across all stocks in the market on that same day**:

```
σ(r_is, r̄_s) = |r_is − r̄_s| / (|r_is| + |r̄_s| + θ)
```

**3. Rank and weight.** For each stock separately, rank its `S_t` days in **descending order of
salience**, `k = 1` (most salient) … `k = S_t`. Salience weights, per BGS equation (3) with
`π_s = 1/S_t`:

```
ω_is = δ^k_is / ( (1/S_t) · Σ_s' δ^k_is' )
```

which normalises to `E[ω] = 1`, i.e. `Σ_s ω_is = S_t`.

**4. The measure.**

```
ST_i,t = cov[ ω_is,t , r_is,t ]
       = Σ_s π_s ω_is r_is  −  Σ_s π_s r_is
       = (salience-weighted mean daily return)  −  (equal-weighted mean daily return)
```

Equivalently and more usefully for implementation: `ST = Σ_s (δ^k_is · r_is) / (Σ_s δ^k_is) −
mean(r_i)`. It is a weighted mean minus a plain mean over one month of daily returns. No
regression, no covariance matrix, no fitted parameter.

**5. Parameters.** `θ = 0.1`, `δ = 0.7`, taken from BGS's experimental calibration. Not estimated.

**6. Portfolio.** Monthly rebalance; sort the cross-section into deciles on `ST`; the predicted
long leg is **decile 1 (lowest `ST`)**. The paper reports both equal-weighted and value-weighted
versions of the decile portfolios (see the size caveat below, which is the single most important
thing in this cluster).

**Implementation details the paper fixes and a candidate must too.** Returns are **close-to-close**
(see the open-to-open falsifier below — this is not a free choice). The market benchmark `r̄_s` is
the cross-sectional average return on day `s`; the paper shows results are robust to which market
index is used. Tie-handling among equal-salience days is not discussed in the version read and must
be made **deterministic** here regardless, or this repo's causality check will read the
non-determinism as a peek.

**Variants the paper itself constructs**, all of which change only `r̄_s`:

| Context (`r̄_s` replaced by) | What it tests |
|---|---|
| Cross-sectional market average (baseline) | the theory as stated |
| The stock's **industry** return (48 FF industries, VW or EW) | a narrower, arguably more natural choice set — reported **stronger** at the one-month horizon, but see below |
| The **risk-free rate** | "stock vs. cash" framing instead of "stock vs. other stocks" — reported **weaker** |
| **Zero** (no context) | `σ` collapses to a monotone function of `|r_is|`: a pure magnitude ranking — reported **substantially weaker**, roughly half the baseline slope |

That last row is the theory's own ablation and it is the most valuable line in the paper for this
lab; see "Implementability".

**Longer state spaces.** ST built on daily returns over a quarter or a year, and on monthly returns
over one or five years, all retain the predicted negative sign, with the relation **gradually**
weakening as the window lengthens. The authors pre-commit to the direction of this test: a gradual
decay is consistent with salience plus limited recall, whereas an **abrupt** death past one month
would indicate the measure was only repackaging one-month reversal.

## Robustness evidence (qualitative only)

No dated performance figures are recorded here, per this folder's anti-lookahead rule. What follows
is sign, ordering and survival only.

- **Univariate sorts.** Average returns decline nearly monotonically across `ST` deciles, in the
  predicted direction. The spread survives adjustment for market, size, value, momentum and a
  liquidity factor.
- **Bivariate sorts.** Deciles of `ST` formed *within* deciles of each control (size,
  book-to-market, momentum, Amihud illiquidity, beta, idiosyncratic volatility, short-term
  reversal, skewness measures) keep the predicted sign and remain significant in every case, and
  the near-monotonicity across `ST` deciles survives.
- **Short-term reversal, three separate ways.** (i) The sequential sort on reversal then `ST`
  keeps the effect among stocks with *similar* one-month returns. (ii) Adding the short-term
  reversal factor to the factor model leaves the long-short alpha large and significant.
  (iii) **The skip-month test**: `ST` measured through month `t−1` still predicts month `t+1`
  returns, across every window length, with only a small drop in magnitude. This is the strongest
  of the three and it is a test the lab can replicate.
- **The measure is mechanically correlated with what it must be distinguished from.** The paper
  states plainly that `ST` is positively associated with the contemporaneous monthly return, and
  that extreme-`ST` deciles hold smaller, more illiquid, higher-beta, more skewed names. This is
  a construction fact, not a finding, and it is the reason the controls above are the substance
  of the paper rather than an appendix.
- **The context ablation is ordered and the ordering comes out as predicted**: market context >
  risk-free context > no context. The paper reads this as support for the model, since a theory in
  which mispricing arises from comparison to *other stocks* requires the market context to carry
  the most information.
- **The open-to-open falsifier, which is the sharpest test in the paper.** Retail investors
  observe close-to-close daily returns, so salience should be a close-to-close phenomenon. If
  instead the results reflected overreaction to fundamental news, the choice of daily-return
  convention should not matter. Built on **open-to-open** daily returns over the same window and
  the same subperiod, `ST`'s predictive coefficient is **small, wrong-signed and statistically
  indistinguishable from zero**, while the close-to-close measure over that identical subperiod is
  strongly negative and significant. The authors present this as hard to reconcile with either a
  risk explanation or a news-overreaction explanation.
- **Conditioning.** Stronger where limits to arbitrage are greater (small size, illiquidity, high
  idiosyncratic volatility, low institutional ownership) and in high-sentiment states. Recorded as
  a **mechanism** — where arbitrage is cheap the mispricing should be corrected — not as a regime
  rule to trade.
- **Parameter robustness.** Results are reported robust to alternative `θ` and `δ` values and to
  an alternative salience functional form from the successor BGS paper.
- **The size row, and it is the one that decides this cluster's fate here.** The effect is
  **materially weaker value-weighted than equal-weighted**, and the authors say why in the
  paper's own words: large stocks have lower retail ownership and smaller limits to arbitrage. The
  VW spread is still reported significant. Whether that survives independent international
  replication is the subject of the third note, and the answer there is largely **no**.
- **Rubric rows.** Venue Tier 1, citations healthy in both indices for a paper of this age,
  costs **not modelled** (a Fama–MacBeth and decile-sort paper), multiple testing not formally
  addressed, sample multi-decade but **single market**. The multi-market row is filled by
  Cakici–Zaremba — hostilely. Tier A on the paper's own merits; **the tradeable claim on this
  universe is not Tier A, and should be read off the third note.**

## Implementability here

**In scope with no data problem at all.** `ST` needs one panel: daily closes. This repo has that,
plus the `open` panel needed for the falsifier. The universe average return on day `s` is the
natural `r̄_s`. Monthly formation matches a month-end rebalance. Cost is trivial: one weighted mean
per name per month.

**What is genuinely attractive here, stated precisely:**

1. **Zero estimated parameters.** `θ = 0.1` and `δ = 0.7` come from laboratory experiments. Under
   this folder's candidate #1 triage rule, `ST` is in the same class as equal weighting — nothing
   to overfit, nothing that degrades as the universe/sample ratio worsens. Almost nothing else this
   lab has tried in the behavioural veins has this property.
2. **The long leg is the tradeable leg.** The predicted positive-return side is **low** `ST`
   (salient downsides, underpriced). Long-only does not amputate the profitable half here, which is
   the recurring problem with residual-reversion and most behavioural spreads.
3. **Two free, pre-registerable, ordered falsifiers that do not require a trial**, and both are
   the paper's *own* identifying tests rather than screens this lab invented:
   - **The context ablation.** Compute `ST` three ways — against the cross-sectional mean
     (baseline), against zero (which collapses to a magnitude ranking on `|r|`), and optionally
     against a risk-free proxy. The theory predicts a **strict ordering**: market context must
     carry more cross-sectional information than no context. If the context-free version ranks the
     universe the same way (high rank correlation / high top-N overlap) or predicts at least as
     well, then what is being measured is the **volatility level**, which is the confound this lab
     has now failed on roughly ten occasions. This test costs one holdings-only computation and can
     retire the vein before any candidate file is written.
   - **The open-to-open falsifier.** This repo has `open` and `close` on the same index and
     columns. Build `ST` on open-to-open daily returns and on close-to-close over the identical
     window. The mechanism predicts the **close-to-close version predicts and the open-to-open
     version does not**. This is the rare falsifier where the *null* result is the confirmation,
     and it is exactly the kind of test that cannot be passed by accident. Note the adjacency to
     the 2026-09-18 overnight/intraday work: that session established this lab can decompose the
     daily bar at the session boundary, and this is a second, independent use for the same
     machinery.

**Pitfalls, and they are serious:**

- **`ST` is reversal-adjacent by construction and this lab has already been burned by exactly this
  shape.** `ST` correlates positively with the contemporaneous monthly return; low `ST` therefore
  tilts toward recent losers. The lab's own 2026-09-19 lesson — *when a score is a signed
  combination of two arms, run the trend/artifact screen on each arm separately* — applies with
  full force, and so does the standing residualisation control (rank of 12−1 momentum, rank of
  trailing volatility). The paper's defence is the skip-month test; **run that here before
  believing anything**, and pre-register that a candidate whose excess dies under the
  two-regressor residualisation is dead, as four behavioural scores before it have been.
- **Family slug.** Under `program.md`'s list this is a short-horizon cross-sectional score on
  closes, i.e. **`price-trend` (legacy, capped at 2 trials per session)**. Say so in the candidate
  rather than filing it somewhere more flattering. The ETF/region adaptation below is the version
  with a defensible claim to a different slug.
- **The size objection is fatal on this universe unless addressed.** The effect is a
  limits-to-arbitrage effect, it is weaker value-weighted, and the international replication finds
  it priced essentially only among microcaps. This universe is ~145 **large** global names. Do not
  write a stock-level `ST` candidate without reading the third note and confronting this directly.
- **Survivorship bias cuts the usual way** — single-stock behavioural alpha on current
  constituents deserves extra scepticism, per `program.md`.
- **Turnover.** Monthly rebalance on a decile of ~145 names, with a signal driven by *last
  month's* daily pattern, is a high-turnover construction at 15 bps/side. No source read models
  costs. The turnover gate is the first thing likely to bite.
- **Determinism.** Fix the salience-rank tie-break explicitly.

**The adaptation worth proposing, flagged clearly as unsupported by any source read.** The
microcap objection is about the *population*, not the *measure*. This universe contains **42 ETFs
across 15 regions**, and the salience construction is defined for any choice set: set the states to
the ETF's daily returns and `r̄_s` to the average across the ETF cross-section on that day. That
gives a region/asset-level `ST` on a population where "microcap" is not a meaningful objection, on
instruments where this repo's survivorship bias is weakest, and at a turnover a 42-name book can
plausibly carry. **No source read here tests salience at the index or ETF level**, so this is a
hypothesis with a mechanism and no empirical support, and it should be run on the **scout** track
and labelled as such. The paper's industry-context variant is the nearest thing to evidence that
changing the choice set is legitimate, and it is not evidence for this.

## Related

- `2026-09-20-salience-theory-choice-under-risk.md` — `σ`, `θ`, `δ`, and why the context-free
  ablation collapses to `|r|`.
- `2026-09-20-salience-international-replication.md` — **read before writing a candidate.**
- `notes/2026-09-01-max-lottery-extreme-positive-returns.md` — the sibling prospect-theory score.
  `ST` is explicitly tested against lottery-demand proxies and reported as not explained by them;
  the context-free ablation of `ST` is close to a `MAX`-style object, so this lab's `MAX` results
  are the right prior for what the ablation should look like.
- `notes/2026-09-18-overnight-intraday-return-decomposition.md` and the 2026-09-18 cluster — the
  machinery for the open-to-open falsifier, and a second use for the `open` panel.
- `notes/2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — the residualisation
  control this candidate must survive.
- `experiments/learnings.md`, 2026-09-19: the per-arm identification rule, and the standing record
  that four successive behavioural scores on this universe reduced to momentum plus the volatility
  level. That is the base rate this candidate is fighting.
