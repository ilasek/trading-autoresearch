---
title: "A Primer on Portfolio Choice with Small Transaction Costs — with: Capital Market Equilibrium with Transaction Costs; Asymptotic Analysis for Optimal Investment and Consumption with Transaction Costs"
authors: Muhle-Karbe, Reppen & Soner; Constantinides; Janeček & Shreve
year: 2017; 1986; 2004
venue: Annual Review of Financial Economics 9, 301–331 (venue tier 2 — peer-reviewed review journal, not one of the rubric's tier-1 outlets); Journal of Political Economy 94(4), 842–862 (venue tier 1); Finance and Stochastics 8(2), 181–206 (venue tier 2 — peer-reviewed mathematical-finance journal)
url: https://doi.org/10.1146/annurev-financial-110716-032445 (full text read from arXiv:1612.01302v2, https://arxiv.org/pdf/1612.01302) ; https://doi.org/10.1086/261410 (NOT READ — cited for the equilibrium result the primer attributes to it) ; https://doi.org/10.1007/s00780-003-0113-4 (NOT READ — cited as the origin of the cube-root scaling, which the primer re-derives in full and which this note takes from the primer)
citations: "Muhle-Karbe–Reppen–Soner: 29 (Semantic Scholar by DOI, checked 2026-10-08; OpenAlex 25, Crossref 23 — three indexes within a few counts of each other, so the modest number is real and not an indexing artifact). Constantinides: 828 (Crossref is-referenced-by-count, checked 2026-10-08). Janeček–Shreve: 132 (Crossref, checked 2026-10-08)."
sample_period: "None — this is theory. The primer contains no empirical sample; its illustration is a calibrated Kim–Omberg model with mean-reverting expected returns, not a backtest."
markets: "None. The results are asset-class agnostic and stated for a single risky asset plus a safe asset; the multi-asset case is discussed and is explicitly unsolved in closed form (see Robustness)."
tier: "B. The mathematics is rigorous and the central scaling result has two independent origins (Janeček–Shreve 2004 and Rogers 2004) plus later rigorous convergence proofs, so the *theory* is settled. It is graded B rather than A because there is no empirical content at all: nothing here has been tested against market data by its authors, the citation counts are modest, and the headline result is an asymptotic valid for *small* costs — a condition a 50 bps stamp duty may well violate (see Implementability)."
validation_overlap: false
published_post_2018: false
---

## Mechanism

Protocol v3 charges the trades that undo drift: "Holdings drift between rebalances and undoing
drift is charged", with costs "per name: a liquidity tier (15/20/30/40 bps per side by trailing
USD volume) plus UK/HK/FR/IT/ES transaction taxes" (`program.md`, Protocol v3). That makes the
question *how far a holding may drift before it is worth paying to correct it* a first-order
design question for the first time in this lab's history — under v1 and v2 drift was free.

This folder has two notes adjacent to that question and neither answers it. A grep across all
170 prior notes returned **zero** for `no trade region`, `Leland` and `Davis-Norman`;
`Constantinides` appeared only in last night's tax-trading notes, in an unrelated capacity.

The gap matters more than a missing citation, because **the policy shape depends on the
functional form of the cost, and the lab's covered policy is the answer to a different cost
form.** The primer states the taxonomy explicitly, and this is the single most useful passage
in it:

> "The fine structure of the optimal strategies crucially depends on the cost at hand. With
> **proportional** costs, one performs the minimal amount of trading to remain in a no-trade
> interval around the frictionless target. With **fixed** costs, it is no longer possible to
> implement such a strategy involving infinitely many small trades; hence, one directly trades
> back to a target portfolio once the boundaries of the no-trade region is reached. Conversely,
> **quadratic** costs lead to smaller penalties for very small trades but make large turnover
> rates prohibitively expensive. Thus, optimal strategies always trade towards the target at
> some finite, absolutely continuous rate."

Four cost forms, four different policies:

| Cost form | Optimal policy | Band scaling in cost λ |
|---|---|---|
| Proportional (bps per side, ad valorem tax) | Trade the **minimum** that keeps you inside the band — i.e. to the **boundary**, never to target | width ∝ λ^(1/3), utility loss ∝ λ^(2/3) |
| Fixed (per-ticket) | On touching the boundary, trade **all the way back to target** | width ∝ λ^(1/4), loss ∝ λ^(1/2) |
| Fixed + proportional | Trade to a point **in between** the boundary and the target | — |
| Quadratic (impact) | **No band at all**: trade toward the target continuously at a finite rate | — |

The last row is Gârleanu–Pedersen's aim portfolio, which this folder covers in
`notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md`: "move a **fixed fraction**
`a/λ` of the distance from the current book to `aim_t`". That rule is correct — for quadratic
costs. **Protocol v3's costs are proportional, not quadratic** (a per-side bps charge and an ad
valorem tax; there is no size-dependent impact term in the v3 description). So the covered
partial-move policy is the solution to a cost geometry this lab does not face, and the
uncovered no-trade-region policy is the solution to the one it does.

