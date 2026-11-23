---
title: "A mix of long-only factor sleeves is NOT a mean–variance-efficient way to hold several signals — and the fraction of the attainable improvement it captures, against a single long-only book of individual names built from the same forecasts"
authors: Clarke, de Silva, Thorley
year: 2016 (corrected May 2017)
venue: "Financial Analysts Journal 72(6), 9–26. Peer-reviewed; a tier-1 practitioner-academic venue in this folder's rubric."
url: https://doi.org/10.2469/faj.v72.n6.3
citations: "56 (OpenAlex, checked 2026-11-23); 43 (Crossref `is-referenced-by-count`, same DOI and date); 2 (Semantic Scholar, same DOI, same date — a clear undercount of the kind this folder's 'disbelieve a lone count' rule exists for, recorded so it is not rediscovered). The SSRN working-paper record `10.2139/ssrn.2616071` carries 4."
sample_period: "1968–2015 simulations. Nothing in the article touches 2016 or later."
markets: "the largest 1,000 US common stocks"
tier: "B−. Peer-reviewed tier-1 venue, respectable citation count for a practitioner-academic article, authors with a long track record in exactly this problem (they are the source of the transfer-coefficient framework this folder already uses), and a near-five-decade simulation on a panel of roughly this repo's width. Held down hard on one axis: **the body was not read**. Every open route failed this session, so the mechanism below is the article's own abstract plus inference from the same authors' other work, and the construction recipe is largely unknown rather than summarised."
validation_overlap: false
published_post_2018: false
read: "NOT read. Abstract only, from the publisher's own page (`rpc.cfainstitute.org/research/financial-analysts-journal/2016/fundamentals-of-efficient-factor-investing-corrected-may-2017`); the article itself is CFA-Institute-member-gated. Blocked: the SSRN green copy OpenAlex names (`papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2668020_code159211.pdf`) returns HTTP 403 with a 5.7 KB Cloudflare 'Just a moment…' body; `cdar.berkeley.edu`, which a search named as hosting a copy, **does not resolve from this environment at all** (`connect_unreachable`, HTTP 502 at the egress proxy — host-side, not a policy block). Cite the corrected (May 2017) version; the original carried an erratum."
---

## Why this source is here

The [2026-11-22] aim is the construction corner where "scouted leads become a challenger", and the
two practitioner articles filed alongside this note argue about *which* construction wins. This one
supplies the quantity both of them talk around: **how far the sleeve mix is from the efficient
long-only book at all.** It is the theory end of the same question, by the authors who gave this
folder the transfer coefficient.

## Mechanism

**The claim, in the authors' own words: "Combining long-only-constrained factor subportfolios is
generally not a mean–variance-efficient way to capture expected factor returns."** The reason is
the one this folder has now recorded from four directions, and the authors' framework is where the
cleanest version of it lives. Each long-only sleeve pays the long-only distortion *separately*: its
holdings are the solution to a constrained problem that can only *underweight* the names its own
signal dislikes, and it has no way to express "this name is also bad on the other signals". Holding
several such sleeves therefore pays the constraint's price once per sleeve and leaves the
cross-signal information on the table. A single pass over individual securities, using *the same*
risk model and *the same* return forecasts, pays it once.

**The magnitude, and why a ratio is recorded here where a performance level is not.** Their
simulated comparison is between three objects: the market portfolio, a fully-invested combination
of four long-only factor sleeves (low beta, small size, value, momentum), and a long-only book of
individual securities built from the same inputs. The sleeve combination captures, in their
abstract's own phrasing, "less than half (e.g., 40%) of the potential improvement over the market
portfolio's Sharpe ratio"; the single-pass security-level book captures "most (about 80%)". Those
are **fractions of an attainable improvement under the paper's own forecasts** — construction
efficiency, not realised performance — which is why they are recorded while every dated Sharpe
level in the article is not. Read them as "the mix leaves roughly half of what the same information
could buy", with the sample flagged above and the usual discount for a simulation whose numerator
is the authors' own optimum.

**What is NOT established by this source, and must not be inferred from it.** The comparison is
against an **optimised** long-only book — same risk model, same forecasts, one pass — and not
against a ranked-and-equal-weighted composite-score book, which is what a practitioner (or this
lab) would actually build. So the 40%-versus-80% gap is an upper bound on what integration can
recover, achieved by an optimiser with a covariance matrix. It says nothing about whether a
*score-weighted* or *rank-selected* composite recovers any of it, and nothing about turnover, costs
or extreme relative risk, which is exactly where the two companion notes disagree with each other.

## Construction recipe

