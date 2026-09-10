---
title: "International Stock Return Comovements" — read as the audit of the Heston–Rouwenhorst country/industry dummy decomposition (with Heston–Rouwenhorst 1994 and Griffin–Karolyi 1998 as the predecessor cluster)
authors: Bekaert, Hodrick, Zhang (primary); Heston, Rouwenhorst (predecessor, not read); Griffin, Karolyi (predecessor, not read)
year: 2009
venue: The Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.2009.01512.x
citations: 827 (Semantic Scholar by DOI, checked 2026-09-10); 650 (Crossref `is-referenced-by-count`, same date). OpenAlex reports **32** for the same DOI — a lone low count against two agreeing indices and a top-journal venue, the seventh instance of session 7's "disbelieve a lone low count" and the largest discrepancy this folder has recorded. Predecessors: Heston–Rouwenhorst 759 (Semantic Scholar) / 781 (OpenAlex) / 500 (Crossref); Griffin–Karolyi 403 (OpenAlex) / 199 (Crossref), all checked 2026-09-10.
sample_period: 1980–2003, weekly (predecessors: 1978–1992 and a mid-1990s sample, both taken second-hand)
markets: 23 developed markets × 26 industries and 23 markets × 9 size/book-to-market styles, USD-denominated, value-weighted
tier: A
validation_overlap: false
published_post_2018: false
read: full text of NBER Working Paper 11906 (December 2005), `nber.org/system/files/working_papers/w11906/w11906.pdf`, served first try. The **published** JF abstract was reconstructed from OpenAlex's `abstract_inverted_index` and matches the working paper on every claim used below, including the model-comparison result that is this note's centrepiece. Heston–Rouwenhorst 1994 and Griffin–Karolyi 1998 are both `oa_status: closed` with no repository copy in OpenAlex, SSRN 403s as documented, and neither was read; their content here is taken **only** as restated inside the primary, and is flagged as such at each use.
---

## Mechanism

A stock's return is not an independent draw. It carries a component shared with every stock
(a global factor), a component shared with the other stocks quoted in its country, and a
component shared with the other stocks in its industry. The economic story for the country
component is partial market segmentation: capital and trade barriers, a common local discount
rate, a common domestic macro shock, a shared currency, and a local investor base whose flows
hit local names together. The industry component is a common cash-flow shock — an input price,
a demand shift, a technology.

This matters to any cross-sectional score because **a score computed on raw returns partly ranks
groups rather than names**. If country effects are large, the top of a global ranking is not
"the best names" but "the names in the country that moved"; demeaning by group is the standard
remedy, and the size of what it removes is the country component's share.

The primary's contribution is to ask whether the *usual* way of measuring that share is right.
The Heston–Rouwenhorst construction — the workhorse of this literature, and the implicit model
behind any group demean — is a **dummy-variable model with unit exposures**: every stock in a
country is assumed to load on that country's factor with a coefficient of exactly one. The
primary's finding is that this restriction is the model's undoing. A parsimonious risk model
that lets each portfolio have its *own*, *time-varying* beta on a global and a regional factor
describes the covariance structure materially better than country and industry dummies do,
even though it uses far fewer factors.

The economic reading is that market integration is a matter of degree and it changes: a name's
exposure to its region is a number between zero and something above one, not a switch. A dummy
model has to push that variation into the factor realizations, where it does not belong.

## Construction recipe

**The dummy decomposition (what a group demean actually assumes).** For portfolio `j` in
country `c` and industry `i`, at each date `t`:

    R[j,t] = alpha[t] + C[c,t] + I[i,t] + eps[j,t]

estimated as **one cross-sectional regression per date** — no time-series estimation at all —
on dummy vectors, under the identifying restrictions that the cap-weighted sum of country
effects and the cap-weighted sum of industry effects are each zero:

    sum_l w_C[l] * C[l,t] = 0        sum_l w_I[l] * I[i,t] = 0

Those restrictions make the intercept `alpha[t]` equal to the value-weighted market return, so
the model reads as market + country deviation + industry deviation + residual. Two restricted
variants are the ones a practitioner actually uses:

- **DC** — country dummies only (industry effects set to zero). *This is exactly a
  country/region demean of the cross-section.*
