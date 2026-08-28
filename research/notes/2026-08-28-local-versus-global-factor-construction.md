---
title: "Size, value, and momentum in international stock returns"
authors: Fama, French
year: 2012
venue: Journal of Financial Economics (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2012.05.011
citations: 1431 (Crossref `is-referenced-by-count`, checked 2026-08-28); Semantic Scholar's DOI endpoint returns 361 for the same DOI — a clear undercount for a paper of this venue and vintage, and another instance of session 7's "disbelieve a lone low count"
sample_period: November 1990 – March 2011 (data from November 1989; the first momentum sort absorbs a year)
markets: 23 developed countries grouped into four regions — North America, Europe, Japan, Asia Pacific ex-Japan; all size groups including microcaps; returns in USD
tier: A
validation_overlap: false
published_post_2018: false
read: full text, typeset JFE article with volume and page headers (`johnhcochrane.com/s/Fama_French_size_value_momentum_JFE.pdf`)
---

## Mechanism

This is an asset-pricing paper, not a strategy paper, and its mechanism content for this repo is
about **what the right cross-section is** rather than about why momentum exists. Two claims:

1. **Pricing is not globally integrated, at least not to the resolution these tests can see.**
   If a single global model priced all assets, global factors should explain regional returns and
   local factors should not. The tests reject that direction: global models fare poorly on
   regional portfolios, while local models — factors and test assets from the same region —
   capture regional average returns rather well for size-value sorts. The authors are careful
   about power in both directions (global-factor regressions fit loosely, so some non-rejections
   are weak; local regressions fit tightly, so some rejections are of models that work well in
   economic terms). The direction of the evidence is nevertheless one-sided.
2. **Momentum is the hardest part of the cross-section for any of these models.** Local models
   have materially more trouble with portfolios carrying extreme momentum exposure than with
   value sorts. The authors' consolation — that real-world portfolios rarely take extreme
   momentum tilts — is precisely the case this repo *is*, so the consolation does not transfer.

The paper offers no behavioural or risk story for momentum itself, and explicitly declines to
endorse the cultural explanation of the Japanese exception (see below).

## Construction recipe

The construction is the reason to read this paper here — it is the canonical answer to "how do
you build a momentum sort on a multi-country universe".

- **Regions, not countries.** 23 developed markets are collapsed into four regions chosen so that
  market integration is a defensible assumption within each: North America (US + Canada), Europe
  (16 countries, EU or EU-aligned), Japan alone, Asia Pacific ex-Japan (Australia, New Zealand,
  Hong Kong, Singapore). Parsimony matters for test power; integration matters for
  interpretability. The authors flag Asia Pacific as the region where integration is most
  questionable.
- **Momentum signal**: cumulative return from `t−11` to `t−1` for a portfolio formed at the end
  of month `t` — the standard 12-1 with the sort month skipped ("skipping the sort month is
  standard in momentum tests"). Portfolios are formed **monthly** (the size-value sorts are
  annual; the size-momentum sorts are not).
- **Breakpoints are regional and are computed from big stocks only.** Momentum terciles use the
  bottom 30 / middle 40 / top 30 of lagged momentum, with breakpoints taken from the region's
  **big** stocks (top 90% of the region's aggregate market cap) so that plentiful microcaps do
  not drive the cutoffs. Size breakpoints are percentages of aggregate regional market cap, not
  counts of firms.
- **Global portfolios still use regional breakpoints.** This is the sentence worth carrying: when
  the authors build *global* size-momentum portfolios, they use **each region's own momentum
  breakpoints** to allocate that region's stocks, and global size breaks only for size. A global
  book is therefore assembled from regionally-ranked components, not from one pooled global
  ranking.
- **Weighting**: value-weight within each portfolio; the WML factor is the equal-weight average
  of a small-stock winner-minus-loser spread and a big-stock one, so the published factor gives
  half its weight to each size half.
- **Currency**: all returns in USD, excess of the one-month US T-bill. The authors state plainly
  that their tests **ignore exchange-rate risk**, which assumes either PPP or that these assets
  cannot hedge exchange risk, and they call this a potential problem in their inferences.

## Robustness evidence (qualitative only)

- **Momentum is present in North America, Europe and Asia Pacific across all size groups, and
  absent in Japan in every size group** — no hint of it in any Japanese size quintile.
- **The size gradient in momentum is the paper's most transferable result.** In every region
  except Japan, the winner-minus-loser spread is larger for small stocks, and the small-minus-big
  difference in average momentum exceeds two standard errors in every region except Japan. In the
  global portfolios the small-stock spread carries a t-statistic above 3 while the **big-stock
  spread's t-statistic is around 1.4** — i.e. on large caps alone, pooled across the developed
  world and over two decades, the momentum premium is not statistically distinguishable from
  zero. Winners show positive momentum in all size groups; it is the *magnitude* that is
  concentrated in small stocks and especially microcaps.
- **The authors' own discipline on the Japan exception is worth more than the exception.** They
  are skeptical of Chui–Titman–Wei's individualism explanation (the argument could run the other
  way: low individualism might *produce* momentum if prices react slowly), and they offer chance
  as "a serious contender" — a Hotelling `T²` test of whether expected WML returns differ across
  the four regions **fails to reject at the 90% level**. A striking regional zero, in a
  two-decade multi-country sample, is not necessarily a regional difference.
- **Sample robustness.** Two decades and 23 developed countries, all size groups (their stated
  contribution over prior international work, which focused on large stocks), value-weighted
  portfolios, results reported region by region rather than pooled. The cost is a relatively
  short sample, which the authors acknowledge and mitigate with diversified test portfolios. No
  transaction costs are modelled anywhere — these are factor returns, not strategies.
- **Multiple testing** is not the paper's frame, but the Hotelling test above is exactly the
  right instinct applied to its own headline exception, which is a mark of methodology honesty.

## Implementability here

- **The strongest and least welcome finding: this repo's universe sits in the size bucket where
  the momentum premium is weakest.** A global large-cap book is the one place in this sample
  where WML is not reliably different from zero. That does not contradict the lab's own measured
  results — the champion is a long-only concentrated book on a survivorship-conditioned universe,
  which is a different object from a value-weighted long-short factor — but it does say that the
  *external* prior for this repo's momentum edge should be near the bottom of the published
  range, not the middle. Combined with Rouwenhorst's roughly two-to-one small-over-large gradient
  and Asness–Moskowitz–Pedersen's statement that their large-liquid universe makes their results
  conservative, this is now three independent sources on the same discount.
- **It supplies the construction detail Rouwenhorst leaves coarse: rank within region, using
  breakpoints from the liquid names, then pool.** For this repo that is a concrete recipe —
  compute the momentum composite's cross-sectional ranks inside coarse regional groups rather
  than in one global pool, and assemble the basket from the top of each group. The paper's own
  global portfolios are built exactly that way. Note that this is a *ranking* change, not a
  weighting change, so it composes with the champion's magnitude weighting rather than competing
  with it: the z-score would be computed within group.
- **Grouping choice.** Four regions is the literature's parsimony point for power. On ~145
  instruments a three-way NA / Europe / Asia-Pacific split is probably the practical limit, and
  Japan's separateness in the source is a reason to *not* fold Japan into a generic Asia bucket
  if the universe has enough Japanese names to stand alone — but see the chance caveat: the
  source's own test cannot reject that the regional differences are noise, so a Japan-specific
  rule is not licensed by this evidence.
- **The skip-month convention is confirmed a third time** ("standard in momentum tests"), and
  the formation cadence — monthly momentum sorts even where the same authors sort annually on
  value — matches the repo's monthly-vintage design.
- **The currency caveat is now explicit and is the honest limit on both this note and
  Rouwenhorst's.** Both papers compute international momentum on returns converted to a single
  currency and both state that exchange-rate risk is ignored rather than handled. This repo's
  USD-converted, unhedged construction is therefore in line with the literature's practice, and
  the literature's practice is an acknowledged approximation, not a validated choice. Nothing
  read here licenses a claim that FX exposure inside the signal is either harmless or helpful.
- **What does not transfer**: everything involving book-to-market (no fundamentals here), the
  factor-model tests themselves (this repo does not run regressions on portfolio returns), and
  the value-weighting convention (the champion is magnitude-weighted, which is a different
  object and is already the lab's largest measured construction gain).

## Related

- `notes/2026-08-28-international-momentum-country-neutral.md` — Rouwenhorst's earlier and
  independent version of the same regional-ranking result, with the variance decomposition this
  paper does not report.
- `notes/2026-08-28-individualism-cross-country-momentum.md` — the cultural explanation of the
  Japan exception that this paper explicitly declines to accept; the disagreement is recorded in
  both notes.
- `notes/2026-08-28-value-momentum-everywhere-global-comovement.md` — the same large-liquid-
  universe discount reached from a different direction, plus the cross-market correlation
  structure this paper does not measure.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` and
  `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the universe-side
  caveats that interact with the size gradient here.
