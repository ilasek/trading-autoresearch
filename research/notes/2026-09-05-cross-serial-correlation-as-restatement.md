---
title: "A Tale of Three Schools: Insights on Autocorrelations of Short-Horizon Stock Returns"
authors: Boudoukh, Richardson, Whitelaw
year: 1994
venue: Review of Financial Studies 7(3), 539–573 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1093/rfs/7.3.539
citations: 292 (Crossref, checked 2026-09-05); 398 (Semantic Scholar, checked 2026-09-05)
sample_period: 1962–1990 (weekly size portfolios); 1982–1991 (index futures versus spot)
markets: US equities (CRSP NYSE/AMEX size portfolios) and US index futures
tier: A
validation_overlap: false
published_post_2018: false
---

**Text read**: the published article in full, from the third author's NYU Stern page
(`pages.stern.nyu.edu/~rwhitela/papers/3schools%20rfs94.pdf`). The PDF is a **scanned image with
no text layer**; it was rendered page-by-page to PNG and read visually (recipe in the access note
below). Equation (3), Table 2 and the concluding section were read directly; the numerical
nontrading calibrations in Section 3 were read from the authors' own summary of them in the
introduction and conclusion rather than from the tables.

## Mechanism

This is the **null hypothesis for the entire `lead-lag-spillover` family**, and it is not a
hand-wave: it is a two-line algebraic result plus a measurement showing the algebra fits.

The paper sorts the interpretations of short-horizon return autocorrelation into three camps.
*Loyalists* hold that markets process information rationally and that the correlations come from
frictions and measurement error — nonsynchronous trading, price discreteness, bid-ask spreads,
different trading/nontrading periods. *Revisionists* hold that markets are efficient but that
time-varying risk premia can autocorrelate returns. *Heretics* hold that prices underreact and
that lead-lag relations reflect slow diffusion of news from big names to small ones. The paper
argues for the loyalists and supplies two distinct arguments.

**First argument — the cross-serial correlation is a restatement, not new information.** Model each
group's return as an AR(1) with contemporaneously correlated shocks:
`R_i,t = a_i + rho_i * R_i,t-1 + e_i,t`. Then the cross-serial correlation between group `i` today
and group `j` yesterday satisfies

```
corr( R_i,t , R_j,t-1 )  =  corr( R_i,t , R_j,t )  *  corr( R_i,t , R_i,t-1 )
```

— **contemporaneous correlation times own first-order autocorrelation, and nothing else.** No
diffusion, no delayed reaction, no information flowing from `j` to `i`. In their data the implied
values and the estimated cross-serials match closely in *both* magnitude and cross-portfolio
ordering. The asymmetry that looks like a lead-lag arises automatically whenever the groups have
unequal own-autocorrelations, because the identity is asymmetric in `i` and `j` through the second
factor. The authors' phrase is that the lead-lag relation is a **"red herring"** — a less efficient
way of describing individual portfolios' own autocorrelation patterns.

This does not contradict Lo–MacKinlay's arithmetic; it reinterprets what fills the `C_k` term.
Cross-autocovariances can be large and asymmetric with no cross-*predictability* whatever, because
`corr(R_i,t, R_j,t)` is large. They cite the further result that in multiple regressions of
small-firm returns on lagged returns of both groups, **lagged large-firm returns add nothing beyond
the small-firm portfolio's own lag** — which is the regression form of the same statement, and the
form a candidate here can run.

**Second argument — nonsynchronous trading has been understated, not overstated.** The standard
model of nontrading assumes a constant per-interval nontrading probability, time-independent, and
homogeneous stocks within a portfolio. Relax those two assumptions — allow time dependence in
nontrading (information, and therefore trading, clusters within and across days) and heterogeneity
in both nontrading probability and market beta across the members of a portfolio — and induced
autocorrelations that the homogeneous model puts near 7% rise to as much as 20%. The conclusion
states it as an economic magnitude: the nontrading effect, in a world where true returns are not
autocorrelated at all, "can conceivably be 18 percent or higher" for the portfolios at issue.
**Researchers should be especially cautious about ruling nonsynchronous trading out.**

