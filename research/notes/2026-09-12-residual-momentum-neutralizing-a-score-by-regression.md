---
title: "Residual Momentum" (with "The Idiosyncratic Momentum Anomaly" as the independent multi-market companion) — read for what the `neutralize`-by-regression operator does to a score and to the book built from it
authors: Blitz, Huij, Martens (2011); Blitz, Hanauer, Vidojevic (2020)
year: 2011
venue: Journal of Empirical Finance (Tier 1); International Review of Economics & Finance (Tier 2)
url: https://doi.org/10.1016/j.jempfin.2011.01.003 · https://doi.org/10.1016/j.iref.2020.05.008
citations: 145 (Semantic Scholar via the SSRN registration 10.2139/ssrn.2319861, checked 2026-09-12 — the Elsevier journal DOI is NOT found in Semantic Scholar); 190 (Crossref on the journal DOI, checked 2026-09-12). Companion: 72 (Semantic Scholar via 10.2139/ssrn.2947044, checked 2026-09-12 — the IREF journal DOI is likewise not found there); 45 (Crossref on the journal DOI, checked 2026-09-12). OpenAlex not consulted: its daily budget was exhausted (`Insufficient budget`, checked 2026-09-12)
sample_period: 1926–2009 (primary, post-formation returns from 1930)
markets: US (CRSP: NYSE/AMEX/Nasdaq domestic primary common stock; closed-end funds, REITs, unit trusts, ADRs and foreign stocks excluded; sub-$1 prices excluded). Companion: developed and emerging markets, sample not read
tier: A for the primary (peer-reviewed, eight decades, construction robustness reported, independently followed up); B for the companion, which is recorded abstract-only
validation_overlap: false for the primary (sample ends 2009). Unverified for the companion — its sample was not read; treat any claim attributed to it as untimed and qualitative
published_post_2018: false for the primary; true for the companion
read_status: primary read in full (accepted manuscript, Erasmus institutional repository). Companion recorded from its published abstract only — no open copy resolved
---

## Mechanism

This is the `neutralize`-by-regression operator in its cleanest published form, and the reason to
read it is not the anomaly but the *why*.

**The problem it solves.** A score built from realized returns inherits whatever the common
factors did during its own formation window. A stock that rose over the last year rose partly
because it loads on factors that rose; ranking on total return therefore ranks partly on
*factor exposure realized in the formation window*. The resulting book is long the factors that
went up and short the factors that went down — a bet nobody chose, which reverses whenever the
sign of a factor's return flips between formation and holding. The exposures are not constant, so
they cannot be netted out by a constant hedge: they are a function of what the factors just did.

**The operator.** Replace the raw return series with the residual from a rolling factor
regression, and rank on the residual. By construction the score no longer contains the part of
the return that the factors explain, so the book inherits much smaller and much less
time-varying factor exposure. The paper's own summary of where the improvement comes from is
unambiguous and is the part worth carrying: **the gain is a variance reduction, not a bigger
spread.** Ranking on residuals does not find better names; it stops the book from making an
unintended factor bet. Within their sample the volatility roughly halves while the raw spread
does not grow, and the risk-adjusted number roughly doubles as a consequence — recorded here as
a *ratio between two constructions on one sample*, with the standing rider that this folder does
not export performance expectations and neither should any hypothesis built on it.

**The second-order consequences, which are the interesting ones for this lab.** Because the
score no longer ranks on factor exposure, the resulting book is also much less tilted toward the
segments that carry those exposures — in their setting, small caps — and therefore much less
exposed to the trading costs and the calendar effects concentrated there. And the payoff is
**less concentrated in the extremes of the cross-section**: the residual score's return-versus-rank
profile is flatter and longer than the raw score's. That is a depth-profile claim, arrived at
from the neutralization side, and it is the mechanism by which this operator could justify a
wider band.

## Construction recipe

Enough to implement without re-reading:

