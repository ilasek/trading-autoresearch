---
title: "Market Frictions, Price Delay, and the Cross-Section of Expected Returns"
authors: Hou, Moskowitz
year: 2005
venue: Review of Financial Studies 18(3), 981–1020 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1093/rfs/hhi023
citations: 909 (Crossref, checked 2026-09-05); 1091 (OpenAlex, checked 2026-09-05); Semantic Scholar returns "not found" for this DOI (checked 2026-09-05)
sample_period: 1963–2001 (weekly return histories; portfolio returns from 1964)
markets: US equities (CRSP NYSE/AMEX/NASDAQ)
tier: A
validation_overlap: false
published_post_2018: false
---

**Text read**: the authors' September 2003 draft in full from a university mirror
(`ruf.rice.edu/~jgsfss/moskowitz.pdf`) — the delay measures and their variants, the portfolio
construction, the size and value decompositions, the size/idiosyncratic-risk interactions and the
trading-cost discussion. This is the pre-publication manuscript of the RFS article; the measure
definitions below are the ones that appear in the published version and in every subsequent
implementation of `DELAY`.

## Mechanism

`SUMMARY.md` has carried `DELAY` for a week as "the direct measure of speed of adjustment that the
volume sort in Chordia–Swaminathan is a proxy for, needs closes only, and nothing in this lab has
used it". This is the source. It does two things: it defines the measure, and it establishes —
against its own authors' interest — exactly where the measure has no variation.

The economics is Merton (1987) **investor recognition**: investors know about, and hold, only a
subset of securities. A stock that few investors follow has its price updated by fewer people, so
its price incorporates market-wide news with a lag, and it must offer a higher expected return to
compensate the investors who do hold it for bearing idiosyncratic risk they cannot diversify away.
The observable signature of "few investors follow this" is therefore **how slowly the price
responds to news everyone else has already traded on** — which is measurable from prices alone,
with no analyst, ownership or coverage data.

The claims the paper establishes: delay-sorted portfolios spread average returns strongly even
after adjusting for size, book-to-market and past-year return; **delay subsumes the size effect**
(after adjusting size-sorted returns for delay, the size spread collapses to insignificance, and
only the component of size *related to* delay predicts returns at all) and captures part of the
value effect; idiosyncratic risk is priced only among the most severely delayed firms; and
post-earnings-announcement drift increases monotonically in delay. The effect is not explained by
microstructure, price impact, or liquidity-risk and informed-trading factors.

**And the constraint that matters here, stated by the authors as a finding.** The premium is
overwhelmingly a property of the extreme tail: it derives almost entirely from the highest-delay
decile, with the lowest-delay decile showing no significant underperformance — an asymmetry the
authors explain as necessary, since "only the most constrained or inefficient assets carry a
premium" **can only hold if those assets are a small fraction of the market**. Their highest-delay
decile is under 0.02% of total US market capitalisation. Sorted within size, the delay premium is
"prevalent only among the smallest stocks", increases monotonically in idiosyncratic volatility,
and is strongest among past-year losers.

## Construction recipe

**The regression.** Once a year, for each name, on **weekly** returns over the prior year, regress
the name's return on the contemporaneous market return and four weekly lags of it:

```
r_j,t = alpha_j + beta_j * Rm_t + sum_{n=1..4} delta_j^(-n) * Rm_(t-n) + eps_j,t
```

If the name responds immediately, `beta_j` is significant and the `delta`s are not. If it responds
with a lag, some `delta`s are.

**The three measures**, from the same fit:

```
D1 = 1 - R2_restricted / R2_unrestricted        # restricted: all delta^(-n) = 0
D2 = sum_n ( n * delta^(-n) ) / ( beta + sum_n delta^(-n) )
D3 = sum_n ( n * delta^(-n)/se(delta^(-n)) ) / ( beta/se(beta) + sum_n delta^(-n)/se(delta^(-n)) )
```

`D1` is the share of contemporaneous return variation attributable to *lagged* market returns — an
F-test on the joint significance of the lags, scaled by total explained variation. `D2` weights
longer lags more heavily; `D3` additionally weights by estimate precision. The three
rank-correlate around 0.90 with each other and produce similar sorts, so `D1` is the one to build.

