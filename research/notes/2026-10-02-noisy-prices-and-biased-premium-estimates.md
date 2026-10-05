---
title: "Liquidity Biases in Asset Pricing Tests — with: Noisy Prices and Inference Regarding Returns"
authors: Asparouhova, Bessembinder, Kalcheva
year: 2010; 2013
venue: Journal of Financial Economics 96(2), 215–237 (Tier 1); Journal of Finance 68(2), 665–714 (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2009.12.011 ; https://doi.org/10.1111/jofi.12010
citations: "ABK 2010 (JFE): 213 (Crossref is-referenced-by-count, checked 2026-10-02); 219 (Semantic Scholar DOI endpoint, checked 2026-10-02). ABK 2013 (JF): 220 (Crossref, checked 2026-10-02); 208 (Semantic Scholar, checked 2026-10-02). OpenAlex not consulted — free daily budget exhausted at session start."
sample_period: "CRSP monthly returns; neither paper's exact window was read. ABK 2010 reports results both including and excluding illiquid securities and separately for NYSE/Amex after decimalization (2001), so its sample straddles that date."
markets: US equities (CRSP), individual securities and characteristic-sorted portfolios
tier: "A on venue, authorship and citation count — both are Tier-1 methodological results about an estimator, and an estimator's bias does not decay. **Coverage here is abstract-level only** (see Access): the mechanism and the *form* of the correction are recorded; the correction's algebra is NOT, and nothing below should be implemented as if it were."
validation_overlap: false
published_post_2018: false
---

## Access

**Neither paper was read. Both abstracts below are authoritative**, read from **ASU's Elsevier Pure
instance** (`asu.elsevierpure.com/en/publications/<slug>`), which serves the full publisher abstract
in the page body for each of Bessembinder's articles. That host is a **new working channel** for
abstracts of closed articles by any author at an institution running Pure, and it is worth trying
before giving up on a closed paper.

Routes that failed:
- Unpaywall reports `oa_status: closed` for both DOIs, and for Blume–Stambaugh (below).
- Semantic Scholar reports `openAccessPdf: GREEN` for the JF article pointing at
  `onlinelibrary.wiley.com/doi/pdfdirect/10.1111/jofi.12010`. **That URL is Cloudflare-challenged**
  (HTTP 403, ~5.7 KB "Just a moment…"). This is the second night running that a GREEN OA flag has
  turned out not to be a fetchable file — after 2026-10-01's bepress case. **Record the rule: an
  `openAccessPdf`/`oa_status: green` from any of the three indexes is a claim about a URL's existence,
  not about its reachability.**
- `www.public.asu.edu/~hbessemb/` — Bessembinder's own page — returns HTTP 200 but the body is an
  **ASU SSO / Cloudflare Access OAuth redirect** (`signin.asu.edu/oauth2/authorize?...`). This is a
  thirteenth distinct refusal shape and a close cousin of the 2026-09-08 `pm-research.com` case: a
  200, no challenge page, just an authorization flow where the content should be. The
  2026-09-18 faculty-page trick fails on any university that has put its `public` tree behind
  Cloudflare Access.
- `eccles.utah.edu` (Asparouhova) hosts no PDFs. `wrap.warwick.ac.uk/188774`, which a search surfaced,
  is a PhD thesis (Tier 4) and was not used.

**A third source in this cluster was located and not covered: Blume & Stambaugh (1983), "Biases in
Computed Returns: An Application to the Size Effect", Journal of Financial Economics 12(3), 387–404**
— 582 Crossref / 830 Semantic Scholar citations (checked 2026-10-02), `oa_status: closed`, no OA
location, and Stambaugh's Wharton page does not host it. It is the origin of this literature.
**Nothing is claimed from it here**; it is recorded so a later session can go straight at it.

## Mechanism

This folder mentions "bid-ask bounce" in thirteen notes and has never once covered the **correction**
for it. That is the gap this note opens, and it is a gap about an *estimator*, not about a signal.

**The setup.** A recorded transaction price is the unobserved fundamental value times a transitory,
mean-reverting error — bid-ask bounce, a stale quote, a thin print, a non-synchronous close. Call it
multiplicative noise. The noise reverses, so it contributes nothing to a long-horizon return. But it
does not wash out of an *average*: a return computed from two noisy prices has the noise in it twice,
with opposite sign, and the arithmetic mean of such returns is biased **upward**, because a
downward-noisy price at the start of a period becomes an upward-looking return over it. The bias is of
the order of the noise variance, so it is largest for exactly the securities whose prices are noisiest.

**ABK 2013 — what gets biased.** From the abstract:

> "Temporary deviations of trade prices from fundamental values impart bias to estimates of mean
> returns to individual securities, to differences in mean returns across portfolios, and to
> parameters estimated in return regressions. We consider a number of corrections, and show them to be
> effective under reasonable assumptions. In an application to the Center for Research in Security
> Prices monthly returns, the corrections indicate significant biases in uncorrected return premium
> estimates associated with an array of firm characteristics. The bias can be large in economic terms,
> for example, equal to 50% or more of the corrected estimate for firm size and share price."

Three distinct objects, and the lab computes all three: a security's mean return, a **difference in
mean returns across portfolios** (which is what every high-minus-low decile spread is), and a
**regression parameter** (which is what every IC and every Fama-MacBeth slope is).

**ABK 2010 — why it is worst where it matters most.** From the abstract:

> "Microstructure noise in security prices biases the results of empirical asset pricing
> specifications, **particularly when security-level explanatory variables are cross-sectionally
> correlated with the amount of noise.** We focus on tests of whether measures of illiquidity … are
> priced in the cross-section of stock returns, and show a significant upward bias in estimated return
> premiums for an array of illiquidity measures in CRSP monthly return data. The upward bias is larger
> when illiquid securities are included in the sample, but persists even for NYSE/Amex stocks after
> decimalization. We introduce a methodological correction to eliminate the biases that simply involves
> weighted least squares (WLS) rather than ordinary least squares (OLS) estimation, and find evidence
> of smaller, but still significant, return premiums for illiquidity after implementing the
> correction."

The emphasised clause is the whole mechanism in one line. **A characteristic that proxies for how
noisy a price is will appear to be priced even if it is not**, because the characteristic and the
estimator's bias are the same thing measured twice. Illiquidity, share price level, size, and
turnover are all such characteristics. The bias is a *confound specific to noise-correlated scores*,
not a uniform haircut.

Two secondary points in that abstract are each worth as much as the headline:

- **It does not go away by cleaning the sample.** The bias shrinks when illiquid names are dropped
  but "persists even for NYSE/Amex stocks after decimalization" — i.e. a large-cap, tight-spread,
  modern sample is *reduced-noise*, not noise-free.
- **The premium does not go to zero.** After the correction the illiquidity premiums are "smaller, but
  still significant." This is a bias result, not a debunking, and importing it as "illiquidity is
  fake" would be a misreading.

**The convergence worth recording.** Hou–Xue–Zhang
(`2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md`) find that 96% of 106
trading-frictions anomalies fail to replicate once the pool's noisiest members are stopped from
dominating the extreme deciles. ABK find that premium estimates for illiquidity measures are upward
biased by noise that is correlated with illiquidity. **These are the same finding reached from
opposite ends** — one by changing the weighting of the pool, the other by changing the estimator —
and that is a much stronger joint statement than either alone.

## Construction recipe

**Deliberately incomplete, because the papers were not read.** What is recorded:

- **The form of the correction is a weighting change, not a new signal and not a filter.** ABK 2010
  describe it as "weighted least squares (WLS) rather than ordinary least squares (OLS)". In a
  cross-sectional regression of returns on a characteristic, replacing OLS with a suitably weighted
  estimator removes the bias. ABK 2013 say they "consider a number of corrections," plural — so there
  is a family, not a single formula.
- **What is NOT recorded, and must not be guessed:** the weights. A plausible-sounding weighting is
  not a citation, and this folder's standing rule is that an estimator is only implementable once its
  algebra has been read. **Treat "the ABK correction" as a named gap, not as an available tool.**
- **What is independently implementable tonight** is the *diagnostic* half, which needs no formula:
  compute the same cross-sectional statistic under two weightings that differ in how much voice they
  give the noisiest names, and read the gap. That is HXZ's grid applied to the estimator rather than
  to the sort, and the folder already has the machinery
  (`2026-09-06-number-of-portfolios-as-tuning-parameter.md`).

## Robustness evidence (qualitative only)

Both papers are Tier-1 methodological results with three-figure citation counts, by authors with a
long track record in microstructure; the 2010 paper's central robustness exercise — showing the bias
survives in a large-cap, post-decimalization subsample — is the one that matters for transfer, because
it is the subsample most like this repo's universe. The result is analytic in origin (the bias follows
from the noise model, not from a regression), which is why it has no decay story. Against it: nothing
read here establishes the magnitude outside US equities, and the 2013 abstract's own hedge —
corrections are effective "under reasonable assumptions" — means the correction is model-dependent in a
way the bias itself is not.

