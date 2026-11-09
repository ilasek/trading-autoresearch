---
title: "The Nominal Share Price Puzzle (read as the lead author's Cornell dissertation of the same title)"
authors: Weld, Michaely, Thaler, Benartzi
year: 2009 (published). Read source: Weld, W. C., *The Nominal Share Price Puzzle*, PhD dissertation, Cornell University, May 2012
venue: Journal of Economic Perspectives 23(2), 121–142 (venue tier 1 — peer-reviewed AEA journal); read source is a doctoral dissertation (tier 2 as a document)
url: https://doi.org/10.1257/jep.23.2.121
citations: 117 (Crossref `is-referenced-by-count`, checked 2026-11-09)
sample_period: 1933–2007 for the core US series (NYSE/AMEX); an NYSE price series back to 1815 for the pre-Depression norm; 16 international exchanges over windows inside 1975–2005; ~197,755 firm-years of spread data over ~80 years
markets: US (NYSE/AMEX) primarily; 16 further exchanges including London, Tokyo, Toronto, Singapore, Korea, Taiwan, Italy, Brussels, Australia, Mexico, Jakarta, Kuala Lumpur, Manila, Bangkok, Johannesburg
tier: A — tier-1 venue, three-figure citations, multi-decade and multi-market, and the paper's own structure is "test four economic explanations and report that all four fail", which is methodology honesty of the kind the rubric asks for
validation_overlap: false (every series ends by 2007)
published_post_2018: false
read: full text of the Cornell dissertation (113 KB of clean text, title line verified, six numbered facts and four numbered hypotheses present). The published JEP article was **not** obtained — see Access.
---

## Access

**The JEP article is unobtained and the dissertation is what was read.** `aeaweb.org` and
`pubs.aeaweb.org` both answered their PDF endpoints for this DOI with **HTTP 403 and a ~5.5 KB
Cloudflare body** — worth recording because JEP is nominally a free-to-read journal, so "the venue
is open access" is not evidence an automated client can fetch it. The route that worked was
**`ecommons.cornell.edu/server/api/core/bitstreams/<uuid>/content`**, and it carries a lesson of its
own: `file` reported the response as **`Unicode text, UTF-8`, not a PDF**, and `pdftotext` failed on
it — because the DSpace bitstream *is* the extracted-text derivative rather than the PDF. The body
was the complete dissertation. **A DSpace bitstream that `file` says is not a PDF is not necessarily
a refusal page; read the first 400 bytes before discarding it.**

**What the dissertation is relative to the article.** Same title, same lead author, three of the
four JEP co-authors are its committee or co-authors on the underlying work, and the document's
structure is the article's structure expanded: the same six numbered facts and the same four
candidate explanations, with the tables the article compresses. Where this note states a number it
is the dissertation's number. The published article's own tables were not seen, and any revision
made between the 2009 article and the 2012 dissertation is unobserved.

## Mechanism

**A stock's nominal price per share is not an outcome; it is a choice, and the choice follows a
norm.** Nothing in frictionless pricing makes any per-share price optimal — a board can set any
price it likes by choosing a split ratio, without changing the firm's value. The paper's content is
that boards nevertheless manage the price, and that the target they manage toward is conventional
rather than economic.

Six facts, in the paper's order:

1. **US nominal share prices have been roughly constant for about seventy-five years.** The
   equal-weighted average price of NYSE/AMEX stocks sits near \$25 across the whole 1933–2007 span
   (value-weighted near \$37), while the price index and the price level of everything else in the
   economy rose by an order of magnitude. Holding nominal price constant through splits therefore
   means a **~90% decline in the real price per share**. The cross-sectional dispersion of prices
   shows no trend either.
2. **Larger firms have higher share prices**, consistently and by a wide margin — top-size-quintile
   NYSE/AMEX names cluster around \$50 a share and bottom-quintile names below \$10. This is not
   mechanical: every large firm could have chosen split ratios that put it at a low price.
