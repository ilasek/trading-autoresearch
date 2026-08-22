---
title: "What Does Rebalancing Really Achieve?"
authors: Cuthbertson, Hayley, Motson, Nitzsche
year: 2016
venue: International Journal of Finance & Economics 21(3), 224–240 — venue tier 2 (peer-reviewed field journal, below the JF/JFE/RFS tier)
url: https://doi.org/10.1002/ijfe.1545  (accepted version read in full: https://openaccess.city.ac.uk/id/eprint/13733/)
citations: 13 (Semantic Scholar, checked 2026-08-22); 9 (Crossref, checked 2026-08-22)
sample_period: none — analytic derivation plus Monte Carlo simulation (100,000 paths, horizons up to 100 years)
markets: n/a (no historical data used)
tier: B — the algebra is checkable and decisive, but the venue is mid-tier, citation count is modest, and there is no empirical content
validation_overlap: false
published_post_2018: false
---

## Mechanism

This paper is a correction, not a discovery, and it is aimed squarely at the literature the folder
covered in session 8. Its claim is that the rebalancing literature systematically **misattributes**:
it conflates *diversification return* — a growth benefit any diversified book earns, rebalanced or
not — with *rebalancing return* — a benefit supposedly created by the rebalancing trades
themselves. Four results, all mechanism-level:

1. **"Excess growth" is not created by rebalancing.** The paper derives, in complete generality,
   that an **unrebalanced** portfolio also has an expected growth rate above the weighted average
   of its components' growth rates. The whole effect is the arithmetic/geometric relation
   `E[GM] ≈ E[AM] − σ²/2` applied to a basket whose variance is below the weighted average of its
   constituents' variances. That relation "makes no presumption about rebalancing — it applies to
   the returns of both rebalanced and unrebalanced portfolios."
2. **Rebalanced and buy-and-hold books start with identical expected growth rates**, and diverge
   only *as the buy-and-hold weights drift* and the book becomes progressively less diversified.
   The gap is therefore a **diversification-decay** gap, not a payment for trading.
3. **Under IID returns the rebalancing trades have zero expected value.** Each trade moves wealth
   into an asset "as likely to outperform as underperform the asset it replaces". The paper's
   summary of the mechanism is that in the absence of mean reversion in relative asset prices, the
   greater expected growth of a rebalanced strategy "is entirely explained by their lower portfolio
   volatilities rather than — as is claimed — being due to the rebalancing trades themselves being
   profitable". The corollary is the one that matters here: **rebalancing trades are profitable
   only where relative prices mean-revert, and lose where relative prices trend.** Explicitly:
   "Rebalancing trades are profitable on average on paths where `S_t` tends to mean revert… when
   `S_t` makes large cumulative moves in either direction (i.e. tends instead to trend) then `P_r`
   underperforms `P_u`."
4. **The infinite-horizon argument does not transfer to finite horizons.** The classic
   "buy on downticks, sell on upticks" argument (Fernholz–Shay) relies on the price returning to
   its starting level, which happens infinitely often with probability one — but the probability
   that the rebalanced book beats the unrebalanced one approaches unity only over horizons far
   beyond any investor's. Over horizons of up to 100 years the rebalanced book won in fewer than
   70% of the authors' 100,000 simulated paths. Worse for the naive reading: **expected terminal
   wealth is higher for the unrebalanced book** (`E[P_u] > E[P_r]`), because the unrebalanced book
   keeps an ever-thinner but ever-more-extended right tail. Median-vs-mean, not a contradiction —
   but it means "rebalancing eventually wins" is a statement about a probability, not about an
   expectation.

The authors' policy conclusion is the negative of the volatility-harvesting slogan: do **not** seek
out volatile assets or trade more to enlarge the rebalancing trades; minimise volatility drag by
diversifying effectively, and "rebalance no more than is necessary to keep portfolio compositions
adequately close to their target allocations".

## Construction recipe

No strategy is proposed, so the recipe is a **reasoning procedure** to apply before crediting any
construction change with a rebalancing benefit:

1. Compare like for like. A rebalanced and an unrebalanced book that start identical are *not*
   comparable later, because the unrebalanced one has different composition. Any claimed
   rebalancing gain measured against a drifted comparator is partly a composition difference.
2. Decompose the claimed gain into (a) the diversification/volatility-drag term, available to both
   books, and (b) the residual attributable to the trades. Under no relative-price autocorrelation
   (b) is zero in expectation.
