---
title: "Maxing out: Stocks as lotteries and the cross-section of expected returns — with its international companion"
authors: Bali, Cakici, Whitelaw; with Cheon, Lee as the cross-country companion
year: 2011 (BCW); 2018 (Cheon–Lee)
venue: Journal of Financial Economics (Tier 1); Management Science (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2010.08.014 — companion https://doi.org/10.1287/mnsc.2017.2830
citations: 1756 for BCW (OpenAlex by DOI, checked 2026-09-01; the Semantic Scholar DOI endpoint returns "not found" for this DOI); 101 for Cheon–Lee (Semantic Scholar by DOI, checked 2026-09-01)
sample_period: July 1962 – December 2005 for BCW's portfolio analysis (CRSP data from January 1926); 1990–2012 for Cheon–Lee
markets: NYSE/Amex/Nasdaq for BCW; ~47,000 stocks across 42 countries for Cheon–Lee
tier: A
validation_overlap: false
published_post_2018: false
---

BCW read **in full** from the corresponding author's own hosting of the typeset JFE article
(`pages.stern.nyu.edu/~rwhitela/papers/max jfe11.pdf`), JFE 99(2), 427–446. Cheon–Lee recorded
**from its published abstract only** (`oa_status` closed; abstract read verbatim from the
Semantic Scholar record for the DOI) — it is used here only for cross-country breadth and the
one structural claim its abstract states outright.

This note exists for **`range-variance`, the one `program.md` family with zero recorded trials**,
which `experiments/learnings.md` declined for a third session on 2026-08-31 with an unusually
clean cause: *seven of the eight screened mechanisms sort on a cross-sectional **level** of
volatility, and the level is this universe's survivorship artifact* (raw Garman–Klass level
IC +0.0766, t = +5.75; a high-minus-low trailing-vol spread of +19.4%/yr on train). The lesson
recorded was "remove the level and nothing is left". The mechanism below is a level-adjacent
sort whose **sign is the opposite of the artifact's**, which is the specific reason it is worth
one more look, and it comes with the lab's own most direct counter-evidence attached (see
*Related*).

## Mechanism

The claim is behavioural and it is about the **upper tail of the recent daily return
distribution**, not about its width.

Many investors hold badly under-diversified books, and there is independent evidence — from
horse-track favourite-longshot bias, from lottery participation, from the trading records of
retail brokerage clients — that people pay above fair value for small probabilities of large
payoffs. Under cumulative prospect theory (Tversky–Kahneman probability weighting, as priced in
Barberis–Huang) or under optimally-distorted beliefs (Brunnermeier–Gollier–Parker), an asset
that offers a lottery-like payoff is **over-priced**, and an over-priced asset has a low
subsequent expected return. So the prediction is a *negative* cross-sectional relation between
a stock's recent extreme-positive-return behaviour and its future return.

The prediction only bites if extreme positive returns are **persistent** — an investor buying
lottery exposure must be able to identify it in advance. BCW verify this directly: a stock in
the top decile of the measure in one month has roughly a one-in-three chance of being in the top
decile the next month and roughly a two-in-three chance of being in the top three deciles, and
the persistence survives firm-level controls. This is the load-bearing empirical premise of the
whole mechanism and it is checkable here at zero cost.

**Why this is not the low-volatility effect wearing a hat.** Volatility is a *symmetric*
statistic; the lottery story is about *asymmetry*, and the two make opposite predictions about
the lower tail. BCW test exactly this with `MIN` (the negative of the minimum daily return over
the month), which is nearly as correlated with volatility as the maximum is (both around 0.75–0.76
with idiosyncratic and total volatility in their sample). A volatility story predicts `MIN` and
`MAX` carry the **same** sign; a skewness-preference or prospect-theory story predicts
**opposite** signs — extreme downside makes a stock undesirable and therefore cheap. The data
side with the asymmetric story: in firm-level regressions containing both, the slope on `MAX`
is negative and the slope on `MIN` is positive. **`MAX` versus `MIN` is the identifying test of
this family, it is free, and this lab has not run it.**

**The strongest structural claim, and the one that reframes a whole neighbouring literature.**
BCW's headline is not the `MAX` premium itself but that including `MAX` **reverses** the
idiosyncratic-volatility puzzle of Ang–Hodrick–Xing–Zhang. Unconditionally, high-idiosyncratic-
volatility stocks look like they earn low returns; conditional on `MAX`, the sign flips and
idiosyncratic risk is *rewarded*, as a world of risk-averse but under-diversified price-setters
would predict. Their reading is that idiosyncratic volatility is largely a proxy for `MAX`, not
the other way round. Cheon–Lee's abstract states the same thing from the cross-country side:
the idiosyncratic-volatility puzzle "exists only for stocks with high MAX".

## Construction recipe

