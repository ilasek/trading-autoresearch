---
title: "Mood beta and seasonalities in stock returns (congruent-mood recurrence, non-congruent reversal, and one loading that integrates them)"
authors: Hirshleifer, Jiang, Meng (published as Hirshleifer, Jiang, DiGiovanni)
year: 2020 (JFE); NBER WP 24676, June 2018, revised February 2019
venue: Journal of Financial Economics 137(1), 272–295 — venue tier 1
url: https://doi.org/10.1016/j.jfineco.2020.02.003 · https://www.nber.org/papers/w24676
citations: 142 (Crossref `is-referenced-by-count`, checked 2026-10-16)
sample_period: US stocks January 1963 – December 2016; DST tests 1967–2016; weather tests January 1963 – May 2016
markets: US only — CRSP common stocks on NYSE/AMEX/NASDAQ, plus the 94 Baker–Wurgler and 79 Keloharju–Linnainmaa–Nyberg characteristic portfolios as alternative test assets
tier: B
validation_overlap: false
published_post_2018: true
read: full text of NBER WP 24676 revision 0 (`nber.org/system/files/working_papers/w24676/revisions/w24676.rev0.pdf`, 1.3 MB; `pdftotext -layout` → 177 KB of text, 918 instances of `" the "`, `( )`-dropout check zero, no ASCII shift). The published JFE version was not obtained; equation and table numbers below are the working paper's. Per `research/README.md`'s anti-lookahead rule **no coefficient or premium magnitude from its tables is recorded here** — only signs, lag structure and which specifications survive controls.
---

## Mechanism

A model in which investors' **mood** fluctuates on a predictable seasonal cycle, and securities
differ in how much their prices respond to it. A mood shift `b` misprices a common factor and, on
top of that, each security's own payoff; a security's mispricing is then
`E(Mᵢ|b) = βᵢ₁·λ_f·γ_f·b + λ_ε·γᵢ·b` — its loading on the mood-prone factor times the factor-wide
mispricing, plus a firm-specific mood sensitivity. In a wide cross-section the firm-specific part
averages out, so the **aggregate** market's mispricing in a mood window is the factor term alone
(their equation 3.4) while the **cross-section** is dispersed in proportion to `βᵢ₁` and `γᵢ`.

Three consequences, each a stated proposition:

1. **Aggregate**: markets earn abnormally high (low) returns in positive (negative) mood windows,
   which is the existing calendar literature restated as a prediction rather than a finding.
2. **Recurrence and reversal (their Proposition 2, and the genuinely new prediction).** Mood shifts
   in two *congruent* windows are positively correlated, so relative performance across securities
   **recurs**; in *non-congruent* windows they are negatively correlated, so relative performance
   **reverses**. Crucially, "cross-sectional seasonal asset returns will recur under the congruent
   mood state and reverse under the non-congruent mood state, **regardless of whether the mood state
   is identified using calendar windows or not**."
3. **Mood beta (Propositions 3–4).** A single loading, estimated from returns in strong-mood
   windows only, subsumes much of the above: high mood beta predicts high returns in future
   high-mood windows and low returns in future low-mood windows. Market beta does not subsume it,
   and in these windows market beta carries a significantly *negative* premium (the low-risk
   anomaly) — which is also the authors' argument that mood beta is not just beta in disguise,
   since a beta story cannot produce the negative premium they estimate for low-mood windows.

This is the mechanism layer under three effects the folder already holds separately: the
same-calendar-month seasonal (Heston–Sadka), the seasonal factor premia of Keloharju–Linnainmaa–
Nyberg, and the weekday cross-sectional effect of
`2026-10-16-day-of-week-and-the-cross-section.md`. It reads them as one phenomenon in which the
*calendar label* is incidental and the **mood congruence of two windows** is what matters.

## Construction recipe

**Step 1 — label mood windows.** Two independent labelling schemes, and the paper runs both:

- *Calendar-labelled (`high`/`low`)*: the months with the highest and lowest average equal-weighted
  market excess return in the sample — January and March as high mood, September and October as
  low — with ex ante justifications (turn-of-year optimism; the SAD channel, where early-autumn
  daylight decline raises the seasonally-affected population most in September–October and March
  sees the largest decline). At the weekday level, Friday is high and Monday low.
- *Realized-extreme-labelled (`best`/`worst`)*: **the two best and two worst months by realized
  equal-weighted market return within each year**, and at the weekday level the best and worst
  weekday within each week. No calendar label at all.

Both labellings produce the same qualitative results, which is the robustness fact that makes the
recipe portable to a panel without US calendar semantics.

**Step 2 — the recurrence/reversal tests (no beta needed).** Fama–MacBeth regressions of a
security's current mood-window return on its own **average return in congruent mood windows** at
annual lags `k = 1`, `2–5`, `6–10` (equation 4.1; the independent variable is the average of the
designated lags). Swapping the regressor for the **non-congruent** window's past return (equations
for 4.1.3/4.1.4) gives the reversal test, with the coefficient sign predicted to flip.

**Step 3 — mood beta.** A time-series regression run **only on mood-window observations**, of the
security's excess return on the contemporaneous **equal-weighted** market excess return:

- *monthly*: `XRETᵢ,MoodMonth = αᵢ + βᵢ,month^Mood · XRET_A,MoodMonth + εᵢ`, on a **10-year rolling
  window, minimum 40 observations** (eight month-slots per year: four high/low plus four
  best/worst, double-counting a month that appears in both, which weights it more);
- *weekday*: the same on mood weekdays, **6-month rolling window, minimum 50 observations**;
- *cheap alternative that gives "qualitatively similar results"*: a **ratio** estimator,
  `(mean excess return in positive-mood windows − mean in negative-mood windows)` for the security,
  divided by the same difference for the market. No regression, two means per security;
- *composite*: the **first principal component** of the monthly and weekday mood betas, extracted
  cross-sectionally each month, roughly equal-weighted on the two by construction.

**Step 4 — use.** Rank the cross-section on mood beta, **flipping the sign when the forecast window
is a low-mood one** (so the spread is always high-minus-low mood beta in congruent terms). The
paper's second-stage regressions also include the historical seasonal return **orthogonalized to
mood beta**, which is the design that establishes how much of the old seasonal signal is the new
loading: for individual stocks the orthogonalized seasonal return's predictive power drops sharply
once mood beta is included, and at the portfolio level the non-congruent **reversal effect largely
disappears** after controlling for mood beta.

**Step 5 — out-of-sample mood windows, identified without returns.** Three, and they are the
paper's answer to the charge that mood windows were chosen by their returns:

- **Pre-holiday**: 13 US holidays celebrated for over a century (New Year's Day, Valentine's Day,
  Presidents' Day, St Patrick's Day, Easter, Mother's Day, Memorial Day, Father's Day, Independence
  Day, Labor Day, Halloween, Thanksgiving, Christmas); window `(−2, 0)` trading days — the two
  trading days before the holiday, plus the holiday itself when it is a trading day.
