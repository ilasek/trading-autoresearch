---
title: "Online Portfolio Selection: A Survey — with: On-Line Portfolio Selection with Moving Average Reversion (OLMAR)"
authors: Li & Hoi (survey); Li & Hoi, extended as Li, Hoi, Sahoo & Liu (OLMAR)
year: 2014 (survey); 2012 (ICML), 2015 (journal version)
venue: "ACM Computing Surveys 46(3), article 35 (venue tier 2 — peer-reviewed CS survey, not a finance tier-1 outlet); ICML 2012 proceedings, extended as Artificial Intelligence 222, 104–123 (venue tier 2)"
url: "https://doi.org/10.1145/2512962 (full text read from the authors' preprint, https://arxiv.org/pdf/1212.2129) · https://doi.org/10.1016/j.artint.2015.01.006 (ICML version read in full from https://arxiv.org/pdf/1206.4626)"
citations: "Survey: 158 (Crossref is-referenced-by-count, checked 2026-10-17). OLMAR journal version: 132 (Crossref, same date)"
sample_period: "The field's four canonical panels, used by both sources: a 36-name US daily panel 1962–1984 and its 23-name continuation 1985–2010; a 30-name US panel 2001–2003; an 88-name Canadian panel 1994–1998"
markets: "US and Canada; blue-chip / index-constituent names only, by the authors' own account"
tier: "B. The survey is a careful, well-cited taxonomy whose chief value here is its explicit statement of the field's modelling assumptions and its own list of open problems — it is honest about what the literature does not do. OLMAR is a complete and clearly specified construction. Both fall short of A on the evidence axis for reasons set out below, all of them structural rather than incidental: costs enter only as an ex-post check, the scoring metric is undiscounted compounded wealth, parameters are chosen on the same panels the significance tests are run on, multiple testing is not acknowledged, and the canonical panel is survivorship-conditioned by construction"
validation_overlap: false
published_post_2018: false
---

## Mechanism

The survey's taxonomy is the reason to read it, and it splits the family by **the direction in
which weight is transferred**:

| Category | What it does | Members |
|---|---|---|
| Benchmarks | buy-and-hold, uniform CRP, best-stock, best CRP (hindsight) | — |
| **Follow-the-Winner** | raise the weight of better-performing assets | Cover's universal portfolio, EG, ONS, follow-the-leader |
| **Follow-the-Loser** | raise the weight of worse-performing assets | Anticor, PAMR, CWMR, **OLMAR**, RMR |
| Pattern-Matching | locate similar historical windows, optimise within them | BK, BNN, CORN |
| Meta-Learning | combine the above as experts | ONS-style aggregators, buy-and-hold over experts |

**Two branches of one literature make opposite trades on the same data and both report winning on
overlapping panels.** The survey records that EG "always performs far behind" the reversion methods
on these panels, and that PAMR and CWMR "suffer from dramatic failures" on one of them. This is the
folder's 2026-10-10 detector — *a family charter with two branches predicting opposite observables* —
arriving unprompted from a source. The right response is not to pick a branch by reported
performance but to ask what each needs to be true.

**The Follow-the-Loser mechanism is mean reversion, and the survey derives a result the lab should
already care about: a constant-rebalanced portfolio *is* a Follow-the-Loser strategy.** Their
Example 3.2, on the Cover–Gluss toy market: a uniform CRP whose holdings drift to `(1/3, 2/3)` after
a period restores `(1/2, 1/2)` by selling the winner and buying the loser, and does so every period.
"In a word, CRP implicitly assumes that if one stock performs poor (good), it tends to perform good
(poor) in the subsequent period, and thus transfers the weights from good-performing stocks to
poor-performing stocks." **So the v3 equal-weight eligible pool — the uniform CRP — is the simplest
member of this branch, and OLMAR is that same wealth transfer amplified** by replacing "restore
fixed weights" with "overweight whatever is furthest below its moving average".

**OLMAR's own contribution is the horizon of the reversion target.** Earlier reversion methods
(PAMR, CWMR) predict `p̃_{t+1} = p_{t−1}`, a single-period reversal, which the authors identify as the
reason those methods fail badly on one panel. OLMAR predicts reversion to a `w`-day moving average
of the price instead: `p̃_{t+1} = MA_t(w) = (1/w)Σ_{i=t−w+1..t} p_i`, expressed in price relatives as

    x̃_{t+1}(w) = (1/w) · ( 1 + 1/x_t + 1/(x_t x_{t−1}) + … + 1/(Π_{i=0..w−2} x_{t−i}) )

