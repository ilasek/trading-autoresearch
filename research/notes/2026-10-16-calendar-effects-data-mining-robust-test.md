---
title: "Testing the significance of calendar effects (a data-mining-robust joint test over the full universe of calendar rules)"
authors: Hansen, Lunde, Nason
year: 2003 (Brown University Department of Economics WP 2003-03); circulated 2005 as Federal Reserve Bank of Atlanta WP 2005-02 with Nason added
venue: working paper (Brown Economics; FRB Atlanta) — venue tier 2. Never published in a journal as far as the indexes show; the authors' methodological lineage (Hansen's SPA test, Hansen–Lunde–Nason's model confidence set) is in tier-1 venues
url: https://economics.brown.edu/sites/default/files/papers/2003-3_paper.pdf · https://doi.org/10.2139/ssrn.388601 · https://ideas.repec.org/p/fip/fedawp/2005-02.html
citations: 32 (Crossref `is-referenced-by-count` on the SSRN record 10.2139/ssrn.388601, checked 2026-10-16). Semantic Scholar's title endpoint returned HTTP 429 and was not retried; OpenAlex was not spent on a working paper. A count this low for a 20-year-old methods paper is real rather than an indexing artifact — this is a working paper that the calendar literature mostly cites through Sullivan–Timmermann–White instead.
sample_period: daily index closes from each index's base date (earliest series reach back decades) to 2002-05-06
markets: 27 stock indices from 10 countries — Denmark, France, Germany, Hong Kong, Italy, Japan, Norway, Sweden, UK, USA; large-cap, mid-cap and small-cap indices per country where available
tier: B
validation_overlap: false
published_post_2018: false
read: full text of the Brown WP (886 KB PDF, `pdftotext -layout` → 170 KB of text, 502 instances of `" the "`, `( )`-dropout check zero). Tables are referenced as "TABLE n ABOUT HERE" and are **not** in the extracted text, so every claim below comes from the prose, which states the directions and the conclusions explicitly. No table number is quoted here.
---

## Mechanism

There is no economic mechanism in this source, and that is the point of it. The paper's subject is
the **inferential** mechanism by which a calendar effect comes to look real: the universe of
possible calendar rules is not given by theory, it is enumerated after the fact, and "even if there
are no calendar specific anomalies, an extensive search (mining) over a large number of possible
calendar effects is likely to yield something that appears to be an 'anomaly' by pure chance." The
authors add a second, sharper observation about the literature's epistemics — in this family
"theoretical explanations have only been suggested after the empirical 'discovery' of the
anomalies", so the usual defence that a mechanism was predicted in advance is unavailable here.

The paper's contribution is a test of the joint hypothesis that **no** calendar subset has a mean
different from the whole-sample mean, with two forms:

- `H₀ : ξ₍₀₎ = ξ₍₁₎ = … = ξ₍ₘ₎` on **mean returns**, and
- `H₀′ : ρ₍₀₎ = ρ₍₁₎ = … = ρ₍ₘ₎` on **standardized returns**, `ρ₍ₖ₎ = ξ₍ₖ₎ / ω̄₍ₖ₎`, where `ω̄₍ₖ₎`
  is the average return standard deviation over the days in calendar set `k`.

The second form is the one that matters for a Sharpe-graded lab, and separating the two is the
source's most transferable idea: a calendar window can have an elevated **mean** purely because it
has elevated **variance**, and then it is not an anomaly in risk-adjusted terms at all.

The reason the test is more powerful than a Bonferroni bound is a structural fact about this family
of hypotheses, and it generalises well beyond calendars. Each candidate rule is an **average of the
same return series over a different subset of days**, so the covariance between two rules' sample
means is determined entirely by the **overlap of their day sets**:

    cov(r̄₍ₖ₎, r̄₍ₗ₎) = (1 / (n₍ₖ₎ n₍ₗ₎)) · Σ_{t ∈ S₍ₖ₎ ∩ S₍ₗ₎} σ²ₜ

Overlaps are known a priori from the calendar. The dependence among the tests is therefore
**computable in closed form rather than estimated or bootstrapped**, which is what buys the power
that Bonferroni throws away by ignoring dependence altogether.

## Construction recipe