- **DI** — industry dummies only.

**The nested return decomposition** (the primary's Section 6.2, attributed there to Campbell,
Lettau, Malkiel and Xu). Needing no estimation at all, it is the cheapest version and it
telescopes:

    R[j,t] = R[MKT,t] + (R[IND,t] - R[MKT,t]) + (R[j,t] - R[IND,t])
           = market + industry-specific + firm-specific

whose variance decomposition for the average firm is a clean three-way split into market
variance, cap-weighted industry-deviation variance, and cap-weighted firm-deviation variance.
Substitute region for industry and it is a region/global/name split computable from returns
alone.

**The risk-model alternative that wins.** Instead of dummies, regress each portfolio on a small
factor set and let the loadings be free:

- factors: a **global market** factor, plus **regional** factors; optionally Fama–French-style
  or statistically-extracted (APT) factors;
- betas estimated so they vary **both across portfolios and over time** — the paper is explicit
  that either alone buys little and both together buy nearly all of the improvement;
- the covariance implied by the model is `beta_j1' * cov(F) * beta_j2`.

**The model-selection statistic** is worth copying because it scores a *covariance model*
rather than a return: `ABSECORR`, the cap-weighted average absolute difference between each
model-implied pairwise correlation and its sample counterpart, computed period by period; and
its RMSE analogue, compared across models with Newey–West standard errors. This is a way to
ask "which grouping describes my universe?" that never scores a strategy and never touches a
return series.

**The measured ordering** (average absolute correlation error, lower is better; these are
properties of a covariance model, not performance of a portfolio):

    global CAPM, unit betas                              0.284
    global CAPM, cross-sectional betas, no time variation 0.251
    global CAPM, betas varying in both dimensions         0.162
    global Fama-French / APT, betas varying in both       0.133 / 0.132
    Heston-Rouwenhorst country + industry dummies (DCI)   0.123
    global + REGIONAL Fama-French / APT, betas varying    0.081 / 0.076

The sentence to carry: **the dummy model beats any risk model built from global factors alone,
and loses to every parsimonious risk model that adds regional factors.** Group membership is
real information; unit loadings on it are not the best way to use it.

**Country versus industry, inside the dummy model.** Shutting down the country dummies leaves
an average correlation error of 0.239; shutting down the industry dummies leaves 0.195. Country
membership is the more important of the two groupings for describing comovement. The primary
reports this while explicitly declining to endorse the stronger claims in either direction that
the surrounding literature has made.

## Robustness evidence (qualitative only)

- **The country-over-industry ordering is the older, replicated result.** The primary restates
  it as the finding of Heston–Rouwenhorst and of Griffin–Karolyi — an independent sample, a much
  wider country set and a far finer industry classification — and its own fit statistics
  reproduce the ordering. Both predecessors are recorded here **second-hand**; neither was read.
- **The ordering is not a constant, and it is sensitive to a small group of industries.** The
  primary reports its comparison both with and without a handful of technology/media/telecom
  industries, and the surrounding literature it surveys disagrees with itself about direction.
  The transferable form is a warning about the *estimand*, not a claim about any period: the
  country/industry split is a quantity that moves, that a few industries can dominate, and that
  different reasonable specifications answer differently. This is the same lesson as
  `notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md`, arriving on a decomposition
  rather than on a sort.
- **The dummy model fails hardest exactly where a demean is used — at the name level.** The
  primary applies both models out of sample to individual firms. The dummy model **over-predicts**
  comovement for pairs that share a country or share an industry (strikingly so for two firms in
  the same industry, and for two firms in the same country), while the free-beta regional model
  tracks both the level and the time variation far better; the model-versus-sample correlation
  never reaches half for the dummy models and is at least three-quarters for the risk model.
  Forcing a unit loading on a group over-corrects the names that are loosely attached to it.
- **Both dimensions of beta variation are needed.** Allowing cross-sectional variation alone, or
  time variation alone, each recovers only a small part of the gain. A static per-name regional
  beta is not enough.
- The primary's own headline results are trend tests over its sample and are deliberately not
  recorded here; nothing in this note depends on them.

## Implementability here