3. **IPO prices are constant too**, which matters because a newly public firm has no legacy price to
   be inertial about and must choose one from scratch.
4. **Open-end mutual fund share prices** have been roughly constant since the 1960s — the same
   convention in a setting with no trading-cost or signalling story.
5. **The pattern is a US pattern, not a market pattern.** On sixteen other exchanges the level,
   the drift and the covariation of average price with the index all differ sharply. In current USD
   the average share price across those exchanges spans roughly **\$0.02 to \$37** — three orders of
   magnitude — and the correlation between the average nominal price and the local index level runs
   from strongly positive to negative depending on the exchange. Tokyo's and London's average
   nominal prices move substantially with their indices; the NYSE's does not.
6. **Maintaining a low price is costly.** In a Fama–MacBeth panel of ~198k firm-years of spread
   estimates spanning ~80 years, **higher-priced firms have significantly lower relative bid-ask
   spreads**, controlling for volume, turnover and market capitalisation (price coefficient
   t ≈ −13). The result survives a non-parametric specification for price.

**Four economic explanations are tested and all four fail.** *Marketability* (low prices broaden
ownership and improve liquidity) is contradicted by fact 6 and by the evidence that relative spreads
widen after splits. *Pay to play* (brokers push low-priced stocks because per-share commissions make
them lucrative) cannot explain the constancy through the collapse of per-share commissions.
*Signalling* cannot explain a price target that has been identical for seventy years across every
information environment. What is left is **customs and norms**: boards split toward the price their
peers trade at, the norm re-formed once after a large shock and has not moved since, and surveys of
managers return "historical company practice" as the most frequent stated reason.

**The norm is peer-relative, not absolute, and that is the operationally useful part.** A model
predicting the post-split target price from a firm's price **deviation from its size and industry
peers** explains **over 62% of the variance in post-split prices**, rising to **over 78%** when the
sample is restricted to genuine splits (ratio ≥ 1.25:1). Independent work cited in support finds
post-split prices converging to the industry norm and split factors increasing in the distance from
it.

## Construction recipe

There is no strategy here; there is a variable definition and its decomposition, which is what this
folder needs it for.

- **The quantity.** Nominal price per share, `P`, in the listing currency. Low- and high-priced
  groups in this literature are the bottom and top **30%** of NYSE common stocks by price; the
  analogous size groups are the bottom and top 30% by capitalisation.
- **Its decomposition.** Over any window, log nominal price accumulates as
  `p_t = p_IPO + Σ(log capital-gain returns) + Σ(log split effects)`. The second term is the market's
  contribution and the third is the board's. Facts 1 and 3 say the third term is chosen so that the
  sum stays near a convention.
- **The peer model.** Regress the post-split target price on the firm's pre-split price deviation
  from its size-decile and industry peers; that is the specification reaching 62–78% R².
- **Exclusions the literature applies by convention**: Berkshire Hathaway is dropped from every mean
  price computation, and stocks below \$5 are dropped from the spread panel.

## Robustness evidence (qualitative only)

- The core US fact is measured over seventy-five years with no trend in either the mean or the
  cross-sectional dispersion, and it is reproduced on a separate NYSE series reaching back to 1815,
  where the pre-Depression norm sits at a clearly different level (prices quoted as a percentage of
  a \$100 par value before 1915). So the norm is **stable but not immutable**: it re-set once, after
  a large shock, and the paper's reading of the euro changeover is that a change in the peer set can
  also move it.
- The multi-market evidence is the strongest part for a global panel: the US pattern does **not**
  replicate on sixteen other exchanges, which is a far more informative negative than a single-market
  robustness table.
- The size–price relation is reported independently by several other groups cited in the text.
- Weakness to state plainly: the surviving explanation — norms — is the one the author concedes
  **cannot be formally tested**, because no model of norm formation exists to test. The paper is
  strong on rejecting the alternatives and explicitly conjectural on what remains.

