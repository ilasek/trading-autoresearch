---
title: "Excess Comovement of Stock Returns: Evidence from Cross-Sectional Variation in Nikkei 225 Weights (read as the HBS working paper, 'A Cross Sectional Analysis of the Excess Comovement of Stock Returns')"
authors: Greenwood
year: 2008 (published); working-paper version read, first draft September 2004, revised March 2005
venue: Review of Financial Studies 21(3), 1153–1186 (venue tier 1); working paper = Harvard Business School Working Paper 05-069
url: https://doi.org/10.1093/rfs/hhm052
citations: 198 (Crossref `is-referenced-by-count`, checked 2026-11-07)
sample_period: 1993–2003 (September 1993 – August 2003)
markets: Japan — Nikkei 225 constituents plus 1,458 non-constituent Tokyo Stock Exchange Section 1 stocks
tier: A — tier-1 venue, three-figure citations, full text read, and the design's identification comes from an institutional weighting rule rather than from an event window
validation_overlap: false (sample ends 2003)
published_post_2018: false
read: full text, HBS working-paper version (425 KB PDF, 46 pages → 119 KB of clean text, 968 instances of `" the "`, zero `( )` dropout, title line verified as the matching working paper)
---

## Access

Read from **`hbs.edu/ris/Publication%20Files/<wp-number>.pdf`** — Harvard Business School's own
flat publication-files directory — which served the complete working paper on the first try. This
is a **new channel for this folder** and it is the `/wp-content/uploads/`-shaped pattern
`research/README.md` keeps rediscovering (2026-10-13 `robjhyndman.com/papers/`, 2026-10-15
`burns-stat.com`, 2026-11-06 `web2-bschool.nus.edu.sg`), now on a US business school. Unlike those,
the filename is **derivable**: it is the working-paper number (`05-069`) and nothing else, so a
search result naming the WP number is enough to construct the URL.

