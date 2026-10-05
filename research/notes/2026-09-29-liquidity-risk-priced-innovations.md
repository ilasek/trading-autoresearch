---
title: "Liquidity Risk as a Priced Innovation — the gamma measure, and what two commissioned replications did to its premium"
authors: Pástor, Stambaugh (2003); Li, Novy-Marx, Velikov (2019); Pontiff, Singla (2019); Pástor, Stambaugh (2019, response)
year: 2003; 2019
venue: "Journal of Political Economy 111(3), 642–685 (Tier 1, peer-reviewed). The three
  replication-exchange papers are all Critical Finance Review 8(1–2) (Tier 1 for this purpose:
  CFR *commissioned* the two replications, which is the strongest form of the rubric's
  replication row)."
url: "https://doi.org/10.1086/374184 ; replications https://doi.org/10.1561/104.00000076 and
  https://doi.org/10.1561/104.00000075 ; response https://doi.org/10.1561/104.00000074"
citations: "Pástor–Stambaugh 2003: 4317 (Crossref by DOI, checked 2026-09-29). Semantic
  Scholar's DOI endpoint returns `Paper with id DOI:10.1086/374184 not found` — a JPE DOI this
  time, after three consecutive sessions of the same failure on RFS DOIs, so the pattern is
  Semantic Scholar's DOI coverage and not one publisher. Li–Novy-Marx–Velikov: 29 (Crossref by
  DOI, checked 2026-09-29). Pontiff–Singla: 21 (Crossref, same date). Pástor–Stambaugh 2019
  response: 21 (Crossref, same date)."
sample_period: "PS 2003: liquidity series August 1962 – December 1999; beta-sorted portfolios
  formed from 1965/1967 onward. The commissioned replications extend the window in both
  directions, the longest starting 1932 and all of them ending 2017."
markets: "US only — NYSE and AMEX ordinary common shares for the aggregate series (NASDAQ
  excluded by construction), NYSE/AMEX/NASDAQ for the sorts. No non-US evidence in any of the
  four papers."
tier: "A as a source *cluster* — a Tier 1 original plus two commissioned independent
  replications is the best evidentiary situation this folder has filed. But the tier splits:
  **the MEASURE is Tier A and replicates essentially exactly; the PRICED PREMIUM is Tier B at
  best and arguably fails.** Read the Robustness section before treating any of this as a
  reason to spend a trial."
validation_overlap: false
published_post_2018: "PS 2003: false. The CFR replication exchange: true (2019) — but its
  content is replication of a pre-2018 claim on samples ending 2017, not a new effect."
---

**Read**: Pástor–Stambaugh in full as NBER Working Paper 8462 (September 2001, 38 pp.), the
pre-publication version of the JPE article; Li–Novy-Marx–Velikov and Pontiff–Singla from the
Critical Finance Review's own hosted PDFs; the Pástor–Stambaugh response as NBER WP 25774. The
construction recipe below is quoted from the working paper's equations (1) and (4)–(8); both
replications state that they reproduce that construction from the published version, and both
report near-exact agreement with the authors' posted series, so the recipe is stable across
versions. **Access note, new refusal mode for this folder's records:** `www.stat.ucla.edu`
answered a course-page PDF request with an outright **`Recv failure: Connection reset by
peer`** over HTTPS and an *SSL certificate* failure over HTTP, while the agent proxy's own
status endpoint reported `bundleCoversEveryHost: true` — i.e. the host, not the proxy. That is
a ninth distinct refusal shape after the Cloudflare 403, OpenAlex's metered budget,
`pm-research.com`'s OpenID redirect, the statusless tunnel death of the 2026-09-15 Tweedie
note, Cambridge's HTML-for-PDF, Imperva's 200-with-212-bytes, `dspace.mit.edu`'s 429 and MDPI's
403. Generalise: **a connection reset and a cert error from the same host are one refusal, not
two problems to debug.**

