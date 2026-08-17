---
title: "Rebalance Timing Luck: The Difference between Hired and Fired" + "Rebalance Timing Luck: The (Dumb) Luck of Smart Beta"
authors: Hoffstein, Sibears, Faber (2019); Hoffstein, Faber, Braun (2020)
year: 2019, 2020
venue: Journal of Index Investing / Journal of Beta Investment Strategies, 10(1), 27 (venue tier 3, practitioner journal); 2020 companion is an SSRN working paper (venue tier 3)
url: https://jii.pm-research.com/content/10/1/27.abstract ; https://ssrn.com/abstract=3673910
citations: 2020 SSRN companion 4 (OpenAlex, checked 2026-08-17); 2019 JII article not indexed in Semantic Scholar or OpenAlex under its DOI (checked 2026-08-17)
sample_period: not verified this session — simulated US large-cap factor indices; the 2020 study builds them from the S&P 500 universe with Sharadar fundamental data, so the sample plausibly runs up to its publication year
markets: US large-cap equity, simulated style indices (value, size, momentum, quality, low volatility)
tier: B — but now the weakest-evidenced source in this folder and a candidate for C. The citation check (2026-08-17) confirmed what was previously only assumed: tier-3 venue, 4 citations on the companion, the JII article not indexed at all. The mechanism is an arithmetic identity and stands on its own; the empirical magnitudes around it should be treated as hypothesis fodder only.
validation_overlap: unverified, assume true (sample end not confirmed; a 2020 publication may touch 2018–2019)
published_post_2018: true
---

## Mechanism

Any strategy that rebalances on a discrete schedule embeds a choice nobody makes
deliberately: **which date within the cycle**. Two managers running an identical process —
same universe, same signal, same holding count, same monthly or annual cadence — who happen
to rebalance on different dates will hold different portfolios and earn different returns,
sometimes for years, purely because they sampled the signal at different moments. The
divergence carries no information: neither date is better ex ante, so the whole spread is
noise added on top of the strategy's own risk.

The authors name and measure this. **Rebalance timing luck is defined as the standard
deviation of returns across identically managed portfolios ("sub-indexes") that differ only
in rebalance date.** Two consequences follow, and they are the reason the concept matters
beyond bookkeeping:

- It is a variance the investor is paid nothing for. Unlike the strategy's factor exposure,
  it has zero expected return, so it is pure dilution of realised information ratio.
- It contaminates *comparisons*. A single backtest of a discretely rebalanced strategy is one
  draw from this distribution, not the distribution's centre. Differences between two
  variants — or between a strategy and its benchmark — that are smaller than the timing-luck
  scale are not evidence of anything.

What drives the magnitude, per their ex ante model and its empirical validation:

- **Turnover** — higher turnover means the date choice changes more of the book, so more
  timing luck.
- **Concentration / holding count** — fewer names means each date-specific selection differs
  more from its neighbours; more holdings damps it.
- **Rebalance frequency** — rebalancing more often means each date's decision governs less of
  the book's lifetime, so *more frequent* rebalancing carries *less* timing luck.
- The opportunity set / nature of the underlying signal — how much the eligible set churns
  between adjacent dates.

(Per this repo's anti-lookahead policy I have deliberately not recorded the papers'
sample-specific magnitudes for how large timing luck was in their simulated indices. The
qualitative point that survives: it is large enough to be economically meaningful relative
to the premia these strategies are trying to harvest, i.e. large enough to decide which
manager looks good.)

## Construction recipe

The fix is the **overlapping-portfolio / tranching / staggered-rebalance** construction:

1. Split capital into N equal tranches.
2. Assign each tranche a different offset within the rebalance cycle — for a monthly cycle,
   N tranches formed in N successive months; for an annual cycle, twelve monthly offsets.
3. Each tranche runs the identical process on its own schedule; it is *not* re-selected off
   the others' dates.
4. Hold the tranches in **equal weight**; the live book is the equal-weighted average of the
   N sub-index weight vectors.

Reported result: equal-weighting across N sub-indexes reduces rebalance timing luck **by a
factor of 1/N**. Caveat on precision — the measure is defined as a standard deviation, and I
could not reach the full text to confirm whether the stated 1/N factor applies to that
standard deviation or to its variance. Treat the direction and the "more tranches, less
timing luck, with diminishing marginal benefit" shape as the reliable content, and do not
build any quantitative claim on the exact exponent without re-reading the source.

