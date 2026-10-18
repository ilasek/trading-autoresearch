---
title: "Cross-sectional dispersion as a priced state variable — sorting stocks on their dispersion beta"
authors: Verousis, Voukelatos
year: 2018 (published); the version read is the May 2017 working paper
venue: Quantitative Finance 18(5), 813–826 — venue tier 2 (peer-reviewed, but not one of the top finance journals). Working paper read from the University of Essex repository
url: https://doi.org/10.1080/14697688.2017.1414515 · working paper read at https://repository.essex.ac.uk/24170/1/CSD_wp_4.pdf
citations: 10 (Crossref `is-referenced-by-count`, checked 2026-10-18); 18 (OpenAlex, same date); 19 (Semantic Scholar, same date)
sample_period: 2 January 1996 – 31 December 2012
markets: United States only — CRSP daily closing quotes and volumes for US-listed stocks, CRSP value-weighted index as the market proxy
tier: B — lightly cited, single market, a single seventeen-year sample, **no transaction costs anywhere in the paper**, and the headline portfolio is a long-short spread. The construction is fully specified and the control set is unusually thorough, which is what keeps it out of C
validation_overlap: false
published_post_2018: false (published May 2018; the version read is the May 2017 working paper, and the sample ends 2012)
read: full text, fetched first try from `repository.essex.ac.uk/24170/1/CSD_wp_4.pdf` (HTTP 200, 1.3 MB), `pdftotext -layout` → 91 KB of text, 653 instances of `" the "`, `( )`-dropout check zero, no ASCII shift. The published *Quantitative Finance* version was not fetched. **Performance magnitudes from the tables are deliberately not recorded here**, per the anti-lookahead rule; signs, monotonicity, significance and estimator diagnostics are.
---

## Mechanism

This note's object is the same statistic as
`2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md` — the width of the
day's cross-section — put to a different use. There it was an *estimator*. Here it is a **state
variable whose innovations carry a price in the cross-section of individual stocks**, which turns a
panel-level number into a name-level characteristic and therefore into something a long-only book
could in principle act on.

The argument runs in three steps. (i) The distance of a stock's return from the market return is
driven by its idiosyncratic shock, so the cross-sectional dispersion of returns is an aggregate
measure of idiosyncratic risk — the authors take this link from Goyal–Santa-Clara and from
Garcia–Mantilla-García–Martellini rather than re-deriving it. (ii) The representative-agent
assumption that makes idiosyncratic risk irrelevant fails, because real investors hold
undiversified portfolios (the Levy / Merton / Malkiel–Xu / Bessembinder class of models), so
aggregate idiosyncratic risk is a risk investors actually bear. (iii) If dispersion is negatively
related to the investment and consumption opportunity set, then stocks that *pay off when
dispersion rises* are hedges, investors bid their prices up, and their expected returns are lower.
**The prediction is a negative price of dispersion risk: high dispersion beta, low expected
return.** That is the sign the paper finds, and it is the same sign Ang–Hodrick–Xing–Zhang find for
aggregate *volatility* risk — a resemblance that is both the result's main support and its main
confound, and the paper confronts it directly.

A second, more mundane reading of the same sign is available and the paper does not fully close it:
a stock whose returns move with the width of the cross-section is a stock that moves a lot on the
days everything moves a lot, which is close to being a high-volatility or high-beta stock, and the
low-volatility and `IVOL` effects already predict that sign. The paper's defence is its control set
(below), not a separate identification.

## Construction recipe

- **The state variable.** Equal-weighted cross-sectional **absolute** deviation of returns about
  the market return, one number per day:

      CSD_t = Σ_i | r_it − r_mkt,t | / (N − 1)

  with `r_mkt` the value-weighted index return. (This is the CSAD of the herding literature. The
  squared-deviation version is the `CSV` of the companion note.) The authors report that results are
  "largely the same" under four alternatives: squared rather than absolute deviations;
  value-weighted rather than equal-weighted deviations; and deviations taken about the
  equal-weighted or the value-weighted *mean stock return* rather than about the index.
- **What enters the regression is the change, not the level.** The pricing variable is `ΔCSD`.
  A level is persistent and a state-variable pricing test needs innovations.
- **Pre-formation loading.** For each stock, each month, a **two-factor daily time-series
  regression over the previous month only**:

      r_it^e = a + β_i,MKT · MKT_t + β_i,ΔCSD · ΔCSD_t + ε_it

  Only the market is included alongside the variable of interest — deliberately, following
  Ang et al. (2006), because adding factors to a pre-formation regression adds noise to the sort.
  A stock needs **at least 15 daily observations** in the window or it is skipped.
