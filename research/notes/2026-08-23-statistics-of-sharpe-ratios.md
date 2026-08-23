---
title: "The Statistics of Sharpe Ratios"
authors: Lo
year: 2002
venue: Financial Analysts Journal 58(4), 36–52 — venue tier 1 (peer-reviewed; Graham and Dodd Scroll Award)
url: https://doi.org/10.2469/faj.v58.n4.2453
citations: 773 (Semantic Scholar, checked 2026-08-23)
sample_period: the derivations are asymptotic theory with no sample; the illustrative application uses monthly mutual-fund and hedge-fund returns
markets: US mutual funds and hedge funds in the illustration only; the results themselves are distribution-free given stationarity
tier: A
validation_overlap: false
published_post_2018: false
full_text: read in full from a course-page mirror of the FAJ article (traders.studentorg.berkeley.edu), carrying the AIMR pagination and copyright line. The publisher endpoints (Taylor & Francis, CFA Institute) were not tried after the author's own MIT page returned 404.
---

## Mechanism

The gate this lab is scored by reads one number: net Sharpe on the validation split. That number
is an **estimator**, built from two unobservable population moments, and it therefore has a
sampling distribution. This paper derives it. Nothing in `research/` has covered the statistical
properties of the objective itself, which — given that `learnings.md` carries a four-point standing
concern about what the gate is measuring — is the largest uncovered gap in the folder.

**The i.i.d. result.** With `SR = (µ − R_f)/σ` estimated by the sample mean and sample standard
deviation over `T` observations, the delta method applied to `g(µ, σ²)` gives an asymptotic
variance that is a weighted sum of the asymptotic variances of `µ̂` and `σ̂²` (no covariance term,
because under i.i.d. returns the two are asymptotically independent). Evaluating the sensitivities
`∂g/∂µ = 1/σ` and `∂g/∂σ² = −(µ − R_f)/(2σ³)` collapses it to a formula with one free parameter:

```
V_IID = 1 + ½·SR²           SE(ŜR) ≈ sqrt( (1 + ½·SR²) / T )
```

Three readings, all in the paper:

1. **Larger Sharpe ratios are estimated *less* precisely in absolute terms.** At `T = 60`, the
   standard error is 0.188 for a true SR of 1.50 and 0.303 for a true SR of 3.00. As a *proportion*
   of the Sharpe ratio the error approaches a floor, `SE/SR → 1/√(2T)`, so a high-Sharpe strategy
   is not proportionally better measured.
2. **Where the error comes from flips with the Sharpe level.** The share of `V_IID` attributable to
   error in `µ̂` is `1/(1 + ½SR²)`. At `SR = 0.25` that is 97.0% — almost all the uncertainty is in
   the mean. At `SR = 2.00` it is 33.3%, and at `SR = 3.00` only 18.2%: for a high-Sharpe book most
   of the estimation error has migrated into the **volatility** estimate.
3. **The whole table.** Lo's Table 1 (asymptotic SE by SR and sample size, i.i.d.) includes, for
   `T = 60`: SR 0.50 → 0.137, 1.00 → 0.158, 1.25 → 0.172, 1.50 → 0.188. For `T = 250`: 0.067,
   0.077, 0.084, 0.092.

**The non-i.i.d. result.** Under stationarity alone — allowing serial correlation, conditional
heteroskedasticity, jumps, factor dependence — a GMM estimator with a Hansen (1982) asymptotic
distribution gives `SE(ŜR) = sqrt(V̂_GMM/T)`, with `V̂_GMM = (∂g/∂θ) Ω (∂g/∂θ)'`. The i.i.d.
independence of `µ̂` and `σ̂²` no longer holds and the covariance term reappears.

**Time aggregation, and this is the result the paper is best known for.** Under i.i.d. returns,
`Var[R_t(q)] = qσ²` and so `SR(q) = √q · SR` — the familiar `√12` or `√252`. Under stationarity,