**Why a band exists at all**, in the primer's own words — the trade-off that pins its width:

> "On the one hand, a narrower no-trade region leads to more frequent trading, and whence also
> higher direct transaction costs. On the other hand, a wider no-trade region leads to larger
> oscillations around the frictionless target portfolio and thus higher indirect losses due to
> displacement from the optimal risk-return trade-off."

With proportional costs, the trading needed to stay inside a band of width ∆ scales as 1/∆ (a
property of reflected Brownian motion and its local time at the boundary), while the loss from
sitting off-target is locally quadratic and so scales as ∆². The total loss is therefore of the
form

    C₁∆² + C₂λ/∆

whose minimiser is of order λ^(1/3), with a minimal utility loss of order λ^(2/3). The primer
notes the parallel argument for fixed costs gives λ^(1/4) and λ^(1/2) instead. Two things follow
that are not obvious:

- **The band is much wider than the cost.** Tripling a cost widens the optimal band by only
  3^(1/3) ≈ 1.44×, but the band's *level* is a cube root, so even a small cost buys a wide band.
  Cube roots are flat: this is why banding works at all, and why fine-tuning a band width is
  low-value (see Implementability).
- **The welfare cost of frictions is λ^(2/3), not λ.** Costs hurt *less* than proportionally,
  because the optimal policy is allowed to respond. A backtest that charges λ while rebalancing
  on a cost-blind schedule overstates the damage a cost-aware strategy would suffer — and
  equally, the gap between the two is the size of the prize for doing item 1 in Implementability.

## Construction recipe

The explicit result, for power utility with constant relative risk aversion γ, one risky asset
and a safe asset. The no-trade region in **weight space** is

    | y/(x+y) − π(t,f) |  ≤  λ^(1/3) · ∆π(t,f)

where π is the frictionless target weight and the halfwidth is

    ∆π = [ (3/(2γ)) · ( π²(1−π)² − 2π(1−π)·π_f·(σ_F/σ_S) + π_f²·(σ_F²/σ_S²) ) ]^(1/3)

with σ_S the risky asset's volatility, σ_F the volatility of the state variable f driving
expected returns, and π_f = ∂π/∂f the sensitivity of the target weight to that state variable.
The primer's summary: "the halfwidth of the asymptotically optimal no-trade region is fully
determined by the volatilities σ_S, σ_F, the risk aversion γ, as well as the frictionless
portfolio weight π and sensitivity π_f with respect to the state variable f."

**The case worth implementing first is the constant-target one**, π_f = 0 (the target weight
does not move with a predictive signal). Then the whole formula collapses to

    halfwidth = λ^(1/3) · (3/(2γ))^(1/3) · [ π(1−π) ]^(2/3)

which has three readable properties, each a design rule:

1. **Band width scales as the name's own cost to the one-third power.** This is the operative
   rule for v3's per-name costs: a name whose round trip costs 3× another's gets a band
   3^(1/3) ≈ 1.44× wider, not 3× wider.
2. **Band width scales as [π(1−π)]^(2/3) in the target weight.** A small position gets a
   *proportionally much wider* band than a large one: at π = 0.001 the halfwidth is ~1% of the
   position itself, while at π = 0.25 it is a far smaller fraction. In a long-only book of ~100
   names at ~1% each, the bands are wide in relative terms, which argues that drift should mostly
   be left alone.
3. **Band width shrinks as γ^(−1/3).** More risk aversion ⇒ tighter tracking. γ is the one free
   parameter and a cube root of it, so getting it wrong by a factor of 8 moves the band by 2×.

