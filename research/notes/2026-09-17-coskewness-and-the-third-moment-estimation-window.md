---
title: "Coskewness — the third-moment comovement premium, and why its replication verdict is a question about the estimation window"
authors: "Harvey, Siddique (the original and its 25-year follow-up); Hou, Xue, Zhang (the replication row that reads null)"
year: "2000 (JF) / 2023 (Critical Finance Review) / 2020 (RFS)"
venue: "Journal of Finance (Tier 1); Critical Finance Review 12, 355–366 (Tier 2 — peer-reviewed, replication-focused, but authored by the original authors about their own paper); Review of Financial Studies (Tier 1)"
url: "https://doi.org/10.1111/0022-1082.00247 (read in full from people.duke.edu/~charvey) ; https://doi.org/10.1561/104.00000134 (read in full from people.duke.edu/~charvey) ; https://doi.org/10.1093/rfs/hhy131"
citations: "Harvey–Siddique 2000: 2365 (Semantic Scholar by DOI, checked 2026-09-17); 2978 (OpenAlex, same date). Harvey–Siddique 2023: 8 (OpenAlex by DOI, checked 2026-09-17; Semantic Scholar's DOI endpoint returns 'not found'). Hou–Xue–Zhang: 1052 (OpenAlex, checked 2026-09-17)."
sample_period: "Harvey–Siddique 2000: Jul 1963–Dec 1993. Harvey–Siddique 2023: the original sample reproduced (Jul 1963–Dec 1993) plus an out-of-sample continuation of roughly the following 25 years. Hou–Xue–Zhang: Jan 1967–Dec 2016."
markets: "US (NYSE/AMEX plus the Nasdaq names CRSP carried at the time) in the original; the replications it surveys cover the US, developed-ex-US and emerging markets."
tier: "A for the mechanism and the original result (JF, ~2.4–3.0k citations, replicated by several independent teams). B for the size of the effect, because the source's own follow-up shows the estimate moves materially with research choices and the strongest single replication reads it as a null under a different estimation window."
validation_overlap: "true — but only through Harvey–Siddique 2023, whose out-of-sample window extends into the lab's validation split. Harvey–Siddique 2000 and Hou–Xue–Zhang are both false."
published_post_2018: "true for Harvey–Siddique 2023 and Hou–Xue–Zhang; false for Harvey–Siddique 2000."
---

All three read in full. Both Harvey–Siddique papers came from the author's own Duke page
(`people.duke.edu/~charvey/Research/Published_Papers/P56...`, `...P157...`) — a clean channel that
served both on the first try where publisher routes would not. **No performance figure from the 2023
paper's out-of-sample window is recorded here**, because that window overlaps the lab's validation
split; only its qualitative replication verdicts and its sensitivity structure are.

## Mechanism

**The object.** Standardised direct coskewness, a factor-loading-shaped statistic:

    β_SKD,i = E[ ε_i · ε²_M ] / sqrt( E[ε²_i] · E[ε²_M] )

where `ε_i` is the residual from regressing asset `i`'s excess return on the market excess return and
`ε_M` is the demeaned market excess return. It is unit-free by construction and — the authors'
stated reason for preferring it over the alternative — its numerator is built from residuals that are
orthogonal to the market by construction, so it is not just a relabelled beta. The alternative
estimator is the coefficient on the **squared** market return in an augmented market-model
regression; the two coincide once the market return and its square are orthogonalised.

**Why it should be priced, and the sign.** The CAPM prices an asset's contribution to a diversified
portfolio's *variance*. Extend the investor's utility to the third moment — Rubinstein,
Kraus–Litzenberger — and the asset's contribution to the portfolio's *skewness* is priced too. An
asset with **negative** coskewness loses more precisely when the market's squared return is large,
i.e. it makes a diversified portfolio's return distribution more left-skewed. Investors who prefer
positive skew must be paid to hold it. So the premium on coskewness itself is **negative**: the
most-negative-coskewness assets should earn the highest expected returns. Harvey–Siddique's framing
of why anyone should care is the sharpest version of the argument and is worth carrying verbatim in
spirit: *the highest-Sharpe-ratio styles often have the most negative skew, which is part of why
their Sharpe ratios are high* — so a Sharpe ratio computed on a negatively skewed book is partly
compensation being mistaken for skill.

That last sentence is the reason this note belongs in a lab whose gate is a Sharpe difference. It is
not a strategy claim; it is a claim about what the scoreboard omits.

**The estimation problem, which is the whole reason the literature disagrees.** Harvey–Siddique are
explicit about it in the follow-up: even moments (variance, kurtosis) are highly persistent, **odd
moments (mean, skew) are not persistent and carry large estimation error**, and any noise in a third
moment is amplified by a cube rather than a square. A realized negative skew is not evidence of an
*expected* negative skew — a name that had a bad run will estimate as negatively coskewed whether or
not it is. Everything downstream — window length, missing-data rule, breakpoints, weighting — is a
response to that one fact, and the effect size moves with each of them.

