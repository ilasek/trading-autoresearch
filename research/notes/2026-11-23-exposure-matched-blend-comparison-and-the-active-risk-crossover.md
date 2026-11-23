---
title: "The mix-versus-integrate comparison CROSSES OVER in the level of active risk — the exposure-matched framework, the offsetting-exposure names only the mix holds, and why the crossover sits above where a long-only book is usually run"
authors: Ghayur, Heaney, Platt
year: 2018
venue: "Financial Analysts Journal 74(3), 70–85. Peer-reviewed; a tier-1 practitioner-academic venue in this folder's rubric (the same standing this folder gives FAJ elsewhere)."
url: https://doi.org/10.2469/faj.v74.n3.5
citations: "24 (Semantic Scholar by DOI, checked 2026-11-23); 18 (Crossref `is-referenced-by-count`, same DOI and date). The SSRN working-paper record `10.2139/ssrn.2895101` carries 1 — the usual preprint artefact."
sample_period: "1979-01 to 2016-06 (US tests). Nothing in the article touches 2017 or later."
markets: "US (Russell 1000, equally weighted), plus developed markets ex-US and emerging markets as robustness. Two-factor (value, momentum), three-factor (+ quality) and four-factor (volatility-exposure-adjusted) strategies."
tier: "B−. Peer-reviewed tier-1 practitioner venue, multi-region, and the design is the right one — exposure-matched books, so the two constructions are compared at equal factor exposure instead of at equal names. Held down because: **the body was not read** (CFA Institute member-only; every open route refused an automated client), so the method below is reconstructed from the published abstract plus the CFA Institute *In Practice* summary of the same article and is second-hand; all three authors are at Goldman Sachs Asset Management, which the article discloses offers products of **both** kinds; and turnover and transaction costs are not discussed at all."
validation_overlap: false
published_post_2018: false
read: "NOT read in full. Two pages read: the publisher's abstract page (`rpc.cfainstitute.org/research/financial-analysts-journal/2018/faj-v74-n3-5`, abstract only, article member-gated) and the CFA Institute *In Practice* summary of the article (`rpc.cfainstitute.org/research/financial-analysts-journal/2018/ip-v3-n1-11-comparing-portfolio-blending`), which carries the method, the mechanism and the regional robustness. Blocked: SSRN (`10.2139/ssrn.2895101`, Cloudflare challenge on the delivery endpoint), and `alphaarchitect.com`'s summary page returned HTTP 403 to an automated client."
---

## Why this source is here

This folder held two opposed claims about the construction the lab is about to need — combine the
family leads by **blending finished long-only books**, or by **blending their scores and building
once**. Fitzgibbons et al. (2017) argue the second wins because a long-only book discards the short
half of a view; Leippold–Rüegg (2018) reply that the evidence for it is a statistical fluke; and the
provider-authored article filed alongside this one argues the first wins once risk and
implementation are counted. None of the three is a test *at matched exposure*, and that is what
this one is.

Its result is the reconciliation: **neither construction wins outright — the comparison crosses
over in the level of active risk**, and the crossover is reported to sit *above* the exposure levels
at which long-only books are usually run.

## Mechanism

**The design: exposure matching.** The two constructions are built to carry **similar factor
exposures**, so the comparison is not confounded by one arm simply taking a stronger tilt. Both are
then run at a range of target tracking errors, from low to high. This is the control the earlier
sources in this folder lack: the practitioner literature's usual horse race compares a concentrated
single-pass book against a diluted sleeve blend and attributes the difference to the construction
when part of it is the tilt.

**The finding, stated as a crossover.** Portfolio blending (the mix of per-signal books) gives
"higher information ratios for low-to-moderate levels of tracking error"; at high tracking error
signal blending (one composite score, one pass) gives "better risk-adjusted performance". The
summary reports the low-exposure gap as statistically significant and as holding across the two-,
three- and four-factor combinations and across the regions tested. The direction at low exposure is
the opposite of the integration argument this folder already carries, and the direction at high
exposure is the same as it.

**The mechanism of the crossover is a statement about *overlap*, and it is the transferable part.**
At low target exposure the two constructions **hold mostly the same names**; what distinguishes them
is a residual set of "securities held only in the portfolio blend" — the names whose signal scores
*offset* each other, which an integrated composite screens out and a mix keeps because each sleeve
only sees its own signal. Those names are reported to **reduce active risk and improve active
return** at low exposure: that is, the dilution the integration literature treats as pure cost is
partly a diversification benefit, and at low active risk the benefit is the larger term. As the
exposure target rises the overlap shrinks, each book holds more names the other does not, and the
mix's advantage is "outweighed by greater stock-specific risk" — the integrated book is then the
better-diversified of the two per unit of active risk, which flips the ranking.

**The practical corollary the authors draw.** Factor exposure is, in their phrasing, "usually best
captured at low to moderate levels of return predictability", and investors generally avoid running
multifactor books at the high exposures where signal blending wins. So the regime in which the
integrated construction is better is the one practitioners are least often in — which turns the
familiar "you trade return for transparency by blending portfolios" framing on its head, since the
mix also gives per-signal attribution of active risk and active return that a composite score
destroys.

## Construction recipe

Reconstructed from the abstract and the *In Practice* summary; the body's parameter choices
(normalisation, selection breadth, rebalance cadence) were not readable this session and are
recorded as unknown rather than guessed.

1. **Signals.** Value and momentum (two-factor); + quality (three-factor); a fourth variant adjusts
   the three-factor book's volatility exposure. Scores are formed per signal cross-sectionally.