- **Signal.** `MAX` = the single largest daily return of the past one month. `MAX(N)` = the
  average of the `N` largest daily returns of the past month, for `N` = 1…5. BCW report `MAX(5)`
  as the *more powerful* version and use it as their preferred control — averaging the top five
  days is a less noisy estimate of the same upper-tail object than a single day. **Prefer
  `MAX(5)` to `MAX(1)`**; that is the construction detail most likely to be dropped by a
  re-implementer and it is the one the authors themselves lean on.
- **Formation window.** One calendar month of daily returns; monthly rebalance; decile sorts.
  The signal is by construction a one-month statistic, so this is a monthly-grid mechanism.
- **Direction.** The *low*-`MAX` portfolio is the high-return leg. That matters here: see
  *Implementability*.
- **The companion sort.** `MIN` = the negative of the smallest daily return of the past month,
  same window. Used as the sign test, not as a signal.
- **Controls the effect is claimed to survive.** Bivariate sorts and Fama–MacBeth regressions
  on size, book-to-market, market beta, momentum (11-month, skipping the formation month),
  short-term reversal (the formation-month return), illiquidity, total and idiosyncratic
  skewness, co-skewness, and a fitted *expected*-skewness measure in the style of
  Boyer–Mitton–Vorkink.
- **What `MAX` is confounded with, in their own descriptive table.** Moving from the low-`MAX`
  to the high-`MAX` decile, median market capitalisation falls by more than an order of
  magnitude, median price falls to single digits, market beta rises from about 0.3 to about 1.2,
  illiquidity rises by more than a factor of ten, idiosyncratic volatility rises by a factor of
  six, the **formation-month return rises steeply** and the prior-11-month return falls steeply.
  A `MAX` sort is therefore simultaneously a small-cap sort, an illiquidity sort, a high-beta
  sort, a *short-term-reversal* sort and a *momentum-loser* sort unless those are controlled.
  The reversal overlap is the sharpest hazard for this repo — see *Pitfalls*.

## Robustness evidence (qualitative only)

- **Multi-decade single-market sample** with the effect present in both value- and
  equal-weighted portfolios and in firm-level regressions, and robust across the full battery of
  controls listed above.
- **Not a microcap artifact, but concentrated in small names.** The authors run three separate
  sample restrictions — dropping low-priced shares, restricting to NYSE-listed stocks only, and
  excluding everything below the NYSE size quintile breakpoint — and the effect remains
  significant, in both weighting schemes, in every one. They state plainly that the findings
  "are certainly concentrated among smaller stocks", and the magnitude and significance rise
  monotonically as capitalisation falls. **Both halves of that sentence should be carried
  forward**: it survives in large caps, and it is weakest there.
- **Cross-country, and only partially.** Cheon–Lee report the `MAX` premium as statistically and
  economically significant worldwide across 42 countries, and — the honest number — the effect
  is present in **26 of the 42**. That is real breadth and a real failure rate; treat it as "a
  widely but not universally present effect", not as a constant of nature.
- **A cultural moderator with a direct precedent in this folder.** Cheon–Lee find the premium
  larger in countries scoring high on Hofstede's individualism index, and larger when aggregate
  volatility is high. `research/notes/2026-08-28-individualism-cross-country-momentum.md` records
  the *same moderator* for momentum, from a different literature. Two behaviourally-motivated
  cross-sectional effects being modulated by the same country variable is either a genuine
  common cause (over-confidence / self-attribution) or an indication that the moderator is a
  weak proxy picking up developed-market data quality; this folder has now seen it twice and
  should stop treating either instance as independent evidence.
- **Known decay.** Not established for this effect specifically in the sources read. The general
  McLean–Pontiff discount applies with full force: `MAX` is a heavily published, easily computed
  signal, and this folder's own note on publication decay is the right prior.

## Implementability here

**In scope on data**: `MAX(N)` and `MIN` need daily closes only. No fundamentals, no intraday,
no options. Monthly formation and monthly rebalance match this repo's grid exactly.