- **Portfolios.** At the start of each month, sort all stocks into **quintiles on `β_i,ΔCSD`**,
  value-weight within quintile, hold one month. Quintile 1 is the most negative loading. A second,
  cruder split by the *sign* of the loading (`N` and `P` portfolios) is reported alongside.
- **The headline portfolio** is long quintile 1 and short quintile 5 — i.e. **long the stocks whose
  returns fall most when dispersion rises**. Mean returns decrease monotonically from quintile 1 to
  quintile 5, which is the form of the result worth copying: a monotone five-point pattern, not a
  spread in isolation.
- **Risk adjustment.** CAPM, three-factor and four-factor (Carhart) alphas of the spread, then a
  Brennan-style two-stage characteristic regression: full-sample loadings on MKT/SMB/HML/MOM are
  removed from each stock's return first, and the residual is regressed cross-sectionally on
  lagged characteristics.
- **The characteristic control set**, which is the paper's strongest feature: size (log market cap),
  past six-month return, and the standard deviation, skewness and kurtosis of returns over the past
  six months; **idiosyncratic volatility** (measured as in Ang et al. 2006); **co-skewness**
  (Harvey–Siddique); a Pástor–Stambaugh stock-level liquidity coefficient; the `R̄²` of the
  four-factor regression as a share-of-systematic-risk measure; and analyst forecast dispersion
  (Diether et al.). The dispersion-beta coefficient stays negative and significant; of the controls,
  only size and co-skewness are themselves significant.
- **Double sorts.** For each of those characteristics plus market beta: sort into quintiles on the
  characteristic first, then on dispersion beta within each, then average the dispersion-sorted
  returns across characteristic quintiles. The monotone pattern survives.
- **Mimicking factor and price of risk.** `F_CSD` is built by regressing `ΔCSD` on the five quintile
  portfolios' returns each month using daily data and holding the five portfolios in proportion to
  the fitted coefficients; a Fama–French-style 2×3 size × dispersion-beta sort gives an alternative
  factor with similar results. The price of risk comes from a standard Fama–MacBeth two-pass.

## Robustness evidence (qualitative only)

- **The sign is stable; the magnitude is not, and the instability is informative.** The effect is
  strongest at a **one-month** formation window and weakens substantially at three months and more.
  The authors read this as conditional betas moving over time, so that older data is less relevant.
  The competing reading — that the one-month loading is mostly estimation noise and the sort is
  partly picking up something short-lived — is not tested against, and **the paper's own estimator
  diagnostic supports taking it seriously**: pre-formation betas span roughly −6.9 to +6.7 across
  quintiles while **post-formation betas span only about −0.03 to +0.22**. Almost all of the sorted
  dispersion in loadings does not persist one month. The authors note this mirrors Ang et al. (2006)
  for aggregate volatility — which makes it a known property of this family of sorts rather than a
  defect of this paper, and equally a known reason to discount it.
- **It is distinct from aggregate volatility risk, but correlated with it.** The dispersion
  mimicking factor and a VIX-change mimicking factor correlate strongly and positively, and both
  carry negative premia; in this sample the dispersion premium stays significant with volatility
  controlled while the volatility premium does not. One sample, one country: treat "distinct" as
  "not subsumed here", not as established.
- **Also controlled for** and not subsumed: analyst forecast dispersion, mean stock variance,
  macroeconomic uncertainty, and mean idiosyncratic volatility — all entered as mimicking-portfolio
  factors. This is a serious attempt at the obvious confounds.
- **Sub-sample splits** by the sign of the market return and by the sign of `ΔCSD` leave the
  relationship significant in both halves, though stronger in up-markets and in rising-dispersion
  months. The up-market asymmetry is not explained and the authors call it surprising.
- **Replication status: none.** This result does not appear in the large replication projects, the
  citation count is small, and no independent out-of-sample or out-of-country test is cited. It is a
  hypothesis with one careful test behind it.
- **Methodology honesty: mixed.** Multiple testing is not discussed. **Transaction costs are never
  modelled** — the words appear once, in a motivating sentence about why investors are undiversified.
  The headline portfolio is a zero-cost long-short, so the paper never has to state what the long
  leg alone does.

## Implementability here

**The long leg is buildable and the cost side is the whole question.**