This repo's universe is ~140 instruments across 15 regions with 42 ETFs, priced as
USD-adjusted daily closes. Every ingredient above is reachable, and one of them is already in
the lab's results.

1. **The lab has already run the DC model without calling it that.** `lv_illiq_region_relative`
   — the region-relative `ILLIQ` that produced the lab's first leg improvement from a stated
   measurement mechanism (2026-09-03) — is a country/region demean, i.e. the DC restriction
   applied to a score instead of to a return. This literature says that construction is a
   *restricted* version of the right model, and names the restriction it imposes: unit exposure
   to the region.
2. **The cheapest upgrade is a free-beta regional residual.** For each name, estimate a rolling
   beta on its regional ETF (the universe carries 42, which is an unusually clean set of regional
   factor proxies — most labs have to build them) and take the residual, rather than subtracting
   the regional mean. Rolling estimation gives the time variation the paper says is essential;
   the per-name coefficient gives the cross-sectional variation. Costs are unaffected — this
   changes a score, not a turnover profile.
3. **A region demean over-corrects loosely-attached names.** This is the firm-level finding
   above and it is the concrete failure mode to look for: names whose true regional beta is well
   below one have too much subtracted and are pushed to the wrong end of the ranking. A free-beta
   residual and a demean will disagree most on exactly those names, which makes the comparison a
   clean two-arm test at one node.
4. **The nested market/region/name decomposition costs nothing and is a diagnostic, not a book.**
   Run on this universe's own returns it answers, in the lab's own data, the question this note
   can only answer from someone else's: how large is the region component here, and therefore
   how much any demean is removing. It scores no candidate and reads no holdout.
5. **`ABSECORR` is a model-selection statistic the lab can afford.** It compares *covariance
   models* on the train split and never touches a candidate's return series — the same class of
   free diagnostic as the 2026-09-06 monotonicity test and 2026-09-08 depth profile.

**Pitfalls.**

- **This repo has no country field.** Region groupings must come from listing currency and an
  obvious NA / Europe / Asia-Pacific split, as `notes/2026-08-28-international-momentum-country-neutral.md`
  already records. Coarser groups mean a *larger* within-group residual and a weaker demean than
  the literature's country-level version, in both directions.
- **No industry field either**, so the industry half of this literature is out of reach directly.
  `notes/2026-08-31-intra-industry-lead-lag-grouping.md` records the lab's grouping substitutes;
  the sector ETFs are the only industry handle, and the lab's 2026-08-31 ETF-versus-constituent
  screen found the reachable side of that a null.
- **42 of ~140 instruments are ETFs**, which have no country of domicile in the sense this
  literature means and are themselves partly *made of* the region factor. A region demean applied
  to a regional ETF is close to subtracting the object from itself. Whatever grouping is used,
  ETFs need their own treatment or exclusion, stated in advance.
- **Rolling betas are estimated, so they are noisy**, and the noise is concentrated in exactly
  the short-history names. The estimation window is a construction node in the sense of
  `notes/2026-09-09-specification-curve-analysis.md`; pre-commit it.
- **Nothing here licenses a book on its own.** This is a measurement mechanism about how a score
  is computed, not a new signal. On this lab's own evidence (2026-09-08) that is the right kind
  of proposal and the wrong kind to expect a promotion from.

## Related

- `notes/2026-08-28-local-versus-global-factor-construction.md` — Fama–French 2012, regional
  breakpoints and locally-built factors. That note establishes *that* regional construction wins;
  this one supplies the covariance-structure reason and says the dummy form of it is not the best
  form.
- `notes/2026-08-28-international-momentum-country-neutral.md` — Rouwenhorst 1998's country-neutral
  variant, and the repo-specific note that region groups must be built from listing currency.
- `notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — the companion, and
  the one that complicates this note: demeaning discards a component that is itself priced.
- `notes/2026-09-10-currency-component-in-usd-converted-returns.md` — what else a region demean
  removes, since region and currency are nearly the same partition on this universe.
- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` — the statistical version of
  the same residual idea, with factors extracted rather than assigned.
- `notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the construction-dispersion
  reading of the "which specification?" problem this literature has in its own house.
- `experiments/learnings.md` (2026-09-03) — `lv_illiq_region_relative`, the lab's own DC model.
