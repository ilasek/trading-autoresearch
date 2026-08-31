---
title: "Price Impact or Trading Volume: Why Is the Amihud (2002) Measure Priced?"
authors: Lou, Shu
year: 2017
venue: Review of Financial Studies (Tier 1 peer-reviewed)
url: https://doi.org/10.1093/rfs/hhx072
citations: 112 (OpenAlex, DOI:10.1093/rfs/hhx072, checked 2026-08-31; Semantic Scholar's DOI endpoint did not resolve this DOI)
sample_period: 1964–2012 (return analysis January 1964 – December 2012)
markets: US equities, NYSE and AMEX ordinary common shares (NASDAQ deliberately excluded; NASDAQ used only as a robustness sample)
tier: A
validation_overlap: false
published_post_2018: false
---

The authors' August 2016 working version read **in full** from an ICMA-hosted mirror
(`icmagroup.org/assets/documents/Regulatory/Secondary-markets/Bond-Market-Liquidity-Library/`);
the published article is RFS 30(12), 4481–4520. This is the paper `SUMMARY.md` has flagged as
an unread follow-up since 2026-08-29 — "the natural follow-up… its answer determines whether
the lab's `liquidity-volume` lead is a price-impact story or a trading-activity story".

**It answers in the opposite direction from the lab's own 2026-08-30 measurement.** That
tension is recorded explicitly in *Related* below rather than adjudicated, and the reason it
is not a straight contradiction is a functional-form difference the lab has not yet tested.

## Mechanism

The Amihud (2002) measure is built as a monthly average of a daily ratio:

    A_it = (1/D_it) · Σ_d |r_id| / DollarVol_id

and is universally read as a *price impact* proxy: return moved per dollar traded, so a high
value means an illiquid stock, and its positive return premium is read as compensation for
bearing that illiquidity. The authors' point of entry is that nobody has checked whether the
premium comes from the ratio at all, and that microstructure theory does not in fact map onto
this particular construct (they quote Chordia–Huh–Subrahmanyam to that effect).

The structural observation that drives everything: **the denominator has vastly more
cross-sectional dispersion than the numerator.** In their sample the 75th/25th percentile
ratio of the volume component is over 100×, while the same ratio for the absolute-return
component is about 2×; the volume component's standard deviation is roughly three times its
own mean, the return component's about 0.7 times its mean. A ratio whose denominator varies by
two orders of magnitude and whose numerator varies by a factor of two is, in cross-section,
mostly its denominator.

So they define a **"constant" measure** that deletes the numerator entirely:

    A_C_it = (1/D_it) · Σ_d 1 / DollarVol_id

and find three things that together do the work of the paper:

1. **A_C carries almost all of A's cross-sectional variation.** Correlation of 0.90 between
   the monthly measures (0.94 for the annual versions). For the turnover-based variant of the
   measure the corresponding correlation is 0.75.
2. **A_C is priced about as strongly as A itself** — the sort on the constant measure produces
   a spread statistically indistinguishable from the sort on the original, both raw and in
   four-factor alpha.
3. **The part of A that is orthogonal to A_C is not priced at all.** Regressing A on A_C
   cross-sectionally and sorting on the residual gives no positive premium (the point estimate
   is slightly negative and insignificant).

Since the |return| numerator is exactly what makes the measure a *price-impact* construct, and
deleting it costs nothing while keeping only it earns nothing, the premium is not being paid
for price impact.

The authors then close the obvious escape route — "maybe the volume component is a *better*
illiquidity proxy" — with a direct horserace. High-frequency benchmarks (a Kyle-λ price-impact
estimate from five-minute signed square-root dollar volume, and three standard spread measures)
are correlated 0.74 with the Amihud measure itself, confirming that A does capture price
impact well; but those benchmarks correlate only **0.35** with the turnover component that
actually drives the pricing. Decomposing A into a fitted transaction-cost component and an
orthogonal non-cost residual, **the non-cost component is priced and the cost component is
not**. The measure's genuine liquidity content and its return premium sit in different places.

Four further tests distinguish a liquidity story from a mispricing story, and all four favour
mispricing:

- **Calendar asymmetry.** The volume premium vanishes in January and is strong in the rest of
  the year; the high-frequency liquidity benchmarks do the exact opposite — they are priced
  only in January, and are unpriced over the full year as a result. Two effects with opposite
  calendar signatures are not the same effect.
- **No scarcity conditioning.** A liquidity premium should be larger when aggregate liquidity
  is scarce and investors care most about it. The volume premium is not larger following
  episodes of high market illiquidity.
- **Sentiment conditioning.** Following high-sentiment periods the volume premium is
  significantly larger, **and the difference comes from the short leg** — the
  Stambaugh–Yu–Yuan signature of overpricing that is hard to arbitrage away.
- **Earnings-window concentration.** The premium is large in the three-day earnings
  announcement window and absent outside it, the La Porta–Lakonishok–Shleifer–Vishny test for
  an anomaly that is corrected by news. Analyst forecast errors point the same way: the market
  is over-optimistic about high-volume stocks relative to low-volume ones.

