---
title: "Is There a Replication Crisis in Finance?"
authors: Jensen, Kelly, Pedersen
year: 2023
venue: Journal of Finance (tier 1)
url: https://doi.org/10.1111/jofi.13249 · full text read 2026-11-01 from NBER Working Paper 28432 (February 2021), https://www.nber.org/system/files/working_papers/w28432/w28432.pdf
citations: 513 (Crossref, checked 2026-08-25); 582 (Crossref, re-checked 2026-11-01). Semantic Scholar's DOI endpoint still returns a clean `not found` for this DOI (re-checked 2026-11-01) — third session in a row, and the note below treats it as that API's failure mode rather than an indexing fact.
sample_period: "US from 1926 (CRSP); non-US from Compustat, beginning 1986 for most developed countries, with a 60-month minimum per country-factor; 153 factors across 93 countries. Sample end read as 2019/2020 in the February 2021 working paper. (This corrects the \"global panel 1990–2020\" recorded on 2026-08-25, which was taken from the abstract rather than the data section.)"
markets: 93 countries, global equities, long-short characteristic factors
tier: A
validation_overlap: true
published_post_2018: true
---

## Mechanism

The empirical, finance-native realisation of hierarchical multiple testing — the third leg of session
11's open question (c), and the one that shows what happens when the idea is actually estimated
rather than derived. `research/README.md` names this paper in its own rubric as a replication
benchmark; it had never been read here.

**The frame.** A factor's alpha is measured against a CAPM benchmark (chosen because, unlike a
Fama–French benchmark, it is not mechanically related to the size and value factors being tested).
The prior is `α ~ N(0, τ²)` — the null is the *centre* of the prior, not a point being tested against
it. The posterior mean is then a shrinkage of the OLS estimate:

```
E(α | α̂) = κ · α̂,        κ = τ² / (τ² + σ²/T) = 1 / (1 + σ²/(τ²T))
```

Three readings, all portable and none requiring the paper's data.

**1. Shrinkage as a prior in units of time.** The posterior mean is exactly what you would get by
prepending `σ²/τ²` periods of observed zero alpha to your `T` periods of observed `α̂`. That converts
an abstract prior strength into a quantity anyone can argue about — "how many years of nothing would
I have to have seen first?" It is the cleanest statement of a prior's price the folder has come
across.

**2. Out-of-sample attenuation is the *prediction*, not the failure.** Because `κ < 1` strictly, a
Bayesian expects future alpha to be smaller in absolute value than the in-sample estimate, always.
Therefore a positive-but-lower out-of-sample result is the expected outcome of correct learning and
is *not* evidence of non-replication. The corollary they test cross-sectionally: if the effects are
real, higher in-sample alpha should still predict higher out-of-sample alpha across factors, and it
does. **This is a direct, mechanism-level statement about this repo's ⚠ standing protocol concern,
and it cuts partly in the gate's favour.** A candidate scoring lower on holdout than on validation is
the *base case*, not an anomaly, and any future reading of that table should stop treating the level
drop as the finding. What remains anomalous in the lab's ladder is a different shape entirely — the
rank correlation between the two splits flipping sign at an identifiable construction change, with
holdout moving monotonically *down* while validation moved monotonically *up*. Attenuation is
predicted; inversion is not. The concern survives, narrowed and better stated.

**3. Alpha-hacking gets its own two discounts** (Proposition 1). Model in-sample returns as carrying
an extra shock `u ~ N(ε̄, σ_u²)` that vanishes out of sample. Then
`E(α|α̂) = −κ₀ + κ_hacking · α̂`, where `κ_hacking = 1/(1 + σ̄²/(τ²T)) ≤ κ` and `κ₀ = κ_hacking · ε̄ ≥ 0`.
Hacking is punished twice and for two different reasons: it inflates the variance (`σ̄² = σ² + σ_u²`),
which shrinks the estimate harder, *and* it adds a mean bias, subtracted as an intercept. In the
"pure alpha-hacking" limit `κ_hacking → 0` and the observed estimate carries no information at all.
The mechanism worth keeping is that **searching adds noise as well as bias**, so a searched estimate
is discounted on a second axis that a bias correction alone would miss.

