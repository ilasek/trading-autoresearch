---
title: "Estimating and Testing Linear Models with Multiple Structural Changes" / "Optimal Detection of Changepoints with a Linear Computational Cost" — how a sample is split into segments at dates nobody specified in advance, exactly rather than greedily, and what the resulting split is and is not evidence of
authors: Bai, Perron (1998); Killick, Fearnhead, Eckley (2012)
year: 1998; 2012
venue: Econometrica 66(1), 47–78 (venue tier 1); Journal of the American Statistical Association 107(500), 1590–1598 (venue tier 1)
url: https://doi.org/10.2307/2998540 ; https://doi.org/10.1080/01621459.2012.737745
citations: 4623 and 2312 (Crossref `is-referenced-by-count`, both checked 2026-10-22, both resolved on the first call). The Bai–Perron companion paper on computation (Journal of Applied Econometrics, `10.1002/jae.659`) carries a further 4445; it was not read and nothing below is attributed to it.
sample_period: none in the statistical sense — both are methods papers. Bai–Perron's asymptotics are supplemented by Monte Carlo (10,000 replications) and two macroeconometric illustrations; PELT's evidence is simulation plus genomic and oceanographic data examples. No market return data of any period appears in either, and no dated empirical claim from either is recorded here.
markets: none
tier: A
validation_overlap: false
published_post_2018: false
read: Bai–Perron from the authors' MIT working-paper version (MIT Dept. of Economics WP 95-17, Sept. 1995), fetched as the Internet Archive's OCR text layer `estimatingtestin00baij_djvu.txt` (142 KB, 1091 instances of `" the "`), which is the pre-publication version of the 1998 Econometrica article; section numbering and proposition numbering below are that version's. PELT from `arxiv.org/pdf/1101.1438` (v3 of 9 Oct 2012, 1.06 MB → 55 KB of clean text via `pdftotext -layout`, 316 instances of `" the "`, no ASCII shift, no `( )` math dropout, title line verified). Andrews (1993), which both papers build on and which is the natural third leg of this cluster, was **not obtained** — see the companion note `2026-10-22-breakdate-inference-unknown-timing.md` for what was and was not read about it.
---

## Mechanism

No economic mechanism — this is machinery, and it is the first note in this folder on the
**detection** half of the regime question. `program.md` charters regime switching inside
`price-trend`, and the folder has 57 notes that mention regimes; it has had **zero** on the
estimators that decide where a regime boundary is. That gap is why this note exists, and the
shape of the gap matters: the lab's own regime work has always been *a signal* (a trend filter,
a volatility trigger, a binary switch), never *a measurement*. These two papers are measurement.

The object both papers estimate is the same, and stating it in one line is most of the value.
Given a series `y_1:n` and a cost function `C(·)` that scores how badly a single segment is
described by one constant parameter vector, choose the number `m` and the locations
`τ_1 < … < τ_m` that minimise

    Σ_{i=1..m+1} C( y_{(τ_{i-1}+1) : τ_i} )  +  β·f(m)

The first term rewards splitting; the penalty `β·f(m)` is what stops the minimiser from putting
a break between every pair of adjacent observations. Essentially every changepoint method in use
— penalised likelihood, least squares with breaks, minimum description length — is this
objective with a different `C` and a different penalty. Bai–Perron is the econometric treatment
with `C` = segment sum of squared residuals from a linear regression; PELT is the algorithmic
treatment for general `C` with a penalty **linear in `m`**.

The reason this is a different object from a timing overlay deserves saying plainly, because it
is the condition under which this vein was worth reading at all. A changepoint estimator does not
produce a position. It produces a *claim about when a parameter changed*, together with an
interval of dates consistent with that claim. It is a diagnostic about a sample, and the honest
uses of it are retrospective.

## Construction recipe

### Bai–Perron: the econometric layer

**The model.** `y_t = x_t'β + z_t'δ_j + u_t` for `t` in regime `j`. The `δ_j` shift at each break;
`β` does not. With `x_t` empty this is the **pure** structural change model (everything shifts);
with `x_t` non-empty it is the **partial** model, which matters because it lets you ask whether
*one particular* coefficient broke while holding the rest fixed.

