---
title: "The Power of Tests for Detecting p-Hacking"
authors: Elliott, Kudrin, Wüthrich
year: 2025
venue: "Review of Economics and Statistics (Tier 1), DOI 10.1162/rest.a.1688. Read in full from the arXiv version (arXiv:2205.07950v4, 11 August 2025); previously circulated as \"(When) Can We Detect p-Hacking?\" Editor: Peter Hull, three referees."
url: "https://doi.org/10.1162/rest.a.1688 (read from https://arxiv.org/pdf/2205.07950)"
citations: "1 (Crossref, checked 2026-11-19) — the Crossref record carries a December 2025 publication date, so the count reflects recency, not reception. Graded on venue, on the fact that it is the power companion to a paper with 66 Crossref citations, and on a replication package the authors publish at github.com/nvkudrin/pHackingPower."
sample_period: "No market estimation window. Theory plus Monte Carlo (5,000 draws per design, nominal level 5%), with an empirical illustration on literature corpora of reported test statistics."
markets: "None. The object is a set of test statistics, not an asset panel."
tier: "A− — Tier-1 venue, theory plus a large simulation study, published replication package, and the headline finding is a negative one about the authors' own earlier tests. The minus is for the citation count being uninformative at this age."
validation_overlap: false
published_post_2018: true
---

## Access

`arxiv.org/pdf/2205.07950` served the complete paper first try (HTTP 200, 6.1 MB, 17 pages by `file`,
`pdftotext -layout` into 257 KB of clean text, 1,020 `" the "`, zero `( )` dropouts, right title on
line 1). The published venue was resolved with
`api.crossref.org/works?query.bibliographic=<title+authors>` — a **title-plus-author bibliographic
query is the right call when a paper's journal version is newer than its preprint**, because the
preprint names the editor but not the journal.

## Mechanism

The companion to `notes/2026-11-19-the-null-shape-of-a-set-of-ones-own-p-values.md`, and the half
that decides whether the folder's standing aim is worth anything. The first paper characterises the
null; this one asks **what power a test of that null actually has**, and the answer is the aim's
conclusion.

The mechanism is simple and it is the thing to carry away. A researcher with several admissible
specifications holds a set of candidate `p`-values `{P1, P2, P3, …}` drawn from a joint distribution
that depends on the true effect `h` and on the data — *not* freely chosen. Searching means applying
a **selection function** `Pr = d(P1, P2, P3, …)`. Power against a search therefore depends entirely
on the functional form of `d(·)`, and the authors are explicit that "it is not the case that
researchers can select any `p`-value they desire."

They study two selection functions, and the two have **completely different detectability**:

- **Threshold.** `Pr = P1·1{P1 ≤ α} + min{P1, P2, …}·1{P1 > α}` — report the preferred specification
  if it clears the target `α`, otherwise go looking. This is the "intuitive" form the earlier
  literature had in mind. It puts a **discontinuity** at `α`, violates the **upper bounds**, and
  sometimes violates **monotonicity**. It is detectable.
- **Minimum.** `Pr = min{P1, P2, …}` — report the smallest. This shifts the whole curve left while
  leaving it monotonically non-increasing and continuous. **Tests for non-increasingness and for
  discontinuities have no power against it, by construction, irrespective of the fraction of
  researchers who do it.** Only the upper-bound restriction can be violated.

The second mechanism worth naming is the role of **correlation among the candidates**. The authors
map Simonsohn's "slow" and "fast" p-hacking onto it directly: slow p-hacking is the case where the
candidate `p`-values move little across specifications, i.e. where they are **highly positively
correlated**; fast p-hacking is where they are **less dependent**. How much a search can move the
reported statistic is therefore a property of the dependence among the things searched over.

## Construction recipe

Not a strategy recipe — a test-selection recipe, plus the diagnostic question to ask before choosing
a test.

**Step 1: write down your own `d(·)`.** Everything follows from it. The paper's whole argument is
that "power against p-hacking" is not a property of a test; it is a property of a (test, selection
function, effect distribution) triple.

