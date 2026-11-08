---
title: "The (Mis)uses of the S&P 500"
authors: Robertson
year: 2023
venue: University of Chicago Business Law Review 2(1), 137–169 (law review; outside the rubric's finance venue tiers — graded on methodology transparency, see tier note)
url: https://businesslawreview.uchicago.edu/sites/default/files/2023-03/Robertson_v2_137-169.pdf
citations: not indexed (Crossref title search returned no match for the article; OpenAlex search returned no match; Semantic Scholar title endpoint answered HTTP 429 — checked 2026-11-08). No DOI is registered for the article.
sample_period: 1989–2017 (mechanical-counterfactual overlap and return comparison); 2015–2017 (daily eligible-set count, limited by the provider retaining no methodology revisions before 2015); 2000–2017 (tracking-error comparison against a live index fund)
markets: US (CRSP, Compustat, Bloomberg, CRSP Survivor-Bias-Free Mutual Fund Database); one committee-run large-cap index
tier: B
validation_overlap: false
published_post_2018: true
---

## Mechanism

Same object as `notes/2026-11-08-committee-discretion-versus-the-published-admission-rule.md`
— the distance between a committee-selected index and a mechanical rule — but measured by
**building the mechanical alternative and comparing the two portfolios**, in names, in size,
and in return space, rather than by asking how much of the committee's choice a regression on
the published criteria can explain.

The economic content is a single claim with three empirical legs: a committee index is *one
particular large-cap portfolio*, not the large-cap portfolio. It is not neutral (the
committee chooses among more qualifying names than it has slots), and it is not constant (its
constituents turn over for both rule-driven and discretionary reasons). Both properties are
construction facts, not market facts, so they are timeless in exactly the way this folder
wants.

## Construction recipe

Three independent measurements of the same gap. All three are implementable by anyone holding
a membership series and a price panel, which is why this is the more portable of the two
notes.

1. **The eligible-set surplus.** On each trading day, count the names satisfying the
   provider's published inclusion criteria, coded *conservatively* (erring toward excluding a
   name when the text is ambiguous), and add to that set any actual constituent that fails the
   coded criteria — because such a name is either evidence the coding is under-inclusive or
   evidence the committee kept it anyway, and in both readings it belongs to the choice set.
   The surplus of the eligible count over the index's size is the committee's room to choose.
   **Measured:** on the median day the eligible set exceeds the index's own size by more than
   a hundred names, i.e. **over 20% of the index's size is slack**, under a coding designed to
   understate it.
2. **The mechanical counterfactual and the overlap table.** Define the mechanical index as the
   *N* largest names by market capitalisation in the price database, selected once a year from
   the prior year-end and held for the year (robustness: daily reselection). Cross-tabulate it
   against actual membership into three populated quadrants — in both, index-only,
   mechanical-only — and report per-quadrant counts, mean and median size, and aggregate size.
   **Measured, as shares rather than levels:** only about **72%** of the committee index's
   names are in the mechanical top-*N* at an average moment; roughly **28%** of its names are
   not; and a comparable count of mechanical-top-*N* names is outside the index. The
   mechanical-only names average about **60% of the average constituent's size** and amount to
   roughly **17% of the index's aggregate value**; the index-only names average about **18% of
   the average constituent's size** and amount to roughly **5%** of it.
   **The finding that kills the natural intuition: the *median* mechanical-only (excluded)
   name is slightly LARGER than the median index constituent**, significant at 1%. Index
   membership is therefore not a size cut with noise around the boundary; it is a different
   selection whose *middle* sits at the same size as the mechanical rule's middle, with the
   two differing in the tails in opposite directions.
3. **The gap in return space.** Build a value-weighted portfolio of the mechanical index
   (dividends reinvested, CRSP delisting returns appended — the author flags this explicitly,
   and it matters), and compute tracking error, mean absolute error and mean squared error
   against the actual index's total-return series. Then **benchmark that number against the
   tracking error of a real, large, low-fee index fund versus the index it tracks** — the
   move that makes an otherwise uninterpretable dispersion number readable.
   **Measured:** the fund tracks its index roughly **20× more closely than the index tracks
   the mechanical counterfactual** (larger still on mean squared error), and the pattern is
   stable across subperiods. Robustness runs — daily reselection, equal weighting, no
   reinvestment of proceeds — all make the gap *larger*, so the headline is the conservative
   case.
4. **Turnover as its own leg.** Separately, counterfactual portfolios frozen at an earlier
   constituent list and run forward isolate the effect of constituent turnover on the index's
   own behaviour; the author reports it as substantial, consistent with an older study of the
   original constituents of the same index. Direction and existence only are recorded here —
   the magnitudes are performance figures over a dated window and are left in the source.

## Robustness evidence (qualitative only)