**The ex ante test.** The two arguments above are about interpretation; the paper's discriminating
experiment is not. Take a small-firm-weighted index and the *futures contract written on it*. Both
are claims on the same fundamentals, but only the index is computed from a basket of infrequently
trading component prices; the futures contract trades continuously in one venue. The spot index's
autocorrelation is significantly higher than the futures', and the futures' own autocorrelation is
**indistinguishable from zero**. The paper checks and rejects the two obvious alternative
explanations for the gap — bid-ask bias in the futures price (moving its autocorrelation by a
negligible amount even under an implausibly wide spread) and stochastic interest rates in the
cost-of-carry relation (which would require negatively autocorrelated rate changes that are large
relative to equity returns). What is left is that the autocorrelation lives in the *measurement of
the basket*, not in the asset.

## Construction recipe

Everything here is a control, not a signal. Three of them, in increasing cost.

**1. The implied-versus-actual screen (two numbers per ordered pair).** For every ordered pair of
series `(i, j)` in whatever partition a lead-lag candidate uses — sector groups, regions, size
groups, ETF versus basket — compute on weekly returns:

```
implied_ij = corr(R_i,t, R_j,t) * corr(R_i,t, R_i,t-1)
actual_ij  = corr(R_i,t, R_j,t-1)
```

and compare the two matrices. If `actual ≈ implied` pairwise, and the *ordering* across pairs is
reproduced, there is no lead-lag content to build on. Only the residual `actual - implied` is
candidate material, and only where it is stable across pairs rather than a scatter of pair-level
noise.

**2. The regression form of the same test.** Regress `R_i,t` on `R_i,t-1` *and* `R_j,t-1` jointly.
The heretic claim is that the coefficient on the leader's lag is non-zero **given the follower's
own lag**. Any lead-lag construction that does not include the follower's own lagged return as a
regressor, or its equivalent as a control leg, has not tested the mechanism it claims.

**3. Weekday robustness — mandatory, cheap, and it changes answers.** Weekly returns must be formed
by choosing a week-ending weekday, and that choice is not innocuous. Estimating the same weekly
autocorrelation for the same portfolio over the same sample, once per week-ending day, produced
estimates that varied by roughly half of their own magnitude between the Monday-ending and
Friday-ending versions, with a Wald test rejecting equality across the five days at high
confidence. The authors' own procedure is therefore to estimate **day by day using overlapping
observations** and to lean on the Hansen–Hodrick / Richardson–Smith result that the overlapping
estimator is more efficient than the single-day one — with the caveat that overlapping estimates
must carry autocorrelation-and-heteroskedasticity-consistent standard errors. **Rule to carry: any
weekly lead-lag statistic reported here must be reported for all five week-ending days, and the
conclusion must survive all five.**

