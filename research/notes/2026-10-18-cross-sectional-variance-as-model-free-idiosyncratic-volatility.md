---
title: "The cross-sectional variance of returns as a model-free estimator of average idiosyncratic variance (and what its biases are)"
authors: Garcia, Mantilla-García, Martellini
year: 2014 (published); working paper read is CIRANO 2013s-01, January 2013
venue: Journal of Financial and Quantitative Analysis 49(5–6), 1133–1165 — venue tier 1, peer-reviewed. The version read is a CIRANO Série Scientifique discussion paper (venue tier 2)
url: https://doi.org/10.1017/S0022109014000489 · working paper read at https://depot.erudit.org/dspace/bitstream/003867dd/1/2013s-01.pdf
citations: 70 (Crossref `is-referenced-by-count`, checked 2026-10-18); 77 (OpenAlex, same date); Semantic Scholar's DOI endpoint answers `Paper with id DOI:10.1017/s0022109014000489 not found` for this indexed DOI — the third S2 failure mode `research/README.md` records, seen again
sample_period: July 1963 – December 2006 (longest sample); monthly model-based comparators built from daily returns over the same window
markets: United States only — CRSP common equity shares, stocks with a missing return or non-positive market capitalisation at the start of a month dropped. Firm count ranges 377 to 7,293 and is above one thousand in 75% of months. International data is explicitly left to further research
tier: A for the estimator theory (Propositions 1–4 are theorems about a cross-sectional average, not empirical regularities, published in a tier-1 journal); B for everything empirical, which is one country and one database
validation_overlap: false
published_post_2018: false
read: full text of CIRANO 2013s-01 (January 2013), fetched first try from `depot.erudit.org/dspace/bitstream/003867dd/1/2013s-01.pdf` (HTTP 200, 399 KB) and parsed with `pdftotext -layout` into 134 KB of text, 956 instances of `" the "`, no ASCII shift. The `( )`-dropout check returns **three** hits, all of them the same artifact: the extractor drops `1/N_t` out of the big-O condition `Σ w² = O(1/N_t)`, which the surrounding prose restates in full ("the existence of a constant C_t such that Σ w² ≤ C_t/N_t"), so no page image was needed. The published JFQA version was not fetched (Cambridge's PDF endpoint answers an automated client with an HTML bot page, per `research/README.md`); the working paper's abstract and the published abstract agree on all four headline claims used below. Table values are present in the extract and **no empirical magnitude from them is recorded here**, per the anti-lookahead rule.
---

## Mechanism

There is no return premium in this paper. It is a **measurement** result, and it is the cheapest
measurement result this folder has filed: it says that a quantity the lab can compute in one line
from one row of its own price panel — the cross-sectional variance of that day's returns — *is* an
estimator of average idiosyncratic variance, with a stated bias, a stated variance, and a stated
condition under which it works.

The setup is a one-factor return model, `r_it = α_it + β_it F_t + ε_it`. Define, for any strictly
positive weighting scheme `w_it` summing to one,

    CSV_t(w) = Σ_i w_it ( r_it − r_t(w) )²,   where  r_t(w) = Σ_i w_it r_it

i.e. the weighted cross-sectional variance of the day's returns about that day's weighted mean
return. **Proposition 1**: under homogeneous betas (`β_it = 1 ∀i`) and homogeneous residual
variance (`E[ε²_it] = σ²_ε(t) ∀i`), for any weighting scheme satisfying `Σ_i w²_it = O(1/N_t)`,

    CSV_t(w) → σ²_ε(t)  almost surely as N_t → ∞.

Two properties follow and they are the reason to care. **It is model-free**: no residuals, no
factor model, no betas, no covariance matrix, nothing estimated. **It is observable at any
frequency**: it is a statistic *of one cross-section*, so a daily series needs one day of data per
point, where every model-based measure of aggregate idiosyncratic volatility needs a time-series
window per point and is therefore monthly at best. Those two advantages are the paper's whole
claim to existence, and both of them transfer to this lab intact.

The economic reading the authors attach — that average idiosyncratic variance proxies for the
investment opportunity set, in the Levy/Merton/Malkiel–Xu class of models where investors are not
fully diversified — is a separate and much weaker claim, and the paper is honest that the
empirical literature on it is unsettled in both directions (Goyal–Santa-Clara against Bali–Cakici–
Yan–Zhang and Wei–Zhang on aggregate prediction; Ang–Hodrick–Xing–Zhang's negative sign against the
theories' positive one at the stock level). **Take the estimator; treat the pricing story as an
open question that this paper does not close.**

## Construction recipe

- **The statistic.** One cross-section of simple returns, one weight vector, two lines:
  `r_bar = Σ w·r`, then `CSV = Σ w·(r − r_bar)²`. Nothing is fitted. Use **equal weights**: see the
  efficiency result below. At equal weights `r_bar` is the equal-weighted pool return.
- **Which weights are admissible.** Any strictly positive scheme with `Σ_i w²_it = O(1/N_t)` —
  equivalently, a constant `C_t` with `Σ w² ≤ C_t/N_t`. Equal weighting satisfies it with `C_t = 1`.
  The condition exists to **rule out concentrated weight vectors**; cap-weighting may or may not
  satisfy it depending on how the weight distribution behaves as `N` grows, which is why the paper
  uses cap-weighting only for comparison.
- **The finite-sample bias, which is explicit and correctable.** Proposition 2:
  `E[CSV_t(w)] = σ²_ε(t)·(1 − Σ_i w²_it)`. The multiplicative factor is known in closed form from
  the weights alone, so the correction is a division — no estimation. At equal weights the factor is
  `(1 − 1/N_t)`, i.e. the familiar `N/(N−1)` small-sample correction and nothing more.
- **The variance.** Proposition 2 also gives, under multivariate-normal residuals,
  `Var[CSV_t(w)] = 2σ⁴_ε(t)·[ (Σ w²)² + Σ w² − 2 Σ w³ ]`.
- **Why equal weights.** Proposition 3: the EW scheme **minimises both the bias and the variance**
  over all positive weighting schemes, and both go to zero as `N_t → ∞`. The EW CSV is therefore
  consistent *and* asymptotically efficient within the class, and it dominates the cap-weighted CSV
  as an estimator of average idiosyncratic variance. This is a theorem, not a preference.
- **Heterogeneous residual variances cost nothing.** Relaxing `E[ε²_it] = σ²_ε(t)` leaves the CSV
  asymptotically unbiased for the *average* idiosyncratic variance of the universe. The paper states
  that this assumption "comes with no loss of generality".
- **Heterogeneous betas cost something, and it does not vanish.** Proposition 4:

      E[CSV_t(w)] = Σ w·σ²_ε,i(t) − Σ w²·σ²_ε,i(t) + E[ F²_t · CSV^β_t ]

  where `CSV^β_t = Σ_i w_it (β_it − Σ_j w_jt β_jt)²` is the cross-sectional variance of betas. The
  first two terms are the average idiosyncratic variance and the vanishing `(1 − 1/N)` bias. **The
  third term is a positive bias that survives `N → ∞`**, and it is the one thing that can make CSV
  something other than what it claims to be. Note its shape: it is beta dispersion *multiplied by
  the squared factor return*, so it is small on quiet days and large exactly on the days the factor
  moves hard. The bias is computable if betas are: the paper measures it directly with CAPM and
  Fama–French betas and reports (qualitatively) that it is not material on its US panel.
- **Aggregation to lower frequency.** Daily CSV is averaged within the month to produce a monthly
  series, and everything is annualised before daily and monthly measures are compared.
- **The free generalisation.** Because the object is a cross-sectional moment, the same construction
  extends to **higher cross-sectional moments** at no extra cost; the paper reports that the
  asymmetry of the cross-sectional return distribution is itself a predictor and flags a full
  treatment of cross-sectional skewness as the obvious next step.

## Robustness evidence (qualitative only)

- **Agreement with the model-based measures is essentially total.** Monthly CSV and the
  model-based aggregate idiosyncratic-variance series (CAPM residuals, Fama–French residuals, the
  Goyal–Santa-Clara measure, the Bali et al. measure) correlate above 99%, in both equal-weighted
  and cap-weighted form. This is a correlation between two *measures*, not a performance claim, and
  it is the strongest single argument for the estimator: a construction that needs no model
  reproduces the ones that do.
- **The beta-dispersion bias was measured rather than assumed away**, against two benchmark factor
  models, and reported as immaterial on a broad US panel. That finding is panel-specific, not a
  theorem, and the theorem says the bias does not vanish with breadth.
- **Replication status of the estimator**: the *estimator* has not been subjected to the
  large-scale replication projects (Hou–Xue–Zhang, Jensen–Kelly–Pedersen) because it is not an
  anomaly. The *predictive* claim it is used to support sits inside an openly contested literature
  that the paper itself lays out on both sides, and the paper's contribution there is to show the
  earlier monthly conclusions are robust to which measure is used — which cuts both ways.
- **Single market.** US only, one database, one share-type screen. The authors name international
  data as unfinished business. Treat any claim here as untested outside the US.
- **Methodology honesty**: high. Bias and variance are derived rather than asserted, the one
  non-vanishing bias is characterised and then measured, the weighting choice is justified by a
  theorem instead of by results, and the competing measures are reproduced rather than
  characterised. No transaction costs anywhere, but nothing here is a strategy.

## Implementability here

**Directly, cheaply and causally — this is a diagnostic, not a candidate.** On a rebalance date the
panel has roughly a thousand eligible names; `CSV_t` over the eligible set is two vector operations
on data the engine already hands `generate_weights`, uses only that date's row, and has zero fitted
parameters, so it cannot fail the causality check and costs nothing in runtime.

Four things decide whether it means here what it means in the paper.

1. **Compute it over the eligible pool, never over a held book.** The admissibility condition
   `Σ w² = O(1/N)` is precisely a ban on concentration, and this lab's books are concentrated by
   design: a `K`-name equal-weighted book has `Σ w² = 1/K`, so at `K = 20` the bias factor
   `(1 − Σ w²)` is 5% and the estimator is measuring the book, not the market. Over the ~1,000-name
   eligible panel the same factor is a tenth of a percent. **Pool-level object, pool-level weights.**
2. **Equal weighting is not a convenience here, it is the matched choice.** v3 grades skill against
   the **equal-weight eligible pool**, and the EW CSV is the cross-sectional variance about exactly
   that benchmark's return. The paper's own argument that the EW measure should forecast the
   *equal-weighted* market return better than the cap-weighted one is the same matching principle,
   and this lab's benchmark happens to be the EW side of it.
3. **The beta-dispersion bias is the term to worry about on this panel, and it is larger here than
   in the paper's setting.** The lab's universe spans nine national indices in several currencies,
   with returns converted to USD and FX unhedged. Cross-sectional dispersion in exposure to *any*
   common factor — the global market, a region, a currency — enters `CSV^β` and is multiplied by the
   squared factor return. A day on which the dollar or a regional index moves hard will raise
   measured CSV without any change in idiosyncratic risk. The lab's own notes on the currency
   component of USD-converted returns and on region-level comovement name the same object from the
   other side. **If CSV is used as a conditioner, demean it within region or regress out the squared
   pool return before using it**, and say which was done.
4. **The timing reading is the one the lab has already closed; the measurement reading is not.**
   The paper's headline is that this measure predicts the aggregate market return. On this universe
   that is the weakest available use: `max_leverage = 1.0` and cash earning only T-bills mean a
   long-only book can act on an aggregate forecast only by sitting in cash, and the complement-window
   rule (`learnings.md`, 2026-09-01) plus the scale-free-objective finding (journal F1, 2026-10-17/18)
   say that channel does not pay here. What survives both is CSV as a **panel-level state variable**:
   a normaliser for active returns, a conditioner for bet size, an input to a cross-sectional score.
   Those are different uses and none of them is aggregate timing.

**Pitfalls specific to this panel.** Non-synchronous closes: a row mixes Tokyo, European and US
closes, so a single day's cross-section contains names whose returns cover different wall-clock
windows, and CSV computed on it is inflated by the asynchrony rather than by idiosyncratic risk —
the lab's non-synchronous-trading note is the right prior here, and a weekly CSV is the cheap
robustness check. Holiday forward-fills put exact zeros into the cross-section for whole regions,
which bias CSV *down* on those dates; the eligible mask does not remove them, because a
forward-filled name is still a member. And the whole construction is in simple returns about the
same date's pool mean — not in excess returns, and not demeaned over time.

## Related

- `2026-10-06-betaless-variance-decomposition-and-average-correlation.md` — Campbell–Lettau–Malkiel–Xu
  get a market/industry/name variance split with no betas by *subtracting* index returns; this paper
  gets the name-level piece alone with no subtraction at all, and Proposition 4 is exactly the price
  CLMX pay implicitly for their unit-beta restriction. Read the two together: same object, two
  routes, and this one states the error term.
- `2026-10-06-common-idiosyncratic-volatility-factor.md` — Herskovic et al. find factor structure in
  what is left after the factors; CSV is the cheapest possible estimate of that leftover's level.
- `2026-10-18-dispersion-beta-and-the-cross-section.md` — the same statistic used as a *state
  variable* whose innovations are priced in the cross-section. That note's `CSD` is the absolute-
  deviation sibling of this note's `CSV`, and the two papers cite each other.
- `2026-10-18-return-dispersion-and-the-measurement-of-active-performance.md` — the same statistic
  used as a *denominator* for active return, which is the use this lab can make for free.
- `2026-08-29-range-based-volatility-estimators.md` — the other "measure volatility better from data
  you already have" result in this family. Note the contrast: range estimators buy efficiency in the
  *time-series* direction from the daily bar's high and low; CSV buys an estimate in the
  *cross-sectional* direction from the panel's width. They are orthogonal improvements.
- Tension with `experiments/learnings.md` (2026-09-01): the lab closed `range-variance` as "nine
  screened mechanisms with one cause … unreachable on this universe". Every one of those nine is a
  **width measure used as a stock-level sort**. CSV is not that: it is one number per date describing
  the panel. The closure is about a different object and does not reach this one — but it is also a
  warning, because the fastest way to waste this estimator is to turn it back into a stock-level sort.
