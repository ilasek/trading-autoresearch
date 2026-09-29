---
title: "Frog in the Pan: Continuous Information and Momentum"
authors: Da, Gurun, Warachka
year: 2014
venue: Review of Financial Studies 27(7), 2171–2218 (Tier 1)
url: https://doi.org/10.1093/rfs/hhu003
citations: "306 (Crossref `is-referenced-by-count` by DOI, checked 2026-09-28); 30
  (Semantic Scholar by the same DOI, checked 2026-09-28). **Tenth consecutive session with a
  split index record** and the largest gap yet recorded here — Semantic Scholar's DOI record
  carries the journal article's title, year and author list but almost none of its citations,
  which is the same shape as the 2026-09-23 Kan–Zhou case. Crossref is the count to read.
  OpenAlex was not available: its free daily budget was already exhausted at the time of the
  check (HTTP 429, `Insufficient budget`). **Read in full** from the typeset RFS PDF on the
  first author's Notre Dame page (`academicweb.nd.edu/~zda/Frog.pdf`), which carries the
  journal's own running headers and pagination."
sample_period: 1927–2007 (a post-1980 subperiod is reported alongside every main result)
markets: US only — CRSP common stocks after delisting adjustment, with a $5 price filter
tier: A
validation_overlap: false
published_post_2018: false
---

Tier A on venue, sample length and methodology honesty; the one rubric row it does **not**
fully earn is replication. A Crossref title search on 2026-09-28 surfaced exactly one indexed
non-US extension of the measure — an *earnings*-momentum study in a price-limit market
(Pacific-Basin Finance Journal, 2016, 9 citations) — which is an adjacent question rather
than a replication of the price-momentum result. **No entry for this effect was located in
the large replication projects this folder grades against**, and nothing here should be read
as saying the effect has been independently confirmed. What is confirmed is that the
construction is unambiguous and cheap, which is the part this lab needs.

## Mechanism

**Limited attention with a magnitude threshold.** The authors' two-period model splits agents
into rational investors, who process every signal, and "frog-in-the-pan" (FIP) investors, who
do not process any signal whose absolute size falls below a threshold `k` until the terminal
payoff is realized. With FIP investors a fraction `m` of the economy, the interim price is

    P₁ = s₁ − m · Σᵢ sᵢ · 1{|sᵢ| < k}

so the price is *short* of fundamentals by exactly the sum of the sub-threshold signals. The
prediction is not "momentum exists" — it is **conditional**: holding the cumulative
formation-period return fixed, continuation should be stronger when that cumulative return was
assembled out of many small increments (much truncation) than when it came from a few large
jumps (little truncation). A series of frequent gradual changes attracts less attention than
one dramatic change, so the same total information is impounded more slowly.

The direction is what makes this different from the usual momentum enhancements: it is a
statement about the **path** by which a given cumulative return arrived, not about the
cumulative return itself. Two names with identical 12-1 returns are predicted to continue
differently.

## Construction recipe

**Information discreteness (ID), the benchmark proxy.** Over the momentum formation window,
let `%pos` and `%neg` be the fractions of daily returns that are positive and negative. With
`PRET` the cumulative return over the formation window:

    ID = sgn(PRET) × [%neg − %pos]                                     (Eq. 1)

- `PRET` is the cumulative return over the **past twelve months skipping the most recent
  month** — the standard 12-1 momentum signal, unchanged.
- `sgn(PRET)` is +1 when `PRET > 0`, −1 when `PRET < 0`.
- **Low ID = continuous information** (many small same-signed days). **High ID = discrete
  information** (few large same-signed days against a majority of opposite-signed days). If
  every daily return shares the sign of `PRET`, ID attains its minimum of −1.
- ID deliberately **ignores magnitude**: each daily return contributes only its sign. The
  authors state the resulting counterexamples plainly (`{2,2,2,2,2,2}` and `{1,1,1,1,1,7}`
  share an ID of −1) and argue they become rarer as the window lengthens.
- ID is interpreted **only after conditioning on `PRET`**; it is not a standalone score. The
  paper's own simulation puts the correlation between ID and continuation at about −0.65 for
  past winners and −0.67 for past losers, and **negligible when `PRET` is near zero**.

**Two documented variants, both worth knowing here.**