i.e. **the ratio of the trailing `w`-day average price to today's price**, computed from price
relatives alone. A name trading below its own moving average gets a predicted relative above one.

**The update is a passive–aggressive step with a Euclidean trust region**, which is the Follow-the-
Loser analogue of the relative-entropy step in `notes/2026-10-17-exponentiated-gradient-portfolio-update.md`:

    b_{t+1} = argmin_{b ∈ Δ_m} ½‖b − b_t‖²   s.t.   b · x̃_{t+1} ≥ ε,     ε > 1

Minimum movement from the current book, subject to the predicted return clearing a threshold. If
the current book already clears it, nothing trades. Otherwise the closed-form solution (before the
simplex constraint) is

    b_{t+1} = b_t + λ_{t+1} (x̃_{t+1} − x̄_{t+1}·1),
    λ_{t+1} = max{0, (ε − b_t·x̃_{t+1}) / ‖x̃_{t+1} − x̄_{t+1}·1‖²},     x̄_{t+1} = (1/m)·1′x̃_{t+1}

followed by a Euclidean projection onto the simplex. The step is a **cross-sectionally demeaned,
dispersion-normalised tilt**: names with above-average predicted relatives gain weight, below-average
lose it, and the denominator is the cross-sectional dispersion of the predictions, so a day on which
all names agree produces a large step and a dispersed day a small one. Linear time in `m`.

## Construction recipe

1. Parameters: reversion threshold `ε > 1`, window `w ≥ 3`. The paper's choices are `ε = 10`,
   `w = 5`, chosen "empirically… which provide a consistent results for OLMAR in all cases".
