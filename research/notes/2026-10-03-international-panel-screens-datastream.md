---
title: "Individual Equity Return Data from Thomson Datastream: Handle with Care! — reached by proxy through: U.K. Cross-Sectional Equity Data: Do Not Trust the Dataset! The Case for Robust Investability Filters"
authors: Ince, Porter (primary, NOT read); Rossi (vehicle, read in full)
year: 2006; 2011
venue: Journal of Financial Research 29(4), 463–479 (Tier 1/2, peer-reviewed); MPRA working paper 38303 (Tier 3 — unrefereed working paper)
url: https://doi.org/10.1111/j.1475-6803.2006.00189.x ; https://mpra.ub.uni-muenchen.de/38303/
citations: "Ince–Porter: 747 (Crossref `is-referenced-by-count`, checked 2026-10-03); 897 (OpenAlex, checked 2026-10-03); Semantic Scholar returns a clean `Paper with id DOI:… not found` for this real, twice-indexed DOI — the **fourth** instance of the failure mode first recorded [2026-10-01] (checked 2026-10-03). Rossi: not indexed (OpenAlex title and keyword search return no result; Semantic Scholar search returned HTTP 429; checked 2026-10-03) — an MPRA working paper with no registered DOI, so per this folder's rubric the missing count is not itself a tier downgrade, but the unrefereed venue is."
sample_period: "Ince–Porter: US 1975–2002 (Datastream versus CRSP), plus unspecified international markets. Rossi: London Stock Exchange, 1990 onward."
markets: "Ince–Porter: US plus several international markets. Rossi: UK (LSE) only, with Bloomberg as a cross-check source."
tier: "Split, and the split is the point. **Ince–Porter is Tier A on its own merits** — peer-reviewed, ~750–900 citations, and the de facto standard citation for screening a commercial international equity panel — **but it was NOT read** (verified closed on all three indexes, zero repository fulltext anywhere; see Access). Everything attributed to it below is **restated from Rossi's survey of it** and is flagged at each use. **Rossi is Tier C** as a source of claims (single market, unrefereed, unindexed) but is a usable *vehicle*: its contribution is an explicit, checkable filter list, not a performance claim, and a recipe can be read off a Tier-C paper in a way an effect size cannot."
validation_overlap: false
published_post_2018: false
---

## Access

**Ince–Porter (2006) was NOT read, and this is the second consecutive night it has defeated every
route.** It was named as gap (c) in the [2026-10-02] open questions — "a genuinely well-aimed gap for
this repo and it should be chased" — and tonight it was chased and reached only by proxy.

Closure is now **documented rather than assumed**: OpenAlex reports `oa_status: closed`,
`any_repository_has_fulltext: false`, and its entire `locations` list is the DOI resolver plus a dead
`blackwell-synergy.com` abstract page. Routes tried and failed tonight:

- **SSRN working paper 486523** (the 2004 version, which Crossref surfaces) — SSRN refuses automated
  clients, as this folder recorded on 2026-08-17 and has re-confirmed since.
- **`econstor.eu` discover search** — returns HTTP 200 with a 7.9 KB body containing no hit for the
  title. econstor remains a good channel; it simply does not hold this paper.
- **`ifm.unibe.ch`** served a 2 MB PDF named `DATASTREAM.pdf` that a search ranked highly for this
  title. **It is a 2017 University of Bern student manual for operating the database, not the paper.**
  Recorded because it *looks like* a hit and is not one — the same shape as the Incapsula and
  `gsbpreserve` cases, but caused by filename coincidence rather than by a refusal.
- Semantic Scholar's `not found` on this DOI removed the usual `openAccessPdf` route before it started.

**A third refusal host, and it is a new shape for a host this folder will meet again.**
**`pyxida.aueb.gr` (Athens University of Economics and Business) is behind Anubis and returns HTTP
200** with a ~2.4 KB body reading `Oh noes! Access Denied: error code …  Protected by Anubis From
Techaro`, on both the `handle/` landing page and the `server/api/core/bitstreams/<uuid>/content`
endpoint. Anubis was first recorded [2026-09-30] at Frankfurt; **note that AUEB runs the same DSpace
software that `ecommons.cornell.edu` served a file from tonight without complaint**, so the
repository platform predicts nothing about reachability — the institution's bot policy does.

**Two further sources on exactly this question were located and NOT read.** Both are recorded so the
next session does not repeat the searches, and **nothing in this note is taken from either**:

- **Landis & Skouras (2021), "Guidelines for asset pricing research using international equity data
  from Thomson Reuters Datastream", *Journal of Banking & Finance* 130, 106128** —
  `10.1016/j.jbankfin.2021.106128`, 47 (Crossref) / 53 (OpenAlex) citations, checked 2026-10-03,
  `oa_status: closed` with no repository copy on any index. **This is the best-aimed source this
  folder has identified for gap (c)** and it is a better target than Ince–Porter itself: per its
  abstract it provides guidelines *and code* to derive high-quality international equity data,
  raising coverage to 91 countries while improving accuracy and **reducing survivorship bias and data
  staleness** — three of this lab's live concerns in one sentence. The AUEB PhD thesis that appears
  to contain it as a chapter (Landis, "Three Essays on Empirical Asset Pricing in International
  Equity Markets") is the Anubis-blocked `pyxida` item above. **Next route, and it is the strong one:
  the paper ships code, so the [2026-09-07] lesson applies — look for the authors' published
  reference implementation**, which would be a complete and unambiguous primary for the screens.
- **Schmidt, von Arx, Schrimpf, Wagner & Ziegler (2019), "Common risk factors in international stock
  markets", *Financial Markets and Portfolio Management* 33(3), 213–241** —
  `10.1007/s11408-019-00334-3`, 58 (Crossref) citations, checked 2026-10-03. Per its abstract it gives
  a "step-by-step description of how appropriately screened data from Thomson Reuters Datastream and
  Worldscope can be used to construct high-quality systematic risk factors" for 23 countries, and is
  cost-aware (its own headline premium is reported as often eroded by transaction costs).
  `archive-ouverte.unige.ch/unige:193794` lists a **public, OA-licensed** published-version PDF with a
  file `resId`, but **five plausible download-URL forms all returned HTTP 404** and the UNIGE API's
  real download path was not found; `link.springer.com` returns a 372 KB HTML landing page for both
  its article and `content/pdf` endpoints, containing the abstract and references but not the body.
  **Next route: find UNIGE's correct bitstream-download path, which would make this fetchable.**

## Mechanism

**A commercial international equity panel is not a clean panel, and its defects are not random — they
are concentrated exactly where cross-sectional strategy research looks.** The following is
**Ince–Porter's content as restated by Rossi**, who surveys it at length and implements it; it is not
read from Ince–Porter.

Their findings, grouped:

**Classification is unreliable, and not point-in-time.**
- Many securities the database flags as common stock **are not** — unit trusts, investment trusts,
  closed-end funds, preferred shares, ADRs, warrants, split issues. The database's own type fields do
  not let you separate them reliably.
- **The full time series of a classification variable often reflects only its most current value.**
  This is a lookahead hazard of exactly the kind this lab worries about: the "sector", "country" or
  "type" of an instrument as stored today is applied backwards over its whole history.
- There is no clean fix from inside the vendor's data. The remedies are a **second data source** and
  **keyword screening on security names**.

**Quantitative series contain dated errors.**
- Stock splits reflected on **incorrect dates**; disagreements in closing prices and dividend
  payments against an independent source; errors in total-return construction; wrong time markers for
  the beginning and end of a price series; and mishandled **returns after suspension periods**.
- **Rounding of low nominal prices** produces discrete, spuriously large percentage jumps.

**And the errors are concentrated in the small-cap end.** Ince–Porter report that most (not all) of
the problems sit in the **smaller size deciles** — which, as Rossi stresses, is precisely what makes
them lethal for studies sorting on cross-sectional characteristics rather than for index-level work.

**The validation diagnostic is the most transferable thing in this note.** Ince–Porter grade their own
filters by computing, per country, the **cross-sectional market-cap-weighted average return of their
sample** and correlating it against that country's **published total-market index return** — an
independently constructed, value-weighted series usable as an "error-free" aggregate. On raw data the
correlation runs **as low as ~0.20**; after their filters it rises to **~0.98**. For the UK
specifically, data-based filters alone are *not* enough to lift the correlation; it reaches ~0.99 only
once the **misclassification** filters are applied. So: the diagnostic is cheap, it is external, and
it distinguishes *which class* of defect is binding.

## Construction recipe

**Ince–Porter's own screens, as restated** (the ones Rossi attributes to them specifically): exclude
stocks trading **below $1** (rounding-driven discrete jumps); apply a **return-reversal filter** — a
very large return immediately reversed is treated as a price error rather than a return, with a
threshold around **±300%** combined with a reversal condition; and screen **security names by keyword**
to remove non-common-stock instruments the type field misclassifies.

**Rossi's implemented list** (his own, read in full from his paper). Sample-selection screens: keep
only instruments flagged as equity; drop foreign-currency denominations, non-common-stock vehicles,
instruments without adjusted price history, non-"major" listings where an issuer has several, and
secondary listings (keeping the primary); require a minimum return history of **24 consecutive months**
verified *without relying on the vendor's own date fields*; drop instruments missing any of
returns/prices/volume/shares outright.

Investability and liquidity screens, which he derives from published index-provider methodology
(MSCI, FTSE) rather than inventing:
- a **minimum market-capitalisation threshold**, with **hysteresis**: once an issue qualifies it stays
  in the sample until its cap falls more than **10% below** the threshold — a deliberate buffer for
  sample stability;
- minimum **annualised monthly turnover of 10%** in each of the past 12 months, and minimum
  **annualised quarterly turnover of 20%** in each rolling quarter of the past year;
- **traded on at least 90% of trading days in the previous 12 months**;
- exclude both **very low and very high nominal prices** (he uses 10 GBp and 10,000 GBp; MSCI uses
  $1 and $10,000) — the low end for rounding and fractional-price jumps, the high end for liquidity.

**The attrition is the headline number, and it is a recipe-level fact rather than a performance one.**
Rossi's raw LSE equity universe of **7,968** instruments falls to **4,092** after basic
classification screens, to **3,127** after cross-checking those against a second source and keyword
screening, and to **1,333** after his data-quality and size screens — **roughly 83% of a raw
single-market commercial equity panel discarded**. Of the instruments that already passed the basic
screens, the single largest cause of further exclusion is **clearly wrong shares-outstanding data
(≈48%)**, followed by **missing volume (≈11%)** and insufficient history (≈6%). He notes these
figures understate the problem, being measured on an already-filtered sample.

## Robustness evidence (qualitative only)

- **Ince–Porter's standing is the strongest evidence available for it**: ~750–900 citations and, as
  Rossi documents, its screens are **echoed by the subsequent international-data literature** —
  Bartram et al. and Guo–Savickas adopt its reversal filter, and later guideline papers
  (Landis–Skouras; Schmidt et al.) exist to extend it. An unread paper whose recipe has been
  independently re-implemented by several Tier-1 teams is better evidenced than its citation count
  alone suggests.
- **Its validation method is self-checking**, which is unusual and raises confidence: the
  raw-versus-filtered correlation against an independent index is a falsifiable grade on the filters,
  not an appeal to authority.
- **Multi-market**: Ince–Porter report the same defects across several international markets, not only
  the US panel they benchmark against CRSP.
- **Rossi's own evidence is weak and is treated as such**: single market, single period, unrefereed,
  uncited, and his cross-checks rest on a commercial second source this lab does not have. His
  *numbers* are recorded here only as orders of magnitude for panel attrition, and his *filter list*
  as a menu — neither as a measured effect.
- **The cleanest limitation, and it is this lab's problem too**: everything here is about one vendor's
  data. Nothing in it is evidence about the free data in `data/store/`, whose defects may be worse,
  better, or simply different. **No source read tonight says anything about the error profile of free
  price data, and this folder should not pretend otherwise.**

## Implementability here

**Not a candidate strategy. This is the data-hygiene half of the cluster** — and it is the half aimed
at the question that has the lab's strategy sessions halted.

- **The single most valuable item is the external-aggregate diagnostic, and this lab can run it with
  zero new data.** Ince–Porter grade a panel by correlating its cross-sectional value-weighted average
  return against an independent published index. **This universe contains ~42 ETFs across 15 regions**,
  a number of which are region or country index trackers — i.e. the lab already holds independently
  constructed, value-weighted aggregates of roughly the same regions its single stocks sit in. So the
  diagnostic becomes internal: **for each region, correlate the cross-sectional average return of that
  region's single stocks against the matching index ETF's return.** A low correlation in a region
  localises a data defect to that region; a high one retires the concern there. It needs no holdout,
  no new download, and no trial. **This is the cheapest data-integrity check available to this repo
  and it has never been run.**
- **Note what it can and cannot settle.** It is a test for *classification and price-series* defects,
  which is what Ince–Porter built it for. It is **not** a test for survivorship — a point-in-time
  membership error leaves the surviving names' prices perfectly correlated with the index while still
  biasing the mean, so a correlation near 1.0 would **not** exonerate `origin/survivorship-pit-v2`'s
  complaint. The two concerns are separate and this diagnostic only closes one of them. Stating that
  explicitly matters because the test is cheap enough to be over-read.
- **The staleness screen is directly implementable and is the one screen the lab arguably needs.**
  "Traded on at least 90% of trading days in the previous 12 months" is computable from closes alone,
  causally, with a rolling window — and in this panel the obvious proxy for "did not trade" is a
  repeated close or, per `2026-09-04-global-liquidity-proxy-horserace.md`, a zero return. The lab's
  own contract says volume is **not** forward-filled and is NaN on foreign holidays, which means a
  genuine non-trading day and a vendor gap look identical in the volume frame. Ince–Porter's finding
  that panels contain real, non-holiday gaps is the reason this distinction is not pedantic.
- **The `liquidity-volume` family is built on the most gap-prone field in the panel.** Rossi's
  attrition table puts **missing volume at ~11%** of an already-screened sample and bad
  shares-outstanding data at ~48%. The lab cannot use shares outstanding at all (no fundamentals), so
  that larger problem is moot here — **but `ILLIQ`, dollar-volume and volume-shock signals all run on
  the field that was second-worst.** Any `liquidity-volume` result should be reported alongside the
  fraction of its signal days that were interpolated or NaN-filled. This compounds the warning in
  `2026-10-03-mean-return-computation-rebalanced-vs-buy-and-hold.md`, which is that volume-sorted
  books also carry a differential averaging bias — **two independent reasons to distrust that family's
  levels specifically.**
- **The low-price screen has a real analogue here and the high-price one does not.** Rounding-driven
  jumps at low nominal prices are a plausible defect in any panel; a `$1`-style floor is cheap
  insurance and is the one Ince–Porter screen most likely to bind on a global panel of ~140 names.
  A high-price exclusion is index-construction practice about liquidity and has no force in a universe
  this small and this liquid.
- **The reversal filter deserves care, not adoption.** "A large return immediately reversed is an
  error" is a reasonable data screen and a **terrible** thing to apply blind in this lab, because
  short-term reversal is a *real effect this universe has been tested on*. A filter that deletes
  exactly the observations a reversal strategy trades would manufacture its own answer. If used at
  all it should be used at the ±300% magnitude Ince–Porter chose — far outside any genuine daily
  move — and never tightened toward the range where real reversals live.
- **The hysteresis idea generalises beyond data hygiene.** Rossi's "once in, stay in until 10% below
  the threshold" is **banding applied to universe membership** rather than to weights, borrowed from
  index-provider practice. That is the same device as the no-trade region in
  `2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`, one level up. The lab's universe is
  fixed, so this is not directly actionable on membership — **but it is directly actionable on any
  candidate that selects a sub-universe by a threshold** (the lab has promoted at least one book that
  is "equal-weight the low-beta 37% of the universe"), where hysteresis on the inclusion rule is a
  turnover reduction the cost model would reward. **Flagged as a mechanism, not measured here.**
- **Pitfall, and it is this folder's standing rule:** none of these thresholds (24 months, 90% of
  days, 10%/20% turnover, the $1 floor) were measured on this universe or on free data. They are
  index-provider conventions for large single markets. Per `CLAUDE.md`'s rule against carrying
  constants across families by analogy, **re-measure them here or say you have not.**