1. **Estimate, per name, a rolling factor regression on monthly excess returns** over a 36-month
   window ending at `t−1`: `r_i,t = α_i + β_1·MKT_t + β_2·SMB_t + β_3·HML_t + ε_i,t`. Only names
   with a complete return history over the window enter.
2. **Build the score from the residuals over the formation window only** — the sum of `ε_i,t`
   over `t−12 … t−2`, i.e. eleven months with the most recent month skipped, exactly as a
   conventional 12-1 momentum signal skips it to avoid short-term reversal.
3. **Standardize the residual sum by the standard deviation of the same name's residuals over the
   same window.** This is not cosmetic: the raw residual sum is a noisy estimate, and dividing by
   its own scale is what turns it into a measure of *how much of a firm-specific shock is news
   rather than noise*. The paper reports that the unstandardized version works but is riskier —
   standardizing is where the variance reduction is bought.
4. **Deliberately exclude the estimated `α` from the score.** The reason is a genuine construction
   trap and generalizes: over two-thirds of the observations behind `α̂` lie *outside* the
   formation window, so folding `α̂` into the score smuggles in returns from `t−36 … t−13` and
   turns the signal into a partial long-term-reversal bet. **Any residual-based score must be
   built only from residuals dated inside the window the signal is supposed to measure.**
5. **Rank into deciles, equal weight inside the band**, overlapping K-month holding periods.
6. **If group effects are the worry, add group factors rather than group dummies.** Their industry
   extension regresses each of 30 industry portfolios on the same three factors, runs a PCA on
   those residuals, and adds the **first five principal components** to the per-name regression.
   The stated reason is a parameter-count argument this lab will recognize: adding 30 industry
   returns directly would mean estimating 34 parameters from 36 observations.

## Robustness evidence (qualitative only)

- **Construction robustness is reported and is broad**: window length varied (24, 36 and 60
  months) with results described as very similar; the (J,K) formation/holding grid; a post-1960
  subsample; and the industry-augmented eight-factor version, which reduces the dynamic exposures
  further still.
- **The complete-history filter is controlled for, and this matters more than it looks.** The
  authors anticipate the objection that requiring 36 months of history selects a different
  universe, and re-run *total*-return momentum under the same filter. The comparison is then
  like-for-like and the difference survives. This is the right control and it is the exact
  control this lab's pool rule needs; see
  `2026-09-12-missing-data-and-complete-case-pools.md` for why it is not a formality.
- **Large caps only**: repeating the analysis on the largest decile leaves the main conclusion
  unchanged. What does shrink is the *share of variance the factors explain* and the size-factor
  side of the dynamic exposure — unsurprising in a more homogeneous universe. This is the single
  most relevant robustness check for this repo, whose universe is ~140 large instruments, and it
  cuts both ways: the operator still helps there, but the thing it removes is smaller there.
- **Calendar stability**, recorded as a proportion with no dates attached, in the manner this
  folder records period counts: the residual construction's monthly returns clear a `t > +2` bar
  in **8 of 12 calendar months** against **3 of 12** for the raw construction. Read it as a
  dispersion statistic about the two constructions, never as a threshold.
- **Independent multi-market follow-up exists.** The 2020 companion, recorded from its abstract
  only, reports that idiosyncratic momentum is a distinct phenomenon existing alongside
  conventional momentum, is priced in the cross-section, and is present across developed and
  emerging markets. That is a qualitative cross-market robustness statement and is all this note
  takes from it; its sample was not read and nothing timed is imported from it.
- The primary predates this lab's validation window entirely, so there is no soft-lookahead
  discount on the mechanism.

## Implementability here

**Reachable.** This repo has daily USD closes for ~140 instruments and a month-end rebalance grid,
so the operator is buildable with no new data: form monthly returns, build the factors *from the
universe itself* (an equal-weighted universe return as the market leg, and region portfolios as
the group legs — there is no fundamentals-based SMB or HML available and none should be faked),
run the rolling per-name regression inside `walkforward` bookkeeping, and rank the standardized
residual sum. Thirty-six monthly observations per name is comfortably inside the history this
store carries for most instruments.

