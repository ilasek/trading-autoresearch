---
title: "Have Individual Stocks Become More Volatile? — the betaless market/group/name variance decomposition, and what it says average correlation is"
authors: Campbell, Lettau, Malkiel, Xu
year: 2001
venue: The Journal of Finance 56(1), 1–43 (venue tier 1)
url: https://doi.org/10.1111/0022-1082.00318
citations: 2554 (Semantic Scholar by DOI, checked 2026-10-06); 2550 (OpenAlex by DOI, same date); 1811 (Crossref `is-referenced-by-count`, same date)
sample_period: July 1962 – December 1997 for the decomposition (1926–1997 for the aggregate-volatility backdrop)
markets: all NYSE, AMEX and NASDAQ firms in CRSP, aggregated into 49 Fama–French industries; firm count rises from ~2,000 to ~8,900 over the sample
tier: A
validation_overlap: false
published_post_2018: false
read: full text of NBER Working Paper 7590 (March 2000) from `nber.org/system/files/working_papers/w7590/w7590.pdf`, served first try. **A tenth "looks like an answer" extraction mode was found here and is recorded in the access findings**: `pdftotext -layout` returns a complete, well-formed 122 KB text file in which the cover pages are plain English and **the entire body is Caesar-shifted by +3 over printable ASCII** (`"Lw lv e| qrz"` = `"It is by now"`; digits shift too, `4<:6` = `1973`, and `/`=`,`, `1`=`.`, `0`=`-`, `+`/`,`=`(`/`)`, `{|}`=`xyz`). It passes `file`, passes `pdffonts`, and passes the `( )` empty-parenthesis grep. Decoded with a 24-line shift-by-−3 script (letters wrapping within case, other printable ASCII shifted plainly); the decoded body reads as clean English and was read from there. Display equations survive structurally — the aggregation identities below are read off the decoded equations (9), (15)–(24) — but Greek symbols are mangled, so every symbol below is named in words rather than copied.
---

## Mechanism

This is a measurement paper, not a premium. Its content for this lab is a **construction that gets a
market / group / name variance split out of a return panel with no betas, no covariance matrix and no
estimation at all** — plus the exact algebraic price of that convenience, which the paper states and
which is the part worth having.

The economic question behind it is why a typical stock's total volatility and the market index's
volatility can move in opposite directions: if individual stocks get noisier while the index does not,
the co-movement between stocks must be falling. That is not a hypothesis in the paper, it is an
identity, and it is the identity that makes average correlation a *summary* of a variance
decomposition rather than an independent object.

## Construction recipe

**The decomposition.** Write a firm's excess return as market + group deviation + name deviation,
where the deviations are plain differences, not regression residuals:

    r_ji,t = r_m,t + (r_i,t − r_m,t) + (r_ji,t − r_i,t)
           = market + group-specific + firm-specific

with `i` a group (their industries; substitute **region** here) and `j` a member. The group return is
the weighted average of its members, the market return is the weighted average of the groups, and the
method is valid for **any** weighting scheme as long as the market return is computed with the same
weights. They use market-cap weights; equal weights are equally legitimate under the theorem.

**Why it works without betas, which is the whole trick.** The three components are *not* orthogonal —
the variance of any one group's return carries a covariance term that reintroduces that group's beta.
But the **weighted average across groups** of those variances is free of the individual covariances,
because the weighted betas sum to one by construction and the cross terms cancel in aggregate. So the
decomposition is valid *for the average member*, never for a single member. Their equations (9) and
(16): the weighted average of firm variances equals market variance + weighted-average group-deviation
variance + weighted-average firm-deviation variance, exactly, with no betas anywhere.

**The estimator, per period, from daily data.** Let `t` index months and `s` index days inside a month.

- `MKT_t` = Σ_{s∈t} (r_m,s − μ_m)², the sum of squared demeaned daily market returns in the month.
- `σ²_IND,i,t` = Σ_{s∈t} (group-deviation)², then `IND_t` = Σ_i w_i,t · σ²_IND,i,t.
- `σ²_FIRM,ji,t` = Σ_{s∈t} (firm-deviation)², averaged within group then across groups to give `FIRM_t`.