The economic reading the authors land on is that high trading volume marks stocks that are
over-priced — through some combination of disagreement, visibility/attention, and sentiment,
all of which prior work has attached to volume — and that the "illiquidity premium" measured
by the Amihud ratio is the low-volume side of that mispricing, not a transaction-cost rent.

## Construction recipe

Everything needed to build the measures, from daily data only:

- **A** — monthly average over the estimation month of `|daily return| / daily dollar volume`.
- **A_C** — the same average with the numerator replaced by 1: **the mean of the reciprocal of
  daily dollar volume**. This is the priced object.
- **AT** / **AT_C** — the same two with turnover (daily share volume / shares outstanding) in
  the denominator instead of dollar volume. Needs shares outstanding, which this repo lacks.
- **|Ret|** — monthly average of daily absolute returns; the numerator on its own.
- **Residual measures** — cross-sectional regression of one measure on another, keep the
  residual, sort on it. This is the paper's main identification device and it is free.

Bookkeeping that matters:

- Require **at least 10 valid days** in the estimation month to compute a monthly measure.
- **Winsorize at the 1st and 99th percentiles of each cross-section.** A mean of reciprocals
  is unbounded above as volume approaches zero; this is not optional.
- **Lag by two months**: measures from month *t−2* are matched to returns in month *t*.
- Use **logs** of the measures in cross-sectional regressions, which makes the scaling of the
  raw measure irrelevant and removes any need to detrend or inflation-adjust volume. Sorting
  monthly does the same job for portfolio tests.
- The findings are reported to hold for Hasbrouck's square-root version of the measure as well.

The decomposition the paper leans on is just a log identity, and it is the useful part:

    ln(A) = ln(|ret|) + ln(A_C)

i.e. the Amihud measure separates cleanly into a **volatility-ish numerator** and a
**pure-volume denominator**, and the two halves can be priced separately in one regression.

## Robustness evidence (qualitative only)

Multi-decade US sample spanning roughly five decades of monthly cross-sections, over a million
firm-months. The core result is reproduced with annual rather than monthly measures, with the
square-root version of the measure, with the turnover-based variant from Brennan–Huh–
Subrahmanyam, on a NASDAQ subsample, and with the "half" (down-day / up-day) Amihud measures.
It also survives being asked as a systematic-factor question: factors built from the volume
component rather than the full measure are what price liquidity risk.

The paper is a decomposition rather than a new anomaly, which is the kind of result that
replicates well — it is arithmetic about a measure plus a set of conditioning tests, not a
discovered spread. It is peer-reviewed at the top tier, and it is the source
Harris–Amato (already in this folder, `2026-08-29-amihud-illiquidity-measure-and-replication.md`)
cite as reaching their conclusion by an independent route: Harris–Amato find that the
day-by-day pairing of |return| with volume contributes essentially nothing over the ratio of
the two means, which is the same finding from the estimator side.

**Single-market.** Everything is US, and specifically NYSE/AMEX. The authors exclude NASDAQ
from the main sample because dealer double-counting inflates its reported volume relative to
NYSE/AMEX — a *market-convention* problem, not an economic one. This matters here more than in
most notes: see the pitfall below.

Known decay: none documented in this paper. McLean–Pontiff's general discount applies, and the
mispricing reading makes it *more* applicable, not less — a mispricing effect concentrated in
the short leg is the archetype of what publication erodes.

## Implementability here

**This opens a construction the lab has not tested, and it is computable exactly.** `A_C` is
the mean of `1 / aux["dollar_volume"]` over a month. It needs no returns, no shares
outstanding, and no fundamentals. It is the single most directly implementable object in this
folder's `liquidity-volume` coverage.

The critical point is that **`A_C` is not any of the volume functionals the lab has already
tested and found null.** The lab's 2026-08-29 screen used log average dollar volume; its
2026-08-30 screen used relative volume. Both are functions of the *mean* of dollar volume.
`A_C` is the **mean of the reciprocal**, and by Jensen's inequality these are different
objects with different cross-sectional orderings: `mean(1/V) ≥ 1/mean(V)`, with the gap
growing in the within-month dispersion of volume. A mean of reciprocals is dominated by the
*quietest days of the month*, so `A_C` ranks instruments by how illiquid they get at their
worst, not by how much they trade on average. That is a genuinely different sort, and it is the
one Lou–Shu identify as the priced one.

Concrete suggestions:

- Build `A_C` per instrument per month-end from the daily dollar-volume panel, requiring ≥10
  valid days, winsorizing the cross-section at 1/99, and taking logs. Sort long-only on high
  `A_C` (i.e. low volume). This is one candidate.
- The **free diagnostic that should come first**: rank-correlate `log(A_C)` against
  `log(mean dollar volume)` in the cross-section. If it comes back near 1.0, `A_C` is the
  functional the lab has already refuted under another name and the family closes properly
  rather than on a technicality. If it comes back materially below 1.0, the lab's null was
  measured on a different object and the `liquidity-volume` verdict is reopened. Either way it
  costs no trial and it resolves the tension recorded below.