**Coskewness is not downside beta.** Ang–Chen–Xing establish this empirically in both directions: a
past-`β⁻` sort produces almost no spread in realized coskewness, and a past-coskewness sort produces
almost flat future `β⁻`. They are different loadings that both describe "asymmetry", and they
replicate differently (see `notes/2026-09-17-downside-beta-and-the-volatility-confound.md`).

**A link to the incumbent's family, from the original paper's own abstract.** Harvey–Siddique report
that the momentum effect is *related* to systematic skewness, with the low-expected-return momentum
portfolios carrying higher skewness than the high-expected-return ones. Read as a mechanism: a
momentum book may already be short systematic skewness, in which case part of its measured premium is
a skew risk premium and part of its measured Sharpe ratio is the artifact above.

## Construction recipe

The original, as restated precisely in the 2023 follow-up:

1. **Estimate** `β_SKD,i` for each asset from a rolling window of **monthly** returns. The base case
   is 60 months; the follow-up also runs 36, 48 and 72.
2. **Missing-data rule**: allow at most `m` missing months out of the window. The base case allows
   12 (the follow-up also runs 0 and 24). This is not a detail — see robustness.
3. **Rank** all assets on `β_SKD` and form three portfolios at **30/70 breakpoints**: `S⁻` = the 30%
   with the most negative coskewness, `S⁰` = the middle 40%, `S⁺` = the 30% with the most positive.
   Value-weighted in the original (the follow-up runs equal-weighted too).
4. **Hold the post-ranking month** (the 61st month for a 60-month window), then roll. The
   `S⁻ − S⁺` spread is the coskewness factor; a long-only expression is `S⁻` alone.
5. The derived loadings `β_SKS` (beta to the `S⁻ − S⁺` spread) and `β_S⁻` (beta to `S⁻`) are how they
   price other assets; for a strategy you want step 3's `S⁻` bucket, not these.

**Hou–Xue–Zhang's implementation, which is the same formula and a different recipe, and the
difference is the point**: they estimate the identical `Cs` statistic from **one month of daily
returns** (minimum 15 daily observations), sort into **deciles**, and hold 1, 6 or 12 months.

## Robustness evidence (qualitative only)

**The replication chain is unusually well documented, and it does not point one way.**

- **Reproduced in sample by independent teams.** A large-scale reproduction project
  (Chen–Zimmermann) recovers a significant in-sample effect at a `t`-statistic near the
  conventional bar, with a premium close to the original's. Note that none of these is a
  reproduction in the strict sense: CRSP's later addition of all Nasdaq names grew the cross-section
  by about half, so every "reproduction" runs on a different universe than the 2000 paper did.
- **McLean–Pontiff** included the variable in their 97-predictor out-of-sample and post-publication
  study; the general finding of that study (large out-of-sample and larger post-publication decay) is
  already in this folder, and the authors report private correspondence that this particular
  variable's out-of-sample behaviour was good. That is hearsay and is recorded as such.
- **Jensen–Kelly–Pedersen replicate it as a *marginal* pass at best.** Positive alpha in the US and
  a larger one in developed-ex-US, **no effect in emerging markets**, and against their own stricter
  significance bar the US estimate does not clear it while the developed-ex-US estimate does. For a
  global universe this is the most relevant single row in the literature, and it says: expect the
  effect outside the US, do not count on it inside, and do not expect it in emerging markets.
- **An independent extension (Anghel et al., in the same Critical Finance Review issue) confirms
  coskewness is priced but finds the *original measure is dominated by better ones*** — including a
  low-noise variant that uses only past returns. So the mechanism survives while the specific
  estimator does not. The alternative estimators were not read here; that is a named gap.
- **Hou–Xue–Zhang read it as a null.** Across all three holding horizons and all eight of their
  specifications, the high-minus-low `Cs` decile spread is **correctly signed** (negative, as the
  theory requires, since their decile 10 is the least-negative coskewness) but **statistically
  indistinguishable from zero everywhere**, with small magnitudes. This is a different kind of
  failure from the `β⁻` row in the same table, which is significantly *wrong*-signed: `Cs` here is
  right-signed and underpowered. The most parsimonious explanation is their estimation window — a
  third moment from ~20 daily observations is dominated by estimation error, exactly the amplification
  Harvey–Siddique warn about — but this is an inference from the two papers' methods, not something
  either paper states, and it should be labelled as such.
- **The original authors' own sensitivity table is the most useful thing in the follow-up.** Holding
  the formula fixed and varying only (i) value- versus equal-weighting, (ii) window length across
  36/48/60/72 months, and (iii) the missing-value limit across 0/12/24, the premium estimate moves by
  roughly a factor of two across the grid. The **missing-value limit** — the choice least likely to
  be pre-registered by anyone — is among the more influential, and equal weighting reads higher than
  value weighting throughout. This is a **non-standard-error result reported by the original authors
  about their own paper**, which is rarer than the finding itself.
- Costs: not modelled in any of the three. A 30/70 tercile sort rebalanced monthly on a long window
  is low-turnover by construction, which is the one thing working in its favour.

## Implementability here