## Implementability here

**This is a live confound in this repo, and it is the first one this folder has found that points in
the same direction as the survivorship artifact while having a completely different cause.**

The lab's data is noisier than CRSP's, for reasons already documented in this folder:

- free daily data, adjusted closes, no vendor-grade cleaning;
- a global universe with **non-synchronous closes** across 15 regions
  (`2026-09-08-nonsynchronous-trading-econometrics.md`);
- volume that is not forward-filled, so foreign-holiday staleness is visible in the panel and
  therefore present in the prices too;
- **USD conversion**, which adds an FX price to every non-US return
  (`2026-09-10-currency-component-in-usd-converted-returns.md`).

And the scores the lab has been screening are precisely the noise-correlated kind: Amihud `ILLIQ`,
Garman-Klass and Parkinson range volatility, dollar-volume measures, price-level and dispersion
statistics. **ABK's clause says an upward-biased premium is exactly what such a score should produce
even if it carries no signal.**

**The consequence for `learnings.md`, and it is a real one.** The lab has attributed its largest
measured artifact — "the level *is* the survivorship artifact", established across fourteen mechanism
screens — entirely to survivorship conditioning. [2026-10-01] supplied the theorem for that channel.
**ABK supply a second channel with the same sign, the same concentration in the noisiest names, and a
different fix**, and the lab has never separated them. The two are distinguishable, and cheaply:

- **Survivorship bias is a property of the pool.** It cannot be removed by changing an estimator; it
  needs a different universe. It should be *invariant* to how the cross-sectional average is weighted.
- **Noise bias is a property of the estimator.** It should *shrink* when the cross-sectional statistic
  is computed in a way that gives the noisiest names less voice, on the same pool.

So: recompute an already-recorded IC — the GK-volatility-level IC and the `ILLIQ` IC are both on
record — under a second weighting of the cross-sectional average. **If the IC moves materially, part of
what the lab has been calling the survivorship artifact is estimator bias.** If it does not move, the
survivorship attribution survives a test it has not yet faced. Train split only, no trial, no holdout,
and either outcome is a finding. This is the same shape as [2026-09-30]'s symbolic-composition test:
before attributing an effect to a mechanism, check whether a cheaper mechanism produces it.

**Second, smaller consequence.** Any future `liquidity-volume` or `range-variance` candidate should be
expected to have an upward-biased *measured* edge for reasons that have nothing to do with its
hypothesis, and the lab's own closures in those families
(`ILLIQ`'s mean channel [2026-09-24], liquidity risk [2026-09-29], dispersion) are **more credible
than they looked**, not less: they are negatives found in spite of a bias that should have flattered
them.

**Pitfalls.**
- Do not implement a weighting "from ABK" that this folder has not read. Record the diagnostic, not
  the estimator.
- Do not read this as "illiquidity is not priced". The correction leaves the premiums "smaller, but
  still significant."
- Do not expect the 50%-of-the-corrected-estimate magnitude to transfer. It is CRSP, monthly, for firm
  size and share price specifically. `CLAUDE.md`'s rule on not importing constants by analogy applies.
- The bias is in the *mean*, which is the numerator of a Sharpe ratio; it does not inflate the
  denominator. That is the same asymmetry as the survival-conditioning theorem
  (`2026-10-01-survival-conditioning-induced-drift.md`), and it is why both channels look like
  "a Sharpe inflated through its numerator" and why neither can be told from the other by looking at
  volatility.

## Related

- `2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — the same finding from the pool
  side rather than the estimator side.
- `2026-10-01-survival-conditioning-induced-drift.md` — the other numerator-only inflation, with a
  different cause and a different fix; this note's main contribution is that the lab has two and has
  only separated one.
- `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — the third member of tonight's set.
- `2026-09-08-nonsynchronous-trading-econometrics.md`, `2026-09-04-high-low-spread-estimator.md`,
  `2026-08-29-range-based-volatility-estimators.md`, `2026-09-18-overnight-intraday-return-decomposition.md`
  — the folder's existing notes on where the noise comes from, none of which cover what it does to a
  premium estimate.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md`, `2026-09-04-global-liquidity-proxy-horserace.md`
  — the measures ABK 2010 is specifically about.
- `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the folder's other
  note on changing an estimator rather than the data.