**And the trading rule, which is the half most likely to be got wrong:** with purely proportional
costs, "it is optimal to perform the minimal amount of trading that keeps the portfolio within
the no-trade region". When a weight breaches the band you trade it **back to the band edge, not
back to the target.** Trading to target is the *fixed*-cost policy. On a book of ~100 names this
distinction is the difference between touching one name a little and reforming the book.

**Where the signal re-enters.** The π_f terms are what a predictive signal does to the band: a
target that moves with a fast-moving signal gets a band shaped by the signal's own volatility
relative to the price's, not just by the cost. Qualitatively this is the same insight as the
aim-portfolio literature's — faster-decaying signals deserve less aggressive tracking — but the
mechanism differs, and the formula above makes the dependence explicit for proportional costs.

## Robustness evidence (qualitative only)

- **The scaling result has two independent origins** (Janeček–Shreve 2004 in *Finance and
  Stochastics*, and Rogers 2004, "Why is the effect of proportional transaction costs O(δ^{2/3})?")
  and the primer cites a subsequent literature establishing *rigorous* convergence of the
  asymptotics via the perturbed-test-function method, not merely formal expansions. The
  foundational no-trade-region results go back to Constantinides (1986), Davis–Norman (1990) and
  Shreve–Soner (1994). For a theoretical result this is as replicated as it gets.
- **It is robust to the cost structure in the coarse sense that matters.** The primer: "the
  'coarse' structure of all these models is nevertheless very similar: In each case, the distance
  from the target is a trade-off against the specific trading cost, balanced by an appropriate
  control. The corresponding expected displacement and average transaction costs display the same
  comparative statics in each case, up to a change of asymptotic convergence rates and constants."
  So *that* a band exists and *which direction* its width moves are robust; the exponent is not.
- **The headline caveat, and it is a real limitation here: there is no closed form for multiple
  risky assets with proportional costs.** The primer is explicit — "less is known about the case
  of several risky assets. In this case, the homogenization approach still reduces the
  dimensionality of the problem but the resulting corrector equations no longer admit an explicit
  solution. As a consequence, numerical methods such as the policy iteration scheme... are needed
  even for the asymptotic analysis." Closed forms in multiple dimensions exist for quadratic and
  fixed costs, **not** for proportional ones. Applying the one-asset halfwidth independently per
  name is therefore a heuristic, and specifically it ignores that correlated names' deviations
  partly offset. Expect it to be too tight (it treats offsetting drifts as two problems).
- **It is a small-cost asymptotic.** The result is a λ → 0 limit. Nobody in this literature claims
  it for large costs, and a 0.5% UK stamp duty on purchases is not obviously small.
- **No empirical validation whatsoever**, by its authors or (so far as this session found)
  independently. Zero cost-modelling honesty concerns in the usual sense — costs *are* the
  subject — but equally zero evidence that the formula improves a real book's net return.
- **Multiple testing**: not applicable; nothing is searched or selected here.

## Implementability here

**Which panel.** The protocol v3 panel (~1,400 point-in-time index members plus 42 ETFs, ~1,000
eligible on a typical validation date). Nothing below depends on panel width — the band is
per-name — but the breadth matters for item 3.

1. **The highest-value item, and it is a construction change rather than a signal: replace "emit
   a full row on a fixed grid" with "emit only the names outside their bands, moved to the band
   edge".** Under v3 this is now expressible, because v3 holds positions as shares between the
   rows a candidate emits and charges only what the candidate actually changes. A candidate can
   therefore emit a **sparse** row — a weight for the breaching names only — and leave the rest to
   drift. Band halfwidth per name from the recipe above, with that name's own v3 cost as λ: the
   liquidity tier (15/20/30/40 bps) plus the listing market's tax where one applies, which is
   where tonight's companion note on transaction taxes feeds in. A FTSE name paying 15 bps plus
   50 bps stamp duty on purchases has λ ≈ 3–4× a liquid untaxed US name's, hence a band ~1.5×
   wider — a modest, principled, non-fitted asymmetry. **This is a mechanism, not a knob:** the
   one free parameter is γ, it enters as γ^(−1/3), and it should be fixed once by argument and
   never swept. The lab's standing rule against parameter sweeps (`learnings.md`: "test ideas, not
   knobs") is satisfied by construction here only if γ is fixed *before* the trial.