```
Var[R_t(q)] = qσ² + 2σ² Σ_{k=1}^{q−1} (q − k) ρ_k

SR(q) = η(q)·SR ,     η(q) = q / sqrt( q + 2 Σ_{k=1}^{q−1} (q − k) ρ_k )
```

which reduces to `√q` only when every autocorrelation `ρ_k` is zero. **Positive serial correlation
pushes `η(q)` below `√q`; negative serial correlation pushes it above.** The reason is mechanical:
positive autocorrelation makes multiperiod variance grow faster than linearly in `q`, inflating the
denominator. The magnitudes are not small — for an AR(1) with a monthly first-order autocorrelation
of −20%, the annual scale factor is 4.17 against `√12 = 3.46` in the i.i.d. case, and 2.88 when the
monthly autocorrelation is +20%. So **the naive `√q` annualisation is a biased estimator whenever
returns are serially correlated, and the bias is signed by the sign of the autocorrelation.**

Lo also records, in passing but flatly, that the apparent unitlessness of the Sharpe ratio is an
illusion — it scales with the horizon over which numerator and denominator are defined, "making a
longer-horizon investment seem more attractive," an interpretation that "is highly misleading" —
and that the Sharpe ratio "is not a complete summary of the risks of a multiperiod investment
strategy and should never be used as the sole criterion for making an investment decision."

## Construction recipe

Not a strategy. Three computations, all of which run on return series the repo **already has
stored** in `experiments/trial_returns/`, i.e. score nothing new and re-run no strategy.

1. **Attach a standard error to every Sharpe ratio quoted.** `SE = sqrt((1 + ½SR²)/T)` with `SR`
   and `T` at the same frequency; convert by the same `η` factor used to annualise. A confidence
   interval is `ŜR ± 1.96·SE`.
2. **Measure the serial correlation of daily strategy returns and compute `η(q)` properly** before
   comparing any annualised figure, or at minimum report `ρ̂_1` so the sign of the bias in the
   naive `√252` is known.
3. **For the non-i.i.d. case, use the GMM/HAC standard error rather than the i.i.d. formula**,
   since a book with monthly rebalancing, hysteresis bands and averaged formation vintages has no
   claim to independent daily returns.

## Robustness evidence (qualitative only)

The derivations are standard asymptotic theory (delta method, CLT, GMM) and are not the kind of
result that decays or fails replication; the assumptions are stated and are weak (finite moments;
stationarity for the general case). The venue is tier 1 and the paper is heavily cited across
performance-measurement practice. Its own stated limitation is that all results are *asymptotic* —
finite-sample behaviour of the Sharpe estimator, particularly for fat-tailed returns, is not
derived, and the paper does not treat the **paired** problem of the standard error of a
*difference* between two Sharpe ratios estimated on the same period, which is the case this lab
actually faces (see below). The empirical illustration is a demonstration of magnitude, not a
result, and no part of it is carried here.

## Implementability here

This is the most directly usable thing in the folder for the axis `learnings.md` says matters most,
and it cuts in an uncomfortable direction.

**(a) The order of magnitude, computed from the formula and the sample length alone.** The
validation split is six years, 1,562 trading days by `learnings.md`'s own count. Take an annualised
Sharpe near the champion's recorded level: the daily Sharpe is small, so `½SR²` is negligible at
that frequency and `V_IID ≈ 1`, giving `SE(ŜR_daily) ≈ 1/√1562 ≈ 0.025`, which annualises to
**≈ 0.40**. Estimating from annual observations instead — six of them — gives
`sqrt((1 + ½·1.2²)/6) ≈ 0.54`. Either way, **the standard error of a single validation Sharpe on
this window is of order 0.4–0.5**, while the entire recorded promotion ladder spans 0.865 → 1.229,
a range of 0.364. The gate's whole history of measured improvement is **smaller than one standard
error of any one of its measurements.**

