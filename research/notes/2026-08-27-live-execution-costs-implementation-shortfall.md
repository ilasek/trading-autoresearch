---
title: "Trading Costs"
authors: Frazzini, Israel, Moskowitz
year: 2018
venue: working paper (AQR / SSRN, tier 3 by venue but tier-1 by data and by author track record; the same team's companion applies the model in a published setting)
url: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3229719 (read in full at https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/3/2021/08/Trading-Cost.pdf)
citations: 121 (Semantic Scholar by DOI 10.2139/ssrn.3229719, checked 2026-08-27); 83 (Crossref is-referenced-by-count, same date)
sample_period: 1998-08 – 2016-06
markets: 21 developed equity markets, 32 exchanges, ~10,000 stocks; $1.7tn of live executed trades, ~700M executions
tier: A on the measurement (the largest live-execution dataset in the literature, out-of-sample-validated against three brokers, a consultant covering >2,000 institutions, and two live index funds); B on generality (one manager, one execution style)
validation_overlap: false
published_post_2018: false
---

Secondary source, **recorded as unread**: Perold (1988), "The implementation shortfall:
paper versus reality", *Journal of Portfolio Management* 14(3), 4–9, DOI
`10.3905/jpm.1988.409150`, 298 citations (Crossref `is-referenced-by-count`, checked
2026-08-27). This is the origin of the implementation-shortfall concept and the only
source this folder wanted for it. It is paywalled at `pm-research.com`, has no repository
copy, and no course-page or author-page mirror was found. Its definition is used here
**only as restated in equations (1)–(3) of the source read**, and is flagged as such below.

## Mechanism

The question this note answers is the one `SUMMARY.md`'s session-13 open question (b)
named as the last untouched cost-side vocabulary: **what is the actual gap between a paper
portfolio's returns and a real one's, and what determines its size?**

**The accounting identity (Perold, second-hand).** Implementation shortfall is
`IS = ret_theory − ret_actual`, decomposed as

```
IS  =  ret_theory  −  cost_execution / P_theory  −  cost_opportunity / P_theory
```

where `P_theory` is the price at which the model *believed* it was trading, `cost_execution`
is the signed difference between execution prices and `P_theory` summed over shares actually
transacted, and `cost_opportunity` is the return foregone on shares the model wanted but
never got. A companion measure, **market impact**, replaces `P_theory` with `P_start`, the
price when trading actually begins; `IS − MI` is therefore the drift between decision and
first fill. Execution cost so defined already contains commissions, effective spread and
price impact — it is not a component to be added to them.

The structural point, and the reason the concept exists: **transaction cost is not a fee, it
is a difference between two portfolios.** A paper book is defined by prices it did not pay.
Anything that moves the achieved price away from the decision price is a cost, including the
cost of *not* trading.

**What the data say drives it.** Sorted by how much they matter:

1. **Trade size relative to the stock's daily volume dominates everything else.** It is the
   single most important determinant, and the relation is **concave**: impact rises with size
   at a decreasing rate. A log–log regression of impact on trade size gives a slope near 0.35
   with `R² ≈ 0.95`; the authors round it to **½ (square-root)** to avoid overfitting and
   because independent theory and independent broker data both land there. An F-test rejects
   a linear specification in favour of the square-root one. Concavity is the load-bearing
   claim, not the exact exponent — the authors say so explicitly.
2. **Volatility raises impact** — both the stock's idiosyncratic volatility and the market's
   contemporaneous volatility level. This is the market-maker inventory-risk prediction and it
   holds in the data.
3. **Firm size lowers impact**, consistent with depth.
4. **Market structure matters little.** Across 21 markets, median impact rises with intraday
   triggered auctions and falls with the number of competing venues; transaction taxes and
   short-sale uptick rules show no significant effect. For the largest trades, exchange rules
   are near-irrelevant.
5. **Impact is mostly permanent.** Roughly 85–90% of the price move does not revert the next
   day. The authors argue — correctly for this repo's purpose — that for after-cost strategy
   returns the **entire** impact (permanent + temporary) is the relevant charge, not just the
   reverting part.
6. **Long and short executions cost about the same.** Conditional on shorting, selling short
   is not measurably dearer than selling long. Any extra cost of the short side is opportunity
   cost or borrow, not execution.

**The headline, and it is a level claim.** Across the whole live sample the mean market
impact is **9.97 bps** and the mean implementation shortfall **11.02 bps** per trade, with
the `IS − MI` difference (1.05 bps) small and statistically indistinguishable from zero.
The **median** is lower (6.18 / 8.63 bps) — costs are right-skewed — and the
**dollar-value-weighted** mean higher (15.14 / 16.06 bps), because the biggest trades are
the dearest. Large-cap trades average 8.90 bps against 18.95 bps for small caps. The average
trade in the sample is **0.9% of the stock's daily volume**, and the average bid-ask spread at
order arrival is 21 bps — of which these trades rarely pay half, because the algorithm posts
patient limit orders rather than demanding liquidity.

**The methodological result that reframes the whole prior literature.** Cost estimators built
from daily or intraday trade-and-quote data measure *the average trade in the market* —
retail, impatient, informed-insider, liquidity-demanding — and therefore vastly overstate what
a patient institutional trader pays. Holding universe, period and the size-independent constant
fixed, and varying only the impact-vs-size function:

| trade size | live-calibrated model | square-root TAQ | linear TAQ |
|---|---|---|---|
| 2% of daily volume | 13.7 bps | 27.1 bps | 44.9 bps |
| 10% of daily volume | 32.3 bps | 60.2 bps | 223.3 bps |

The linear TAQ specification is the one used by Korajczyk–Sadka (2004) and, in spirit, by
Lesmond–Schill–Zhou (2004) and Novy-Marx–Velikov. **Square-root TAQ models run about 2× live
costs; linear TAQ models run 3×–10× live costs, the gap widening with size.** An out-of-sample
test on two live index funds settles which is right: the live-calibrated model predicts their
actual annual trading costs almost exactly, while the linear TAQ model overstates them by
about 6× and 12× respectively.

## Construction recipe

The estimated cost function, which is the usable object:

```
MI  =  a  +  b·x  +  c·sign(x)·√|x|
x   =  100 × (dollars traded) / (stock's average past-year daily dollar volume)
```

with `a` absorbing the level terms evaluated at their medians — a time trend, `log(1+ME)`,
idiosyncratic volatility, and the market's volatility level — and `b`, `c` the linear and
square-root size coefficients. Contemporaneous market and characteristic-matched returns enter
the descriptive regression but are **dropped for ex-ante use**, since their expectation at
daily frequency is zero. Everything remaining is known before the trade.

Portfolio-level annual cost is then just

```
TC  =  turnover × MI(x),      x = (turnover × NAV / n) / (h · dtv),
dtv = Σ_i w_i · (stock i's one-year median daily dollar volume)
```

for a book of `n` names rebalanced `h` times a year. That is the whole capacity calculator:
**one number for how much you trade, one for how big you are relative to the volume you trade
in.** It is the form in which the index-fund out-of-sample test was run.

## Robustness evidence (qualitative only)

- **Out-of-sample on four independent channels**: three brokers (ITG, Deutsche Bank, JP
  Morgan), the ANcerno consultant database covering >2,000 institutions and >2,000 brokers,
  and two live passive index funds. The model matches all four; TAQ-calibrated models match
  none of them.
- **Cross-market**: coefficient estimates are similar in the US and in the 20 other developed
  markets, which is 20 out-of-sample countries for a result usually established on US data
  alone. This folder has repeatedly downgraded single-market evidence; this source does not
  need that discount.
- **Endogeneity**: portfolio formation and trade execution are separate systems — the
  algorithm chooses *how patiently* to trade, never *what* to trade — and 99.9% of intended
  trades complete, with a mean realised horizon slightly under one day. As an extra control,
  costs on "forced" first trades from new benchmark-tracking inflows, which have no scope to
  avoid expensive names, are no different from the rest.
- **The honest caveats, stated by the authors.** It is *one* manager, trading long-horizon
  signals, with a proprietary patient-execution algorithm, on a universe that deliberately
  excludes microcaps, penny stocks and very thinly traded names. The costs are therefore those
  of a patient large trader in liquid names — which is a description of the good case, not the
  average one. The regressions' `R²` is just over 10%; the authors defend this as high for a
  near-daily return as dependent variable, which is fair, but it means the model predicts the
  *level* of costs far better than any individual trade's cost.
- **No replication in the Hou–Xue–Zhang / Jensen–Kelly–Pedersen sense** exists or could — the
  input data is proprietary. What substitutes for it is the four-channel out-of-sample match
  above, which is a stronger check than most replications this folder has recorded.

## Implementability here

**The direct verdict on this repo's cost model, and it is the reason to read this note.** The
engine charges a flat **15 bps per side** with a one-day execution lag. Two facts line up
exactly:

- The engine's benchmark price *is* the implementation-shortfall benchmark. The source defines
  `P_theory` as "the closing price at the time the strategy's desired holdings and trades are
  generated, which is typically the prior day's closing price". That is this repo's
  signal-at-close-`t`, trade-at-`t+1` convention, stated in the same words. The repo is
  therefore charging the right *quantity*; the only question is the level.
- On level, the repo is **conservative to fair**. 15 bps/side sits above the live mean per-trade
  IS (11.02 bps) and just under the dollar-weighted mean (16.06 bps) of a manager trading at
  ~0.9% of daily volume in a universe of comparable liquidity to this one. It is roughly 1.7×
  the live median. For a book of this repo's size on ~145 liquid global stocks and ETFs, the
  15 bps charge is not optimistic and is probably a little punitive.

**Consequence, and it closes rather than opens.** `learnings.md` already prices the champion's
entire cost drag at 0.45%/yr ≈ 0.019 Sharpe at 3.0× turnover, and declares turnover reduction
a spent lever. This source removes the remaining doubt about that conclusion from the opposite
direction: the *rate* is not understated either, so the true drag is not secretly larger than
the modelled one. **Cost is not where this repo's edge is hiding, in either direction.** The
prediction of session 13's open question (b) — that this literature would close rather than
open — is confirmed, and this is the specific form the closure takes.

**What the flat model genuinely misses, ranked by whether it can bite here.**

1. *Size-independence.* The real function is `a + b·x + c·√x`; the repo's is the constant `a`
   alone. That is correct only in the small-`x` limit. It means the repo's backtests are
   **capacity-blind**: they are valid at some notional and silently wrong above it, with no
   term that degrades. This is not a bug to fix (the engine is frozen and the data has no
   volume field) but it is a caveat that belongs next to survivorship in `learnings.md`'s
   permanent list — *every Sharpe in this repo is a small-fund Sharpe*.
2. *Volatility-independence.* Impact scales with the traded name's volatility. A cross-sectional
   momentum basket systematically holds the high-volatility tail of its universe, so a flat bps
   charge under-charges precisely the book this repo runs. See the companion note on the
   functional form for the exact scaling and for why the size of this effect is still small at
   3.0× turnover.
3. *Opportunity cost is zero here by construction.* The engine fills every target weight. The
   source's own trades complete 99.9% of the time, so this is the same regime, and the
   `cost_opportunity` term of the identity can be honestly ignored — but only because the book
   is small and the names liquid. It is the term that would appear first if either changed.

**A screen this yields, costing no trial.** When importing a *net-of-cost* claim from any paper,
check which cost estimator produced it. A verdict built on a **linear** price-impact model
calibrated to TAQ data (Korajczyk–Sadka's `Δp/p = λ·Δq`; Lesmond et al.'s LDV proportional
estimate; Novy-Marx–Velikov's effective spread) is measuring the average market participant,
not a patient institution, and overstates a patient trader's cost by roughly **2× at best and
an order of magnitude at large sizes**. This does not make such papers wrong — it makes their
*net* conclusions inapplicable to a patient book, while leaving their *gross* results and their
cross-sectional patterns untouched. Applied immediately in the companion note on the
momentum-cost debate.

**What is not available here.** The cost model needs dollar volume, market capitalisation and
idiosyncratic volatility. The repo has the third (from the returns it already holds) and
neither of the first two, and `program.md` gates additional data behind human approval. So the
capacity calculator cannot be run on this universe, and no attempt should be made to proxy
`dtv` from adjusted closes. The honest status is: **mechanism sourced, level verified as
adequate, capacity unmeasurable with the data the repo has** — the same shape of answer session
13 reached on survivorship.

## Related

- `notes/2026-08-27-market-impact-functional-form-and-trade-rate.md` — the independent broker
  estimate of the same function, which adds the execution-*rate* dimension and the volatility
  scaling this note only names.
- `notes/2026-08-27-momentum-net-of-costs-debate.md` — where the cost-estimator screen above
  does its work: two tier-1 papers reach opposite verdicts on momentum, and this source's
  measurement is the tiebreaker.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the mitigation side,
  declared closed for idea supply in session 2. This note grades the *level* those mitigations
  are applied to, which was the piece never sourced.
- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — the theory of what to
  do about proportional costs (a no-trade band). This note establishes that the repo's
  proportional rate is roughly right, which is the premise that theory needs.
