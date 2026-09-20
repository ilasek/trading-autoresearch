---
title: "Salience Theory and the Cross-Section of Stock Returns: International and Further Evidence"
authors: Cakici, Zaremba
year: 2022 (JFE 146(2), 689–725)
venue: Journal of Financial Economics (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2021.10.010
citations: 103 (Crossref is-referenced-by-count, checked 2026-09-20); 109 (OpenAlex by DOI, checked 2026-09-20); Semantic Scholar's DOI endpoint returns "not found" for this DOI
sample_period: "the past three decades" per the abstract (≈1990 onward); exact end year NOT verified — full text not read
markets: 49 countries, developed and emerging
tier: A
validation_overlap: true (a three-decade sample in a 2022 publication necessarily reaches into 2018–2023)
published_post_2018: true
---

**NOT READ.** Only the **published abstract** was obtained, and it is quoted verbatim below.
Channels tried and their responses: `sciencedirect.com` **403** to both the article URL and its
`pdfft` endpoint (Cloudflare bot challenge, as documented in `research/README.md`);
`papers.ssrn.com` delivery endpoint **403**; OpenAlex and Unpaywall both report the article
`is_oa: true` / `oa_status: hybrid` with the **publisher as the only OA location** and
`any_repository_has_fulltext: false` — i.e. there is no green copy anywhere to fall back to;
`api.core.ac.uk` redirected into a bot-check; HAL holds nothing by this title; the author's own
site (`sites.google.com/view/adamzaremba`) links the DOI and no PDF. **A hybrid-OA article whose
only OA location is an endpoint that refuses automated clients is, in practice, unreadable here.**
Recorded as such rather than as an egress failure.

Consequently: **no construction detail, no table, and no robustness row below is sourced from this
paper's body.** Everything attributed to it is in its own abstract's words. That is a real
limitation and it is why the strategy agent should treat the qualifications below as *directionally
established by a Tier-1 venue* rather than as numbers it can reason against.

Third of three notes from 2026-09-20. **This note exists to stop a candidate, or to force it onto a
different population.** Read `2026-09-20-salience-theory-stock-prices.md` first.

## Mechanism

None of its own — this is a replication and stress test of the salience-theory (ST) measure defined
in Cosemans–Frehen, taken to an international panel. Its contribution is **where the effect lives
and where it does not**, which is the question this lab needs answered and which a single-market
paper cannot answer.

The abstract, verbatim:

> "Motivated by existing evidence of the salience theory (ST) effect in the United States, we
> investigate its importance in 49 countries over the past three decades. Initial results suggest a
> negative relationship between the ST measure and future returns. The underperformance of low ST
> stocks is the strongest in countries with high idiosyncratic risk. However, the salience effect
> has three vital limitations. First, a substantial part of the anomaly can be attributed to the
> short-term return reversal. Second, it is priced primarily among microcaps. Third, the premium is
> realized predominantly following severe down markets and volatility spikes. Outside of microcaps
> and extreme market conditions, the salience effect does not exist."

Note one thing the abstract's second sentence does *not* say, and the note does not claim: the
direction of the headline result **replicates**. The sign is right, internationally, across a large
country panel. The paper's quarrel is entirely with the effect's **scope**.

## Construction recipe

Not recoverable — the body was not read. The measure is stated to be "the ST measure", i.e. the
Cosemans–Frehen construction; implement from that note. Whether this paper varies `θ`, `δ`, the
window, or the choice of `r̄_s` is **unknown here**, and no claim in this note depends on it.

## Robustness evidence (qualitative only)

Three qualifications, each attributed to the abstract, and each one a hostile finding for a
large-cap implementation:

- **A substantial part of the anomaly is short-term return reversal.** This is a direct
  contradiction of Cosemans–Frehen's central defence, which devotes an entire section and three
  separate tests (sequential sort, reversal-factor alpha, skip-month) to arguing that `ST` is
  distinct from reversal. Two Tier-1 papers in the same journal disagree about the same measure.
  **The tension is recorded here explicitly and is not resolved by anything read tonight.** It is
  also, usefully, decidable on this repo's own data: the skip-month test is the discriminating one,
  and it is free.
- **It is priced primarily among microcaps.** Cosemans–Frehen's own value-weighted results are
  materially weaker than their equal-weighted ones and they attribute that to large stocks having
  lower retail ownership and smaller limits to arbitrage. This paper pushes the same finding to its
  conclusion across 49 countries. **This is the row that governs implementability on a
  ~145-name large-cap universe**, and it points one way.
- **The premium is realised predominantly following severe down markets and volatility spikes.**
  Recorded as a statement about the effect's **conditional structure**, not as any claim about any
  period. Two implications. First, an unconditional long-only book harvesting `ST` is trying to
  collect a premium the source says is concentrated in states this book cannot select into ex ante.
  Second, a conditional version is a **regime-timing** construction, which is `price-trend`-legacy
  territory and which this lab has priced before.
- **And the summary sentence is the one to carry:** *outside of microcaps and extreme market
  conditions, the salience effect does not exist.* Both exclusions bind on this universe.
- **Replication weight.** This is the good kind of source for the rubric's replication row: an
  independent team, a hostile prior, a much broader sample, and a Tier-1 venue willing to publish
  the negative. It is not in Hou–Xue–Zhang or Jensen–Kelly–Pedersen (both predate the ST measure's
  prominence), so it is the only replication evidence this cluster has.
- **Rubric rows.** Venue Tier 1; citations healthy for a paper of this age in both indices that
  hold it; sample multi-decade and genuinely multi-market (49 countries, developed and emerging),
  which is the strongest sample row in this cluster; costs and multiple testing — **unknown, body
  not read**. Tier A on venue, breadth and independence. **The `validation_overlap` flag is `true`:
  a three-decade sample published in 2022 necessarily overlaps this repo's 2018–2023 validation
  split, so discount the novelty of anything built on it accordingly.**

**An index-behaviour note worth keeping.** Semantic Scholar's DOI endpoint returns **"not found"**
for this JFE DOI — no record at all, not a low count — while Crossref gives 103 and OpenAlex 109.
That is the second instance in two sessions (Grinblatt–Han, 2026-09-19) of the S2 DOI endpoint
simply lacking a JFE record. Per the session-7 rule, disbelieve the lone outlier; here the outlier
is an *absence*, and the two independent indices agree closely, so the count is reliable.

## Implementability here

**This note's practical output is a constraint, not a construction.** Taken with
`2026-09-20-salience-theory-stock-prices.md`:

1. **A stock-level, unconditional, long-only `ST` book on this universe is an anti-candidate.**
   The universe is ~145 large global names. The one independent multi-market replication says the
   effect is priced primarily among microcaps and does not exist outside them and extreme market
   states. Writing that candidate spends a trial — permanently raising the deflated-Sharpe bar for
   everything after it — to test a proposition a Tier-1 replication has already answered on a
   sample vastly larger than this one. **Do not spend a trial on it.** If the lab wants the
   number anyway, it can have most of it free: run the context ablation and the skip-month check
   from the second note as holdings-only computations first.
2. **What survives is the free diagnostic pair, and it survives precisely because it is free.**
   The context ablation (market-context `ST` versus context-free `ST`, which collapses to a
   magnitude ranking on `|r|`) and the open-to-open falsifier cost no trial, are the sources' own
   identifying tests, and make **ordered, pre-registerable** predictions. Both are worth running
   even though the book is an anti-candidate, because both measure something about *this universe*
   that generalises past salience: the ablation says how much of any day-weighting scheme's content
   is the volatility level, and the open-to-open test is a second, independent use of the session
   boundary the 2026-09-18 cluster opened.
3. **The ETF/region adaptation is the only version with a live claim to a trial, and it is a scout.**
   The microcap objection is about the population, not the measure. Applying `ST` across the
   42-ETF cross-section — states are the ETF's daily returns, `r̄_s` is the average across ETFs
   that day — moves the construction to a population where "microcap" is not a meaningful
   objection and where this repo's survivorship bias is weakest. **No source read tonight tests
   salience at the index or ETF level**, so this has a mechanism and no empirical support: scout
   track, and say so.
4. **Reconciling the two papers is itself worth one free measurement.** If the skip-month version
   of `ST` retains its rank-ordering here, Cosemans–Frehen's defence transfers; if it collapses,
   Cakici–Zaremba's first limitation transfers, and the vein closes on this universe for the same
   reason the reference-point vein closed on 2026-09-19. Either way the lab learns which of two
   Tier-1 papers describes its own data, which is worth more than the candidate was.

## Related

- `2026-09-20-salience-theory-stock-prices.md` — the measure, and the paper this one contradicts.
- `2026-09-20-salience-theory-choice-under-risk.md` — the theory primitive.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the standing prior on what happens to a
  single-market anomaly when an independent team takes it abroad. This cluster is a clean instance:
  sign replicates, scope collapses.
- `experiments/learnings.md`, 2026-09-19 — the reference-point vein closed on exactly this pattern
  (an attractive behavioural score whose tail excess was momentum plus the volatility level). The
  base rate on this universe is unkind to this whole class, and this note is the first in the
  cluster to say so before a trial rather than after one.
