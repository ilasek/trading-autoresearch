---
title: "What Factors Drive Global Stock Returns?" — read for its decomposition of a firm characteristic into a group mean and a group-demeaned residual, and for what neutralizing a sort by country costs and buys
authors: Hou, Karolyi, Kho
year: 2011
venue: The Review of Financial Studies (venue tier 1)
url: https://doi.org/10.1093/rfs/hhr013
citations: 623 (OpenAlex, checked 2026-09-10); 529 (Crossref `is-referenced-by-count`, same date). Semantic Scholar's DOI endpoint returns "not found" for `10.1093/rfs/hhr013`, which is the same behaviour session 11 recorded for `hhv059` and session 12 for two `jofi` DOIs — an Oxford/Wiley finance DOI missing there is not evidence a paper is unindexed.
sample_period: 1981–2003 in the version read; the published abstract says "a three-decade period" and 27,000 stocks against the working paper's 29,000 over 1981–2003, so the published sample is somewhat longer and was **not** read. Either span ends well before this repo's validation window.
markets: ~29,000 individual stocks in 49 developed and emerging countries, monthly, USD
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the December 2006 working-paper version, from a third-party document mirror (`gyanresearch.wdfiles.com/local--files/alpha/SSRN-id908345.pdf`, 54pp) after SSRN's own delivery endpoint returned the documented 403. The **published** RFS abstract was reconstructed from OpenAlex's `abstract_inverted_index` and agrees with the working paper on the headline factor result; the published tables were not read, so every figure below is from the working paper and is quoted as a ratio or a sign, never as a level.
---

## Mechanism

Take any cross-sectional score `X` and any partition of the universe into groups — countries,
regions, industries. `X` splits exactly into two pieces:

    X[i] = mean(X | group(i))  +  ( X[i] - mean(X | group(i)) )
           \___ between ___/      \________ within _________/

Demeaning a score by group keeps the second piece and throws away the first. That is normally
described as *removing a nuisance* — the group bet nobody asked for. The mechanism this paper
supplies is that the between-group piece is **not a nuisance in general: it is a signal in its
own right, and for most characteristics it is the larger of the two.**

Why it should be so is not mysterious. A country's average valuation, average size or average
liquidity is a real quantity: it reflects that country's discount rate, its investor base, its
market structure. A stock is cheap either because it is cheap relative to its neighbours or
because its whole market is cheap, and both are reasons to expect a higher return. Demeaning
asserts, without testing, that only the first reason is real.

The paper's second mechanism is about the *portfolio* rather than the score. Neutralizing a sort
by group forces every group into the book in proportion to its weight. That does two things at
once and in the same direction: it removes the between-group return (cutting the premium) and it
removes the between-group common variation (cutting the volatility). Whether the ratio improves
is therefore an empirical question with no a-priori answer, and it has a different answer for
every score.

## Construction recipe

**The two-way characteristic decomposition.** For each characteristic and each date, form two
regressors from one:

- `m(X)` — the mean of `X` over the firm's country of domicile (and, separately, over its global
  industry);
- `dm(X)` — the firm's own `X` minus that mean.

Then run Fama–MacBeth cross-sectional regressions of forward returns on `m(X)` and `dm(X)`,
**both together and separately**. The point of entering them jointly is that the two are
orthogonal by construction, so the joint regression reads as two independent tests rather than a
horse race.

**The group-neutral sort.** Rank within group, then pool ranks: assign stocks with the same
*intra-country* (or *intra-industry*) rank into the same quintile, so that every group is
represented in the extreme portfolios at least proportionally to its weight. The paper requires a
minimum of 15 stocks in a country in a given year for that country to qualify — a
group-size floor is part of the construction, not an afterthought. Compare the group-neutral
portfolio against the global (pooled-rank) portfolio built from the identical characteristic,
identical breakpoints logic and identical rebalance cadence, so the only thing that moves is the
ranking partition.

**What was found, as signs and ratios.**

- Both halves are priced. The `dm` (demeaned, firm-specific) coefficients are reliably
  significant for every characteristic tested and agree in sign and rough magnitude with the
  undecomposed regression — i.e. **demeaning does not destroy the signal**.
