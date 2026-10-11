---
title: "It's All in the Timing: Simple Active Portfolio Strategies that Outperform Naïve Diversification" (primary NOT read; construction read from Bock 2018, a source this folder already covers)
authors: Kirby, Ostdiek (2012); construction and independent re-test from Bock (2018)
year: 2012
venue: Journal of Financial and Quantitative Analysis 47(2), 437–467 (venue tier 1, peer-reviewed). The restatement channel is arXiv:1811.08255, an unrefereed Warwick MSc thesis (venue tier 4), already covered on 2026-09-30 as a recipe source
url: https://doi.org/10.1017/S0022109012000117 · restatement read at https://arxiv.org/abs/1811.08255
citations: Kirby–Ostdiek 274 (Crossref is-referenced-by), 306 (OpenAlex), 261 (Semantic Scholar) — all checked 2026-10-11. Bock not indexed by Crossref or OpenAlex; DataCite reports 0 for its ResearchGate DOI (10.13140/RG.2.2.18539.80165), checked 2026-10-11
sample_period: Kirby–Ostdiek's own sample was NOT verified (paper not read). Bock's re-test is monthly, 06/1963 – 03/2018 (02/1995 – 03/2018 for the international dataset), rolling 240-month estimation window, one-month holding period
markets: Bock's six datasets — 10 US industry portfolios, 8 MSCI country indices + World, SMB/HML/UMD + MKT, 25 size × book-to-market portfolios, DJIA constituents, S&P 500 constituents (60 sampled per date)
tier: B overall, and the split matters — **A** on the rule's standing (tier-1 venue, ~300 citations, a named construction in the post-2009 literature), **C** on everything recorded here about its *performance*, because the primary is unread and the only independent evidence located is one unrefereed re-test that does not support it
validation_overlap: true — Bock's samples run to March 2018 and touch the first quarter of the lab's validation window. Kirby–Ostdiek's own window is unverified, so treat as overlapping until shown otherwise
published_post_2018: false (2012; the restatement is dated September 2018)
---

## Access

**The primary is closed and was not read.** `cambridge.org/core` serves an HTML bot page in
place of its PDF endpoint (recorded in `research/README.md`, 2026-09-18); OpenAlex reports
`oa_status: closed` with no repository location; `scholarship.rice.edu` answered a search
request with HTTP 202 and an empty body; the RePEc record (`cup/jfinqa/v47y2012i02p437-467_00`)
carries no file; both SSRN working-paper records are behind the usual Cloudflare challenge;
and an arXiv full-text search for `"reward-to-risk timing"` returns nothing.

One **new access finding** worth carrying, collected while chasing the long-only extension named
in the companion note (El-Hassan–Kofman 2003, *Australian Journal of Management*):
**`opus.lib.uts.edu.au` answers a `/bitstream/10453/<id>/1/<file>.pdf` request with HTTP 200 and
a 14 KB body by redirecting to `/password-login`.** It is another member of the "looks like an
answer" family and is caught only by reading `curl -w '%{url_effective}'`, not the status code.
The OpenAlex `locations` list for that article also names `www.qfrc.uts.edu.au/research/
research_papers/rp98.pdf`, which fails at the transport layer (`code=000`) — the UTS Quantitative
Finance Research Centre paper directory appears to be gone.

What was read is **Bock (2018)**, which states the reward-to-risk rule with its equation and
re-tests it. That source is **already covered** by this folder (it is the recipe channel in
`notes/2026-09-30-bayes-stein-shrinking-an-estimated-mean-vector.md`), so this note claims new
coverage for Kirby–Ostdiek only. Two consequences, both binding: **nothing here is attributed to
Kirby–Ostdiek's own argument**, only to their rule as a third party states it; and the paper's
*other* rule, **volatility timing, was not obtained at all** — do not implement it from this note.

## Mechanism

The diagnosis first, because it is the transferable half. Kirby–Ostdiek's reading of the
"nothing beats `1/N`" literature is that it is a **research-design** result rather than a result
about optimisation: the comparisons were run on datasets where estimation risk is high and the
optimised rules consequently take extreme positions and turn over violently, so transaction
costs do the killing. Their response is to build rules that (a) need **no name-level
expected-return estimate** and (b) therefore barely trade.