**4. Correlated evidence is worth less, with a formula** (Proposition 2). Observing the same factor in
a second market gives `E(α | α̂, α̂_g) = κ_g · ½(α̂ + α̂_g)` with
`κ_g = 1 / (1 + (σ²/τ²T)·(1+ρ)/2)`, decreasing in the correlation `ρ` and collapsing to the
single-market `κ` at `ρ = 1`. Two effects run at once: the two estimates are shrunk toward *each
other* and toward zero. This is the same fact the DSR literature expresses as "a tight family is
nearly one trial", derived from the other side and with a continuous knob instead of a count.

**5. The hierarchy, and the reversal it produces** (Proposition 3). Write `α_i = c + w_i` with `c` the
component common to all factors (`~N(0, τ_c²)`) and `w_i` idiosyncratic (`~N(0, τ_w²)`). The posterior
for factor `i` then depends on *every* observed alpha, decomposing into a shrunk average `α̂·` plus a
shrunk deviation `(α̂_i − α̂·)`, and the posterior variance of every alpha is strictly lower than in
isolation and decreasing in `N`. The empirical implementation adds a level:
`α_i = α_o + c_j + s_n + w_i` — a dogmatic zero overall component, a theme-cluster component, a
characteristic component shared across regions, and an idiosyncratic residual, giving prior
covariance `Ω = MM′τ_c² + ZZ′τ_s² + Iτ_w²` for membership matrices `M`, `Z`.

The reversal is the paper's headline and is a claim about the *sign* of an effect, not its size.
Under a frequentist correction, more related tests means a higher bar and fewer discoveries. Under
the joint hierarchical model, more related tests means the common component is estimated more
precisely, so **a large family of related strategies is partly evidence rather than only a penalty**.
The two forces genuinely oppose: the zero-alpha prior imposes conservatism (fewer discoveries), the
borrowed strength tightens every posterior (more discoveries), and which dominates is an empirical
question with no general answer. In their data the two roughly offset. They quote Gelman–Hill–Yajima
approvingly: "the problem of multiple comparisons can disappear entirely when viewed from a
hierarchical Bayesian perspective" — an overstatement the authors' own decomposition immediately
qualifies, since the disappearance is contingent on which force wins.

**6. The taxonomy.** Their answer to "the factor zoo is too big" is that it is not a zoo of hundreds
of distinct things but a modest number of themes — an algorithmic clustering into 13, with high
within-theme return correlation and economic-concept similarity and low across-theme correlation.
Most themes replicate; when the theme portfolios are put together, most of them enter an ex-post
tangency portfolio with positive weight. The mechanism claim is that within a theme there are many
detailed configuration choices for one economic concept, which is exactly why within-theme factors
are highly correlated — and hence why the theme, not the factor, is the natural unit.

**7. Publication bias is handled by where the prior comes from.** Because prior hyperparameters are
fitted by empirical Bayes to a literature that only published its winners, the prior itself inherits
the bias. Their fix is to estimate the prior from data *not* subject to selection — out-of-sample
periods, or externally supplied estimates — which shrinks full-sample alphas harder. The structural
lesson transfers even though the specific fix does not: **an empirical-Bayes prior fitted to a
selected record is an optimistic prior**, and the repair is to source the prior from outside the
selection.

## Construction recipe

Not a strategy recipe — an inference recipe, recorded because it is the concrete form the previous
two notes' machinery takes when someone actually builds it.

1. Choose a benchmark not mechanically related to the things being tested; estimate each candidate's
   alpha and residual volatility against it.
2. Partition candidates into themes by an algorithm, not by hand: cluster on return correlation and
   concept similarity so that within-theme correlation is high and across-theme correlation low.
3. Specify the hierarchy as additive components — global, cluster, characteristic, idiosyncratic —
   each with its own prior variance, giving the block-structured prior covariance `Ω` above.
4. Fit the prior variances by empirical Bayes, but source them from data outside the selected record
   if the record was selected; add explicit extra conservatism and report the sensitivity.
