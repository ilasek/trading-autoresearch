---
title: "Capital Gains Overhang with a Dynamic Reference Point"
authors: Riley, Summers, Duxbury
year: 2020
venue: Management Science (Tier 1)
url: https://doi.org/10.1287/mnsc.2019.3404 — accepted version read from White Rose eprints, https://eprints.whiterose.ac.uk/id/eprint/146448/
citations: 18 (Semantic Scholar by DOI, checked 2026-09-19)
sample_period: daily data from January 1958; monthly market tests January 1963 – December 2016. The lab experiment that supplies the weights uses price charts sampled from the same 1963–2016 panel.
markets: US only — NYSE, AMEX and NASDAQ common shares (codes 10 & 11), NASDAQ volume halved for dealer double-counting, bottom market-cap decile dropped each month as a liquidity screen
tier: B
validation_overlap: false
published_post_2018: true
---

Read **in full** from the accepted-version PDF in the White Rose institutional repository — the
green-OA channel the README lists as reliable, first try. Management Science, 66(10), 4726–4745.

Third of three notes from 2026-09-19. The other two change *what is done with* the capital gains
overhang; this one changes **which price the investor is assumed to be comparing against**, and it
is the note that connects the vein to two objects this lab has already ruled on.

## Mechanism

Every reference-dependent asset-pricing model, Grinblatt–Han's included, assumes the reference
point is **fixed at the purchase price**. Prospect theory itself says no such thing: the reference
point is a free primitive of the theory and has received far less attention than the shape of the
value function around it. There is direct experimental evidence (Baucells, Weber and Welfens) that
reference points **adapt** as the price path unfolds, with intermediate prices mattering.

The claim here is that reference-point adaptation is (i) measurable, (ii) driven by a small set of
**salient points in the observed price chart**, and (iii) enough to improve a pricing model when
it is substituted into the overhang machinery. The economic content is unchanged from
Grinblatt–Han — a spread between price and reference point, closed by selling pressure from
holders who feel themselves in gain — but the register of "who is in gain" is rebuilt.

The salient points that carry weight, in the authors' own experiment, are the **purchase price**,
the **maximum** and **minimum** of the observed path, the **final (current) price**, and — the
extension over prior work — the **52-week maximum and minimum**. The average price does not
survive once collinearity is controlled. Adaptation is asymmetric: recent highs are more salient
than recent lows, consistent with a separate experimental literature finding that reference points
adjust more in gains than in losses.

## Construction recipe

**Step 1 — the weights are unchanged.** Same survival-probability weights as Grinblatt–Han, but on
a **daily** grid rather than weekly:

```
Ref_t = (1/k) · Σ_{n=1..1260} { V_{t−n} · Π_{i=1..n−1}[1 − V_{t−n+i}] } · X_{t−n}
g_t   = (P_t − Ref_t) / P_t              # P lagged one week against the reference point
```

with `V` = daily share volume ÷ shares outstanding. Daily turnover is described as strictly more
accurate than weekly and merely more expensive; the authors note this is now the common practice
in papers building on the model.

**Step 2 — swap the price `X` that the weights are applied to.** Grinblatt–Han use
`X_{t−n} = P_{t−n}`, the purchase price. Five alternatives are built, each evaluated **over the
life of that cohort's investment** — i.e. for shares bought `n` days ago, the maximum is the
maximum since `t−n`, not an unconditional maximum:

| Reference point | `X` for the cohort that bought at `t−n` |
|---|---|
| `RefPurchase` | the price at `t−n` (the original) |
| `RefMax` / `RefMin` | max / min price from `t−n` to `t` |
| `RefMax52` / `RefMin52` | 52-week high / low as seen by that cohort |
| `RefAverage` | mean price from `t−n` to `t` |

Each feeds the same `g` formula, giving `CGO`, `CGOMax`, `CGOMin`, `CGOMax52`, `CGOMin52`,
`CGOAverage`.

**Step 3 — the composites.** Weights come from the lab experiment (regressions of elicited
reference points on the chart's salient prices, selected across six specifications on R² and
variance inflation factors):

```
RefCom1 ∝ 0.33·Purchase + 0.29·Max   + 0.14·Min   + 0.23·Final
RefCom2 ∝ 0.43·Purchase + 0.45·Max52 + 0.11·Min52
```

