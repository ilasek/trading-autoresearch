---
title: "On Computing Mean Returns and the Small Firm Premium — with: Biases in Computed Returns: An Application to the Size Effect"
authors: Roll (primary, read in full); Blume, Stambaugh (companion, abstract only)
year: 1983; 1983
venue: Journal of Financial Economics 12(3), 371–386 (Tier 1); Journal of Financial Economics 12(3), 387–404 (Tier 1) — the two papers appeared back-to-back in the same issue and cross-cite each other as "this issue"
url: https://doi.org/10.1016/0304-405X(83)90055-7 ; https://doi.org/10.1016/0304-405X(83)90056-9
citations: "Roll 1983: 225 (Crossref `is-referenced-by-count`, checked 2026-10-03); 314 (OpenAlex, checked 2026-10-03). Blume–Stambaugh 1983: 582 (Crossref, checked 2026-10-03); 830 (Semantic Scholar DOI endpoint, checked 2026-10-03); 819 (OpenAlex, checked 2026-10-03). The three indexes agree on ordering and on magnitude class; Crossref is consistently the lowest, as this folder has recorded before."
sample_period: "Roll: 1963–1981, CRSP daily. Blume–Stambaugh: CRSP daily; the exact window was NOT read (abstract only) and is not claimed here."
markets: US equities (NYSE and AMEX), individual securities and size-sorted portfolios
tier: "A. Both are Tier-1, multi-decade-cited, and — decisively for this folder — they are results about an **estimator**, not about a premium. An estimator's bias does not decay with publication, so McLean–Pontiff does not apply and the 1983 vintage is not a discount. Roll was read in full and everything attributed to it below is from the text. Blume–Stambaugh is **abstract-only** (see Access); its algebra is NOT recorded and nothing below should be implemented as if it were."
validation_overlap: false
published_post_2018: false
---

## Access

**Roll (1983) was read in full.** `oa_status: closed` on every index, but OpenAlex's `locations`
list named a Caltech landing page, and **`authors.library.caltech.edu` served the typeset publisher
PDF on the first try**: read the `records/<id>/files/<file>.pdf` link out of the landing page at
`authors.library.caltech.edu/95130/` (the file is the Elsevier `1-s2.0-...-main.pdf`). This is a
**new working channel** and a clean instance of the 2026-09-18 faculty-page lesson one step out —
an author's *institutional library*, found via OpenAlex's location list rather than by guessing.
Worth trying for any closed article by a Caltech-affiliated author.

**Blume–Stambaugh (1983) was NOT read.** Its abstract below is authoritative, taken from the
authors' own working-paper series: **`rodneywhitecenter.wharton.upenn.edu/working-papers-abstract/working-paper-abstracts-1983/`**
serves the abstract of Rodney L. White Center working paper **11-83**, which is this paper. That host
is a **second new working channel** — it carries abstract pages per year from 1970 to 2014, and it is
the obvious first stop for any Wharton finance paper of that era. The paper itself is
`oa_status: closed` with no repository fulltext on any index, and it is not hosted on Stambaugh's
Wharton page. This **partially closes gap (b) named in the [2026-10-02] open questions** — the
mechanism and the headline bias ordering are now recorded from an authoritative abstract plus Roll's
full text, which restates Blume–Stambaugh's result directly; the algebra remains uncovered.

Verbatim abstract (Blume–Stambaugh, RLW WP 11-83):

> Previous estimates of a "size effect" based on daily returns data are biased. Several properties of
> quoted closing prices impart an upward bias to computed returns on individual stocks. Returns
> computed for buy-and-hold portfolios largely avoid the bias induced by closing prices. Based on such
> buy-and-hold returns, the full-year size effect is half as large as previously reported, and all of
> the full-year effect is, on average, due to the month of January.

## Mechanism

**The claim is that how you average returns is itself a return.** Three different ways of computing
the mean return of an equally-weighted set of `N` securities over a review period of `τ` sub-periods
give three systematically different numbers from *identical* data. Roll names them:

- **Arithmetic (`AR`)** — average returns across firms *and* days to get the portfolio's mean
  single-period return, then raise it to the `τ`-th power. Easiest to compute; corresponds to no
  actual portfolio.
- **Buy-and-hold (`BH`)** — link each security's own returns across the `τ` periods first, *then*
  average across securities. This is what an investor who buys equal dollar amounts and does nothing
  actually experiences.
- **Rebalanced (`RB`)** — the return on a portfolio that starts equally weighted and is restored to
  equal weights at the end of every sub-period.

Under temporal independence (Roll §2.2), Jensen's inequality orders them:

- `E(R_AR) ≥ E(R_RB)`, strict whenever the portfolio's unexpected return has non-zero variance;
- `E(R_BH) > E(R_RB)`, strict whenever `N > 1` and at least two securities have different expected
  returns — and the gap **grows with the cross-sectional variance of expected returns**;
- `AR` versus `BH` is **ambiguous**: `BH` rises with cross-sectional dispersion of expected returns,
  `AR` rises with the intertemporal variance of the portfolio's unexpected return. Under
  cross-sectional normality Roll reduces `AR` to `E(R_AR) = μ̄^τ·[1 + k·var(ε̄)]` with `k > 0`, making
  the tradeoff explicit.

With serial dependence (Roll §2.3), the doubling algebra gives the result that matters:

- `E(R_AR − R_RB) = ½(σ²_ε̄ − σ_ε̄1,ε̄2) > 0` **in all circumstances** — the arithmetic mean exceeds
  the rebalanced mean regardless of dependence;
- `E(R_BH − R_RB)` = the cross-sectional variance of expected returns **plus** a term in the
  *individual* securities' own serial covariance. So **negative serial dependence in individual
  unexpected returns, or positive serial dependence in the portfolio's returns, pushes `RB` up**, and
  enough of it makes the rebalanced mean exceed the buy-and-hold mean.

The economics of why that dependence is present, and present *asymmetrically*:

- **Bid-ask bounce** (Niederhoffer–Osborne 1966, cited): when a market maker is on one side of most
  trades, successive transactions alternate between bid and ask, inducing negative first-order serial
  dependence in an individual security's measured returns.
- **Non-synchronous trading** (Scholes–Williams 1977, cited): individual assets show first-order
  *negative* serial dependence while diversified portfolios show *positive* dependence.
- The signs matter because the estimators load on different objects: **`BH` means are driven mainly by
  individual-asset serial dependence, while `AR` and `RB` means are driven by portfolio serial
  dependence.** Hence lengthening the review period makes `BH` fall and `AR`/`RB` rise.
- Blume–Stambaugh add the *level* channel: properties of **quoted closing prices** impart an upward
  bias to computed individual-stock returns, which buy-and-hold largely escapes.

**Roll's own generalisation is the sentence this lab should read twice.** From his conclusion:
*"if serial dependence differs systematically with the item being investigated, the computational
method can be quite material."* And from his abstract: *"Similar biases can be expected in mean
returns when securities are classified by any variable related to trading volume."* He names size,
dividend yield, price/earnings and beta as exposed. The bias is not a constant you can ignore as a
level shift — **it is a function of the sorting variable**, so any cross-sectional sort on something
correlated with trading frequency inherits a differential bias between its buckets.

## Construction recipe

Not a strategy. The recipe is an **estimator choice**, and it is a short list:

1. **Decide which of `AR`, `BH`, `RB` your number is**, and say so. These are three different
   quantities and the literature's convention is that *investment experience is portrayed by
   buy-and-hold*; `AR` and `RB` are used because they are easier to compute.
2. **To measure a premium, link each instrument's own returns over the holding interval first, then
   average across instruments** (`BH`). To measure what a rebalanced book earns, compute `RB` — but
   do not then report it as the premium.
3. **The marginal effect of the review period diminishes with its length.** Roll: the effect on the
   measured mean "should be greater when changing from, say, a daily to a weekly review period than
   from a monthly to an annual period." The damage is concentrated at the short end.
4. **Diagnose rather than assume**: the gap between `AR`/`RB` and `BH` is driven by (i) the
   cross-sectional variance of expected returns and (ii) the first-order serial covariance of
   individual and portfolio returns. Both are directly measurable without new data.

## Robustness evidence (qualitative only)

- **Two independent papers, same issue, same conclusion, different methods** — Roll via the
  arithmetic of the three estimators plus CRSP daily data, Blume–Stambaugh via the properties of
  quoted closing prices. Both report that the measured size premium is **about half as large** under
  buy-and-hold as under the rebalanced/arithmetic methods, and Roll reports it becomes only
  marginally significant at conventional levels under buy-and-hold. (Recorded as a statement about
  the **estimator's bias magnitude**, which is these papers' contribution; the dated premium levels
  in both papers are deliberately not recorded here.)
- The result is **analytic, not empirical** at its core — the Jensen's-inequality orderings hold by
  construction for any return series, so there is no sample to decay and no replication question in
  the usual sense. The empirical content is only *how large* the gap is in a given panel.
- Blume–Stambaugh additionally report the measured effect concentrating in a single calendar month,
  which this folder notes as a **seasonality interaction** and nothing more; see
  `2026-08-29-same-calendar-month-seasonality.md` for the family that would own that question.
