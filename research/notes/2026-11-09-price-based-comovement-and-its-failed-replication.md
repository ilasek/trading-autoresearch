---
title: "Price-based return comovement, and Comovement revisited — the claim and the replication that removes it"
authors: Green, Hwang (claim); Chen, Singal, Whitelaw (replication)
year: 2009 (Green–Hwang); 2016 (Chen–Singal–Whitelaw)
venue: both Journal of Financial Economics (venue tier 1) — JFE 93(1), 37–50 and JFE 121(3), 624–644
url: https://doi.org/10.1016/j.jfineco.2008.09.002 ; https://doi.org/10.1016/j.jfineco.2016.05.007
citations: Green–Hwang 213; Chen–Singal–Whitelaw 78 (both Crossref `is-referenced-by-count`, checked 2026-11-09; Semantic Scholar returns `not found` for the 2016 DOI, its third failure mode again)
sample_period: Green–Hwang 1971–2004; Chen–Singal–Whitelaw 1971–2012 for splits and 1976–2012 for index additions, with a 1976–2011 momentum-beta panel
markets: US (CRSP common stock; S&P 500 additions; two-for-one splits)
tier: A for the pair — two tier-1 articles, three- and two-figure citations, the second a direct replication of the first with a stated model, matched controls and a non-synchronous-trading adjustment
validation_overlap: false (both samples end by 2012)
published_post_2018: false
read: Chen–Singal–Whitelaw in full (typeset published JFE version, 174 KB of clean text, 1,101 instances of `" the "`, zero `( )` dropout, title line verified). **Green–Hwang was NOT obtained** — see Access; its claims below are relayed from the replication's own description of it and are flagged in-text.
---

## Access

**Chen–Singal–Whitelaw** came from **`pages.stern.nyu.edu/~<user>/papers/<Title With Spaces>.pdf`** —
an NYU Stern faculty flat directory, typeset published version, first try. This extends the
2026-09-18 faculty-page lesson and the 2026-10-13 `robjhyndman.com/papers/` lesson to a third shape
of filename: **title-with-spaces, percent-encoded**, rather than a short slug.

**Green–Hwang is unobtained across four channels.** OpenAlex reports `oa_status: green` with its
only OA location pointing at **SSRN**, which answered the exact `papers.ssrn.com/sol3/Delivery.cfm`
URL a search surfaced with **HTTP 403 and a 5.6 KB Cloudflare body** (re-confirming the standing
finding, now for a `Delivery.cfm` path rather than an abstract page); `citeseerx.ist.psu.edu`
returned **HTTP 000, zero bytes** — a transport failure, not an origin refusal; ScienceDirect is
closed; and a guessed university-host path 403'd. **Nothing in this note is attributed to
Green–Hwang except what Chen–Singal–Whitelaw state about it**, and that is said again at each point
of use. The replication describes the original's design, sample and headline coefficients in enough
detail to be a usable secondary for the *claim*; it is obviously not a neutral one for the *verdict*.

## Mechanism

### The claim (relayed, not read)

Stocks with **similar nominal price levels comove more than fundamentals justify**, because
investors categorise stocks by price. The test event is a stock split, chosen because a split
changes a firm's price category without changing anything real. As the replication describes it,
Green–Hwang run a regression of the splitting stock's return on the returns of a **high-priced**
portfolio and a **low-priced** portfolio before and after the split, and report that the loading on
the low-priced group rises and the loading on the high-priced group falls.

The price-band construction is worth recording because it is reusable: with `p` the pre-split price,
the **high-priced** comparison portfolio holds stocks priced in `[3p/4, 5p/4]` and the **low-priced**
portfolio stocks in `[1p/4, 3p/4]`. The event windows are the year ending one month before the split
and the year beginning one month after. The sample is two-for-one splits of ordinary common stock
with a pre-split price of at least \$10.

This claim sits inside a much larger literature on **excess comovement** — index additions and
deletions, index weight changes, retail-correlated trading, shared headquarters, shared
institutional ownership, closed-end funds, commodity futures — whose standard explanation is an
**asset-class effect**: correlated, non-fundamental demand for everything in a category.

### The replication, and what it actually establishes

Chen–Singal–Whitelaw re-examine two canonical cases, S&P 500 index additions and stock splits, and
their contribution is three separable things.

