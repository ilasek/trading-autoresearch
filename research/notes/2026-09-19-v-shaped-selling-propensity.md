---
title: "Asset Pricing When Traders Sell Extreme Winners and Losers — the V-shaped disposition effect"
authors: An (Li An)
year: 2016 (RFS 29(3), 823–861); read from the December 2013 working-paper version, "The V-shaped Disposition Effect"
venue: Review of Financial Studies (Tier 1)
url: https://doi.org/10.1093/rfs/hhv060 — version read: http://www.columbia.edu/~la2329/The%20V-shaped%20Disposition%20Effect.pdf
citations: 65 (Semantic Scholar by DOI, checked 2026-09-19); 58 (OpenAlex by DOI, checked 2026-09-19)
sample_period: 1970–2011 in the version read (monthly formation, daily price and volume inputs)
markets: US only (CRSP); institutional-ownership subsamples begin 1980
tier: B
validation_overlap: false
published_post_2018: false
---

Read **in full**, but in the author's **December 2013 working-paper version** hosted on a Columbia
personal page. The published RFS article is closed (`openAccessPdf: CLOSED` on Semantic Scholar)
and was **not read**; its title changed on publication and its sample may have been extended, so
every construction detail below is attributed to the version read and the published version may
differ. Where this note says "the paper", it means the 2013 version.

This is the second of three notes from 2026-09-19 and it is the one that carries a **candidate
book**. Read `2026-09-19-capital-gains-overhang-reference-price.md` first for the base
construction; this note changes its functional form.

## Mechanism

Grinblatt–Han model the disposition effect as a **monotonically increasing** selling propensity:
the larger your gain, the more likely you sell. Ben-David and Hirshleifer, working with
individual-investor trading records, show that this is the wrong shape. The empirical selling
schedule is **V-shaped in profit**: selling probability rises as the magnitude of a gain *or* of a
loss increases, with the minimum near zero profit and the gain arm steeper than the loss arm. The
asymmetry is what reconciles the V with the original stylised fact — because the gain side is
steeper, average selling is still higher for gains than for losses, so the V is *consistent with*
the disposition effect while contradicting the functional form everyone had assumed.

The pricing implication is the paper's contribution. If holders sell harder as `|profit|` grows,
then a stock on which the aggregate holder base sits on **both large unrealized gains and large
unrealized losses** faces heavier selling pressure. Selling pressure temporarily depresses the
price; the price later reverts toward fundamental value. So the prediction is that stocks at
**both extremes** of the overhang distribution earn more subsequently — a **U-shape in the signed
overhang**, not a monotone increasing relation.

That has a sharp corollary the paper makes explicit and this lab should care about: **the loss
side predicts the opposite of momentum.** Momentum says past losers keep losing; this mechanism
says a stock whose holders sit on large unrealized losses is under selling pressure and therefore
cheap. Whatever this signal is, it is not trend wearing a hat — the two make opposite predictions
on half the cross-section. That is an unusually clean identification property for a candidate on
this universe, where the standing failure mode is a new name for an old sort.

The behavioural source is argued to be **belief-based rather than preference-based**. Loss
aversion and realization utility both explain why people avoid realising losses, and both generate
a monotone schedule; neither generates a minimum at zero profit. Belief updating — investors who
have seen a large move in either direction revise and trade — does.

## Construction recipe

Split Grinblatt–Han's overhang into its gain and loss halves, keeping their weights exactly.

```
gain_{t−n} = (P_t − P_{t−n}) / P_t · 1{P_{t−n} ≤ P_t}        # ≥ 0
loss_{t−n} = (P_t − P_{t−n}) / P_t · 1{P_{t−n} >  P_t}        # ≤ 0
ω_{t−n}    = (1/k) · V_{t−n} · Π_{i=1..n−1} [1 − V_{t−n+i}]

Gain_t = Σ_n ω_{t−n} · gain_{t−n}
Loss_t = Σ_n ω_{t−n} · loss_{t−n}
```

with `V` the turnover ratio and `k` the usual normaliser. Three deliberate departures from
Grinblatt–Han: gains and losses are **measured separately** rather than netted; **daily** rather
than weekly past prices are used; and **both** the current price and the purchase prices are
lagged by **10 trading days** to keep bid-ask bounce out — long enough to clear microstructure,
short enough not to miss an effect the investor-level evidence says is strongest at short prior
holding periods. History is truncated at **five years** and the weights over all days (gain days
and loss days together) are renormalised to sum to one.