**4. The traded-versus-computed control (the futures test's analogue).** The paper's cleanest
evidence comes from comparing a *computed basket* against a *continuously traded claim on the same
thing*. Where such a pair exists, the difference in their autocorrelations bounds how much of the
basket's autocorrelation is measurement.

## Robustness evidence (qualitative only)

Multi-decade weekly sample, with the autocorrelation estimates reported by subperiod as well as
overall; the seasonality-across-weekdays result is reported for the full sample and for four equal
subperiods. The implied-versus-actual comparison is run across all five size portfolios and the
market, not on a favourable pair, and the authors note the small systematic direction of the
residual (their model's implied values run slightly *below* the estimates) and call it consistent
with sampling error rather than suppressing it. The nontrading calibrations are numerical exercises
built on stylised facts from the independent nontrading literature rather than free parameters. The
futures test is a genuine out-of-sample design: it predicts the sign of a difference in a second
market before measuring it.

The honest limits: single market; the nontrading argument is a calibration, so it establishes that
frictions *can* produce the observed magnitudes, not that they do; and the authors say explicitly
that it remains an open question whether the residual autocorrelation after nontrading is
time-varying risk premia or some other microstructure effect. This is a paper that narrows the
space of explanations rather than closing it.

## Implementability here

**This universe is the worst case for every mechanism in the paper, and that is the point.**

- **Nonsynchronous trading is not a subtlety here, it is the design.** 15 regions with
  non-overlapping trading sessions, USD conversion of foreign closes, and closes forward-filled
  across foreign holidays while volume is not. The paper's finding is that nontrading effects are
  *understated* even in a single-venue US sample when heterogeneity in nontrading probability and
  beta is allowed for. A global daily panel is that heterogeneity taken to its limit. `SUMMARY.md`
  already carried the instruction to assume a daily region-level lead-lag result is a time-zone
  artifact until a weekly version reproduces it; this note is the source for it, and it upgrades
  the instruction: the weekly version is necessary but **not sufficient**, because screen 1 above
  can still explain the weekly result away.
- **The lab's own family lead is exactly the object the null predicts.** #58
  (`ll_group_lastmonth_lead`) buys the members of the top sector groups by median trailing 21-day
  return; #62 held the laggard half of the *same* groups and came back a null, closing the
  diffusion reading. Under this paper, that pair of results is the expected outcome and needs no
  new mechanism: a group-trend book is a bet on the group series' **own** autocorrelation, and
  within-group ordering has nothing to say because there was never a diffusion channel. Screen 1
  run on the lab's own 12 group series decides between "the family lead is an own-autocorrelation
  object" and "there is residual cross-predictability" for the cost of two correlation matrices.
- **The traded-versus-computed control is buildable here, and it is the one good use left for an
  object the lab has already screened dead.** The universe holds 42 ETFs alongside single names.
  `SUMMARY.md` records that the ETF-versus-constituent *signal* was screened dead by the lab. As a
  **diagnostic** it is a different object: a region ETF is a claim that trades in one venue with
  one closing time, while the equal-weighted basket of that region's constituents is computed from
  prices set in a foreign session. If the basket series is autocorrelated and the ETF series is
  not, the autocorrelation is measurement, exactly as spot-versus-futures showed. This does not
  require a trial or a candidate file. Known limit before it is run: the lab has already recorded
  that only 5 of 42 ETFs reach a 20-year lookback, so this is a *recent-window* diagnostic and
  should be reported as one.
- **Costs are not the binding objection for once, which makes the identification objection the
  whole story.** The lab's two lead-lag trials ran 13.8x and 18.3x annual turnover and spent their
  entire margin over the equal-weight floor on execution. If screen 1 says the residual is empty,
  the family closes on an identified cause and the turnover problem never needs solving.

**What would count as evidence *for* the family after this note.** A stable, signed residual
`actual - implied` over ordered pairs, surviving all five week-ending weekdays, with the leader's
lagged return significant in the joint regression that already contains the follower's own lag. The
paper does not say that is impossible — it says nobody had shown it, and that the two cheap
alternatives had not been ruled out first.

## Related

- `notes/2026-09-05-contrarian-profit-decomposition.md` — Lo–MacKinlay, the source of the asymmetry
  evidence this paper reinterprets. **Read as a pair.** The identity there is not disputed; what is
  disputed is what fills its `C_k` term.
- `notes/2026-09-05-price-delay-market-frictions.md` — takes the loyalist/friction reading
  seriously enough to *measure* per-name adjustment speed, and finds it concentrated where this
  universe has no members.
- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` — Hong–Torous–Valkanov, whose count
  discipline is the multiple-testing complement to this note's identification discipline: 15
  regions give 210 ordered pairs.
- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — Chordia–Swaminathan report
  their asymmetry surviving a control for the follower's own autocorrelation, which is screen 2
  above; that is the strongest existing counter-evidence in this folder.
- `notes/2026-08-31-intra-industry-lead-lag-grouping.md` — the grouping-choice question, which
  screen 1 should be run separately for.