**1. The standard test statistic is uninformative.** The literature's evidence is the change in
coefficients of a **bivariate** regression of the stock's return on the old group's and the new
group's returns. A simple model shows those coefficients are **extremely sensitive to parameters
that have nothing to do with excess comovement**: in a bivariate regression both group returns proxy
for the same fundamental factor, so the relative size of a group's idiosyncratic variance determines
how much weight it gets. **A rise in one group's idiosyncratic risk shifts the coefficient away from
it even in a world with zero excess comovement.** The model also shows that the **univariate**
regression on the **old** group after the event — a specification neither original paper runs —
is the one that separates the hypotheses, because excess comovement predicts the loading on the
abandoned group falls while a pure fundamental-beta change predicts it rises along with everything
else.

**2. Run properly, the split evidence disappears.** In the univariate regressions, the splitting
stock's beta rises against the low-priced group **and rises by nearly the same amount** against the
high-priced group it supposedly left. That is the signature of a stock whose market beta went up,
not of a stock that changed category. The bivariate regressions still show the published pattern,
which is the point of part 1.

**3. The reason is momentum, and this is the part that is new rather than corrective.** Both event
samples are selected on past performance — only stocks that have risen split, and an index committee
favours larger, better-performing names (see the folder's index-rule cluster for the committee
half). **57% of the split sample sits in the top two momentum deciles**, against 37% for index
additions. The authors then measure what happens to betas around a momentum sort, independent of any
event, on annual June sorts 1976–2011 of stocks priced ≥\$10 outside the smallest NYSE size decile,
with 252-day rolling betas and a 21-day skip:

| Momentum decile | Year −2 | Year −1 | Year 0 | Year +1 | Year +2 |
|---|---|---|---|---|---|
| 10 (winners) | 0.964 | 0.976 | **1.143** | **1.271** | 1.166 |
| 9 | 0.918 | 0.916 | 0.981 | 1.038 | 0.994 |
| middle 6 | 0.818 | 0.829 | 0.832 | 0.834 | 0.841 |
| 2 | 0.903 | 0.925 | 0.917 | 0.876 | 0.888 |
| 1 (losers) | 1.047 | 1.094 | 1.092 | 1.031 | 1.015 |

**A winner's market beta rises sharply through the formation year, keeps rising through the first
holding year, and only then decays; a loser's drifts down.** The winner changes are significant at
every step up to Year +1 and insignificant from Year +1 to Year +2. The middle six deciles move by
essentially nothing.

**4. With that controlled, nothing is left.** Each event stock is matched to a firm in the same size
decile with the closest past-year return, betas are estimated with **Dimson (1979) leads and lags**
to handle non-synchronous trading, and the comparison becomes a difference-in-difference-in-
difference across event and matched samples. For **both** S&P 500 additions and splits the event and
matched samples show beta changes that are **not significantly different**. The authors' summary is
that there is "no longer any evidence of meaningful excess comovement from either an economic or
statistical standpoint", and that the existing results reflect **changes in comovement with
fundamentals**. The two adjustments do different work in the two samples: for splits the Dimson
correction does little and the **momentum control is decisive**; for index additions both are
needed.

Two earlier papers reach compatible conclusions on single cases (one on FTSE 100 turnover, one on
S&P 500 turnover), both by arguing the events coincide with fundamental changes.

## Construction recipe

Nothing here is a strategy; these are test-design rules.

- **To test whether a group change caused comovement**, report the **univariate** regression on the
  **old** group's return after the event, not only the bivariate pair. The sign of that coefficient
  is the discriminating statistic.
- **Never read a bivariate loading shift as an economic magnitude** when both regressors proxy for a
  common factor; the split of weight between them is set by their relative idiosyncratic variances.
- **Match on size decile and past-year return** before attributing a beta change to an event, and
  difference across the matched pair.
- **Adjust betas for non-synchronous trading** with Dimson leads and lags (here, two of each) when
  the event stocks trade at a different frequency from the comparison portfolios.
- **Price-band comparison portfolios**: `[3p/4, 5p/4]` and `[1p/4, 3p/4]` around a reference price
  `p`, as above.

## Robustness evidence (qualitative only)

