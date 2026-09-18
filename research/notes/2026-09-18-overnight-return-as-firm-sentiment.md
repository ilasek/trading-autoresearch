---
title: "Overnight Returns and Firm-Specific Investor Sentiment"
authors: Aboody, Even-Tov, Lehavy, Trueman
year: 2018
venue: Journal of Financial and Quantitative Analysis 53(2), 485–505 (Tier 1)
url: https://doi.org/10.1017/S0022109017000989 (read in full at https://anderson-review.ucla.edu/wp-content/uploads/2021/03/Aboody-et-al_overnight_returns_and_firmspecific_investor_sentiment_JFQA2018.pdf)
citations: 188 (Semantic Scholar by DOI, checked 2026-09-18)
sample_period: July 1992 – December 2013 (CRSP opening prices begin July 1992); long-horizon test formed each December 1992–2012
markets: CRSP US common stocks with prior-year-end price > $5 and market capitalisation > $10m
tier: A
validation_overlap: false
published_post_2018: false
---

**Why this note is the operative one of the three filed tonight.** The other two
(`2026-09-18-overnight-intraday-return-decomposition.md`,
`2026-09-18-beta-at-night-versus-day.md`) describe effects whose premia accrue inside a window this
repo cannot hold separately, and both end in diagnostics. This paper's long-horizon result is measured
on **close-to-close buy-and-hold total returns over a 12-month holding period**, which is exactly the
shape this engine executes, and its **long leg carries the effect on its own**. It is the one
construction in this literature that survives contact with a long-only, 24-hour-holding lab.

## Mechanism

**The claim.** A stock's overnight return is a usable proxy for *firm-specific* investor sentiment —
the demand of sentiment-influenced (retail-leaning, attention-driven) investors for that particular
name, as distinct from the market-wide sentiment indices (closed-end fund discounts, IPO underpricing,
NYSE turnover) the literature normally uses. The argument is validation-by-properties: if overnight
returns really measure sentiment demand, they should exhibit the three things sentiment is known to
do, and the paper tests each.

1. **Short-term persistence.** Sentiment-driven share demand is persistent over days-to-weeks.
   Overnight returns duly show short-term continuation: high-overnight-return stocks keep earning
   high overnight returns for several subsequent weeks.
2. **Stronger where valuation is soft.** Sentiment matters more for firms that are hard to value.
   The persistence is duly stronger for high-return-volatility, small, young, unprofitable and
   high-expected-growth firms, and stronger where **institutional ownership is lower** — i.e. exactly
   where the sentiment-influenced clientele is a larger share of the marginal demand.
3. **Long-horizon reversal.** Sentiment-driven mispricing is temporary, so it must unwind. Stocks
   with high short-term overnight returns subsequently **underperform** those with low ones over the
   following year.

Point 3 is the tradeable one, and its direction is the one that matters here: **the cheap side of
this sort is the low-overnight-return side, and the cheap side is the side a long-only book can
hold.**

**Why the two horizons point opposite ways and that is not a contradiction.** Persistent demand
pushes the price up while it lasts (continuation), and the part of that push that was not information
must eventually come out (reversal). This is the same clientele/price-pressure structure as
Lou–Polk–Skouras, seen at two different horizons rather than in two different periods of the day, and
the two papers cite and corroborate each other. The mechanism is behavioural and explicitly so; no
risk story is offered or claimed.

## Construction recipe

**Overnight return, direct form.** `CTO_{i,d} = (O_{i,d} − C_{i,d−1}) / C_{i,d−1}`, with **both**
prices adjusted for splits, stock dividends and cash dividends. An overnight period is treated as
**missing** if either the prior close or the current open is unavailable — no filling. *(Contrast
Lou–Polk–Skouras, who impute the overnight leg from the intraday leg and the close-to-close return to
sidestep the adjustment-timing question. Two published conventions; see the pitfalls below for which
one this repo should use.)*