**The universe (181 calendar effects).** The enumeration is the reusable artifact; it is "almost
identical to that [Sullivan–Timmermann–White] used to construct 9,452 trading rules from":

| Group | Count | Definition |
|---|---|---|
| Day-of-the-week | 5 | Monday … Friday, each measured close-to-close from the previous trading day |
| Month-of-the-year | 12 | January … December |
| Weekday-of-the-month | 60 | the 5 × 12 interaction (Mondays in December, …) |
| Week-of-the-month | 65 | 5 + 5 × 12; weeks counted from the month's first trading day, so the first and last week may be short |
| Semi-month | 26 | 2 + 2 × 12; split at date ≤ 15 versus ≥ 16 |
| Turn-of-the-month | 8 | each of the last four and first four trading days of the month, separately |
| End-of-year | 3 | pre-Christmas from mid-December; between Christmas and New Year; the pair {last trading day before Christmas, last trading day before New Year} |
| Holiday | 2 | pre-holiday (a trading day directly preceding a market closure that would normally be a trading day) and post-holiday (the day after a pre-holiday) |

They also run two **nested sub-universes** deliberately: a 17-effect universe (the 12 months plus
the 5 weekdays), which they call "the smallest universe that one is required to control for" when
evaluating a Monday or January effect, and a 5-effect universe (the 2 holiday plus the 3 end-of-year
effects).

**The statistic.** Let `S₍ₖ₎` be the set of days in effect `k`, `S₍₀₎` the whole sample, and build
the `n × (m+1)` averaging matrix `A` with `A_{t,(k)} = 1/n₍ₖ₎` if `t ∈ S₍ₖ₎` and 0 otherwise (each
column sums to 1, and `A'r = r̄`). Then

- `Σ̂ = A' diag(σ̂²₁, …, σ̂²ₙ) A` — under constant variance this collapses to `σ̂² A'A`;
- for day-varying variance, partition the sample into `q` groups within which `µₜ` and `σ²ₜ` are
  taken as constant (weekday, month, …), estimate each group's variance, and map group variances
  back onto days;
- the hypothesis is `ξ = ι·θ`, i.e. `B = ι` (a vector of ones), and the statistic is
  `T = X' B⊥ (B⊥' Σ B⊥)⁺ B⊥' X` with the Moore–Penrose inverse handling the singularity that
  overlapping calendar sets necessarily create. `T` is `χ²` with `f = rank(B⊥' Σ B⊥)` degrees of
  freedom;
- for the standardized form, replace `Σ` by `Λ⁻¹ Σ Λ⁻¹` with `Λ = diag(ω̄₍₀₎, …, ω̄₍ₘ₎)`.

Returns are log closes, dividends assumed accumulated in the index, and serial correlation is
assumed away (`cov(rₛ, rₜ) = 0`), which is the test's main maintained assumption.

**The subsample diagnostic.** They plot *dynamic p-values* — the test re-run on rolling windows of
1000 observations (~4 years) — for each of the three universes, against the index level. This is
the diagnostic that distinguishes an effect present throughout from one carried by a handful of
windows, and it is cheap to copy.

## Robustness evidence (qualitative only)

- **Multi-market and multi-cap**: 27 indices, 10 countries, including Hong Kong and Japan. The one
  series whose failure to reject they attribute to the test rather than the data is the Hong Kong
  composite, on a short sample (n = 571) and hence low power — they say so rather than reporting it
  as a null.
- **The verdict depends on the universe you control for, in the direction that matters.** Over the
  full 181-effect universe the joint null is rejected for almost all indices. Over the 17-effect
  universe of weekdays and months — the *minimum* control they consider defensible for a claim
  about Monday or January — **the majority of series show no significant calendar effects**, so
  "there is not much evidence in favor of Monday and January effects". The exceptions are small-
  and mid-cap indices and two large-cap indices. In other words the famous named effects are the
  ones that do not survive, while the joint rejection over the wide universe is carried by the
  other groups (end-of-year, holiday, semi-month, turn-of-month, week-of-month).
- **The largest raw anomalies are the end-of-year windows, across almost all countries — and their
  significance does not survive standardization.** The authors' own reading: "the larger returns
  that these effects have produced historically are associated with a higher variance in returns, so
  there is little evidence that standardized returns are significantly different around holidays
  than the rest of the year." Their conclusion is that there is a holiday effect **in returns** and
  little evidence of one **in standardized returns**.