This note exists because this folder has twice said in print that it had not opened this
literature. `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` sets the
illiquidity-*risk* literature (naming Pástor–Stambaugh 2003 and Acharya–Pedersen 2005) aside as
a different literature from the level measure it covers, and
`notes/2026-09-04-commonality-in-liquidity-across-countries.md` repeats the same disclaimer.
The lab meanwhile closed `liquidity-volume` **on the mean channel** (`learnings.md`
[2026-09-24]) — that closure was measured on an illiquidity *level* score. The risk channel is a
different object, and this is what it is worth.

## Mechanism

**The economic claim.** In standard asset pricing, a security whose low returns coincide with
bad states must pay more. Market-wide liquidity is a candidate bad state: it fluctuates, the
fluctuations are common across securities, and an investor who must trade dislikes holding
assets that fall precisely when trading gets expensive. So expected returns should be
cross-sectionally related not to a security's own liquidity *level* (that is the
Amihud–Mendelson channel, already covered here) but to the **sensitivity of its return to
innovations in aggregate liquidity** — its liquidity beta.

**The measure's own mechanism, which is the part worth having.** Per-name liquidity is
identified from *volume-related return reversal*. If signed volume is read as order flow, then
in an illiquid name a day's order flow in one direction is followed by a price move in the
opposite direction the next day: risk-averse market makers who absorb the flow are compensated
by buying low or selling high, and the compensation is larger when the flow is larger. The
per-name statistic is therefore the coefficient on *signed dollar volume* in a
next-day-return regression, and it is expected to be **negative**, larger in absolute value
when liquidity is worse. The authors derive the specification as an approximation to the
Campbell–Grossman–Wang equilibrium, and are explicit that the exact specification is
"somewhat arbitrary, as is any liquidity measure."

They also flag the mechanism's own confound, in print: asymmetric information can *weaken* the
volume-related reversal and even reverse it into volume-related continuation for names where
information-motivated trading dominates (Llorente–Michaely–Saar–Wang). So the measure is not
a clean read of trading cost; it is a read of reversal-per-unit-of-flow, which is a different
thing wherever informed trading matters.

## Construction recipe

**Step 1 — per-name monthly liquidity.** For each name `i` and month `t`, OLS on daily data
within the month:

    r_e[i,d+1] = θ + φ·r[i,d] + γ_it · sign(r_e[i,d]) · v[i,d] + ε

where `r_e = r_i − r_market` (excess of the market return that day), `v` is **dollar volume in
millions**, and `γ_it` is the liquidity estimate. Filters as specified: at least **15**
consecutive usable days in the month, and names priced below $5 or above $1000 excluded. Note
the deliberate asymmetry — the *excess* return signs the volume and is the dependent variable,
while the *total* return is the lagged-return control, so the control is less correlated with
the regressor of interest.

**Step 2 — aggregate the level.** `γ_t = (1/N) Σ_i γ_it`, equally weighted across names with
data that month.

**Step 3 — de-trend it.** Raw `γ_t` shrinks in magnitude as dollar volumes grow, so scale by
the market's own size: `(m_t / m_1)·γ_t`, where `m_t` is the total dollar value at the end of
month `t−1` of the names in that month's average and month 1 is the series' first month. This
is a *units* fix, not a normalisation of the signal, and it is the step most likely to be
skipped by an implementer and to matter.

**Step 4 — take innovations, not levels.** The scaled series is persistent. Form the scaled
difference `Δγ_t = (m_t/m_1)(γ_t − γ_{t−1})`, then regress

    Δγ_t = a + b·Δγ_{t−1} + c·(m_t/m_1)·γ_{t−1} + u_t

and define the innovation `L_t = u_t / 100`. The residuals of this regression are serially
uncorrelated; the division by 100 is cosmetic scaling.

**Step 5 — per-name liquidity beta.** `β_L` is the coefficient on `L_t` in a monthly multiple
regression that *also* includes the other pricing factors (market, size, value in the original;
momentum added in robustness), so that `β_L` captures comovement with aggregate liquidity
distinct from comovement with those factors.

