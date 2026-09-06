---
title: "The role of shorting, firm size, and time on market anomalies"
authors: Israel, Moskowitz
year: 2013
venue: Journal of Financial Economics 108(2), 275–301 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2012.11.005 — the typeset JFE article read in full from a public mirror, https://gritcap.com/enoalroa/2020/10/Israel-and-Moskowitz-The-role-of-shorting-firm-size-and-time-on-market-anomalies-2012.pdf
citations: 163 (Crossref `is-referenced-by-count`, checked 2026-09-06); 200 (OpenAlex, same date); Semantic Scholar's DOI endpoint returns "not found" for this DOI — an **eighth** instance of this folder's standing "disbelieve a lone count" rule, and the second consecutive session in which the missing index is Semantic Scholar on a tier-1 finance DOI
sample_period: 1926–2011 (US equities; momentum from 1927), 1972–2011 (international equities and other asset classes)
markets: US equities (CRSP/Compustat via the Fama–French portfolio construction), four international equity markets, five non-equity asset classes
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full**: the published 27-page article — the long/short decomposition and its two
objectives, the factor-portfolio results, the size-conditioned 5x5 tables with the "percent long
side" statistic and its formal test, the subperiod and international robustness, and the trading
cost / institutional-ownership analysis.

Third note of the 2026-09-06 session, and the one that decides *which end of a ranking a
long-only book is entitled to care about*.

## Mechanism

The paper's organising distinction is between two objectives that the anomaly literature runs
together, and the lab sits squarely on one side of it:

- **If you care about raw returns**, shorting is close to irrelevant. Across size, value and
  momentum, the return premia are dominated by the contribution of the long positions — in the
  size-conditioned tables, the long side accounts for **more than 100%** of the raw
  long-minus-short spread in every size quintile for both value and momentum, meaning the short
  leg *subtracts* from raw return. This has a trivial cause and it is worth stating plainly:
  the short leg is still equities, so it carries a positive expected return that a short
  position gives away.
- **If you care about returns relative to a benchmark**, shorting matters a great deal. Measured
  in market-adjusted alphas, the long side accounts for essentially all of the size premium,
  roughly 60% of the value premium and about half of the momentum premium — the rest lives in
  the short leg, which a long-only investor can only approximate by underweighting relative to
  benchmark weight.

The economic reading is that market exposure is doing the heavy lifting in a long-only version
of any of these strategies: the long-only portfolios carry betas above one, so their raw returns
are largely a levered market position. What survives after removing the market is the honest
measure of what the sort adds — and long-only versions of value and momentum do produce
positive, significant market alphas, so the constraint does not extinguish the effect.

The second mechanism is the size interaction, and it points in opposite directions for the two
strategies. **The value premium declines monotonically with firm size and is insignificant among
the largest two quintiles**, both in the spread and in the long-only leg. **Momentum shows no
reliable relation with size** — it is present and stable across every size group. Shorting's
importance moves with size too: as firms get smaller, shorting becomes *less* important for
momentum and *more* important for value.

## Construction recipe

Nothing here is a strategy; it is a decomposition, and the decomposition is the tool.

1. **Build the sort** (quintiles or deciles, value-weighted, monthly rebalance, standard
   Fama–French breakpoints), and keep three return series: the top portfolio, the bottom
   portfolio, and the spread.
2. **Decompose in both objectives.** For raw excess returns, report the top portfolio's excess
   return over the risk-free rate alongside the spread. For benchmark-relative, regress each on
   the market and use CAPM alphas. The two decompositions can and do give different answers;
   reporting only one is the error the paper is correcting.
3. **The "percent long side" statistic** — the long leg's contribution divided by the spread's,
   computed separately for raw returns and for alphas — with a **formal test of whether it
   differs from 50%**, an equal split. Values above 100% mean the short leg is a drag on that
   objective.
4. **Condition on size** by running the whole decomposition inside each cell of a 5x5
   size-by-characteristic grid, so that "the premium is concentrated in stocks I cannot trade"
   and "the premium needs a short leg I cannot take" are separated rather than confounded.
5. **Test stability by splitting the sample into long (20-year) blocks** and asking whether the
   dispersion of block estimates exceeds what chance would produce, rather than narrating which
   block was strongest — the discipline this folder's anti-lookahead rules require anyway.

## Robustness evidence (qualitative only)

As strong as this folder has recorded. Eighty-six years of US equity data; four international
equity markets and five other asset classes over roughly four decades; the long/short split
comes out near even in market-adjusted terms in the other markets too. Subperiod variation in
all three premia is **consistent with random chance**, and the authors find little evidence that
changes in trading costs, institutional ownership, or hedge-fund participation are related to
the premia (the one exception being a decline in the size premium with rising institutional
ownership).

The paper is a corrective replication as much as a study: two well-known earlier conclusions —
that momentum is markedly stronger among small caps, and that about two-thirds of momentum
profits come from the short side — are shown to be **specific to the samples in which they were
first measured**, and do not hold in the longer panel or in the other markets. That is exactly
the sort of finding the rubric's "replication" column exists to reward, and it cuts against a
claim this folder would otherwise have carried forward.