**But the lab has already measured one version of this operator, and it lost. The tension is
real and must be stated rather than smoothed over.** On 2026-09-10 the free-beta regional
residual was screened against the plain region demean and lost decisively — the demean's score
carried a strongly positive IC while the residual's was indistinguishable from zero, and the rank
of *what the residual adds over the demean* had a significantly **negative** IC. Two reasons were
recorded: the region factor is priced here with the **wrong sign**, so removing 100% of it (unit
loading) beats removing `β_i` times it; and a free beta estimates one parameter per name per date,
whose measured IQR of 0.944 around a true value near 1 is that estimation error made visible.

Three things separate that screen from this paper, and they are what a future session would have
to change before claiming the question is open:

1. **What was measured.** The lab screened the operator on **IC and top-band excess** — return
   statistics of the *score*. This paper's mechanism is a **variance** claim about the *book*:
   smaller and less time-varying factor exposure, hence lower volatility, hence a better ratio at
   an unchanged spread. An IC screen cannot see that. If the operator is ever revisited, the
   pre-committed statistic must be the book's realized volatility and its formation-window-conditional
   factor exposure, not the score's IC. That said — the lab's screen found the residual's IC
   *negative* where it added to the demean, which is evidence against the score even on this
   paper's own terms, because a variance reduction that also deletes the signal is not a trade.
2. **Whether the factor being removed is priced with the right sign.** This paper's premise is
   that the removed exposures are unwanted *risk*. The lab measured its region factor as carrying
   a component priced with the wrong sign, which inverts the premise. **Do not re-run this against
   the region factor.** The untested version is the *market* leg — removing exposure to the
   universe-wide return, where the sign question does not arise the same way.
3. **The standardization step, which the lab's version did not have.** Dividing the residual sum
   by its own residual volatility is where this paper says the risk reduction is actually bought.
   A residual score without it is not this construction.

**Costs and pitfalls.** (a) Per-name rolling regressions at every month-end are the expensive shape
this repo's own triage rule (`SUMMARY.md` #1) penalizes — count the parameters before writing the
candidate, and prefer the industry-PCA trick (a handful of factors standing in for many groups)
over adding group returns directly. (b) The walk-forward discipline is non-negotiable: the
regression window must end at `t−1` and the causality check will catch a full-sample fit. (c) The
`α̂`-exclusion rule in step 4 is easy to get wrong and silently turns the score into a
reversal signal. (d) ETFs sit awkwardly in a per-name factor regression whose factors are built
from the same universe — the 2026-09-10 ETF finding applies here too, and the instrument-class
node should be stated in the hypothesis rather than inherited.

**Honest priority.** Given (1)–(3), this is not a candidate ready to spend a trial on. What it is:
a specification of what the operator was *supposed* to do, which the lab's one measurement of it
did not test, plus two free preconditions (the market-leg version, the standardization step) that
would have to pass a free screen before any trial. If either fails, the neutralize operator is
closed here on evidence rather than by omission, and that is a finding worth having.

## Related

- `2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md` — "align, then rank" is the
  same instruction as "residualize, then rank", reached from the statistics side.
- `2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — the unit-loading
  alternative that beat the free-beta residual here, and why.
- `2026-08-17-momentum-crash-risk-management.md` — the dynamic-factor-exposure story is the same
  one behind momentum crashes; residualization and volatility scaling are two answers to one
  problem.
- `2026-08-17-momentum-horizon-echo.md` — the 12-1 formation window and the skipped month.
- `2026-09-12-missing-data-and-complete-case-pools.md` — the 36-month complete-history filter, and
  why this paper was right to control for it.
- `2026-08-22-long-only-as-l1-regularization.md`, `2026-09-06-long-side-share-of-anomaly-profits.md`
  — everything above is measured on a long–short decile spread; only the long half is reachable
  here, and the variance-reduction claim is about the spread portfolio, not about the top band
  alone.