**Step 6 — sort, and the honest part of the design.** Sorting on the *historical* `β_L`
requires a long estimation window (five years of monthly data minimum, explicitly longer than
the three years used elsewhere in the paper, "with no other information about liquidity beta
brought to bear"). Because historical betas are noisy, the paper's primary results instead sort
on a **predicted** `β_L`, modelled as a linear function of observable characteristics. Critically
for anyone reproducing it: the innovation series is **re-estimated at every formation date using
only data available then** — steps 3–4 are redone each year, so `L_t` is a causal series by
construction. That discipline is exactly this repo's walk-forward rule, stated in a 2001 paper.

## Robustness evidence (qualitative only)

This is the section that decides the note, and it is unusually clean because the Critical
Finance Review *commissioned* two independent replications.

- **The measure replicates, essentially perfectly.** One replication team reports a correlation
  of 0.989 between their reconstructed aggregate series and the original; the other reports a
  correlation of one to five significant digits, and publishes its code. There is no doubt about
  the construction recipe above.
- **The premium does not survive construction variation.** Pontiff–Singla concur with the
  original premium estimate *inside* the original window, then vary the index in ways intended
  to *improve* power — value-weighting instead of equal-weighting, including zero-volume days,
  dropping the price filters, and a modification aimed at reducing estimation error — and
  report that these "cast doubt on whether the gamma premium is compensation for liquidity
  risk." Building five further liquidity-risk indices from other popular proxies, they report
  that **none of ten specifications produces a statistically significant risk premium**, and
  that the estimate is not stable when the window is extended in either direction.
- **The traded factor is construction-sensitive in a specific, damning way.**
  Li–Novy-Marx–Velikov replicate the historical-beta traded factor and find it *sensitive to
  construction details*: significantly weaker when rebalanced at its **natural monthly
  frequency**, and weaker with either more or less extreme sorts. A factor that needs a
  non-natural rebalance frequency and one particular sort depth is a specification, not an
  effect.
- **The predicted-beta factor is worse than fragile — it is confounded.** The same team reports
  it is harder to replicate and "difficult to interpret because characteristics chosen to
  predict liquidity risk introduce mechanical relations to other known anomalies." Step 6's
  primary design is therefore contaminated by construction, which is precisely the failure mode
  `notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md` and the lab's own
  construction-nonstandard-error number are about.
- **One finding that cuts the other way, and it matters here.** Li–Novy-Marx–Velikov state
  plainly that, contrary to the original's claim, **liquidity risk appears essentially unrelated
  to momentum**. Whatever this leg is, it is not the incumbent in costume.
- **The authors' response concedes the mechanics, not the interpretation.** Pástor–Stambaugh
  (2019) accept both replications of the measure, argue the premium estimates hold up, and offer
  guidance on when to use the traded versus the non-traded factor and on improving the precision
  of liquidity-beta estimates — i.e. they treat beta-estimation noise as the live problem, which
  is the same thing the replications found.
- **Single market, no costs.** All four papers are US-only. None models transaction costs for
  the beta-sorted book, which for a sort on a *liquidity* characteristic is the obvious missing
  control: the high-beta decile is not cost-neutral against the low one.

## Implementability here

**What is reachable.** Everything in steps 1–4 runs on exactly the panel this repo now passes to
a candidate: daily closes give `r_i`, the universe average gives `r_market`, and `dollar_volume`
is the `v` the regression needs. No fundamentals, no intraday. This is one of the very few
Tier 1 asset-pricing constructions whose *inputs* are a literal match for `aux`.

**What breaks, and it is not small.**

1. **The panel's calendar will corrupt step 1 before anything else does.** `learnings.md`
   [2026-09-28] measured that `%zero` on this panel tracks *coverage*, not illiquidity
   (`spearman(%zero, panel coverage) = +0.632`, and both liquidity correlations came out the
   wrong sign), because `load_prices` forward-fills across the union of fifteen exchange
   calendars. A forward-filled day has a manufactured zero return **and** a NaN or stale volume,
   so `sign(r_e)·v` is a manufactured zero regressor and the daily lag `d → d+1` crosses
   holidays. Any attempt at `γ_it` must drop non-traded days per name *before* forming the
   daily pairs, and must then check that enough names still clear the 15-day minimum. On a
   universe whose foreign names lose a week a year to holidays, this is the whole
   implementation, not a detail.
2. **N = 139 where the original had 939 to 2,121.** The aggregate series is a cross-sectional
   average of noisy per-name regressions; its sampling error scales like `1/√N`. The innovation
   series `L_t` here would be roughly four times noisier than the published one before any
   other difference, and `L_t` is then the *regressor* in step 5, so the attenuation compounds.
3. **Step 5 cannot be run as specified.** SMB and HML need market cap and book-to-market, which
   this repo does not have. The reduced regression is market (+ optionally a within-universe
   momentum factor) only, which means the resulting `β_L` is *not* the paper's `β_L`: it retains
   whatever liquidity–size comovement the original removes. Say so in any hypothesis rather than
   claiming the construction.
4. **Sorting needs 5 years of monthly history per name for the historical route, and the
   predicted route is the one the replications say is confounded.** Given `learnings.md`
   [2026-09-13] (removing short-history names costs the momentum leg, placebo clean), the
   history requirement interacts with a known level effect on this universe.

**What this folder recommends, and it is not a candidate.** Given that the premium fails ten of
ten specifications in a commissioned replication, that the traded version needs an unnatural
rebalance frequency, and that this lab has *already measured* that a decorrelated leg with no
alpha moves nothing (`SUMMARY.md` #140(a), and the `liquidity-volume` closure of
[2026-09-24] priced exactly that case at an appraisal ratio of +0.078/yr), **a `β_L`-sorted
challenger is a low-prior trial and this note does not propose one.** What the construction is
worth here is different and cheaper:

- **As a state variable, not a score.** Steps 1–4 produce a *single time series* — a causal,
  daily-data-only measure of the universe's own aggregate liquidity innovation. That is a
  candidate conditioner and a candidate diagnostic (e.g. does the seat's paired `t` against a
  challenger concentrate in low-`L_t` months?), and it costs zero trials to compute. Note the
  lab's standing result that blending beats switching (`learnings.md` [2026-09-17]) before
  proposing it as a *switch*.
- **As a falsifier for the `%zero` finding.** `γ_it` and `%zero` are two liquidity proxies on
  the same panel that should agree in sign; [2026-09-28] showed `%zero` inverted. If `γ_it`
  also fails to rank the names the way ADV and ILLIQ do, the conclusion is about the *panel*,
  not about either proxy — and that is a free result of the same kind as the `%zero` census.
- **Use every screen to kill, never to forecast** (`learnings.md` [2026-09-28]) applies
  directly: this series is a screen.

## Related

- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the level measure, and the
  note that set this literature aside as a different one.
- `notes/2026-08-31-amihud-volume-component-decomposition.md`,
  `notes/2026-09-04-global-liquidity-proxy-horserace.md`,
  `notes/2026-09-04-high-low-spread-estimator.md` — the proxies whose horserace this measure was
  never entered in, because it measures reversal-per-flow rather than a spread.
- `notes/2026-09-04-commonality-in-liquidity-across-countries.md` — the commonality that makes
  an aggregate series meaningful at all, and the Tier 1 statement that ILLIQ levels are not
  comparable across countries (which applies to `γ_it` levels for the same reason).
- `notes/2026-09-29-liquidity-adjusted-capm-three-betas.md` — the theory-grounded
  decomposition of the same risk into three betas, and the finding that all three are collinear
  with the *level* this lab already closed.
- `notes/2026-09-29-funding-liquidity-and-margin-spirals.md` — why aggregate liquidity has a
  common factor and a volatility link at all.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md` (Lo–MacKinlay non-trading, rejected on this panel at its signature moment, `learnings.md` [2026-09-16]) and `learnings.md` [2026-09-28] — the two
  places this panel's calendar has already broken an imported daily-frequency construction.
