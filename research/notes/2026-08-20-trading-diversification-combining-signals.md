---
title: "A Transaction-Cost Perspective on the Multitude of Firm Characteristics"
authors: DeMiguel, Martín-Utrera, Nogales, Uppal
year: 2020
venue: Review of Financial Studies 33(5), 2180–2222 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhz085 (read in full at https://lbsresearch.london.edu/id/eprint/1124/1/DeMiguel_TransactionCostPerspective.pdf)
citations: 193 (OpenAlex, checked 2026-08-20); 177 (Crossref is-referenced-by-count, same date). Semantic Scholar's DOI endpoint returns 24 for this DOI — a clear undercount; recorded so the discrepancy is not rediscovered.
sample_period: 1980-01 – 2014-12 (significance tests run on 1988-05 – 2014-12)
markets: US stocks (CRSP / Compustat), 51 firm characteristics
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

The question is "how many characteristics does an investor's optimal portfolio actually need?",
and the answer inverts the usual intuition: **transaction costs *increase* the number of jointly
significant characteristics** — in their tests, from six without costs to fifteen with them.
The reason is a mechanism this folder has not recorded in any form, and which is the cost-side
counterpart to everything it has on averaging.

**Trading diversification.** Several signals held simultaneously must all be rebalanced by
trading the *same underlying instruments*. If one signal wants to buy a name this period and
another wants to sell it, the two trades net against each other inside the book and only the
residual is executed. So the turnover of a combined book is strictly less than the average
turnover of its legs traded separately — by exactly the amount their rebalancing trades fail to
be perfectly correlated. This is not risk diversification (which is about return covariance);
it is diversification of *trades*, and it is what makes a characteristic that is unprofitable
gross become worth holding net: it can earn its keep by cancelling somebody else's trades.

**Proposition 3 puts a closed form on it**, which is the reason this note matters more than its
empirical results. Let `trade_{i,k}` be the trade in instrument `i` required to rebalance leg
`k`, and let those `K` trades be jointly normal with zero mean and covariance `Ω`. Then

```
turnover(equal-weighted combination)     √(eᵀ Ω e)
────────────────────────────────────  =  ───────────   < 1
turnover(legs traded in isolation)       Σ_k √(Ω_kk)
```

with two specialisations that are directly usable:

```
equal variances σ², equal pairwise trade correlation ρ:     √( (1 + ρ(K−1)) / K )
zero trade correlation (ρ = 0):                             1 / √K
```

Read off the three consequences the authors draw: trading diversification exists whenever the
trades are not perfectly correlated; it **grows with `K`**; and it **shrinks as the legs'
rebalancing trades become more correlated**. Note what the free parameter is — the correlation
of *trades*, not of scores, not of weights, not of returns.

A corollary they observe empirically and that is worth stating separately: **a leg's marginal
contribution to portfolio turnover can be negative.** Adding it reduces the book's absolute
turnover. "Every extra leg costs turnover" is false as a general claim.

## Construction recipe

The paper's machinery, for reference — this repo would use the proposition, not the pipeline:

- Portfolios are **parametric portfolio policies** in the Brandt–Santa-Clara–Valkanov sense
  (weights linear in cross-sectionally standardised characteristics, coefficients fitted to a
  utility objective), extended with an explicit transaction-cost term, using the
  value-weighted portfolio as benchmark.
- Costs are modelled with both proportional and quadratic specifications; the authors state the
  trading-diversification turnover reduction holds "regardless of the particular manner in which
  transaction costs are modeled", which is what makes the proposition portable.
- Multiple testing is handled by **screen-and-clean**: a lasso (L1) screen stage to shortlist
  characteristics, then joint significance tested on the *unregularised* policy over only the
  survivors — explicitly to avoid the overfitting bias in one-stage regularised selection.
- The turnover comparison itself is done on an equal-weighted combination of the 51
  characteristic portfolios, with each characteristic's sign flipped so its long-short leg has
  positive average return.

## Robustness evidence (qualitative only)

- Proposition 3 is algebra under a stated distributional assumption (jointly normal, zero-mean
  trades) and cannot decay; what can fail is the normality assumption and the equal-weighting
  simplification, which the authors say extends to generic portfolios of characteristics.
- The empirical magnitude matches the closed form well. Across 51 characteristics, the
  average monthly turnover needed to trade them in isolation is 24.09% against 6.71% for the
  equal-weighted combination — a 72.15% reduction, against the zero-correlation prediction of
  `1 − 1/√51 ≈ 86%`. The gap is explained by the measured average pairwise correlation of
  rebalancing trades, 5.47%: close to zero but positive, which is the direction that lifts the
  ratio. *(These are turnover statistics, not returns.)*
- Multi-decade US sample; single market. Costs are the paper's subject rather than an
  afterthought, and multiple testing is explicitly handled — the two rubric axes most papers in
  this folder fail.
- It builds directly on Novy-Marx–Velikov (2016), already covered here, and states the
  advance precisely: that paper tests cost-mitigation for **one characteristic at a time**,
  which by construction cannot see a benefit that only exists in combination.
- The authors argue their finding is unlikely to be data-mined, since the 51 characteristics
  were discovered by others for return prediction, not for anything to do with trade
  correlation. That is a fair argument.

## Implementability here

**This is the first source in the folder that supplies a free, pre-trial, holdings-only
prediction of the *cost* consequence of an averaging proposal.** The existing pre-trial
diagnostics measure rank correlation of scores and overlap of weights; Proposition 3 says the
statistic governing turnover is the correlation of the *rebalancing trades*
`trade_{i,k} = w_{i,t+1,k} − w_{i,t,k}(1 + r_{i,t+1})`. That is computable from holdings and
prices with no returns scored and no trial spent, and it converts directly into a predicted
turnover ratio `√((1 + ρ(K−1))/K)` before anything is built. Given `learnings.md`'s standing
rule — measure the mechanism's premise first and pre-register the effect size — this is a
ready-made instance.

**It also retro-predicts the champion's turnover, which is the check that the mechanism
transfers.** The lab has recorded the six-vintage overlap book at 3.5x turnover against 7.9x
for the single-vintage version on the same base — a ratio of 0.44, against `1/√6 = 0.41` for
uncorrelated trades. The vintages' trades are positively correlated (their weight overlap is
recorded at 0.645), and positive correlation is exactly what lifts the ratio above `1/√K`. The
sign, the magnitude and the direction of the deviation all agree. Two honest caveats: the
proposition's `K` legs are *different signals* while the lab's are *vintages of one signal*, and
the lab's comparison is not a controlled one (breadth changes too). Treat this as the mechanism
being consistent, not as a measurement.