5. Report the posterior distribution, not a point estimate — from it, read off the posterior FDR, the
   expected fraction of true effects, and credible intervals for both.

## Robustness evidence (qualitative only)

Tier-1 venue, heavily cited for its age, multi-decade US sample extended to a broad international
panel, with the model, the taxonomy and the data construction documented at length. The paper is
itself a replication study and engages its opponent's construction choices directly rather than
around them. Its central empirical result — that the large majority of published factors survive,
against roughly a third in the study it responds to — is a *meta-statistic about a literature*, not a
performance figure about any tradable book, and is recorded here on that basis; no factor's returns
in any period are recorded in this note. Costs are not the paper's subject and are not modelled;
the factors are long-short and characteristic-sorted.

Two honest weaknesses. The result is sensitive to the prior in a way the authors are candid about:
adding conservatism moves the replication rate by several percentage points, so "does finance
replicate?" is partly a question about `τ`, and different reasonable priors give different answers
without anyone being wrong. And they report that out-of-sample attenuation in the data is *somewhat
stronger* than their own model predicts, which they attribute to arbitrage or residual data mining —
i.e. the model does not fully explain the decay it exists to reinterpret.

**Lookahead flags matter here more than usual.** The sample runs to 2020 and the paper was published
in 2023, so `validation_overlap: true` and `published_post_2018: true` both apply. Only the
*mechanism* is carried above. No period-specific performance figure, no claim about what worked
when, and nothing from after 2023 appears in this note or should be inferred from it.

## Implementability here

**Explanatory only, and doubly so** — it needs fundamentals (book-to-market and the rest), long-short
construction, and a factor-alpha benchmark, none of which this repo has, and its conclusions concern
a published literature rather than a portfolio. The engine is frozen. What transfers is machinery and
one correction.

**1. The correction, and it is the most useful thing in this session.** The lab's ⚠ standing protocol
concern has been recorded partly as "validation and holdout disagree, and holdout keeps falling".
This source says the *level* fall is predicted by correct Bayesian learning under any positive
shrinkage, so it carries no information on its own — the estimate you promoted on was optimistic by
construction, and a smaller number afterwards is what optimism-corrected means. The part of the
concern that survives this is the part that was always the real evidence: a **sign flip in the
relationship** between the two splits at an identified structural change, with the two series moving
monotonically in opposite directions across a run of promotions. Future statements of the concern
should lead with the inversion and drop the level drop, which is now sourced as expected. This
narrows the case and makes it harder to dismiss, which is the point.

**2. The trial-count fact the repo has been observing locally now has a formula.** `learnings.md`
records DSR clustering — 11 effective trials against 45 recorded — as a local observation about the
deflator. Proposition 2's `κ_g` is the same phenomenon with a knob: evidence from a correlated second
look is discounted continuously in `ρ`, collapsing to no new information at `ρ = 1`. The repo's
within-family ladder is the high-`ρ` regime, so the local observation is not an artifact of the DSR's
particular clustering estimator; it is what any joint model would say.

**3. The reversal, offered as a lens and explicitly not as licence.** Under a hierarchical model, a
family of correlated candidates can be collectively more convincing than any member alone. It is
tempting to read that as "the lab's ladder of near-miss buffered-momentum variants is corroborating
evidence rather than multiple testing". **That reading is not available here**, for three stated
reasons: the gate is frequentist and frozen; the hierarchical gain comes from *borrowing strength
across weakly-correlated units*, whereas the repo's ladder is near-perfectly correlated variants of
one construction, which is precisely the `ρ → 1` case where the formula says the extra evidence is
worth nothing; and the conservative half of the trade-off (heavier shrinkage) applies regardless
while the informative half does not. The honest summary is that the hierarchical framing would treat
this repo's *families* as the unit and its within-family variants as one observation — which is the
same conclusion the DSR clustering already reached.