- **Daylight Saving Time weekends**: Friday close to Monday close over the two annual clock changes
  (Tuesday close substituted when Monday is not the week's first trading day) — a sleep-disruption
  mood shock with no return-based selection.
- **Weather**: station-level NOAA hourly cloud cover averaged 05:00–08:00 across stations within 50
  miles of the NYSE's zip centroid, **deseasonalized** by the same-week sample mean, with sunny and
  cloudy days defined as the least and most cloudy **quartiles** and the middle half treated as
  moderate.

Controls used throughout: **market beta estimated identically but on all windows** rather than mood
windows only, and **sentiment beta** (60 monthly returns, minimum 36, on the Baker–Wurgler
sentiment index orthogonalized to macro variables, alongside the value-weighted market).

## Robustness evidence (qualitative only)

- **Two independent mood labellings** (calendar-named versus realized-extreme) give the same
  qualitative recurrence and reversal results, at both monthly and weekday frequency.
- **Three out-of-sample mood identifications** that use no return information to select the window
  (holidays, DST, weather), all showing high-mood-beta securities outperforming in ascending-mood
  windows and underperforming in descending ones. The DST and weather tests also reproduce the
  prior aggregate findings they build on.
- **Long lag structure.** Recurrence is present out to annual lags 6–10, i.e. the loading being
  picked up is stable over a decade rather than a one-year echo. For individual stocks the
  **first annual lag is insignificant** for recurrence, while the non-congruent **reversal is
  present even at `k = 1`**, where 12-month momentum would push the other way — a sign contrast
  that is hard to produce by accident.
- **Survives the two obvious rival loadings**: market beta and Baker–Wurgler sentiment beta.
  Sentiment beta is insignificant; market beta's premium in these windows is significantly
  negative.
- **Three test-asset sets** (individual stocks, 94 BW portfolios, 79 KLN portfolios), with the
  portfolio-level effects stronger than the stock-level ones. Portfolios are deliberately
  **equal-weighted** rather than value-weighted, "because we believe that mood should have a
  stronger impact on small firms than on large firms" — the authors' own localisation of the
  mechanism, and the single most important line in the paper for this lab.
- **Gaps.** US only; no international replication in the paper. **No transaction costs and no
  turnover discussion anywhere** — the words do not appear. No multiple-testing haircut. The
  calendar-named mood months are selected partly on their own realized sample means, which is a
  post-selection problem of the shape `2026-09-15-inference-on-winners-post-selection-estimation.md`
  describes; the ex ante SAD/turn-of-year rationale and the independent `best`/`worst` labelling
  mitigate it but do not remove it. `published_post_2018: true`, so the novelty discount applies.
- Not independently replicated as far as this session established.

## Implementability here

This is the most buildable of tonight's three sources, and it bears directly on a leg the lab
already trades.

- **It is a candidate *refinement of the seated seasonal leg*, not a new family, and it adds no
  turnover.** The lab's `seasonal_same_month_return` averages a name's own past same-calendar-month
  returns unconditionally. Proposition 2 says that average is a mixture of two effects with
  **opposite signs**: recurrence from mood-congruent past months and reversal from non-congruent
  ones. The refinement is to split the formation months by mood congruence and take the difference
  (congruent-window history minus non-congruent-window history) instead of the plain mean. It
  rebalances on exactly the same monthly grid, so none of `learnings.md`'s calendar-overlay cost
  arithmetic applies — this is a **selection** change, which is the only kind of change the
  long-only budget constraint leaves reachable (the same conclusion
  `2026-09-25-short-term-residual-reversal.md` reached for `statistical-arbitrage`).
- **The `best`/`worst` labelling is what makes it runnable on a 15-region panel.** Calendar-named
  mood months are US-specific and this panel spans regions with different turn-of-year conventions,
  different daylight profiles (including southern-hemisphere names, where the SAD channel's sign
  inverts — see `2026-10-05-sad-weather-exchange-and-the-integration-escape.md`) and different
  holidays. The realized-extreme labelling needs none of that: per year, take the two best and two
  worst months of the **equal-weight eligible pool**'s return — which is also v3's benchmark, so
  the labelling is computed from the same series the gate scores against. It is causal (labels for
  year `t` use only year `t`'s own realized pool returns, and they enter as *formation* windows at
  lags ≥ 1 year), needs closes only, and costs one pass over the pool's monthly return series.
- **Mood beta is cheap here and the ratio estimator is cheaper.** `generate_weights` has a ~60 s
  budget per call on a ~1,000-name panel; the regression form is one univariate OLS per name on a
  10-year rolling window of ~80 mood-month observations, and the ratio form is two means per name.
  Both are comfortably inside budget. The walk-forward requirement is satisfied naturally because
  the estimator only ever uses realized past mood windows.
- **The pre-registration this candidate needs, and it is not optional.** Mood beta is a beta
  estimated on a *subset* of dates, so on this universe it will load on the volatility level —
  which `learnings.md` measures as the survivorship artifact directly (+19.4%/yr high-minus-low vol
  spread on train) and which [2026-09-17] showed turns `beta-minus` into "the volatility level
  wearing a risk label". So **pre-commit, before any trial: the rank correlation of mood beta with
  (a) trailing total volatility, (b) trailing market beta estimated on all months. If either is
  high, the candidate is the refuted volatility-level object and should be filed as such** rather
  than reinterpreted afterwards. This is the same discipline `SUMMARY.md`'s `#260` asks of the
  risk-weighting candidate, and the source itself supplies the discriminating test: its mechanism
  predicts a **sign flip** between high-mood and low-mood windows, whereas a volatility-level
  artifact does not flip.
- **The mechanism's own localisation is the standing caveat.** The authors equal-weight their test
  portfolios specifically because mood should bite harder on small firms; this panel is nine
  large-cap national indices' members plus ETFs. By `research/README.md`'s grading rule that makes
  a weak or null result here **uninformative about the mechanism**, and it should be stated in the
  hypothesis before the trial rather than used as an excuse after. The same rule flags the ETF
  sleeve: an ETF has no firm-specific mood sensitivity `γᵢ`, though it does have a factor loading
  `βᵢ₁`, so the mood-beta story *does* have content for ETFs where the same-calendar-month story
  (per `learnings.md` [2026-09-02], an effect absent in the ETF sleeve here) did not. That is a
  cheap, pre-signable contrast: mood beta should work in the ETF sleeve while the seasonal mean does
  not.
- **Pre-holiday windows are derivable, DST is derivable, weather is not.** Holiday windows come
  from the `volume` frame's NaN blocks per region (closes are forward-filled and cannot see a
  closure), with `learnings.md`'s vendor-gap caution; DST change dates are pure calendar arithmetic
  for the northern and southern hemispheres separately. NOAA cloud cover is outside this repo's
  data and the no-market-data rule covers fetching anything else, so the weather test is not
  reachable — do not propose it.