**Step 2: pick the test from `d(·)`.** The simulations (5,000 draws, nominal 5%, power traced against
the fraction of searchers `τ`, over designs covering control-variable selection in linear
regression, instrument selection in IV, and standard-error selection by lag length and clustering
level) give a clear ordering:

- **CS2B — monotonicity restrictions *and* upper bounds combined — has the highest power overall**
  and is the recommended default.
- Among monotonicity-only tests, **CS1 beats LCM**. LCM can have **non-monotonic power curves**,
  because its statistic converges to zero in probability for strictly decreasing `p`-curves
  (Beare–Moon 2015) — a real pathology, not a simulation artifact.
- **Discontinuity tests are a complement, not a substitute**: they are the strongest instrument
  where the search targets a threshold, and they are the natural partner to the bound tests.
- **The classical Binomial test on `[0.04, 0.05]` — the one the original `p`-curve literature uses —
  often has no or low power.** The authors' diagnosis generalises past this one test: a test that
  "only exploit[s] testable implications **locally**" has power only against very specific forms of
  search. The one exception they find is lag-length selection under thresholding, which produces an
  isolated spike just below the cutoff, and there the Binomial test is among the best.
- **Under the minimum approach, CSUB and CS2B have nearly identical power curves**, which the authors
  read as showing that CS2B's power comes mainly from the **bounds**. If a search is a
  minimum-selection search, the bounds are the only restriction doing work.

**Step 3: check where your true effects sit.** Power is **not monotone in `h`**. Under the minimum
approach, large `h` pushes `p`-values close to zero, where the upper bounds are hard to violate, so
bound-based tests have **very low or no power** at `h = 2` and under their empirically calibrated
effect distribution `Π̂`. The high-power region is where the data are informative but the true
effects sit **near the conventional cutoffs** — exactly where the incentive to search is largest.

**Step 4: count your degrees of freedom.** Appendix J: the larger `K` (the number of specifications
available to search over), the **higher** the power of CSUB and CS2B. More search is more detectable,
holding the selection function fixed.

**Step 5: do not read a non-rejection as a clean bill.** Stated in the conclusion in as many words:
"failure to reject using tests for p-hacking based on p-values does not really indicate the absence
of p-hacking."

**And the publication-bias rider.** Publication bias on top of a search "often increases but can
also **decrease** the power of the tests for rejecting the joint null". It is not a
one-directional nuisance.

## Robustness evidence (qualitative only)

- **Theory plus simulation, with the simulation designed around real econometric practice** rather
  than around abstract DGPs: three families of search (covariate selection, instrument selection,
  standard-error selection) crossed with two selection functions, several effect distributions
  including an empirically calibrated one, and `K` varied.
- **Replication package published** by the authors (`github.com/nvkudrin/pHackingPower`), covering
  all figures and Monte Carlo results.
- **The honesty is the strongest signal.** The headline is that the authors' own Econometrica tests
  have low power in many settings and none in some, that the field's most-used test (Binomial) is
  often the weakest, and that one of their own recommended tests (LCM) has a non-monotonic power
  curve. They also report that for CS1/CSUB/CS2B "the optimization routine fails to converge for
  some realizations of the data due to nearly singular covariance matrix estimates", and they count
  those as **non-rejections** — a conservative choice stated openly, and one that matters at small
  sample sizes.
- **The limitation to record**: the paper does not cover Caliper tests (its own footnote 2 excludes
  them), so nothing here grades the bunching-based literature.
- **Open at the authors' own hands**: they note the lack of power has "already motivated the
  development of new tests", citing Kudrin (2024b). Named, unobtained, and a reasonable pointer if a
  later session needs more.

## Implementability here

Together with the companion note this **closes the folder's standing aim, in the negative**, and
that is the most useful thing it can do. Four findings.