2. Initialise `b₁ = (1/m)·1`.
3. Each day: observe `x_t`; compute `x̃_{t+1}(w)` by the telescoping formula above; compute `x̄` and
   `λ`; take the step; project onto the simplex (Duchi et al.'s linear-time projection).
4. **Expert aggregation, `BAH_W(OLMAR)`.** Because performance is sensitive to `w`, run one OLMAR
   per `w ∈ {3,…,W}` (the paper uses `W = 30`, so 28 experts) and hold them buy-and-hold, weighted
   by their own accumulated wealth — the same no-meta-turnover device as Blum–Kalai's randomised
   universal portfolio. The paper also reports `MAX(OLMAR)`, the best single expert, and labels it
   **in hindsight**.
5. The authors' reported sensitivity: wealth "sharply increases when `ε` approaches 1 and flattens
   when `ε` crosses a threshold"; in `w`, performance rises, "spikes with a data-dependant value, and
   then decreases", with the buy-and-hold-over-experts version smoothing that dependence.

**One derivation this folder adds, because it changes the implementability verdict and is not in the
paper.** At the recommended `ε = 10`, the constraint `b·x̃ ≥ 10` demands a predicted one-day gross
return of ten times capital, which no cross-section of daily price relatives can supply. So
`λ = (ε − b_t·x̃)/‖x̃ − x̄1‖²` has a numerator pinned near `ε − 1 ≈ 9` and a denominator that is the
(small) squared dispersion of predicted relatives — `λ` is therefore large on every single day, the
pre-projection step leaves the simplex by a wide margin, and **the simplex projection is what
actually determines the book: a sparse, near-vertex portfolio concentrated on the few names furthest
below their moving average, rebuilt daily.** `ε` is described as a threshold but at the recommended
value it is a saturation switch, which is exactly what the paper's own flat-above-a-threshold
sensitivity curve reports. Practical reading: **this construction is near-100% daily turnover and
maximal concentration by design, and `ε` near 1 is the only setting at which it is anything else.**

## Robustness evidence (qualitative only)

The useful evidence here is about what the evaluation assumes, and both sources are explicit.

- **The survey states the field's model assumptions in three lines, and the second one is decisive
  for this lab.** Verbatim: "(1) Transaction cost: we assume no transaction costs/taxes in the
  model; (2) Market liquidity: we assume that one can buy and sell any quantity of any asset **in
  its closing prices**; (3) Impact cost: we assume market behavior is not affected by any portfolio
  selection strategy." Assumption (2) is a same-close fill — the convention protocol v3 abolished.
- **The scoring metric is undiscounted compounded wealth.** OLMAR: "we adopt the most common metric,
  cumulative wealth… Results with other metrics, including risk-adjusted return, will be included in
  the long version of this paper." A daily-rebalanced book scored by compounding a daily
  cross-sectional average is precisely the estimator
  `notes/2026-10-03-caveat-compounder-daily-rebalancing-bias.md` measures an upward bias in, and the
  bias grows with the number of names and the dispersion — which is the regime this construction
  deliberately occupies.
- **Costs enter only as an ex-post scalability check, never into the decision rule.** OLMAR reports
  break-even cost rates and concludes it "can withstand reasonable transaction cost rates"; the
  survey's own open-problems list says of the whole family that cost-aware models "can not be
  explicitly conveyed in an algorithmic perspective" and that extending the algorithms to account
  for costs is an open challenge. The optimisation that chooses the trade does not know costs exist.
- **Liquidity is unmodelled and the survey says so**: "although all published algorithms claim that
  in the back tests they choose blue chip stocks, which have the highest liquidity, it can not solve
  the concern of market liquidity… no algorithm has ever considered this issue in its algorithm
  formulation."
- **Parameters are selected on the panels the significance tests are then run on**, and multiple
  testing is not acknowledged anywhere in either source. The reported `t`-statistics are computed on
  the same four panels used to pick `ε` and `w`; `MAX(OLMAR)` is labelled as hindsight but reported
  alongside the rest. The folder's own machinery is the right discount
  (`notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-09-01-multi-signal-overfitting-critical-t.md`).
- **The canonical panel is survivorship-conditioned by construction.** The field's benchmark dataset
  is a few dozen names with a continuous multi-decade daily history — i.e. names selected for having
  survived the sample. The folder holds the direct results on what that does
  (`notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`,
  `notes/2026-10-01-survival-conditioning-induced-drift.md`,
  `notes/2026-10-02-delisting-returns-the-other-half-of-survivorship.md`), and this is the single
  largest unquantified discount on every number the family reports.
- **No independent replication of the reversion branch on a cost-and-execution-realistic panel** has
  been located by this folder. The authors' own cross-panel evidence is that reversion methods fail
  badly on at least one of four panels, which is itself the most informative robustness statement in
  the cluster: the mechanism is panel-dependent, and the branch's own proponents say so.
- **The i.i.d. premise is disavowed by this branch, deliberately.** The survey opens §3.3 by saying
  the best-CRP target's optimality rests on i.i.d. returns, "which however does not always hold for
  the real-world data and thus often results in inferior empirical performance" — so Follow-the-Loser
  is explicitly a bet *against* the assumption under which Follow-the-Winner's target is optimal.
  The two branches are not two implementations; they are two hypotheses about return autocorrelation.
- **McLean–Pontiff**: a decade-and-a-half-old, well-cited CS literature with public code and public
  datasets.

## Implementability here

**The verdict is an anti-candidate, and uniquely among this folder's anti-candidates the lab has
already run the measurement that refutes it, before reading the source.**

`experiments/learnings.md` [2026-10-08]: re-measured under v3, the two residual-reversion leads fell
to skill of −0.01 and +0.00 against the pool, with negative train skill in both sub-periods, and the
entry names what had been carrying them — **"fills at the close the signal was computed on (bid-ask
bounce on the last day of a 21-day reversal), free daily rebalancing, and one flat 15 bps on books
tilted toward illiquid, 71%-non-US, stamp-duty-paying names."** Those are, item for item, the
survey's assumptions (2), (1) and (1) again. **There is no tension between source and refutation:
read the assumption list and the two agree.** The same entry supplies the companion lesson — those
books still sat at the 99th–100th percentile of their random-selection null, because "random books
churned 22× a year pay the same costs and earn nothing; beating the null is not beating the pool."

Point by point against this repo's constraints:

- **Execution.** v3 fills a row emitted on date `d` at each name's first *real* close after `d`. The
  signal `x̃_{t+1} = MA_t(w)/p_t` is a function of the close on `d`, so the whole of the one-day
  component of the reversion is given away to the fill. At `w = 5` most of the predicted reversion
  *is* the one-day component. The construction does not survive the translation, and v3's release
  notes say this was the intent: "same-close mean reversion… [is] gone, by design".