**Reachable, with one real constraint: it needs years of history before it produces a signal.** The
statistic needs monthly returns, which come free from daily closes, but the base recipe wants 60
monthly observations — five years of burn-in per instrument before the first weight. Verify the
store's span and the train split's length can absorb that; a 36-month window is the source-sanctioned
short option and the follow-up shows it is not the weak member of the grid. Do not shorten to a
window of daily returns inside a single month to avoid the burn-in: that is precisely the
specification that reads null in Hou–Xue–Zhang.

**The long-only expression is the natural one, which is unusual for this folder.** The tradeable
bucket is `S⁻` — the most-negative-coskewness third — held long. The short leg (`S⁺`) is the leg you
were going to drop anyway. Coarse 30/70 breakpoints suit a ~145-instrument universe far better than
deciles (a tercile is ~48 names; cap at 25% and the position count is comfortable), and the source's
own breakpoints *are* the coarse ones. Cross-check against
`notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md` before choosing anything finer.

**Pre-register the four knobs before looking at a single number.** The follow-up's sensitivity table
is a ready-made specification curve: weighting scheme, window length, missing-value limit,
breakpoints. This lab has measured its own construction non-standard error and knows that knobs carry
dispersion (2026-09-14). Fix all four in the journal first; picking the best cell afterwards is the
specification search the lab exists to avoid, and this folder now has a note on what a selected
maximum is worth.

**Universe-specific cautions:**

- **The market proxy defines `ε_M`, and this universe is global.** Prefer the equal-weighted universe
  return and say so; a US proxy imports the same time-zone artifact that closed
  `lead-lag-spillover`.
- **ETFs will cluster at one end.** A diversified regional ETF's residual `ε_i` is small and its
  coskewness is close to the market's own, so 42 of ~145 instruments are near-degenerate on this
  statistic. Run it within-type or demean by type, and report which.
- **Survivorship works against the mechanism, which makes a null here uninformative.** Negative
  coskewness is the property of a name that collapses with the market; the universe is today's
  constituents, so the most negatively-coskewed names of the past are largely absent. A flat result
  is weak evidence; a positive result is the interesting one. Compare
  `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md`.
- **Jensen–Kelly–Pedersen's geography split is a free pre-registration.** They find the effect in
  developed-ex-US and not in the US. This universe spans 15 regions, so the prediction is
  directional and testable in one screen: if the signal works here, it should work better outside
  the US names. Stating that in advance costs nothing and makes the result falsifiable in a second
  dimension.
- **One diagnostic that is free and should come first.** Measure the champion's realized coskewness
  against the universe. If the momentum book is already short systematic skewness — which
  Harvey–Siddique's own momentum result predicts — then an `S⁻` book is not diversification, it is
  more of the same exposure, and part of the incumbent's measured Sharpe ratio is a skew premium.
  Holdings-only, no trial spent, and it is the kind of screen `learnings.md` credits with killing
  ideas cheaply.

## Tensions with this lab's own results — stated, not smoothed over

1. **`range-variance` was closed on evidence (2026-09-14) and vol-of-vol is on the do-not-extend
   list.** Coskewness is a third *co*moment against the market, not a volatility estimator, and the
   whole point of the standardisation is that it is a loading rather than a risk level. But a session
   proposing it should say that plainly rather than letting the family heading carry the argument.
2. **`learnings.md`: "Weight concentration is not risk concentration."** The lab has repeatedly found
   that concentration diagnostics mislead here. A skew-based signal is a distributional claim of the
   same genre, and the lab's own history says to be sceptical that a distributional statistic
   measured on this universe means what the literature's does.
3. **The one place this note cuts against the lab's gate rather than proposing a book.** If a
   negatively skewed book earns a higher Sharpe ratio *because* it is negatively skewed, then the
   deflated-Sharpe machinery — which corrects for selection and for skewness in the *selected*
   series — is not correcting for the fact that Sharpe ratio is the wrong currency for a skewed
   payoff. This folder has the growth-optimal and utility material that bears on it
   (2026-08-23), and this is an addition to that argument, not to the multiple-testing one. It
   proposes nothing and licenses no change to a frozen threshold.

## Related

- `notes/2026-09-17-downside-beta-and-the-volatility-confound.md` — the second-moment asymmetry, shown
  by Ang–Chen–Xing to be a distinct loading, with the opposite replication verdict.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` and
  `notes/2026-08-24-deflated-sharpe-ratio.md` — where skewness already enters this lab's scoring.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the decay study that includes this
  predictor.
- `notes/2026-09-09-nonstandard-errors-evidence-generating-process.md`,
  `notes/2026-09-09-specification-curve-analysis.md`,
  `notes/2026-09-15-inference-on-winners-post-selection-estimation.md` — the follow-up's sensitivity
  grid is a specification curve published by a paper's own authors, and these are the notes that say
  what to do with one.
- `notes/2026-09-12-missing-data-and-complete-case-pools.md` — the missing-value limit being an
  influential knob is the same finding from the other side.
- `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — why survivorship makes a null
  here uninformative.