Note that the mechanism is *averaging imperfectly correlated variants of the same process* —
so it needs the tranches to be genuinely differently-dated. Anything that re-synchronises
them (re-selecting each tranche against the current date's ranking) destroys the effect.

## Robustness evidence (qualitative only)

- The core claim is close to a statistical identity — averaging N imperfectly correlated
  estimates of the same target reduces the dispersion of the average — which is why it
  travels well and does not depend on a particular market or era.
- The empirical half is thinner: practitioner research, one market (US large-cap), simulated
  indices built by the authors, no independent replication that I could verify, and the ex
  ante model is the authors' own. The tier-B rating is driven by this, not by the logic.
- The drivers (turnover, concentration, frequency) are validated empirically across several
  style sleeves rather than a single strategy, which is the strongest part of the evidence.
- Standing caution from `2026-08-17-mclean-pontiff-publication-decay.md` does **not** apply
  here in its usual form: this is not a return predictor that arbitrage capital can compete
  away, it is a property of how portfolios are sampled in time. There is nothing to decay.

## Implementability here

**Directly on the repo's live axis, and it partly fills a gap SUMMARY.md flagged.** The
open-questions list noted that the lab's overlapping-tranche result had no literature behind
its *economic* claim — Jegadeesh–Titman use overlapping vintages only as a statistical
estimator. This source is the literature that does treat tranching as a portfolio
improvement. But be precise about what it claims:

1. **It supports tranching as dispersion reduction, not as an expected-return gain.** The
   claimed benefit is a smaller spread of outcomes around the same mean. The lab's finding —
   that the six-tranche book earns *more* than the single-vintage one, and that pruning the
   stale names hurts — is a claim about expected return, and it remains beyond this source
   too. What this source does add is that the lab's temporal-breadth mechanism and its own
   variance mechanism are compatible and would compound: decorrelated formation dates both
   diversify the sampling noise and, per the lab, hold names no contemporaneous rule would.

2. **The most useful thing here is a measurement caution, not a new candidate.** Every
   non-tranched backtest in this repo — including the single-vintage comparisons that the
   overlap was scored against — is one draw from a timing-luck distribution, while the
   tranched book is closer to that distribution's centre. Part of any measured Sharpe gap
   between a K=1 and a K=6 version of the same strategy is therefore mechanical, and the
   *sign* of the luck component in any single comparison is unknowable. This does not
   threaten the overlap finding (which is large, and corroborated by the pruning diagnostic
   moving three metrics at once), but it does mean small Sharpe differences between variants
   that differ in rebalance mechanics should be treated as noise by default.

3. **The drivers table gives a free ex ante reading, no trial required.** Timing luck rises
   with turnover and concentration and falls with holding count and rebalance frequency —
   which says the repo's *most* timing-luck-exposed constructions are exactly the
   magnitude-weighted narrow-basket ones (high concentration), and that the wider 35/20
   basket was, in addition to its lower turnover, a timing-luck reduction. This is a
   holdings-only property: it can be reasoned about from the weight matrix, which the
   learnings file already endorses as a way to pre-empt trials.

4. **Do not turn this into a K sweep.** `learnings.md` forbids that explicitly, and this
   source gives no reason to reopen it: 1/N-shaped benefits have diminishing marginal returns,
   so the argument for any particular K stays where the Jegadeesh–Titman note put it (bounded
   above by the post-formation reversal horizon), not in a scan.

Limits for this repo: US large-cap, long-only style indices are a decent structural match
(long-only, discrete rebalance), but the strategies studied are lower-turnover index products
than a momentum book, and the paper is practitioner work whose empirical half I could not
verify directly. Treat the mechanism as sound and the measurements as unchecked.

## Related

- `2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the same construction, framed as a
  statistical estimator; read the two together to see what each does and does not claim.
- `2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the cost-side account of
  rebalance mechanics; note that this source says *more frequent* rebalancing lowers timing
  luck while that one says it raises cost, so cadence trades one against the other.
- `experiments/learnings.md`: "Overlapping formation tranches are the strongest mechanism in
  the repo" and "Breadth only pays when it comes from decorrelated formation dates" — the
  latter is exactly the condition this construction requires to work.
