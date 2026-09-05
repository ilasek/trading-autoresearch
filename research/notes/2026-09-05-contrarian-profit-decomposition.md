---
title: "When Are Contrarian Profits Due to Stock Market Overreaction?"
authors: Lo, MacKinlay
year: 1990
venue: Review of Financial Studies 3(2), 175–205 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1093/rfs/3.2.175
citations: 1334 (Crossref, checked 2026-09-05); 1892 (Semantic Scholar, checked 2026-09-05)
sample_period: 1962–1987 (weekly CRSP NYSE–AMEX), with the two halves analysed separately
markets: US equities, individual names and size-sorted portfolios
tier: A
validation_overlap: false
published_post_2018: false
---

**Text read**: NBER Working Paper 2977 (May 1989), the working-paper version of the published
article, in full from `nber.org/system/files/working_papers/w2977/w2977.pdf` — derivation,
decomposition, the empirical appraisal and the cross-autocorrelation matrices. The algebra below
is the paper's own and is unchanged in the published version, which is where every later citation
of the decomposition points.

**Why a second record of this source exists.** This folder already holds a *qualitative* record of
Lo–MacKinlay inside `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`, where it
appears as one of three clustered sources and supplies one sentence: contrarian profits need not be
overreaction, because cross-autocovariances can supply them. That record is correct and is not
superseded. What it does not contain is **the identity itself** — which is the only part of this
paper that is implementable, and which the lab now needs, because `lead-lag-spillover` has a family
lead whose mechanism claim the lab's own follow-up trial closed. This note is the canonical record
of the algebra; the earlier note keeps the reversal-family reading.

## Mechanism

The paper's object is not a strategy but an **accounting identity for a strategy's expected
profit**, and the identity is what transfers.

Take the textbook contrarian rule: at each date, weight each name by minus its deviation from the
equal-weighted cross-sectional mean, `k` periods ago.

```
w_i,t(k) = -(1/N) * ( R_i,t-k  -  R_m,t-k ),      R_m,t = (1/N) * sum_j R_j,t
```

