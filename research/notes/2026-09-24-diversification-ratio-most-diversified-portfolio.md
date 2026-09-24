---
title: "Toward Maximum Diversification — with: Properties of the Most Diversified Portfolio"
authors: Choueifaty, Coignard (2008); Choueifaty, Froidure, Reynier (2013)
year: 2008; 2013
venue: Journal of Portfolio Management 35(1), 40–51 (Tier 1 by this folder's rubric,
  practitioner-authored); Journal of Investment Strategies 2(2), 49–70 (Tier 3, minor
  peer-reviewed practitioner journal)
url: https://doi.org/10.3905/jpm.2008.35.1.40 ; https://doi.org/10.21314/jois.2013.033
citations: "Choueifaty–Coignard: 474 (Semantic Scholar by DOI, checked 2026-09-24); 430
  (Crossref is-referenced-by-count, checked 2026-09-24). Choueifaty–Froidure–Reynier:
  118 (Crossref by DOI 10.21314/jois.2013.033, checked 2026-09-24); Semantic Scholar's
  DOI endpoint returns 'not found' for that DOI and resolves only the SSRN preprint
  record (10.2139/ssrn.1895459, 20 on Crossref), which badly undercounts the article —
  the split-work index gap recorded on 2026-09-23 for Kan–Zhou, second instance. Both
  papers read in full from the authors' firm-hosted PDFs at `tobam.fr`."
sample_period: "2008 paper: December 1990 – February 2008 (tests start December 1991).
  2013 paper: the decade to 2011, MSCI World."
markets: "2008: S&P 500 and DJ Euro Stoxx Large Cap. 2013: MSCI World (~1,500 developed
  names; top half by market cap used, ~793 names on average), USD-converted."
tier: C
validation_overlap: false
published_post_2018: false
---

Tier C, and the reason is worth stating precisely because the two halves of this source
deserve different treatment. **The algebra is unimpeachable** — the diversification-ratio
decomposition and the MDP's core properties are theorems, proved in the 2013 paper's
appendices, and they cannot decay or fail to replicate. **The empirical case is a firm
publishing backtests of its own product**: no multiple-testing discussion, costs handled
by asserting that a deliberately high round-number cost assumption would not overturn the
ranking, and the comparison set chosen by the authors. This folder should take the
identities and the invariance argument and take nothing else. The tier reflects the
evidence, not the mathematics.

## Mechanism

**The diversification ratio.** For a long-only book with weights `w`, per-name volatilities
`σ_i` and portfolio volatility `σ(w)`:

    DR(w) = (Σ_i w_i σ_i) / σ(w)

the ratio of the *weighted average* of the parts' volatilities to the volatility of the
whole. It is ≥ 1 for any long-only book, equals 1 for a single name, and equals `√N` for
`N` equal-weighted independent names of equal volatility. `DR²` reads as an **effective
number of independent risk factors** the book is exposed to.

**The decomposition, and this is the part this lab should take away tonight.** The 2013
paper proves

    DR(w) = [ ρ̄(w)·(1 − CR(w)) + CR(w) ]^(−1/2)

with two explicitly separated terms:

- `ρ̄(w)` — the **volatility-weighted average pairwise correlation** of the holdings,
  `ρ̄ = Σ_{i≠j} (w_i σ_i)(w_j σ_j) ρ_ij / Σ_{i≠j} (w_i σ_i)(w_j σ_j)`;
- `CR(w)` — the **volatility-weighted concentration ratio**,
  `CR = Σ_i (w_i σ_i)² / (Σ_i w_i σ_i)²`, a Herfindahl index computed on *risk*
  contributions rather than on weights. It is 1 for a one-name book and `1/N` for an
  equal-risk book.

So a book's diversification is exactly two things — **how much the holdings replicate each
other, and how unevenly the risk is spread** — and the formula says how they trade off.
Two corollaries fall straight out: if correlations go to 1, `DR` → 1 whatever the
concentration; and if all pairwise correlations are *equal*, `DR` varies only through `CR`,
so maximising diversification reduces to minimising concentration.

**Why that matters here, specifically.** The 2026-09-23 nightly recorded its risk-bet
statistic's third consecutive miss and named the blind spot exactly: it is a Herfindahl
over *normalised* risk shares, "scale-free in the correlation level — it sees how risk is
divided, never how much of it there is", and resolved to print mean pairwise correlation
beside it. **That resolution is right and this decomposition is its closed form.** The
lab's statistic is (a normalisation of) the `CR` term; the number it decided to print
beside it is the `ρ̄` term; and the identity above is how the two combine into one
diagnostic. Trial #98's own numbers are the worked example: `CR`-like concentration flat,
`ρ̄` down 0.242 → 0.174, so `DR` must have risen — which is precisely the book-volatility
fall the risk-bet count failed to predict.