- The replication **extends** the original index sample from 1976–2000 to 1976–2012 and reports
  subperiods separately; the index-addition beta difference is significant in only one of three
  subperiods, which is itself a robustness failure of the original independent of the matched-control
  argument.
- Results are reproduced on weekly as well as daily data.
- The momentum-beta table is estimated on 36 annual sorts and is a general cross-sectional fact,
  not an event study, so it does not inherit the event samples' selection.
- The authors are candid that the split sample's momentum match is **imperfect** — even the median
  matched return falls short of the original sample's, with larger gaps in the extremes — and argue
  the direction of that imperfection works against their own conclusion.
- **Tension to state, not to resolve**: this folder holds two notes resting on the design
  Chen–Singal–Whitelaw criticise —
  `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` (Nikkei weight variation)
  and `2026-11-07-index-addition-comovement-across-forty-national-indices.md` (forty markets). Both
  are cited by name inside the replication's own list of the excess-comovement literature. Neither is
  refuted by it: the Nikkei paper's identification is a continuous **weighting rule** rather than a
  before/after event window, and the forty-market paper's cross-country design is not a US event
  study. But **both report bivariate-style loading changes, and the criticism of that statistic is
  general.** Read their magnitudes as upper bounds, and treat any comovement result on this panel
  that lacks a momentum-matched control as unestablished.

## Implementability here

**Three things, none of them a candidate file.**

1. **A free refusal test, and it is cheap.** Any hypothesis of the form "names that join / leave /
   resemble group *G* comove more with *G*" must carry a **momentum-matched control** before it is
   written, because on this panel the obvious group-change events — a name becoming `eligible`
   (`#410`, `#411`), a name entering a price or liquidity band — are all selected on past
   performance in exactly the way the replication describes. Without that control the measurement
   returns the beta drift of a winner. The lab already owns the matching ingredients: `eligible`
   gives the cohort, `prices` gives the 252-day return, and a size proxy is the one missing piece
   (`#408`), for which the dollar-volume decile is the available substitute with `#405`'s resolution
   caveat attached.
2. **A reading rule about what a winner book owns, and it bears directly on the skill measure.** A
   long-only cross-sectional momentum book holds names whose market beta is **rising through the
   holding year** — roughly +0.18 from two years before formation to formation and a further +0.13
   into the first holding year in the table above, against a middle-decile beta that does not move.
   This lab scores **skill = book Sharpe − equal-weight pool Sharpe on the same days**, which is a
   difference of Sharpes and therefore does **not** net out a beta difference. A winner-selected book
   carries a structurally higher beta than the pool for about a year after formation, so in a period
   when the pool's own return is positive, part of a measured positive skill is that beta, and in a
   period when it is negative, part of a measured negative skill is too. **This is a candidate
   explanation for sign instability between the lab's two sheets that does not require either sheet
   to be wrong**, and it is testable for free: compute the book's realised beta to the equal-weight
   pool over train and over validation and report both alongside the skill. No trial is needed.
3. **The price-level leg specifically.** The one piece of return-side evidence that the nominal price
   level is a real categorisation variable — the split-comovement result — **does not survive a
   momentum-matched control.** Combined with the two companion notes, the honest position for this
   lab is: the price level is a *chosen* quantity, it is a *cost* variable, across this panel's nine
   markets it is mostly a *currency-and-convention* variable, and in the lab's own back-adjusted
   panel it is *contaminated by the future*; the one claim that it carries genuine non-fundamental
   return structure is the weakest of the four. **Do not write a candidate whose economic case is
   price-level categorisation.**

## Related

- `2026-11-09-the-nominal-share-price-puzzle-and-the-price-norm.md`,
  `2026-11-09-catering-through-nominal-share-prices.md` — the other two legs; the catering paper
  cites Green–Hwang as motivation and the replication removes that leg without touching the catering
  results.
- `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md`,
  `2026-11-07-index-addition-comovement-across-forty-national-indices.md`,
  `2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — the folder's existing
  excess-comovement cluster, all of which this note qualifies rather than refutes; see the tension
  paragraph above.
- `2026-09-08-nonsynchronous-trading-econometrics.md` — the Dimson adjustment used here, and the
  reason it matters more for some samples than others.
- `2026-08-17-jegadeesh-titman-overlapping-momentum.md` and the rest of the `price-trend` cluster —
  the beta term structure in point 2 is a property of every one of them.
