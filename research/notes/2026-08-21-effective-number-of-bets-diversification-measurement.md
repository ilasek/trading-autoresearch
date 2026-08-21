---
title: "Managing Diversification (effective number of bets) — with: How many independent bets are there?"
authors: Meucci; Polakow & Gebbie
year: 2009; 2008
venue: Risk magazine 22(5) (tier 3, credible practitioner, refereed by the magazine); Journal of Asset Management 9 (tier 3, minor peer-reviewed practitioner journal)
url: https://ssrn.com/abstract=1358533 ; https://doi.org/10.1057/jam.2008.26 (preprint arXiv:physics/0601166)
citations: "Meucci 2009: not indexed (Semantic Scholar DOI endpoint on 10.2139/ssrn.1358533 → not found; Semantic Scholar title search → HTTP 429 on three attempts; OpenAlex → daily budget exhausted; Crossref → no record, checked 2026-08-21). Its follow-up, Meucci–Santangelo–Deguest, resolves at 27 (Crossref, 10.2139/ssrn.2276632) and 16 (Semantic Scholar, checked 2026-08-21). Polakow–Gebbie: 12 (Semantic Scholar, checked 2026-08-21); 7 (Crossref)"
sample_period: "Meucci: no historical study — illustrations only, on a 30-stock mid-cap example with an exponentially smoothed daily covariance. Polakow–Gebbie: ~4.3 years of daily data from March 2003"
markets: "Meucci: illustrative US mid-caps (Russell 3000 subset). Polakow–Gebbie: South Africa — 41 liquid JSE equities, 7–8 government bonds, cash, property, international bonds and equities"
tier: C (Meucci's construction is algebra and cannot decay, but neither source carries an empirical study that meets this folder's bar; the venue tier, citation counts and sample breadth are all weak)
validation_overlap: false
published_post_2018: false
---

Full text read directly for both: the SSRN/`top1000funds` mirror of Meucci's article (dated
September 2010, of the piece published as *Risk* 22(5):74–79), and the arXiv preprint of
Polakow–Gebbie. The follow-up that fixes Meucci's main technical weakness —
Meucci–Santangelo–Deguest, *Risk Budgeting and Diversification Based on Optimized Uncorrelated
Factors* (minimum-torsion bets) — **was not read** (SSRN served a bot challenge); it is
mentioned below only as a known refinement, never as evidence.

## Mechanism

Both sources attack the same measurement error: **counting positions is not counting bets.**

**Meucci — the effective number of bets.** In an uncorrelated market, variances are additive
over positions and maximum diversification is equal variance-adjusted weights. In a correlated
market they are not, and the standard measures (percentage of risk explained by systematic
factors; weighted sum of position volatilities minus portfolio volatility; Herfindahl indices
on *weights*) all fail — the weight-based ones because they ignore volatilities and
correlations entirely, and none of them localises *where* the concentration is. The fix is to
change basis to something that *is* additive:

1. Eigendecompose the return covariance, `E'ΣE = Λ`. The columns of `E` are the **principal
   portfolios**; their returns `R̃ = E⁻¹R` are uncorrelated by construction and their variances
   are the eigenvalues.
2. Re-express the book in that basis: `w̃ = E⁻¹w`.
3. Form the **diversification distribution**
   `p_n = w̃_n² λ_n / Var(R_w)`, `n = 1…N`.
   These are non-negative and sum to one, so they are probability masses. Meucci proves `p_n`
   equals the **R² of a regression of the total portfolio return on the n-th principal
   portfolio** — it is a genuine share of risk, not a normalised marginal contribution.
4. Summarise the distribution's dispersion by its **exponentiated entropy**:

   ```
   N_Ent = exp( − Σ_n p_n ln p_n )
   ```

   `N_Ent = 1` when all risk comes from a single principal portfolio; `N_Ent = N` when risk is
   spread evenly. It is read as *the number of uncorrelated bets the book actually holds*.