2. **Arm A — portfolio blending.** One long-only portfolio per signal, each built to a target
   exposure; hold the portfolios in a weighted mix (equal weights in the base case, as far as the
   summary indicates).
3. **Arm B — signal blending.** One composite score per security from the single-signal scores; one
   portfolio-construction pass on the composite.
4. **The matching step, which is the method.** Build each arm at a sequence of target active-risk
   levels and compare arms **only** at matched factor exposure. Report the comparison as a function
   of that level rather than at one point.
5. **Universe and benchmark.** Russell 1000, equally weighted, with the regional tests run on
   developed-ex-US and emerging-market panels.
6. **Not specified in what was readable, and not assumed here**: rebalance frequency, position
   bounds, whether the arms are optimised against a risk model or ranked-and-weighted, and any
   treatment of costs.

## Robustness evidence (qualitative only)

- **Sample.** Nearly four decades, monthly or finer, one large-cap US panel, with two further
  regions as out-of-sample checks. The regional and factor-count robustness is the strongest thing
  about the design and is reported as holding.
- **The comparison is contested in both directions in peer-reviewed venues**: this article's
  low-exposure result points the opposite way to Fitzgibbons et al.'s integration argument, and
  Leippold–Rüegg's rebuttal of *that* argument says neither construction dominates. The honest
  reading across all four sources this folder now holds is that the **ranking is a function of
  active risk and signal correlation**, that no source has settled its sign at a given point, and
  that the lab must therefore measure it rather than assume it.
- **Conflict of interest, disclosed in the article**: the authors' employer sells products built
  both ways, which is a weaker conflict than the provider-authored companion note's (where one arm
  *is* the firm's product) but a conflict nonetheless.
- **Not read in full.** The mechanism, the crossover and the regional robustness are second-hand
  from CFA Institute's own summary of the article. Treat the *shape* of the finding as reliable and
  any detail of implementation as unverified.
- **Anti-lookahead.** The summary carries dated performance levels (information ratios, active
  returns, active risks over 1979–2016) and **none is recorded here**; only the direction of each
  comparison and the existence of the crossover are. Sample ends mid-2016, so nothing in the omitted
  numbers could reach the lab's validation window.

## Implementability here

- **This is the source that tells the lab *which question to ask* about combining its leads.** Not
  "mix or integrate" but "**at what active risk am I running, and which side of the crossover is
  that?**" Under protocol v3 the lab's objective is already benchmark-relative — skill against the
  equal-weight eligible pool — so active risk is a quantity it can compute for any candidate it has
  stored, without a new trial.
- **The lab is almost certainly on the low-active-risk side, which argues for the mix.** A v3
  candidate is long-only, capped at 25%, graded against an equal-weight pool of ~1,000 eligible
  names; its realised tracking error against that pool is the relevant exposure measure. If it sits
  in the low-to-moderate band, this source predicts the **mix of leads beats the composite score** —
  the opposite of what the folder's existing integration note predicts, and the reason this note
  exists. Measure the band first; the folder's own `#508`–`#512` material gives the benchmark-relative
  machinery to do it.
- **The one free pre-trial measurement this source implies, and it is the lab's own `#60` sharpened.**
  Build both arms' *holdings* from stored lead scores at a handful of rebalance dates — no returns
  needed — and compute (a) the **name overlap** between the mix and the composite book, and (b) for
  the names the mix holds and the composite does not, their composite rank. This source says those
  two numbers are the whole mechanism: high overlap plus offsetting-score exclusives means the two
  constructions will be hard to separate and the mix will carry slightly less active risk; low
  overlap means the lab is on the far side of the crossover and the composite is the better bet.
  Holdings-only, costs nothing, and it predicts the sign of the comparison before a trial is spent.
- **What the crossover means for the de-concentration constants in `learnings.md`.** Those were
  measured by walking *down* a concentration dial inside one family on the v1 panel, i.e. by moving
  along the active-risk axis this source says the ranking depends on — with the construction held
  fixed. Read together, the two say the lab's "price of de-concentration" is not a constant of the
  lab but a **local slope**, and that its sign can differ between constructions at the same
  concentration. That is a reason to re-measure rather than to re-use, which `CLAUDE.md` already
  requires for v3 and which this source supplies an independent argument for.
- **What does not transfer.** Quality needs fundamentals; the volatility-adjusted fourth variant is
  a de-risking overlay of the kind `learnings.md` has refuted on this universe; and because the
  article discusses no turnover and no costs, its ranking is a **gross** ranking. Under v3's cost
  schedule the mix has a second, independent advantage this source does not price (its sleeves'
  trades net, and a selection-driven book churns less than a score-weighted one) — that argument has
  to come from the companion note, not from here.

## Related

- `notes/2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` — the provider-authored
  article arguing the mix wins once risk and turnover are counted, and supplying the filter that
  recovers part of integration's exposure advantage inside a mix.
- `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` — the integration argument this
  crossover bounds, and its peer-reviewed rebuttal. The three boundary conditions recorded there
  (signal correlation, active-risk target, signal count) are exactly the axes this article varies.
- `notes/2026-11-23-long-only-sleeve-mix-and-how-much-of-the-efficient-book-it-captures.md` — the
  theory of why a sleeve mix is not mean–variance efficient, which is a statement about the
  *unconstrained-optimum* comparison rather than about the mix-versus-composite comparison here.
- `notes/2026-11-22-enhanced-indexation-as-a-benchmark-relative-linear-program.md` — the
  benchmark-relative machinery with which the lab can compute the active-risk level this note says
  decides the question.
- `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — Novy-Marx's equivalence, which says
  mixing and integrating coincide for linear composites without truncation; this article's crossover
  is what the long-only truncation adds, measured at matched exposure.