- **`#485` — this lab's seat decision is a MINIMUM-selection search, so the monotonicity and
  discontinuity readings of its own board have ZERO power by construction.** The protocol runs
  candidates and the gate takes the best; `FAMILY_LEAD` records "the best result yet in its family".
  That is `Pr = min{P1, P2, …}`, not a threshold rule — the lab does not stop searching when it
  clears `α`, and it does not have a single preferred candidate it reports first. Combined with the
  companion note's `#480` (the lab's composite one-sided null breaks the non-increasingness
  restriction itself) this is **belt and braces**: the shape restriction is both invalid here and
  powerless here. **No session should read left-skew, humps or discontinuities in the lab's recorded
  statistics as evidence about its search.**
- **`#486` — and the one restriction that would have power is the one the lab is worst placed to
  use.** Under minimum selection only the **upper bounds** bite, their power depends on `τ` being
  large, and the authors find **no test has power at all** under the minimum approach when the effect
  distribution puts mass on large `h`. The lab's own effect sizes are small and near its cutoff,
  which is the favourable corner — but "even if p-hacking leads to violations of the testable
  restrictions, these violations may be small and can thus only be detected based on **large samples
  of p-values**." The lab has **27 recorded trials**, which its own audit calls 7–12 independent
  bets. The corpora in these two papers run to 49,838 and 352,817 statistics. **The lab is three to
  four orders of magnitude short of the sample size at which this instrument does anything**, and
  that is an arithmetic statement, not a judgement about search quality.
- **`#487` — the favourable structural fact the folder should state, because it reframes the
  question.** The lab writes **every** trial to `experiments/trials.jsonl` and the protocol forbids
  rewriting that history. **There is no file drawer here.** The selection function applies to the
  *seat*, not to the *record*. So the distribution of the lab's recorded statistics is not a selected
  distribution at all, and the `p`-curve literature's object — inferring an unobserved search from a
  selected sample — does not describe this lab's problem. What the lab actually has is the *whole*
  search, observed. The right question about it is therefore not "was it gamed" but "what is the
  deflation benchmark built from it worth", which is a different vein and one the folder already
  holds (`notes/2026-08-24-multiple-testing-haircut.md`, `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md`,
  and the online-FWER vein). **The 2026-11-16 nightly's reading of its `null_pctile` values, and the
  2026-11-18 nightly's reading of its skills against their error bars, are better understood as
  descriptive statistics of a fully observed search than as tests of a selection hypothesis.**
- **`#488` — the transferable discipline, and the only thing here the lab should actually adopt.**
  Power is a property of the (test, selection function, effect distribution) triple, so **state the
  selection function before reading a set of statistics.** Applied to the lab: the correlation
  structure among the *candidates considered* is what decides how far a search can move the reported
  number. The folder's `rho = +0.0888` cross-trial active-return correlation says the lab's
  candidates are close to independent — the "fast" regime, where a search moves the reported
  statistic a lot per candidate tried. That is the regime in which a search is most consequential
  and, under minimum selection, least detectable from the statistics alone. **The remedy is
  pre-registration of the candidate count, not a post-hoc diagnostic** — which is where the folder's
  existing online-FWER vein already points, and this paper is the authority for preferring it.

**Pitfall.** Do not take the CS2B recommendation as an instrument to run here. It is the right
default in the paper's setting (tens of thousands of statistics, similar tests, continuous
`p`-values) and it fails all three of those preconditions on this board.

## Related

- Companion, and the source of Theorems 1–3 and the bounds this paper evaluates:
  `notes/2026-11-19-the-null-shape-of-a-set-of-ones-own-p-values.md`.
- The dispersion half of the same aim: `notes/2026-11-19-dependence-robust-inference-on-a-set-of-estimates.md`.
- `notes/2026-10-01-limits-of-p-hacking-publication-bias.md` — the counterweight literature on
  whether search can generate the observed tail at all. Different object (fits a publication
  probability to a corpus); same vein.
- `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md`, `notes/2026-08-24-multiple-testing-haircut.md`,
  `notes/2026-09-01-multi-signal-overfitting-critical-t.md`, `notes/2026-08-25-bayesianized-p-values-prior-odds.md`
  — the haircut and prior-odds veins, which `#487` argues are the right frame for this lab's board.
- Named and unobtained: Kudrin (2024b) on newer, more powerful tests; Beare–Moon (2015) on the LCM
  statistic's degeneracy. Neither pursued.
