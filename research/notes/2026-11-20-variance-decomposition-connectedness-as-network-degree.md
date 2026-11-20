---
title: "On the network topology of variance decompositions: Measuring the connectedness of financial firms"
authors: Diebold, Yilmaz
year: 2014
venue: Journal of Econometrics 182(1), 119–134 (venue tier 1)
url: https://doi.org/10.1016/j.jeconom.2014.04.012 — read in full from the NBER working-paper version, https://www.nber.org/papers/w17490.pdf (1.3 MB, `pdftotext -layout` → 108 KB of clean text, 690 instances of `" the "`, no ASCII shift, zero `( )` dropout)
citations: 4708 (Crossref `is-referenced-by-count`, checked 2026-11-20)
sample_period: 1999–2010 (the empirical illustration; the paper's content is a method)
markets: 13 US financial-institution stocks (illustration only)
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full**: the connectedness-table construction, the generalized variance decomposition
definition, the section relating connectedness measures to network degrees, the three estimation
choices (reference universe, horizon, approximating model), the volatility-input discussion, and
the static and rolling applications. The crisis-period narrative in sections 4.2–4.4 was
deliberately **not** recorded: it is event commentary, which this folder's anti-lookahead policy
forbids, and nothing in it is needed for the construction.

Third note of the 2026-11-20 session. It is the **instrument** the other two rest on: the only part
of the `network momentum` vein that this repo could actually build, with the one identity that says
what a "centrality" number computed this way *is*.

## Mechanism

Not a return mechanism — a measurement. The paper's claim is that a **forecast-error variance
decomposition is a network**, and therefore that the whole apparatus of network statistics is
already available to anyone who has fitted a vector autoregression.

Fit a VAR to `N` series. The `H`-step-ahead forecast-error variance of series `i` decomposes into
the shares attributable to shocks in each series `j`. Collect those shares in an `N × N` table
`D^H = [d^H_ij]`. Then:

- **the off-diagonal element `d_ij` is a directed, weighted edge** from `j` to `i`;
- **the row sum over `j ≠ i` is the FROM-degree of node `i`** (how much of `i`'s forecast-error
  variance comes from others) — the paper's total directional connectedness `C_{i←•}`;
- **the column sum over `i ≠ j` is the TO-degree of node `j`** (how much of everyone else's
  forecast-error variance `j` supplies) — `C_{•←j}`;
- **the mean degree of the network is total connectedness `C`** — the same number whether computed
  to or from, because row sums and column sums have the same total.

The identity is the content: *total directional connectedness measures are exactly the from- and
to-degrees of the weighted directed network implied by the variance decomposition, and total
connectedness is exactly its mean degree.* A researcher who computes a VAR decomposition has
computed degree centrality, whether or not the word "network" is used. Three properties follow and
matter for anyone ranking a cross-section on such a number: the adjacency matrix is **weighted**
(edges in `[0,1]`), **directed** (`d_ij ≠ d_ji`, so `i`'s influence on `j` is a different number
from `j`'s on `i`), and **row-constrained** (rows sum to one, so the diagonal is `1 −` the
from-degree rather than zero).

Why the directedness is the whole point for this lab: a **contemporaneous correlation matrix** is
symmetric and can express no lead-lag at all. The VAR decomposition at horizon `H > 0` is the
minimal object that can distinguish a transmitter from a receiver. The paper notes that pairwise
connectedness may be small at short `H` and larger at long `H`, precisely because shocks reach `i`
only with a lag — so `H` is the knob that separates contemporaneous co-movement from propagation.

## Construction recipe

**The object `x`.** The illustration uses the **natural log of daily volatility** per name, not
returns. Logs are taken because volatilities are right-skewed and the generalized decomposition
invokes normality, and because volatilities are far more strongly serially correlated than returns
— which is what makes a VAR approximation informative at all. (The illustration estimates
volatility from intraday data; the 2021 peer-momentum paper that builds on this method substitutes
**GARCH on daily returns** for exactly that reason, and a daily **range** estimator is the third
option.)

**The approximating model.** A **VAR(3)** on the `N` log-volatility series, estimated on a
**one-sided rolling window of `w = 100` days** for the time-varying version, or on the full sample
for the static table.

**The decomposition.** The **generalized** (Koop–Pesaran–Potter / Pesaran–Shin) variance
decomposition, not a Cholesky one, because the generalized version is **invariant to the ordering
of the variables** while Cholesky directional measures can be ordering-sensitive. Its entries are
`d^gH_ij = σ_jj^{-1} Σ_{h<H} (e_i' Θ_h Σ e_j)² / Σ_{h<H} (e_i' Θ_h Σ Θ_h' e_i)`, with `Θ_h` the
moving-average coefficient matrices of the non-orthogonalised VAR and `Σ` the shock covariance.
Because generalized shocks are not orthogonal, **rows do not sum to one and must be rescaled**
(`d̃_ij = d_ij / Σ_j d_ij`) before anything is interpreted as a share or a weight. Skipping that
rescaling is the obvious implementation error.

**The horizon.** Anchored at **`H = 12` days**, with 6 and 18 also examined. The paper's own
guidance for a portfolio application is explicit and useful: *link `H` to the rebalancing period.*

**Degrees and centrality.** From-degree = rescaled row sum off-diagonal; to-degree = column sum
off-diagonal; net = to minus from. Eigenvector centrality and closeness require only the same
matrix.

## Robustness evidence (qualitative only)

- **The two degree distributions are shaped very differently, and only one of them has
  cross-sectional dispersion.** In the illustration the **from**-degrees are distributed tightly
  (a narrow band, with a steep survivor function), while the **to**-degrees are spread widely over
  a much larger range. The paper states it as a general observation about its table: *the spread of
  the from-degree distribution is noticeably less than that of the to-degree distribution* — names
  are much alike as **receivers** of shocks and highly differentiated as **transmitters**. The
  particular widths are one 13-name sector sample and should not be carried anywhere, but the shape
  is a construction instruction: **rank a cross-section on the to-degree or the net degree, never on
  the from-degree**, which may be nearly constant across names.
- **Total connectedness is robust to Cholesky ordering in the authors' experience; directional
  connectedness is not** — hence the generalized decomposition.
- Total connectedness is stable across window widths 75/100/125 days and horizons 6/12/18 days,
  with shorter windows noisier; the authors explicitly decline to call this "robustness", because
  connectedness at a 6-day horizon and at an 18-day horizon are *different objects* rather than two
  estimates of one.
- **The paper's sharpest warning, and it generalises past this method.** *"Connectedness
  measurements generally will not, and should not, be robust to choice of reference universe."*
  Centrality is defined only relative to the node set chosen: the same name is central in one peer
  group and peripheral in another, and there is no universe-free centrality number. A result that
  moves when the peer set is redefined is not thereby refuted — the object changed.
- Methodology honesty is high: the paper separates what is assumption from what is estimate
  (`C(x, H, A(L), M(θ))` carries every choice in the notation), says plainly that identification
  assumptions may fail and that reasonable people disagree, and that its normality assumption is an
  assumption. Replication status: the method is the base of a very large applied literature
  (4,708 Crossref citations), which is adoption rather than replication of a return claim — there
  is no return claim here to replicate.

## Implementability here

**Reachable, with one binding arithmetic constraint.** Everything needed is daily: a per-name
volatility series, a VAR, a matrix decomposition.

**The dimension arithmetic, which decides the design.** A VAR(`p`) on `N` nodes has `N²p`
coefficients, i.e. `Np` regressors per equation, and needs `w ≫ Np` observations per equation to be
estimable by OLS. At the paper's own settings (`p = 3`, `w = 100`) that caps `N` at roughly a dozen
— which is exactly the size of its illustration. The eligible panel here is **~1,000 names on a
typical validation date**, so a single system over the panel is not merely slow but **not
identified**: `N = 1000, p = 3` is three million coefficients. Three ways out, in order of
preference for this repo:

1. **Partition into peer groups and fit one small system per group**, which is what the
   peer-momentum paper does (49 industries, minimum 5 members). Here the partition would be
   **listing region / index**, giving systems of order 30–250 names — still too large for `w = 100`
   at `p = 3`, so pair it with (2) or (3).
2. **Shrink.** The high-dimensional extension is Demirer, Diebold, Liu & Yilmaz
   (*Journal of Applied Econometrics* 33(1), `10.1002/jae.2585`, **622** Crossref citations, checked
   2026-11-20), an elastic-net/LASSO VAR used on roughly a hundred nodes. **Not read — a named
   unobtained pointer**, and the one source to fetch if this vein is ever taken further.
3. **Lower `p` and lengthen `w`.** `p = 1` with `w = 500` daily observations makes `N ≈ 40` comfortably
   estimable by OLS and costs only the propagation structure beyond one lag; the horizon `H` still
   carries multi-day propagation through the moving-average representation.

**Runtime.** `program.md` allows ~60s per `generate_weights` call and the protocol calls it about
seven times per trial. Per group, the cost is one VAR fit (`O(N²w)` plus a `Np × Np` solve), `H`
matrix products of `N × N`, and one eigen-decomposition if eigenvector centrality is wanted — all
trivial at `N ≤ 50`, and all of it needed only **once a year** on the paper's own schedule, not at
every rebalance. The expensive part is the **per-name volatility model**: a GARCH fit per name per
year over ~1,400 names is the thing to measure before writing a candidate, and the cheap substitute
is a **range-based** estimator from the `high`/`low` panels
(`notes/2026-08-29-range-based-volatility-estimators.md`), which costs a rolling window and no
optimisation.

**Two pitfalls specific to this panel.** (i) Volume and foreign-holiday gaps: the input series must
be a real daily series per name, and `aux` volume is not forward-filled, so a region-partitioned
system has to be fitted on that region's own trading calendar —
`strategies/lib/calendar_peers.py` is the existing instrument for that. (ii) The reference-universe
warning bites hardest here: a point-in-time panel's node set **changes every year by construction**,
so a name's centrality series mixes genuine change with membership change. Any centrality
time-series claim on this panel needs the membership channel held fixed before it means anything —
the same confound `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` and
the 2026-10-26/27 price-history-depth entry already record.

**Pre-registration note.** If a candidate in this vein is ever written, the **first** free screen is
the one this note makes cheap: compute the directed decomposition's row weights and the equal
weights over the same peer set, and report their rank correlation. The decomposition is only worth
its runtime if that correlation is well below one.

## Related

- The return mechanism this instrument serves, and its placebo test — which bounds what the
  instrument is worth: `notes/2026-11-20-peer-momentum-influence-weighted-peer-returns.md`.
- Centrality used as a characteristic rather than a weight:
  `notes/2026-11-20-network-centrality-as-a-priced-characteristic.md`.
- The volatility inputs: `notes/2026-08-29-range-based-volatility-estimators.md`,
  `notes/2026-09-21-har-rv-volatility-cascade.md`,
  `notes/2026-09-21-panel-volatility-models-and-risk-targeting.md`.
- Where this folder has met eigen-decompositions of a cross-sectional second-moment matrix before,
  and the nulls that go with them: `notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md`,
  `notes/2026-10-06-absorption-ratio-eigenvalue-concentration.md`,
  `notes/2026-10-06-betaless-variance-decomposition-and-average-correlation.md`.
- The lead-lag objects the lab has already measured with an *undirected* neighbourhood:
  `experiments/learnings.md` 2026-09-25.
