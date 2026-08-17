---
title: "Time Series Momentum" + "Time-series momentum: Is it there?" (replication challenge) + "A Century of Evidence on Trend-Following Investing"
authors: Moskowitz, Ooi, Pedersen (2012); Huang, Li, Wang, Zhou (2020); Hurst, Ooi, Pedersen (2017)
year: 2012, 2020, 2017
venue: Journal of Financial Economics 104(2) (venue tier 1); Journal of Financial Economics 135(3), 774–794 (venue tier 1); Journal of Portfolio Management 44(1) (venue tier 1 practitioner-academic)
url: https://doi.org/10.1016/j.jfineco.2011.11.003 ; https://doi.org/10.1016/j.jfineco.2019.09.007 ; https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
citations: not verified this session (Crossref and Semantic Scholar APIs returned 403 at the egress proxy; publisher and preprint domains egress-blocked). Moskowitz–Ooi–Pedersen is one of the most-cited papers in the trend-following literature; no count was resolvable.
sample_period: MOP 1965–2009; HLWZ in-sample 1985:01–2015:12, out-of-sample 2000:01–2015:12; HOP 1880–2016
markets: MOP — 58 futures/forwards across equity indices, currencies, commodities, sovereign bonds. HLWZ — ~55 futures, same asset-class span. HOP — 67 markets across four asset classes
tier: A (for the evidence base as a whole, including the challenge; the *effect* is best described as contested — see below)
validation_overlap: false (all three samples end 2016 or earlier)
published_post_2018: true for HLWZ (2020); false for MOP (2012) and HOP (2017)
---

## Mechanism

Time-series momentum (TSM) is the claim that an instrument's **own** past return predicts its
own future return — distinct from cross-sectional momentum, which claims only that *relative*
past performance predicts *relative* future performance. A cross-sectional winner can have a
negative own-return forecast; a TSM long requires a positive one. The lab's entire momentum
line to date is cross-sectional, so this is a genuinely different object, not a variant.

Proposed economic mechanisms, in the order the literature takes them seriously:

- **Initial under-reaction, delayed over-reaction.** News diffuses gradually, so prices drift in
  the direction of the news for months; sentiment-driven extrapolation then pushes past fair
  value. MOP support this with the observation that predictability that is positive at one to
  twelve months **partially reverses at longer horizons** — the signature that distinguishes an
  under-reaction story from a pure risk premium.
- **Non-speculative hedging demand.** Producers and hedgers take price-insensitive positions;
  speculators absorbing them earn a premium that shows up as trend persistence.
- **"Crisis alpha" as a structural property, not a historical accident.** A long-short trend
  system flips short as a protracted decline develops, so it profits from drawdowns that unfold
  *slowly enough for the signal to turn*. This is a statement about the payoff shape — trend
  following is long-optionality-like, paying in sustained directional moves of either sign and
  bleeding in choppy, mean-reverting conditions. It is not a claim that any particular episode
  went any particular way, and it explicitly does *not* extend to fast crashes.

## Construction recipe

The canonical MOP construction, which HOP extends and most practitioner systems approximate:

- **Signal**: the sign of the instrument's own trailing 12-month excess return. Sign only — the
  magnitude is deliberately discarded, because magnitude carries little extra information and a
  lot of extra noise.
- **Position**: long if positive, short if negative. Held one month, then re-evaluated.
- **Sizing**: each position scaled by the **inverse of its own ex-ante volatility**, so every
  instrument contributes comparable risk. This is the step that makes 58 heterogeneous futures
  combinable at all, and it is intrinsic to the construction rather than an overlay.
- **Portfolio**: scaled to a constant target volatility; MOP-lineage work uses a rolling
  equally-weighted covariance estimate (HOP: three-year rolling monthly) for the portfolio-level
  scaling.
- **Multi-horizon ensemble (HOP)**: run the same rule at **1-, 3- and 12-month** lookbacks
  simultaneously and combine, rather than choosing one horizon. Note this is the same
  average-don't-select principle as the two companion ensemble notes, applied to lookback length.

## Robustness evidence (qualitative only)

**This is the section that matters most for this source, because the effect is contested.**

*Supporting side.* MOP's original evidence spans four asset classes over multiple decades and is
peer-reviewed at tier 1. HOP extends the sample to well over a century and reports the effect
present in **every decade** of that sample and across varied macro environments (recessions and
expansions, war and peace, high and low rates, high and low inflation) — a qualitative
subperiod-stability statement of the kind that is genuinely strong evidence, since a
century-plus sample is far outside any plausible data-mining window.

*Challenging side, and it is serious.* Huang–Li–Wang–Zhou revisit TSM in the JFE and find:

- **Asset-by-asset time-series regressions show little evidence of TSM**, in-sample or
  out-of-sample. The effect is not visible where the hypothesis actually lives.
- The large t-statistic in the **pooled** regression — the specification the original result
  leans on — **is not statistically reliable**: it falls below the critical values of both
  parametric and non-parametric bootstraps. The pooled standard errors were overstating
  significance.
- Most damaging for an implementer: the TSM *strategy* is profitable, but its performance is
  **virtually the same as a strategy based on the historical sample mean, which requires no
  predictability at all**. That is, the trading profits are attributable to being long assets
  with positive average returns and short those without — not to the time-series predictability
  the signal claims to exploit.