**The conditional version is the one that matters for a constrained book.** The first principal
portfolio is essentially "the market". For a fully-invested equity book the **budget constraint
alone fixes the exposure to it** — Meucci shows this explicitly for a single-sector portfolio,
where the budget constraint fully determines the first exposure and has no effect on the
others. So the *unconditional* `N_Ent` of any fully-invested long-only book is dominated by a
term the manager cannot act on, and will look bad for a reason that is not a choice. The
actionable statistic drops the first `K` masses and renormalises,
`p̃_n = p_n / Σ_{m>K} p_m`, giving a **conditional** effective number of bets over the
directions actually available. Generally, when constraints restrict rebalancing to directions
satisfying `A·Δw = 0`, the principal portfolios are replaced by *conditional* principal
portfolios computed inside that subspace.

**Polakow–Gebbie — the same point aimed at the fundamental law.** Their two lemmas are
"independence is not separateness" (the `√N` in `IR ≈ IC·√N` counts *independent* bets, and
practitioners substitute the count of *separate* positions) and "skill does not scale over
breadth" (there is no reason for the IC to stay constant as the universe widens into
instruments the forecaster understands less well; IC is an average over bets and needs
disaggregating before it is scaled). Their estimator of independence is deliberately crude:
take the SVD of the return matrix and count eigenvalues `≥ 1` of the correlation matrix
(the **Kaiser–Guttman** stopping criterion); that integer is the effective dimensionality, and
it replaces `N` in the fundamental law. They note the entropy-based alternatives exist and
warn that many entropy formulations presuppose independence among the states they are counting
— the exact problem Meucci's change of basis is designed to avoid.

## Construction recipe

Holdings-and-covariance diagnostics, not strategies.

**Effective number of bets (Meucci):**
```
Σ  = trailing covariance of instrument returns
Σ  = E Λ E'                       # eigendecomposition, eigenvalues descending
w̃  = E⁻¹ w                        # exposures to principal portfolios
p   = (w̃² * λ) / (w' Σ w)         # diversification distribution, sums to 1
N_Ent      = exp(-Σ p ln p)                          # unconditional
N_Ent|K=1  = exp(-Σ_{n>1} p̃ ln p̃),  p̃ = p_{n>1}/Σp_{n>1}   # conditional on the market leg
```
Benchmark-relative variant: replace `w` by `w − b` throughout; `p` becomes the tracking-error
concentration and `N_Ent` the effective number of *relative* bets.

**Effective dimensionality (Polakow–Gebbie):** correlation matrix of the candidate universe's
returns → eigenvalues → count those `≥ 1` → that count is the breadth `N` to put under the
square root, rather than the instrument count.

## Robustness evidence (qualitative only)

- **Meucci's contribution is derivation, not evidence.** The identity `Σ p_n = 1`, the R²
  interpretation, and the `1 ≤ N_Ent ≤ N−K` bounds are algebra and cannot decay. There is no
  historical study in the paper — only worked illustrations on a 30-stock example. Nothing
  here has been replicated because there is nothing empirical to replicate.
- **Polakow–Gebbie's evidence is thin and single-market**: one emerging market, roughly four
  years of daily data, 41 stocks. Its qualitative findings are (a) effective dimensionality is
  far below the instrument count — their 41-stock universe supported no more than eight
  dimensions, so effective breadth was about half what `√41` would suggest; (b) adding a whole
  extra *asset class* (seven to eight government bonds) raised effective dimensionality by
  about one, because the same macro drivers move both; (c) diversification "opportunities may
  be both limited and overstated". Direction, not magnitude, is what survives from this.
- **Methodology honesty**: Meucci publishes documented reference code; Polakow–Gebbie chose
  their estimator explicitly "for ease of replication". Neither models transaction costs.
  Neither discusses multiple testing, and neither needs to — no strategy is being selected.
- **Known technical weakness, acknowledged by its own literature**: principal portfolios are
  eigenvectors of an *estimated* covariance, and are unstable and hard to interpret. Meucci
  lists random matrix theory among the paper's own keywords, and the follow-up work on
  **minimum-torsion bets** exists precisely to replace principal components with a set of
  uncorrelated factors that stay close to the factors the manager actually allocates on. Not
  read this session; flagged so nobody treats PCA-based `N_Ent` as the settled version.
  Kaiser–Guttman is likewise an arbitrary cutoff, known to be crude in its own literature.

## Implementability here

This is the folder's open question (b) — *effective number of bets / effective
dimensionality, worth exactly one session* — and the session's verdict is: **the axis yields
one real correction and one real screen, from tier-C sources, and should now be closed.**

