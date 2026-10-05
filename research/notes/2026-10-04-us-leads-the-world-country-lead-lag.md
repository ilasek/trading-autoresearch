---
title: "Does the US lead the world? Cross-country return lead-lag, and what survives controlling for the other countries jointly"
authors: Rapach, Strauss, Zhou (anchor, NOT read); Aye, Balcilar, Gupta (re-estimation, read in full); Siliverstovs (abstract only)
year: 2013; 2017 (online 2015); 2016
venue: Journal of Finance 68(4), 1633–1662 (Tier 1, peer-reviewed); Empirica 44(1), 121–146 (Tier 2, peer-reviewed); KOF Working Paper 16-408, ETH Zurich (Tier 3, unrefereed)
url: https://doi.org/10.1111/jofi.12041 ; https://doi.org/10.1007/s10663-015-9313-3 ; https://doi.org/10.3929/ethz-a-010689622
citations: "Rapach–Strauss–Zhou: 675 (Crossref `is-referenced-by-count`, checked 2026-10-04); 717 (OpenAlex); 462 (Semantic Scholar) — all three indexes resolve it, which is itself worth recording after four nights of Semantic Scholar `not found` on real DOIs. Aye–Balcilar–Gupta: 23 (Crossref) / 25 (OpenAlex), checked 2026-10-04. Siliverstovs: not resolved by DOI (the ETH handle returned HTTP 500); RePEc reports 10 citations, checked 2026-10-04."
sample_period: "Rapach–Strauss–Zhou: 1980:2–2010:12 monthly (restated by the re-estimation, which uses the identical dataset and range). Aye–Balcilar–Gupta: the same 1980:2–2010:12 for its subsample replication, extended to 1980:2–2014:12 (Sweden 1982:3) for its own rolling-window analysis."
markets: 11 industrialised countries — Australia, Canada, France, Germany, Italy, Japan, Netherlands, Sweden, Switzerland, United Kingdom, United States. Returns in local currency.
tier: "B for the cluster, and the downgrade is the finding rather than a complaint about access. The anchor is Tier A on venue and citations and was **NOT read** (closed on every index and route tried); the only source read in full is a Tier-2 re-estimation **using the anchor's own models, data and sample range**, which reproduces the anchor's result under two of its four specifications and **reverses it under the other two**. A Tier-A claim that a Tier-2 re-run on identical data overturns in half its specifications is a Tier-B claim."
validation_overlap: false
published_post_2018: false
---

## Access

**The anchor is closed on every route tried and nothing in this note is taken from it beyond its
abstract.** `10.1111/jofi.12041`: Unpaywall `is_oa: false`; OpenAlex `oa_status: closed`,
`any_repository_has_fulltext: false`, `locations` list containing only the DOI resolver; Semantic
Scholar `openAccessPdf.status: CLOSED` with an empty URL. Routes tried and failed:

- **The corresponding author's own publication page** (`sites.google.com/slu.edu/daverapach/
  publications`) lists this article with its full abstract and links **only the Journal of Finance
  Internet Appendix**, not the paper. Worth recording as a near-miss: the faculty-page lesson
  ([2026-09-18], extended [2026-10-03]) works, but a prolific author's own page can host the
  *supplement* and not the article.
- **A new "looks like an answer" refusal mode, the eighth this folder has catalogued.**
  `sites.google.com/a/slu.edu/rapachde/JF_8895_IA_RAPACH_STRAUSS_ZHOU.pdf` — a legacy Google Sites
  file URL with a `.pdf` extension — returns **HTTP 200 with a ~940 KB body that is the Google Sites
  application shell**, not the file, and the `?attredirects=0&d=1` legacy download form returns the
  same. No Drive file id is embedded, so there is nothing to follow. Like the Incapsula [2026-09-18]
  and `gsbpreserve` cases it answers rather than refuses; the only tell is `file` on the result.
- **`api.fatcat.wiki` (scholar.archive.org's metadata API) died with `Recv failure: Connection reset
  by peer`** on a DOI lookup. This is the same transport signature `research/README.md` records for
  `web.archive.org` [2026-10-01] and should be reported the same way: **a transport failure through
  this environment's relay, not an origin refusal.** The `archive.org` metadata and availability APIs
  remain reachable; `fatcat.wiki` is not.
- `apps.olin.wustl.edu/faculty/zhou/` (404) and `sites.slu.edu/rapachde/` (TLS handshake failure,
  `SSL_ERROR_SYSCALL`) are both dead; the live pages are `olin.wustl.edu/faculty/guofu-zhou` and the
  Google Sites address above, neither of which carries the file.

**The re-estimation was reached first try and is the note's evidentiary basis.**
`repository.up.ac.za/bitstreams/<uuid>/download` (University of Pretoria, the third author's
institution) served a 451 KB PDF that parses cleanly. **University of Pretoria's DSpace is a working
channel** and this is the third institution in two nights to serve a closed article's working paper
from a co-author's home repository.

**The third source is unread.** `doi.org/10.3929/ethz-a-010689622` redirected to
`research-collection.ethz.ch/handle/20.500.11850/118883` and returned **HTTP 500**; the DSpace REST
API returned **401** on `/server/api/core/items` and **403** on
`/server/api/discover/search/objects`. Three error classes from one host, so this is server/policy
behaviour rather than a rate limit. The abstract was taken from the RePEc listing and is the only
thing used from it.

## Mechanism

**Gradual information diffusion across borders.** A return shock originating in one market is
information about global fundamentals, but it is not incorporated into other markets' prices
immediately — attention, analyst coverage and the cost of processing foreign news are all finite — so
the shock shows up abroad partly contemporaneously and partly with a lag. The lag is what makes a
lagged foreign return a predictor. The anchor's abstract states exactly this: *"return shocks arising
in the United States are only fully reflected in equity prices outside of the United States with a
lag, consistent with a gradual information diffusion explanation."*

This is the same mechanism family this folder already holds for **industries**
(`2026-08-30-industry-lead-lag-gradual-diffusion.md`), for **within-industry firm pairs**
(`2026-08-31-intra-industry-lead-lag-grouping.md`) and for **price delay**
(`2026-09-05-price-delay-market-frictions.md`). The cross-country version's extra content is the
claim of **asymmetry**: one specific node (the US) is said to lead, and the others are said not to
lead it. Asymmetry is what distinguishes a genuine diffusion story from the mechanical
cross-autocorrelation that `2026-09-05-cross-serial-correlation-as-restatement.md` and
`2026-09-08-nonsynchronous-trading-econometrics.md` show can be generated by own-autocorrelation plus
non-synchronous measurement with no diffusion at all.

**The structural formalisation, and it is the part that survives.** Both sources estimate a
**news-diffusion model** by two-step GMM with two structural parameters per country pair: a total
impact (`δ̃_{i,USA}`, the full eventual effect of a unit US return shock on country `i`) and a
**diffusion parameter** (`θ̃_{i,USA}`, the fraction of that total impact incorporated
*contemporaneously*). `θ̃ < 1` is the information friction; `θ̃ = 1` is instantaneous diffusion and no
predictability. The re-estimation rejects `δ̃ = 0` at 1% **for every country in every subperiod**, and
rejects `θ̃ = 1` in favour of `θ̃ < 1` in **48 of 66 cases** — fewer than the anchor's reported 100%,
but the same sign, and the pooled estimates are uniformly `δ̃ > 0` and `θ̃ < 1`. **So the underlying
friction is robust; what is fragile is the identification of which market is the source.**

## Construction recipe

Four specifications, in increasing order of how much they control for, and the ordering is the point.

1. **Pairwise predictive regression.** Regress country `i`'s excess return on its own lagged return,
   country `j`'s lagged return, and country `i`'s national predictors (nominal short rate, dividend
   yield). One regression per ordered pair. This is the specification that produces "the US leads".
2. **Pooled predictive regression.** The same, imposing common slopes on the national predictors
   across countries (`β_{i,b} = β_b`, `β_{i,d} = β_d`) while keeping country-specific intercepts.
3. **Augmented VAR(1) with all countries' lagged returns**, estimated by **pooled OLS**. This is the
   specification that asks whether country `j` predicts country `i` *after controlling for the other
   nine countries' lagged returns* — a joint rather than a pairwise question.
4. **The same augmented VAR estimated by adaptive elastic net** (Zou–Zhang), with bias-corrected wild
   bootstrap confidence intervals, to recover power and precision in a wide predictor set.

Plus the **news-diffusion GMM model** above, and — the re-estimation's own addition — **Bai–Perron
multiple-structural-break tests**, a **BDS nonlinearity test**, and a **residual-based bootstrap
modified-LR Granger causality test applied to rolling subsample windows**, which date-stamps when a
causal relation holds instead of assuming it is constant. The rolling specification imposes
`Φ₁₂(L) = 0` (US returns treated as exogenous), justified by the pairwise finding that non-US returns
mostly do not predict the US.

**Lag order by Schwarz criterion; returns as first log differences of local-currency price indices
minus the annualised 3-month Treasury bill rate; monthly frequency throughout.** Local currency, not
USD, and the re-estimation says why: converting would mix the FX return into the predictability being
measured.

## Robustness evidence (qualitative only)

**Two of four specifications reproduce the anchor; two reverse it.** This is the note's reason to
exist and it is a like-for-like comparison — the re-estimation uses *the anchor's own dataset and
sample range* for its subsample work, so the divergence is specification, not data.

- **Pairwise predictive regression: reproduces.** US lagged returns significantly predict every
  other country's returns in at least one subperiod except Japan and Switzerland; **34 of 66
  significant cases**, and the US has the largest coefficient in 15 cases. Only Sweden consistently
  predicts the US in return.
- **News-diffusion GMM: reproduces**, with the quantitative softening noted above (48/66 against
  100%).
- **Pooled predictive regression: reverses.** The re-estimation reports "a completely different
  result with respect to the size and significance of the coefficients, `R²` and `χ²` statistics",
  attributing it to accounting for structural breaks.
- **Augmented VAR, pooled OLS: reverses hard.** **No significant role for US returns over
  international returns at any subperiod.** Instead **Switzerland** shows the strongest positive
  predictive power, then Sweden, with the Netherlands negative.
- **Augmented VAR, adaptive elastic net: reverses.** **Switzerland leads with 27 of 66 significant
  cases; the US falls to 8 of 66** and is weaker where it appears.

**The ordering has an interpretation and it is the transferable one.** The specifications that find a
US lead are the ones that look at **one foreign market at a time**; the specifications that look at
**all ten simultaneously** attribute the lead elsewhere. A pairwise regression cannot distinguish "the
US leads" from "the US is the most correlated member of a bloc that leads"; a joint specification can,
and when it does, the US is not the node it picks. That is not a refutation of the diffusion mechanism
— the structural `θ̃ < 1` result survives both — it is a refutation of the **source attribution**.

**A second source reports the relation is state-dependent.** Siliverstovs (abstract only, unrefereed)
reports that the international predictability of excess returns from lagged US returns is
**asymmetric across business-cycle states**, with most of the positive evidence accruing during US
recessions and only limited evidence during expansions, across 10 industrialised countries. The
re-estimation reaches a compatible conclusion from a different direction — its rolling bootstrap
finds US predictive ability significant "at certain sub-periods" for every country and concludes
that "it would be misleading to rely on results based on constant-parameter linear models". **Two
independent sources therefore say the same thing: this is a conditional relation, and a
constant-coefficient estimate of it is an average over states.**

**No tension with `experiments/learnings.md` is created by this note**, and one alignment is worth
stating: the lab's `lead-lag-spillover` work has been at the industry/group level, and this is the
first source cluster here at the **country** level. The learnings file's warning not to carry
`price-trend` constants into a new family by analogy applies in full.

## Implementability here

**This universe is unusually well suited to the question and badly suited to the sources' answer.**
`program.md` notes 15 regions and 42 ETFs, which is exactly the panel a country lead-lag test wants —
far better than the sources' 11 countries. But three of the sources' ingredients are unavailable
here, and one of them is load-bearing.

**What is not available.** The nominal short rate and dividend yield controls are **fundamentals and
macro series this lab does not have**, and they are not decoration: they are what makes the predictive
regression a statement about lagged *returns* rather than about a correlated valuation level. Excess
returns over a bill rate are likewise unavailable. So any implementation here is the sources'
specification **with the national controls dropped**, which is a weaker test than either source ran,
and the hypothesis must say so rather than claim the paper's result.

**What is available, and the ordering is deliberate — the cheapest is also the one that decides the
rest.**

1. **Free, zero trials: run the specification ladder, not the signal.** The entire content above is
   that a pairwise and a joint specification disagree about *which* region leads. On this panel, with
   ETF-level region returns only, estimate (a) pairwise lagged-return predictive regressions for every
   ordered region pair on **train only**, and (b) the joint version with all regions' lagged returns
   included. **Then compare the identity of the leading node across the two.** If the ladder's two
   rungs disagree here as they do in the source, the family's headline claim is unidentified on this
   panel and no trial should be spent on a US-leads signal. If they agree, that agreement is the
   strongest motivation this family has had.
2. **The anti-candidate, stated so it is not built.** **Do not build a "lag the US ETF into the other
   regions" signal on the strength of the anchor's title.** On the two specifications that control for
   the other regions jointly, the leading node in the sources' own data is **Switzerland**, not the
   US — a result nobody would have guessed and which no economic story in either paper predicts, which
   is itself a reason to treat *any* single-node attribution here as fragile. The honest form of this
   family's signal is **region-neutral cross-sectional**: rank regions on the prior period's return of
   *the whole set*, rather than nominating a leader.
3. **Non-synchronous measurement is the first confound, not the second.** This panel's index is the
   union of fifteen exchange calendars and is forward-filled
   (`experiments/learnings.md` records the limit as 10 days, and the `%zero` finding
   [Measured 2026-09-28] shows what that construction does to a statistic imported as a proxy). A
   cross-region lead-lag estimate on a forward-filled union calendar will find lead-lag that is
   **calendar artifact**, and `2026-09-08-nonsynchronous-trading-econometrics.md` plus
   `2026-09-05-cross-serial-correlation-as-restatement.md` give the correction. Any measurement under
   (1) must be run at a frequency coarse enough — monthly, matching the sources — that a one-day
   holiday offset cannot generate the result.
4. **If a scout is eventually spent here, the state-dependence finding forbids the obvious overlay.**
   Two sources say the relation holds in some states and not others. The lab's own record is that
   **three de-risking/regime overlays on this book all backfired out of sample**
   (`experiments/learnings.md`, first strategy learning). Conditioning a lead-lag signal on a
   recession or trend state is therefore a construction this lab has already paid to learn about:
   **use the state-dependence as a reason to expect a low unconditional `t`, not as a licence to build
   a switch.**

## Related

- `2026-08-30-industry-lead-lag-gradual-diffusion.md`, `2026-08-31-intra-industry-lead-lag-grouping.md`
  — the same mechanism at the industry and within-industry level, which is where this family's
  coverage was until now.
- `2026-09-05-cross-serial-correlation-as-restatement.md`,
  `2026-09-08-nonsynchronous-trading-econometrics.md` — the two ways a lead-lag estimate on this panel
  can be an artifact; both are preconditions for item (1).
- `2026-09-05-price-delay-market-frictions.md` — the cross-sectional measure of the same friction.
- `2026-08-28-international-momentum-country-neutral.md`,
  `2026-09-10-country-industry-global-return-decomposition.md`,
  `2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — what a country axis does to a
  global cross-section; relevant to the region-neutral form in item (2).
- `2026-09-10-currency-component-in-usd-converted-returns.md` — the sources keep returns in local
  currency on purpose; this lab's panel is USD-converted, so that note is the bridge.
- `2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — covers Rapach–Strauss–Zhou
  (2010, RFS), the same authors' combination paper, and is the only prior coverage of this group here.
