---
title: "Understanding Defensive Equity" + "Betting Against Betting Against Beta"
authors: Novy-Marx (2016); Novy-Marx, Velikov (2022)
year: 2016, 2022
venue: NBER Working Paper 20591 (venue tier 2, heavily-cited author with a track record in this exact area); Journal of Financial Economics 143(1), 80–106 (venue tier 1)
url: https://doi.org/10.3386/w20591 ; https://doi.org/10.1016/j.jfineco.2021.05.023
citations: Understanding Defensive Equity 55 (Semantic Scholar by DOI, checked 2026-08-18); Betting Against Betting Against Beta 100 (OpenAlex by DOI, checked 2026-08-18 — Semantic Scholar did not resolve this DOI)
sample_period: January 1968 – December 2015 (Understanding Defensive Equity); January 1968 – December 2017 (Betting Against Betting Against Beta)
markets: US common stocks (NYSE, AMEX, NASDAQ), NYSE breakpoints; one section of Understanding Defensive Equity extends to international samples from 1986
tier: A
validation_overlap: false
published_post_2018: false (Understanding Defensive Equity), true (Betting Against Betting Against Beta)
---

## Mechanism

These two papers are the skeptical case on family 5, and they are not the usual "the effect
decayed" complaint. Neither disputes that low-volatility portfolios have outperformed
high-volatility ones. Both argue that the *reason* is not a low-risk premium, and each
identifies a different substitute cause. Read together they are unusually decisive for this
repo, because both substitute causes are things this repo structurally cannot access.

**Paper 1 — the defensive premium is a size/profitability/valuation premium wearing a
volatility costume.** Novy-Marx starts from a fact rather than a factor: volatility is
strongly negatively related to firm size, and **even more strongly negatively related to
operating profitability** — profitability is described as the single most significant
predictor of low volatility, exceeding even market capitalisation. So sorting on volatility
is an indirect sort on profitability, size and valuation whether you intend it or not. High
volatility and high beta stocks tilt hard toward **small, unprofitable, growth** firms, and
that corner is exactly where the Fama–French three-factor model is known to misprice. The
apparent alpha of defensive equity is then the mechanical consequence of two known facts
composed: defensive strategies underweight unprofitable small growth, and unprofitable
small growth is the segment standard models price worst.

The finding that decides the matter for this repo is the conditional one. **Within style
segments, defensive performance is concentrated entirely in small growth** — and in large
value, the sign flips: aggressive (high-volatility) stocks *significantly outperform*
defensive ones. The premium is not a broad property of the risk dimension; it is a property
of one corner of the size/value grid.

The paper's own summary of what an investor should take from it is worth carrying verbatim
in substance: an investor would have benefited from avoiding unprofitable small-cap growth
firms, but defensive strategies are an **inefficient back door** to that exclusion — the
premia are better accessed directly, and the back door is transactionally expensive.

**Paper 2 — the flagship factor's headline performance is a construction artifact.**
Novy-Marx and Velikov take apart Frazzini–Pedersen's BAB and identify three non-standard
procedures, arguing that each contributes to the published result while none is required by
the underlying economics:

1. **Rank weighting.** Weighting stocks within each leg by beta-rank distance from the
   median, rather than by market capitalisation, produces portfolios "almost
   indistinguishable from simple, equal-weighted portfolios". The authors' point is not what
   rank weighting does (tilt toward extreme betas) but what it *avoids* doing (cap
   weighting) — it is a **back door to equal weighting** an asset-pricing factor.
2. **Hedging by leveraging.** Levering the low-beta leg and de-levering the high-beta leg to
   beta 1 — rather than hedging the dollar-neutral low-minus-high strategy by buying the
   value-weighted market — means the hedge is performed with those same rank-weighted
   (≈ equal-weighted) portfolios. So procedure 2 is a **back door to hedging with the
   equal-weighted market** rather than the value-weighted one, and the resulting factor is
   more similar to the equal-weighted market than to the value-weighted market.