- `ID_MAG` (Eq. 2) restores magnitude but *down*-weights it. Sort the formation window's daily
  returns into firm-specific quintiles by `|return|`; assign monotonically declining weights
  `wᵢ = 5/15, 4/15, 3/15, 2/15, 1/15` from the smallest-magnitude quintile to the largest; then

      ID_MAG = −(1/N) · sgn(PRET) · Σᵢ sgn(Returnᵢ) · wᵢ

  It reduces to ID when all daily magnitudes are equal. The declining scheme is conceded to be
  arbitrary; other monotone declining schemes are reported to behave alike.
- `ID_Z` (Eq. 3) normalises away zero-return days, which Eq. 1 implicitly charges against
  continuity because `%pos + %neg + %zero = 1`:

      ID_Z = sgn(PRET) × [%neg − %pos] / [%neg + %pos]

  identical to ID when there are no zero-return days. **This variant is the one that matters
  for this repo — see Implementability.**

**Portfolio formation.** Monthly. Sort into quintiles on `PRET`, then subdivide each `PRET`
quintile into ID sub-portfolios (a *sequential* double sort). Post-formation returns measured
over six months and three years. Because ID and `PRET` are positively correlated, the
sequential sort's second stage can itself generate `PRET` variation, so the paper also reports
an **independent** double sort on `PRET` × ID as the control; both give the same monotone
pattern. A one-month gap between formation and holding is retained throughout.

**Holding horizon, and this is construction-relevant rather than performance.** Marginal
month-by-month continuation following *continuous* information remains statistically
distinguishable from zero out to roughly the eighth month after formation; following
*discrete* information it is indistinguishable from zero by about the third. The authors argue
this horizon is what makes limited attention, rather than risk, the plausible explanation, and
note explicitly that it means the effect does **not** require frequent rebalancing to harvest.

## Robustness evidence (qualitative only)

- **Monotone across the ID sort in both the full sample and the post-1980 subsample**, and in
  both the sequential and the independent double sort.
- **Survives being rebuilt on market-adjusted daily returns** (subtracting the daily
  value-weighted market return before taking signs), so it is not an artifact of market-state
  co-movement in the sign counts.
- **Survives Fama–MacBeth regressions** controlling for size, book-to-market, turnover,
  idiosyncratic volatility (four-factor residual, Fu-style), analyst coverage, institutional
  ownership, earnings surprises, the Hou–Moskowitz price-delay measure, the Grinblatt–Han
  unrealised-capital-gains variable and the Frazzini capital-gains-overhang variable.
- **Survives orthogonalisation**: the paper constructs a *residual* ID from a regression of ID
  on `|PRET|`, return consistency, book-to-market, size, turnover and the rest, and reports the
  conditioning result holds on the residual.
- **Distinguished from the disposition effect** by splitting ID into its winner-side and
  loser-side halves (`PosID`, `NegID`) and comparing against the Grinblatt–Moskowitz return-
  consistency variable, which requires eight of twelve monthly returns to share the sign of
  `PRET`.
- **No long-run reversal** following continuous information, which is the paper's evidence for
  underreaction rather than for overreaction-then-correction. This matters here: a conditioner
  whose gains reverse is a turnover trap.
- **Not replicated independently, as far as this session could establish** (see the tier note).
  Single market, single data vendor, no transaction costs anywhere in the paper, and multiple
  testing is not formally addressed.

## Implementability here

**In scope on closes alone.** ID needs only the sign of each daily return inside the 12-1
window and the sign of the cumulative return — the one-argument `generate_weights(prices)`
contract suffices. Cost: one pass over the visible window, trivially causal.

**The repo-specific trap, and it is severe enough that the naive form should not be written.**
This universe is 145 global instruments on a shared daily index, and `prices` is
**forward-filled across foreign holidays**. A forward-filled close produces an exact
**zero** daily return that is an artifact of the calendar, not of the market. Eq. 1 charges
those zeros against `%pos + %neg`, so an instrument that trades on fewer of the panel's days
looks mechanically *more discrete* than a US name with identical price behaviour — an ID sort
on the raw panel would partly be a sort on **which region a name trades in**. `ID_Z` (Eq. 3)
is the paper's own fix and normalises exactly this quantity away. **Use `ID_Z`, and report
`%zero` per instrument alongside it.** The same hazard applies to any future signed-daily-
return score here, and `%zero` is itself the Lesmond–Ogden–Trzcinka illiquidity proxy, so the
diagnostic is worth having on its own.

