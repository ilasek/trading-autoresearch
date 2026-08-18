---
title: "Low-Risk Investing without Industry Bets"
authors: Asness, Frazzini, Pedersen
year: 2014
venue: Financial Analysts Journal 70(4), 24–41 (venue tier 1)
url: https://doi.org/10.2469/faj.v70.n4.1
citations: 82 (Semantic Scholar, checked 2026-08-18)
sample_period: US 1926–2012 (BAB returns from April 1929); global 1986–2012 (BAB returns from January 1988)
markets: 57,441 stocks across 24 developed markets; 49 Fama–French industries in the US, 73 GICS industries globally
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The low-risk effect is the observation, going back to Black–Jensen–Scholes (1972), that the
empirical security market line is **too flat** relative to the CAPM: safe stocks earn more
than the model predicts and risky stocks earn less. The proposed economic cause is
**leverage aversion / funding constraints**. An investor who wants more expected return than
the market offers but cannot (or will not) borrow must get it by holding high-beta assets
instead. That bids up high-beta prices and depresses their expected returns, leaving a
premium on the low-beta end that only a *levered* investor can harvest. The premium
therefore survives precisely because arbitraging it requires the leverage most investors
lack — which is a structural, not behavioural, story.

This note was chased for one specific reason: `learnings.md` closes the low-vol family on
this universe "absent a genuinely different vol construction (e.g. sector-neutralized, not
raw trailing)", and this paper is the literature's dedicated treatment of exactly that
construction. Its target claim is that low-risk investing is *not* merely a bet on stodgy
industries. The authors decompose the effect into an industry-selection component and a
within-industry stock-selection component and find **both work**, with the industry-neutral
version realizing the higher Sharpe ratio in both the US and global samples, and delivering
positive returns in every one of the 49 US industries and in most of the 70 global ones.

The paper also offers a mechanism for *why* the industry-neutral version is the stronger
one, and it is the leverage story applied one level down: hedging out industry risk makes
the strategy more hedged, and a more-hedged strategy needs **more notional exposure per
unit of volatility**. The authors report that the industry-neutral portfolios have higher
`($Long + $Short)/Volatility` than the industry version, and read the ordering as
confirmation of the leverage-constraint model — the harder a bet is to fund, the better it
pays. Keep that inference in view when reading the implementability section below: the
paper's own explanation for the best variant is that it demands the most leverage.

## Construction recipe

**Beta estimation** (following Frazzini–Pedersen 2014), stated in full because a later note
in this folder attacks precisely this step:

```
β_i^ts = ρ_i · (σ_i / σ_m)
```

with `σ_i`, `σ_m` estimated as **one-year daily** standard deviations and `ρ_i` as a
**rolling five-year correlation of three-day (overlapping) returns**. Three-day returns are
used to blunt nonsynchronous trading across markets; the longer correlation horizon is
justified on the grounds that correlations move more slowly than volatilities. Betas are
then shrunk Vasicek-style toward the cross-sectional mean of 1:

```
β_i = 0.6 · β_i^ts + 0.4 · 1
```

Shrinkage does not change the ranks (all sorts are ordinal); it only changes the leverage
applied to the legs.

**Standard BAB.** At each calendar month end, rank all securities in ascending beta. Split
at the country median: below → low-beta portfolio, above → high-beta portfolio. Within each
leg, weight by **beta rank distance from the mean rank**, not by beta itself (explicitly to
limit the influence of data errors and extreme values). With `z` the rank vector and `z̄`
the mean rank,

```
w_H = k (z − z̄)⁺ ,  w_L = k (z − z̄)⁻ ,  k = 2 / |1ᵀ(z − z̄)|
```

so each leg's weights sum to 1. The factor is then made market-neutral **by leverage**: the
low-beta leg is levered up to beta 1 and the high-beta leg de-levered to beta 1, and the
factor is their difference. Rebalanced monthly.

**Industry-neutral BAB.** Run the identical construction *within* each industry (a stock is
"high beta" if its beta is above the median for its industry within its country), producing
one self-financing zero-beta BAB per industry, then aggregate:
`BAB_Intra = Σ_j w_j · BAB_j`. Four aggregation schemes are all reported and all work:
equal weight, value weight (lagged industry market cap), name weight (stock count), and
**equal risk weight** — rescale each industry BAB to a 10% ex ante annualized volatility at
formation, then equal-weight the rescaled portfolios.

**Industry BAB.** Build value-weighted industry portfolios, then apply the same BAB
construction across those industry portfolios. Globally, do it per country first and then
value-weight countries, so the factor is country-neutral.

**One construction detail worth stealing, from the cost section.** In the tradable
large-cap subsample the authors reduce turnover by **averaging each stock's portfolio
weight over the past 12 months**, described as a simple version of transaction-cost
optimisation. That is structurally the champion's overlapping-tranche mechanism (a trailing
average of target-weight vectors) appearing in a tier-1 source — but note carefully that it
is framed here purely as a *cost* technique, so this is one more source that does **not**
make the lab's temporal-breadth *return* claim.

## Robustness evidence (qualitative only)

- Positive returns in **every one of the 49 US industries** for the industry-neutral BAB, and
  in the large majority of the 70 global industries.
- Positive in every 20-year US subperiod since 1929 and every global subperiod examined; the
  industry BAB is the weaker of the two and fails in one US subperiod.
