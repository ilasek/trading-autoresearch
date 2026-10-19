---
title: "Deep Learning in Asset Pricing" — using the no-arbitrage moment condition as the learner's criterion function instead of a forecast error, and choosing adversarially which pricing errors the loss is allowed to ignore
authors: Chen, Pelger, Zhu
year: 2024
venue: Management Science 70(2), 714–750 (venue tier 1)
url: https://doi.org/10.1287/mnsc.2023.4695 (read as arXiv:1904.00745v6, `arxiv.org/pdf/1904.00745`)
citations: 394 (Crossref `is-referenced-by-count`, checked 2026-10-19). Semantic Scholar's DOI endpoint returns `not found` for `10.1287/mnsc.2023.4695` — the same miss pattern `research/README.md` records for tier-1 finance DOIs, and not evidence the paper is unindexed. The SSRN working-paper registration `10.2139/ssrn.3350138` separately carries 58.
sample_period: 1967–2016 (training 1967–1986, validation 1987–1991, out-of-sample test 1992–2016)
markets: US — all available CRSP stocks (~10,000 names), monthly, with 46 time-varying firm characteristics and 178 macroeconomic time series
tier: A
validation_overlap: false
published_post_2018: true
read: full text of arXiv:1904.00745v6 (11 Aug 2021, 41 pp.), `pdftotext -layout` → 297 KB of clean text, 1,830 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified. Sections I–III, the loss and architecture specification, the variable-importance discussion and the robustness summary were read; the Internet Appendix (`10.2139/ssrn.3600206`) was not. The typeset Management Science article is closed; the v6 preprint predates publication by three years, so section numbering and the venue's final numbers may differ, and nothing below relies on a figure's exact value.
---

## Mechanism

The third answer to the question the other two notes in tonight's cluster ask — *what should the
learner minimise?* — and the one with the strongest venue behind it.

The paper's own one-line statement of its innovation is "to use the fundamental no-arbitrage
condition as criterion function". The structure is worth stating carefully because the transferable
content is the structure and not the architecture.

**The objective.** No-arbitrage says `E[M_{t+1} R^e_{t+1,i}] = 0` conditionally, for every asset. That
single conditional statement implies **infinitely many** unconditional moment conditions: for any
function `g(·)` of the information set, `E[M_{t+1} R^e_{t+1,i} g(I_t, I_{t,i})] = 0`. Each choice of
`g` is a choice of *which portfolios, at which times*, the model is required to price — i.e. a choice
of **test assets**. Classical practice picks `g` by hand (indicator functions for 25 size/value
buckets, say); setting `g` to a constant reduces to minimising each stock's unconditional pricing
error. The paper's move is to make `g` a second learned function and solve

```
min_ω  max_g   (1/N) Σ_j  E[ (1 − Σ_i ω(I_t,I_{t,i}) R^e_{t+1,i}) R^e_{t+1,j} g(I_t,I_{t,j}) ]²
```

a minimax game: one network proposes a stochastic discount factor, the adversary proposes the
conditioning function under which that SDF prices worst, and they alternate. **Nothing in this loss
is a forecast error.** The authors are explicit: "A key element of our approach is to avoid estimating
directly conditional means of stock returns." The SDF weights are what is fitted; the risk loadings
then follow as conditional second moments `E_t[F_{t+1} R^e_{t+1,i}]`, which are far better estimable
than conditional first moments.

**Why the minimax rather than a fixed `g`.** This is Hansen–Jagannathan (1997), cited as the economic
motivation: if a candidate SDF is only a proxy and cannot price everything, then **minimising the
largest achievable pricing error is equivalent to finding the admissible SDF closest in a
least-squares sense**. Choosing `g` adversarially is the data-driven version of the field's own
research protocol — modeller proposes a factor model, adversary proposes the anomaly it misprices,
modeller revises — and Hansen–Jagannathan's conclusion that minimax estimation behaves well **under
misspecification** and yields SDFs with substantially less variation than conventional efficient GMM
is the reason to prefer it when the model is known to be wrong, which is always.

**Two design details inside the loss that carry more transferable content than the networks do.**