3. Ask what sign of relative-price autocorrelation the strategy is betting on. Constant-weight
   rebalancing is a **contrarian** overlay: it is long relative-price mean reversion. If the
   underlying signal is long continuation, the two are working against each other.
4. Check the horizon. Results proved as `T → ∞` say little at the horizons a backtest measures, and
   probability-of-outperformance and expected-terminal-wealth can point in opposite directions.

## Robustness evidence (qualitative only)

The core arguments are algebraic and hold under the standard geometric-Brownian assumptions the
rebalancing literature itself uses, so there is little to replicate; the simulations are chosen to
be the setting *least* favourable to the unrebalanced book (IID, no autocorrelation) and the result
still goes against the received claim. The paper has been through peer review at a credible field
journal and thanks Willenbrock — whose note is in this folder — among its commenters, so it is a
considered response inside the same conversation rather than an outside attack. Its weaknesses are
the ones any purely theoretical paper has here: modest citation count, no empirical work, and no
transaction costs modelled (costs are invoked only in the policy conclusion, where they strengthen
the argument). It says nothing about whether relative prices actually do mean-revert in any market
— explicitly out of scope.

## Implementability here

Nothing to build; this is a **screen and a correction**, and it lands on a question the folder
raised itself.

- **It corrects session 8's own framing.** `SUMMARY.md` recorded the rebalancing term as "a
  quantity the champion is currently *giving away*". On this source's reading that is wrong in two
  places at once. (i) The part of the effect that is real — the diversification / volatility-drag
  reduction — is **not** given away: the champion earns it by holding a diversified basket at all,
  whether or not it re-targets. (ii) The part that is genuinely specific to the resetting trades
  has positive expected value only if relative prices mean-revert, and a cross-sectional momentum
  book exists on the bet that they do not. So the incremental term is not an unclaimed prize; on
  this book its expected sign is **negative**, and the champion's monthly re-target to
  signal-proportional targets is paying for it in both cost and expectation.
- **It supplies a mechanism for two results the lab already has, and predicts the sign of a third.**
  The trial that re-targeted weekly from a fresher composite lost badly, and the trial that let a
  compounding `prev_weight × price growth` tilt run also lost — those bracket the re-target cadence
  empirically. This source says *why* the two directions are not symmetric: more frequent resetting
  is a larger contrarian overlay on a continuation signal, which is the wrong direction twice over
  (expectation and cost); letting weights compound indefinitely is the opposite error, discarding
  the signal entirely. The recorded ranking is exactly the shape the mechanism predicts. It also
  supplies the missing argument for the membership buffer under its *new* justification: a
  hold-band suppresses resetting trades, i.e. removes contrarian trades a momentum book does not
  want, which is a distinct claim from the cost claim `learnings.md` retired.
- **It tightens the existing "mean-shifting vs dispersion-shrinking" principle with a third
  category.** Before crediting a construction change, ask not only whether it moves the centre or
  narrows the distribution, but **which sign of relative-price autocorrelation it is implicitly
  long**. Constant-weight rebalancing is long mean reversion; letting winners run is long
  continuation; the champion does both at once and the two legs partially cancel.
- **Do not turn this into a "stop rebalancing" proposal.** The paper does not say weights should be
  left to drift — that loses the signal and, per its own result 2, degrades diversification
  monotonically. It says the *marginal* trade has no free return attached to it. The buildable
  content is already covered by the folder's re-target-cadence bracket and by the buffer; treat this
  note as explanation and as a bar for future claims, not as a new candidate.
- **Tension with the folder's session-8 note, recorded rather than smoothed over.** Willenbrock
  settles the *identity* (a rebalanced book's geometric return exceeds the weighted average of its
  constituents' geometric returns) and this paper does not dispute the algebra — it disputes the
  *attribution*, showing the same excess appears without rebalancing. Both can be true because they
  are claims about different comparators. Where they genuinely disagree is on whether the term is
  evidence that rebalancing pays; on that, this source is the more careful one and should govern.

## Related

- `notes/2026-08-21-diversification-return-and-rebalancing.md` — the source this one corrects.
- `notes/2026-08-22-excess-growth-and-return-decomposition.md` — the identity in its most general
  form; this note is the guard rail on how to read it.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — banding suppresses
  low-information trades on cost grounds; this source adds an expectation-side reason on a
  continuation signal.
- `experiments/learnings.md` — the re-target-cadence bracket (weekly re-target and unbounded weight
  drift both lost) and the buffer's retired cost justification.