**What this note does not license.** No magnitude, no expectation about which months will turn out
to be the pool's best or worst here, and no claim that mood beta is skill on this panel. The content
is a labelling scheme, two estimators, a sign-flip discriminating test, and a pre-registration
requirement.

## Related

- `2026-08-29-same-calendar-month-seasonality.md` — Heston–Sadka, the effect this paper
  re-explains, and the folder's account of the seated seasonal leg's construction and cost problem.
  The tension to carry: Heston–Sadka read the same-month effect as a **stationary firm-specific
  seasonal**, this paper reads it as **mood congruence**, and the discriminating prediction is
  reversal across non-congruent windows, which a stationary-component story does not predict.
- `2026-09-02-return-seasonalities-common-factors.md` — Keloharju–Linnainmaa–Nyberg's seasonal
  factor premia, which the authors accept as the proximate mechanism and then ask what drives.
- `2026-10-16-day-of-week-and-the-cross-section.md` — the weekday instance; Monday/Friday is this
  paper's canonical non-congruent pair, and both sources agree the effect is cross-sectional rather
  than aggregate.
- `2026-10-16-calendar-effects-data-mining-robust-test.md` — the index-level significance question,
  and the small-cap localisation that independently matches this paper's equal-weighting choice.
- `2026-10-04-sad-daylight-seasonal-mechanism.md`,
  `2026-10-05-sad-weather-exchange-and-the-integration-escape.md` — the SAD channel this paper uses
  to justify its low-mood months, and the folder's existing reasons to doubt it generalises across
  hemispheres and integrated markets.
- `2026-10-07-past-return-consistency-and-the-seasonal-in-the-past-return-relation.md` — the other
  recent note on what a past-return-based seasonal signal is actually measuring.
- `2026-09-17-downside-beta-and-the-volatility-confound.md`,
  `2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the confound any
  beta-estimated-on-a-subset signal inherits on this universe.
- `2026-09-15-inference-on-winners-post-selection-estimation.md` — why selecting mood months by
  their own realized means is a post-selection problem, and why the `best`/`worst` labelling and
  the out-of-sample windows are the parts to lean on.
- `2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — a mood-beta book is a cross-sectional
  slice and is therefore inside the dimensions v3's null is drawn over, unlike a timing overlay.