- **Costs.** Near-full daily turnover at 15/20/30/40 bps per side plus UK and HK stamp duty and the
  French/Italian/Spanish FTTs. The lab's own calibration — a 1.3× turnover book pays ~14 bps/yr,
  while a 10.6× book lost 0.22 of skill to a cost doubling — puts a ~250× turnover book's cost drag
  far beyond any plausible gross edge.
- **Concentration.** The near-vertex book the `ε = 10` projection produces violates the 25% position
  cap outright; capping it turns the construction into "equal-weight the four most oversold eligible
  names", a rule whose turnover is unchanged and which the folder's concentration work says will be
  graded against a *wider* null (`notes/2026-10-15-random-portfolio-inference-concentration-of-measure.md`).
- **Panel mismatch, and it runs in the unhelpful direction.** The branch's own literature localises
  its effect to small blue-chip panels and reports failure on others; the v2 panel is nine large-cap
  national indices, so a null here would be weak evidence either way — the standing rule from
  `research/README.md` about mechanisms whose literature localises them outside this panel.
- **Non-synchronous closes.** A one-day cross-sectional reversion signal on a 15-region panel is
  partly measuring the stale-price autocorrelation of
  `notes/2026-09-08-nonsynchronous-trading-econometrics.md`, which v3's next-real-print fill rule
  removes from the tradeable side while leaving it in the signal.

**What is worth taking from the cluster, rather than discarded with it.** Three items, all of them
mechanism rather than signal.

1. **The CRP-is-reversion identity is the cleanest statement this folder has of what the v3 benchmark
   is doing**, and it closes a loop: the pool's rebalancing channel is a Follow-the-Loser bet
   (`notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md`), which has zero expected
   value under i.i.d. and pays only where relative prices mean-revert
   (`notes/2026-08-22-rebalancing-return-attribution-critique.md`) — and v3's fill rule denies
   candidates the one-day part of exactly that effect while the pool, being a slow monthly-ish
   restorer of equal weights, keeps whatever lives at longer horizons. **The benchmark is allowed a
   mechanism the protocol takes away from challengers at short horizons.** That is a structural
   observation about the lab's own grading, not a complaint, and it predicts the sign of a
   measurable quantity: the pool's advantage should concentrate in the slower part of the reversion.
2. **The passive–aggressive step is a reusable operator with no parameters to fit.** "Move the
   minimum Euclidean distance such that the predicted return clears `ε`" is a sensible answer to the
   trade-sizing question for *any* score, and at `ε` just above the book's current predicted return
   it is a genuine no-trade region — the dispersion-normalised cousin of the relative-entropy step.
   Taken at a sane `ε` it is a turnover control, and that is how the folder should file it.
3. **Buy-and-hold over experts is the free aggregator**, and it is the same device in three separate
   sources now (Blum–Kalai's random CRPs, `BAH(OLMAR)` over windows, the survey's meta-learning
   category). It costs no meta-level turnover, it needs no covariance matrix, and it is the exact
   shape `program.md` charters for `portfolio-learning`. The lookback-grid version of it is also
   where `notes/2026-10-16-calendar-effects-data-mining-robust-test.md`'s derivable-correlation rule
   (`#266`) applies, since the experts are averages over overlapping windows of one sample.

## Related

- `notes/2026-10-17-universal-portfolios-and-the-best-constant-rebalanced-portfolio.md` ·
  `notes/2026-10-17-exponentiated-gradient-portfolio-update.md` — the Follow-the-Winner branch, its
  guarantees, and the simplex all three share.
- `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` ·
  `notes/2026-08-22-rebalancing-return-attribution-critique.md` ·
  `notes/2026-08-21-diversification-return-and-rebalancing.md` — the rebalancing channel this branch
  amplifies, and the refutation of its unconditional version.
- `notes/2026-10-03-caveat-compounder-daily-rebalancing-bias.md` — why a compounded daily-rebalanced
  wealth figure is the wrong estimator for exactly this construction.
- `notes/2026-09-25-short-term-residual-reversal.md` · `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`
  — the finance literature on the same effect, with the liquidity-provision reading the CS literature
  lacks.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` ·
  `notes/2026-10-01-survival-conditioning-induced-drift.md` — the discount on the canonical panel.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md` — the stale-price component of any
  one-day cross-sectional reversion signal on this panel.