## Implementability here

**This note is not a candidate. It is about what the lab's own price panel is, and it changes how
one specific recent measurement should be read.**

1. **What this lab stores is not the nominal price.** `prices` is a USD-adjusted, back-adjusted
   series. Back-adjustment divides earlier prices by the cumulative factor for every split and
   dividend between then and the end of the series, so the stored level at date `t` is the nominal
   price at `t` **divided by a quantity that is a function of the name's future**. Under the
   decomposition above, the nominal price accumulates *past* returns and *past* board decisions; the
   stored adjusted level removes them and substitutes the negative of the *future* ones. Any score
   correlated with the stored level is therefore correlated with a quantity no investor could have
   observed at `t`. This is a statement about the data construction, not about any effect, and it is
   consistent with the sign and the horizon amplification the lab measured on `log P` on 2026-11-08
   — a longer forward window overlaps more of the adjustment that produced the level. **Filed as
   support for the standing engine issues of 2026-10-18 / 2026-10-22, not as a new one.**
2. **Across this panel's nine indices, the cross-sectional price level is mostly a listing
   convention.** Fact 5 puts three orders of magnitude between exchanges' average nominal prices,
   before any USD conversion, and the lab's panel spans Tokyo, Hong Kong, London (quoted in pence),
   Zurich, Amsterdam, Paris, Frankfurt and the US. A pooled cross-sectional rank on price level is
   therefore close to a **set of country dummies with a currency overlay**. The nightly's
   recommendation to partial out `log P` **within region** is the right form and this is the reason:
   across regions the variable has essentially no firm-level content.
3. **Within a region, the residual price level is largely a size-and-industry peer variable** (facts
   2 and the 62–78% peer model). So "control for the price level" is **not** a neutral nuisance
   removal — within region it removes a sizeable part of whatever size tilt a score carries. A score
   whose sign flips under that control has not been cleaned; it has been told that its content was a
   size-and-convention tilt. That is still worth knowing, but it should be reported as *what the
   control removed*, not as *the score was contaminated and is now clean*.
4. **Price level is a cost variable, and the lab's cost model does not see it.** Fact 6 says relative
   spreads fall in price **after** controlling for volume, turnover and size. Protocol v3 assigns
   liquidity tiers from trailing median USD volume only. So two names in the same v3 cost tier with
   different nominal prices do not have the same true cost, and the error is signed: the
   lower-priced name is undercharged. Any book that systematically tilts toward low nominal prices
   is flattered by the cost model by an amount this panel cannot measure. **No tiering change is
   proposed here** — the cost model is the engine's and this is for the human.
5. **Nothing here is tradeable as stated.** Nominal price is not recoverable from a back-adjusted
   series without a share count or an adjustment-factor series, neither of which the `prices` + `aux`
   contract supplies (same block as `#408`). The one thing the panel *can* compute — the stored
   adjusted level — is the contaminated quantity, not the economic one.

## Related

- `2026-11-09-catering-through-nominal-share-prices.md` — the same object with the board's decision
  modelled as a response to a time-varying valuation premium rather than to a norm; the two papers
  are in open disagreement about *why* and in agreement about *that*.
- `2026-11-09-price-based-comovement-and-its-failed-replication.md` — the question of whether the
  price level has any return-relevant content at all, and the replication that says the headline
  evidence for it does not survive a momentum-matched control.
- `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` — already warns against
  substituting nominal price for index overweight; facts 2 and 5 here are the reason that warning is
  right and strengthen it from "entangled" to "not the same variable at all across regions".
- `2026-10-03-international-panel-screens-datastream.md` — its low-nominal-price screen (rounding
  artefacts) is a different concern about the same variable, and fact 5 says the screen's threshold
  cannot be a single USD number on a multi-exchange panel.
- `2026-11-06-illiquidity-premium-and-where-the-size-screen-sits.md` — fact 6 is a second channel by
  which a price-level tilt becomes a cost tilt.