**Short-horizon test (weekly, for completeness — not the tradeable one).** A week runs Wednesday to
Tuesday (following Lehmann, Barber et al.). A stock's weekly overnight return is the average of its
daily overnight returns that week, times five. Rank all stocks each week, split into deciles, and
measure the top-minus-bottom difference in **overnight** returns over weeks `w+1` through `w+4`.

**Long-horizon test — this is the recipe to copy.**

1. **Formation, once a year, at the end of December.** For each stock with at least **15 daily
   overnight returns available in December**, compute the **average daily overnight return during
   December**.
2. **Rank ascending, split into deciles.**
3. **Hold decile 1 (the *lowest* average December overnight return), equal-weighted, for 12 months**,
   beginning the month after formation. Buy-and-hold total (close-to-close) returns.
4. Evaluation is the intercept of a monthly Carhart four-factor regression of the portfolio's excess
   return on `Rm−Rf`, `SMB`, `HML`, `WML`.
5. The hard-to-value conditioning is a **double sort**: rank into quartiles on the conditioning
   variable first (measured at end-September so its value is known at December formation — a
   deliberate, stated causality precaution), then into overnight-return deciles *within* each
   quartile.

**Hard-to-value proxies used:** return volatility (high = hard), size (small = hard), firm age (young
= hard), profitability (low = hard), expected growth rate (high = hard).

## Robustness evidence (qualitative only)

- **The long leg carries the result on its own.** In the full-sample four-factor regression, the
  portfolio long decile 1 alone has a **significantly positive** alpha, while the decile-10-only
  portfolio's alpha is negative but **not significant**. The long/short spread is significant. For a
  lab that cannot short, this is the single most important line in the paper: the effect is not an
  artifact of an unreachable short leg. Compare
  `notes/2026-09-06-long-side-share-of-anomaly-profits.md`, whose general finding is the opposite
  (anomaly profits usually sit on the short side) — this one is an exception, which is why it is worth
  a note.
- **The long leg's factor loadings say it is decorrelated from this lab's incumbent.** Decile 1 loads
  *below one* on the market, *positively* on SMB, near zero on HML, and **negatively on WML** (the
  momentum factor), all strongly significant. A long-only book built on this characteristic is
  structurally a low-beta, small-tilted, **anti-momentum** book. `program.md` says a challenger needs a
  decorrelated leg and `experiments/learnings.md` prices the required gain off that correlation; a
  negative momentum loading is the rarest thing on the lab's leaderboard. *(This is a statement about
  loadings, not about returns.)*