- **Where the effect survives everything: small-cap indices.** Significant in the full universe, in
  the 17-effect universe, in subsamples, and — uniquely — still significant in **standardized**
  returns. This is the paper's single most robust empirical claim and the authors lead their
  conclusion with it.
- **Decay, recorded without dates.** For the series where a standardized holiday/end-of-year effect
  is significant in the full sample, the rolling-window analysis places that significance in the
  earlier part of the sample and not the later; and for one large-cap series the 5-effect universe's
  full-sample rejection is traced to "a few isolated events". So: a documented decay pattern of the
  McLean–Pontiff shape, plus a warning that a full-sample calendar rejection can be an
  influential-observations result.
- **Cross-market confirmation is not independent evidence, and they demonstrate it rather than
  asserting it.** The rolling p-value paths of the two large US indices they study are nearly
  identical, and indices across countries are correlated too; hence "an analysis of different
  indices cannot be viewed as independent tests, and hence, cross-indices studies is not
  necessarily a good way to control for the danger of data mining". They make the same point
  analytically: two datasets can be mined jointly, and overlapping-in-time datasets are dependent.
- **Honest about its own limits**: no transaction costs anywhere (it is a significance test, not a
  strategy evaluation), no out-of-sample period, serial independence assumed, and the authors state
  plainly that the universe choice "will involve a subjective element, in terms of universe of
  calendar effects that are under investigation, as different choices can lead to different
  results".
- **Not independently replicated** as such; it is itself an independent re-examination of a
  literature whose primaries this folder cites through
  `2026-09-15-reality-check-max-statistic-under-dependence.md`.

## Implementability here

The source is not a strategy, so "implementable" means three transfers, and the first two are free.

- **The standardized-return hypothesis is a screen the lab has never run, and it is the cheapest
  remaining check on the `calendar` half of `seasonality-calendar`.** `experiments/learnings.md`
  closed that half twice — [2026-09-01] on the complement-window sign condition, [2026-09-02] on
  boundary-crossing cost, with the general rule that a monthly overlay needs a window losing more
  than ~3.6%/yr. Both closures were measured in **mean** units (bps/day and %/yr). This source says
  the *prior* question is whether the window differs in **Sharpe** units at all, and reports that
  for the largest and most cross-country-consistent calendar effects it does not, because the high
  mean comes with high variance. Concretely: for every window the lab has already measured
  (turn-of-month T−3..T+3, T−8..T−4, Mondays, Nov–Apr), divide the window's mean by the window's own
  return standard deviation and compare with the complement. This re-reads numbers the lab already
  has, costs no trial, and either *strengthens* both closures with a third independent reason or —
  if some window does show a standardized gap — identifies the one window where the cost arithmetic
  is worth revisiting. **Prediction to pre-register before looking: Monday is the window most likely
  to survive standardization** (the source finds Monday has the lowest *standardized* return in the
  one large-cap US series where it shows up at all), and turn-of-month and the end-of-year windows
  the least likely, since those are the ones it attributes to variance.
- **The covariance-from-overlap identity is a better effective-trial-count than the lab's
  clustering estimate, wherever the candidates are averages over overlapping subsets of one
  sample.** The lab's deflated-Sharpe bar needs an effective number of trials, and
  `2026-09-16-clustering-trials-onc-effective-number-of-trials.md` and
  `2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` get it by clustering
  or eigenvalue-counting *estimated* return correlations. For a family of rules that differ only in
  **which days (or which names) they average over**, the correlation is not an estimation problem:
  it is `|S_k ∩ S_l| / √(|S_k||S_l|)` weighted by per-day variance. Two uses. (a) Any calendar
  screen the lab runs should be deflated against the whole enumerated universe it implicitly
  searched, with the exact correlation structure, not against the handful of windows actually
  reported. (b) The same algebra applies to **top-K books with overlapping membership**, which is
  what every one of the lab's family leads is — so this is a route to a *derived* rather than
  measured answer to "how many independent bets are on the board", and it is the natural companion
  to the v3 null's concentration-of-measure reading in
  `2026-10-15-random-portfolios-as-the-null-of-no-skill.md`.
