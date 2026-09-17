---
title: "Downside beta — asymmetric comovement from daily returns, why the raw sort inverts at the top, and the replication that reads the wrong sign"
authors: "Ang, Chen, Xing (primary); Hou, Xue, Zhang (the replication)"
year: "2006 (RFS; NBER WP 2005) / 2020 (RFS; advance article 2018)"
venue: "Review of Financial Studies (Tier 1) for both"
url: "https://doi.org/10.1093/rfs/hhj035 (read in full as https://www.nber.org/system/files/working_papers/w11824/w11824.pdf) ; https://doi.org/10.1093/rfs/hhy131 (read in full from the author-hosted copy at theinvestmentcapm.com)"
citations: "Ang–Chen–Xing 1101 (OpenAlex and Crossref by DOI, checked 2026-09-17; Semantic Scholar's DOI endpoint returns 'not found' for this DOI). Hou–Xue–Zhang 1052 (OpenAlex, checked 2026-09-17); 835 (Semantic Scholar by DOI, same date)."
sample_period: "Ang–Chen–Xing: Jul 1962/Jul 1963–Dec 2001 (risk measures from Jul 1962, portfolio formation from Jul 1963). Hou–Xue–Zhang: Jan 1967–Dec 2016."
markets: "US only. Ang–Chen–Xing's main universe is NYSE-listed stocks (deliberately, to suppress illiquidity effects), with NYSE/AMEX/NASDAQ as a robustness check; Hou–Xue–Zhang use NYSE/AMEX/NASDAQ with NYSE breakpoints."
tier: "A on evidence quality for both — but the *net verdict* on the tradeable signal is negative, and that is the finding to carry."
validation_overlap: false
published_post_2018: "true for Hou–Xue–Zhang (RFS 2020, advance article 2018); false for Ang–Chen–Xing. Neither sample touches 2018–2023."
---

Both papers read in full. The Ang–Chen–Xing text used is the December 2005 NBER working paper
(w11824); the 2006 RFS version was not read, though the working paper already thanks the editor
(Harvey), two anonymous referees and incorporates their comments, so it is a post-review draft.
Hou–Xue–Zhang was read from the author-hosted copy of the RFS article on `theinvestmentcapm.com`
(page headers show the Oxford advance-article stamp), so the text is the version of record's typeset
proof rather than the publisher's own file.

## Mechanism

**The object.** Split the market's daily returns at their own mean and measure comovement only on
the down half:

    β⁻ = Cov(r_i, r_m | r_m < μ_m) / Var(r_m | r_m < μ_m)

with `β⁺` the mirror image on the up half. Three derived quantities matter: **relative downside
beta** `β⁻ − β` (asymmetry net of the ordinary market beta), `β⁺ − β`, and the outright asymmetry
`β⁺ − β⁻`.

**Why it should be priced.** An investor who dislikes losses more than the equivalent gain — a
disappointment-averse or loss-averse investor, and the reference is to the Gul / Ang–Bekaert–Liu line
of utility that conditions on a downside event directly rather than approximating it with a moment —
demands compensation for holding an asset that comoves with the market *specifically when the market
falls*. An asset with high `β⁻` fails you when diversification is worth most. So `β⁻` should carry a
positive premium **over and above** ordinary beta, and `β⁺` should not carry the same premium (an
asset that participates in rallies is desirable, not risky). Ang–Chen–Xing find exactly that pattern
contemporaneously: mean excess returns and CAPM alphas both rise in realized `β⁻` and in realized
`β⁻ − β`, and they are explicit that this is **distinct from coskewness** — a `β⁻` sort produces
almost no spread in realized coskewness, so the two are different loadings (see
`notes/2026-09-17-coskewness-and-the-third-moment-estimation-window.md`).

**The gap between "priced" and "tradeable", which is the whole content of this note.** A
contemporaneous relation between *realized* `β⁻` and *realized* returns is not a strategy. To trade
it you must forecast next period's `β⁻` from past data, and Ang–Chen–Xing are unusually honest that
this is where it breaks:

- Past `β⁻` does predict future `β⁻` — the sort stays monotone out of sample — but the **spread it
  delivers in future `β⁻` is less than half the spread available in realized `β⁻`**. The 12-month
  autocorrelation of `β⁻` among NYSE stocks is modest.
- The persistence is **much worse for high-volatility names** (their reported one-year
  autocorrelation of one-year `β⁻` for very volatile stocks is roughly a third of the figure for a
  typical stock), because `β⁻` estimated from one down-half of one year of daily data is a noisy
  statistic and noise scales with the asset's volatility.
- **Returns on past-`β⁻` quintiles rise from Q1 to Q4 and then fall at Q5.** The pattern is not
  monotone; it inverts exactly where the estimate is noisiest.