- The **residual trick is free and reusable**: cross-sectionally regress any composite signal
  on its suspected driver and sort on the residual. Lou–Shu use it to prove which half of a
  ratio carries a premium. The lab has a standing problem of exactly this shape — a signal
  that may be a known signal in costume — and this is a cheaper instrument for it than another
  trial. (`SUMMARY.md` #52's own-lag control and #57c's confound are the same manoeuvre.)

Pitfalls, and the first is severe:

- **Cross-market volume is not comparable, and this universe spans 15 regions.** Lou–Shu drop
  an entire exchange from a *single-country* sample because its volume convention differs.
  This repo's universe crosses fifteen market structures with different reporting conventions,
  different retail/institutional mixes, different tick regimes, and non-overlapping sessions.
  A raw cross-sectional sort on any volume functional over this universe will substantially be
  sorting on *venue*. Any `A_C` candidate should be **cross-sectionally normalised within
  region** (the folder's `2026-08-28-international-momentum-country-neutral.md` grouping screen
  applies unchanged), and a candidate that is not should be read as a region bet.
- **Long-only discounts this specific effect harder than most.** The sentiment test locates the
  premium's conditional variation in the **short leg** — the overpriced high-volume names. A
  long-only book cannot short them; it can only decline to hold them, and in a ~145-name
  universe the underweight available is small. This is the same structural discount the folder
  recorded for momentum in `2026-08-27-momentum-net-of-costs-debate.md`, arriving in a second
  family.
- **The mispricing reading changes what the signal is claiming.** If the premium is
  compensation for illiquidity it should be robust and persistent; if it is mispricing it is a
  decaying anomaly in hard-to-arbitrage names, and this universe is 140 large, liquid, globally
  known instruments — the opposite tail from where the effect is documented to live. This
  sharpens rather than resolves the folder's standing tension about this universe's instrument
  set (recorded 2026-08-29 between Gu–Kelly–Xiu and Amihud/McLean–Pontiff).
- **ETFs break the story.** 42 of ~145 instruments are ETFs, whose dollar volume reflects
  creation/redemption and hedging flow, not disagreement about a firm's value. The
  disagreement/attention/sentiment mechanism does not transfer. Either exclude ETFs from an
  `A_C` sort or neutralise the stock/ETF split explicitly.
- **Volume is not forward-filled and is NaN on foreign holidays.** Reciprocals of a sparse
  series need the ≥10-valid-days rule enforced per instrument-month, not assumed.
- **Turnover-based variants are unavailable** — no shares outstanding in this repo — so `AT`
  and `AT_C` are out of reach, and with them the paper's cleanest normalisation for firm size.
  `SUMMARY.md` #53 already recorded relative volume as the substitute and the lab measured it
  null; that null stands and is not what this note reopens.

## Related

- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the same measure from the
  estimator side. Harris–Amato's finding that the day-by-day pairing adds nothing over the
  ratio of means is the mirror image of this paper's finding that the numerator adds nothing.
  This note is the pricing-side companion `SUMMARY.md` said to fetch.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` and
  `2026-08-27-momentum-net-of-costs-debate.md` — the short-leg discount recurring.
- `notes/2026-08-29-same-calendar-month-seasonality.md` — the January asymmetry here is a
  calendar conditioning result and is usable as a screen in that family too: two candidate
  mechanisms with opposite January signatures are not the same mechanism.
- **Tension with `experiments/learnings.md`, recorded not adjudicated.** The lab's 2026-08-30
  entry concludes that "the family's live content is `ILLIQ`'s **price-impact numerator** and
  not trading activity under any normalisation, which answers the Lou–Shu question… without the
  paper." Lou–Shu conclude the exact opposite on a five-decade US sample: the numerator is
  inert and the denominator carries the premium. Three things stop this being a clean
  refutation of either side, and all three are testable here for free:
  1. **The functionals differ.** The lab tested log *mean* dollar volume and relative volume;
     Lou–Shu's priced object is the mean of the *reciprocal*. "Under any normalisation" is a
     stronger claim than the two normalisations actually tested support, and the rank
     correlation between them settles it at zero cost.
  2. **The universes differ in the way that matters most for this effect.** Lou–Shu's premium
     lives in a US single-market cross-section that includes small illiquid names; this
     universe is large, liquid, global, and survivorship-conditioned, and cross-region volume
     is not comparable without neutralisation.
  3. **The lab's null was measured as an IC, Lou–Shu's premium is a sorted spread conditioned
     on sentiment and earnings windows.** An unconditional IC of zero is consistent with a
     conditionally concentrated premium, and the paper's own tests are all conditioning tests.

  The lab's note that "a null that passes its own identifying test is worth more than one that
  fails it" is right and is not being contradicted here; what is contradicted is only the
  clause "under any normalisation".