**Estimating break locations.** The estimator is the global minimiser of the total SSR over all
admissible partitions. The naive search is `O(T^m)`; the paper's dynamic-programming recursion
does it in **`O(T²)` least-squares operations at most, for any number of breaks**. The recursion
is the standard one: precompute the SSR of every contiguous segment, then solve for the optimal
partition of `y_1:s` in terms of the optimal partition of `y_1:t` for `t < s`.

**Trimming is not optional and it is a real parameter.** Admissible break fractions are restricted
to

    Λ_ε = { (λ_1,…,λ_k) : |λ_{i+1} − λ_i| ≥ ε,  λ_1 ≥ ε,  λ_k ≤ 1 − ε }

for some `ε > 0`. Breaks cannot sit near the sample boundaries or near each other, because there
would not be enough observations to identify the subsample parameters. Hansen's exposition (the
companion note) records the conventional range as **`ε` between 5% and 15%**. Every critical value
below is a function of `ε`, so `ε` must be fixed *before* looking and reported.

**The partial model needs an iterative scheme.** The DP recursion cannot be applied directly when
`β` is common across regimes, because the optimal partition and the estimate of `β` each depend on
the other. Bai–Perron use Sargan's alternating minimisation: minimise over the break dates holding
`β` fixed (this is a pure-structural-change DP step on `y_t − x_t'β`), then regress to update `β`
holding the partition fixed, and iterate; each iteration decreases the objective. The recommended
start is to run the pure model first and take `β` from the regression on that partition.

**Testing.** Three tests, in increasing order of how little you have to assume:

- `supF_T(k; q)` — tests no break against exactly `k` breaks, where `q` is the number of
  coefficients allowed to shift. It is the ordinary `F` statistic for equality of the `δ_j`,
  maximised over `Λ_ε`. For `k = 1` this is the statistic of Andrews (1993); Bai–Perron's
  contribution is the generalisation to `k > 1` and the tables, which they simulate (10,000
  replications) for up to 9 breaks and up to 10 shifting regressors.
- `DmaxF_T(M, q)` — the **double maximum** test: no break against *an unknown* number of breaks up
  to a bound `M`, taking `max_{1≤m≤M} supF_T(m; q)`. Each `supF_T(m;q)` is divided by `m`, which
  the authors describe as an implicit prior accounting for a fixed sample becoming less informative
  as `m` grows. They report that critical values vary little for `M` above 5.
- `F_T(ℓ+1 | ℓ)` — the sequential test of `ℓ` breaks against `ℓ+1`, which is how you choose `m` in
  practice: fit `ℓ` breaks, test for one more inside each existing segment, stop at the first
  failure to reject.

**The sequential procedure is not consistent for the number of breaks at fixed size, and the
paper says so.** Run at a fixed level `α`, it over-selects: the asymptotic probability of choosing
`m_0 + j` breaks is `α^j`. That decays fast, which is why the authors still prefer it to an
information criterion (you never have to fit models with more breaks than the truth), but the
estimate is biased upward by construction. Consistency requires letting `α_T → 0` slowly with the
sample (their Proposition 9).

**Confidence intervals for the break dates, which are the output most worth having.** The break
*fractions* converge at rate `T` — faster than the usual `√T`, which is what makes dating feasible
at all. Under uncorrelated errors the limiting distribution of the scaled break-date error is
`argmax_s { W(s) − |s|/2 }` for a two-sided Brownian motion `W`, whose CDF is available in closed
form (Yao 1987); Bai–Perron quote the **95% quantile as 7.7 and the 97.5% quantile as 11.0**.
Building the interval needs consistent estimates of the segment second-moment matrix, the error
variance, and the **magnitude of the coefficient shift at that break** — and that last dependence
is the whole story: the interval's width scales inversely with the squared size of the break. With
serial correlation present, the limiting distribution changes and the long-run variance must be
estimated by a kernel method (Andrews 1991); with trending regressors it changes again.

### PELT: the algorithmic layer

