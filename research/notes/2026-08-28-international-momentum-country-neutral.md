---
title: "International Momentum Strategies"
authors: Rouwenhorst
year: 1998
venue: The Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/0022-1082.95722
citations: 1357 (Crossref `is-referenced-by-count`, checked 2026-08-28); Semantic Scholar's DOI endpoint returns "not found" for this DOI, though it resolved the two other Journal of Finance DOIs looked up the same session — its JF misses skew to older vintages
sample_period: 1978–1995 (returns tested 1980–1995)
markets: 2,190 stocks from 12 European countries (Austria, Belgium, Denmark, France, Germany, Italy, Netherlands, Norway, Spain, Sweden, Switzerland, UK), 60–90% of each country's market cap
tier: A
validation_overlap: false
published_post_2018: false
read: full text, Yale ICF working-paper depot (`depot.som.yale.edu/icf/papers/fileuploads/2528/original/97-95.pdf`), the February 1997 revision of the article published in JF 1998
---

## Mechanism

The paper's purpose is not to propose a mechanism but to test whether the US momentum result is
a data-snooping artifact. Its logic is the one this repo should care about: return continuation
found in **substantially the same database of US stocks** by many researchers cannot rule out
that the anomaly is an outcome of an elaborate collective search; an independent international
sample can. The finding is that medium-term continuation is present in every one of twelve
European markets, survives risk adjustment, and — this is the part that limits the independence
claim — is **materially correlated with US momentum**, so the international sample is not a
clean second draw.

On the economics, the author's reading is that the result points either to a serious
misspecification of standard asset-pricing models or to a general tendency of markets to
underreact to information. He does not choose. Two structural facts he does establish and that
carry mechanism content:

- Winners and losers are both drawn disproportionately from the **tails of the volatility
  distribution** — the decile portfolios' standard deviations are U-shaped in past return, with
  the extreme deciles running roughly a third higher than the middle. Stocks with higher
  volatility are mechanically more likely to show extreme past performance, so a momentum sort
  is partly a volatility sort. This is the same asymmetry session 14 priced on the cost side,
  arrived at from the return side.
- Losers are on average **smaller** than winners, and both are smaller than the average firm.
  So an unconstrained momentum sort takes a size bet even when nobody asked for one, and the
  loser leg behaves like small stocks irrespective of its own size.

## Construction recipe

Jegadeesh–Titman mechanics applied to a pooled international cross-section:

- **Signal**: cumulative past `J`-month return, `J ∈ {3, 6, 9, 12}`. Stocks need at least 12
  months of history. Ranked into deciles at each month end; top decile = winners.
- **Holding**: `K ∈ {3, 6, 9, 12}` months, no rebalancing within a tranche. The reported return
  is the average across `K` overlapping vintages started one month apart — equivalently, a
  composite book that recommits `1/K` of capital each month. This is the same overlapping-tranche
  structure the champion uses, and the same one Jegadeesh–Titman use, i.e. a third independent
  appearance of it as the field's default rather than a choice.
- **Weighting**: equal weight at formation.
- **Skip**: the base results form portfolios at the end of the ranking period. Delaying formation
  by one month **raises** the winner-minus-loser spread at the shorter ranking and holding
  intervals, and the gain comes almost entirely from the **loser** leg's return falling — i.e.
  from removing short-horizon reversal / bid-ask bounce on the leg this repo does not hold.
- **Currency**: all returns are converted to a **single common currency** (Deutschmarks) using
  spot exchange rates, and momentum is computed on those converted returns. Nothing is hedged.
- **Country-neutral variant**: rank stocks into deciles **against other stocks from the same
  local market only**, then take the top decile from each country. The resulting book holds the
  same country allocation as an equal-weighted index of the twelve markets.
- **Size-neutral variant**: sort on market cap first, then on past return **within each size
  decile**; take the extreme past-return group from each size decile.
- **Size-and-country-neutral variant**: within each country, split into three coarse size groups
  (bottom 30 / middle 40 / top 30), then rank on past six-month return inside each of the 36
  country-size cells.

## Robustness evidence (qualitative only)

- **Pervasiveness.** Winners beat losers in all twelve countries; the spread carries a
  t-statistic above 2 in eleven of them, including each of the three largest markets. It holds
  in every size decile and in every one of the three coarse size groups.
- **Country neutralisation is close to free on the mean and large on the variance.** Ranking
  within country rather than globally lowers the spread's mean only slightly, but the winner and
  loser legs' correlation rises sharply (roughly 0.74 → 0.88) and the **spread's volatility falls
  by about 40%**, so the t-statistic rises substantially. The interpretation the paper draws:
  return continuation is **not** country momentum in disguise — but a large share of an
  unconstrained international momentum book's variance *is* country-specific and is diversifiable
  by construction rather than by adding names.
- **Not a size effect.** Continuation is stronger for small firms — the small-cap spread runs
  roughly twice the large-cap spread — but is present and significant in every size group, and
  the middle-size-group spread is statistically indistinguishable from the size-country-neutral
  book's. Controlling for market beta or an international SMB factor *increases* the abnormal
  return, because losers load more on the size factor than winners do.