1. **The average is taken over `N · D` *instrumented stocks*, not over `D` managed portfolios.** With
   ~10,000 stocks and 8 instruments that is ~80,000 moment conditions rather than 8. The consequence
   the authors draw is the one worth copying: averaging squared pricing errors over all instrumented
   stocks means "our SDF will depend only on information that affects a very large proportion of the
   stocks, that is, systematic mispricing", and "the adversarial approach will only select instruments
   that lead to mispricing for most stocks." **The loss's aggregation level is itself a de-noising
   device**, and it is what stops the model chasing name-specific residuals. (They also note the
   all-stocks average upper-bounds the `D`-portfolio errors, so nothing is lost, and convergence is
   faster — the game closes after three rounds.)
2. **Each asset's moment condition is weighted by `√T_i / √T̄`.** The panel is unbalanced; moment
   convergence is `1/√T_i`; so moments estimated more precisely get more weight and assets observed
   only briefly get less. This is a principled answer to a question this lab's panel poses acutely
   and has so far answered implicitly.

## Construction recipe

**The objective, stated so it can be ported without the deep learning.**

- Fit a function `ω(·)` mapping each name's characteristics (and shared state variables) to an SDF
  weight, with `M_{t+1} = 1 − Σ_i ω_{t,i} R^e_{t+1,i}` — i.e. the SDF *is* a long–short portfolio of
  the cross-section, with weights that are a single function of characteristics, constant across names
  and across time. (Note the structural identity with the parametric-portfolio-policy form in
  `2026-08-20-parametric-portfolio-policies.md`: weights as a fixed function of standardised
  characteristics. CPZ differ in what the function is chosen to minimise.)
- Choose the loss as `(1/N) Σ_i (√T_i/√T̄) · [ (1/T_i) Σ_t M_{t+1} R^e_{t+1,i} ĝ(I_t, I_{t,i}) ]²` —
  the weighted squared mean pricing error of each *instrumented* asset.
- Choose `ĝ` to maximise that same quantity, over a restricted, normalised class (the paper
  normalises instruments to `[−1, 1]`), then re-minimise over `ω`. Three alternations sufficed.
- The explicit comparator, run on the same data and the same features: a feedforward net minimising
  `(1/T)Σ_t (1/N_t)Σ_i (R^e_{t+1,i} − µ(I_t,I_{t,i}))²` — the Gu–Kelly–Xiu design, i.e. MSE on
  realised excess returns. The two differ *only* in the criterion (plus the adversary and the macro
  encoder), which is what makes the comparison informative.

**The machinery, recorded for completeness and mostly out of scope here.** Two-layer feedforward nets
for `ω` and for `g`; a separate LSTM for each, compressing the 178 macro series into **four** hidden
state processes; dropout rather than `l1`/`l2` ("generally better performance"); adaptive learning
rate; **ensemble averaging over nine fits from different random starts** for every network including
the forecasting benchmark, because a single fit depends on its initialisation (averaging beyond nine
adds nothing); hyperparameters — depth, width, number of macro states, number of instruments,
conditioning-network structure — tuned on the 1987–1991 validation split by maximising validation
SDF Sharpe. The selected model: two layers, four states, eight instruments.

**The macro-input lesson, which is a construction rule and not a result about one dataset.** Feeding
the 178 macro series as **last differences** is worse than leaving them out entirely: differencing
"loses all dynamic information and renders the macroeconomic time series essentially useless", and
including the degraded series makes it *harder* to separate signal from noise. The full time-series
dynamics have to be summarised (here by the LSTM) or the variables should be omitted.

## Robustness evidence (qualitative only)

- **The headline comparative result, and it is the chain's thesis in one sentence: the no-arbitrage
  objective produces a model that explains more return variation out of sample than a model whose
  objective *is* to maximise explained variation.** The authors put it as the no-arbitrage condition
  "disciplining" the model and yielding better results "among several dimensions". A loss can beat
  another loss on the other loss's own metric.
- **An off-the-shelf prediction net can lose to a *linear* no-arbitrage model.** "When used for asset
  pricing, off-the-shelf simple prediction approaches can perform worse than even linear no-arbitrage
  models." The binding constraint is the objective, not the flexibility of the functional form. This
  is the same conclusion `2026-10-19-learning-to-rank-cross-sectional-selection.md` reaches from the
  ranking side, where an MSE-trained net lands barely above random selection and below a one-line
  heuristic — two independent literatures, two different wrong objectives, the same failure.
