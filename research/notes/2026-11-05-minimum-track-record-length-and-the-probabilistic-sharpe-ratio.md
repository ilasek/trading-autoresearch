---
title: "The Sharpe Ratio Efficient Frontier (Probabilistic Sharpe Ratio and Minimum Track Record Length)"
authors: Bailey, López de Prado
year: 2012
venue: The Journal of Risk 15(2), 3–44 — peer-reviewed field journal, venue tier 2 by this folder's rubric. The core results are closed forms derived off Mertens'/Christie's asymptotic variance of the Sharpe estimator, not an empirical regularity, and all three of the paper's own worked examples were reproduced to the printed decimal here (see Robustness), so the tier understates how checkable it is.
url: https://doi.org/10.21314/jor.2012.255 (working-paper record https://doi.org/10.2139/ssrn.1821643; full text read from the first author's own page, https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf, 46 pp.)
citations: 149 (Crossref, checked 2026-11-05); 187 (OpenAlex, same DOI, checked 2026-11-05). Semantic Scholar does not resolve the Journal of Risk DOI (checked 2026-11-05), and the SSRN record 10.2139/ssrn.1821643 carries only 10 Crossref cites — the split-record / "disbelieve a lone low count" pattern this folder has recorded repeatedly, so neither low number is the article's count.
sample_period: methodological — closed forms plus a Monte-Carlo study over 96,551 synthetic two-component Normal mixtures (1,000 draws each); one illustration applies the formulas to monthly hedge-fund style index returns, 2000–2011
markets: none material. The illustration uses HFR style indices purely to display PSR and MinTRL values; no market claim is made or recorded here
tier: B+
validation_overlap: false
published_post_2018: false
---

## Mechanism

The Sharpe ratio's **point estimate** carries no information about the third and fourth moments.
Its **sampling variance** does. The paper's engine is Mertens' (2002) asymptotic result — also
derived by Christie (2005) under the weaker assumption of stationary and ergodic returns, and
shown by Opdyke (2007) to be the *same* expression — that the estimated Sharpe ratio is
asymptotically Normal with

```
Var(ŜR)  =  (1 / (n−1)) · [ 1  −  γ₃·ŜR  +  ((γ₄ − 1)/4)·ŜR² ]
```