Three details that matter for a causal implementation and are easy to get wrong. (a) **Only the market
term is demeaned**; the deviation terms are sums of raw squares, because a deviation from a weighted
average already has weighted mean zero. (b) `μ_m` in their implementation is the **full-sample** mean
of the market return — a lookahead if copied literally into a backtest; their own footnote says
time-varying means give almost identical results, so **use a trailing mean or no demeaning at all**.
(c) Weights are taken from the **previous** period and held constant within the period.

**The average-correlation identity, which is the state variable.** If all names had the same pairwise
correlation ρ, the market portfolio's variance would be ρ times any individual name's variance, and the
market model's R² for a typical name would be ρ. Names are not identical, but the paper shows this
remains a good approximation: they compute the full set of pairwise correlations and, separately, the
cross-sectional average market-model R², and report the two series are **almost indistinguishable**.
So:

    average pairwise correlation ≈ average market-model R² ≈ MKT_t / (MKT_t + IND_t + FIRM_t)

which means a lab can have average correlation **without ever forming a correlation matrix** — it falls
out of the same three sums. On a 140-name panel that is a convenience; on a wide panel it is the
difference between feasible and not.

**Their two measurement windows for the correlation series, worth copying because the two disagree
systematically**: pairwise correlations from the **previous 12 months of daily** returns, recomputed
monthly; and from the **previous 60 months of monthly** returns, also recomputed monthly. Their filters:
drop names with a daily return above 200% or with zero returns on at least 75% of the last 12 months'
days.

## Robustness evidence (qualitative only)

- **Tier A on the identities, which are arithmetic and cannot decay**: the betas-cancel-in-aggregate
  result, the three-way sum, and the correlation ≈ R² approximation are algebra plus one empirical
  check, not an effect with a sample.
- **The decomposition is not actually orthogonal, and the paper gives the exact leakage term.** Their
  equations (17) and (18): the betaless group component equals the true CAPM group component **plus**
  the cross-sectional variance of group betas times market variance; the betaless firm component equals
  the true firm component **plus** cross-sectional variance of firm betas on the market times market
  variance **plus** cross-sectional variance of firm betas on their group times group variance. In
  words: **if betas are dispersed, market variance leaks into the "group" and "name" buckets, and the
  three series will co-move even if the true components do not.** The authors argue, and check in their
  Section IV.A, that realistic beta dispersion makes this effect small. That check is on one market in
  one sample; the *form* of the leakage is exact and transfers everywhere.
- **The empirical trend claims are a different and weaker thing from the identities.** They are
  single-market, single-sample, and the paper is honest that its explanations for them are suggestions
  rather than tests. They are also the part with the richest later literature — this is among the most
  replicated measurement results in the field, and the folder's CIV note from tonight is one of its
  descendants — but nothing in this note depends on them.
- **Multiple testing is not an issue here** because no selection is performed; nothing is sorted,
  ranked or traded.
- **Daily and monthly correlation estimates differ systematically and the paper says why**: the daily
  figure is lower, both because daily returns carry negatively autocorrelated idiosyncratic components
  and because the two estimators weight the sample differently. **A co-movement state variable's level
  is therefore an artifact of its sampling interval**, which is a direct warning for any fixed
  threshold.

**Anti-lookahead note.** The paper's headline is a secular trend, stated with dated endpoints. Those
numbers are deliberately not recorded here. What *is* recorded, because it is a construction
constraint rather than a result, is the **qualitative** fact that panel-wide co-movement level is not
stationary over multi-decade samples — it drifted substantially over their sample as name-level
volatility rose relative to market volatility — so **any state variable built on the level of average
correlation, or on the level of a variance share, needs a trailing standardisation rather than a fixed
threshold.**

## Implementability here

**Entirely computable, cheap, and the group axis is already the lab's.** Substitute **region** (or
sector, if ever available) for industry and the construction is: market = weighted average of all 140+
instruments; region deviation = region return minus market return; name deviation = name return minus
its region return; three monthly sums of squares from daily closes. No covariance matrix, no betas, no
estimation window beyond the month. This is the cheapest co-movement statistic in the folder.

