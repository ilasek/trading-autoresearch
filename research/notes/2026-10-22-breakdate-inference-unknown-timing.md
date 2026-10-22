---
title: "The New Econometrics of Structural Change: Dating Breaks in U.S. Labor Productivity" — why a split date chosen by a researcher is not a testable hypothesis, what the null distribution of a maximised break statistic is instead, and how wide a credible break-date interval turns out to be
authors: Hansen, Bruce E.
year: 2001
venue: Journal of Economic Perspectives 15(4), 117–128 (venue tier 1; an invited expository article rather than a research contribution — see Robustness)
url: https://doi.org/10.1257/jep.15.4.117
citations: 606 (Crossref `is-referenced-by-count`, checked 2026-10-22, resolved on the first call)
sample_period: 1947-02 to 2001-04 (651 monthly observations), U.S. manufacturing/durables labour productivity. Macroeconomic output data, not market returns — no asset-price series of any period appears in the article.
markets: none (U.S. macroeconomic time series only)
tier: A
validation_overlap: false
published_post_2018: false
read: full text, read visually. `users.ssc.wisc.edu/~bhansen/papers/jep_01.pdf` served the typeset article on the first try (1.32 MB, 12 pages), but it is a **text-layerless scan** — `pdffonts` prints an empty font table and `pdftotext` yields 12 characters from 12 pages — so it was rendered with `pdftoppm -png -r 125 -gray` and read as images. Pages 1–4 (framing, the Chow critique, the Quandt statistic, Andrews critical values), 6–7 (breakdate estimation and confidence intervals) and 8 and 11 (break-versus-random-walk, conclusion) were read; pages 5, 9 and 10 were not, and nothing is attributed to them. **Andrews (1993) itself was not obtained** — see Robustness for the access record; every statement about it below is Hansen's or Bai–Perron's characterisation, attributed as such, and no claim rests on text of Andrews that was not read.
---

## Mechanism

No economic mechanism. This note is about an inference problem, and the reason it belongs in this
folder is that the lab already has the problem under a different name.

The setup: a parameter may have changed at some date inside a sample, and you want to know whether
it did. The classical answer is the **Chow (1960) test** — split the sample at a date, estimate the
model on each half, test equality of the two parameter vectors with an `F` statistic. Hansen's
article is built around the observation that this test is almost never usable as advertised,
because the Chow test requires the breakdate to be **known a priori**, and a researcher has only two
ways to get one:

- pick an arbitrary date, in which case the test may be uninformative because it misses the true
  break; or
- pick a date from a known feature of the data, in which case the candidate breakdate is
  **endogenous** — correlated with the data — and the test **rejects falsely**.

He is blunt about the consequence: results are "highly sensitive to these arbitrary choices,
different researchers can easily reach quite distinct conclusions — hardly an example of sound
scientific practice." His opening complaint is the same point stated as method: one can always pick
groups of years in which an average is lower than in some other group of years, and "this ad hoc
selection of convenient time periods hardly qualifies as serious analysis."

The demonstration is one line long and is the single most transferable thing in the article. For
his series, a Chow statistic computed at one candidate breakdate is **3.9**; computed at a
breakdate **two years later** it is **7.1**. The 5% `χ²` critical value is 6.0. Two nearly adjacent
split dates straddle the threshold and give opposite answers.

**Why this lands here.** This lab's protocol reports train skill for **1997–2008 and 2009–2017
separately**. That is a Chow split at a date a human chose. Whatever else those two numbers are,
they are not a test of whether the strategy's behaviour changed, and the gap between them is not
evidence of a regime unless the split survives the machinery below.

## Construction recipe

**Step 1 — treat the breakdate as unknown.** The fix goes back to Quandt (1960): compute the Chow
statistic at *every* admissible candidate breakdate and take the largest. Hansen's framing is worth
keeping verbatim as a mental model: imagine a "devilish trickster who is willing to go to any
extreme to prove the existence of a structural break", who performs every possible Chow test and
reports the worst case. That maximum is the **Quandt statistic** (equivalently `supF`, `supWald`,
or `supLR` depending on the form).

**Step 2 — trim.** Candidates too near either end of the sample cannot be used, because there are
not enough observations to identify the subsample parameters. The convention is to search the
interior `τ` to `(1−τ)` fraction of the sample, with the **trimming parameter `τ` typically between
5% and 15%**; Hansen uses 5%. This is the same `ε` as in the Bai–Perron note and the same warning
applies: it must be fixed before looking.