Mostly unknown, because the body was not read. What the abstract fixes:

1. **Inputs.** One risk model and one set of return forecasts, held *identical* across the arms being
   compared — this is the article's methodological point as much as its finding.
2. **Arm A.** Four fully-invested, long-only factor subportfolios (low beta, small size, value,
   momentum), combined.
3. **Arm B.** One long-only optimised portfolio of individual securities from the same inputs.
4. **Comparison statistic.** The fraction of the *attainable* Sharpe-ratio improvement over the
   market portfolio that each arm captures, computed by simulating optimal combinations of factor
   and security portfolios.
5. **Universe.** The largest 1,000 US common stocks.
6. **Unknown and not guessed here**: sleeve construction (how each subportfolio is formed), the
   weights at which sleeves are combined, forecast construction, rebalance cadence, position
   bounds, whether costs appear anywhere, and how the attainable optimum is defined.

## Robustness evidence (qualitative only)

- **Sample.** Close to five decades, one market, a panel of ~1,000 names — the same order as this
  repo's eligible cross-section, which makes the breadth of the result unusually transferable for a
  US-only study.
- **Provenance.** The authors are the originators of the transfer-coefficient framework and have
  published the long-only minimum-variance composition result this folder already holds; this is
  their own framework applied to the multifactor case, so it is internally consistent with a body of
  work the folder has graded well.
- **Replication.** No independent replication was found this session. The *direction* of the claim is
  corroborated, from a different starting point, by the integration literature already in the folder
  (and by the algebra in `notes/2026-09-01-multi-signal-overfitting-critical-t.md`, which says a
  linear composite and a portfolio of single-signal books coincide **until** the long-only truncation
  is applied — this article is a measurement of what the truncation costs when applied per sleeve).
  The *magnitude* rests on one paper's simulation and should not be carried as a constant.
- **Known gap.** An efficiency comparison with no cost model is a comparison of paper books. The
  companion notes supply the turnover and extreme-risk side and point the other way, which is the
  honest state of this literature.
- **Anti-lookahead.** No dated performance figure from this article is recorded; the two fractions
  quoted are ratios of attainable improvement under the paper's own inputs. Sample ends 2015.

## Implementability here

- **The statement that matters is the one the lab can act on without the magnitude: a blend of
  per-lead long-only books is a construction that pays the long-only constraint once per lead.** On
  this repo's panel the constraint is severe — `#375`'s one-bit truncation means a lead's score is
  expressible only as membership — so "once per lead" is a real cost, and it is the cost a composite
  score avoids.
- **But the arm that avoids it in this paper is an optimiser the lab cannot run as specified.**
  Arm B needs a covariance matrix over ~1,000 eligible names plus return forecasts in return units.
  The lab's leads are *ranks*, its weighting is capped and long-only, and `learnings.md` records
  repeated failures of covariance-based weighting on this universe. So the practical reading is: the
  40%-versus-80% gap is the **ceiling** on what a better combination operator could recover here,
  not a forecast of what a rank-composite candidate will recover. A candidate that captures a small
  part of it is behaving as this literature predicts.
- **Two free, holdings-only measurements it motivates.** (a) The **per-lead constraint cost**: for
  each lead, the difference between its score's rank information content on the full eligible panel
  and the information content of the membership-only (truncated) version of it the book can express
  — the lab's own `#376` screen, run per lead and then on the composite, which is exactly the
  "once per sleeve versus once in total" quantity. (b) The **overlap/dilution pair** described in
  the companion note: the names a mix holds that a composite would not, and their composite rank.
- **Grade the magnitude down before using it in any hypothesis.** It is a simulation output, from an
  abstract, in a single market, with the authors' own optimum as the denominator, and no costs. The
  mechanism transfers; the fraction does not.

## Related

- `notes/2026-11-23-exposure-matched-blend-comparison-and-the-active-risk-crossover.md` — the
  peer-reviewed result that the mix-versus-composite ranking crosses over in active risk, which this
  efficiency comparison (measured against an unconstrained-optimum denominator) does not capture.
- `notes/2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` — the construction that
  tries to recover part of this gap inside a mix, plus the turnover and extreme-risk costs this
  article does not price.
- `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` — the same mechanism (the long-only
  constraint discards the short half of each view) argued without the efficiency denominator.
- `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — the equivalence that makes the
  long-only truncation the *whole* source of the gap.
- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md`,
  `notes/2026-09-24-long-only-minimum-variance-composition.md`,
  `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the transfer-coefficient and
  long-only-geometry material by the same authors that this folder already holds (the 2002 and 2004
  transfer-coefficient primaries remain unobtained).