**The rare favourable asymmetry: the reachable leg is the profitable one.** This folder has
repeatedly filed effects where long-only can only reach the leg that does not pay
(`statistical-arbitrage`'s residual reversion, the ETF lead-lag asymmetry). Here it is the other
way round: the **low**-`MAX` decile is the high-return leg, so a long-only book holds it
directly. What long-only forfeits is the (larger) underperformance of the extreme-`MAX` tail,
which is why the authors' own conclusion — that exploiting the phenomenon "would require
shorting stocks with extreme positive returns" — is about capturing the full *spread*, not about
which end carries the return. The long-only version of the idea is a **screen or an underweight**,
not a spread trade.

**The cost objection the authors raise does not transfer.** BCW note that high-`MAX` stocks are
small and illiquid and that transaction costs are "a serious impediment". That argument is about
holding the short leg in microcaps. A ~145-name universe of global large caps and ETFs has no
such tail, so the cost objection is much weaker here — and so, symmetrically, is the effect.

**Three concrete constructions, cheapest first:**

1. **The free identifying screen, before anything is built.** Compute `MAX(5)` and `MIN` on the
   train split and check (a) the decile-transition persistence of `MAX(5)`, (b) the sign of the
   `MAX` and `MIN` information coefficients. If `MAX` and `MIN` carry the *same* sign here, the
   lottery mechanism is absent on this universe and what is left is volatility — which the lab
   has already refuted three ways. This is a two-number test that either opens the family or
   closes it a fourth time, and it costs no trial.
2. **`MAX(5)` orthogonalised against trailing volatility**, then used as a long-only tilt or an
   exclusion screen on top of an existing book. The correct control is *volatility*, not size:
   the lab has already shown (2026-08-29) that its `ILLIQ` scout is not a disguised volatility
   tilt using exactly this within-tercile technique, so the machinery exists.
3. **As a negative screen on the champion's holdings** — drop or halve the weight of names in
   the top `MAX(5)` decile. This is the construction the mechanism most naturally supports
   (avoid over-priced lottery names), it adds little turnover, and it is measurable against the
   incumbent without a new signal.

**Pitfalls, in order of how likely they are to bite:**

- **`MAX(5)` is a one-month statistic dominated by the formation month's biggest up-days, and
  this repo has just measured that raw short-term reversal is the strongest thing on its
  universe** (5-day reversal IC +0.0455, t = +4.49). A `MAX` sort with a negative sign is
  *mechanically* correlated with a reversal sort with a negative sign. Any positive result must
  be shown to survive within reversal terciles, or it is reversal in costume. BCW control for
  exactly this and it is the first control to reproduce.
- **The survivorship direction is favourable, and that is the point.** This universe's
  constituent selection makes high-volatility names look *good* (+19.4%/yr high-minus-low on
  train). A `MAX` effect predicts high-tail names look *bad*. The artifact therefore works
  against the hypothesis, so a positive finding here is more credible than the same-sized
  finding on a level sort — and a null is correspondingly uninformative, because the artifact
  could be masking it. State which of those two you are in before running.
- **Compression.** With ~145 large liquid instruments there is no low-priced, high-`MAX` tail at
  all; the cross-sectional spread in `MAX(5)` will be a small fraction of what a CRSP-wide sort
  sees, and the source's own evidence says the effect is weakest exactly here.
- **ETFs are diversified by construction and cannot be lottery assets.** Roughly 42 of the
  instruments here are funds; including them in a `MAX` sort mixes objects the mechanism does
  not apply to. Sort within the single-name subset or add a fund indicator.
- **Region and currency.** Daily returns are USD-converted across 15 non-overlapping sessions;
  a single large FX move can manufacture a `MAX` day that is not a lottery event at the local
  level. `SUMMARY.md` #57c already records this class of contamination for daily
  cross-correlation and it applies verbatim to a one-day-extreme statistic.

## Related

- **`experiments/learnings.md`, 2026-08-29** — "the range-lottery measure (−7.95%/yr, t = −4.30,
  which is just low-vol)". This is the lab's own screen of a *range-based* lottery proxy, and it
  is the closest existing evidence. Two things about it. (i) The **sign is right and the
  statistic is strong**: it is not a null, it is a significant effect in the direction this
  mechanism predicts, dismissed on the grounds of collinearity with volatility rather than on
  its own significance. (ii) A range-based proxy — a function of the daily high-low — is a
  measure of *width*, which is precisely the symmetric object BCW's `MIN` test is designed to
  separate from the asymmetric one. The sources therefore do not contradict the lab's
  measurement; they say the lab measured the confounded quantity and dismissed it using the
  confound. The distinguishing test (upper-tail-only signal, `MIN` as the sign control,
  within-volatility-tercile conditioning) has not been run.
- **`experiments/learnings.md`, 2026-08-31 (`range-variance`, third decline)** — "the level *is*
  the survivorship artifact ... remove the level and nothing is left". `MAX(5)` is a level
  statistic, so on that reading it should have been captured. It was not, in the sense that the
  eight screened mechanisms are all width statistics; the upper-tail asymmetry is a different
  functional of the same daily bars. This is the same class of narrowing as `SUMMARY.md` #58's
  (a family closed on the mean of a quantity when the mechanism is about a different functional
  of it), and it should be resolved the same way — by measuring, not by argument.
- **`research/notes/2026-08-29-range-based-volatility-estimators.md`** — the estimator ladder.
  Note that if the lab wants an *asymmetric* upper-tail statistic from the full bar rather than
  from closes, `h = ln(H) − ln(O)` alone (the upside half of the Parkinson input) is the natural
  analogue of `MAX`, and `l` the analogue of `MIN`. That version is not in either source and
  would be an extension, not a replication.
- **`research/notes/2026-08-28-individualism-cross-country-momentum.md`** — the same cultural
  moderator, on a different effect. See *Robustness* above.
- **`research/notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md`** —
  independently finds idiosyncratic volatility *losing* its incremental predictive power once
  the sample is restricted to large firms, which is consistent with BCW's claim that the
  idiosyncratic-volatility result was never the primitive.