**Step 3 — do not use `χ²` critical values.** This is the entire point. Because the statistic is a
maximum over candidate dates, its null distribution is not that of a single Chow test. The problem
was open for three decades and was solved in the early 1990s, most generally by **Andrews (1993)**
and **Andrews–Ploberger (1994)**, who provide tables of critical values; **Hansen (1997)** gives a
method for computing `p`-values. The size of the correction is the number to remember: for a model
with two parameters, Hansen reports the **Andrews 5% critical value as 12.9 against a `χ²` 5%
critical value of 6.0** — "just over twice". Using the wrong table does not shade a conclusion; it
roughly halves the bar.

**Step 4 — prefer bootstrap critical values to asymptotic ones.** Two separate cautions in the
article, both in the author's own voice. Hansen (2000) is cited for the result that **Andrews'
critical values are not robust to structural change in the marginal distribution of the
regressors**, and the remedy is to simulate robust critical values case by case. And in the
unit-root section he records that the literature found **asymptotic critical values should be used
only as a crude guide, with finite-sample bootstrap critical values much preferred**. For this lab
that is a cheap instruction rather than a caveat: bootstrap machinery is already standard here.

**Step 5 — estimate the date by least squares, and read the shape of the curve.** The breakdate
estimator is the candidate that minimises the sum of squared errors computed across both
subsamples. Hansen gives the diagnostic that comes free with it: plot SSE against candidate
breakdate. **If the parameters are constant, the curve varies erratically and randomly; if there is
a break, the curve varies systematically and has a well-defined minimum near the true date.** A
pronounced `V` indicates good identification. Multiple local minima are candidate multiple breaks
— the global minimum is the estimator, the other local minima can be treated "(cautiously)" as
further candidates, which is the sequential strategy of Chong (1995) and Bai (1997b): split at the
estimate, continue on the subsamples, and iterate with re-estimation of earlier breakdates on the
refined samples.

**Step 6 — report the interval, not the date.** Bai's limiting theory gives confidence intervals
for the breakdate that are easy to compute (the machinery is in the companion Bai–Perron note), and
Bai–Lumsdaine–Stock (1998) extend it to several series with simultaneous breaks, with the finding
that **using multiple time series improves dating precision** — a point with an obvious analogue on
a wide panel.

## Robustness evidence (qualitative only)

**The headline result, kept deliberately free of its dates, because it is the part that transfers.**
On a 651-observation monthly series, Hansen's procedure finds evidence of three breaks. One is
estimated precisely — its 90% confidence interval spans about four years. The other two are not:
their 90% intervals span **roughly twelve and eleven years respectively**. On a series with more
than six hundred observations, the data localise two of three breaks only to within about a decade.
The Bai–Lumsdaine–Stock application he cites behaves the same way: a quarterly series over roughly
thirty-five years yields a breakdate whose 90% interval is about five and a half years wide.

And the sharpest version: the breakdate that the applied literature had conventionally assumed for
this series **lies outside every one of those confidence intervals**. A convention about when a
series changed survived for years while being inconsistent with what the data could support. The
general statement, which is the one to carry: **a break date is estimated with far more uncertainty
than the confidence with which breaks are normally asserted, and the precision is governed by the
magnitude of the break relative to the noise — not by the length of the sample.** Hansen's one
tightly-dated break is tight because the parameter shift at it was large; his two loose ones are
loose because theirs were small. A later section of the article confirms the pattern directly, with
a large shift in a mean growth rate producing an interval about nineteen months wide.

**A second robustness point that is really an identification warning.** The article's third topic
is distinguishing a broken trend from a random walk, and the reason the two are hard to separate is
structural: **a trend break produces serial-correlation properties similar to those of a random
walk**. Perron (1989) tested the random-walk hypothesis against a trend-break alternative with the
breakdate specified as known; a collection of later papers objected that it is unreasonable to
believe the choice was made independently of the data, and proposed selecting the breakdate that
produces the most evidence against the random walk. Hansen's observation about that exchange is the
one worth extracting, because it is a general principle and not a fact about unit roots: the
modified procedure can return **the same numerical value** of the test statistic as the original,
and still be a different test — "the test is constructed using a different *procedure*, and hence it
has a different sampling distribution", with much larger critical values. The same number, obtained
by searching rather than by specifying, means something weaker.

**Venue and status.** The *Journal of Economic Perspectives* is tier 1 but is an expository outlet;
this article contributes no theorem. It is the right source for the *construction* and the
*pitfalls*, and the wrong source to cite for any of the underlying results, each of which belongs to
Andrews, Bai, Perron, Quandt or Chow. Treated that way it is Tier A for what it is used for here.
Its 606 citations for a survey of this kind reflect that it became the standard entry point.