- **Duration and reversal.** In event time the spread is positive for about the first eleven
  months after formation and turns (insignificantly) negative in the second year; the cumulative
  payoff peaks near twelve months and is flat thereafter. This is the same bound on signal age
  the folder already carries from Jegadeesh–Titman, reproduced on an independent sample.
- **The independence claim is partly self-limiting.** The country-neutral European momentum
  return correlates ~0.43 with the US momentum return over the common sample, and regressing one
  on the other leaves an intercept that is still strongly significant but roughly a third smaller
  than the unconditional mean. So Europe is *partly* an independent confirmation and *partly* the
  same bet. The author explicitly declines to say whether the common component is a priced
  momentum factor, shared SMB/industry exposure, or both.
- **Cost honesty.** Costs are handled by a bound rather than a model: the sample is large,
  liquid stocks with round-trip costs typically under 1%, and the event-time payoff exceeds a
  two-percent round-trip charge only for holding periods of about four months or longer. That is
  an argument for *not* rebalancing a momentum book quickly, and it is made on a sample whose
  cost level is roughly comparable to this repo's assumed 15 bps/side.

## Implementability here

Directly relevant, and the most useful thing in it is a construction variant this repo has never
tried and which is **not** the one `learnings.md` refuted.

- **Country/region-neutral ranking is a different proposal from sector-neutral scoring.** The lab
  tested neutralising the composite z-score within coarse sector/asset-class groups and it lost
  Sharpe while raising turnover; candidate #5 generalised that into a screen — do not neutralise
  unless you can name the mechanism by which the signal would load on the group even if the
  effect were absent. **Country membership passes that screen where sector membership failed it.**
  The named mechanism is in the paper and is documented independently (Heston–Rouwenhorst,
  Griffin–Karolyi): international stock returns contain large country-specific components, so a
  globally pooled momentum sort mechanically overweights whichever *market* rose, in a way that a
  sector sort of already-sector-spanning names does not. That is a confound with a mechanism, not
  a diversification reflex, and the measured consequence is the one the screen would predict —
  the mean is barely touched and the variance falls a lot.
- **What the repo would actually build**: rank the momentum composite within coarse
  currency/region groups (the repo has no country field, but its instruments carry a listing
  currency and an obvious NA / Europe / Asia-Pacific split) rather than in one global pool, then
  take the top names per group. Note the direction of the expected gain carefully — it is a
  **variance** effect, so it should be predicted as a Sharpe gain with a flat or slightly lower
  numerator, and it will *not* show up as a higher mean return. Candidate #24's design test
  applies: name the sign before running it.
- **Two pitfalls specific to this universe.** (i) With ~145 instruments spanning stocks *and*
  ETFs, per-group counts get thin fast; a three-way regional split is near the limit and a
  country split is not available. (ii) The repo's ETF sleeve includes country and regional funds,
  so a regional neutralisation applied to the whole universe would be neutralising a group the
  ETF instruments *are*, not one they belong to — the grouping must be applied to the stock leg
  or the two legs must be grouped separately.
- **The currency treatment is confirmed, not merely assumed.** This repo converts non-USD
  instruments to USD and computes signals on the converted series, unhedged. That is exactly what
  this paper does (into DM), and the result holds — so the repo's convention is the literature's
  convention, and momentum measured on common-currency returns is not a known artifact. What the
  paper does *not* do is separate the FX component from the local-return component, so nothing
  here supports or refutes the sharper claim that the FX part of the signal carries information.
- **The size discount transfers and is unfavourable.** The spread in the largest size group runs
  roughly half the smallest group's. This repo's universe is global large caps plus ETFs — the
  weakest end of that gradient. Every momentum magnitude in this literature should be read as an
  upper bound for this book, and this is now the second independent source saying so.
- **The skip-month gain is loser-leg-driven**, which means a long-only book gets less of it than
  the headline suggests. The champion's 6-1/12-1 composite already skips; this source says the
  reason it helps is mostly about the leg the repo never holds, so the skip should be kept for
  the reversal-avoidance reason `learnings.md` already records, not credited with the full
  published improvement.

## Related

- `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md` — same overlapping-tranche
  mechanics, and the same two-year reversal bound on tranche depth, on the US sample.
- `notes/2026-08-17-momentum-horizon-echo.md` — Goyal–Wahal's non-US evidence, the other source
  in this folder that says "the applicable prior for this repo's global pool is the non-US one".
- `notes/2026-08-18-low-risk-investing-industry-neutral.md` — candidate #5's group-neutralisation
  screen. This note supplies the first grouping the folder has found that **passes** it.
- `notes/2026-08-28-local-versus-global-factor-construction.md` — Fama–French's independent and
  much later evidence that the ranking cross-section should be regional, plus the large-cap
  discount stated a second time.
- `notes/2026-08-27-momentum-net-of-costs-debate.md` — the cost side of the same question; this
  paper's holding-period bound is a crude version of the same argument.
