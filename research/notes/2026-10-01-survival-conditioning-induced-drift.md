---
title: "Survival"
authors: Brown, Goetzmann, Ross
year: 1995
venue: Journal of Finance 50(3), 853–873 (Tier 1)
url: https://doi.org/10.1111/j.1540-6261.1995.tb04039.x · read from the NYU Stern working-paper version FD-94-21, https://archivefda.dlib.nyu.edu/bitstream/2451/27218/2/wpa94021.pdf (title page reads "Forthcoming, The Journal of Finance", dated March 5, 1995)
citations: 373 (Crossref is-referenced-by-count, checked 2026-10-01); 306 (OpenAlex, checked 2026-10-01)
sample_period: "No estimation sample — the paper is analytic. Its numerical work is simulation (60,000 replications of weekly zero-mean Normal returns, annualised SD 0.20, holding periods from 4 weeks to 320 years) plus calibration illustrations."
markets: none estimated; the motivating institutional facts are the 20th-century histories of the world's equity exchanges
tier: A — Tier-1 venue, closed-form results, heavily cited, and the central claims are theorems rather than estimates, so there is nothing in them to decay
validation_overlap: false
published_post_2018: false
---

## Access

**Read in full** (the parts that matter: abstract, Section I's derivation, the long-horizon
variance-ratio result, the event-study and stock-split sections) from the **NYU Faculty Digital
Archive**, which hosts the Stern Finance working-paper series. The deposited file is a **scan with no
text layer** — `pypdf` returned 34 characters from 35 pages, and `pdftotext` returned 35 bytes — so it
was rendered to page images with `pdftoppm` and read visually.

Two tooling notes for the folder's recipe:

- **`pdftoppm` *is* installed in this environment.** `research/README.md` states (2026-09-08) that it
  is not, and that `pymupdf` is the workaround. That is now out of date:
  `pdftoppm -png -r 130 -gray <file>.pdf <prefix>` worked first time and needs no scratchpad install.
  `pdftotext` is also present. Neither helps on a text-layerless scan beyond confirming it *is* one —
  check `pdffonts`, which printed an empty font table here, as the one-command diagnostic.
- **The NYU Faculty Digital Archive (`archivefda.dlib.nyu.edu`) is a working channel** for pre-1996
  finance working papers, and it is reachable when `web.archive.org` is not. Find the handle through
  its own search endpoint (`/simple-search?query=...`), then read the `bitstream/2451/<id>/<n>/<file>`
  link out of the landing page. Note the mirror hostname `archive.nyu.edu` answered the *landing page*
  but not the bitstream; `archivefda.dlib.nyu.edu` served both.

## Mechanism

Every empirical result in finance is computed on a series that **was there to be computed on**. The
paper's move is to treat that as an explicit conditioning event and ask what it does to the
distribution of the conditioned process. The answer is a single formula with large consequences.

Let price follow `dp = μ dt + σ dz`, and let `A` be the set of paths that survive — the paper's
leading case is `A = {paths whose running minimum stays above a lower reservation level p̲}`. Write
`π(p,t) = Pr(A | p, t)` for the probability that a path currently at `p` survives. Then (Lemma 1, from
Karlin–Taylor, used by Ross 1987) the process **conditional on being in `A`** is itself a diffusion:

    dp* = μ* dt + σ* dz,      μ* = μ + σ² · (π_p / π),      σ* = σ.

Three features of that line carry everything:

1. **The induced drift is proportional to `σ²`.** Conditioning on survival does not add a constant —
   it adds a term scaled by the *variance* of the thing being conditioned. Volatile securities are
   dragged upward hardest.
2. **The diffusion coefficient is unchanged** (`σ* = σ`). Survivorship inflates the numerator of a
   Sharpe ratio and leaves the denominator alone. There is no compensating increase in measured risk
   to net it out against.
3. **The drift is local in the distance to the failure boundary.** With `μ = 0` and `T → ∞` the
   expression collapses to the clean form

        dp* = σ²/(p − p̲) dt + σ dz,

   so the induced return is **largest for names closest to the level at which they would have been
   removed** and decays hyperbolically as a name moves away from it.

With zero true drift the mean surviving path solves out in closed form:

    p̄_t = σ · sqrt( (p₀ + p̲)²/σ² + 2t ),

**increasing and concave in `t`, with the degree of concavity increasing in `σ`.** Concavity is the
second consequence: average return early in a surviving history exceeds average return late in it,
not because anything changed but because the conditioning binds hardest when the path is near the
boundary, which is at the start.

For a positive-drift process the authors solve the stationary problem directly:
`π(p) = 1 − exp(−2μ(p − p̲)/σ²)`, giving the compact statement

    μ* = μ + 2μ(1 − π(p)) / π(p),

