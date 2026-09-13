---
title: "Bad News Travels Slowly: Size, Analyst Coverage, and the Profitability of Momentum Strategies"
authors: Hong, Lim, Stein
year: 2000
venue: Journal of Finance (Tier 1)
url: https://doi.org/10.1111/0022-1082.00206
citations: 2638 (Semantic Scholar by DOI, checked 2026-09-13); 2094 (Crossref, same date); OpenAlex returns 4 for the same DOI — a clear undercount, recorded as another instance of the folder's "disbelieve a lone low count" rule
sample_period: analyst-coverage data from 1976; momentum strategies run 1/1980 – 12/1996
markets: US — CRSP NYSE/AMEX/Nasdaq, with I/B/E/S analyst coverage
tier: A
validation_overlap: false
published_post_2018: false
---

Read **in full** from the typeset *Journal of Finance* article (vol. LV no. 1, 265–295), served by
the lead author's own university page (`columbia.edu/~hh2679/jf-badnews.pdf`); the MIT co-author's
page (`web.mit.edu/jcstein/www/badnews.pdf`) carries the January 1999 draft with the same content
and was read as a cross-check. The **NBER working-paper PDF (w6553) is a text-layerless scan** —
`pypdf` extracts 58 characters from 59 pages — so the NBER channel, usually this folder's most
reliable, was the wrong one here and the author pages were right.

This is the paper the previous note's `COV` proxy comes from, and it is the cleanest statement in
the literature of *why* a continuation effect should be stronger in some names than others. It also
contains the single most important discount this folder can offer on the lab's own universe.

## Mechanism

**Gradual information diffusion.** The model behind it (Hong–Stein 1999) assumes investors observe
different pieces of firm-specific private information at different times, and that they cannot
condition on the information contained in prices. Information therefore seeps into the price over
time rather than jumping into it, which produces positive medium-horizon autocorrelation
mechanically. The testable content is comparative: **wherever information diffuses more slowly,
continuation should be stronger.**

The paper's three results are three ways of measuring diffusion speed:

1. **Size.** Past the very smallest stocks, momentum profitability **declines sharply with market
   capitalisation**. The exception at the bottom is explained separately — for the tiniest names,
   thin market-making capacity, not information flow, is the binding friction.
2. **Residual analyst coverage.** Holding size fixed, momentum works better among low-coverage
   stocks. Analysts are the population that propagates firm-specific news, so fewer of them means
   slower diffusion.
3. **The asymmetry, which is the paper's own favourite result.** The coverage effect is
   **much more pronounced among past losers than among past winners.** The mechanism offered is
   managerial: a firm sitting on good news has every incentive to push it out itself through
   disclosure, so outside analysts are nearly redundant; a firm sitting on bad news does not, so
   the marginal contribution of analysts to getting the news out is largest precisely when the news
   is bad. Hence: bad news travels slowly.

The authors are candid about the alternative they cannot fully exclude: coverage might proxy for
transaction costs or shorting difficulty that size does not capture, and short-sale constraints
independently slow price adjustment to negative information. They test two further proxies — share
turnover, and a dummy for the existence of listed options (a shorting-ease proxy, since puts
substitute for a direct short) — and report the results robust to both, while stating plainly that
they have no perfect stock-level cost measure.

## Construction recipe

- **Momentum leg**: six-month formation, six-month holding, raw returns, **equal-weighted**.
- **Bands, and the rationale matters more than the numbers.** They do *not* use deciles. The
  cross-section is cut into three: worst 30% (`P1`), middle 40% (`P2`), best 30% (`P3`), and the
  momentum measure is `P3 − P1`. The stated reason is signal-to-noise: the paper's object is
  **comparisons of momentum across subsamples**, and once the sample is also cut by size and
  coverage there are a dozen subsamples, so extreme deciles would leave too few names per cell to
  compare anything. Wide bands are the deliberate price paid for a clean cross-subsample contrast.
- **Residual coverage**: run a **cross-sectional regression of analyst coverage on firm size every
  month** and keep the residual; sort on that. A variant adding industry dummies changes the fit
  only marginally and is reported as not altering the conclusions, so the size-only regression is
  the baseline. Alternatives tried and reported robust: running the coverage regression separately
  within each size class, and using the industry-augmented residual.
- **Universe screen**: the main coverage tests **drop everything below the 20th NYSE/AMEX
  percentile**, so the results are not a microcap artifact. The size table that establishes result
  (1) is run on the full universe precisely to show where the bottom-decile exception lives.
- **Sorting order**: size and coverage are used both singly and in a joint sort; the interaction is
  reported in a plausible direction (the marginal importance of coverage is greatest among small
  stocks), which is itself a warning that the two variables are not separable.