Methodology honesty: costs are discussed rather than modelled (deliberately — the authors argue
a cost model is investor-specific), and the smallest size groupings are acknowledged to be
micro-caps that are hard to trade. Multiple testing is not an issue for a decomposition of
already-known effects.

## Implementability here

**This repo is a raw-return, long-only, unlevered, mega-cap book with no benchmark.** Reading the
paper against those four constraints:

1. **The applicable regime is the raw-return one, and it is the favourable one.** The lab's gate
   scores a book's own Sharpe, not an alpha against a market portfolio. In that objective the
   short leg is not merely unavailable, it is not wanted: it subtracts from raw return in every
   size quintile the paper measures. The long-only constraint this folder has repeatedly
   described as a cost (`notes/2026-08-22-long-only-as-l1-regularization.md`,
   `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`'s transfer coefficient) is
   much less binding under a raw-return objective than under a benchmark-relative one, and the
   folder has not previously drawn that distinction.
2. **But the raw-return result is mostly beta, and the lab should not mistake it for signal.**
   The long-only legs carry betas above one, which is why their raw returns look strong. On this
   universe the equivalent statement is that any long-only book is first a global-equity
   position and only second a score. The lab's gate compares candidates against an incumbent
   built the same way, which nets most of that out — but the number that transfers from this
   paper is the *market-adjusted* share, not the raw one.
3. **The exact analogue of "percent long side" for an equal-weight long-only book is computable
   for free on train, and it is a different statistic than the lab currently computes.** For a
   book holding `k` of `n` names equally, active weights against the equal-weight universe are
   `+(1/k − 1/n)` on a held name and `−1/n` on an excluded one, so

       active return = mean(held) − mean(all)

   and the *shortfall of the bottom band below the universe mean* enters the book's return with
   exactly the same standing as the *excess of the top band above it*. The free measurement is
   therefore the demeaned profile across bins: **does the bottom band underperform the universe
   mean by more than the top band outperforms it?** The lab currently reports top-`k` excess
   only, so for every score it holds, half of this statistic has never been looked at.
4. **If the answer is "the bottom carries it", the construction that follows is one this lab has
   never built.** Every one of its ~30 books is a *selection* — hold the top band. The
   alternative is an **exclusion book**: hold the whole scoreable universe equally except the
   worst quantile. That is not shorting and does not need leverage; it is the long-only way to
   use information that lives at the bad end. It is also, by construction, the widest possible
   book, which is the direction the lab's own 2026-09-05 breadth bracket pointed outside
   `price-trend`.
5. **The size interaction discounts one family and clears another.** A ~145-name universe of
   large, liquid global names is precisely where the paper finds the value-type premium weakest.
   The lab has no fundamentals, so it cannot build value anyway — but the transferable form of
   the claim is broader: **a characteristic whose premium is size-dependent is unavailable here
   in advance**, while momentum-type signals, which show no reliable size relation over the full
   panel, are not discounted on this axis. That is a rare piece of good news for a universe this
   large-cap, and it is the opposite of the tension recorded below.

**Pitfalls.**

- **The paper's decomposition is against a market benchmark; this repo has none.** Do not import
  "60% of value comes from the long side" as a number to expect here. What transfers is the
  method and the identity in (3), not the shares.
- **Their smallest quintiles are micro-caps far below anything in this universe**, and their own
  footnote says so. Any statement conditioned on the small end is out of scope here; only the
  large-quintile rows are relevant, and those are the weakest rows for value.
- **An exclusion book has a different cost profile than a selection book**, not obviously worse:
  it turns over only at the boundary of the excluded quantile, but it holds many more names, so
  per-name position sizes fall and the 25% cap never binds. The lab's own bracket already
  measured that wider books traded no more; that is a fact about its own engine, not something
  this paper establishes.
- **`gross leverage ≤ 1.0` is untouched by any of this.** Nothing here suggests levering, and
  the paper's long-only legs are beta > 1 only because they are stock portfolios, not because
  they are levered.

## Related

- `notes/2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — the Up/Down statistic is the
  formal version of "which end carries the pattern", and it and the identity in (3) above are
  answering the same question with different machinery. Run them together on the same score.
- `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md` — an exclusion book is the
  extreme wide-band point of the same axis, so `J` and the choice of construction shape are not
  independent decisions.
- `notes/2026-08-22-long-only-as-l1-regularization.md` and
  `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — both treat the long-only
  constraint as pure information loss. **A tension to record rather than smooth:** the transfer
  coefficient framing measures loss against a benchmark-relative optimum, and this paper says
  that under a raw-return objective the same constraint costs far less and may cost nothing. The
  folder should stop quoting the long-only constraint's cost without saying which objective the
  cost is measured against. Neither source is wrong; they are answering different questions, and
  this repo's gate asks the raw-return one.
- `notes/2026-09-02-anomalies-by-size-group.md` (Fama–French 2008) and
  `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` (Freyberger et al.)
  both conclude that most characteristics fade among large stocks. This paper agrees for
  value-type characteristics and **disagrees for momentum**, on an 86-year panel plus eight
  other markets — which is a genuine narrowing of a claim this folder has been applying
  uniformly.