**The identity that explains the inversion, and it is the transferable part.** Rewrite

    β⁻ = ρ⁻ · σ⁻_i / σ⁻_m,    ρ⁻ = corr(r_i, r_m | r_m < μ_m)

A high `β⁻` can come from high **downside correlation** `ρ⁻` — which is the priced thing, the
"fails you when the market falls" content — or from high **downside volatility of the asset itself**
`σ⁻_i`, which is not. And high own volatility carries the opposite-signed idiosyncratic-volatility
effect (their own companion result: very high total or idiosyncratic volatility goes with low
returns). So `β⁻` is a *sum of a wanted and an unwanted component*, the unwanted one dominates at the
top of the sort, and that is why Q5 breaks. **The correct object to sort on is the correlation, not
the beta.**

Their refinement is the coarse version of that: drop the highest-volatility names and past high `β⁻`
does predict high future returns for the rest, which they note is the large majority of the market by
capitalisation. Note what this is — a **double sort with a volatility exclusion** — and that the lab
has a standing result about exactly that shape (see *Tensions*).

**`β⁺` is a null.** Past `β⁺` has no predictive ability for future returns, with or without the
volatility exclusion. So the asymmetry is genuinely one-sided: only the down half carries anything.

## Construction recipe

1. **Market proxy**: a value-weighted market excess return. Compute `μ_m` as the mean market excess
   return **over the same estimation window** (this is what "downside" is defined relative to — not
   zero, and not a longer-run mean).
2. **Estimation window**: 12 months of **daily** returns, using only the days with `r_m < μ_m`.
   Hou–Xue–Zhang's implementation, which follows the paper, requires a minimum of 50 such daily
   observations. Ang–Chen–Xing report the results survive 24-month windows of weekly data.
3. **Sort** at the beginning of each month `t` into quintiles (or deciles) on `β⁻`, hold one month,
   rebalance. Their portfolios are equal-weighted, with value-weighted robustness checks.
4. **The refinement**: within the sort, exclude or separate the highest-volatility names, using
   trailing daily return volatility over the same window. Ang–Chen–Xing reach this from a
   Fama–MacBeth regression of the determinants of `β⁻`, in which volatility is the confound; they
   also name book-to-market and momentum as interacting, which are out of scope here.
5. The sharper version implied by the identity, which the paper does not itself implement as a
   strategy: **sort on `ρ⁻` directly**, or on `β⁻ − β` (relative downside beta), rather than on `β⁻`.

## Robustness evidence (qualitative only)

- Ang–Chen–Xing's *contemporaneous* result is robust across weighting schemes, exchange universes,
  non-overlapping subsamples and weekly-versus-daily estimation, and survives controls for
  coskewness, size, book-to-market, momentum and liquidity. Their restriction to NYSE names is
  stated to understate the effect.
- **The tradeable version fails the standard replication, with the wrong sign.** Hou–Xue–Zhang
  include `β⁻` in their library exactly as specified above (12 months of daily returns, minimum 50
  down-days, deciles, rebalanced monthly, held 1 / 6 / 12 months). Across all three holding horizons
  and all eight of their specifications — NYSE and all-exchange breakpoints, value- and
  equal-weighted, Fama–MacBeth WLS and OLS, and the small-sample variants — **the high-minus-low
  decile spread is negative in every single cell.** It is statistically indistinguishable from zero
  under value weighting and **significantly negative** under equal weighting and under FM-OLS. So the
  raw sort does not merely fail to pay; in the specifications with power it pays in reverse.
- The two results are reconcilable, and the reconciliation is the mechanism above: Hou–Xue–Zhang
  sort into **deciles without the volatility exclusion**, which loads the extreme decile with exactly
  the high-volatility names whose `β⁻` is noisiest and whose own-volatility effect is negative.
  Ang–Chen–Xing's own Q5 inversion predicts this. **This is not a defence of the raw signal — it is
  the reason not to trade it — but it does mean the replication failure is a failure of `β⁻` as a
  sort, not a refutation of asymmetric comovement as a priced dimension.**
- Hou–Xue–Zhang's broader context matters for how much weight to put on any single row: a large
  majority of the anomalies in their library fail a single-test `|t| > 1.96` hurdle once microcaps
  are handled with NYSE breakpoints and value weighting, and their frictions category fails almost
  completely. Their beta-family rows generally read as nulls.
- Costs: neither paper's headline is net of costs. Both are monthly-rebalanced sorts.

## Implementability here

**Cheap, in scope, and already partly built.** `β⁻` needs only daily closes and a market proxy; both
exist. `strategies/lib/features.py` has cross-sectional normalisation and long-only weighting
helpers. A long-only expression is the top-`k` names by the chosen statistic, capped at 25%, monthly
rebalance — the repo's standard shape. History requirement is one year plus the rebalance grid, which
is nothing.

