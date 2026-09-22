---
title: "Arbitrage Asymmetry and the Idiosyncratic Volatility Puzzle"
authors: Stambaugh, Yu, Yuan
year: 2015
venue: Journal of Finance 70(5) — Tier 1 (top peer-reviewed)
url: https://doi.org/10.1111/jofi.12286
citations: 1022 (OpenAlex, checked 2026-09-22); 924 (Crossref is-referenced-by-count,
  checked 2026-09-22). Semantic Scholar's DOI endpoint returns "not found" for this DOI —
  an index gap, not a low count; this is the third such miss recorded here in four sessions
  (Grinblatt–Han 2026-09-19, Cakici–Zaremba 2026-09-20). Read in full from the NBER
  working-paper version (w18560), which is the same paper.
sample_period: 1965–2011
markets: US equities (CRSP/Compustat)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the note that makes tonight's cluster actionable, because it is the one that says
what the **sign** of an arbitrage-risk effect should be, and it says the sign depends on
something.

Two ingredients:

1. **Arbitrage risk permits mispricing.** Idiosyncratic volatility is what an arbitrageur
   cannot hedge away, so higher IVOL deters the trade that would correct a price. Among
   **overpriced** names, therefore, the highest-IVOL ones are the *most* overpriced, and the
   IVOL–return relation is **negative**. Among **underpriced** names, the highest-IVOL ones
   are the *most* underpriced, and the relation is **positive**.
2. **Arbitrage asymmetry.** The impediments bear harder on the short side than the long
   side, so more of the potential *under*pricing has already been competed away. The
   positive branch is therefore compressed and the negative branch is not.

Aggregate the two branches over the whole cross-section and the negative branch dominates —
which is the observed "IVOL puzzle" (a negative unconditional relation between idiosyncratic
volatility and subsequent return) falling out as an artifact of pooling two effects with
opposite signs and unequal magnitudes. The data behave as predicted: a significant positive
IVOL effect among the most underpriced, a stronger negative effect among the most
overpriced, no monotone effect in the middle of the mispricing scale, and a negative effect
overall. The magnitudes are dated and deliberately not recorded here; the ordering and the
asymmetry — the negative branch several times the positive one — are the transferable part.

**Why the asymmetry exists**, argued from first principles rather than asserted, and this is
the part that is independent of any dataset:

- **Margin mechanics.** A position's margin ratio is `m = equity / position size`. After an
  identical adverse percentage move, a long and a short lose identical equity, but the
  long's *position size falls* while the short's *rises*. The short's `m` therefore
  deteriorates faster, and in practice maintenance requirements are stricter for shorts
  (FINRA: 25% long, 30% short). The authors work the arithmetic: an equally-margined long
  and short with the same maintenance requirement face a call at roughly a 33% adverse move
  versus a 20% adverse move respectively — and with the stricter short requirement, closer
  to 15%.
- **Compounding skewness.** Repeated adverse moves compound *against* a short (position
  grows) and *for* a long (position shrinks). Multi-period returns are positively skewed,
  which is tail risk for the short side. The authors work a lognormal example over an
  evaluation year and get a materially larger Value-at-Risk for the short.
- **Recall and squeeze.** A stock loan can be recalled, forcing closure of an
  eventually-profitable position. There is no long-side counterpart.
- **Population.** The institutions that short are small in aggregate relative to those that
  cannot; individuals essentially never short; and shorting costs rise with dispersion of
  opinion, i.e. precisely when shorting is most warranted.

None of these four depends on a sample. They are properties of the instrument.

A secondary result worth carrying: **mispricing is larger among high-IVOL names**, and the
difference between the overpriced and underpriced extremes widens with IVOL — with the
widening attributable mainly to the short legs. The corollary for a long-only operator is
uncomfortable: the names where the sort works hardest are the names whose profitable side
you cannot hold.

The paper also resolves a discrimination that `2026-09-22-limits-of-arbitrage-performance-based.md`
raises and cannot settle: Merton (1987) predicts high idiosyncratic risk earns *higher*
returns as rational compensation under segmentation; Shleifer–Vishny predict some high-IVOL
names are overpriced and earn *lower* returns. An unconditional IVOL sort cannot tell them
apart. Conditioning on the direction of relative mispricing can, and does: **the sign flips**,
which no rational-compensation story predicts.

## Construction recipe

**IVOL.** Following Ang–Hodrick–Xing–Zhang: regress the name's **daily** returns within the
most recent month on the three Fama–French factors (`MKT`, `SMB`, `HML`) and take the
standard deviation of the residuals. One month of daily data, refit monthly. Short window by
design — the measure is meant to be current, not stable.

**Mispricing measure.** For each of eleven anomalies, rank every stock each month so that
the **highest** rank goes to the anomaly value associated with the *lowest* subsequent
return in the published literature (so high rank = more overpriced). The composite is the
**arithmetic average of the eleven ranks**. The authors are explicit that this averaging of
*ranks* materially outperforms the alternative of averaging the eleven anomalies' *portfolio
returns* — and, consistent with the asymmetry thesis, almost all of that improvement lands
on the overpriced end.

**The double sort.** Each month: sort into five mispricing categories; within each, sort into
five IVOL categories; equal counts at both stages; value-weight within each of the 25 cells.
Read the IVOL effect *within* each mispricing row.

Robustness constructions the authors run and that any reimplementation should run too: an
**independent** two-way sort (common IVOL breakpoints across mispricing quintiles) in place
of the dependent one, and **equal-weighted** cells in place of value-weighted. Both reproduce
all three features — positive branch among the underpriced, stronger negative branch among
the overpriced, negative aggregate.

