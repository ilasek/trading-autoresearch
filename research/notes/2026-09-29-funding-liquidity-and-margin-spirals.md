---
title: "Market Liquidity and Funding Liquidity — the mechanism under liquidity commonality"
authors: Brunnermeier, Pedersen
year: 2009
venue: Review of Financial Studies 22(6), 2201–2238 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1093/rfs/hhn098
citations: "5136 (Semantic Scholar by DOI, checked 2026-09-29 — the DOI endpoint resolved this
  RFS record, unlike three previous sessions' RFS lookups); 3993 (Crossref by DOI, same date)."
sample_period: "n/a — equilibrium theory. The paper contains no estimation sample; it derives a
  model and lists testable predictions. Its stylised-fact motivation cites the pre-2009
  empirical literature."
markets: none (theory, framed on securities traded by capital-constrained intermediaries)
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full** as NBER Working Paper 12939 (February 2007, 48 pp.), the working-paper version
of the 2009 RFS article; parsed cleanly, including the appendix proofs. The predictions quoted
below are from its concluding section, which the published version retains as its
new-testable-predictions list. Nothing in this note depends on the paper's motivating narrative,
which is deliberately not recorded here.

This is the third of tonight's notes and the only one that is not a construction. It is filed
because the other two hand this lab a measurement — an aggregate liquidity innovation series —
whose *interpretation* depends entirely on whether such a series has a common driver at all. If
each name's liquidity wanders independently, a cross-sectional average of 139 noisy per-name
estimates is just noise with a name. This paper is the reason to expect otherwise, and it
supplies the one conditioning variable this lab can actually compute.

## Mechanism