- **The country-mean half is significant too, and its coefficients are *larger in magnitude*
  than the demeaned half's for every characteristic tested except book-to-market.** For the
  cash-flow-to-price characteristic the country-mean coefficient is about **twice** the
  demeaned one.
- **But the mean half is estimated far less precisely**, and this is the qualification that
  matters more than the point estimates: on that same characteristic the country-mean
  coefficient carries `t = 2.21` against `t = 5.53` for the demeaned one. There are only as many
  distinct values of `m(X)` per date as there are countries, so the between-group regressor has a
  tiny effective sample however many stocks are in the panel. A bigger coefficient on a much
  weaker `t` is what a low-breadth bet looks like.
- **The industry-mean half is a null for almost everything** — small coefficients, not reliably
  different from zero — **with one loud exception: momentum.** The industry-mean past-return
  coefficient is strongly positive and several times the size of the firm-specific one
  (`t = 3.86` simple, `t = 5.62` multiple). Group-level momentum is a separate live effect from
  name-level momentum.
- **The portfolio evidence agrees with the regression evidence, score by score.** Country-neutral
  versions of the characteristics whose *country mean* was priced lose much of their premium;
  the country-neutral version of book-to-market — whose country mean was *not* priced — loses
  almost none of it. That correspondence is the paper's own internal consistency check and is
  the reason to trust the decomposition rather than the sort alone.
- **Country-neutralizing cuts volatility far harder than industry-neutralizing.** For one
  valuation ratio the group-neutral factor's volatility falls to roughly **55%** of its global
  counterpart's when neutralized by country, but only to roughly **93%** when neutralized by
  industry. For momentum, industry-neutralizing takes volatility to about **84%** and the premium
  to about **78%** of the global version's — the one place industry-neutralizing bites.

## Robustness evidence (qualitative only)

- **Wide, genuinely out-of-sample panel**: 49 countries including emerging markets, tens of
  thousands of names, a multi-decade monthly sample. The authors frame the whole exercise as an
  out-of-sample test of effects first found in the US and argue on that basis that a spurious
  explanation is unlikely — the same logic `notes/2026-08-28-international-momentum-country-neutral.md`
  records for Rouwenhorst, applied to a much larger cross-section.
- **Momentum survives everywhere** — across countries, across industries, at the firm level and at
  the industry level — and is one of only two extra-market factors the paper retains. Its factor
  is also reported as having low correlation with the other characteristic factors, which is the
  property this lab prices when it asks what a decorrelated leg is worth.
- **The country-versus-industry asymmetry replicates the comovement literature from the return
  side.** Country groupings matter for common variation and industry groupings mostly do not,
  which is the same ordering
  `notes/2026-09-10-country-industry-global-return-decomposition.md` records from covariance-model
  fits on a different sample and a different method.
- **Known weakness, stated by the authors**: they cannot separate a risk interpretation from a
  mispricing one, and they flag the cash-flow-to-price result as the contentious part. Nothing in
  this note depends on which interpretation is right — the decomposition is a measurement, and it
  is agnostic.
- **Not a replication of the decomposition itself.** The `m`/`dm` split was proposed in a
  practitioner working paper (Asness, Porter and Stevens, *Predicting Stock Returns Using
  Industry-Relative Firm Characteristics*, ~147 Semantic Scholar citations, checked 2026-09-10)
  which is **not read** — SSRN 403s and AQR's own page serves only a two-page disclosure wrapper
  in place of the file. The present paper is a peer-reviewed, Tier-1, independent, global
  application of the same decomposition, which is why it is the primary here; the earlier paper
  is credited but nothing is taken from it.

## Implementability here

The decomposition needs no data this repo lacks: a score, a partition, and a mean. Everything
below is a train-split measurement that scores no candidate and reads no holdout.