**Time-series conditioning** (optional, and unreachable here): split months on a market-wide
sentiment index and check that the negative branch strengthens when overpricing is more
likely and the positive branch strengthens when underpricing is.

## Robustness evidence (qualitative only)

- Three independent sort constructions (dependent, independent, equal-weighted) give the
  same qualitative picture, which is a stronger form of robustness than most cross-sectional
  papers report.
- The joint set of findings — sign depends on mispricing direction; each branch varies with
  the market-wide mispricing direction; both effects stronger on the overpriced side — is
  used by the authors as a discriminator against the six competing explanations of the IVOL
  puzzle they enumerate (disclosure, institutional ownership/shorting activity,
  idiosyncratic skewness, lottery preference, return reversal, volatility-factor loadings).
  Their argument is not that those channels are absent but that none of them predicts the
  conditional sign flip.
- The sign-flip result is independently reproduced by Cao and Han (2010), who also sort on a
  composite of anomaly rankings and also find negative (positive) IVOL effects among
  relatively overpriced (underpriced) stocks. Those authors do not find the *asymmetry*,
  which the present authors attribute to a difference in how the composite was built. So:
  the conditional sign flip has independent support; the asymmetry magnitude has less.
- Related corroboration from Jin (2012): long–short anomaly spreads are wider among
  high-IVOL names, and the widening is attributable primarily to the short legs.
- **Gaps against the rubric.** Single market (US). Transaction costs are **not** modelled at
  all, and the construction refits IVOL monthly on one month of daily data, which is the
  high-turnover end of the spectrum. Multiple testing is not formally treated. The
  mispricing measure is built from eleven already-published anomalies, so it inherits
  whatever selection those carry.

## Implementability here

**Read this section as an anti-candidate with one salvage, not as a recipe.**

**Why the obvious construction is forbidden here.** The headline transferable prediction is
that, *within the underpriced side of a cross-section*, high IVOL should earn more. A
long-only lab is always on the underpriced side by construction: it holds the top band of
its own score. So the literal instruction is "inside the champion's long leg, overweight the
high-idiosyncratic-volatility names". **On this universe that instruction is
indistinguishable from tilting into the identified survivorship artifact.**
`experiments/learnings.md` (2026-09-06 onward, fourteen mechanism screens) establishes that
21-day Garman–Klass volatility has the largest |IC| of any score in this repo with the
*wrong* sign — high volatility predicts high forward return — because the constituents are
current survivors. The literature's prediction and the artifact **have the same sign**.
A positive result would be uninterpretable, and `SUMMARY.md` #134 already forbids the
cross-sectional volatility sort for exactly this reason. **This note does not license an
exception; it is a second, independent reason to hold #134.**

That collision is worth stating in general form, because it is the useful output: *when a
literature's conditioning variable coincides with a universe's known bias channel, the test
is not merely noisy — it is unidentified, and no amount of care in construction fixes it.*
The fix has to change the variable.

**The one salvage, and it is free.** The paper's identifying evidence is not the level of
either branch; it is the **sign flip between them**. The artifact story predicts a positive
volatility–return relation *everywhere in this universe*, top band and bottom band alike,
because every name in the pool is a survivor. The arbitrage-asymmetry story predicts
**opposite signs** in the two bands of a mispricing sort. That is a genuinely discriminating
test and it costs no trial:

- Take a score the lab already holds. Split the universe into bands on it.
- Within each band, sort on idiosyncratic volatility — residual standard deviation against a
  universe-return factor (this repo has no `SMB`/`HML`; an equal-weight universe return, or
  a market-plus-region pair, is the available substitute and should be named as such).
- Compare the sign of the high-minus-low IVOL forward return in the **top** band against the
  **bottom** band, on train only.
- **Same sign in both bands → the artifact, and the vein closes for zero trials.**
  Opposite signs → the first evidence on this universe that something other than
  survivorship is moving with volatility, which would be worth more than any book this vein
  could produce.

This is the same shape as the lab's own per-arm identification rule (2026-09-19) and the
same shape as the 2026-09-20 ordered-ablation logic: an *ordered* prediction that the
confound cannot imitate, rather than a threshold the confound can clear.

**What cannot be built here at all**: the mispricing measure (ten of its eleven inputs are
accounting variables), the Fama–French residualisation (no `SMB`/`HML`), and the sentiment
conditioning (see `2026-09-22-anomaly-profits-short-leg-asymmetry.md`). A one-month daily
IVOL window is also at the fast end for a repo that charges 15 bps per side and rebalances
monthly; if the salvage test survives, any book built on it should use a longer window and
say why.

## Related

- `2026-09-22-limits-of-arbitrage-performance-based.md` — the theory, and the
  Merton-versus-Shleifer–Vishny discrimination this note resolves.
- `2026-09-22-anomaly-profits-short-leg-asymmetry.md` — the same authors' asymmetry from the
  sentiment side, and the long-only discount.
- `2026-09-22-arbitrage-risk-substitute-portfolios.md` — the arbitrage-risk variable that is
  a **ratio** rather than a level, and therefore the one of tonight's four that escapes the
  collision described above.
- `experiments/learnings.md`, 2026-09-06 onward, and `SUMMARY.md` #134 — the survivorship
  artifact and the standing prohibition this note reinforces rather than weakens.
- `notes/2026-09-01-max-lottery-extreme-positive-returns.md` — the competing lottery-preference explanation of the
  same IVOL fact, already covered here and already refuted by the lab.