**Choices the authors made deliberately, each with a stated reason. All of them transfer.**

- **Weekly, not daily or monthly.** Monthly gives almost no cross-sectional dispersion in delay
  (most stocks respond within a month) and much higher estimation error. Daily would give more
  dispersion but confounds it with bid-ask bounce and nonsynchronous trading. Weekly is the
  compromise, and the delay they are hunting takes several weeks.
- **Wednesday-to-Wednesday weeks.** Explicitly because Friday-to-Friday returns show high
  autocorrelation and Monday-to-Monday low; Wednesday is chosen as the compromise. (This is a
  *point estimate* choice, and the weekday-seasonality result in
  `notes/2026-09-05-cross-serial-correlation-as-restatement.md` says it must be checked across all
  five week-ending days rather than assumed.)
- **Lags of the market only, never the stock's own lags.** Adding own-return lags gives nearly
  identical results but destroys interpretability at the portfolio level, because portfolio
  autocorrelation and individual autocorrelation have opposite signs (Lo–MacKinlay). Using only
  the market response keeps individual and portfolio delay comparable.
- **Four lags.** Coefficients beyond lag 5 are negligible and volatile; most of the significance
  sits at lags 1–2. Robust to seven lags with a triangular weighting scheme (rank correlation ~0.90
  with the simple version).
- **Sign is ignored** — the measures use raw coefficients because most lagged coefficients are zero
  or positive; using absolute values changes nothing.
- **Skip at least a month** between the measurement window and the return window, and rebalance
  annually. Turnover of the resulting book is about 35% per year: delay rankings are persistent,
  and this is a genuinely low-turnover construction.

**The noise correction, which is the most important construction detail for a small universe.**
Individual-name coefficients from 52 weekly observations with five regressors are estimated
imprecisely, and the authors do not use them directly. They sort names into 10 size x 10 delay
portfolios on the *pre-ranking individual* estimate, then **re-estimate the regression on the
portfolio return series using the entire past sample**, and assign the portfolio's delay to each
member. They report that the shorter the pre-ranking window, the weaker the sort — explicitly
attributed to estimation noise. **The individual-level `D1` is a noisy input to a grouping step,
not a signal.**

## Robustness evidence (qualitative only)

Multi-decade US sample; results reported by subperiod, excluding January, for NYSE/AMEX and NASDAQ
separately, and across three alternative delay definitions plus a version adding *leading* market
returns (rank correlation 0.91 with the baseline). Return adjustment is layered — a
125-portfolio characteristic benchmark on size, book-to-market and past-year return, *then*
three-, four-, five- and six-factor time-series regressions adding a traded liquidity-risk factor
and an informed-trading factor — and the delay intercept survives all of them. That is unusually
thorough risk adjustment, and it is what makes the paper's negative results credible too.

The authors model costs qualitatively rather than net them out: they compute the round-trip cost
that would wipe out the premium for the subset of delayed firms that have *some* analyst and
institutional coverage, compare it to published cost estimates for the smallest size quintile, and
then make the more decisive point themselves — that even at full exploitation the **dollar**
capacity of the strategy is trivially small, which is their answer to why the premium is not
arbitraged away. Single market. `DELAY` is widely reused as a measure in subsequent literature; the
folder has not verified an independent replication of the *premium*, and Chordia–Swaminathan is
independent evidence for the underlying speed-of-adjustment mechanism rather than for this
measure's return spread.

## Implementability here

**The measure is fully buildable on closes alone; the premium is not reachable, and the source says
so before this repo has to spend a trial finding out.**

Buildable: weekly returns from the daily USD close panel, an equal-weighted own-universe index in
place of the CRSP market, a 52-week rolling regression per name with four lags, annual (or
month-end, with a skip) refit, `D1` per name. It costs closes only, it has an annual refit, and
its natural turnover is low — which for once is not the objection.

**The pre-registered kill line, and it comes from the source rather than from this folder.** The
paper reports the spread in the average delay characteristic between the top and bottom quintiles
as **0.26 among the smallest stocks and 0.03 among the largest**. This universe is ~145 large,
globally-known instruments — the largest end of every one of that paper's sorts. The precondition
is therefore a single free measurement:

> Compute `D1` for every name at each annual refit and report the cross-sectional dispersion
> (top-quintile mean minus bottom-quintile mean, and the p90/p10 ratio). **If the top-minus-bottom
> spread is near 0.03 rather than near 0.26, the measure has nothing to sort on here and
> `lead-lag-spillover`'s per-name branch closes on its identified cause — the same shape as the
> Corwin–Schultz precondition that closed `range-variance` a twelfth time.** No trial is spent
> either way.

Two further discounts that stack, and neither needs measuring:

- Delay's premium lives in the extreme tail (a decile under 0.02% of market capitalisation, with
  no significant effect at the low-delay end). A long-only book on ~145 names cannot construct that
  tail; it is not that the effect is small here, it is that the population is absent. This is the
  same reading as `SUMMARY.md` #68's big-stock rule and #73's microcap discount, now with a third
  independent source and a *stated* size interaction rather than an inferred one.
- The delay premium rises monotonically in idiosyncratic volatility and is strongest among past
  losers. This repo's universe is survivorship-conditioned current constituents, so its
  high-idiosyncratic-volatility tail is selected on having survived — the exact confound
  `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` describes, and the same
  one the lab measured when it decomposed `ILLIQ` and found the numerator to be survivorship-
  inflated volatility.

**The use that survives the discounts is as a *grouping* variable, not a premium.** The paper's own
construction treats individual `D1` as too noisy to trade and uses it to *sort names into
portfolios*, then measures delay on the portfolios. That is a different object from a `D1` level
sort and it is the object `lead-lag-spillover` actually needs: a leader/laggard partition estimated
from prices rather than assumed from size or region. A candidate would use `D1` to split the
universe into fast- and slow-adjusting halves and ask whether the fast half's lagged return
predicts the slow half's — which is a cross-quantity, and is the screen Chordia–Swaminathan warn is
required because own-autocorrelation is *not* a valid speed-of-adjustment measure (a name reacting
to today's and yesterday's news shows positive own-autocorrelation while being the faster
adjuster). Run it only if the dispersion precondition passes, and run it through the
implied-versus-actual control in
`notes/2026-09-05-cross-serial-correlation-as-restatement.md` — a `D1` partition sorts on precisely
the own-autocorrelation quantity that makes that control bite hardest.

**Pitfalls specific to this repo.**
- The market proxy must be an own-universe equal-weighted index. There is no external market series
  and none may be fetched.
- Non-overlapping regional sessions put a *mechanical* lag-1 market coefficient on every non-US
  name: an Asian close reflects the previous US session. `D1` will then rank names by time zone,
  not by attention. Region-demeaning `D1` is the obvious repair and is the same operator that
  produced the lab's `ILLIQ` result — but note that the venue-unit account behind that result does
  not apply here (`D1` is a unit-free variance ratio, and the lab measured that operator as inert
  on unit-free scores). The correct control is the **weekly** frequency plus a region-demean, and
  a placebo on US-only names.
- Fifty-two weekly observations and five regressors leaves 47 degrees of freedom per name per year.
  This is exactly the "noisily-estimated parameter" that `SUMMARY.md` #1's triage screen exists to
  kill. The paper's own answer — group first, estimate on the group series over a long window — is
  the version that passes that screen, and it is the version to build.

## Related

- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — where `DELAY` first entered
  this folder, second-hand, as the direct measure the volume sort proxies for. This note is the
  primary record.
- `notes/2026-09-05-cross-serial-correlation-as-restatement.md` — the control any `D1`-partitioned
  lead-lag test must pass, and the reason the weekday convention above is not settled.
- `notes/2026-09-05-contrarian-profit-decomposition.md` — the reason this paper deliberately
  excludes own-return lags from the delay regression.
- `notes/2026-09-02-anomalies-by-size-group.md` and
  `notes/2026-09-03-machine-learning-economic-restrictions.md` — the folder's two existing
  size-conditional discounts; this is the third and the most explicit about the delay channel.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the paper uses Amihud's
  measure as one of its liquidity controls and reports delay strongly inversely related to it,
  which is why a `D1` leg and the lab's seated `ILLIQ` leg should not be assumed decorrelated.
