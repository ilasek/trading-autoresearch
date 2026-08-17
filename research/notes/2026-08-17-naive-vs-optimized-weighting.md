---
title: "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?" + rebuttal "In Defense of Optimization: The Fallacy of 1/N"
authors: DeMiguel, Garlappi, Uppal (2009); Kritzman, Page, Turkington (2010)
year: 2009, 2010
venue: Review of Financial Studies 22(5), 1915–1953 (venue tier 1); Financial Analysts Journal 66(2), 31–39 (venue tier 1 practitioner-academic)
url: https://academic.oup.com/rfs/article-abstract/22/5/1915/1592901 ; https://doi.org/10.2469/faj.v66.n2.6
citations: not verified this session (all scholar APIs and publisher domains egress-blocked); both are among the most-cited portfolio-construction papers of their decade, but no count was resolvable
sample_period: seven empirical datasets, monthly, mostly US, ending in the mid-2000s (exact spans not verified this session)
markets: US equity portfolios (industry, size/book-to-market sorts, factor sets) plus international index sets
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The question is what to do with the *weights* once the members of a portfolio are chosen, and
the answer is a statement about estimation error rather than about markets.

Mean-variance optimisation is optimal given the true means and covariances. In practice both
are estimated from a finite sample, and the optimiser is a maximiser: it loads on whichever
assets' *estimates* look best, which is systematically the assets whose estimation noise
happened to be favourable. The error is therefore not merely passed through, it is amplified.
The equal-weight (1/N) rule estimates nothing, so it contributes zero estimation error — it
is a biased but variance-free estimator of the optimal weights.

The paper's central empirical result: across seven datasets and fourteen optimisation models
— including Bayesian shrinkage, moment restrictions and other estimation-error corrections —
**none was consistently better than 1/N on Sharpe ratio, certainty-equivalent return, or
turnover**. Their analytic companion result quantifies why, and it is the number worth
remembering because it is a calibration rather than a realised performance figure: with
parameters calibrated to US equities, the estimation window a sample-based mean-variance
strategy would need in order to reliably beat 1/N is on the order of **3,000 months for 25
assets and 6,000 months for 50** — centuries of data. At any realistic sample length,
estimation error dominates the optimisation gain.

**The rebuttal sharpens rather than reverses this.** Kritzman–Page–Turkington argue the
result is an indictment of the *inputs*, not of optimisation: DGU feed the optimiser rolling
short-window (60–120 month) sample means as expected returns, which produce implausible
forecasts. Using longer-window estimates, or even naive-but-plausible non-sample assumptions,
optimised portfolios beat equal weight out of sample in their tests. The synthesis both sides
effectively agree on:

- **Expected returns are the fragile input.** Almost all of the damage comes from estimating
  means from short samples; covariance estimates are comparatively well behaved.
- **The cost of a weighting scheme scales with how many parameters it needs estimated**, and
  with how noisily each is estimated.
- **1/N is a genuinely strong benchmark**, not a straw man — any scheme that beats it must
  earn back its own estimation error.

## Construction recipe

Not a strategy so much as a decision rule for weighting schemes:

- **Baseline**: equal weight across the chosen names. Zero estimated parameters.
- **If deviating from equal weight, count the parameters you are estimating and where they
  come from.** A scheme driven by a directly observed cross-sectional quantity is cheap; a
  scheme requiring a full covariance matrix, or a return forecast per asset from a short
  rolling window, is expensive, and the expense grows with the number of assets relative to
  the sample length.
- **If expected returns must enter, do not use short-window rolling sample means.** Use a
  long-sample or structurally motivated estimate. This is the rebuttal's operative
  prescription and the one point where the two papers give actionable, compatible advice.
- Shrinkage / norm constraints / short-sale constraints all help, but in DGU's tests none
  helped enough to reliably clear 1/N.

## Robustness evidence (qualitative only)

- Multiple datasets, multiple competing models, and both an empirical and an analytic route to
  the same conclusion — this is one of the better-designed horse races in the literature.
- The result has been contested from the start (the rebuttal above, and a substantial
  follow-on literature on when optimisation does add value), which is itself evidence of
  scrutiny rather than of fragility. The contested part is the *conclusion for practice*; the
  mechanism (optimisers amplify estimation error in means) is not contested by anyone.
- Limits: the datasets are asset-class and portfolio-sort level, not single-name cross-sections
  of a hundred-plus instruments; and the comparison is about *unconditional* weighting, with
  no cross-sectional predictive signal in play. Neither paper studies signal-proportional
  weighting, which is the scheme this repo actually uses.

## Implementability here

The lab's strongest recorded weighting result — magnitude weighting, sizing positions in
proportion to a composite momentum z-score — sits *outside* the object these papers study, and
getting that boundary right matters:

1. **Magnitude weighting is not optimisation and does not inherit this warning.** It estimates
   no covariance matrix and forecasts no return level; it is a monotone transform of an
   observed cross-sectional score. Its effective estimated-parameter count is near zero, which
   is why DGU's argument does not condemn it, and it is a coherent reason why the lab's
   escalation from equal weight → rank weight → z-score magnitude weight kept working when so
   many "smarter" weighting schemes in the literature do not.

2. **It does condemn the direction the lab has already refuted twice.** Inverse-volatility
   weighting between sleeves, risk parity across the ETF sleeve, and anything that would size
   positions off an estimated covariance matrix are all in the expensive-parameter class.
   The lab's empirical refutations and this literature's estimation-error argument point the
   same way, which raises confidence that those closures are structural rather than
   sample-specific. **Treat any future proposal to weight by estimated risk quantities as
   requiring a new argument for why its estimation error is small, not merely a new backtest.**

3. **The strongest caution this source offers, stated plainly.** 1/N is a hard benchmark
   precisely because deviations from it usually pay for themselves in estimation error. The
   lab's magnitude weighting beat equal weight by a large margin on validation — a result
   which, against this prior, is notable enough to deserve scrutiny of *how* it wins.
   The learnings file already records the two facts that bear on this: validation maxDD widened
   monotonically with each concentration step, and one year dominates the validation window's
   P&L. A concentration lever that pays mostly through a single strong period is exactly the
   configuration where an apparently free improvement is really a shift along a risk axis the
   objective does not price. The lab's own square-root-dampening test cuts the other way (less
   concentration was worse on both Sharpe and DSR), which is real evidence the gain is signal
   rather than variance artifact — but that test explored one direction only. Record this as a
   standing caveat on the repo's best mechanism, not as a refutation of it.

4. **Scale note.** DGU's estimation-window arithmetic worsens with the number of assets
   relative to sample length. A ~145-instrument universe with a few decades of daily data is
   firmly in the region where covariance-based weighting is unreliable and signal-proportional
   or equal weighting is not. This is a structural fact about the repo's data, not a tuning
   question.

## Related

- `2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` and
  `2026-08-17-rebalance-timing-luck-tranching.md` — the other two legs of the
  portfolio-construction literature: which trades to skip, and when to trade. This note covers
  how much to hold.
- `experiments/learnings.md`: "Within-basket weighting scheme, not just membership/buffering,
  is a major untapped lever — and the direction matters" (the result this note contextualises);
  "Inverse-vol / risk-weighting between sleeves of unequal diversification always favours the
  more-diversified leg" (the refutation this note supplies an external mechanism for); and
  "The validation window is not a homogeneous sample" (the reason point 3 above is worth
  keeping live).