## Related

- `2026-10-03-mean-return-computation-rebalanced-vs-buy-and-hold.md` and
  `2026-10-03-caveat-compounder-daily-rebalancing-bias.md` — tonight's other two notes. The link is
  causal, not thematic: the defects catalogued here (bounce at low prices, stale and non-synchronous
  quotes, suspension artifacts) are the *generators* of the individual-security negative
  autocorrelation that drives the averaging bias those notes quantify. **Dirty panel → more bounce →
  bigger estimator bias.**
- `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — the leavers problem. Ince–Porter
  report coverage and survivorship distortions in the same panel, and their non-point-in-time
  classification fields are a concrete mechanism for how a panel comes to be survivorship-conditioned
  in the first place.
- `2026-10-01-survival-conditioning-induced-drift.md` — what that conditioning does to a mean.
- `2026-09-04-commonality-in-liquidity-across-countries.md` — Karolyi–Lee–van Dijk, already covered;
  its data appendix was named [2026-10-02] as a possible route to these screens and remains one.
- `2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — Hou–Karolyi–Kho, already
  covered; the other named route.
- `2026-09-04-global-liquidity-proxy-horserace.md` — the zero-return proxy, which is how the staleness
  screen above would actually be computed here.
- `2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — banding, of which Rossi's
  membership buffer is the universe-level case.