**What it adds.** Bai–Perron's DP is `O(T²)`. The classic exact alternatives are worse: Segment
Neighbourhood is `O(Qn²)`, which is cubic when the number of changepoints grows with `n`. The
universally-used cheap alternative, **Binary Segmentation** — find the single best break, split,
recurse on each half, stop when no split improves the objective — is `O(n log n)` but is
**approximate**: it is a greedy search, and nothing guarantees its answer is the minimiser of the
objective it is nominally optimising.

**The pruning result (Theorem 3.1).** Assume there is a constant `K` such that for all `t<s<T`

    C(y_{(t+1):s}) + C(y_{(s+1):T}) + K  ≤  C(y_{(t+1):T})

(i.e. splitting never increases cost by more than `K`; for a negative-log-likelihood cost `K = 0`).
Then if

    F(t) + C(y_{(t+1):s}) + K  ≥  F(s)

holds at time `s`, the candidate `t` can **never** be the optimal last changepoint at any future
time `T > s`, and can be deleted from the candidate set permanently. Dropping pruned candidates
from the optimal-partitioning recursion gives Pruned Exact Linear Time — exact, and `O(n)` under
mild conditions on how segment lengths are distributed.

**Penalty choice is the free parameter and it is where the judgement lives.** PELT's basic form
requires `β·f(m)` linear in `m`, i.e. `f(m) = m`. The standard choices are AIC (`β = 2p`) and
SIC/BIC (`β = p·log n`), with `p` the number of parameters added per changepoint. For a concave
`f`, the paper gives a fixed-point trick: run PELT with constant `γ = f'(1)`, get `m_0`, re-run
with `γ = f'(m_0)`, iterate to convergence.

**Two honesty points the authors volunteer, both worth carrying.** First, **PELT is not in practice
faster than Binary Segmentation** — their argument for it is exactness, not speed. Second, the
accuracy gap between exact and greedy segmentation is **large when the number of changepoints grows
with the sample and negligible when the number is fixed**. If you expect one or two breaks in a
fixed window, Binary Segmentation gives you the same answer for less work; the exact algorithm earns
its keep when breaks accumulate with sample length.

## Robustness evidence (qualitative only)

Both are methods papers, so "robustness" means the conditions under which the theory holds rather
than out-of-sample survival, and both are unusually explicit about those conditions.

Bai–Perron's asymptotics require the breaks to be asymptotically distinct and interior (the `ε`
trimming), and the limiting distributions change — not merely shift — in the presence of serial
correlation, heteroskedasticity, and trending regressors. The critical values are simulated, not
analytic, and are indexed by `(k, q, ε)`. The method has been absorbed into applied econometrics
to the tune of several thousand citations across both the theory and computation papers, and the
sequential-testing strategy it recommends is the standard one; its known weakness, stated by the
authors rather than by critics, is the inconsistency of that strategy at fixed test size.

PELT's exactness is a theorem, not an empirical claim, and the linear-time result is conditional:
it needs the number of changepoints to grow roughly linearly with `n`, and it needs the cost
function to satisfy the sub-additivity condition (which the authors note almost all costs used in
practice do). Their simulations compare against both exact competitors and Binary Segmentation on
change-in-variance and change-in-mean problems; the authors report the accuracy advantage over
Binary Segmentation as substantial in the growing-`m` regime and negligible in the fixed-`m`
regime, which is a limitation they could have buried and did not.

Neither paper has been through a finance replication exercise of the Hou–Xue–Zhang or
Jensen–Kelly–Pedersen kind, because neither proposes a finance effect. The relevant decay question
(McLean–Pontiff) does not apply: an estimator does not get arbitraged away.

## Implementability here

**Runtime is a non-issue and that is unusual for this folder.** PELT is `O(n)` and Bai–Perron's DP
is `O(T²)` in segment-SSR evaluations, on a *single series* of at most a few thousand daily
observations. Both are comfortably inside the protocol's ~60s-per-call budget even if run per
instrument; the `O(T²)` precompute on a 6,000-day series is a few tens of millions of flops.
`scipy`/`numpy` is enough — neither needs a package the repo lacks. Nothing here is a heavy learner.