Three channels failed around it, all worth recording. **`people.hbs.edu/<user>/` does not resolve
at all** (`HTTP 000`, connection never established) — a transport failure, not an origin refusal —
so the 2026-09-18 faculty-page lesson does *not* extend to HBS personal pages. **The HBS faculty
profile page returns HTTP 403** with a 30 KB body. And **`dash.harvard.edu` (Harvard's DSpace)
answered a search URL with HTTP 202 and `size_download=0`** — the same zero-byte-2xx mode
`research/README.md` records for `escholarship.org` (2026-10-16) and `sci2s.ugr.es` (2026-10-13),
now on a third host. OpenAlex's green location for this DOI is **SSRN**, which is a known refusal,
and its fourth location is a **CiteSeerX summary page** that also failed to connect.

**What was read is the working paper, not the version of record.** The claims below are the
working paper's. The abstracts of the two versions agree on every hypothesis and on the direction
and rough size of every result, but section and table numbering will not match the RFS article, and
one robustness table is **not in the working paper at all** — the text says it "is available from
the author on request". So the robustness claims in this note are the paper's *descriptions* of
tests whose table was not seen.

## Mechanism

The paper's subject is not a signal. It is **what an index's own weighting rule does to the
measured covariance matrix of its members** — and it is the cleanest available statement of that,
because the Nikkei 225's rule makes index weight nearly unrelated to anything economic.

The Nikkei 225 is **price-weighted**. Its level is the sum of constituents' face-value-adjusted
prices divided by a divisor:

> `index = Σ_i (P_i / (FV_i / 50)) / D_t`

so a constituent's index weight is its face-value-adjusted price divided by the sum of all 225
such prices. Most constituents have face value 50; a handful have 500, 5,000 or 50,000. The
divisor is adjusted for splits, capital changes and repurchases **to preserve continuity of the
index level, explicitly not of the weights** — after a two-for-one split a constituent's effective
weight halves and the divisor absorbs the level change.

The consequence is that **index weight is a price level, not a size**. Measured against the weight
the same stock takes in the value-weighted TOPIX, the average Nikkei constituent is overweighted by
a factor of roughly 5.7, and individual names by a factor of ten or more. Smaller names tend to be
the overweighted ones, so the rule tilts index demand *away* from capitalisation.

The economic mechanism on top of that rule is the **category/habitat demand channel**: a pool of
capital tracks the index, so when it is added to or withdrawn from, it buys or sells every
constituent *in proportion to index weight*. Under limits to arbitrage those correlated,
uninformed, weight-proportional demand shocks move prices, so a constituent's return acquires a
component proportional to its own index weight times a common demand shock. Three predictions
follow, and they are the paper's: a constituent's comovement with the rest of the index should rise
with its overweighting; its comovement with **non**-index stocks should *fall* with its
overweighting (index capital is funded by selling outside the index); and both should move at
addition and deletion in proportion to overweighting at the event.

The competing account is **information diffusion** — index membership proxies for the speed at
which a stock absorbs economy-wide news. The design discriminates between the two, and the result
goes against the information account: the effect scales with *how much* weight the rule assigns,
which the diffusion story has no reason to predict.

## Construction recipe

The measurement, which is the reusable part:

1. **Overweighting.** `OW_it = log(1 + w_index,it / w_valueweight,it)`, where `w_index` is the
   price-weighted index weight and `w_valueweight` is the stock's weight in a capitalisation-weighted
   index of the same market. Non-members take `OW = 0` by construction (`log(1+0)`). The paper
   notes the measure is a positive monotone transform of the within-index value-weighted alternative,
   so the two are **identical in the cross-section** and differ only in the time series.
2. **Comovement.** For each stock and each date, a univariate regression of the stock's return on
   the **equal-weighted** return of the long-term constituents, over a trailing 100 days (or 50
   weeks). Keep both the slope and the `R²`. The index surrogate is *equal*-weighted on purpose —
   the model is about covariance with an equally-weighted index return, and value-weighting it
   would reintroduce the weights being tested.
3. **Conditional comovement.** A bivariate regression adding the value-weighted broad-market
   (TOPIX) return, so the two slopes separate comovement with index members from comovement with
   everything else.
4. **Cross-sectional stage.** Regress each period's comovement measure on **lagged** overweighting,
   measured 100 days earlier — the lag is what stops the relation being manufactured by the price
   moves that set the weights inside the estimation window. Average the coefficients Fama–MacBeth
   style across non-overlapping cross-sections. Control for log size and price-to-book.

Magnitudes, as mechanism sizes rather than performance: a one-standard-deviation rise in
overweighting goes with an index beta higher by about 0.22, and overweighting alone accounts for
something above a fifth of the cross-sectional variation in index beta. The `R²` version of the
dependent variable moves with the slope version, which the paper reads as the relation running
through **correlation** rather than through the overweighted stocks simply being more volatile.

## Robustness evidence (qualitative only)

- **Sign stability.** The cross-sectional coefficient is positive in *every* one of the
  non-overlapping cross-sections, not merely on average.
- **Window length.** Widening the comovement estimation window from 100 to 250 days cuts the number
  of cross-sections and widens the standard errors; the paper reports the result surviving.
- **Standard errors.** The headline `t`-statistics are Fama–MacBeth, which assume no
  autocorrelation in the coefficient series. Allowing autocorrelation Newey–West style drops the
  key `t` from about 10 to about 7 at two lags and about 6.5 at four. Honest, and it is the right
  direction of honesty: the finding survives, visibly smaller.
- **Alternative overweighting measures.** Index weight scaled by average daily yen trading volume
  (a crude price-impact proxy) reproduces the result. **Unscaled** index weight does not fully: the
  conditional-comovement relation holds but the headline one loses significance — and the paper says
  plainly why, which is that unscaled weight mislabels large liquid names as overweighted. So the
  effect is about weight *relative to the stock's capacity to absorb demand*, not about weight.
- **Known limitation the author states.** The addition/deletion tests have few usable events and
  confound overweighting with the time-varying variance of index demand, which is the stated reason
  the cross-sectional design is the main one.
- **Generalisation, as a conjecture.** The paper expects the effect wherever periodic demand varies
  across names, and reads the drift of index families toward **float-adjusted** weighting as
  consistent with arbitrary weighting being recognised as costly. That conjecture is tested
  elsewhere and is the subject of this session's other two notes
  (`2026-11-07-free-float-redefinition-as-a-benchmark-change.md`,
  `2026-11-07-index-addition-comovement-across-forty-national-indices.md`).

Not recorded, deliberately: the paper reports that a trade betting on reversion in overweighted
names was profitable in its sample. That is a performance claim and `research/README.md`'s
anti-lookahead rule 1 excludes it; it is mentioned only so a later session does not think the note
missed it.

## Implementability here

**The headline construction is not reproducible on this panel, and the reason is specific enough to
save a night.** Three independent blocks, in descending order of how fatal they are:

1. **The overweighting measure needs an unadjusted price and a share count, and this panel has
   neither.** The Nikkei weight is the *raw* face-value-adjusted price, and the divisor is
   deliberately *not* used to hold weights constant through splits. This repo's panel is
   **USD-adjusted daily closes** — adjusted for exactly the corporate actions the divisor absorbs —
   so a split-adjusted series does not track the index weight it is supposed to proxy. The
   denominator is worse: `w_valueweight` needs market capitalisation, i.e. shares outstanding,
   which is a fundamental and is not in the contract (`prices`, plus `aux`'s open / high / low /
   volume / dollar_volume). There is no path from the visible panel to `OW`.
2. **The face-value adjustment is unobservable.** Even the numerator's cross-sectional *ranking*
   would need to know which names carry face value 500, 5,000 or 50,000 rather than 50 — a
   per-instrument constant found in the index rulebook, not in price data.
3. **Identifying which names the rule even applies to would mean identifying the Japanese book**,
   and under protocol v2 a candidate may not name a stock or read the membership files, so there is
   no sanctioned label for listing market. `experiments/learnings.md` is explicit that `region` was
   the finest venue label `data/universe.yaml` carried, and that file is now off-limits to a
   candidate.

What survives, and it is worth more than the blocked recipe:

- **A warning about the panel's own covariance structure.** This repo's panel is the union of
  members of nine indices, and one of the nine — the Nikkei 225 — weights its members by price.
  Greenwood's result says that index's constituents carry a comovement component induced by the
  *rule*, concentrated in its overweighted names. Any candidate that estimates a covariance matrix,
  runs PCA, counts factors or clusters this panel is estimating a matrix with a slab of
  rule-induced, non-fundamental correlation in it. That bears directly on `statistical-arbitrage`
  (`2026-08-30-pca-residual-statistical-arbitrage-long-only.md`) and on `portfolio-learning`
  (`2026-09-07-hierarchical-risk-parity-clustering-allocation.md`): a residual defined against
  principal components of *this* panel is residual to index-demand commonality as well as to
  fundamentals, and a cluster found in it may be an index rather than an industry.
- **The one testable fragment that is reachable.** The *direction* of the mechanism is a statement
  about dispersion, not about weights: index-demand commonality should make members' pairwise
  correlation higher than fundamentals warrant, and should make it **move with index-tracking
  flow**. `2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md` and
  `2026-10-06-betaless-variance-decomposition-and-average-correlation.md` already give this folder
  model-free average-correlation estimators computable from closes alone. Rising average
  correlation inside a membership cohort is observable; attributing it to the weighting rule is not.
- **A caution about the random-portfolio gate.** Protocol v2's hard gate draws 200 random
  portfolios from the same point-in-time pool with the same holdings schedule. If rule-induced
  comovement raises correlation among the pool's members, it raises it for the random portfolios
  too, so the gate already nets out the part of a candidate's performance that is this effect. A
  candidate whose edge *is* index-demand commonality should expect the random-portfolio null to be
  unusually hard to clear — which is the gate working, not a nuisance.

**Pitfall worth stating once.** It is tempting to read "overweighted names have high betas" as a
low-risk-investing signal with the sign flipped. It is not: `OW` is not observable here, and the
nearest observable proxy — nominal price level — is both split-adjusted away and, per
`2026-09-01-max-lottery-extreme-positive-returns.md` and the low-vol literature in this folder,
already entangled with effects the lab has measured. Do not substitute price level for `OW`.

## Related

- `2026-11-07-free-float-redefinition-as-a-benchmark-change.md` — the same object (an index
  weighting rule moving betas) at the moment a rule *changes*, across many non-US markets.
- `2026-11-07-index-addition-comovement-across-forty-national-indices.md` — whether this Nikkei
  finding generalises to the other national indices in this repo's panel. It largely does, and the
  moderator it identifies is index concentration.
- `2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — the US index-effect
  literature, which **explicitly leaves the non-US case open** and names the TOPIX and Nikkei 225 as
  the gap. This note is the first half of closing that.
- `2026-11-06-index-membership-is-not-an-information-free-selection.md` and
  `2026-11-06-investability-frictions-and-the-microcap-screen.md` — the admission rule as a
  selection; this note is the admission rule as a *weighting*.
- `2026-10-10-etf-arbitrage-shock-propagation.md` — already builds on Greenwood's (2005)
  risk-averse market-maker model; the demand channel here is the same family of argument.
- `2026-08-30-pca-residual-statistical-arbitrage-long-only.md`,
  `2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — the two constructions most
  exposed to rule-induced correlation in this panel.