where `ŜR` is in the **sampling frequency's own units** (not annualized), `γ₃` is skewness and
`γ₄` is kurtosis (so `γ₄ = 3` under Normality and the bracket collapses to `1 + ŜR²/2`, which is
Lo's familiar form). Negative skew and fat tails *raise* the variance of the estimator; the
distribution that looks best by point estimate can be the one whose point estimate is least
trustworthy. The paper's first contribution is to read this probabilistically rather than as an
error bar:

```
PSR(SR*)  =  Prob[ SR > SR* ]  ≈  Z[ (ŜR − SR*)·√(n−1) / √(1 − γ₃·ŜR + ((γ₄−1)/4)·ŜR²) ]
```

`Z` the standard Normal CDF. PSR rises with the observed Sharpe, with the number of observations,
and with positive skew; it falls with fat tails. Because it is computed in the data's own
frequency, it needs no annualization convention — which matters for strategies that rebalance
irregularly, where an annualized Sharpe is partly a calendar artifact.

The second contribution, and the one this note is filed for, is the **inversion**. Asking "how
many observations do I need before I can claim, at confidence `α`, that the true Sharpe exceeds a
threshold `SR*`?" gives the **Minimum Track Record Length**:

```
MinTRL  =  1  +  [ 1 − γ₃·ŜR + ((γ₄−1)/4)·ŜR² ] · ( Z_α / (ŜR − SR*) )²        [observations]
```

This is a **design** object, not a correction. It is the smallest sample on which a stated effect
could be established at a stated confidence — i.e. a minimum detectable effect read in units of
sample size instead of units of effect — and every input is something a designer sets or measures
before the test: the gap to be detected, the confidence required, the sampling frequency, and the
non-Normality of the series.

Two structural readings the paper states explicitly:

1. **The requirement explodes as the gap narrows**, quadratically: `MinTRL ∝ (ŜR − SR*)⁻²`. A
   design that must resolve a half-size difference needs four times the observations.
2. **Non-Normality is a tax paid in time, and it can be bought back.** A manager with negative
   skew and fat tails is penalised relative to a Normal one, but the penalty is a longer required
   record rather than a lower score — the two are interchangeable in the formula.

## Construction recipe

- Compute everything in the **native frequency**. `ŜR` daily, `n` in days, `SR*` converted to
  daily (`SR*_annual/√252`). Annualize only for reporting.
- `γ₃`, `γ₄` are the sample skewness and kurtosis of the same return series (`γ₄` on the raw,
  not excess, convention — Normality is `γ₄ = 3`).
- `Z_α` is the one-sided Normal quantile: 1.645 at 95%, 1.282 at 90%.
- `SR* = 0` tests "any skill at all". Any other `SR*` tests "better than that benchmark level",
  which is the version this lab needs.
- **Frequency is not neutral, and the direction is counter-intuitive.** For the *same annualized*
  Sharpe, a higher-frequency series needs *less calendar time*, because the bracket's `ŜR²` term
  is small in native units. The paper's own worked case: an annualized `ŜR = 2` tested against
  `SR* = 1` at 95% needs 2.73 years of daily data, 2.83 of weekly (+3.7%), 3.24 of monthly
  (+18.7%). Hence its advice to report at the highest frequency at which the IID assumption is
  not violated — the gain is real but it is borrowed against that assumption.
- **The CLT floor the paper flags against itself.** Eqs. for PSR/MinTRL are asymptotic. A MinTRL
  that comes out below ~30 observations is not a licence to use 30 observations; the *moments fed
  into* the formula must themselves come from a long enough series, and the fourth moment needs
  the longest. The paper's own Monte-Carlo (Figures 3–4) finds estimation error in `γ₃` and
  especially `γ₄` carries both bias and scale effects, while the mean's error does not and the
  standard deviation's is biased toward *under*stating risk.

## Robustness evidence (qualitative only)

- **Not an empirical finding, so the replication question does not apply in its usual form; the
  relevant check is arithmetic, and it passes.** All three MinTRL examples printed in the paper
  reproduce exactly from the formula above, independently here: daily 2.731 years, weekly 2.829,
  monthly 3.240 (paper: 2.73 / 2.83 / 3.24). This also pins down the two parts of the formula a
  reader could plausibly get wrong — the additive `1 +` and the `(γ₄−1)/4` coefficient — which
  matters because the equation glyphs do not survive text extraction from any available copy.
- **The variance expression has three independent derivations** (Mertens 2002, Christie 2005 via
  GMM, Opdyke 2007 proving their equality), and Christie's holds under stationarity and ergodicity
  rather than IID — so the PSR/MinTRL machinery does not require IID returns, only the weaker
  condition. It *does* require that the series be a single, stationary regime; nothing in it
  handles autocorrelation in squared returns, which this folder's own Sharpe-inference note
  records as the usual case in practice.
- **Known boundary, stated by the authors.** MinTRL is derived for `N = 1`: a single track record
  being evaluated on its own. It says nothing about selection across many candidates, and the
  authors' own follow-up work says so in as many words. That is the complementary note filed
  tonight.
- The paper's other half — the "Sharpe ratio Efficient Frontier", a mean–variance optimization
  over PSR rather than SR — is **not** recorded here beyond this sentence: it requires a
  leverage/non-Normality parameterisation the lab has no use for at gross leverage ≤ 1.0.
- **Anti-lookahead note.** The paper's Section 6 reports PSR and MinTRL values for named hedge-fund
  style indices over a dated monthly window. None of those figures, rankings or style narratives
  are recorded here, and the sample ends well before this lab's validation window.

## Implementability here

**Status against the acceptance criterion this note was commissioned under** (admit a source only
if it yields a computable minimum detectable effect as a function of something the lab controls):
**it reaches, in closed form, and the controlled inputs are the number of observations, the
sampling frequency, the benchmark level and the required confidence.** What it does *not* supply
is the lab's own statistic, and the gap matters:

**1. MinTRL as printed is the wrong variance for v3.** v3 scores *skill* — the candidate's Sharpe
minus the equal-weight pool's **on the same days**. MinTRL treats `SR*` as a known constant. The
pool's Sharpe is estimated on the same sample, and estimated with a very high correlation to the
candidate's. Substituting the pool's realised Sharpe for `SR*` in the formula above is therefore
not conservative — it is simply a different experiment. The right variance is the paired one this
folder already holds (`notes/2026-08-24-testing-differences-of-sharpe-ratios.md`):

```
SE(skill)  ≈  √( 2·(1 − ρ) / T )        annualized, to first order in Sh
```

with `ρ` the correlation between the candidate's and the pool's daily return series. The useful
move is to keep MinTRL's *inversion* and swap its variance:

```
MDE(skill)  =  (Z_α + Z_power) · SE(skill)        [minimum detectable skill]
T_required  =  2·(1 − ρ) · ( (Z_α + Z_power) / Δ )²     [observations, for a target skill Δ]
```

**2. The number the design question was asking for.** At the lab's validation width
(`T = 1562` daily observations, the figure the folder's own Sharpe-difference note uses) and a
one-sided 95% test, the minimum detectable skill is governed almost entirely by `ρ`:

| `ρ` (candidate vs pool) | `SE(skill)` | MDE at 50% power | MDE at 80% power |
|---|---|---|---|
| 0.99 | 0.057 | 0.094 | 0.142 |
| 0.98 | 0.080 | 0.132 | 0.200 |
| 0.95 | 0.127 | 0.209 | 0.316 |
| 0.90 | 0.180 | 0.296 | 0.448 |
| 0.80 | 0.254 | 0.418 | 0.633 |

(My arithmetic from the formula above; `Z_0.95 = 1.645`, `Z_0.80 = 0.842`.) Two consequences, both
decision-relevant and neither of them in the source:

- **The conventional reading of a confidence interval is a 50%-power statement.** "Is the interval
  clear of zero?" asks whether the *observed* effect is significant, which is detectability at
  coin-flip power. Requiring 80% power multiplies the required observations by
  `((1.645+0.842)/1.645)² = 2.29` — i.e. **the lab's validation window would have to be 2.3× longer**
  to detect, with 80% confidence of detecting it, the smallest skill its intervals currently call
  significant. Any statement of the form "the design could have seen it" should name which of the
  two it means.
- **Detectability is a ratio, not a level, and that is a real tension with the diversification
  rule.** A candidate that is a small tilt on the pool has a tiny `SE` and so a tiny MDE; a
  structurally different book has three to four times the MDE. But a small tilt also has a small
  attainable skill. The question a candidate's design has to answer is therefore not "is this
  different from the pool" but **"does its attainable skill grow faster than `√(1−ρ)`?"** —
  computable before any trial from the intended tilt's size. `program.md`'s instruction to spend
  the budget across families is a mandate about *what to learn*, and this is a statement about
  *what can be measured*; they pull in opposite directions and the trade-off is the human owner's
  to make, not this folder's.

**3. The non-Normality term is a free, unused screen.** v3 reports a bootstrap interval, which
absorbs skew and kurtosis implicitly. MinTRL's bracket makes the same information explicit and
one-dimensional: `1 − γ₃·ŜR + ((γ₄−1)/4)·ŜR²` evaluated on a candidate's own daily active-return
series says, in a single number, how much longer a record this construction needs than a Normal
one with the same Sharpe. It costs nothing to print alongside the interval, and it is the natural
place to catch the construction classes this lab keeps building — short-horizon reversal and
tail-selecting books — whose active returns are negatively skewed by construction.

**4. Pitfall specific to the repo.** MinTRL is in **observations**, and `n` for a monthly-rebalance
candidate is not the number of rebalances; it is the number of return observations, which is
daily. Converting a monthly-rebalance strategy's MinTRL into "months of rebalances" inflates the
requirement by about `√21` and is the most likely way to misuse this formula here.

## Related

- `notes/2026-08-23-statistics-of-sharpe-ratios.md` — Lo (2002), the IID case of the same variance
  (`1 + ŜR²/2`) and the autocorrelation correction this paper does not make.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the paired variance that must be
  substituted for MinTRL's constant-`SR*` assumption; it already notes that **power rises with `ρ`**,
  which is the same fact as the table above, read from the other end.
- `notes/2026-11-05-minimum-backtest-length-and-the-expected-maximum-sharpe.md` — the `N > 1`
  complement, by the same authors, which is explicitly the problem MinTRL does not address.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — the same authors' post-hoc correction. DSR deflates
  a number after it exists; MinTRL sizes the sample before it does. The two are the two ends the
  [2026-11-04] open-questions entry asked to bracket.
- `notes/2026-09-23-spanning-test-power-and-step-down.md` — the only prior note in this folder that
  derives a power function, for a spanning `F`-test rather than for a Sharpe difference; its
  conclusion that mean-based detection is very hard at realistic sample sizes is the same message
  arriving through a different statistic.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — `#323`'s separation rate answers
  a *different* question (which of several candidates is best) and says so; this answers whether
  any of them is distinguishable from the pool at all.
- `notes/2026-10-30-cost-aware-alpha-investing-and-the-sample-size-lever.md` — already carries a
  level–power–sample-size link, for a sequential testing budget rather than for the Sharpe
  statistic. The [2026-11-04] claim that this folder had **zero** notes bearing on ex-ante
  detectability was therefore overstated; what was genuinely absent is the MDE of the lab's own
  skill statistic, which is item 2 above.