3. **The beta estimator.** The FP beta is not a regression slope. The authors give the
   identity

   ```
   β_FP,i = [ (σ_i,1yr / σ_i,5yr) / (σ_mkt,1yr / σ_mkt,5yr) ] · β_i,5yr
   ```

   — a genuine five-year CAPM beta multiplied by the stock's short-horizon-to-long-horizon
   volatility ratio, scaled by the market's. Cross-sectionally this blends beta with stock
   volatility; in the time series it is biased in a way **predictable from market
   volatility**. The consequence is not a small measurement quibble: the paper's headline
   theoretical evidence, "beta compression" when funding-liquidity risk is high, is argued
   to be this estimator's mechanical bias rather than a market phenomenon.

The size consequence of (1) and (2) together: **for each dollar invested in BAB, the
strategy commits on average $1.05 to stocks in the bottom 1% of total market
capitalisation.** Under standard value weighting the effect is far smaller. Net of
transaction costs BAB's profitability falls by nearly 60% and it retains no significant
alpha against the Fama–French five-factor model — what survives is compensation for
profitability and investment exposures, i.e. Paper 1's conclusion reached from the
construction side.

## Construction recipe

Recorded mainly so the lab can recognise these constructions when they appear elsewhere,
since the verdict below is negative.

- **Defensive sorts (Paper 1).** Volatilities and betas estimated **each month from one year
  of daily data**. Quintile portfolios formed monthly on **NYSE breakpoints** (explicitly
  *not* CRSP breakpoints — the author notes CRSP breaks produce extreme size biases, with
  the high-volatility quintile collapsing to sub-$250m average market cap and under ~1.2% of
  total market capitalisation). Value-weighted returns, monthly rebalance.
- **The breakpoint choice is the methodological lesson.** Two defensible-sounding
  implementations of "sort stocks into volatility quintiles" differ mainly in *how much
  microcap exposure they smuggle in*, and that difference drives the result. This is a
  breakpoint analogue of the lab's own "check what the code actually reads" lesson.
- **Standard-construction BAB (Paper 2's counterfactual).** Same beta sort, but cap-weight
  within legs and hedge the dollar-neutral low-minus-high spread by buying the
  value-weighted market in proportion to its observed short market tilt, instead of levering
  each leg to beta 1. This is the version the authors consider a fair test of the economics.
- **Costs.** Paper 2 estimates transaction costs following Novy-Marx–Velikov's own cost
  methodology and reports BAB's costs averaging around 60 bps/month — roughly an order of
  magnitude above what this repo's whole champion pays per year in cost drag, and a direct
  consequence of trading the microcap tail.

## Robustness evidence (qualitative only)

- Both papers use multi-decade US samples with standard, disclosed portfolio construction,
  and both model transaction costs explicitly.
- Paper 2 is a **direct, tier-1, published replication challenge** to a tier-1 published
  factor — the strongest form of replication evidence the rubric recognises. It reproduces
  the original series first (very high correlation with the published factor, matching
  Sharpe) and only then varies one construction choice at a time. That order matters: the
  disagreement is demonstrably about construction, not about data or coding.
- Paper 1 explicitly notes that earlier work — including Blitz–van Vliet and the
  Asness–Frazzini–Pedersen paper in the companion note — rejected size and value as
  explanations, and locates their error in the omission of **profitability**, a variable
  that postdates most of that work's model specifications.
- **Direct contradiction to record, not to smooth over.** Asness–Frazzini–Pedersen report
  the low-risk effect present in both small-cap and large-cap subsamples, US and global.
  Novy-Marx reports that within large value it **reverses**, and Novy-Marx–Velikov report
  that once the microcap overweight is removed by standard weighting the effect is far
  weaker. These are not reconcilable by reading harder; they are a live disagreement about
  whether the effect exists away from the small end. Two things tilt the weight of evidence
  toward the skeptical side *for this repo specifically*: the disagreement is about the
  large-cap end, which is the only end this repo trades; and AFP's own size split shows
  large-cap alphas weaker than small-cap alphas in every column, so even the favourable
  source agrees on the direction of the gradient, only not on where it hits zero.
- Limits worth stating: Paper 1 is a working paper (tier 2 venue) with a modest citation
  count, and both papers are US-only. Paper 1's central variable (profitability) is
  unobservable in this repo, so its explanation cannot be tested here — it can only be
  believed or not.

## Implementability here

**Verdict: family 5 is closed on this universe, and now for a stated mechanism rather than
only by the lab's two empirical refutations.** This is the strongest form of closure this
folder can produce — an independent literature predicting the lab's result before seeing it.

The argument, in the order the constraints bite:

1. **The premium lives where this repo cannot trade.** Paper 1 puts defensive
   outperformance in the small-growth corner and finds the *opposite* sign in large value;
   Paper 2 puts BAB's performance in the bottom 1% of market capitalisation. The repo's
   universe is ~145 large, liquid global stocks and ETFs. There is no signal refinement
   that relocates a universe. This is the same structural point McLean–Pontiff made about
   surviving predictability concentrating in high-idiosyncratic-risk, low-liquidity
   names — a second, independent arrival at "a large slice of the anomaly zoo is
   unavailable here", now specific to family 5.
2. **The surviving cause needs fundamentals.** What Paper 2 finds still standing after costs
   is compensation for **profitability and investment** exposures. The repo has daily
   adjusted closes and nothing else. Even if one accepted the effect entirely, the
   implementable route to it is closed and the price-based route is the "inefficient back
   door" Paper 1 names.
3. **The costs are wrong by an order of magnitude.** A strategy whose published net result
   depends on trading microcaps at ~60 bps/month is not a candidate under a flat 15 bps/side
   assumption applied to large caps — and note the direction of the error: a flat cost model
   *understates* what this strategy would really pay, so a backtest here would flatter it.
4. **This closes the sector-neutral escape hatch specifically.** `learnings.md` left family 5
   open pending "a genuinely different vol construction (e.g. sector-neutralized, not raw
   trailing)". The companion note supplies that construction; this note supplies the reason
   it does not rescue the family — the industry-neutral variant is the *most* leverage-hungry
   version of a bet whose payoff is leverage, and the skeptical literature says the residual
   is a size and profitability tilt in any case. **Both halves of the named gap are now
   filled, and both point the same way. Family 5 should be treated as closed rather than
   merely uncovered.**