each substituted for `X` inside the same weighted sum, producing `CGOCom1` and `CGOCom2`.

**Step 4 — the tests.** Monthly Fama–MacBeth cross-sectional regressions with the Grinblatt–Han
control set — momentum (12-month less the last month), short-term reversal (last month),
long-term reversal (3 years less the last year), average daily turnover over the last year, log
market cap — plus log book-to-market, and with dividend-record-date and earnings-announcement
indicators. Also double sorts of `CGO` against each composite, and regressions of forward trading
volume on the same variables. `CGO` and long-term reversal require a minimum of three years of
history out of the possible five, else set missing. Prices are split-adjusted before the overhang
is computed.

## Robustness evidence (qualitative only)

- **The purchase price is not special.** Each of the single-alternative overhangs — built on the
  maximum, the minimum, the 52-week maximum or the 52-week minimum — is reported as **an equally
  good predictor** of one-month-ahead returns as the original. The authors flag this as the
  surprising result, and it is: the object doing the work is *a* weighted summary of the price
  path, not specifically the cost basis.
- **The composites dominate in a joint test.** The traditional `CGO` is no longer a positive
  predictor once either composite is in the regression. In double sorts, `CGO` is rarely
  predictive after first sorting on a composite, while the composites generally remain predictive
  after first sorting on `CGO`. Same shape of evidence, and the same direction, as An's horse race
  against `CGO` in the neighbouring note — **two independent papers, modifying the base signal in
  two different ways, both report that their modification subsumes it.**
- **A second, non-return outcome moves the same way.** Forward one-week raw volume and forward
  abnormal volume are both more sensitive to the composites than to `CGO`. An effect that shows up
  in *trading* as well as in *returns* is harder to explain as a return-space artifact, and this is
  the note's strongest robustness row.
- **Moderators disagree with the neighbouring note, informatively.** Interacting the overhang with
  three speculativeness proxies, only **turnover** moderates it positively; **market
  capitalisation and idiosyncratic volatility do not moderate it at all**. The authors offer the
  model's own reading — high turnover is the rate at which the mispricing is closed, so
  Grinblatt–Han themselves predict expected return is increasing in the overhang *multiplied by*
  current turnover. Note the tension with An (own note), who reports the effect concentrated in
  small, high-volatility, low-institutional-ownership names: **on this sample, the size and
  volatility cuts are flat.** For a large-cap universe like this repo's, that disagreement is the
  difference between "the signal is absent here" and "it is fine here", and it is unresolved.
- **Weighting and subsample.** Results are reported robust to value-weighted regressions (weights
  = √market cap) and within the top-quintile-turnover subsample.
- **Rubric rows that fail, and one that is unusual.** Single market (US). **Costs are not
  modeled** — the string does not appear. Multiple testing is not formally addressed, and it
  matters more here than in the other two notes, because **the composite weights are selected**:
  six experimental specifications were compared on R² and VIF and two were carried forward into
  the market test. That is a specification search whose winner is then used as if pre-registered —
  precisely the object this folder's post-selection notes are about. Finally, the weights come from
  **169 lab participants** (109 male, 60 female, ages ~30–65) eliciting a neutral-feeling selling
  price on 30 real price charts. Real price paths are a genuine improvement in ecological validity
  over synthetic ones, and the exclusion rules are documented and cross-checked against an
  alternative outlier screen — but these are not the reference points of the marginal investor in a
  US equity, and the paper's market test inherits whatever the lab population's idiosyncrasies are.
  Tier B on venue and honesty; it does not reach A.

## Implementability here

**Why this note matters even though it is not the candidate.** It supplies three things the other
two do not: a **cheap variant ladder**, an explicit **tie to two objects this lab has already
ruled on**, and a **falsifiable claim about what is doing the work**.

**The claim to test, and it is nearly free.** If the maximum-based, minimum-based and
purchase-based overhangs are all equally good predictors, then the specific cost-basis story is
not what generates the prediction — some weighted functional of the past price path is. On this
universe that hypothesis has a cheap and decisive test: **build `CGO`, `CGOMax` and `CGOMin` and
rank-correlate all three against each other and against the trailing total return.** If they are
near-collinear here, the vein reduces to one signal and only one trial is warranted; if the
alternatives diverge, the paper's claim that they are interchangeable does not transfer, which is
itself a finding. Run this before choosing which overhang to spend the trial on.