i.e. **the observed mean exceeds the true mean by a factor governed entirely by the ex-ante survival
probability.** Their calibration illustration: a true equity premium of exactly zero shows up as an
observed premium of 8% against a 4% riskless rate when `π(p)` is 50% — "perhaps not unreasonable given
the number of stock markets that have survived the past 100 years."

The framework is not tied to the absorbing-barrier story. Any `A` works, and the paper does three
others:

- **`A` = paths that attain their maximum at a point `t*`** (Ross 1987): the mean path rises *at an
  increasing rate* up to `t*`. The authors' gloss is worth keeping verbatim — "the perils of data
  snooping extend even to preliminary curiosity."
- **`A` = paths whose terminal price exceeds the average of the path** (their stock-split case): the
  cumulative average excess return trends smoothly upward over the whole pre-event window and flattens
  immediately after. The entire pre-event "run-up" is manufactured by the selection rule.
- **Event windows with a scheduled announcement**: a rise at one announcement implies a
  *first-order stochastic* increase at every **later** one within the surviving sample. Conditioning
  on survival induces **positive serial dependence across periods** in the survivors.

## Construction recipe

There is no strategy to build here; what the paper supplies is a **null** and a set of quantities to
compute against it.

- **The survivorship drift as a function of two observables.** Given a name's volatility `σ` and its
  distance from a plausible delisting/exit level `p − p̲`, the induced annual drift under zero true
  drift is `σ²/(p − p̲)`. This is a per-name number that needs no return data beyond the volatility
  estimate, and it is monotone increasing in `σ` and decreasing in distance-to-failure.
- **The long-horizon variance-ratio floor.** For the absorbing-barrier case with zero drift, the
  variance of holding-period returns per unit time, `ω[T]`, is everywhere decreasing in the holding
  period `T`, starts at the unconditional `σ²`, and converges to

        lim(T→∞) ω[T] = ((4 − π)/2) · σ²,

  i.e. **a variance ratio of (4 − π)/2 ≈ 0.4292**, independently of `σ` and independently of how far
  the starting price sits from the barrier. Read as a null: a survivor-selected panel is expected to
  show a long-horizon variance ratio materially below one — "substantial mean reversion will be
  evident for any stock return history that has survived, so long as the investigator studies a
  sufficiently long holding period" — with no mean reversion present in the data-generating process.
- **What the constant does and does not cover.** The `(4−π)/2` figure is derived for zero drift and a
  *fixed* barrier. It extends trivially to a barrier that rises at exactly the drift rate. The authors
  state plainly that they could not obtain analytic results when the barrier rises at a rate differing
  from the expected return, or when survival depends on the price relative to its **previous maximum**
  — those cases are handled by simulation, and the paper's own simulation design (weekly zero-mean
  Normal returns at annualised SD 0.20, holding periods 4 weeks to 320 years, 60,000 replications) is
  the template for extending it.

## Robustness evidence (qualitative only)

- The central results are **theorems**, derived from the Karlin–Taylor conditioning lemma and
  Ross (1987), not estimates. They cannot decay, and replication status is not the right axis to grade
  them on — what can be wrong is the *applicability* of the diffusion-plus-absorbing-barrier
  idealisation, not the algebra.
- The paper is explicit about the limits of the closed forms: the direction **and** magnitude of the
  long-horizon bias are "sensitive to the choice of return horizon, the ex ante viability of the
  exchange in question, and to the criteria for survival." The `(4−π)/2` limit is the one case where
  the criteria are simple enough to solve; elsewhere the sign is still determined but the size is not.
- The authors note the honest gap in the other direction too: the empirical long-horizon
  variance-ratio literature they cite does not report ratios anywhere near as low as `(4−π)/2`, which
  is evidence that real survival criteria are weaker than a hard absorbing barrier — the theorem
  bounds a direction, not an observed magnitude.
- The framework has been applied by the same authors across several distinct conditioning sets
  (market survival, event studies, stock splits, the maximum-attainment case), which is the relevant
  form of robustness for an analytic result: one mechanism, several unrelated empirical settings.

## Implementability here

Nothing here becomes a candidate. This note is a **discount function and a null**, and it is the
closest thing in this folder to a theory of the lab's single most-measured artifact.

**The direct hit.** `experiments/learnings.md` records, from this repo's own data, a
high-minus-low volatility spread of **+19.4%/yr on train**, a raw Garman–Klass volatility-level IC of
**+0.0766 (t = +5.75)**, and the conclusion that "the level *is* the survivorship artifact" — reached
inductively, across fourteen mechanism screens, with no theory attached. **This paper is the theory.**
A universe built from today's constituents is exactly a survival-conditioned sample; the conditioning
adds a drift proportional to `σ²` and leaves `σ` untouched; therefore a positive cross-sectional
relation between volatility level and realised return is **what a survivorship-selected panel must
show even when no such relation exists in the population.** The lab's measured artifact is the
literature's theorem. Three things follow:

1. **The lab's refusal to trade the volatility level is now over-determined, not merely empirical.**
   The lab's repeated decisions to decline `range-variance` candidates built on a cross-sectional
   volatility level were made on measured grounds. They do not need re-litigating, and a future
   session should not treat "we only measured it, we never explained it" as an opening.
2. **The artifact is predicted to be concentrated in the names nearest to exit**, because the drift
   goes as `1/(p − p̲)`. This repo cannot observe `p̲`, but it has proxies that order names by
   distance-to-failure — price level, illiquidity, drawdown from a long high. A free diagnostic: sort
   on a distance-to-failure proxy *within* volatility bucket and check whether the volatility-level IC
   concentrates in the near-boundary tercile. If it does, the survivorship account is corroborated by
   a second, independent implication of the same formula. If the IC is flat in distance-to-failure,
   the account is incomplete and something else is carrying the level effect.
3. **It is a `σ²` scaling, which means the artifact is a *variance* effect, not a volatility effect.**
   Any screen the lab builds against it should be specified on squared volatility, and a de-levelling
   that is linear in `σ` is not the right de-levelling. The lab's within-name de-levelled range
   volatility came back a clean null (IC +0.0087 / +0.0132), which is consistent — but it tested
   *removal* of the level, not the functional form of the inflation.

**The second hit, and it is the uncomfortable one.** The event-study result —  a rise in one period
implies a first-order stochastic increase in **later** periods within the surviving sample — says that
survivorship conditioning manufactures **positive cross-period dependence**, which is the signature of
continuation. This repo's champion is a cross-sectional momentum rule run on a current-constituent
universe. The paper does not say momentum is an artifact; it says a survivor-selected panel has a
continuation component that is there by construction, of unknown size. That is a reason the
`survivorship-pit-v2` branch's re-scoring of the seated champion under a point-in-time universe
deserves to be taken seriously on mechanism grounds rather than dismissed as a harness quirk — and a
reason the human's cutover decision (`experiments/journal.md`, 2026-09-29 and 2026-09-30) is the
highest-value open item in the repo.

**Two cautions on the cutover itself, both from this paper.**

- A point-in-time *membership* fix removes the `A = {in the index today}` conditioning. It does
  **not** remove the `A = {price history exists and is continuous}` conditioning, which is the one the
  paper is actually about. Names whose series simply stop are still absent from the panel unless their
  exit return is supplied. The bias direction is unchanged; only its size falls.
- The `(4−π)/2 ≈ 0.4292` variance-ratio limit is a free, parameter-free **falsifier for the fix**. If
  the lab ever computes long-horizon variance ratios on the current panel and on a point-in-time
  panel, the current one should sit lower. This is a diagnostic on the *data*, not a trial, so it
  costs nothing against the deflator — but it reads the panel, not the holdout, and it belongs to the
  strategy agent, not here.

**Pitfalls.** (i) The closed forms assume a fixed barrier and zero (or exactly-matched) drift; this
repo's universe is selected on *relative* capitalisation rank, which is the paper's harder,
unsolved case. Use the formulas for sign and ordering, not for magnitude. (ii) The illustrative
equity-premium calibration is a century-scale market-level statement and has no bearing on any
cross-sectional result here; do not import it. (iii) Nothing in this note licenses a *trade* on the
survivorship artifact — the lab has stated repeatedly that spending a trial to build on it would be
knowingly building on hindsight, and this paper strengthens that position rather than weakening it.

## Related

- `research/notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the **other half** of
  the same problem and the natural companion. That note covers selection on *end-of-period ranking*
  (Daniel–Sornette–Wöhrmann; Cai–Houge), measured by matched portfolios; this one covers selection on
  *continued existence*, derived analytically. The stock-split case here (`A = {p_T > path average}`)
  is formally the same object as that note's look-ahead selection, which is why both produce a smooth
  pre-period run-up that flattens at the selection date.
- `research/notes/2026-10-01-discovery-sample-and-anomaly-decay.md` (this session) — a third
  conditioning set: selection on *the sample in which the effect was found*. Survival, end-of-period
  rank and discovery-sample selection are three instances of one operator.
- `research/notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` — the cross-sectional
  return distribution this conditioning acts on.
- `experiments/learnings.md`, the `range-variance` entries (notably 2026-09-01 onward) — the lab's
  own measurement of the artifact this paper derives.
- `experiments/journal.md`, the `## Protocol issue` entries of 2026-09-29 and 2026-09-30 — the
  point-in-time cutover decision this note bears on.