- **Methodology honesty is this source's strength and the reason it is graded B rather than C
  despite the venue.** Every construction is specified in appendices, each robustness variant
  is reported with its direction, delisting bias is handled rather than mentioned, the
  conservative coding choices are named as biasing against the paper's own conclusion, and the
  author states explicitly that nothing in the analysis claims the committee index is
  constructed *wrongly* or that either index outperforms the other — the exercise quantifies
  discretion, not quality. That last disclaimer is also the reason this note carries no
  performance claim.
- **Two legs converge on the same number from different directions.** The eligible-set surplus
  and the mechanical-overlap exercise are independent measurements and both land at
  "discretion accounts for roughly 5% of the index's aggregate value" — the first via slack in
  the choice set, the second via the index-only quadrant's share of value.
- **Weakest elements.** (i) Single market, single index, no replication, no DOI, not indexed in
  Crossref/OpenAlex, and a law review rather than a finance journal — by the rubric's venue
  ladder this is below tier 3's practitioner research in *review process* while being above it
  in *reproducibility*; graded B on the methodology column alone and it should not be cited as
  if peer-reviewed in finance. (ii) The eligible-set leg covers only three years, because the
  provider confirmed to the author that pre-2015 methodology revisions are not retained — a
  hard data limit, not a design choice. (iii) The mechanical counterfactual selects on market
  capitalisation, which is the mechanical rule most favourable to finding a *small* gap; a
  different mechanical rule would give a different number.
- **A second source's conclusion, relayed at second hand and flagged as such.** This article
  reports that a peer-reviewed study of discretionary constituent changes in the same index
  (Geppert, Ivanov & Karels, *Review of Quantitative Finance and Accounting* 37(1), 21,
  `10.1007/s11156-010-0193-0`, 12 Crossref citations, checked 2026-11-08) concludes those
  changes made the index **more representative of macroeconomic business-cycle measures —
  inflation, industrial production, oil prices — and notably not of equity performance**. That
  primary was **not obtained** (closed at the publisher; OpenAlex reports
  `any_repository_has_fulltext: false`; the author's dissertation path at the degree-granting
  institution 404s), so it is recorded as a named pointer and nothing in this folder should
  rest on it. If it is ever read, the claim to check is that a committee's objective function
  is a *representativeness* objective, which would explain both notes' findings at once.

## Implementability here

- **This is the quantitative answer to "how different is the `eligible` panel from a size
  screen", and it is a free reading rule.** A candidate that builds its own universe as
  "top-*N* by any size-like proxy" is not approximating the panel: it would differ in roughly a
  quarter of its names, and in return space by about an order of magnitude more than an index
  fund differs from its index. The median-size result is the sharper half — because the
  excluded names' *median* size matches the included names' median size, there is no size
  threshold that recovers membership, and **"eligible" cannot be re-derived from any size
  ordering this repo could construct.** (It could not be constructed anyway: market
  capitalisation needs a share count, outside the contract — `#408`.)
- **It bounds what the pool benchmark is.** Every skill number in this lab is measured against
  the equal-weight eligible pool. This source says that pool is a committee-and-rule artefact
  whose distance from a mechanical large-cap pool is material in return space. It does **not**
  say the pool is a bad benchmark — the lab's gate defines skill against it, and that is the
  definition. It says the pool should not be *described* as "the large-cap universe", and that a
  candidate motivated by "the pool is just big names" is motivated by something false.
- **Nothing to build; two things to stop doing.** No candidate follows from this source.
  What follows is (i) do not substitute a self-constructed top-*N* universe for `eligible` in
  reasoning about what the gate will measure, and (ii) do not assume the panel's churn is
  rule-driven and therefore mechanically forecastable — turnover has a discretionary component
  whose share of value this source puts at roughly a twentieth, and whose effect on the index's
  own behaviour it measures as substantial.
- **One cheap diagnostic that IS available**, offered as a free measurement in the sense the
  lab uses the term (holdings-only, no returns scored): the panel's own `eligible` frame
  supports counting, per index sub-population and per date, how many names are eligible and
  how the count moves — the lab cannot see the *surplus* (the qualifying non-members are not
  columns), but it can see the churn rate, and a sub-population whose churn is smooth is
  behaving like a rank rule while one whose churn is lumpy is behaving like a committee. That
  is a one-line distinction with a real consequence for `#411`'s cohort scout, which pools
  admissions across nine regimes.

## Related

- `notes/2026-11-08-committee-discretion-versus-the-published-admission-rule.md` — the
  regression measurement of the same gap, plus the mechanically-ruled-index contrast and the
  discretionary/rules-based split of entrants.
- `notes/2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` — the
  rule-induced, non-fundamental component of this panel's covariance (`#407`); this note adds
  that the *membership* side carries a discretionary component too.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md`,
  `notes/2026-11-06-investability-frictions-and-the-microcap-screen.md` — the panel-admission
  cluster.
- `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md`,
  `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` — what the equal-weight
  pool benchmark mechanically is; this note says what its *membership* is.