By construction `Gain_t + Loss_t = CGO_t`, the Grinblatt–Han overhang. The signal is the other
linear combination:

```
VSP_t = Gain_t − 0.2 · Loss_t                                  # Loss ≤ 0, so both terms add
```

The `0.2` encodes the V's asymmetry — the loss arm is about a fifth as steep as the gain arm. The
paper reports that replacing it with 0.1, 0.3 or 0.5 leaves the estimated coefficient's
t-statistic essentially unchanged, so **the asymmetry constant is not a tuning knob and should not
be searched over**; fix it at 0.2 and pre-register it. High `VSP` means large gains *and* large
losses in the holder base, and the prediction is that high `VSP` earns more next month.

**The residualisation is part of the construction, not an afterthought.** Before sorting, the raw
`VSP` (and, for comparison, the raw `CGO`) is replaced by the residual from a cross-sectional
regression on

```
Ret_{t−1},  Ret_{t−12,t−2},  Ret_{t−36,t−13},  log(mktcap),  turnover,  ivol
```

i.e. short-term reversal, momentum, long-term reversal, size, average trailing turnover, and
idiosyncratic volatility. The paper's stated reason for the `ivol` control is exactly this lab's
recurring problem, in the author's own words: *stocks with large unrealized gains and losses are
likely to have high price volatility*, and volatility is independently related to low subsequent
returns. **`VSP` is mechanically a dispersion statistic** — you cannot have a large `|overhang|`
without a large past price move — and the paper treats neutralising it as a precondition for
reading the sort at all, not as a robustness check.

Formation is monthly; sorts are quintiles on the residual; the regression evidence is
Fama–MacBeth. A further decomposition splits each half by prior holding period — **Recent** gain
and loss overhang from purchase prices inside the past year, **Distant** from one to five years
back — with the weights across all four parts normalised to sum to one.

## Robustness evidence (qualitative only)

- **The horse race is the headline.** With `VSP` in the regression, the Grinblatt–Han `CGO` effect
  disappears. The paper's reading: `CGO`'s predictive power was **borrowing** from the V-shape all
  along, because a monotone summary of a V-shaped schedule picks up part of it. This is a direct
  attack on the previous note's signal and it should be read as one.
- **Functional-form stability.** The asymmetry constant can be moved over a wide range with
  essentially no change in significance (above).
- **Horizon.** Predictability is stronger for gains and losses accrued in the **recent** past than
  in the distant past, matching the investor-level finding that the V is sharpest at short prior
  holding periods. A mechanism-consistent gradient, not a free parameter.
- **Asymmetry is stable across subsamples.** The gain effect is reported as three to six times the
  loss effect across groups — consistent with, and independently supportive of, the `0.2`.
- **Speculativeness cuts the right way.** Sorting into subsamples by institutional ownership,
  size, turnover and volatility — each **size-adjusted** first, by taking terciles within
  market-cap deciles and then collapsing, to stop every cut from becoming a size test — the effect
  is stronger among low-institutional-ownership, small, high-turnover and high-volatility stocks.
  That is the prediction if speculative trading drives the V. The paper is honest that a
  limits-to-arbitrage reading fits the same pattern.
- **The subsample result that matters most here, and it is bad news for this repo.** In the
  **high market-capitalisation** subsample the **gain effect completely disappears**; the paper
  concludes the V-shaped disposition effect is most prevalent among middle and small firms. This
  repo's universe is ~145 large global names and ETFs — the cell where half the signal is reported
  absent. Nothing in this note should be imported without that discount in front of it.
- **Rubric rows that fail.** Single market (US). **Costs are not modeled** — the string
  "transaction cost" does not appear in the version read, and the reported strategy results are
  gross. No independent replication of this specific construction was found. The version read is a
  working paper, though the published outlet is Tier 1. Hence tier B despite the venue.
- **Multiple testing.** The paper argues from a pre-specified functional form with one constant,
  not from a search, which is better than most; but it does not conduct a formal multiple-testing
  correction.

## Implementability here

**This is the one construction in tonight's cluster shaped like a portfolio, and it is the one to
run.** The recipe is fully specified, the signal is computable from `prices` plus `aux["volume"]`,
the prediction has a sign, and its identifying test is cheap.

**Sign and side.** High `VSP` → high subsequent return. A long-only book takes the **top** of the
residual `VSP` ranking. The reachable leg is the predicted-positive leg.