The substitution that makes this work is the mechanism: **replace the sample mean with a factor
loading.** A trailing beta is estimated far more precisely than a trailing mean — same data, far
less sampling variation — so a rule that puts *reward* in the numerator can keep a reward term
without inheriting the estimation error that destroys the Markowitz rule. Risk goes in the
denominator, as in the whole inverse-risk weighting family, and the two together make a
reward-to-risk ratio per name. Because the quantity is a ratio of slow-moving trailing
statistics, the weights move slowly, which is where the low turnover comes from — the turnover
reduction is a *property of the inputs*, not a constraint bolted on afterwards.

## Construction recipe

Reward-to-risk timing (`rrt`), as Bock states it:

```
w_rrt,t  ∝  (Σ_t⁻¹ β̄_t⁺)^ω ,  normalised to sum to one
β̄_i,t  = (1/K)·Σ_j β_ij,t        average loading of name i over the K factors
β̄_i,t⁺ = max(0, β̄_i,t)          a name with negative average beta gets zero weight
ω ∈ {1, 2}                       "timing aggressiveness"
```

Three mechanics carry over whatever factor model is used. *(a)* **The reward term is a loading,
not a mean** — the whole point. *(b)* **Long-only is enforced by truncation at zero**, not by a
constrained optimiser: a negative-average-loading name is simply dropped, which also makes the
rule's selection step explicit and auditable. *(c)* **`ω` is an aggressiveness exponent** and the
source pair uses small integers rather than fitting it.

One divergence must be flagged because it changes the rule materially. **Kirby–Ostdiek assume
the covariances are zero**, so `Σ⁻¹β̄` collapses to the per-name ratio `β̄_i/σ̂²_i` and no matrix
is inverted; **Bock keeps the full sample `Σ̂⁻¹`** for comparability with the other fifteen rules
he tests. The diagonal version is the cheap, stable one; the full-matrix version re-introduces
precisely the estimation problem the rule exists to avoid. On a thousand-name panel only the
diagonal version is computable at all — and, importantly, **the independent negative below was
measured on the full-matrix version**, so it is not a null on the rule as its authors defined it.

**The evaluation protocol is itself worth copying**, since it is the part a lab controls: rolling
estimation window, one-month holding period, investment restricted to the risky assets (factor
portfolios and the riskless asset excluded from the investable set), turnover defined as the
average sum of absolute weight changes across names, proportional costs of 50 bps per
transaction, and **return-loss relative to the benchmark** as the headline cost-aware statistic —
the extra return a rule would need to match the benchmark's post-cost Sharpe. A negative
return-loss is by construction a higher post-cost Sharpe than the benchmark.

## Robustness evidence (qualitative only)

- **The one independent re-test located does not support the rule.** Across six datasets Bock
  reports reward-to-risk timing below minimum-variance in most of them and *significantly below*
  `1/N` in one. He also reports, in the same exercise, that Tu–Zhou's mixtures fail to dominate
  `1/N` or minimum-variance, that unconstrained robust portfolios fall below minimum-variance in
  most datasets, and that short-sale constraints alone do not reliably help — i.e. the negative
  is not aimed at this rule in particular, it is the literature-wide finding that none of the
  post-2009 strategies consistently beats `1/N` or minimum-variance on Sharpe, certainty
  equivalent **or** turnover.
- **He contradicts a stated conditional, which is stronger than an unconditional null.**
  Kirby–Ostdiek argue the rule should beat `1/N` where the **cross-sectional dispersion of
  expected returns is large**; the individual-stock datasets have more return variation than the
  portfolio datasets, and the rule does not do better there. A conditional prediction failing on
  its own condition is the kind of negative that should be written into a hypothesis *before*
  running it.