**4. The two-discount reading of search.** Proposition 1's separation of hacking into a variance
inflation and a mean bias is worth carrying into how the lab reads its own record. The variance term
means that a candidate found by trying many configurations should be discounted *even if* one
believes no explicit bias was introduced, because the search itself made the estimate noisier. The
lab's magnitude-weighting ladder and buffer-width choices are the natural place this applies.

**5. The taxonomy point, and it is actionable at zero cost.** The unit of both shrinkage and
weighting should be an algorithmically-defined cluster with high within-correlation, not an
individual candidate. `program.md`'s seven families are a hand-authored version of exactly that
object. Nothing needs to change; but any future journal entry that reasons about "how many things
have we really tried" should reason at the family level, and the folder's other two notes this
session both independently require the same grouping.

**Pitfalls.** (a) Do not import the replication rate as a statement about what works; it is about a
published literature, on data this repo does not have, over a window that overlaps validation.
(b) The prior sensitivity is real — any argument of the form "the Bayesian view says X" is an
argument about a chosen `τ`. (c) The out-of-sample attenuation result assumes the in-sample estimate
was the thing selected on; in this repo it was, which is why the point applies, but it is not a
general licence to expect decay everywhere.

## Addendum — 2026-11-01: the breakouts by size group, region and theme, read from the full text

The 2026-08-25 note was written without the paper's empirical breakouts. Session 79 read the full
text (NBER WP 28432) specifically to answer the question the [2026-10-31] open question had posed —
*which of this folder's filed mechanisms should be expected to survive on nine large-cap developed
indices, rather than asserted* — and the paper does report the three things that question asked for.
Recorded here rather than in a new note, per `research/README.md`'s rule on revisiting a source.

**(a) By size group: replication is NOT a small-stock phenomenon, and this is the strongest
available answer to the pessimistic reading.** Factors rebuilt from five US size subsamples defined
on NYSE breakpoints — mega (top 20%), large (80th–50th), small (50th–20th), micro (20th–1st) and
nano (below the 1st percentile) — give empirical-Bayes replication rates of **77.3% (mega) and
81.5% (large)** against **84.0% for the full US sample**, with micro at 81.5% and nano at 71.4%.
The authors' conclusion is that "criticisms of factor replicability based on arguments around stock
size or liquidity are largely groundless". More useful than the rates: the **cluster-level alpha
ordering is broadly similar across size groups**, with a Spearman rank correlation of **73% between
mega-cap and micro-cap cluster alphas** and only the nano sample deviating (35% against mega).

  **What this does and does not license for this repo.** It is direct evidence that *most* of this
  literature is not a microcap artefact, so `research/README.md`'s clause — a null here is
  uninformative for a mechanism the literature localises to small, thin or retail-held names —
  should be applied **narrowly**, to the mechanisms whose own literature localises them, not as a
  blanket excuse for a large-cap panel. It does **not** overturn the cross-sectional-dispersion
  fact from `notes/2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md`: the *existence*
  of these effects survives into mega-caps; their *magnitude* is still largest where dispersion is
  largest. Both can hold, and the reconciliation is that a large-cap panel compresses the spread
  without removing the sign.

**(b) By theme: three of the thirteen fail, and one of the three is a `program.md` family.** Ten of
13 themes replicate at **75% or better** under the Bayesian estimates. The exceptions are
**seasonality, leverage and size** — and the paper explains two of them rather than leaving them as
noise. *Size* is stronger in emerging markets and in micro and nano stocks, which the authors tie to
the illiquidity-premium theory: the premium should scale with trading-cost differences, and those
differences are much larger in emerging and micro names. *Leverage* fails on CAPM alpha but becomes
**one of the most heavily weighted clusters** once other themes are controlled for, through its
hedging of the value and low-risk clusters — i.e. its failure is a benchmark artefact, not an
absence. **Seasonality is left unexplained and is simply weak.**

  **This matters for the lab's own record.** `seasonality-calendar` is the family this lab has spent
  the most recent effort on, and its results there are a run of region-matched nulls and one
  mechanism closed on cost arithmetic. The weakest theme in the largest Bayesian replication study
  of this literature is **the same family**. That is independent corroboration of the lab's own
  nulls rather than a reason to keep looking, and it should be read alongside the standing
  correction that this folder's "significantly inverted" seasonality discount was withdrawn by the
  lab on 2026-10-15 and is a **null**, not an inversion.