1. **The lab's existing "effective bets" number is not this object, and the difference has a
   sign.** `learnings.md` records the champion at "13.3 effective bets by weight against 6.0 by
   risk", the risk figure coming from the marginal risk-contribution vector `x_i · ∂_i σ(x)`.
   Meucci's specific criticism is of exactly that construction: risk contributions of
   *correlated* assets are marginal, not additive, so a Herfindahl-type count over them is not
   a count of anything uncorrelated. `N_Ent` counts uncorrelated sources. The lab should either
   compute `N_Ent` or relabel its statistic as a correlated-contribution count. Note the likely
   direction: changing basis usually finds **fewer** independent bets than a contribution
   count, so 6.0 is more likely an over- than an under-statement.
2. **The conditional version is the one to compute, and this is free.** A fully-invested,
   long-only, ~145-instrument equity book has its first-principal-portfolio exposure pinned by
   the budget constraint. An unconditional `N_Ent` on the champion will therefore be low for a
   reason no candidate can change, and would make every future construction look equally
   undiversified. `N_Ent` conditional on `K=1` measures the part the strategy controls. This is
   a strict improvement to a diagnostic the lab already runs, needs no new data, and scores no
   returns — it is covered by the holdings-only exemption on the same footing as the existing
   risk-contribution vector. Per the companion note this session, a plain trailing sample
   covariance is the right input; no factor model or shrinkage estimator is warranted.
3. **A free pre-trial screen for any breadth-widening proposal.** The folder currently says the
   `N` lever is saturated *because 145 is a large number*. Polakow–Gebbie say that is the wrong
   reason: what saturates is **effective dimensionality**, which stops rising long before the
   instrument count does, and which barely moved in their case even when a whole new asset
   class was added. The corrected statement — stronger, and testable before a trial — is that
   widening the basket inside this universe adds no *eigen-directions*, so it cannot raise `N`
   in the fundamental law. Concrete screen: count the correlation eigenvalues `≥ 1` of the
   current universe; if a proposed instrument set does not raise that count, breadth widening
   is a no-op on paper. This retro-predicts the lab's measured no-op from basket-breadth
   widening, and — importantly — it predicts the same for the buffer-band vintage axis, which
   was killed for free at 0.963 weight overlap.
4. **Honest counterweight, recorded rather than smoothed.** If effective `N` here is genuinely
   small (their emerging-market book collapsed 41 names to ~8 dimensions), then in
   `IR = mean(IC)/sqrt(σ_IC² + φ/N)` the term `φ/N` is **not** negligible against `σ_IC²`, and
   the folder's claim that "the `N` lever is saturated" is doing more work than the algebra
   supports. What is saturated is the ability to raise `N` *within this universe*; the term
   itself may still be live. The two readings differ in what they license: the first says stop
   thinking about breadth, the second says breadth is unreachable rather than exhausted. Prefer
   the second — it is the one the sources support — and note that neither opens a build, since
   the repo's instrument list is fixed.
5. **What must not be imported.** Meucci's actual proposal is the **mean-diversification
   efficient frontier**: maximise `N_Ent(w)` subject to a return floor. That is an optimiser
   over an estimated covariance's eigenstructure — the most estimation-hungry object this
   folder has yet seen, and it is closed here by screen #1 and by the ERC theorem before it is
   a candidate. Take the measurement, decline the objective. This is the same split as the
   risk-contribution entry in `learnings.md`: the diagnostic that reveals a problem does not
   license the optimisation that would create a worse one.

## Related

- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the `N` term this sharpens
  and partly puts under tension.
- `notes/2026-08-18-risk-parity-equal-risk-contribution.md` — where the risk-contribution
  vector `x_i ∂_i σ(x)` entered this folder; point 1 is a correction to how it is being read.
- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — why a plain trailing
  covariance suffices as the input, and why constraints pin the first principal exposure.
- `notes/2026-08-21-diversification-return-and-rebalancing.md` — the return-side consequence of
  the same quantity: a book whose risk collapses onto few principal portfolios also has little
  `σ_i² − σ_ip²` to harvest.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — why point 5 declines the frontier.
- `experiments/learnings.md`, "Weight concentration is not risk concentration" and "A vintage
  axis is only a vintage axis if its members disagree about membership".