- **Not the bid-ask bounce.** The obvious microstructure story — stocks close at the bid and open at
  the ask, so an overnight-return sort is a spread sort, and spreads are persistent — is tested
  directly by recomputing overnight returns from **quote midpoints** (last valid midpoint before the
  close, first valid midpoint after the open, using Berkman et al.'s quote data). Conclusions
  unchanged.
- **Not beta, size, book-to-market or momentum.** The short-horizon persistence survives partitioning
  on each of those four separately; every partition's overnight-return difference stays reliably
  positive. Size changes the *magnitude* (larger in small stocks) but not the sign or significance.
- **The cross-sectional conditioning works in the predicted direction at both horizons.** The
  long-horizon reversal is significant in **every** hardest-to-value subsample and in only one of the
  five easiest-to-value subsamples. An effect that strengthens exactly where its proposed mechanism
  says it should is the informative kind — the lab's own standard from `learnings.md` 2026-08-30 ("a
  null that passes its own identifying test is worth more than one that fails it") applied to a
  positive result.
- **The critical negative result, stated by the authors themselves.** For the *short-horizon* test
  they also report the subsequent **close-to-close** returns by overnight-return decile, and find
  **no monotonic relation** and differences much smaller than in the overnight component. In other
  words: the short-horizon overnight continuation **is not close-to-close tradeable**, independently
  confirming the cross-period offset in `notes/2026-09-18-overnight-intraday-return-decomposition.md`
  and the lab's own 2026-08-30 screen. Only the long-horizon reversal is a close-to-close object.
- **Costs are not modelled anywhere in the paper.** No turnover figures, no spread assumptions.
  Mitigating: the long-horizon construction rebalances **once a year**, which is about the lowest
  turnover any candidate in this repo has ever proposed.
- **Replication status.** Single-market (US), single sample, no third-party replication row. The
  supporting literature it leans on (retail-demand underperformance; market-wide sentiment predicting
  speculative-stock underperformance) is independently established, and the clientele half is
  corroborated by Lou–Polk–Skouras on different data. **This is the weakest link in the note**: a
  Tier-A venue and a heavily cited paper, but the specific long-horizon portfolio result rests on one
  sample and one formation month.

## Implementability here

**The candidate, stated so it can be pre-registered.** Rank the universe on its trailing average
daily **overnight return** (component-decomposed from the daily bar), hold the *lowest* names
long-only, equal-weighted, for twelve months. Every input is in scope; the holding period is long; the
long leg is the paying leg; and the construction is mechanically unrelated to trend, which is what
`program.md`'s budget rules are asking for.

**Family slug.** Not obvious, and the strategy agent should decide rather than inherit a guess. The
signal is built from the non-close columns of the daily bar, which is `range-variance`'s clause ("what
the extra intraday information in a daily bar is actually worth"); the mechanism is a
clientele/liquidity-demand story, which reads `liquidity-volume`; the object is a past return, which
reads `price-trend` and would then be **capped at two trials and bring the legacy cap with it**. This
note's view: it is not a trend signal — it is a *component* of a return, and the paper's own factor
regression shows the resulting book loads *negatively* on momentum — so `price-trend` would be the
wrong slug and an expensive one.

**Four design decisions the source does not settle, and the honest handling of each:**

1. **The December formation month is untested elsewhere in the paper.** Every long-horizon result is
   formed at end-December. That collides with tax-loss selling, the turn-of-year effect and the
   January seasonal — all of which this folder already covers
   (`notes/2026-09-02-turn-of-month-payment-cycle.md`,
   `notes/2026-08-29-same-calendar-month-seasonality.md`) — and the paper does not disentangle them.
   **Two ways to handle this and they are not equivalent:** (a) reproduce December-only, which
   inherits the confound and gives ~30 annual formations in the train split; or (b) form at **every**
   month-end with overlapping 12-month tranches, which removes the calendar confound, raises the
   effective sample enormously, and is the construction this lab already has machinery and a note for
   (`notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md`; overlapping tranches are the
   strongest single mechanism in `learnings.md`). **(b) is the better design and is *untested in the
   source* — say so in the hypothesis rather than implying the paper supports it.** If (b) is run,
   the December-only version is the natural control, and a large gap between them is itself a finding
   about which effect was being measured.
2. **The formation window is one month of daily overnight returns** (≥15 observations). Do not
   lengthen it to "look more like momentum"; the source's short-horizon evidence says the sentiment
   signal is a days-to-weeks object and the long-horizon test deliberately forms on a *short* window
   and holds long. Formation length is the one parameter with direct source support at its stated
   value.
3. **Averaging versus summing.** The paper uses the **average daily** overnight return in the month,
   not the compounded monthly overnight return, which makes the signal robust to a name having fewer
   trading days than its peers — non-trivial in a 15-region universe on one calendar. Copy the
   average.
4. **Decile 1 of ~145 names is ~14 positions**, close to the book size the lab's existing
   constructions use, and well inside the 25% position cap. No re-derivation needed.

**Data pitfalls — the same four as the companion notes, and one extra.**

- **Verify the `open` panel's adjustment and currency basis before computing anything** (see
  `notes/2026-09-18-overnight-intraday-return-decomposition.md`). This paper's direct
  `(O_d − C_{d−1}) / C_{d−1}` form assumes both prices are adjusted on the same basis; **this repo
  should use Lou–Polk–Skouras's imputation instead** (`r_intraday = close/open − 1` from same-day
  prices, `r_overnight` backed out of the adjusted close-to-close return), because it is robust to an
  unknown adjustment convention and to any same-day scaling common to both prices. The signal is the
  same object either way when the panels are consistent, and only the imputed form is safe when they
  might not be.