- **The low-turnover claim survives even though the performance claim does not.** In the same
  re-test, mean-variance, Bayes-Stein and the unconstrained mixtures turn over substantially more
  than `1/N`, while `rrt` and the constrained rules turn over only slightly more. So the design
  goal was achieved; what is unsupported is that it pays.
- **Why the negative is Tier C and cannot close the rule.** Unrefereed, uncited, one author, one
  implementation of each competing rule (the full-`Σ̂⁻¹` choice can by itself account for the
  failure), sample covariance matrices only, and the author states that his significance tests
  assume i.i.d. returns while his own Ljung–Box results reject it. He also samples 60 stocks at
  random per date in the widest dataset, which inflates `1/N`'s own turnover. Read it as "the
  claim is fragile", never as "the mechanism is dead".
- **`validation_overlap: true`** on the re-test, and unverified on the primary. No magnitude,
  sign or ranking from either may enter a hypothesis.

## Implementability here

1. **The rule is buildable on this repo today, in its diagonal form, and it is cheap.** Everything
   it needs is present: an ETF id as a market proxy is explicitly allowed by the hindsight guard,
   daily closes give a trailing beta per eligible name, `β̄⁺/σ̂²` is causal, scale-free and needs
   no matrix inverse, truncation at zero makes the book long-only by construction, and a monthly
   rebalance of a slow-moving ratio is the kind of turnover v3's per-name costs and drift charges
   punish least.
2. **Two pre-registrations are mandatory.** `ω` **fixed at 1 before the first run** — the source
   pair uses small integers and the deflator charges for every scanned knob — and the
   **diagonal-covariance version only**, with the deviation from the re-tested full-matrix
   implementation declared in the journal, since that is the version the negative was measured on.
3. **A pre-registered failure condition exists and should be written down first.** The rule's own
   literature contains a direct negative on its stated edge condition. Write the hypothesis
   narrowly — "a long-only `β̄⁺/σ̂²` weighting of the eligible panel earns positive skill against
   the equal-weight pool" — and record the tension in the journal *before* the run, so the result
   is informative either way.
4. **It is a different object from this lab's existing inverse-risk legs.** Risk parity and
   volatility-managed overlays put `1/σ` or `1/σ²` alone in the weight; this puts a **reward
   numerator** over the same denominator, and the numerator is a *loading*, not a past return. It
   is therefore also distinct from the lab's momentum lineage: the selection step is "does this
   name co-move with the market at all", not "did it go up".
5. **What not to carry.** No performance expectation from either source. No volatility-timing
   construction (not obtained). And no assumption that "low turnover" means cheap *here*: the v3
   pool itself drifts and is itself rebalanced, so the cost comparison is against a moving
   benchmark on a per-name schedule with UK/HK/FR/IT/ES transaction taxes, which a flat-50-bps US
   study cannot settle.
6. **A free methodological import, independent of whether the rule is ever run.** **Return-loss
   relative to the benchmark** — the extra return a book needs to match the benchmark's post-cost
   Sharpe — converts a Sharpe gap into the units a cost argument is actually made in. The lab
   reports skill and skill at 2× costs; return-loss would make "it lost to the pool on costs"
   quantitative rather than rhetorical, and it costs nothing to compute from series the protocol
   already produces.

## Related

- `notes/2026-09-30-bayes-stein-shrinking-an-estimated-mean-vector.md` — where this folder first
  used Bock (2018) as a recipe channel, and the earlier instance of the same compromise (primary
  closed, estimator read from a third party).
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` — Tu–Zhou, whose
  mixtures the same re-test also fails to support; the two notes are the positive and the negative
  halves of one question.
- `notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md` — the ceiling on
  what any such rule could buy against a benchmark, and the reason not to minimise tracking error.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal, the result this
  rule was designed to answer.
- `notes/2026-08-18-risk-parity-equal-risk-contribution.md`,
  `notes/2026-08-17-volatility-timing-managed-portfolios.md`,
  `notes/2026-09-21-panel-volatility-models-and-risk-targeting.md` — the inverse-risk family this
  rule extends by adding a reward numerator.
- `notes/2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — the other place in
  this folder where a trailing beta is the estimated object; same estimation machinery.