**What is genuinely worth keeping, and it is not a strategy idea.** Paper 2 is an
independent, tier-1 instance of the lab's own hardest-won lesson — *before crediting a
component, check what its code actually reads*. The lab learned it by discovering that its
champion's "basket-own vol-spike trim" was silently reading an eleven-name legacy cohort,
at a cost of four trials. Novy-Marx and Velikov show a published factor with hundreds of
citations whose headline performance came from two weighting conventions nobody read as
weighting decisions, and whose theoretical support came from an estimator that was not
estimating what its name said. **Generalised screen: for any imported result, write down
what the construction actually computes, in primitive terms, and check it against what the
paper says it computes.** The FP-beta identity is the model of how to do it — a single line
of algebra that reveals the estimator is a beta multiplied by a short-to-long volatility
ratio. Note in passing, without over-reading it: the champion's own vol-spike trim is also a
short-over-long realized-volatility ratio (21d/252d), so this literature is a reminder that
such a ratio is *its own signal*, not a proxy for the level of anything.

**Pitfall.** Do not read "defensive equity is explained by profitability" as a suggestion to
find a price-based profitability proxy. That is the "find a better score" direction
`learnings.md` marks as heavily explored and low-yield after four refutations, and Paper 1
explicitly says the back door is worse than the direct route this repo cannot take.

## Related

- `2026-08-18-low-risk-investing-industry-neutral.md` — the source these two dispute; read
  as a pair.
- `2026-08-17-mclean-pontiff-publication-decay.md` — surviving predictability concentrating
  in illiquid, high-idiosyncratic-risk names; same structural conclusion, arrived at from
  the decay side.
- `2026-08-17-naive-vs-optimized-weighting.md` — rank/equal weighting versus cap weighting as
  a first-order performance driver.
- `experiments/learnings.md` — "Low-vol stock tilt is refuted, standalone and as a
  within-momentum filter" (the empirical refutation this note supplies a mechanism for), and
  "before crediting a component, check what its code actually reads" (trials #37–#40).