1. **The single highest-value free measurement this note supports: split every score the lab
   owns into its two halves and IC each half separately.** The lab's scores are `ILLIQ`,
   same-minus-other-month seasonality, 21-day reversal, trailing-return momentum, the learned
   block. For each, form `m(score)` over region and `dm(score)`, and measure the information
   coefficient of each half at the horizons already in use. Three outcomes and all three are
   findings: only `dm` carries content (demeaning is free and correct), both carry content (a
   demean is discarding signal and the two halves should be separate legs), or only `m` carries
   content (the "signal" is a region bet in costume, which is the failure mode
   `experiments/learnings.md` records for close-location value being "reversal in costume").
2. **It puts a specific, falsifiable question to the lab's own best measurement result.**
   `lv_illiq_region_relative` beat raw `ILLIQ` (2026-09-03). This literature says the between-region
   half of `ILLIQ` should *also* have been priced, and that neutralizing removes it. If the lab's
   region demean improved things anyway, then on this universe the between-region half is noise
   or is dominated by its own low breadth — and that is worth knowing explicitly rather than by
   implication, because it also predicts what a region demean will do to *every other* score.
3. **The low-breadth caveat is the one to carry, and it is sharper here than in the paper.**
   The between-group regressor has as many distinct values per date as there are groups. This
   repo has ~15 regions, against the paper's 49 countries. A between-region bet on this universe
   is a bet with breadth 15 at most, and `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`
   prices what that costs. Expect the `m` half here to be *less* attractive than the paper's, not
   more, and say so before measuring rather than after.
4. **The group-size floor is a real construction node.** The paper's 15-stocks-per-country
   minimum has a direct analogue: some of this universe's 15 regions carry very few names, and a
   region mean over three instruments is not a region mean. Pre-commit the floor and the handling
   of the regions it excludes — this is precisely the kind of node
   `notes/2026-09-09-specification-curve-analysis.md` says should be written down before anything
   is scored.
5. **Group-level momentum is the one *between*-group effect this literature says is live**, and
   it is the one the lab has the least reason to expect from its own results. `price-trend` is
   capped and legacy, so this is not a licence to build there; but if any between-group half
   shows content on this universe, the prior from this paper is that it is the trailing-return
   one.
6. **The ETF problem, again and worse.** A region-mean score computed over a group that contains
   that region's own ETF is partly reading the ETF's score back into the mean. Either exclude
   ETFs from the mean or compute the mean on constituents only, decided in advance.

**Pitfalls.**

- **Most of the paper's characteristics need fundamentals and are unreachable here.** Only past
  returns and size are directly computable; the transferable object is the *method*, not the
  characteristic list. Do not import the paper's ranking of which characteristics matter.
- **A country demean and a region demean are not the same partition**, and this repo has no
  country field. The coarser grouping mixes countries inside a region, which shrinks the
  between-group piece and inflates the within-group one relative to the paper — in an unknown
  amount, so re-measure rather than adjust by analogy.
- **The premium-and-volatility trade means a Sharpe comparison is the only honest scoreboard**,
  and a Sharpe difference of the size this lab usually sees is not individually resolvable
  (`notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md`). Read the two halves' ICs, which
  are cheap and have their own null, rather than betting a trial on the ordering.
- The costs of a group-neutral book differ from a pooled one — it holds different names, and on
  this universe the cheap and expensive names are not evenly spread across regions
  (`notes/2026-09-04-global-liquidity-proxy-horserace.md`). A neutralization is a turnover change
  as well as a signal change.

## Related

- `notes/2026-09-10-country-industry-global-return-decomposition.md` — the companion, from the
  covariance side: group membership is real, but unit loadings on it are the wrong way to use it.
  Read together, the pair says a demean both *over-corrects* (that note) and *discards a priced
  component* (this one).
- `notes/2026-09-10-currency-component-in-usd-converted-returns.md` — one concrete thing the
  between-region component contains.
- `notes/2026-08-28-local-versus-global-factor-construction.md` — regional breakpoints; the
  portfolio-construction counterpart of the group-neutral sort here.
- `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` and
  `notes/2026-09-02-anomalies-by-size-group.md` — the other two notes about which slice of the
  cross-section a characteristic's content actually lives in.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — why a 15-group bet is a
  low-breadth bet.
- `experiments/learnings.md` (2026-09-03, `lv_illiq_region_relative`) — the lab's own demean, and
  the result this note puts a question to.