**(c) By region, and the ordering is the actionable part.** Cluster-level alphas across US,
developed-ex-US and emerging are broadly consistent, with Spearman rank correlations of **71%
between US and developed-ex-US** and **48% between US and emerging**. The standout exception is the
**size theme**, far more important in emerging markets than in developed ones. Separately, raw OLS
replication rates in developed and emerging markets are **lower** than in the US, and the
frequentist Benjamini–Yekutieli correction hits them especially hard, while the Bayesian posterior
conditioned on the global cross-section recovers much of the loss by borrowing precision across
regions.

  **Two consequences.** First, this repo's panel is nine **developed** large-cap indices, and the
  relevant correlation is therefore the 71% one, not the 48% one: a mechanism filed from US
  evidence should be expected to rank similarly here, which is a materially more favourable prior
  than this folder has been assuming. Second, the per-region OLS rates being lower is partly a
  **sample-length and breadth** effect — the paper requires at least 5 names per leg and 60 monthly
  observations per country-factor, and the non-US panels are shorter — which is the same
  thin-cross-section friction stated as a mechanism in
  `notes/2026-11-01-anomalies-across-the-globe-country-neutral.md`.

**(d) The construction choices, now recorded, because they are the measurement.** Terciles, not
deciles. Breakpoints computed on **non-micro names only** (above the NYSE 20th percentile), with
micro-caps then distributed into those same buckets rather than setting the cuts. **Capped
value weighting** — market equity winsorised at the NYSE 80th percentile — chosen so that neither
tiny names nor a single mega name dominates (their stated example: one stock was over 70% of a
national market's capitalisation). Accounting data assumed public **four months** after fiscal
period end. A four-quarter aggregation of quarterly flow items to defuse business seasonality.
Valuation ratios always on the most recent price. Factors signed as the original paper claimed.
At least 5 names per leg, at least 60 monthly observations per country-factor, at least 3 countries
for a regional aggregate; country factors aggregated **capitalisation-weighted**. Performance-based
delistings assigned **−30%** where delisting returns are unavailable. Themes formed by
**hierarchical agglomerative clustering with Ward linkage on `1 − correlation` of CAPM-residual
returns**, cut at 13 clusters; within-cluster average pairwise correlation exceeds 0.5 in 10 of 13.

  The decomposition of their gap against the pessimistic study is construction, item by item:
  longer sample **+4.3**, one holding period instead of three **+4.0**, **capped value weights
  +8.5**, 15 added factors **+2.4**, other construction details **+2.7**, excluding factors the
  original papers found insignificant **+7.8**, and **CAPM alpha instead of raw return +20.2**
  percentage points. **The single largest term is not a construction choice at all — it is testing
  the right statistic.** The folder's general form of this is in
  `notes/2026-11-01-reproduction-versus-replication-open-source.md`.

**(e) The alpha-hacking test, and the shrinkage benchmark it is run against.** The paper embeds
hacking as an in-sample return inflation with both a mean bias and an extra variance, and shows the
posterior then becomes `E(α|α̂) = −κ₀ + κ_hacking · α̂` with `κ_hacking ≤ κ` and `κ₀ ≥ 0`: pure
hacking implies a **zero slope and a negative intercept** in a cross-sectional regression of
out-of-sample alpha on in-sample alpha. Empirically the slope is **significantly positive and the
intercept is positive**, so pure alpha-hacking is rejected. But the slope is also **well below the
Bayesian benchmark**: with no hacking and no arbitrage the expected slope is

```
κ = 1 / (1 + σ²/(T τ²))
```

which their own empirical-Bayes hyperparameters put at about **0.9**, against realised slopes
materially lower, plus a concave shape in the scatter. Their reading: not p-hacking, but the
**highest in-sample alphas** are either data-mined or arbitraged down.

  **This is a usable screen and it is the sharpest form of the "shrink, don't re-threshold" idea
  this folder holds.** The formula is the one already in this note's Mechanism section, now with its
  two inputs identified: `τ` is the **cross-sectional dispersion of true effects in the candidate
  population**, estimable by empirical Bayes from the dispersion of measured effects net of sampling
  noise, and `σ²/T` is the sampling variance of one measurement. The lab's analogue is immediate:
  given a candidate's measured skill and the dispersion of skills across its own recorded trial
  population, the **expected forward skill is `κ × measured`, with `κ < 1` always**, and the
  concavity result says the shrinkage should be **heavier at the top of the distribution** — i.e.
  heaviest for exactly the candidate a session wants to promote. Two cautions that are this
  folder's: the magnitudes `τ_c ≈ 0.38%` and `τ_w ≈ 0.21%` per month are properties of *their*
  factor population and must not be carried here (the required re-measurement is on this lab's own
  trial record); and estimating `τ` from the lab's record is only honest because that record is
  **uncensored**, which is the precondition `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md`
  shows the published literature fails.

**(f) One correction this addendum owes the 2026-08-25 text.** The frequentist comparison the
original note reports — that the Benjamini–Yekutieli correction cuts the replication rate sharply
while the Bayesian treatment does not — must now be read with the result that **BY Theorem 1.3 is
isomorphic to assuming a false-factor share of about 6.3 at this study's factor count**, an
impossible value, and therefore *always* raises the hurdle. The size of that gap is substantially a
property of the chosen frequentist algorithm rather than a measurement of what multiple testing
costs. See `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md`, item 4.

**(g) What still is NOT in this paper, and it is the binding one.** **Costs are not modelled** —
the phrase "transaction cost" appears once, in a theory aside about the size premium. Every
replication rate above is a statement about a **gross long-short factor return's statistical
significance**, not about tradable alpha. A theme replicating at 84% says nothing about whether it
survives v3's 15/20/30/40 bps tiers plus UK and Hong Kong stamp duty and the continental FTTs. The
whole replication debate — all three corners of it — is pre-cost, and the cost third is estimated
elsewhere (`notes/2026-10-14-net-expected-returns-of-the-anomaly-zoo.md`,
`notes/2026-11-01-reproduction-versus-replication-open-source.md`).

## Related

- `notes/2026-11-01-reproduction-versus-replication-open-source.md` — the "pure reproduction"
  complement this paper names in its own introduction, and the source of the construction-elasticity
  magnitudes that addendum item (g) says are missing here.
- `notes/2026-11-01-anomalies-across-the-globe-country-neutral.md` — the international
  post-publication study this paper cites, and the country-neutral construction convention behind
  addendum item (c).
- `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md` — the identification argument behind
  addendum items (e) and (f), and the reason the shrinkage half of this paper's machinery is the
  transferable half.
- `notes/2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — the study this one
  responds to, read here in full on 2026-10-02; addendum items (a) and (d) are the reconciliation.
- `notes/2026-08-25-prior-weighted-multiple-testing.md` — the grouped "sieve" weighting scheme this
  paper's theme taxonomy realises empirically: partition into economically coherent clusters,
  estimate at the cluster level, so no single test can up-weight itself.
- `notes/2026-08-25-bayesianized-p-values-prior-odds.md` — the same Bayesian logic applied to a single
  hypothesis with an explicit prior, and the source of the "raise the threshold" position this paper
  argues is unnecessarily crude. The two disagree in emphasis and both are tier A; the disagreement
  is recorded rather than resolved, and its substance is whether related tests are penalty or
  evidence.
- `notes/2026-08-24-deflated-sharpe-ratio.md` and `notes/2026-08-24-multiple-testing-haircut.md` — the
  frequentist corrections this paper calls "unnecessarily crude", including the Benjamini–Yekutieli
  procedure it benchmarks itself against.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the decay result this paper reinterprets:
  post-publication attenuation as Bayesian learning rather than as failure.
- `experiments/learnings.md` — the ⚠ standing protocol concern (point 1 above narrows it) and the DSR
  clustering observation (point 2 above supplies its formula).