**The loop.** Traders (speculators, in the paper's language) supply market liquidity, and their
ability to do so depends on their *funding* liquidity — capital, and the margins they are
charged. Conversely, the margins financiers charge depend on the asset's *market* liquidity,
because an illiquid position is expensive to unwind if the trader defaults. Each side therefore
depends on the other, and under stated conditions the loop is destabilising: a shock that
reduces speculator capital widens margins, which forces position reduction, which worsens market
liquidity, which widens margins again. The paper names the two reinforcing channels a **margin
spiral** and a **loss spiral**.

**Why this is the mechanism for five stylised facts at once.** The model delivers, from one
structure, that market liquidity (i) can suddenly dry up, (ii) has commonality across
securities, (iii) is related to volatility, (iv) is subject to flight to quality, and (v)
comoves with the market. The *source* of commonality is the crucial one for this lab: the
speculators' shadow cost of capital is a **single state variable** shared across every security
they hold. Commonality in liquidity is not a property of the securities; it is the footprint of
one constraint binding on the intermediaries who make their markets. That is why a
cross-sectional average of per-name liquidity estimates is a meaningful aggregate rather than an
averaging of idiosyncrasies — and it is why the aggregate should be read as a *funding* state,
not as an average trading cost.

**Two structural features with direct construction consequences.**

- **Non-linearity.** The effect of speculator capital on market liquidity is highly non-linear: a
  marginal change in capital does almost nothing when speculators are far from their constraints
  and a great deal when they are close. Liquidity risk is therefore a *tail* object. A linear
  monthly beta on a liquidity innovation series — which is exactly what both of tonight's other
  notes construct — is the wrong functional form for the mechanism it is named after. This is,
  to this folder's knowledge, the sharpest statement available of why a well-motivated liquidity
  risk can be real and still fail to show up in an unconditional linear premium.
- **Cross-sectional asymmetry.** The sensitivity of margins and liquidity to speculator capital
  is *larger for securities that are risky and illiquid on average*. The spiral hits the illiquid
  end hardest. This is the theoretical counterpart of the collinearity Acharya–Pedersen measure
  between the three liquidity betas and the illiquidity level: the model says the level and the
  risk are not two independent characteristics but two readings of one exposure.

**Flight to quality.** As funding tightens, liquidity does not fall uniformly: the
cross-sectional *dispersion* of illiquidity widens, because the constrained intermediary retreats
to the assets with the lowest margins. The observable implication is about dispersion and
about the cross-sectional spread of a liquidity characteristic, not about its level.

## Construction recipe

The paper is theory; what it offers is a small number of constructions that follow from its
predictions and are stated in its own terms.

1. **Margins, and hence illiquidity, depend on volatility — and on which volatility.** The paper
   is explicit about the empirical counterpart: *fundamental* volatility is captured by price
   changes over a **longer** horizon, while total (fundamental plus liquidity-driven) volatility
   is captured by **short-horizon** price changes, "as in the literature on variance ratios."
   The construction this licenses is a ratio of short-horizon to long-horizon realised
   volatility, per name or for the universe, as a proxy for the *liquidity-driven component* of
   volatility. It needs daily closes only.
2. **Illiquidity should comove with volatility in both the time series and the cross section.**
   That is a sign-restricted, falsifiable prediction on two objects this lab already computes.
3. **A measure of funding tightness should explain the comovement of market liquidity.** Not
   implementable here — it needs intermediary balance-sheet or margin data. Record it as the
   part of the mechanism this universe cannot see, and do not substitute a price-based proxy
   while calling it funding.
4. **"Commonality of fragility"**: especially sharp liquidity reductions should occur
   *simultaneously* across many assets. The observable is the cross-sectional count of names
   experiencing a large liquidity deterioration in the same period, which is a different
   statistic from the average liquidity level.
5. **Conditional skewness.** Because constrained traders lose in the spiral and do not gain
   symmetrically when prices revert, the model predicts negatively skewed returns for the
   constrained intermediaries and conditional skewness (with unconditional kurtosis) in security
   prices. A skewness prediction that is *conditional on a funding state* is not the same claim
   as the unconditional idiosyncratic-skewness literature.

## Robustness evidence (qualitative only)

- **This is a model, and the rubric's replication row does not apply to it.** It is Tier A on
  venue, on citation weight, and on having become the standard reference for the mechanism; it
  is *not* evidence that any particular liquidity signal earns anything. Treat every sentence
  above as a reason an effect could exist, never as evidence that it does.
- **What the model explains was already documented, which is its strength and its limit.** The
  five stylised facts were established in the empirical literature the paper cites; the
  contribution is unifying them under one constraint, not discovering them. So the model gets no
  independent credit for them, and the folder should not read "explains five facts" as five
  confirmations.
- **The genuinely new predictions are, by the authors' own list, mostly about data this
  universe does not have** — margin requirements, prime-broker data, identified exogenous shocks
  to trading capital. The two that are reachable here (the volatility link and the
  variance-ratio decomposition of it) are the weakest tests of the mechanism, because
  volatility and illiquidity comove for reasons that have nothing to do with funding.
- **No cost modelling and no portfolio construction**, since there is no empirical section.

## Implementability here

**What this note is for.** It is the mechanism paper for the two constructions filed beside it,
and it changes the recommendation on both — downward for a sorted book, upward for a diagnostic.

1. **It explains why a liquidity-risk *premium* can fail replication without the mechanism being
   wrong.** The effect is non-linear in the distance to the constraint and concentrated in a
   tail; the tests that fail (`notes/2026-09-29-liquidity-risk-priced-innovations.md`) estimate
   an unconditional linear beta at monthly frequency. That is a real explanation and it is also
   an unfalsifiable-sounding one, so it must be held to this folder's own standard: **it licenses
   a conditional diagnostic, never a rescue of a book whose unconditional premium failed.** The
   lab's rule from [2026-09-28] — use every screen to kill, never to forecast — is the right
   posture.
2. **It predicts the lab's own collinearity problem before the data does.** Because the spiral
   is stronger for names that are illiquid on average, a liquidity-risk score on this universe
   should be close to an illiquidity-level score — the thing the lab already closed
   (`learnings.md` [2026-09-24]). Anyone proposing a `β_L` candidate here should expect the
   orthogonality screen to fail *on theoretical grounds*, not only empirically.
3. **The one cheap, genuinely new construction is the variance-ratio split.** Short-horizon over
   long-horizon realised volatility, computed causally from daily closes, is a candidate proxy
   for the liquidity-driven share of volatility. Before proposing it as a *score*, note three
   existing lab results it collides with: `range-variance` was closed on fifteen screens of one
   object (`learnings.md` [2026-09-13]); `beta-minus` turned out to be the volatility level
   wearing a risk label ([2026-09-17]); and a better variance forecast is not a better input once
   the forecast is smoothed ([2026-09-21]). A short/long volatility ratio is a *shape* statistic
   rather than a level, which is the one respect in which it is not already refuted — and that is
   the only claim this folder will make for it.
4. **Flight to quality is a dispersion prediction, and dispersion is where this lab has a
   standing result.** `learnings.md` [2026-09-18] records that a signed sort whose both ends beat
   the pool is a dispersion effect. The flight-to-quality prediction says the cross-sectional
   spread of illiquidity should widen when funding tightens — testable as a correlation between
   two series the lab can compute, with no trial spent and no score to sort on.

**What not to do with this note.** Do not use it to justify a regime switch on a funding proxy.
The lab has measured that blending beats switching on external state (`learnings.md`
[2026-09-17]), and this paper supplies no funding proxy that this universe can observe — only the
argument that one exists. Substituting a price-based proxy and calling it funding liquidity would
be exactly the imported-proxy inversion that [2026-09-28] caught with the `%zero` census.

## Related

- `notes/2026-09-29-liquidity-risk-priced-innovations.md` — the measure and the commissioned
  replications; this note is the reason its aggregate series has a common driver, and the reason
  its unconditional linear test is the wrong shape for the mechanism.
- `notes/2026-09-29-liquidity-adjusted-capm-three-betas.md` — the three-beta decomposition whose
  measured collinearity with the illiquidity level this model predicts.
- `notes/2026-09-04-commonality-in-liquidity-across-countries.md` — commonality measured
  directly across markets, which is the empirical object this mechanism generates.
- `notes/2026-09-22-limits-of-arbitrage-performance-based.md` — the closest thing already in this
  folder: performance-based arbitrage, the same capital-constraint logic, and the note the lab's
  seated champion's arbitrage-risk term descends from.
- `notes/2026-09-05-price-delay-market-frictions.md` — the folder's only prior use of a
  variance-ratio-style statistic, and the place to check before building the short/long ratio.
- `notes/2026-09-21-har-rv-volatility-cascade.md`,
  `notes/2026-09-21-panel-volatility-models-and-risk-targeting.md` — the volatility machinery a
  variance-ratio construction would reuse, and the lab's measured verdict on better forecasts.