- **Mask non-trading days.** A forward-filled close paired with a stale open manufactures a fake
  overnight return; on this universe's foreign holidays that is a systematic, region-correlated error,
  not noise. The paper's own rule — treat the overnight period as **missing** if either price is
  unavailable — is the right one, and the non-forward-filled volume panel is the mask this repo has.
- **"Overnight" is a local window.** Comparing a Tokyo name's overnight return with a New York name's
  is comparing different periods of the world clock. Region-demean the score, or at minimum report the
  un-demeaned version as a control
  (`notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md`).
- **Survivorship cuts against this one specifically.** The hard-to-value conditioning says the effect
  is strongest in small, young, unprofitable, high-volatility names. This universe is 145 large,
  current, *surviving* names — the easiest-to-value end of the paper's own spectrum, where four of its
  five subsamples show no significant effect. **The pre-registered expectation should therefore be a
  weak effect, not the paper's headline**, and if the lab measures something strong here that is a
  reason for suspicion rather than celebration. This is the same trap as every previous
  `low-vol`/`risk-level` sort on this universe
  (`notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`).
- **Free screen before the trial.** The signal's rank correlation with the champion's own score and
  with the trailing total return costs nothing. The paper's factor regression predicts a *negative*
  momentum loading; if the measured correlation with the incumbent's holdings is strongly **positive**
  on this universe, the construction is trend in costume (the lab has caught exactly that twice —
  close-location value, 2026-08-30) and the trial should not be spent. Pre-register the sign.

## Related

- `notes/2026-09-18-overnight-intraday-return-decomposition.md` — the clientele mechanism and the
  data-handling recipe; also the reason the *short*-horizon version of this signal is not tradeable
  close-to-close.
- `notes/2026-09-18-beta-at-night-versus-day.md` — the systematic counterpart.
- `notes/2026-09-06-long-side-share-of-anomaly-profits.md` — the usual finding that the short leg pays;
  this paper is a documented exception, which is what makes it reachable.
- `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the overlapping-tranche construction
  that fixes the December confound.
- `notes/2026-09-02-turn-of-month-payment-cycle.md`, `notes/2026-08-29-same-calendar-month-seasonality.md`
  — the calendar effects the December formation is entangled with.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`,
  `notes/2026-09-13-listing-age-as-a-level-effect.md` — why the hard-to-value half of this paper is
  mostly out of this universe's reach.
- **Two sources named but NOT read**, so no claim here rests on them: Berkman, Koch, Tuttle & Zhang,
  "Paying Attention: Overnight Returns and the Hidden Cost of Buying at the Open" (JFQA 2012,
  `10.1017/S0022109012000270`, 186 citations on Semantic Scholar, checked 2026-09-18) — the
  attention/retail-buying-at-the-open source this paper borrows quote data from; `cambridge.org/core`
  returned an HTML bot page instead of the PDF and `papers.ssrn.com` 403'd. And Akbas, Boehmer, Jiang
  & Koch, "Overnight returns, daytime reversals, and future stock returns" (JFE 2022,
  `10.1016/j.jfineco.2021.09.019`, 65 citations, checked 2026-09-18) — per its published abstract it
  builds a monthly *count* of days on which a positive overnight return was followed by a negative
  daytime reversal and reports that a more intense tug of war predicts **higher** future
  cross-sectional returns. That construction is the most directly book-shaped thing in this
  literature and its sign appears to run opposite to this note's signal, but OpenAlex reports the
  article closed with no repository full text, `ink.library.smu.edu.sg` is behind an Incapsula bot
  wall and SSRN 403s. **Abstract only; the definition of a "reversal day" and every threshold in it
  are unknown here. Do not build a candidate from it** — it is recorded so a future session with
  access knows what to fetch.