**(b) The essential caveat, stated before anyone quotes (a).** That calculation is the precision of
*one* strategy's Sharpe against an unknown truth. It is **not** the precision of the *difference*
between two candidates evaluated on the same six years, and the difference is what the gate
actually decides on. Two books built from the same signal on the same universe have return series
correlated near 1, and for highly correlated series `SE(ŜR_A − ŜR_B)` is far smaller than
`√2·SE(ŜR)` — potentially by an order of magnitude. Lo does not derive that paired standard error,
so this note **cannot** conclude that the ladder's steps are statistically meaningless, and any use
of it that does is overreach. What it does establish is the weaker but still decisive point: the
gate is comparing point estimates whose *individual* precision is far coarser than the differences
being adjudicated, so the ladder's total movement is not evidence about the population Sharpe of
any candidate. Deriving the paired standard error is a named gap and is recorded in the open
questions.

**(c) A free diagnostic the lab has not run, and it may bias every annualised number in the
repo.** Every Sharpe here is presumably annualised from daily returns by `√252`. Lo's `η(q)` says
that is correct only under zero serial correlation. A monthly-rebalanced book with hysteresis
bands, forward-filled constant weights between rebalances, and six overlapping formation vintages
has every structural reason to produce autocorrelated daily returns — and `learnings.md` has
already established that `sanitize_weights` holds the weight vector exactly constant between the 88
emitted rows, which makes the book a fixed portfolio for ~18 trading days at a stretch. Measuring
`ρ̂_1 … ρ̂_k` on the stored validation return series and computing `η(252)` costs nothing, scores
no returns, and answers whether the repo's headline statistic carries a systematic bias — and in
which direction. If `ρ̂_1 > 0`, every annualised Sharpe in the repo is **overstated**.

**(d) It sharpens, without resolving, the ⚠ standing protocol concern.** That concern is that
validation Sharpe has risen monotonically while holdout Sharpe fell. This note supplies the missing
piece of the framing: the gate reads a statistic whose sampling error on a six-year window is large
relative to the increments it adjudicates, and it reads it as if it were the population value. That
is not a claim the gate is broken — `program.md` defines the objective and the engine computes it
correctly — but it is the standard-error account of why a six-year window can be, in
`learnings.md`'s own words, "a *weak* discriminator." It also gives the train-split observation
recorded there a statistical reason rather than only a correlation: the train split has ~14,261
days against validation's ~1,562, so a Sharpe estimated on it has roughly **three times smaller**
standard error, which is exactly what one would expect of a column that tracks the holdout better.
That is an argument for the human weighing the concern; it is not licence for any session to select
on train, which `program.md` forbids.

**(e) Reading item 2 of the mechanism against this repo's own numbers.** For a book with Sharpe
near 1.2, `1/(1 + ½·1.2²) = 58%` of the estimator's asymptotic variance comes from the mean and
the remaining **42% from the volatility estimate** — against 3% at a Sharpe of 0.25. So on a book
this good, a construction change that alters realised volatility moves a substantial share of the
statistic's *noise*, not only its level, and the share grows with every step up the Sharpe ladder.
Worth remembering for the candidates in `learnings.md` recorded as having "raised Sharpe through
the denominator."

## Related

- `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md` — the same sample-size conclusion
  from the growth literature, via time-to-dominance rather than standard errors: two strategies
  with modestly different edges need enormous samples to separate, and the requirement scales
  sharply with the volatility of the better one.
- `notes/2026-08-23-geometric-mean-maximization-fallacy.md` — the companion argument that log
  growth is not this statistic's currency; together the three notes say the folder's imports and
  the lab's gate are denominated differently *and* the gate's own denomination is imprecise.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the other external justification for
  discounting an in-sample statistic.
- `notes/2026-08-20-parametric-portfolio-policies.md` — the mechanism by which selecting on a
  sample objective with too little curvature picks the high-variance candidate; this note supplies
  the size of the noise that selection is operating on.
- `experiments/learnings.md` — the ⚠ standing protocol concern, and the note that
  `experiments/trial_returns/` makes decompositions of stored return series free.