What transfers cleanly: `ΔCSD` over the eligible pool is free to compute (see the companion note),
the pre-formation regression is two regressors on ~21 daily observations per name — trivially
walk-forward, trivially causal, and `O(N)` — and the sort output is a long-only quintile. A
candidate would hold the lowest-dispersion-beta names, equal-weighted, rebalanced monthly. That is
a plain `range-variance` scout with no estimated covariance matrix anywhere in it, which matters
because the covariance-fitted weighting axis is the one the lab closed on 2026-10-17/18.

Four reasons to expect less here than the paper reports, all of which should be pre-registered
rather than discovered:

1. **The long leg is not the spread.** Everything reported is a long-short quintile portfolio; the
   lab can hold only quintile 1. The folder's own
   `2026-09-06-long-side-share-of-anomaly-profits.md` is the relevant prior on what fraction of a
   documented spread survives dropping the short leg, and this paper gives no evidence on the split.
2. **Monthly re-sorting on a one-month loading is a turnover engine, and v3 charges for it.** The
   effect decays as the formation window lengthens, so the construction that works is exactly the
   construction that trades most. Under v3 a name costs 15–40 bps per side by liquidity tier **plus**
   UK/HK/FR/IT/ES transaction taxes, and holdings drift between rebalances is charged too. Before
   writing a candidate, compute the implied monthly name turnover of a quintile sort on a
   one-month-estimated loading and price it; if it is anywhere near the lab's recorded multiples,
   the paper's own decay curve says the cheaper long-window version is the weaker signal.
3. **The confound this lab has already met twice.** A one-month loading on `ΔCSD` is mechanically
   large for names that move hard on days the cross-section is wide. The journal's 2026-10-17/18
   finding that "a correlation score standardised by own volatility is still a volatility score with
   the sign flipped" is the same shape of failure, and the lab has separately recorded that the
   low-volatility anomaly is absent on this panel and that Sharpe is flat in beta here. **The
   screen to run before the trial is free**: rank-correlate the dispersion-beta score against total
   volatility, idiosyncratic volatility and market beta on the eligible panel. If `|ρ|` is large,
   the candidate is a relabel of an axis this panel has already said is empty, and the paper's US
   control set does not transfer.
4. **The paper's market proxy and this lab's benchmark are different objects.** `CSD` is measured
   about a *value-weighted* index; v3 grades against the *equal-weight* eligible pool. Measuring
   dispersion about the pool mean is both one of the paper's own robustness variants and the
   matched choice here — use it, and say so.

**A fifth consideration specific to this panel, and it cuts the other way.** The paper's universe is
all of CRSP, where dispersion is dominated by small and thinly traded names. This lab's panel is
nine large-cap national indices, so the cross-section is *narrower* and the dispersion-beta sort has
less to work with — but it is also *multi-region and multi-currency*, so a day's dispersion contains
a regional and an FX component that no US paper has to think about. A dispersion beta estimated on
that panel may be a **region or currency loading in disguise**. Demeaning `ΔCSD` within region, or
building the loading against a region-demeaned dispersion series, is the cheap guard; the lab's
region-neutralisation result is the warning that the guard may remove the signal with the noise.

## Related

- `2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md` — the estimator
  behind this note's state variable, with the bias terms this note's `CSD` inherits. Garcia et al.
  are cited here as the source of the dispersion/idiosyncratic-risk link.
- `2026-10-18-return-dispersion-and-the-measurement-of-active-performance.md` — the third use of the
  same statistic: as a denominator rather than a signal.
- `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` and
  `2026-10-06-common-idiosyncratic-volatility-factor.md` — the nearest priced-idiosyncratic-risk
  results in the folder; this paper's sign agrees with the `IVOL` puzzle's sign, and the overlap is
  the first thing to rule out.
- `2026-09-06-long-side-share-of-anomaly-profits.md` — the standing discount for a long-short result
  read by a long-only lab.
- `experiments/learnings.md` (2026-09-01), which closed `range-variance` as "nine screened
  mechanisms with one cause". **This candidate is in tension with that closure and the tension is
  worth stating rather than hiding**: the nine were width measures *of a single name's own returns*
  used as a sort; this is a loading *on a panel-level series*. They are different scores. But the
  closure's stated cause — that everything in the family turns out to be one volatility axis the
  panel does not pay for — is exactly what the pre-trial correlation screen above is designed to
  detect, and if that screen fails, this is the tenth mechanism with the same cause rather than a
  new one.
