---
title: "Volatility-Managed Portfolios" + replication challenge "On the Performance of Volatility-Managed Portfolios"
authors: Moreira, Muir (2017); Cederburg, O'Doherty, Wang, Yan (2020)
year: 2017, 2020
venue: Journal of Finance 72(4), 1611–1644 (venue tier 1); Journal of Financial Economics 138(1), 95–117 (venue tier 1)
url: https://doi.org/10.1111/jofi.12513 ; https://doi.org/10.1016/j.jfineco.2020.04.015
citations: Moreira–Muir (2017) 412; Cederburg–O'Doherty–Wang–Yan (2020) 94 (Semantic Scholar, checked 2026-08-17)
sample_period: Moreira–Muir 1926–2015 (shorter for later-starting factors); Cederburg et al. samples start 1926–1967 by factor and end December 2016
markets: US equity factors (market, size, value, momentum, profitability, investment, ROE, BAB), an FX carry factor, 94 additional US anomaly portfolios, and 20 OECD stock market indices in the Moreira–Muir appendix
tier: A
validation_overlap: false
published_post_2018: false (Moreira–Muir), true (Cederburg et al.)
---

## Mechanism

The claim is the cleanest possible statement of volatility timing, and it rests on an
asymmetry between two forecastability facts rather than on any market story.

A mean-variance investor holds a weight in a risky portfolio proportional to `μ_t / σ²_t`.
Volatility is **highly forecastable at short horizons** — it is variable and persistent, so
last month's realized variance is a usable estimate of this month's. Expected return is
**not** forecastable at those horizons, and in particular is only weakly related to
short-horizon variance forecasts. If `σ²_t` moves a lot and `μ_t` does not move with it, then
the optimal weight moves with `1/σ²_t`, and a rule that simply scales exposure by inverse
lagged variance captures a real time-varying risk-return trade-off without forecasting
returns at all.

The authors emphasise that this is *contrary* to the usual risk-premium story: their rule
takes **less** risk in recessions and crises, when volatility is high, and yet does not give
up average return. A standard risk-based model would say expected returns rise enough in bad
states to compensate for the higher variance; the empirical content of the paper is that they
do not rise proportionally. That is why the result is framed as a challenge to structural
models of time-varying expected returns rather than as a new risk premium.

A mechanically important corollary, easy to miss: **the gain is a function of how much
volatility varies.** If volatility were constant, the managed portfolio would be identical to
the buy-and-hold portfolio and the alpha would be exactly zero. The authors point to this
directly when explaining why their effect is weaker in subsamples where volatility varied
less. Volatility timing is not a signal about assets; it is a bet on the dispersion of the
variance process itself.

**The replication challenge attacks the empirical claim on three distinct fronts, none of
which is "the effect is not in the data".** Cederburg, O'Doherty, Wang and Yan reproduce the
spanning-regression alphas and then argue those alphas do not correspond to anything a
real-time investor can hold:

1. **Direct comparison.** Extended from nine factors to 103 equity strategies (9 factors + 94
   anomaly portfolios grouped into eight categories), volatility management "degrades and
   improves performance at about the same frequency". The handful of strategies where direct
   volatility scaling clearly wins — the market, momentum, and betting-against-beta factors —
   are exactly the ones the prior literature had already singled out, which is a selection
   pattern, not a pervasive phenomenon. Their economic reading of the roughly even split is
   that individual factors have a *generally positive* risk-return trade-off, i.e. `μ_t` does
   tend to move with `σ_t` for most strategies, which is precisely the condition under which
   volatility timing should not help.
2. **The spanning regression is not a portfolio.** A positive alpha from regressing the
   managed factor on the original one implies a combination strategy whose weights are the
   regression coefficients — estimated over the *full sample*. A real-time investor must
   estimate them from past data only. Implemented that way (expanding window, 120-month
   initial training period, standard leverage constraint, CRRA utility), the combination
   portfolios generally earn **lower certainty-equivalent returns and lower Sharpe ratios than
   simply holding the original unmanaged portfolio**.
3. **Why the real-time version fails: structural instability.** The spanning-regression
   parameters are not stable over time, so past-estimated combination weights are systematically
   wrong going forward. This is the same failure mode the ensembles note already records from a
   different literature — estimated weights are the expensive part — arriving here as the
   diagnosis of a specific published result.

## Construction recipe

The managed return in month `t+1` is

```
f_managed[t+1] = (c / σ̂²_t) * f[t+1]
```

- `f` is the buy-and-hold **excess** return of the portfolio being managed.
- `σ̂²_t` is the **realized variance of daily returns within month `t`** — the plain sum of
  squared daily returns, annualized by the day count, with no parameter estimation. The
  authors stress that this makes the rule real-time implementable. (An appendix shows a
  fitted log-variance forecasting model does somewhat better; the simple version is the
  headline.)
- `c` is a single constant that scales average exposure. It is chosen so the managed
  portfolio has the **same unconditional standard deviation as the unmanaged one**, which
  makes the two directly comparable and means any Sharpe difference is a mean difference.
- Rebalance cadence: monthly. Exposure changes once a month; nothing about asset selection
  changes.

Two construction details that matter far more for an implementer than the headline:

- **`c` is a full-sample constant.** Both papers state plainly that the investor does not know
  it in real time. Moreira–Muir argue this is harmless because Sharpe ratios and appraisal
  ratios are invariant to `c`; Cederburg et al. accept that for the *direct* comparison but
  show it is not harmless for the combination strategies, which is where the large in-sample
  gains lived.