- **The clearest diagnosis of *how* the MSE objective goes wrong, and it is the most useful paragraph
  in the paper for this lab.** Variable-importance sensitivities show all models agreeing that trading
  frictions and past returns are the leading categories — but the **MSE-trained** net's SDF loads its
  first fourteen characteristics almost entirely on frictions and past returns, heavily on short-term
  reversal, unexplained-volume illiquidity and size, "which raises the suspicion that a simple
  forecasting approach might focus mainly on illiquid penny stocks". The no-arbitrage model with
  adversarial test assets spreads its first twenty variables across all six anomaly categories. **The
  MSE objective's attractor is the illiquid micro-cap tail**, because that is where realised return
  variance — and therefore squared-error reduction — is largest.
- **Characteristics enter the SDF approximately *linearly* in isolation; the gain from flexibility is
  interactions.** This is the paper's second main finding and it is stated as a subtlety that also
  explains why linear factor models work as well as they do. Additive non-linear models (additive
  splines, kernels) therefore buy little; what they rule out, and what the network captures, is the
  multi-dimensional interaction.
- **Stability.** The *functional form* of the SDF estimated on 1967–1986 performs well on
  1992–2016 — a twenty-year-old fit applied twenty-five years later — and re-estimating on a rolling
  window produces an SDF highly correlated with the fixed one, with only minor improvement. Exposures
  move because characteristics move; the mapping does not. Results are reported robust to the tuning
  parameters (all validation-selected configurations "capture essentially the same asset pricing
  model") and to excluding small and illiquid stocks from the test assets or from the SDF, which is
  the robustness check that matters most for transfer to a large-cap panel.
- **Honest limits.** The SDF's positivity is not enforced (it happens to be positive in sample). The
  objective is only an *approximate* arbitrage condition in the Ross / Chamberlain–Rothschild sense.
  Convergence of the game is empirical, not proved. And the two failures of honesty that matter for
  grading: **transaction costs are not modelled anywhere** — every reported gain is gross, as in the
  two prior ML notes in this folder — and **multiple testing is not treated**, although the
  hyperparameter search is tuned on a held-out validation split rather than on the test sample, and
  the ensemble-of-nine is a genuine variance control rather than a search.
- **Replication status.** Not independently replicated as such, but the model is one of the
  architectures re-run by Avramov–Cheng–Metzker
  (`2026-09-03-machine-learning-economic-restrictions.md`), which is the closest thing to an external
  re-measurement the folder holds, and it is the established comparator in the ML-asset-pricing
  literature alongside Gu–Kelly–Xiu.

## Implementability here

**The model is out of reach; two pieces of the objective are free, and one is a warning that explains
a pattern this lab has already measured.**

What is out of reach, stated plainly so nobody plans around it: 46 firm characteristics and 178 macro
series are unavailable (`program.md`: no fundamentals), LSTMs and GANs are not in a scikit-learn plus
scipy stack, a nine-fit ensemble of randomly initialised networks collides with the causality check's
`1e-6` determinism requirement unless every seed is fixed, and the SDF as written is a **long–short**
portfolio while this lab is long-only with gross leverage ≤ 1 — so `M = 1 − Σ ω_i R_i` cannot be held
as a book at all. Do not attempt a port.

What transfers:

1. **The warning, and it is the most valuable item: an MSE objective on this panel is pulled toward
   illiquidity and short-term reversal, and both of those are already known dead ends here.** CPZ
   diagnose the pull as a property of the *objective*, not of the data. This lab has independently
   measured the destination: twelve sessions of `liquidity-volume` nulls [`learnings.md` 2026-09-25],
   a short-horizon cost wall on reversal objects (`SUMMARY.md` #18), and a standing finding that
   cross-sectional *level* scores on liquidity are confounded with the survivorship/level artifact
   [`learnings.md` 2026-08-31]. Worse, the micro-cap tail where the MSE objective's gradient lives is
   **excluded by construction** from a nine-large-cap-index panel, so on this universe an MSE learner
   is pulled toward a region that is simultaneously the wrong region and an absent one. **Any
   penalised-linear or tree candidate in `statistical-learning` fitted on squared forward-return error
   should be expected, a priori, to collapse onto the frictions-and-reversal block** — and that
   prediction is checkable for free from the fitted coefficients, before the trial is scored.
2. **Weight each name's contribution to the loss by `√T_i`.** This repo's panel is unbalanced in
   exactly the way the device is for: a column enters only once its name has been eligible, names
   leave on index deletion, and `program.md` records coverage of index members at 89–97% over
   validation against 40–66% over 1996–2008. An unweighted pooled loss therefore lets short-lived,
   thinly-covered early names move the fit as much as a name observed for twenty years. `√T_i/√T̄`
   weighting is one line, is motivated by the convergence rate rather than by taste, and is a free
   change to any learner the lab writes. It also sits beside — and is distinct from — the lab's own
   finding that a candidate's un-invested warm-up is charged against a fully-invested pool
   [`learnings.md` 2026-10-15/16]: that one is about scoring, this one is about fitting.
3. **The aggregation level of the loss is a de-noising choice.** Averaging squared errors over *every*
   instrumented name forces the fit onto structure that is common to most of the cross-section. The
   lab's analogue, available without any of the machinery: when evaluating a learned score, penalise
   its error on **every** eligible name rather than on a handful of extreme-decile portfolios, and
   expect the resulting fit to be duller and more systematic. This is the mechanism-level reason a
   model trained to price a few sorted portfolios can look excellent and select badly.
4. **Linear first, interactions second — and this is now a measured claim rather than a style
   preference.** `program.md` already instructs "prefer few features and a penalised linear model
   first"; CPZ supply the reason it is nearly right (characteristics enter approximately linearly in
   isolation) and the one specific thing it misses (interactions, not curvature). So the cheapest
   upgrade path from a penalised linear model on this panel is **pairwise products of a few
   standardised characteristics**, not a deeper or wider learner — and additive non-linear forms are
   explicitly the least promising direction.
5. **If macro state variables are ever added, do not feed last differences.** The panel's reachable
   macro-like inputs are ETF-derived series, and the temptation is to pass their latest change. CPZ
   measured that as worse than omission. Summarise the dynamics or leave them out. (Separately: v3's
   region-and-type-matched null means a *shared* state variable moves the replicas with the candidate
   and cannot by itself move the percentile [`learnings.md` 2026-10-13/14], so a macro state belongs
   in a candidate as a conditioner of cross-sectional selection, never as a timing signal.)

**Pitfall.** The paper's thesis is that an economically motivated objective beats a statistical one.
It is not that *any* reweighting of the loss helps, and the elicitability note in this cluster
(`2026-10-19-consistent-scoring-functions-and-elicitability.md`) is the check on that: CPZ's loss is a
squared *moment* condition — a well-posed GMM criterion with an identification argument behind it —
not a mean loss reweighted by the realisation, which Gneiting's Theorem 2.7 shows would silently
re-target a tilted distribution. The difference between those two things is the difference between
this paper and a mistake that looks like it.

## Related

- `2026-10-19-consistent-scoring-functions-and-elicitability.md` — the theory of what a loss elicits,
  and the discipline that separates a principled change of objective from a reweighting.
- `2026-10-19-learning-to-rank-cross-sectional-selection.md` — the same "wrong objective loses to a
  simple model" result from the information-retrieval side, on a decision this lab can actually run.
- `2026-08-29-machine-learning-cross-section-comparative.md` — Gu–Kelly–Xiu, whose best feedforward
  net is this paper's explicit comparator and whose objective is the one being argued against.
- `2026-09-03-machine-learning-economic-restrictions.md` — Avramov–Cheng–Metzker re-run this model
  among others and locate where learned-signal profitability actually lives; the closest thing to an
  external re-measurement of CPZ in this folder.
- `2026-08-20-parametric-portfolio-policies.md` — the same "weights as a fixed function of
  standardised characteristics" algebra, with realised utility rather than a pricing error as the
  criterion. The two together bracket the economic-objective family.
- `2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md` — the shrinkage route to an SDF over many
  characteristics, and the natural comparison for what the adversary buys over a penalty.
- `2026-08-26-skewness-and-concentration-of-stock-returns.md` and `experiments/learnings.md`
  2026-08-31 — why the MSE objective's attractor is the illiquid tail, and why that tail is both a
  dead end and absent on this panel.