**The most diversified portfolio (MDP)** is then `argmax DR(w)` over long-only,
fully-invested `w`. It exists and is unique when the covariance matrix is definite, and it
has two equivalent characterisations that are more informative than the optimisation:

1. **Every name held by the MDP has the same correlation to it, and every name *not* held
   is more correlated to it than the held names are.** A name is excluded not because it is
   unattractive but because it is already represented.
2. **For any long-only portfolio `w`, `corr(w, MDP) ≥ DR(w)/DR(MDP)`.** The more
   diversified a book is, the more correlated it must be with the MDP — which is what makes
   the MDP the "undiversifiable" portfolio.

Property (1) is the cleanest statement in the literature of what a *membership* rule based
on co-movement is doing, and it is the same act trial #98 performed by a different route.

**Optimality.** Maximising `DR` is equivalent to maximising the Sharpe ratio **under one
explicit assumption**: that expected excess returns are proportional to volatilities
(equal ex-ante Sharpe ratios across single assets — "risk is homogeneously rewarded").
The authors are open that this is an assumption, not a finding. It is also the assumption
this repo's own evidence is least willing to grant, since its universe is survivors and its
volatility level is a known artifact.

## Construction recipe

**Estimation (2008 paper, which is the more explicit of the two):**

- Covariance from **250 days of daily returns**, re-estimated at each month-end; names with
  under 250 days of history excluded.
- Long-only, fully invested, plus a **4% cap on each name's risk contribution** and issuer
  weight caps.
- Their robustness claim, which is the useful one: **the hierarchy of correlations is far
  more stable than the level of correlations**, so books built from differently estimated
  covariance matrices come out similar, and changing the data frequency or the estimation
  window has little effect. They report that even a perfect-foresight covariance matrix
  produces only slightly different books. *Read as a licence for rank-based co-movement
  scores over level-based ones — which is how this repo already works.*

**Estimation (2013 paper), two additions that matter for a global universe:**

- **Non-synchronous closes are handled explicitly.** Markets in different time zones never
  trade simultaneously, but their offset is nearly constant; they estimate correlations
  with a "plesiochronous" estimator that accounts for the delay between observations. This
  is the same problem BAC solves with overlapping three-day returns
  (`notes/2026-09-24-betting-against-correlation-decomposing-beta.md`), reached
  independently by a different route. **Two independent sources treating a daily
  cross-market correlation estimate as biased unless corrected is the strongest form this
  folder's evidence takes.**
- When observations are fewer than assets the sample matrix is singular; they use the blunt
  fix of shrinking the correlation matrix halfway toward the identity.
- Semi-annual rebalance, cap and region constraints, and a turnover penalty calibrated so
  the penalised book stays within a fixed tracking error of the unpenalised one.

**The invariance properties** (2013, §4) are a construction *test* rather than a recipe,
and they are the part of this source with the most surprising bite on this repo's universe:

| | Duplication | Leverage | Polico |
|---|---|---|---|
| Equal-weight | No | No | No |
| Equal-risk-contribution | No | Yes | No |
| Minimum-variance | Yes | No | No |
| MDP | Yes | Yes | Yes |

- **Duplication invariance** — adding a second listing of an asset already in the universe
  must not change the book.
- **Leverage invariance** — a company levering or delevering must not change the weight
  allocated to its underlying business.
- **Polico invariance** — adding a *positive linear combination* of assets already in the
  universe (their own example: launching a long-only leveraged ETF on a subset) must not
  change the weights on the originals, because that exposure was already available.

## Robustness evidence (qualitative only)

- The decomposition, the core properties and the invariance results are **proved**, not
  estimated, and they hold for any definite covariance matrix.
- The empirical comparisons span a US, a Eurozone and a global developed universe, and
  cover more than one market cycle.
- **Everything else is weak.** The backtests are the authors' own product, compared against
  index alternatives they selected; there is no multiple-testing treatment; costs are
  addressed by an assertion that a generous round-number cost assumption preserves the
  ranking rather than by a cost model; and no independent replication of the empirical
  claims was located this session. The `DR`/`MDP` construction is also the subject of a
  commercial mandate, which is a reason for care rather than dismissal but is a reason.

## Implementability here