- **The implied leverage is enormous in calm periods.** Cederburg et al. report the
  time-series distribution of the implied position `c/σ̂²_t`: the median sits near 1×, but the
  **99th percentile runs roughly 4.5× to 8.6× the unmanaged position** across the nine
  factors, while the 1st percentile is near 0.03–0.06×. The rule is not "de-risk in
  turbulence"; it is a two-sided rule whose upside half requires multiples of leverage.

Cost- and leverage-aware variants that Moreira–Muir themselves test (their transaction-cost
table) are the ones worth copying if the mechanism is attempted anywhere: scale by realized
**standard deviation** instead of variance, use a fitted expected variance instead of raw
realized variance, and — directly relevant here — **cap the scalar at 1 or at 1.5**
(`min(c/σ̂²_t, 1)`). Each reduces trading and therefore cost. Their cost assumptions span
roughly 1 bp to 14 bps per unit traded, calibrated from prior work including an allowance for
costs rising with volatility.

## Robustness evidence (qualitative only)

- **Sample robustness (original).** Multi-decade, spanning the full modern CRSP era, with
  point estimates positive in every 30-year subsample examined and across factor families
  including profitability, investment and q-factor variants; also present across a
  cross-country set of OECD stock-market indices in the appendix. Subsample strength tracks
  how much volatility varied, as the mechanism implies.
- **Robustness the original establishes against alternative explanations.** The strategy is
  shown not to produce fatter left tails or option-like payoffs, not to be explained by
  downside/disaster/jump risk or the variance risk premium, and to be distinct from
  cross-sectional low-risk anomalies (risk parity, betting-against-beta). It also survives
  their modeled transaction costs and hard leverage caps, and works through options with
  embedded leverage.
- **Replication status is the crux.** The effect *in-sample* replicates: Cederburg et al.
  explicitly confirm the spanning-regression alphas on a 10×-larger strategy set. What does
  not replicate is the **investor-relevant** version. This is a strong form of replication
  challenge — it grants the statistical result and denies the economic one — and it comes from
  a tier-1 venue, post-dating and directly targeting the original.
- **Known limits of the challenge.** Their real-time tests still find genuine gains for a
  minority of strategies, momentum among them. So the honest summary is not "volatility timing
  does not work" but "**volatility timing is not a general property of equity strategies, and
  its documented successes are concentrated in a few factors that were selected on that
  basis**".

## Implementability here

This is the first dedicated source for `program.md` family 3, and the verdict is largely
negative for reasons that are structural rather than empirical.

**Three hard blockers, in order of severity:**

1. **Gross leverage ≤ 1.0 removes the profitable half of the rule.** The implied position runs
   to several multiples of the base portfolio at the 99th percentile of the distribution, and
   the median sits at ~1×. Under a hard cap the achievable rule is `min(c/σ̂²_t, 1)` — the
   de-risking half only, which is the variant Moreira–Muir test explicitly and which
   correspondingly earns a smaller alpha than the uncapped version in their own table. This
   is the same one-sidedness the momentum crash-risk note already recorded, now confirmed with
   the source's own construction rather than inferred.
2. **The lab has already measured the long-only version of this mechanism, and it lost.** The
   trials record says the correctly-specified basket-own-volatility trim was *worse than
   deleting the overlay*. Read against this source, that is not a contradiction: Moreira–Muir
   scale a **factor** (a long-short spread) by **its own** variance; a long-only momentum
   basket's variance is dominated by market beta, so it rises in melt-ups as well as crashes.
   The trigger is measuring the thing being de-risked, which the lab identified independently
   as the wrong signal.
3. **The full-sample `c` is not available and matters more than the papers' framing suggests.**
   The invariance argument holds only for the *pure* scaled portfolio. The moment the rule is
   combined with an unmanaged leg — which is what a long-only book with a cash buffer actually
   is — the mixing weight is an estimated quantity, and that is exactly the parameter
   Cederburg et al. show is structurally unstable out of sample.

**What is worth keeping.** The mechanism-level condition for volatility timing to add value is
sharp and testable without a trial: **it pays only where conditional expected return does not
rise with conditional variance.** Cederburg et al.'s roughly even split across 103 strategies
is direct evidence that for most equity strategies it does rise, and the corollary is that a
volatility overlay's value cannot be assumed from the existence of the literature — it has to
be argued for the specific book. The lab's own defensive-cohort finding is a *different*
mechanism (a style-orthogonal, market-level stress proxy), and this source neither supports
nor undermines it.

**Pitfalls if any family-3 candidate is ever attempted.** (a) Do not import the alpha from
spanning regressions; that number is not a portfolio. (b) Do not use `1/σ²` sizing unbounded —
under a leverage cap the shape of the rule changes qualitatively, not just in magnitude.
(c) Prefer scaling by standard deviation over variance and capping the scalar, both of which
the source itself endorses on cost grounds. (d) Remember the effect is a bet on the dispersion
of the variance process, so a period or universe with stable volatility yields nothing by
construction.

## Related

- `2026-08-17-momentum-crash-risk-management.md` — the momentum-specific version of the same
  scaling idea; that note's short-leg argument and this note's leverage-cap argument are the
  two independent reasons the family does not transfer to a long-only book.
- `2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the structural-instability
  diagnosis here is the combination-puzzle mechanism reappearing as a replication failure.
- `2026-08-17-naive-vs-optimized-weighting.md` — same estimation-error law: the parameters you
  must estimate are where the out-of-sample loss comes from.
- Tension with `experiments/learnings.md`: the lab refuted inverse-vol weighting and basket-own
  vol trimming. Nothing here reopens either; the source's own replication literature and the
  leverage cap both point the same way.
