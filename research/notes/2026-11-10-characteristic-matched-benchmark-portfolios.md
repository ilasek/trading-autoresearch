---
title: "Measuring Mutual Fund Performance with Characteristic-Based Benchmarks"
authors: Daniel, Grinblatt, Titman, Wermers
year: 1997
venue: Journal of Finance 52(3), 1035–1058 — venue tier 1
url: https://doi.org/10.1111/j.1540-6261.1997.tb02724.x
citations: 1560 (Crossref, checked 2026-11-10)
sample_period: quarterly holdings 1974-12-31 to 1994-12-31; style analysis over 1975–1994
markets: US — NYSE/AMEX/Nasdaq common stocks, with NYSE-based breakpoints
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The matched-**portfolio** form of the matched control, and the one whose matching dimensions include
**prior-year return**. Where Barber–Lyon match one firm to one firm, this paper matches every held
stock to a passive portfolio of stocks sharing its characteristics, and subtracts.

The motivating problem is squarely the one the [2026-11-09] handover named: a performance measure is
being computed on a book that was *selected on the very characteristic you are trying to price*. The
authors state it about mutual funds in a form that transfers verbatim — the earlier literature's
benchmarks "may not fully account for return anomalies, such as the size, book-to-market, and
momentum effects", and the favourable numbers earlier studies reported "may have been due to a
simple momentum screen in the selection criteria of the funds, rather than" any skill. Replace
"funds" with "candidate strategies" and "skill" with "skill over the equal-weight pool" and it is
this lab's measurement problem.

**The idea.** If the characteristics are what price the cross-section, then the correct benchmark
for a stock is *the return of other stocks with the same characteristics*, not a factor model's
fitted value. The paper is explicit that this is an assumption with content: the characteristic-based
approach "assumes that characteristics provide better estimates of expected returns than do factor
sensitivities", citing the companion Daniel–Titman work, and it notes that the approach is not
*inconsistent* with a covariance-based model but remains appropriate when such models are violated.

**The payoff is a three-way decomposition**, and this is the part the folder does not have anywhere.
A book's return above its characteristic benchmark splits into:

1. **CS — characteristic selectivity.** Did the book pick names that beat *other names with the same
   characteristics*? This is the part that survives the screen.
2. **CT — characteristic timing.** Did the book *shift weight into* a characteristic ahead of that
   characteristic paying? This is timing the style, not picking within it.
3. **AS — average style.** What does the book earn simply by *sitting in* high-premium
   characteristic cells? This is the static tilt.

The decomposition exists because selection, timing and tilt are three different claims that a single
"excess return over a benchmark" number silently adds together.

## Construction recipe

**The benchmark portfolios (the control group), from the paper's Appendix:**

- Formed **each July**, from all common stocks meeting the data requirements.
- **The triple sort is NESTED, not independent** — this is the detail that is easy to get wrong and
  it changes the design completely:
  1. Sort the whole universe into **quintiles on size** (market equity just prior to the formation
     date). Breakpoints are from **NYSE firms only**, set so that an equal number of NYSE firms
     falls in each of the five; AMEX/Nasdaq names are then included in the analysis and slotted in.
  2. **Within each size quintile**, sort into **quintiles on book-to-market** → 25 size/BM
     portfolios. (Their book-to-market is **industry-adjusted**: each firm's ratio less the
     long-term industry average, over 50 industries.)
  3. **Within each of the 25**, sort into **quintiles on the preceding twelve-month return** → **125**
     portfolios.
  Because each sort is run *inside* the previous one, every cell is populated by construction — a
  nested sort cannot produce the empty corners an independent 5 × 5 × 5 cut would.
- **The momentum sort uses the twelve-month return through the end of MAY** — i.e. one month short
  of the June/July formation date. The authors state the reason: the skip avoids bid-ask bounce and
  monthly return reversal. **This is a skip-month, and it is not optional.**
- Each cell's return is **value-weighted** and the portfolios are explicitly **buy-and-hold**. The
  authors' stated reason is to avoid "biases in computed returns from rebalancing" and to avoid
  putting too much weight on extremely small stocks. The first clause is the Barber–Lyon rebalancing
  bias, named here as a construction constraint on a benchmark portfolio.