**Access record for Andrews (1993), which is the primary this note repeatedly points at and does
not read.** Crossref resolves `10.2307/2951764` (Econometrica 61(4), 821–856, **3065** citations,
checked 2026-10-22). The full text was not obtained. The Cowles Foundation discussion-paper version
(DP 943) is listed by both RePEc and Cowles, but the legacy path
`cowles.yale.edu/sites/default/files/files/pub/d09/d0943.pdf` returns HTTP 200 **with an HTML body**,
and the current Cowles record page `cowles.yale.edu/node/145655` is a **1.1 MB Drupal shell
containing no PDF href at all** — only favicons — so the Cowles site holds the record without the
file. One further item located but not fetched, recorded for a later session: a search result points
to a file named `andrewsCorrect.pdf` on the `gretlml.univpm.it` mailing-list archive, which is
plausibly the **Andrews (2003) corrigendum**; secondary sources state that corrigendum revised
Table I because the critical values for `p = 8` were too small. That is an unverified pointer, it is
flagged as such, and **nothing in this note depends on it** — but anyone implementing from Andrews'
tables should resolve it first.

## Implementability here

**Cost: negligible, and no new dependency.** Everything above is a loop over candidate split dates
with an OLS fit on each side, plus a bootstrap for critical values. On a single daily series of a
few thousand observations this is seconds, and the lab already bootstraps as a matter of course.

**The application that fits the rules is a diagnostic on the lab's own measurement apparatus, and
it reads no holdout.** Three concrete and free uses, in descending order of how much they would
change:

1. **Test the train subperiod split.** The protocol reports 1997–2008 and 2009–2017 train skill
   separately. Those are human-chosen boundaries, which is exactly the endogenous-Chow situation.
   Running a `supF` over admissible split dates on a champion or family-lead return series, with
   bootstrap critical values and a reported confidence interval, answers whether the subperiod
   decomposition is a split the data supports. Given the interval widths above, the likely honest
   answer is that a daily return series localises a break in its own mean only very coarsely — and
   **that** is the finding: it would mean the two reported train numbers are a convention, and that
   a difference between them is weaker evidence of regime-dependence than it reads as.
2. **Put an interval on any future claim that a family "stopped working".** The folder and the
   journal both contain reasoning of the form "this behaved differently in the earlier part of the
   sample". The machinery above converts that from an assertion into an estimate with an interval,
   and the interval is usually wide.
3. **Use the SSE-versus-breakdate curve as a shape diagnostic before any regime work.** An erratic
   curve with no well-defined minimum is direct evidence that there is no break to find, and it
   costs one plot. This is the cheapest possible pre-screen on the whole regime vein, and it can
   rule the vein out without spending a trial.

**The connection to a problem this lab already tracks, which is the real reason to care.**
`SUMMARY.md` carries a standing cross-family section on what a selected maximum is worth, and a
second on what a count of correlated trials is worth. The Quandt/Andrews problem is the *same*
problem with a clean closed-form answer: a statistic maximised over a continuum of correlated
candidates has a known, strictly larger null distribution, and ignoring the maximisation roughly
halves the critical value. That is a worked, published instance of the lab's own deflation
machinery arriving from the structural-break literature, and the "same number, different procedure,
different sampling distribution" formulation is a crisper statement of it than the folder currently
has.

**Pitfalls.** (1) The trimming fraction is a researcher degree of freedom that every critical value
is conditional on. (2) Andrews' asymptotic critical values are themselves not robust to change in
the regressors' marginal distribution — bootstrap. (3) A break and a unit root mimic each other's
serial correlation, so on a near-random-walk price series a "detected break" needs the random-walk
alternative ruled out before it means anything. (4) Nothing here licenses *trading* a detected
break: every statement above is retrospective, and the real-time version of the problem is the
subject of the Ang–Timmermann note, where it goes considerably worse.

## Related

- `2026-10-22-multiple-changepoint-estimation-bai-perron-pelt.md` — the estimation machinery this
  note is the inference half of. Bai–Perron's `supF`, `DmaxF` and `F(ℓ+1|ℓ)` are the multi-break
  generalisations of the Quandt statistic described here; read together.
- `2026-10-22-regime-switching-financial-markets.md` — the real-time counterpart. This note's
  methods date breaks after the fact; that one records what happens when you must infer the state
  as it arrives.
- `2026-08-17-averaging-over-estimation-windows.md` — what to do with a break estimate once you
  have one, and the standing argument for averaging over windows rather than splitting at a date.
- `SUMMARY.md`, "What a selected maximum is worth — post-selection estimation, and the dependence
  among candidates" and "What a count of correlated trials is worth" — the lab's existing treatment
  of the same statistical problem. No tension; this is independent published confirmation with a
  closed-form magnitude attached.
- `experiments/learnings.md` — no direct tension. The lab's regime refutations are about overlays
  that trade; nothing in this note proposes trading anything.