- Present in **both small-cap and large-cap** subsamples, US and global. This is the single
  most important robustness claim for this repo and it is directly contradicted by the
  replication note below — see `2026-08-18-defensive-equity-replication-and-construction.md`.
  Note also that the large-cap alphas are visibly the weaker of the two size splits in every
  column, i.e. even on the paper's own evidence the effect thins toward large caps.
- Industry exposures are real but partial: regressing BAB weights on industry dummies gives
  an average monthly R² of about 25% (versus about 10% for a book-to-price factor), so
  industries explain a nontrivial but minority share of the holdings. The long tilts are the
  intuitive defensives (utilities, banks, retail, food, tobacco); the short tilts are
  cyclicals (autos, steel, machinery, transport).
- Not a value bet: the industry-neutral versions carry very low and sometimes **negative**
  HML loadings, which is a genuine rebuttal of the "low-risk is repackaged value" claim.
- Costs are modelled, using market-impact functions estimated from live institutional
  trading data, and the authors report net returns and breakeven cost levels rather than
  gross only. This is the methodology-honesty item that keeps the source at tier A.
- Known contested ground: the *interpretation* of the residual alpha. Both papers in the
  companion note argue the effect is explained by profitability/size/valuation exposures the
  four-factor model used here does not contain, and that the construction itself is doing
  work the paper does not attribute to it.

## Implementability here

**Verdict: not implementable as specified, and the paper's own mechanism explains why —
this is a third instance of the standing "which leg / what does it need?" screen, and the
first where the blocker is leverage rather than the short side.**

Four blockers, in order of severity:

1. **The long leg is defined by leverage.** BAB's low-beta leg is levered *up to beta 1*.
   That is not decoration — it is what converts a low-beta basket's modest raw return into
   the factor's headline result, and it is the direct expression of the economic mechanism
   (you get paid because you must borrow to take this bet). Gross leverage ≤ 1.0 removes
   exactly this. An unlevered long-only low-beta basket is not a weakened BAB; it is the
   thing BAB says is *cheap to hold and therefore low-returning* — the asset the constrained
   investor already owns. This is the family's version of the pattern already recorded twice
   in `SUMMARY.md`: the published object's payoff lives in a leg or a lever this repo cannot
   own.
2. **It is long–short, and the paper's own subperiod table shows both legs contribute.**
   Unlike momentum crash-risk management (where the mechanism lived entirely in the short
   leg), here the US long side carries significant standalone alpha, so a long-only
   translation is not *empty* — but that alpha is measured on the **levered** leg, which
   returns us to blocker 1, and the global long-side alphas are not significant.
3. **The industry-neutral variant, the best one, is the most leverage-hungry.** The paper's
   explanation for its superiority is that it requires more notional per unit of risk. So
   the specific construction this repo was told to look for is the one whose advantage is
   least accessible under a leverage cap.
4. **Universe.** The repo's ~145 instruments are large, liquid, global names — the size
   bucket where this paper's own results are weakest and where the companion note argues
   they are absent.

**What is worth adapting, and how far.** The one genuinely portable idea is the
*neutralisation layer*, separated from the low-risk signal it is applied to. The paper's
useful structural result is that a within-group version of a cross-sectional bet can beat
the ungrouped version, by removing a common exposure that the raw sort loads on
incidentally. The lab has tested that shape once — sector-neutralizing the composite
momentum z-score — and it **lost badly** (Sharpe 1.03 → 0.87, turnover up). That is a
tension worth stating rather than smoothing: this source says group-neutralisation helps,
the lab measured it hurting. The honest reconciliation is that they are neutralising
different things for different reasons. AFP neutralise a signal (beta) that is
*mechanically* correlated with industry membership — utilities are low-beta as a category —
so the group tilt is a confound to be removed. The lab's momentum z-score is not
mechanically industry-linked in that way, and the pruning-style result already on record
says top-momentum names already span sectors; there the group constraint only discards
information. **Screen to carry: neutralise a group exposure only when the signal is
mechanically confounded with the grouping, not as a general diversification reflex.**

**Pitfalls if anyone revisits this anyway.** (a) Rank weighting within the leg is not a
neutral detail — see the companion note, where it is the single largest driver of the
published result. (b) The beta estimator here is *not* a regression beta and mixes two
different horizons; the companion note shows what that mixture actually measures. (c) Do
not import the "equal risk weight" aggregation as an endorsement of inverse-vol weighting:
it is applied across ~49–70 *comparably diversified* industry sub-factors, which is
precisely the condition the lab's two inverse-vol refutations violated — see
`2026-08-18-risk-parity-equal-risk-contribution.md` for why that distinction is the whole
ballgame.

## Related

- `2026-08-18-defensive-equity-replication-and-construction.md` — the tier-1 replication
  challenge to this literature; read the two together, they disagree.
- `2026-08-18-risk-parity-equal-risk-contribution.md` — the equal-risk-weight aggregation
  used here, and the condition under which it is the right thing to do.
- `2026-08-17-momentum-crash-risk-management.md` — the first "the mechanism lives in a leg
  you cannot own" case; this is the third.
- `2026-08-17-naive-vs-optimized-weighting.md` — rank weighting versus estimated weighting.
- `experiments/learnings.md` — "Low-vol stock tilt is refuted, standalone and as a
  within-momentum filter", and the sector-neutral momentum trial that lost 0.16 of Sharpe.