- The grid is re-formed **annually**; each stock is **re-assigned to its cell each quarter**.
- Data requirements for inclusion: at least two years of accounting data, market-value data at the
  end of the preceding December and the preceding June, and **at least six monthly returns in the
  twelve months before formation** (so the momentum variable is computable).

**What is differenced.** For a stock `j` held with weight `w_{j,t−1}`, the benchmark-adjusted return
in month `t` is `R_{j,t} − R^{b_{j,t−1}}_t`: the stock's return minus the month-`t` return of the
cell it belonged to **as of `t−1`**. The CS measure is the weighted sum over holdings:

```
CS_t = Σ_j  w_{j,t−1} · ( R_{j,t} − R^{b_{j,t−1}}_t )
```

then averaged over months. The authors' worked example is worth repeating because it fixes the
timing convention: a fund holding IBM at the end of March has IBM's April return less the April
return of the portfolio that best matched IBM on **prior-year return, book-to-market and size** —
i.e. the match is struck on information available *before* the return being measured, and the
benchmark is a portfolio, so it does not need a surviving twin.

**The timing measure, and the trick in it.** CT differences the *same* stock's benchmark return
against itself at two weight vintages:

```
CT_t = Σ_j  ( w_{j,t−1} · R^{b_{j,t−1}}_t  −  w_{j,t−13} · R^{b_{j,t−13}}_t )
```

The second term uses the weight **and the cell assignment** from twelve months earlier. So CT asks:
how much of this month's characteristic exposure was *recently acquired*, and did the characteristic
pay this month? A book that drifted into high-momentum names just before momentum paid scores
positive CT; a book that always sat there scores zero CT and positive AS. **The one-year lag is the
construction's whole content** — it defines "recently" and is the knob.

**AS** is the residual of the three: what the book earns from its long-run average cell occupancy.

**Note on the source read.** A JSTOR scan of the complete article (pp. 1035–1058) from the first
author's own site, with no text layer; Sections II.A–II.C and the Appendix were read from rendered
page images. `file -b` reported this document as **10 pages** and `pdfinfo` as **25** — the latter is
correct, and had `file`'s number been trusted the Appendix above would have been recorded as
unobtained and the sort recorded as independent rather than nested.

## Robustness evidence (qualitative only)

- The design has been adopted widely enough that the benchmark return series are maintained as a
  public dataset by one of the authors, with a standing citation requirement — adoption is itself
  the replication evidence here, rather than a single independent re-run.
- The authors re-estimated their style classifications over five-year sub-periods and report the
  style assignments were consistent across them, which is a stability statement about the matching
  variables, not about any performance number.
- The approach is explicitly positioned against two alternatives measured on the same data (a
  past-weights benchmark, and factor-model intercepts), so the paper is a comparison of benchmark
  constructions rather than an advertisement for one.
- Qualitatively, the paper's own conclusion is that the persistence other studies attributed to
  manager skill is better explained by **momentum exposure** — i.e. the characteristic benchmark
  absorbed what a cruder benchmark had reported as selection ability. That is the mechanism-level
  claim; no magnitudes are carried.

## Implementability here

**This is the construction the lab is closest to being able to build, and the match to protocol v3
is unusually clean in one dimension and blocked in another.**

- **Momentum quintile: directly computable.** Prior-year return on each `eligible` name is a
  one-line causal computation from `prices`.
- **Size quintile: not available as stated.** Market value of equity needs a share count. `#408`
  establishes this panel has none and the back-adjusted price level is not a substitute (`#423`).
  The honest substitute is a **trailing dollar-volume quintile** — available from `aux`, causal, and
  a genuine liquidity axis — but it must be described as a liquidity match, not a size match.
- **Book-to-market: not available at all.** No fundamentals.

So the implementable version on this panel is a **2-D grid, not 3-D**: prior-year return × trailing
dollar-volume, say 5 × 5 = 25 cells, value-weighted inside each cell by dollar volume (there being no
capitalisation to weight by), re-formed on the lab's rebalance cadence with breakpoints taken from
the **eligible** panel on each date. Add **region** as a third axis only if the cells stay populated —
`#421` says a pooled cut across nine markets is partly a region bet, which argues for region-neutral
cells, while the cell-count arithmetic argues against (5 × 5 × 9 = 225 cells against ~1,000 eligible
names is about four names per cell, which is noise). **Measure the occupancy before choosing**: a
2-D grid with a region *control* applied afterwards is likely the better trade on this panel.