**But do not implement the headline sort.** The literature's net verdict on `β⁻` deciles is a
significant *negative* spread. Proposing a long-high-`β⁻` book here would be re-testing a refuted
construction, which `CLAUDE.md` forbids absent a stated reason. The two things that are *not*
refuted and have never been measured on this universe:

1. **Sort on downside correlation `ρ⁻` rather than downside beta.** This is the identity's wanted
   component with the volatility term divided out, it is one line of code past `β⁻`, and no paper in
   this folder has tested it as a standalone signal. It is also the cleanest possible test of whether
   Hou–Xue–Zhang's negative sign is the volatility confound or the mechanism: if `ρ⁻` sorts flat and
   `β⁻` sorts negative, the confound explanation holds and the family closes honestly.
2. **The asymmetry `β⁺ − β⁻`, or `β⁻ − β`, as a *screen* rather than a book.** The lab's momentum
   champion holds whatever the trend sort selects; nobody has measured whether that basket is loaded
   on downside comovement. That is a holdings-only diagnostic of the kind `learnings.md` says keeps
   killing ideas for free, and it costs no trial.

**Universe mismatches to state before trusting anything:**

- **A market proxy must be chosen, and the choice is not innocent.** The universe is global (about
  145 instruments across 15 regions, 42 of them ETFs), so "the market" could be the equal-weighted
  universe, a cap-weighted proxy, or a US index inside the universe. Because `β⁻` is defined relative
  to `μ_m` *of that proxy*, a US proxy makes "downside days" US downside days, and non-US instruments
  then inherit a time-zone artifact — the lab closed `lead-lag-spillover` on precisely that
  mechanism (2026-09-16). Prefer the equal-weighted universe return, and say which was used.
- **ETFs and single stocks are not comparable on this statistic.** A regional equity ETF has `ρ⁻`
  near one almost mechanically; 42 of the instruments are ETFs. Either run it within-type or
  demean by type. This is the same grouping-axis question as
  `notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md`.
- **Survivorship.** The universe is today's constituents, so the down-half comovement of names that
  did not survive is missing, and downside comovement is exactly the property a delisted name would
  have had. This biases against finding a premium, which makes a null here weakly informative and a
  positive result suspect.
- **Estimation noise is the mechanism's known failure mode, and this universe has few names.** With
  ~145 instruments, a quintile is ~29 names and a decile ~15; the top bucket is where the noise
  inverts the sign. Prefer coarse buckets, and read
  `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md` first.

## Tensions with this lab's own results — stated, not smoothed over

1. **`learnings.md`: "Low-vol stock tilt is refuted, standalone and as a within-momentum filter,"**
   with the stated failure mode that filtering a high-momentum pool by low volatility discards the
   pool's strongest compounders. Ang–Chen–Xing's refinement is a volatility **exclusion** applied to
   a different primary sort. The shapes rhyme, and the lab's measured result is that this shape
   destroys value here. So the volatility-excluded `β⁻` sort — the only version the source itself
   endorses as tradeable — is the version this lab has the most specific reason to doubt. That is an
   argument for testing `ρ⁻` (which needs no exclusion) instead.
2. **`CLAUDE.md`: do not carry `learnings.md`'s constants into a new family by analogy.** The
   de-concentration price and the required-gain table were measured on `price-trend`. Nothing here
   licenses assuming a 15-name bucket behaves the same way on a comovement sort. Re-measure or say
   you have not.
3. **`range-variance` is a family the lab closed on evidence (2026-09-14), and vol-of-vol in any
   form is on the do-not-extend list.** Downside *correlation* is not a volatility estimator — it is
   a comovement statistic, and the identity above is precisely the argument for why the volatility
   part must be divided out. But a session proposing it should say explicitly that it is not a fourth
   vol-of-vol variant, and should expect to be asked.

## Related

- `notes/2026-09-17-coskewness-and-the-third-moment-estimation-window.md` — the other asymmetry
  measure; Ang–Chen–Xing show the two are empirically distinct loadings, and the two notes reach
  opposite verdicts on which one survives replication.
- `notes/2026-09-01-max-lottery-extreme-positive-returns.md` — the upside-tail counterpart, and the
  reason `β⁺` being a null is not surprising.
- `notes/2026-08-18-low-risk-investing-industry-neutral.md`,
  `notes/2026-08-18-defensive-equity-replication-and-construction.md` — the beta-family material,
  including betting-against-beta, whose Hou–Xue–Zhang rows are also nulls.
- `notes/2026-08-29-range-based-volatility-estimators.md` — the family the lab has since closed.
- `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md`,
  `notes/2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — a sort that rises then inverts at
  the top is the textbook case those two notes exist to handle.
- `experiments/learnings.md` — "Low-vol stock tilt is refuted"; the holdings-only-diagnostic rule.