- Independently confirmed and quantified in a later Tier-1 paper covered tonight — see
  `2026-10-03-caveat-compounder-daily-rebalancing-bias.md`, which measures the `AR`-vs-`BH` gap
  directly and shows it does **not** shrink with the number of instruments.

## Implementability here

This is **not a candidate strategy. It is a possible defect in how any result here is computed**, and
it belongs to the same cluster as [2026-10-01]'s survivorship theorem and [2026-10-02]'s pool-weighting
and estimator channels.

- **It is a fourth mechanism with the lab's familiar artifact signature.** The lab's `learnings.md`
  attributes this universe's volatility-*level* effect to survivorship; [2026-10-02] added the pool's
  weighting and multiplicative price noise. Roll adds a fourth: **the averaging method itself**,
  upward-biased for `AR`/`RB` relative to `BH`, with the gap growing in the variance of the portfolio's
  unexpected return — i.e. **worst for the noisiest books**, exactly the other three signatures. The
  [2026-10-02] rule ("a confirmed mechanism with no rival mechanism considered is an unidentified one")
  applies to itself: the discriminator here is also an invariance, and it is named below.
- **The separating property is the review period, and it is free.** Survivorship, pool weighting and
  price noise are all invariant to how you *average* a fixed set of returns. The Roll bias is not: it
  must shrink as the review period lengthens, and shrink *fastest* at the short end. So recomputing an
  already-recorded statistic at two review periods (daily-linked versus monthly-linked) separates this
  channel from the other three without touching new data or the holdout.
- **The direct hazard is the engine, not the candidates.** The lab's strategies rebalance monthly,
  which Roll's diminishing-marginal-effect result says is the safe end. But weights are forward-filled
  to a **daily** grid with a 1-day execution lag, so whether the reported Sharpe is an `RB`-at-daily
  number or a `BH` number depends on arithmetic this agent is **not permitted to read** (`engine/` is
  out of scope for the research agent, and this note does not claim to know). **That is a question for
  the strategy agent or the human, and it is cheap to answer by inspection.** It is worth answering
  because it is upstream of every number on the leaderboard.
- **The `liquidity-volume` family is the most exposed, by Roll's own words.** Roll says the bias
  should be expected "when securities are classified by any variable related to trading volume". That
  is a literal description of `ILLIQ` and dollar-volume sorts. Any measured edge on a volume-related
  sort has a component that is pure estimator choice, differing between buckets because serial
  dependence differs between them — the illiquid bucket has more bid-ask bounce, so more negative
  individual serial dependence, so a larger `AR`/`RB`-over-`BH` gap. **The sign is predictable: an
  illiquidity-sorted long-only book should look better under rebalanced arithmetic than under
  buy-and-hold, and by more than a liquid-sorted book does.** That is a falsifiable ordering across
  books the lab has already built.
- **Low-volatility and range-variance books are exposed the same way**, since Roll names beta as a
  classifying variable with the same problem, and the `AR`-over-`RB` gap is explicitly `½σ²_ε̄`.
- **Costs do not rescue it.** This bias is in the *measurement*, not in the trading, so the lab's
  15 bps/side does nothing to it. Conversely, note Roll's caveat (echoed in the companion note) that
  the comparison is not advice to rebalance monthly in reality — it is about the arithmetic's
  approximation of a holding experience.
- **Pitfall:** do not read this as "use buy-and-hold everywhere". A monthly-rebalanced equal-weight
  book genuinely *is* an `RB` object, and its `RB` return is its honest return. The error is
  computing a number one way and interpreting it as the other.

## Related

- `2026-10-03-caveat-compounder-daily-rebalancing-bias.md` — the direct measurement of this gap, and
  the size-invariance result that makes it relevant to a 140-instrument universe.
- `2026-10-03-international-panel-screens-datastream.md` — the third of tonight's cluster: the panel
  defects that feed the noise term this bias is increasing in.
- `2026-10-02-noisy-prices-and-biased-premium-estimates.md` — Asparouhova–Bessembinder–Kalcheva; the
  closest sibling, and the note that named Blume–Stambaugh as gap (b). ABK's correction is a
  *weighting* change within a regression; Roll's is an *averaging* change. Both are numerator-only
  biases that shrink when noisy names get less voice.
- `2026-10-01-survival-conditioning-induced-drift.md` — the first of the four same-signature channels.
- `2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — Hou–Xue–Zhang; the pool-weighting
  channel, and the note whose "96% of trading-frictions anomalies fail once the pool is controlled"
  finding is about the same family Roll's volume warning targets.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md` — the family most exposed here.