**Correction to the paragraph above, which the Appendix overturns — and the corrected version is
better for this panel, not worse.** The occupancy arithmetic assumed an *independent* 5 × 5 × 5 cut.
The sort is **nested**, so every cell is populated by construction and the empty-corner objection
disappears. The right build here is therefore three nested levels, not a 2-D grid with a bolted-on
control:

1. **Outer: region** (or listing market) — exact matching on a discrete variable, which `#421` wants
   anyway and which `#429` says is **free**, since discrete covariates do not count toward the
   continuous-covariate dimension that drives matching bias.
2. **Within each region: quintiles on trailing dollar-volume** — the honest substitute for the size
   sort, and it **must be described as a liquidity match, not a size match**.
3. **Within each of those: bins on the twelve-month return through one month before the formation
   date** — the skip-month is part of the construction, for the reason the authors give.

Choose the inner bin count from the **smallest region's** membership rather than the panel total,
and drop to terciles on the inner sorts where a region is thin. Weight within a cell by trailing
dollar volume, and hold each cell **buy-and-hold** between re-formations rather than restoring
weights — that is the authors' explicit choice and it is the same bias `#432` is about.

**The decomposition is the real prize, and it is free.** Any candidate the lab runs can have its
excess-over-pool split into the three pieces without a new trial:

- **AS** — what the book earns from *sitting* in a characteristic cell relative to the pool's cell
  mix. A large AS and a zero CS says the candidate is a static tilt wearing a signal's clothes. The
  lab has diagnosed exactly this by hand before (`learnings.md`'s "style tilt in costume" entry);
  CS/CT/AS is the general form of that diagnosis.
- **CT** — whether the book's *changes* in cell exposure anticipate when the cell pays. This is the
  component a genuine timing signal should load on, and it is the one no existing lab diagnostic
  isolates.
- **CS** — within-cell picking, which is what "skill" ought to mean once the characteristic grid is
  the benchmark.

Reported next to skill, this says **which of three different claims** a candidate's number is making.
It is a stronger version of the standing recommendation in `#425` (report realised beta next to
skill) and of `#413`'s pre-trial composition rule: both are about making a measured number say what
it is made of.

**Pitfalls, named.**

- **The CS benchmark is a different null from the equal-weight pool, and must not be reported as
  replacing it.** The pool is the gate's null and `engine/protocol.py` owns it. A characteristic-cell
  benchmark is a *diagnostic* — it answers "relative to names like these", which is a question the
  gate does not ask.
- **A momentum-matched benchmark will mechanically flatten a momentum candidate's measured skill to
  near zero, and that is the point, not a failure.** `price-trend` is the lab's most-worked family;
  running the folder's existing leads against a prior-return-matched benchmark would say how much of
  their measured skill is within-cell picking versus cell occupancy. It is also the exact design
  `#424` used to kill a comovement result, so a null there is informative.
- **Cell assignment must be struck before the return window and held**, exactly as the `t−1`
  subscript says. Re-assigning a name to the cell it occupies at the *end* of the measurement month
  is the standard lookahead and the lab's causality check would catch it.
- **Value weighting inside a cell is not optional for the stated reason** — the authors chose it to
  avoid rebalancing bias in the benchmark, which is the same bias `2026-11-10-control-firm-versus-reference-portfolio-biases.md`
  shows inflates an equal-weight benchmark. An equal-weighted cell return reintroduces it.
- **Do not import the quintile count.** Five cuts per axis is calibrated to a US cross-section of
  thousands; `SUMMARY.md`'s sorted-book cluster already holds the literature on how many bins a
  panel supports.

## Related

- `notes/2026-11-10-performance-matched-controls-and-mean-reversion.md` — matching on the selection
  variable; the single-firm form of the same design.
- `notes/2026-11-10-control-firm-versus-reference-portfolio-biases.md` — the argument that a matched
  *firm* beats a matched *portfolio* for test specification, and the rebalancing bias that forces
  value weighting inside a cell here.
- `notes/2026-11-10-matching-estimator-bias-and-the-dimension-of-the-match.md` — why moving from one
  continuous matching variable to three is not a free improvement in the match.
- `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md`,
  `notes/2026-08-17-momentum-horizon-echo.md` — the prior-year-return axis this grid matches on.
- `SUMMARY.md`, "The shape of a sorted book" — bin counts and monotonicity on a panel this wide.