- Their overall verdict: the evidence for TSM is weak, particularly across a large cross-section
  of assets.

This is exactly the replication-status evidence the rubric asks for, and it points down. Two
tier-1 JFE papers disagree about whether the effect exists as specified. The honest tier
assignment for the *evidence base* is A — this is a well-studied, high-quality literature — but
the honest assessment of the *effect* is **contested, with the most recent peer-reviewed word
being sceptical**, and with the sceptical paper's alternative explanation (unconditional risk
premia, not predictability) being the more parsimonious one.

## Implementability here

**Blunt summary: this family reads much worse against this repo's constraints than its citation
count suggests, and the literature read carefully predicts the lab's three refutations rather
than contradicting them.**

Four structural obstacles, in descending severity:

1. **The evidence base is long-short; the repo is long-only.** A TSM system's positions are
   symmetric by construction, and the "crisis alpha" property — the main reason to want trend
   exposure alongside an equity book — comes entirely from the ability to **go short** as a
   decline develops. Long-only, the rule degenerates to "hold the asset when its trend is up,
   hold cash when it is down", which keeps the whipsaw cost and discards the payoff. This is
   the same short-leg-dependence trap already documented for momentum crash management
   (`notes/2026-08-17-momentum-crash-risk-management.md`) — now the second instance, which
   makes "which leg generates this?" look like a standing law rather than a one-off.
2. **The evidence base is multi-asset futures; the repo is a global stock+ETF universe.** MOP's
   and HOP's results are portfolio-level, across four weakly-correlated asset classes. Much of
   what makes those results attractive is diversification across ~60 instruments whose trends
   are largely independent. A long-only equity/ETF book has one dominant common factor, so a
   trend overlay on it is close to a single bet on that factor's direction, repeatedly taken.
3. **Inverse-volatility sizing is intrinsic to the construction and is refuted here twice.**
   The construction is not separable from its risk-scaling. The lab has established that
   inverse-vol weighting between sleeves of unequal diversification systematically favours the
   lower-return leg, and that risk-weighting underperformed capital-weighting on its ETF sleeve.
   Importing the construction means importing the refuted component.
4. **Gross leverage ≤ 1.0 makes volatility targeting one-sided.** Same constraint already
   recorded for crash-risk management: the lab can scale down but not up, so it gets the
   return-costing half of the mechanism only.

**Explicit tension with `learnings.md`, recorded rather than smoothed over.** The lab has
refuted three trend/regime overlays: per-asset 200-day-MA filtering on an ETF sleeve, a binary
SPY-trend regime switch, and (adjacently) drawdown-state braking. A naive reading of MOP/HOP
would say "but trend following is one of the best-evidenced effects in finance, so the lab must
have implemented it wrong." That reading is wrong, and the four obstacles above are why: the
lab implemented the only version its constraints permit — long-only, single-asset-class,
un-leveraged — and that version is not the object the evidence is about. Add HLWZ's finding
that even the full long-short multi-asset version's profits may be unconditional-mean effects
rather than predictability, and **the prior on family 2 should be revised down, not up.** The
lab's three refutations are consistent with the literature properly read.

What survives as usable, mechanism-only:
- **The multi-horizon-ensemble principle** (run 1/3/12-month lookbacks together rather than
  selecting one) is horizon-averaging and transfers cleanly to *cross-sectional* scoring, where
  the champion's 6-1/12-1 composite is already a two-component instance. This is the one part of
  the note that connects to something the lab has working, and it is better motivated by the two
  companion ensemble notes than by this one.
- **The sign-only construction** — discarding signal magnitude as noise — is a real mechanism
  claim and is the *opposite* direction to the lab's magnitude-weighting result, which is the
  repo's biggest single Sharpe gain. Recorded as a genuine contradiction between the TSM
  literature's design choice and this lab's strongest empirical finding. The reconciliation is
  probably that MOP discard magnitude in a *time-series* setting across heterogeneous assets
  where magnitudes are not comparable, whereas the lab uses magnitude *cross-sectionally* within
  one universe where they are. Worth stating so nobody "fixes" magnitude weighting by reading
  this paper.

**Recommended posture: family 2 is low-prior on this universe.** Not closed — the multi-horizon
principle is live and the family has zero coverage in the repo's trial history — but any
candidate should state up front which of the four obstacles it escapes, and should not lean on
MOP/HOP citation weight as if the evidence transferred.

## Related

- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md` and
  `notes/2026-08-17-averaging-over-estimation-windows.md` — the multi-horizon combination in HOP
  is an instance of the principle those notes develop properly.
- `notes/2026-08-17-momentum-crash-risk-management.md` — the first documented case of a momentum
  mechanism living entirely in the short leg; this is the second.
- `notes/2026-08-17-moving-average-rules-anatomy.md` — why the many trend rules in this family
  are largely the same object, and how to triage a new one without a trial.
- `experiments/learnings.md`: three refuted de-risking/trend overlays (consistent with this note,
  not contradicted by it); inverse-vol weighting refuted twice (a required component here);
  magnitude weighting (contradicted by MOP's sign-only design — see above).