**How to apply it so that it can actually move this book.** `learnings.md` [2026-09-27]
measured that the seat holds ~61% of gross in its ten largest weights and ~1.4% in its ten
smallest of ~48, and that an overlay acting on membership at rank 15–25 moved 8.27% of gross
and still landed at `rho` 0.9984. **A candidate that uses ID as a membership filter or as a
band-margin tiebreak will land in that same 1.4%-of-gross channel and is not worth a trial.**
The form that can move the top ten is a **score-level** one: adjust the momentum score itself
before the magnitude-weighting step, e.g. combine the cross-sectional rank of `PRET` with the
cross-sectional rank of `−ID_Z` (within the sign-conditioned population) into one score, then
weight as the champion already does. That changes the ten largest weights, which is what
`learnings.md` says is required, and it is a *score* change rather than the weighting-function
re-sweep the 2026-09-27 next-ideas list names as an anti-candidate.

**Pre-screens this lab's own rules require, before any file is written.**

1. **The reversal-in-costume screen** (`learnings.md` 2026-09-01, now credited with saving
   three trials). Compute, on train month-ends only, the Spearman correlation of `ID_Z` against
   the trailing 252-day return, against 12-1 momentum, and against the 21-day reversal score.
   The paper says ID and `PRET` are *positively* correlated by construction, so a non-zero
   reading is expected — pre-register the threshold **and the summary statistic it is read on**
   (`learnings.md` 2026-09-27: name mean or median in the same sentence as the number), and
   pre-register that the interesting quantity is the correlation of ID **within** the winner
   tail, not across the whole cross-section, since the paper's own simulation says ID carries
   nothing where `PRET` is near zero.
2. **The ETF question, which has no analogue in the source.** 42 of the ~145 instruments are
   diversified baskets. A basket's daily return is an average, so it is *mechanically* smoother
   and will sort continuous. ID on an ETF is therefore partly a diversification measure.
   Measure the ID distribution for the ETF and single-name cohorts separately before letting a
   pooled sort run, or condition within cohort.
3. **Turnover.** ID is computed over a twelve-month window, so it should be slow, and the
   source's eight-month persistence says the holding period need not be short. This is the rare
   conditioner that should *not* cost turnover — which matters because `learnings.md`
   [2026-09-27] bounds the whole cost-remedy class on this seat at +0.0249, so a candidate that
   *adds* turnover starts from behind.

**What this note does not license.** Nothing here is a performance expectation. The effect is
measured on US single names 1927–2007 with no costs charged; this universe is 145 global
instruments including baskets, with 15 bps/side and a 1-day lag. Import the construction and
the conditioning logic; import no magnitude.

## Related

- Conditioners of continuation already filed here, and the vein's record is poor:
  `notes/2026-09-13-information-uncertainty-and-price-continuation.md`,
  `notes/2026-09-13-analyst-coverage-and-the-speed-of-bad-news.md`,
  `notes/2026-08-17-momentum-horizon-echo.md`.
- **Tension to state rather than bury.** The three path-shape / reference-point veins this lab
  has run all closed: `experiments/learnings.md` [2026-09-19] closed the reference-point vein
  (capital-gains overhang, V-shaped selling) on five pre-registered readings, [2026-09-20]
  closed salience on five more and zero trials, and [2026-09-27] recorded 52-week-high proximity
  as the first of three "reversal in costume" findings. ID is in the same broad class — a
  statistic of the price path over the formation window — and a reasonable prior is that it
  fails here too. **What distinguishes it is that it is explicitly a conditioner on `PRET`
  rather than a substitute for it**, so its failure mode is different: the previous three died
  because they turned out to *be* a return score already in the book, and screen 1 above is the
  exact test of whether ID does the same. If it does, the vein closes for one free measurement
  and no trial — which is the outcome this folder should be equally happy with.
- Related refuted constants not to import: `experiments/learnings.md`'s de-concentration price
  and required-gain table were measured on `price-trend` constructions, and this is one, so they
  apply — including the `rho ≈ 0.99` column that is the only one this family reaches.