- **The small-cap localisation is a closure argument for this universe, and it should be written
  down as one.** `research/README.md`'s rule for grading a source against the protocol-v2 panel: a
  mechanism whose own literature localises its effect to small, thinly traded or retail-held names
  is excluded **by construction** on a pool of large-cap national index members, and a null on such
  a mechanism here is uninformative rather than evidence against it. This source localises the only
  data-mining-robust, standardization-surviving calendar effect it finds to **small- and mid-cap
  indices**, in ten countries, across subsamples. So the honest statement for the lab is not "the
  calendar half is dead" but "the calendar half's survivable form is not reachable on this panel" —
  the same shape as `learnings.md`'s standing "real, large, significant and structurally
  unreachable" category (5–10 day reversal, regional neutralisation, the calendar overlay).
- **Two construction cautions if a calendar screen is run on this panel anyway.** (a) The repo
  forward-fills closes across foreign holidays, which manufactures exact zero returns, so a
  pre-/post-holiday classification built from the close panel alone will mislabel days; the
  non-forward-filled `volume` frame's NaN blocks are the usable holiday calendar, with
  `learnings.md`'s own caution that a vendor gap and a real closure are indistinguishable there.
  (b) The test assumes serially uncorrelated returns; on a 15-region panel with non-synchronous
  closes that assumption is violated at the daily frequency for reasons
  `2026-09-08-nonsynchronous-trading-econometrics.md` sets out, so a `χ²` from this recipe run on
  pooled global daily data would be mis-sized.

**What this note does not license.** No magnitude, no window, no "January is real". The content is
a universe enumeration, a closed-form dependence structure, a standardized-return hypothesis, and a
localisation of the surviving effect to a cap segment this panel does not contain.

## Related

- `2026-09-15-reality-check-max-statistic-under-dependence.md` — White's Reality Check and
  Sullivan–Timmermann–White, which this paper positions itself against: their bootstrap evaluates
  the **best** rule in the universe (a max statistic), this one evaluates the universe **jointly**
  (a quadratic form). The max statistic answers "is the winner better than chance"; the `χ²`
  answers "is there any structure here at all", and has power where many rules deviate a little.
  **STW 2001 (J. Econometrics, DOI `10.1016/S0304-4076(01)00077-X`, 203 citations on Crossref,
  checked 2026-10-16) is the primary this note stands in for and it is an unobtained pointer**:
  OpenAlex and Semantic Scholar both report it closed, its only repository location
  (`eprints.lse.ac.uk/18482`) is a record holding no file, and UCSD's eScholarship — the green
  location named by RePEc — answered three different paths with **HTTP 202 and a zero-byte body**,
  then 403 with a browser user-agent.
- `2026-09-16-does-meff-control-the-familywise-error-rate.md`,
  `2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md`,
  `2026-09-16-clustering-trials-onc-effective-number-of-trials.md` — the folder's existing
  treatments of dependence among tests, all of which *estimate* the dependence this source
  *derives*.
- `2026-08-24-deflated-sharpe-ratio.md`, `2026-08-24-multiple-testing-haircut.md`,
  `2026-10-01-limits-of-p-hacking-publication-bias.md`,
  `2026-09-09-specification-curve-analysis.md` — the haircut machinery and the universe-enumeration
  idea this source applies to one family.
- `2026-09-02-turn-of-month-payment-cycle.md`, `2026-10-04-halloween-six-month-seasonal.md`,
  `2026-08-29-same-calendar-month-seasonality.md`,
  `2026-09-02-return-seasonalities-common-factors.md` — the specific calendar effects whose named
  versions this source finds do *not* survive control over even a 17-effect universe.
- `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the
  "significance driven by a few isolated events" finding in its subsample analysis.
- `2026-08-17-mclean-pontiff-publication-decay.md` — the decay pattern its rolling p-values show.
- `2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md`,
  `2026-09-02-anomalies-by-size-group.md` — the size-segment question this source answers in the
  direction least convenient for this panel.
- `2026-10-16-day-of-week-and-the-cross-section.md` — the companion result: the index-level weekday
  effect this source cannot certify becomes a **cross-sectional** effect in a panel of individual
  stocks, which is a different test on different data and is not in tension with this one.