**The 52-week-high connection must be stated plainly rather than discovered later.** `RefMax52`
and `RefMin52` are functions of the 52-week high and low, and the authors themselves connect their
result to George–Hwang. **This lab has tried 52-week-high proximity and refuted it.** So
`CGOCom2`, which puts 0.45 of its weight on a 52-week maximum, is **partly a re-run of a refuted
object** and should not be proposed as though it were new. `CGOCom1` (path max/min over each
cohort's own horizon, not a fixed 52-week window) is the genuinely different construction, because
the window length is cohort-specific and turnover-weighted rather than fixed at 252 days. If
anything from this note is trialled, it should be `CGOCom1`, and the journal should say in advance
that `CGOCom2` was declined for overlap with an existing refutation.

**It also answers a standing gap on the input side.** The 2026-09-18 input-side sweep recorded
that nothing in this folder is written about **`high`/`low` as a pair outside the range-volatility
estimators**. This is that note: the running maximum and minimum of a price path, used as a level
rather than as a range. Two implementation choices follow, and they should be separated. The paper
computes its extremes from the daily **closing** series; this repo has true intraday `aux["high"]`
and `aux["low"]`, so a cohort's maximum can be either the max close or the max intraday high.
**Use the max of closes**, matching the source, and treat the intraday version as a separate idea —
the intraday extreme is a different object (it embeds the bar's range, which this universe's
survivorship artifact loads on), and conflating them would make a failure uninterpretable.

**Constraints carried over from the base note.** No shares outstanding, so the turnover weights
need the `V_t = v̄ · vol_t / mean_{252}(vol_t)` substitute with a single pre-registered `v̄`;
missing volume fills to zero turnover; ETFs have no meaningful holder register; the multi-year
history requirement is a pool rule that selects on listing age. Two notes specific to this paper:
its **three-of-five-years** minimum is a more permissive pool rule than Grinblatt–Han's full five
and is the one to copy on a universe this small; and its **split-adjustment** step is unavailable
here in the direction that matters — the repo's prices are adjusted but its volume is a native
share count, so a split date misplaces weight, which is a defect to record rather than repair.

**One construction detail worth copying regardless of which variant runs.** The `RefCom1` weight
on the **final price** is 0.23. A reference point that partly *is* the current price mechanically
shrinks the overhang toward zero and damps the signal's cross-sectional spread; that is not a bug
in the source (it reflects real anchoring on the current quote) but it does mean the composite's
scale is not comparable with the base `CGO`'s, so any comparison between them must be done on
**ranks**, not on levels or on raw regression coefficients.

**Turnover as a multiplier, not just as a weight.** Both this paper and Grinblatt–Han report that
the overhang's predictive power improves when it is **multiplied by current turnover**, because
turnover is the rate at which the spread closes. Grinblatt–Han dropped that factor for parsimony,
and this paper's positive turnover interaction recovers it. On this repo the multiplier is cheap
(`vol_t / mean_{252}(vol_t)` needs no shares outstanding at all, since it is a ratio) and it is a
**one-parameter-free variant** of whatever overhang book is built. Keep it as the designed pair's
second arm rather than as a knob to tune.

## Related

- `research/notes/2026-09-19-capital-gains-overhang-reference-price.md` — the base construction
  whose reference price this paper replaces.
- `research/notes/2026-09-19-v-shaped-selling-propensity.md` — the other modification of the same
  base, and the one carrying tonight's candidate. The two modifications are orthogonal (one
  changes the price fed into the weights, the other changes how gains and losses are combined) and
  are composable in principle; do not compose them on a first trial.
- `research/notes/2026-09-15-inference-on-winners-post-selection-estimation.md` and
  `research/notes/2026-09-09-specification-curve-analysis.md` — the composite weights are the
  winner of a six-model selection, which is the object those notes are about.
- `experiments/learnings.md` — the 52-week-high-proximity refutation, which overlaps `CGOCom2`
  directly, and the standing finding that this universe's volatility/dispersion level is a
  survivorship artifact.
- `research/SUMMARY.md` — the 2026-09-18 open question on `high`/`low` as a pair, which this note
  partially closes.