Weights sum to zero by construction (an arbitrage portfolio: it shorts last period's winners and
buys last period's losers, in proportion to how far each deviated). The profit is
`pi_t(k) = sum_i w_i,t(k) * R_i,t`. Taking expectations and writing `Gamma_k` for the lag-`k`
autocovariance matrix of the return vector (`Gamma_k[i][j] = cov(R_i,t-k, R_j,t)`), expected profit
decomposes into **exactly three terms**:

```
E[pi_t(k)]  =  C_k  +  O_k  -  sigma2_mu

C_k       = (1/N^2) * ( ones' Gamma_k ones  -  trace(Gamma_k) )     # OFF-diagonals only
O_k       = -((N-1)/N^2) * trace(Gamma_k)                            # DIAGONALS only
sigma2_mu = (1/N) * sum_i ( mu_i - mu_bar )^2                        # NO autocovariance at all
```

Read the three terms as three different economic claims, because that is what they are:

- **`C_k` is lead-lag.** It depends only on the *cross*-autocovariances — name `j`'s past return
  covarying with name `i`'s future return. Positive cross-autocovariances make `C_k > 0`.
- **`O_k` is own reversal.** It depends only on the *diagonals*. Negative own-autocovariance
  (individual names reverse) makes `O_k > 0`. This is the overreaction story, and it is one
  term of three.
- **`sigma2_mu` is neither.** It is the cross-sectional variance of the *unconditional mean*
  returns, it does not depend on `k`, and it enters with a **minus** sign for a contrarian book —
  equivalently, with a **plus** sign for a momentum book. It is what a cross-sectional
  ranking earns from names simply having persistently different average returns, with no
  time-series predictability anywhere in the system.

The paper's central negative result follows directly: a contrarian rule can be profitable **even if
every individual security's returns are serially independent**, purely through `C_k`. If A's high
return today implies B's high return tomorrow, then selling A and buying B pays, though neither
name predicts itself. Overreaction is *sufficient* but not *necessary*, and the decomposition says
which of the two is doing the work in any given dataset.

The reverse implication is the one that constrains interpretation elsewhere. Equal-weighted index
returns are positively autocorrelated while individual names are weakly *negatively*
autocorrelated; since the index autocorrelation's numerator is the sum of all elements of
`Gamma_1`, and the diagonal contribution is negative, the off-diagonals must be strongly positive.
**Portfolio-level positive autocorrelation and name-level negative autocorrelation are not in
conflict — they jointly imply large cross-effects.**

## Construction recipe

Nothing here is a strategy; all of it is measurement, and all of it runs on returns the lab already
has.

**1. The decomposition, as a diagnostic.** For any cross-sectional book of the deviation-weighted
form, estimate `Gamma_k`, then report `C_k`, `O_k` and `sigma2_mu` as *percentages of expected
profit*. That is the paper's own Table 3 and it is the whole method. Note that a rank-based or
banded long-only book is not literally the weight scheme above, so the identity does not apply to
it exactly; it applies to the deviation-weighted long-short twin, which is the right object for
asking *where a signal's content comes from* before deciding how to hold it.

**2. Frequency and horizon.** Weekly returns, lags `k = 1..4`. The paper reports the cross term
carrying roughly half of expected contrarian profit at lag 1, and the pattern surviving at lags 2
through 4. Positive expected profit at lags ≥ 2 is itself a test: a model in which the only sources
are a positively autocorrelated common factor plus bid-ask bounce implies expected profits can be
positive **only at lag 1** and must be negative beyond it. So the lag profile discriminates
microstructure from everything else without any extra data.

**3. The asymmetry test — the part that identifies lead-lag direction.** Form group-level return
series (they use five size-sorted quintiles plus the equal-weighted index), then estimate the full
cross-autocorrelation matrix `T_k` where element `(i,j)` is `corr(R_i,t-k, R_j,t)`. **Lead-lag is
the asymmetry of that matrix, not any single entry.** In their data the entries below the diagonal
systematically exceed those above it, and the largest asymmetry is stark: last week's large-stock
return correlates with this week's small-stock return an order of magnitude more strongly than the
reverse. A symmetric `T_1` means no lead-lag regardless of how large its entries are.

**4. Sampling theory that must come with it.** The published standard errors relax
covariance-stationarity to weakly dependent, heterogeneously distributed returns
(their Appendix 2). Do not use i.i.d. standard errors on any of the three terms. They also flag a
finding worth expecting: `C_k` and `O_k` are strongly *negatively* correlated as estimators, so
`E[pi_t(k)]` can be significant at lags where neither component is — never conclude "no lead-lag
and no reversal" from two insignificant components.

## Robustness evidence (qualitative only)

Multi-decade weekly sample split into halves, with the decomposition re-run on each; the paper
reports the pattern essentially unchanged across both, with the cross term carrying at least half
of expected profit at lag 1 in each. The authors identify and address their own **survivorship
bias** explicitly: requiring continuous listing over the full sample selects survivors, and the
half-sample re-estimations exist to bound it. Methodology honesty is high — they name the
competing microstructure explanation, derive its testable implication (sign of expected profits at
lags ≥ 2), and test it rather than asserting it away. The decomposition is analytic, so it does not
"replicate" in the anomaly sense; it is an identity and later work argues about which term
dominates, not about whether the identity holds. That argument is the subject of
`notes/2026-09-05-cross-serial-correlation-as-restatement.md`, which should be read against this
note rather than after it.

The paper does not model transaction costs and does not claim tradeability; the size-conditional
observation it does make is that profit *per dollar of long/short position* is roughly twice as
large among the smallest quintile, with the authors declining to interpret this as inefficiency
because they have not controlled for risk or market depth.

## Implementability here

**The decomposition is free and it is aimed at a live question.** `lead-lag-spillover` has two
recorded trials. #58 (`ll_group_lastmonth_lead`) is the family lead: it holds all members of the
three sector groups with the highest median trailing 21-day return. #62 held only the laggard half
of the *same* groups and came back a null, which the lab correctly read as closing the diffusion
claim and relabelling #58 "one-month group trend". Put in this paper's terms, the lab has
established that #58 is **not** a `C_k` object at the name-within-group level, and has not
established what it is. The identity says there are only two remaining possibilities — group-level
own-autocorrelation (`O_k` computed on group series) or persistent cross-sectional dispersion in
group mean returns (`sigma2_mu`) — and both are computable from the group return series the
candidate already builds, with no trial and no returns scored beyond what the trial recorded.

**`sigma2_mu` is the term this repo should worry about most, and no other note here names it.**
The universe is **current** constituents, so survivorship conditioning inflates exactly the
quantity `sigma2_mu` measures: the surviving names' realised mean returns are more dispersed, and
more persistently ranked, than a point-in-time panel's would be. `sigma2_mu` enters a *momentum*
book's expected profit positively and requires **no forecastability of any kind** — it is the
purely mechanical component. Every cross-sectional ranking book in this lab, the champion included,
collects it. That gives a concrete, sourced form to a caveat `learnings.md` currently states
qualitatively, and it suggests the honest version of any lead-lag hypothesis: *does the signal add
anything beyond `sigma2_mu`*, which is answered by re-running the decomposition with the names
demeaned by their own full-sample means (the term vanishes by construction) and asking whether the
remaining `C_k` is still there.

**Frequency: weekly, and this is not optional here.** The lab's lead-lag trials are monthly-signal
books. The identity is defined at any horizon, but the *cross* term is a short-horizon object in
this literature and the daily frequency is unusable on this universe for a reason `SUMMARY.md`
already states: 15 regions with non-overlapping sessions and unhedged USD conversion manufacture a
mechanical daily "US leads Asia" cross-correlation. Weekly returns absorb the session offset.
Compute group series weekly; report the lag profile `k = 1..4`.

**Pitfalls specific to this repo.**
- The `N` in the identity is the number of *series*, and the terms scale differently in `N`
  (`C_k` sums `N(N-1)` off-diagonals, `O_k` sums `N` diagonals). With 12–15 groups rather than
  hundreds of names, the off-diagonal count is small and `C_k` is correspondingly noisy. Report
  the terms with the paper's heteroskedasticity-robust errors or not at all.
- The identity is about a *zero-net* deviation-weighted book. This lab's books are long-only,
  gross 1.0, banded. Use the identity to decide **what a signal contains**, then decide separately
  how to hold it; do not read `E[pi_t(k)]` as a prediction of any book's Sharpe.
- The asymmetry test needs a group partition. The lab has one (the sector groups #58 used) and
  `region` besides. Both are cheap; run both, and expect the region version to be the one
  contaminated by session offsets even weekly.

## Related

- `notes/2026-09-05-cross-serial-correlation-as-restatement.md` — the direct rebuttal: a null in
  which the asymmetry of `T_k` arises with no lead-lag at all. **Do not use this note's asymmetry
  test without that note's control.**
- `notes/2026-09-05-price-delay-market-frictions.md` — the per-name measure of adjustment speed
  that this paper's cross-effects are usually attributed to, with its own dispersion precondition.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — the folder's earlier,
  qualitative record of this source, kept for the reversal-family reading.
- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — Chordia–Swaminathan, which
  builds on this paper's cross-effects and asks *which* names lead.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — `sigma2_mu` is the
  algebraic form of the mechanism that note describes.