2. **The caution that makes item 1 honest: the lab's existing band evidence is about a different
   band.** `learnings.md` records hysteresis bands repeatedly, and they are bands on **score rank**
   — "hold while ranked in the top 25, enter only in the top 15" (`mom_12m_buffered`), with a later
   entry recording a band construction that *doubled* turnover when the underlying score was a
   bounded ratio clustering near 1.0. A no-trade region is a band on **portfolio weight**, a
   different object with a different failure mode: a rank band controls *membership* churn, a
   weight band controls *re-sizing* churn. The lab has already decomposed turnover into those two
   components (`learnings.md`: "entry/exit vs re-sizing turnover decomposition" among its cheap
   diagnostics) and found re-sizing to be a large share. **So the evidence that rank banding works
   is not evidence that weight banding works, and vice versa — and they are complementary, not
   substitutes.** The clean candidate applies both: a rank band on membership, a weight band on
   sizing.
3. **A free pre-check before spending a trial, which is the right first step.** On train data
   only, take any existing book's holdings schedule and compute what fraction of its charged
   turnover comes from re-sizing within a band of the width the formula gives. If that fraction is
   small, item 1 buys nothing and this vein closes cheaply; if large, item 1 is the cheapest
   turnover reduction available under v3 and does not touch the signal at all. This costs no
   trial, reads no holdout, and uses machinery `learnings.md` says the lab already has.
4. **An honest expectation, not a promise.** The welfare gain from optimal banding is of order
   λ^(2/3) against a *cost-blind* alternative, and v3's measured skills sit at about zero with 90%
   intervals of roughly ±0.33 (`learnings.md`, Protocol v3). A construction improvement of this
   kind reduces cost drag; it does not manufacture skill. If a book has no gross edge, banding its
   rebalances cannot give it one — the right claim for a hypothesis built on this is "recovers a
   known cost drag", and the v3 skill interval is wide enough that recovering a cost drag may not
   be separable from noise in a single trial. Judge it on the turnover and cost decomposition as
   well as on skill.

**Pitfalls.** (a) Trade to the band **edge**, not to target — trading to target is the fixed-cost
policy and throws away most of the benefit. (b) The per-name independent band ignores correlation
and is therefore conservatively tight; do not "fix" that by widening bands arbitrarily, since
that re-introduces a fitted parameter. (c) The asymptotic assumes small costs; for the 0.5%
stamp-duty names it is being used outside its proven regime, which is an argument for taking the
direction (wider) and not the exact multiple. (d) A weight band makes holdings path-dependent, so
the candidate's output depends on its own history — this is fine under v3's drift model but means
the causality check sees a path-dependent map; keep it deterministic. (e) γ is not a free
parameter to tune against validation.

## Related

- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — Gârleanu–Pedersen's
  aim portfolio and fixed-fraction partial move. **Read together with this note**: that is the
  *quadratic*-cost policy, this is the *proportional*-cost policy, and v3 charges proportional
  costs. The two are not variants of one idea; they are solutions to different problems, and the
  primer's §6.3 taxonomy is the authority for saying so.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — Novy-Marx–Velikov's
  banding/buy-hold spread and staggered partial rebalancing. Those are *empirically validated
  heuristics on score ranks*; this note supplies the *theory for the weight-space band and its
  width*. Novy-Marx–Velikov tell you banding pays; the primer tells you how wide and where to
  trade to.
- `notes/2026-10-08-securities-transaction-taxes-turnover-and-holding-period.md` (tonight) — the
  source of the per-name λ asymmetry that makes item 1 more than a restatement of "trade less".
  An STT's only adjustment margin is turnover; this note is how that margin is set optimally.
- `notes/2026-08-21-diversification-return-and-rebalancing.md` and
  `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the other half of the drift
  question: what is *given up* by letting weights drift away from equal. Those notes argue about
  whether the rebalancing "return" is real; this note is agnostic on that and prices only the
  displacement loss from the investor's own objective.
- `experiments/learnings.md` — the hysteresis-band entries (both the `mom_12m_buffered` success
  and the 52-week-high turnover blow-up) and the entry/exit-vs-re-sizing turnover decomposition.
  No contradiction with this note, because those bands are on rank and this one is on weight; see
  Implementability item 2, which is the most important caveat in this note.