**The use that fits the lab's rules, and it is a diagnostic rather than a candidate.** The protocol
already reports train skill for **1997–2008 and 2009–2017 separately**. Those boundaries were chosen
by a human. Hansen's companion exposition shows exactly what is wrong with that: a pre-chosen split
date is a Chow test with a breakdate picked from a known feature of the data, and two split dates a
short distance apart can give opposite answers. The directly useful application of these two papers
is therefore to ask, of the lab's own existing return series, **where a break-date estimator puts
the break and how wide the interval around it is** — and specifically whether the lab's two reported
train subperiods are a split the data supports, or an interval-free convention. This costs no trial,
reads no holdout, and the likely answer (the confidence interval is wide enough to contain several
plausible splits) is itself a recordable finding about how much weight the subperiod decomposition
can bear.

**Where it must not go, and the lab has already paid for this lesson three times.**
`experiments/learnings.md` records three de-risking overlays — inverse-vol plus vol targeting, a
per-asset 200dma trend filter, and a **binary SPY-trend regime switch** — that all cut train-period
drawdown and all lost more validation Sharpe than they saved, via dilution and whipsaw. A
changepoint estimator wired to a position is the fourth member of that family, and nothing in these
two papers argues it would fare differently. The reason it would not is in the companion
Ang–Timmermann note: real-time regime inference both lags and false-alarms, and false alarms are
whipsaw. **If a candidate comes out of this vein, the burden is to show it is not a timing overlay.**

**Three pitfalls specific to using these estimators on this panel.**

1. **A break found by maximising a statistic over candidate dates does not have the null
   distribution of a break at a date you specified.** This is the same post-selection problem
   `SUMMARY.md` already tracks under "what a selected maximum is worth", arriving from a new
   direction, and it is the subject of the companion note. Using a `χ²` critical value on a
   `supF` statistic overstates significance by roughly a factor of two in the critical value.
2. **The trimming parameter `ε` is a researcher degree of freedom with teeth.** It determines which
   dates are even admissible, and every critical value is conditional on it. Fix it first.
3. **The penalty, not the data, chooses the number of breaks.** AIC and BIC give different answers,
   and the sequential-test route over-selects at fixed size. Any statement of the form "there are
   `k` regimes" is a statement about `β` as much as about the series — which is the same shape as
   this folder's standing warning that a count of selected features is a property of the selector.

**One construction that is genuinely new to this lab, if a candidate is ever wanted from here.**
Both papers treat *change in variance* as a first-class target, not only change in mean — PELT's
simulations are largely change-in-variance, and Bai–Perron's partial model can hold the mean fixed
and let only the scale shift. The lab's regime attempts have all been mean/trend objects. A
segmentation of the **cross-sectional dispersion** or **realised covariance** series, used to define
an estimation window rather than an exposure, would be a different use of the machinery, and it
connects to the existing note `2026-08-17-averaging-over-estimation-windows.md`, whose
Pesaran–Timmermann result is precisely about choosing an estimation window when breaks are present.
That is the natural composition and it is already half-covered here.

## Related

- `2026-10-22-breakdate-inference-unknown-timing.md` — the companion: what the null distribution of
  a maximised break statistic actually is, how wide break-date intervals really are, and why
  bootstrap critical values beat asymptotic ones here. Read the two together.
- `2026-10-22-regime-switching-financial-markets.md` — the other half of the vein: Markov-switching
  rather than discrete-break, and the filtered-versus-smoothed lookahead trap that applies to both.
- `2026-08-17-averaging-over-estimation-windows.md` — Pesaran–Timmermann on estimation-window choice
  under breaks. The natural downstream use of a break estimate, and already in the folder.
- `2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the standing alternative to
  detecting a break at all: average over windows/models instead of selecting one. On this lab's
  record, averaging has repeatedly beaten switching.
- `experiments/learnings.md`, "De-risking overlays on momentum reliably backfire out-of-sample" and
  "Blending beats switching" — the two refutations any candidate from this vein has to answer. No
  tension with these papers, because neither paper claims a timing result; the tension would be
  created by the lab, not imported.