**The free diagnostic, and this file ranks it as tonight's most actionable output.**
Compute, for every candidate book and the champion, on train only and from the holdings
the lab already samples:

    ρ̄  = Σ_{i≠j} (w_i σ_i)(w_j σ_j) ρ_ij / Σ_{i≠j} (w_i σ_i)(w_j σ_j)
    CR = Σ_i (w_i σ_i)² / (Σ_i w_i σ_i)²
    DR = [ρ̄(1 − CR) + CR]^(−1/2)

and print all three beside the existing effective-risk-bet count. This costs no trial, no
holdout, and no new data: the 252-day trailing covariance in the 2026-09-23 journal entry
is already the input. It converts the nightly's resolution ("print mean pairwise
correlation beside it") from a habit into an identity with a **check**: `DR` computed from
the two terms must reproduce `weighted avg vol / book vol` computed directly, which is a
free correctness test on the lab's own covariance handling. Use the volatility-weighted
`ρ̄` above rather than an unweighted mean pairwise correlation — the unweighted version
does not satisfy the identity and will not reconcile.

**The ETF problem this repo has and the literature happens to answer.** 42 of ~140
instruments here are ETFs. A regional or broad ETF **is a polico** — a positive linear
combination of names already in the universe — and a regional ETF holding names also listed
individually is close to a duplication. The table above says that equal-weight and
equal-risk-contribution constructions are *not* invariant to either, and minimum-variance
is not invariant to leverage or policos. **Any breadth-style or risk-parity-style book this
lab builds over a mixed stock+ETF universe is therefore double-counting exposure by
construction, and the size of the error depends on the ETF/stock mix rather than on
anything economic.** This is a sharper statement of the same problem the 2026-09-22 rider
attacked with a within-type demean, and it argues the demean is a patch on a construction
that is not invariant, not a fix.

**As a book (scout, not challenger).** A long-only MDP on this universe is implementable —
250-day covariance, monthly rebalance, 25% cap — but it is an `n × n` objective and
`SUMMARY.md` #1's triage rule stands against it. The honest framing is that the MDP is the
*ceiling* the lab's cheap co-movement selectors are approximating: `E/Var` estimates one
spanning number per name, the MDP solves the full problem. If a scout is ever spent here,
the interesting measurement is not its Sharpe but **how much of the MDP's `DR` a one-number-
per-name selector captures** — which is a question about construction, answerable on train,
and the kind of result that transfers even when the book fails.

**Pitfalls.**

- **The equal-Sharpe assumption is the whole optimality argument** and this repo has
  reasons to reject it. Treat `DR` as a *diagnostic* the lab should print, and the MDP as a
  *benchmark*, not as an objective to promote into the seat.
- `ρ̄` is a weighted average over a full pairwise matrix. On 145 names with a 252-day
  window that is a heavily estimated object, though as a *summary statistic* rather than an
  optimisation input its estimation error is far less damaging — this is the same reason
  the lab's existing risk-bet count is tolerable.
- The `DR` identity is defined for long-only books with positive weights, which is this
  repo's only case. Do not apply it to a score, a signal, or a long-short leg.
- Non-synchronous closes bias `ρ̄` **downward** for cross-region pairs. A book that looks
  more diversified because it holds more foreign names may be partly measuring the calendar.
  The same 3-day-overlap correction the BAC note proposes applies here, and should be
  applied to the diagnostic before anyone reads a change in `ρ̄` as a finding.

## Related

- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — Meucci's
  PCA/torsion bet count, the other answer to "how diversified is this book". **The two are
  different objects and should both be printed**: Meucci's measure changes basis to
  uncorrelated principal portfolios and asks how evenly risk is spread across them; `DR`
  stays in the asset basis and factors the answer into a correlation term and a
  concentration term. Meucci's diagnosis of the weight-Herfindahl family — that it ignores
  volatilities and correlations entirely — is exactly the blind spot the 2026-09-23 nightly
  rediscovered empirically.
- `notes/2026-09-24-long-only-minimum-variance-composition.md` — the competing long-only
  objective; note that MV is *not* leverage- or polico-invariant by the table above.
- `notes/2026-09-24-betting-against-correlation-decomposing-beta.md` — the independent
  arrival at the non-synchronous-correlation correction, and the sorting (rather than
  optimising) route to the same co-movement bet.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — the other
  clustering-based long-only allocator in this folder.
- `experiments/learnings.md` [2026-09-23] — the risk-bet statistic's third miss and its
  named blind spot, which this note's decomposition closes.