Four concrete uses, in increasing cost:

1. **It gives `average correlation` for free as a by-product**, which is the rival summary to tonight's
   absorption-ratio note. The two disagree by construction: `MKT/(MKT+IND+FIRM)` is a **correlation-like,
   equally-weighted-across-pairs** statistic, while the absorption ratio is **covariance-weighted**. The
   folder now holds both and the comparison is one line of code on the same panel.
2. **It prices what a region demean removes.** `notes/2026-09-10-country-industry-global-return-decomposition.md`
   already records that a country/region demean *is* the dummy-variable model, and records this
   decomposition second-hand from that paper's Section 6.2. What this primary adds and that note does not
   carry is the **leakage term**: a region demean does not remove region risk cleanly, it removes region
   risk plus `CSV(β_region) × market variance`. On this universe, where regional ETFs and single names
   sit in the same pool and beta dispersion is large, that term is not obviously small, and it is
   measurable for free: compute both the betaless split and a CAPM-beta split on train and read the gap.
3. **It is a legitimate `range-variance` scout construction**, and the family needs one that is not a
   width level. `experiments/learnings.md` closes `range-variance` on the finding that ten screened
   mechanisms all sort on a **cross-sectional level of width** and that the width level is the
   survivorship artifact. `MKT/(MKT+IND+FIRM)` is not a cross-sectional sort at all — it is a single
   panel-level time series — so the closure's stated cause does not cover it. That is a reason to look,
   not a reason to expect a result.
4. **Pitfalls specific to this panel.** (a) **Non-synchronous closes** depress `MKT` relative to `IND`
   and `FIRM` on a 15-region daily panel, biasing the correlation estimate down — see
   `notes/2026-09-08-nonsynchronous-trading-econometrics.md`; the paper's own daily-vs-monthly gap is
   the same effect in a single market and is the cleanest evidence that it is real. (b) **ETFs and their
   own constituents are both in the pool**, so a regional ETF's "name deviation" is near-mechanically
   small and the firm component is contaminated by the instrument type rather than by the name; a pool
   rule is required before the statistic means anything, and the folder's
   `notes/2026-09-12-missing-data-and-complete-case-pools.md` governs it. (c) **USD conversion puts an
   FX factor in every non-US return**, which this decomposition will book as *region* variance — correct
   for what the lab actually trades, but it means the "region" component is partly currency; see
   `notes/2026-09-10-currency-component-in-usd-converted-returns.md`.

## Related

- `notes/2026-10-06-absorption-ratio-eigenvalue-concentration.md` — the covariance-weighted rival to
  this note's equally-weighted average correlation, and the only other co-movement state variable in
  this folder.
- `notes/2026-10-06-common-idiosyncratic-volatility-factor.md` — tonight's third note, which takes the
  `FIRM` component of exactly this decomposition and shows it has a factor structure of its own.
- `notes/2026-09-10-country-industry-global-return-decomposition.md` — holds this decomposition
  second-hand and audits the dummy model it belongs to; the leakage term above is what that note
  could not carry.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md`,
  `notes/2026-09-10-currency-component-in-usd-converted-returns.md`,
  `notes/2026-09-12-missing-data-and-complete-case-pools.md` — the three panel-specific confounds.
- **Pollet & Wilson, "Average correlation and stock market returns", JFE 96(3), 364–380, 2010,
  `10.1016/j.jfineco.2010.02.011`** — the obvious companion, which argues average correlation predicts
  market returns where market variance does not, on the grounds that variance moves for reasons
  unrelated to aggregate risk. **NOT READ and nothing is claimed from it**: SSRN returns 403, the Oxford
  ORA record holds metadata with no file, the HKUST repository redirect-loops, both CiteSeerX locations
  die with a connection reset, and the author's Google Sites page is the ~918 KB application shell
  `research/README.md` warns about. Recorded here so the next session does not repeat the searches, and
  flagged as the folder's new top unreached source in `SUMMARY.md`.