## Robustness evidence (qualitative only)

- Cross-market corroboration for the underlying momentum effect is cited from European and emerging
  market samples; the *conditioning* results are US-only and this paper is their origin.
- The winner/loser asymmetry is reported as much more pronounced once the tiniest stocks are
  excluded — i.e. the asymmetry is not a microcap artifact, it is revealed by removing microcaps.
- Ratio-form magnitude, admissible under this folder's standing rule (proportional effects yes,
  levels and dated numbers no): **momentum profits are roughly 60% greater in the lowest-residual-
  coverage third of the sample than in the highest**. Recorded as a proportion for scale only — it
  is a property of a mid-1980s-to-1990s US cross-section with tens of thousands of name-months and
  has **no standing as a threshold on 140 global names**.
- The size gradient is stated as strong enough that momentum is economically and statistically
  weak at the top of the size distribution. This is the claim with the most direct bearing here and
  it is stated qualitatively on purpose.
- Heavily cited and heavily built on; the diffusion mechanism survives into the later lead-lag
  literature this folder has already covered. No dedicated replication study of the *coverage*
  result was found; treat result (2) as less firmly established than result (1).

## Implementability here

**Analyst coverage does not exist in this repo and never will.** The note's value is therefore in
four transferable pieces, ordered by what they are worth:

1. **A discount, and it is the reason to read this paper.** This universe is ~140 large global
   stocks and ETFs — squarely in the size region where this source says momentum profitability is
   *weakest*, and its top size decile is where the effect is closest to absent. The lab's
   `price-trend` champion works anyway, which is a fact about this universe, not a refutation; but
   any proposal whose pitch is "more momentum, better measured" should be read against a Tier-A
   source saying the effect's natural habitat is smaller names than these. Pair it with
   `notes/2026-09-02-anomalies-by-size-group.md`: that note says fewer predictors survive among big
   stocks, this one says by how much the flagship one fades along the size axis.
2. **A design rule the lab can adopt for free.** When the object of a measurement is *the
   difference between two subsamples* rather than the level of one book, widen the bands. The
   30/40/30 cut with an explicit signal-to-noise justification is directly applicable to the lab's
   own conditional screens, which have repeatedly compared narrow top bands across arms and then
   had to argue about pool counts. This is a screening convention, not a candidate, and it costs
   nothing.
3. **A tension with a verdict the lab reached on 2026-09-12, which must be stated rather than
   smoothed over.** The lab closed the `neutralize` operator on evidence — a free-beta regional
   residual lost to the plain demean, and the placebo rule went against it. Here, the residual
   *is* the identification: coverage is so strongly correlated with size that the raw variable
   tests nothing, and the monthly cross-sectional regression of the proxy on size is the only
   reason result (2) is interpretable at all. The two are not in contradiction — the lab
   neutralised a *score* against a factor to improve a book, while this paper neutralises a
   *conditioning variable* against a confound to make a comparison identifiable — but the
   distinction is exactly the kind the folder's own audit history says gets lost. **If the lab ever
   conditions on a proxy that is heavily correlated with size or liquidity, the residualisation is
   part of the test's identification and its 2026-09-12 closure does not apply.**
4. **A long-only discount that compounds with the previous note's.** The coverage effect is
   concentrated on the loser side. In a long-only book the loser side is not held; the conditioning
   payoff that survives is the smaller, winner-side one. Two independent Tier-A sources
   (this and Zhang) now agree on that asymmetry and on its direction, which makes it a
   standing property rather than one paper's finding.

**Pitfall.** Do not try to substitute a price-derived proxy for analyst coverage and call it the
same test. The closest available substitutes here — dollar volume, `ILLIQ` — are things the lab has
already measured as *level* signals in `liquidity-volume`, and the seated lead there is one of them.
Re-entering the same variable as a momentum conditioner is a legitimate but **different** hypothesis
and should be pre-registered as such, with the leg-level result held fixed, or it will read as a
second look at a characteristic that already has a seat.

## Related

- `notes/2026-09-13-information-uncertainty-and-price-continuation.md` — the same conditioning
  logic with six proxies, one of which (`AGE`) this repo can actually build.
- `notes/2026-09-02-anomalies-by-size-group.md` — the size axis measured across many predictors.
- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md`,
  `notes/2026-09-05-price-delay-market-frictions.md` — the same diffusion mechanism measured as a
  lag between assets rather than as a cross-sectional strength gradient; the lab's `DELAY`
  statistic came back at its own null, which is a datum against diffusion being detectable on this
  universe and should be weighed against result (2) here.
- `notes/2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — the operator whose
  closure this note qualifies.
- `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md` — the band-width question this
  paper answers pragmatically for cross-subsample comparisons.
