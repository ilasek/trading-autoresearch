---
title: "Asset pricing: A tale of night and day"
authors: Hendershott, Livdan, Rösch
year: 2020
venue: Journal of Financial Economics 138(3), 635–662 (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2020.06.006 (read in full at http://faculty.haas.berkeley.edu/hender/CAPMday-night.pdf)
citations: 94 (Semantic Scholar by DOI, checked 2026-09-18)
sample_period: US 1992–2016 (opening prices constrain the start); international 1990–2014; US Treasury futures 1996–2013
markets: All US publicly listed common stocks (CRSP), plus 39 foreign countries (Datastream, common stocks only), plus 10 industry and 25 book-to-market portfolios and five- and ten-year US Treasury futures
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

**The claim, in one line: the security market line is not flat — it is the sum of an upward-sloping
night and a downward-sloping day.** Sort stocks into beta deciles and plot average return against
post-ranking beta separately for the close-to-open window and the open-to-close window. The night
relation is monotonically **positive**, the way the CAPM says it should be. The day relation is
**negative**. Add the two and you get the familiar too-flat 24-hour SML that the literature has been
explaining with borrowing constraints, mismeasured betas and unobservable market portfolios since
Black–Jensen–Scholes. The paper's contribution is that the flatness is not a weak version of the CAPM;
it is **two strong and opposite relations cancelling**.

**Where this goes beyond Lou–Polk–Skouras.** That paper's decomposition is cross-sectional and
characteristic-by-characteristic, and it reports that the *market beta* strategy earns its premium
intraday with an opposite-signed overnight component. This paper makes the systematic version the
object of study and shows the sign pattern is a property of **beta itself**, not of one sorting
variable: it survives for 10 industry portfolios, 25 book-to-market portfolios, cash-flow-news betas
and discount-rate-news betas separately, individual US stocks, and individual international stocks.

**The second, stranger finding.** The *intercepts* of the night and day SMLs imply materially
different risk-free rates for the two periods. They check this against something outside the equity
market: front-month five- and ten-year US Treasury futures returns also differ in sign between night
and day, in the direction the equity intercepts imply. That is an independent corroboration from a
different asset class, and it is the part of the paper that most resists a pure microstructure reading.

**No settled cause.** The authors do not claim one. Their own suggestion is that a model with
heterogeneous agents and time-varying constraints — a marginal investor who systematically differs
between the day and the night — would be needed, and that such a model could generate a negative
daytime risk premium. They pose the correct risk-free rate for a 24-hour holding period as an open
question rather than answering it. Treat this as a well-replicated empirical regularity with an
acknowledged theoretical gap, the same epistemic status as the tug-of-war decomposition.

## Construction recipe

1. **Split each daily bar** into a night return (previous close → open) and a day return (open →
   close).
2. **Estimate beta from daily *night* returns over a one-year rolling window.** This is their headline
   choice. It is not load-bearing: they re-run with betas estimated from close-to-close returns
   (their Fig. 4 and the surrounding tables) and the night-positive / day-negative pattern is
   unchanged. Use whichever the repo already has.
3. **Form ten beta-decile portfolios every month**, equal- or value-weighted (both reported; the
   pattern holds for both, and the night-minus-day slope difference is of comparable magnitude in the
   US and international samples).
4. **Measure average day and night returns per portfolio**, estimate post-ranking betas over the full
   sample, and fit the SML separately for each period. Fama–MacBeth and pooled-panel specifications
   with a `Day × β` interaction both appear; international tests pool countries with country dummies
   and cluster standard errors by day.

## Robustness evidence (qualitative only)

- **Multi-market and deep.** 39 foreign countries alongside the US, with the same sign pattern in
  both the EU and Asia groupings. Regional day slopes differ in size; both are negative, and both
  regions' night slopes are positive.
- **Not an artifact of the beta estimator.** Same conclusion with betas from close-to-close returns.
- **Not an artifact of closure length.** They re-estimate separately for one-night, two-night,
  three-night and four-night returns (ordinary nights, weekends, mid-week holidays, extended
  holiday weekends). The pattern holds in each group; it is not a weekend effect in disguise.
- **Holds across the day, not just at the open.** Splitting the session into thirteen half-hour
  intervals, the SML is flat only between roughly 11:00 and 14:00 and is downward-sloping in every
  other interval — so the negative daytime slope is not concentrated in the opening auction. This
  matters because it rules out the cheapest microstructure story.
- **Corroborated outside equities** by Treasury futures day/night returns.
- **One important caveat the authors surface themselves.** The abnormally high *daytime* return of the
  lowest-beta portfolio is **partly driven by stocks priced under $5**; excluding them substantially
  lowers the low-beta portfolio's expected day return. A visible part of the "low beta wins intraday"
  picture is a low-priced-stock effect.
- **Costs are not modelled.** No transaction-cost analysis anywhere in the paper, and no trading
  strategy is proposed. It is an asset-pricing paper, not a strategy paper.
- **Replication status.** No formal third-party replication row (Hou–Xue–Zhang, Jensen–Kelly–Pedersen)
  covers "the day/night SML" because it is not a characteristic anomaly. The 39-country evidence and
  the Treasury-futures corroboration inside the paper are the robustness on offer.

## Implementability here

**This is a diagnostic and an interpretation rule, not a book. Say that plainly before it becomes a
trial.** A long-only, close-to-close, 24-hour-holding repo collects the **sum** of the two slopes,
which is the flat SML everyone already has. There is no way to hold beta overnight and not during the
day inside the strategy contract; a proposal that needs to would be out of scope regardless of merit.

**What it does buy this lab, and it is worth having:**

1. **An interpretation of the lab's own repeated volatility-sort failures.** `experiments/learnings.md`
   records ten or eleven separate occasions on which a risk-level sort on this universe behaved
   contrary to the published sign, most recently the 2026-09-17 finding that `beta⁻` is "the
   volatility level wearing a risk label" and the identity `β⁻ = ρ⁻ · σ⁻ᵢ / σ⁻ₘ`. This paper adds a
   *second* decomposition of the same statistic, orthogonal to that one: a 24-hour beta is a sum of a
   night beta-premium and a day beta-premium with opposite signs. **Before sorting on any beta-like
   quantity, factor it — and this note supplies a factorisation the 2026-09-17 note did not have.**
   The lab's standing rule from that session ("before sorting on any ratio or beta, factor it and ask
   whether every factor has the sign you want") applies to the time-of-day factorisation too.
2. **A cheap, trial-free diagnostic with a pre-registerable prediction.** Decompose the *champion's*
   realised daily returns into night and day components and ask where its premium accrues. Lou–Polk–
   Skouras predicts a momentum book earns overnight; this paper predicts a book with any beta tilt
   earns its beta component overnight and pays it back intraday. Both are holdings-only computations
   on data the lab already has, cost no trial, and if this universe does *not* show the night/day
   split at all, that single result retires this whole literature for this repo — which is the
   cheapest possible outcome and should be measured first. Pre-register the expected sign.
3. **A warning about a specific measurement shortcut.** If the lab ever estimates beta or volatility
   from *overnight* returns thinking it is a cleaner risk estimate, this paper says the resulting
   sort has a different expected sign in the two periods and nets to roughly nothing over 24 hours.
   It is not a better risk estimator for a close-to-close book; it is a different one.

**Pitfalls carried over from `notes/2026-09-18-overnight-intraday-return-decomposition.md`** (all of
them apply here unchanged): verify the `open` panel's adjustment and currency basis before computing
anything; prefer the imputed overnight return to the direct `open_t / close_{t−1}` ratio; mask foreign
holidays where a forward-filled close would manufacture a fake overnight return; remember that
"overnight" is a *local* window, so the night/day split of a Tokyo name and a New York name are
different periods of the world clock. The last point is sharper here than in the LPS note: this
paper's international tests estimate betas **within country** and pool with country dummies, precisely
so that a Japanese night and an American night are never differenced.

**And one universe-specific caveat.** The low-priced-stock driver of the low-beta daytime return does
not exist in this universe (145 large, current, surviving names), so if the lab measures the day/night
split here it should expect the *low-beta daytime* leg to be weaker than the paper's headline figure
suggests — the paper's own robustness check is the right comparison, not its main figure.

## Related

- `notes/2026-09-18-overnight-intraday-return-decomposition.md` — the characteristic-level version of
  the same split, including the data-handling recipe this note depends on.
- `notes/2026-09-18-overnight-return-as-firm-sentiment.md` — the one branch of this literature with a
  close-to-close tradeable horizon.
- `notes/2026-09-17-downside-beta-and-the-volatility-confound.md` — the other factorisation of a
  beta-like statistic, and the lab's own measured verdict on it. Read together: a sorted beta is a
  product of a comovement and a level term *and* a sum of a night and a day term, and this universe
  has already broken the first reading.
- `notes/2026-08-17-volatility-timing-managed-portfolios.md` and the low-vol material in
  `SUMMARY.md` section 5 — the family whose sign this paper says is period-dependent.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — why this universe's
  high-volatility names are survivors, the lab's standing explanation for its own sign flips; the
  night/day split is a *second* candidate explanation and the two are not exclusive.