**A real amendment to `SUMMARY.md` screen #2, and it should not be smoothed over.** The folder's
standing test before any ensemble is *are the components estimates of the same quantity, or
different return streams?* — with the second answer treated as a dilution tax. This source
supplies a countervailing term the screen does not contain: components estimating *different*
quantities still net their trades against each other, and that saving does not require them to
be estimates of anything in common. So the screen is right about the **gross** return axis and
incomplete on the **net** one. The correct form is: a second leg's contribution is
`(dilution of gross Sharpe) + (turnover saved by trade cancellation) × (cost rate)`, and the
first term is what the lab has measured while the second has never been measured here.

**Whether that changes any verdict is a separate question, and the honest answer is: probably
not, but for a stated reason rather than by assumption.** `learnings.md` prices the champion's
*total* cost drag at ~0.019 Sharpe and records that turnover was ruled out as the explanation
for a 3.4pp annual return gap three times over. A mechanism that can at most recover a fraction
of ~0.019 Sharpe cannot overturn a dilution tax measured at ~0.02 Sharpe per 20% of capital.
So: **not grounds to reopen the ETF-sleeve blend.** It *is* grounds to stop describing added
legs as unambiguously turnover-costly, and to compute the joint-book turnover rather than
assume it is the weighted average of the legs'.

**What does not transfer.** The characteristics are overwhelmingly fundamental (the
significance results are about which of 51 firm characteristics matter) and this repo has no
fundamentals; the portfolios are benchmark-relative long-short; and the fitted parametric
policy is the estimated-coefficient class that `notes/2026-08-20-parametric-portfolio-policies.md`
records as the failure mode this lab's protocol exists to punish. Import Proposition 3 and the
marginal-turnover idea; import nothing else.

## Related

- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — Novy-Marx–Velikov, the
  paper this one extends. `SUMMARY.md` closed the cost-mitigation family "by enumeration" over
  three techniques (screening, frequency reduction, banding); trade cancellation across legs is
  a **fourth** that the enumeration missed, because it is not a property of one book's trading.
- `notes/2026-08-20-parametric-portfolio-policies.md` — the estimation machinery used here.
- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — the same cost axis
  from the dynamic-optimisation side; Gârleanu–Pedersen's Proposition 5 says the optimal book is
  an average of past targets, and this source says why averaging targets is cheap to trade.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the screen this
  note amends.