**The turnover problem is the same as in the base note and has the same answer.** No shares
outstanding here, so use `V_t = v̄ · vol_t / mean_{252}(vol_t)` clipped into `(0,1)` with a single
pre-registered `v̄` (Grinblatt–Han's own calibration: an average holding period near two years,
`v̄ ≈ 1/504` per trading day). Missing volume on foreign holidays fills to **zero** turnover, which
is both the natural and the correct reading.

**Three pre-registered controls, in this order, before any trial:**

1. **The volatility control, which this family has failed ten times.** `VSP` is a dispersion
   statistic by construction. Compute its rank correlation with trailing realised volatility and
   its top-decile overlap with a plain volatility sort **before** anything else. The paper's own
   repair is the residualisation above — and note it neutralises against `ivol`, momentum,
   reversal, long-term reversal, size and turnover **simultaneously**, which is the folder's
   "residual of a score by regression" operator applied to six regressors at once on a
   145-name cross-section. That is a lot of degrees of freedom for this universe; consider the
   reduced set (trailing return, trailing volatility) and say which was chosen and why.
2. **The identifying test, which is free and is the reason to bother.** The mechanism predicts
   the **loss half** carries a sign *opposite* to momentum. Run `Gain` and `Loss` as two separate
   scores and check the loss half's sign against trailing return. If the loss half simply tracks
   trend, the mechanism has failed here regardless of what the combined book scores — this is the
   analogue of the identifying test the 2026-09-18 candidate failed, and it should be declared in
   advance as a falsifier rather than discovered afterwards.
3. **The breadth control.** Five years of history is a pool rule that selects on listing age and
   interacts with the survivorship-biased constituent list; compare only against a
   breadth-matched control.

**A tension with the lab's own reading, and it runs in both directions.** The 2026-09-18 nightly
found a **U-shape** in a gain/loss-flavoured sort — both bands positive — and read it as a
dispersion object, since on this universe dispersion is the survivorship artifact. An's mechanism
predicts exactly a U-shape in the signed overhang, so the same observation is this literature's
*signature* and the lab's *artifact*. Both readings cannot be dismissed by assertion, and they are
separable: the artifact reading says the U survives collapsing to `|score|` and dies inside a
volatility tercile; the mechanism reading says the **asymmetry** is real (gain arm steeper than
loss arm, by a factor the paper puts at three to six) and survives the volatility neutralisation.
**Test the asymmetry, not the U.** A symmetric U is the artifact; an asymmetric V with the gain
arm steeper is the mechanism. This is the cheapest discriminating measurement in tonight's notes
and it should be run before the trial, not after.

**Expect a smaller effect here than in the source, for a stated reason.** The universe is the
large-cap cell where the paper reports the gain effect vanishing. Do not import an expectation of
magnitude — the folder's standing rule — but *do* import the direction of the discount, because it
is a cross-sectional statement about which stocks the effect lives in, not a period-specific one.

**Cost profile.** `Gain` and `Loss` are five-year weighted averages and move slowly, but the
signal's content is concentrated in the *recent* year, and formation is monthly. Expect higher
turnover than the base `CGO` book and check the drag explicitly against 15 bps/side before
reading the Sharpe.

**ETFs.** As in the base note: creation and redemption make a share-count-based holder register
ill-defined, and the behavioural story is about identifiable holders sitting on gains. Restrict to
single names or state why not.

## Related

- `research/notes/2026-09-19-capital-gains-overhang-reference-price.md` — the base construction,
  which this paper argues is the wrong linear combination of the same two halves.
- `research/notes/2026-09-19-dynamic-reference-point-composite-cgo.md` — the third member of
  tonight's cluster; it changes the *price* the weights are applied to rather than the functional
  form, and the two modifications are independent and composable.
- `research/notes/2026-09-01-max-lottery-extreme-positive-returns.md` — the other note here whose
  signal is a functional of the return *distribution*, and which carries the same
  "is it the volatility level?" identification problem and the same style of answer (an asymmetry
  test that a symmetric-dispersion story cannot pass).
- `research/notes/2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — the
  operator this paper's residualisation step is an instance of.
- `research/notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` — the
  standing question of which characteristics survive in a large-stock universe, which is exactly
  the cell where this paper reports its gain effect disappearing.
- `experiments/learnings.md` — the repeated finding that a cross-sectional *level* of volatility
  is this universe's survivorship artifact, and the 2026-09-18 U-shape result discussed above.
