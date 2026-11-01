---
title: "Anomalies across the globe: Once public, no longer existent?"
authors: Jacobs, Müller
year: 2020
venue: Journal of Financial Economics 135(1), 213–230 (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2019.06.004 · full text read from the authors' own January 2017 working draft at https://wp.lancs.ac.uk/fofi2018/files/2018/03/FoFI-2018-0174-Sebastian-M%C3%BCller2.pdf
citations: 221 (Crossref `is-referenced-by-count`, checked 2026-11-01). Semantic Scholar's DOI endpoint returns `Paper with id DOI:10.1016/j.jfineco.2019.06.004 not found` (checked 2026-11-01) — the clean-`not found` failure mode again, not an indexing fact.
sample_period: 1980-01 to 2015-12 (baseline), with each anomaly's own published in-sample window used to define its pre-publication period; more than two million anomaly-country-months
markets: 39 stock markets (US from CRSP/Compustat; all others from Datastream/Worldscope; IBES for all), 231 cross-sectional anomalies from 153 papers in the version read — 241 in the published version
tier: A — Tier-1 venue, three-figure citations, the largest multi-market anomaly panel of its kind, a uniform construction applied to every anomaly and every country, explicit about its own subjectivity in anomaly/date selection, and it tests its own preferred explanation and reports that the obvious version of it fails.
validation_overlap: false (sample ends 2015-12, before this lab's 2018–2023 validation window)
published_post_2018: true (JFE 2020; the version read is the authors' January 2017 draft)
---

## Access

**Read in full** from a **conference-programme site**: `wp.lancs.ac.uk/fofi2018/files/2018/03/`,
the Frontiers of Finance 2018 paper repository at Lancaster, served the authors' complete January
2017 draft on the first try (192 KB; `pdftotext -layout` → 145 KB of clean text, 525 instances of
`" the "`, zero `( )` dropout, no ASCII shift). This is the fourth confirmed instance of this
file's conference-mirror lesson (after `top1000funds.com` 2026-08-21, the EFMA programme
2026-10-31 and `aeaweb.org/conference` 2026-10-16) and the second Lancaster host after
`eprints.lancs.ac.uk`.

**Where the draft and the published version differ, stated rather than assumed.** The draft
implements **231** anomalies across 39 markets; the published version implements **241** across
the same 39 markets. The authors' own February 2020 workshop deck — fetched and *not used as a
source*, see Access notes in `SUMMARY.md` — states the published count as 241 and the published
headline in the identical words as the draft abstract. **The central claim is unchanged between
the two**: of the 39 markets, only the US shows a reliable post-publication decline in long-short
returns. Every quantitative detail recorded below is from the draft; nothing is attributed to the
published version that the draft does not say.

Two channels for the published version are **named and not obtained**:
`unicreditgroup.eu/content/dam/.../wp-135-Jacobs-e-Mueller.pdf` returned **HTTP 403 with a 13.8 KB
HTML body**, and the two **mediaTUM** records OpenAlex lists as green locations
(`mediatum.ub.tum.de/1534292`, `/node?id=1522738`) are **records with no file** — a 45 KB
JavaScript shell with no `.pdf` href, and the conventional `doc/<id>/<id>.pdf` and
`download/<id>` paths return 404 and 400. That is the Pure/DSpace "a `locations[]` entry is
evidence of a record, not of a file" caution (2026-10-04, 2026-10-16) on a third platform.

## Mechanism

Two mechanisms, and the second is the one this repo needs.

**Mechanism 1 — publication-driven decay is a *market-level* property, not a property of the
effect.** The motivating result in the literature is that US anomaly long-short returns fall after
the paper announcing them is published, read as arbitrageurs learning about mispricing from
academic work. Applied uniformly to 39 markets, the decline is **reliable in the US and in none of
the other 38**, while *unconditional* long-short predictability is broadly similar across most
developed markets. So the same effect, measured the same way, decays in one market and not in the
others — which means the decay is caused by something attached to the **market** (who is reading,
with how much capital, under what frictions), not by something attached to the **mechanism**.

The authors test the obvious frictions explanation and **report that it fails**, which is the most
useful thing in the paper. Five standard firm-level limits-to-arbitrage proxies — size, turnover,
the fraction of zero-return days, the Corwin–Schultz high-low spread estimate, and idiosyncratic
volatility (the first four proxying transaction costs, the last proxying the arbitrageur's holding
cost) — are **roughly comparable** between US anomaly portfolios and pooled other-developed-market
ones. There is some evidence of lower transaction costs in the US; holding costs are comparable or
slightly *higher* there. Standard arbitrage costs therefore explain at best a fraction of the
difference. A market-integration test fails too: post-publication comovement between US and
other-developed anomaly legs does rise, but the **neutral middle-quintile control portfolios rise
by the same amount**, so the increase is globalisation and currency, not coordinated arbitrage.
What is left is the harder-to-measure set — shorting costs, investment mandates, benchmarking,
currency risk, information costs, where the quantitative-arbitrage capital actually sits — plus one
friction that is directly structural and is this note's second mechanism.

**Mechanism 2 — the thin-cross-section friction, which is a statement about this repo's own
panel.** The authors name, as a distinct impediment, "the relatively low number of stocks in many
non-U.S. markets": an arbitrageur applying filter rules, or aiming at style- or sector-neutral
construction, faces a cross-section that may simply be too small, and the resulting lack of
diversification shows up as **more crash risk** — they document a materially fatter left tail in
the pooled non-US developed anomaly-month distribution than in the US one. The chain is: **fewer
names → binding filters and failed neutrality → less diversification → fatter left tail → an
agency problem for whoever is carrying it**. That is a mechanism, not a measurement artefact, and
it is the first source in this folder that states it as the reason a non-US cross-sectional book is
harder than a US one of the same design.

Their own screen is the evidence for how binding it is: requiring a $10M lagged market
capitalisation and 25 eligible firms per country-month already means "smaller developed markets
(Austria, Belgium, etc.) typically have too few eligible firms to implement a sufficiently broad
anomaly universe with a sufficiently long time series", and raising the capitalisation hurdle
further "substantially decreases the number of implementable anomalies even in the largest
developed markets".

## Construction recipe

This is the paper's most directly transferable content: **the literature's own convention for
running one cross-sectional signal across many countries.**

1. **Country-neutral portfolios, formed separately per country.** For each
   (country, month, anomaly) triple, sort that country's eligible names and go long the most
   favourable quintile and short the least favourable quintile *within the country*. Aggregate
   across countries afterwards. **Never pool countries into one global sort.** The stated reason is
   that a pooled sort confounds the signal with cross-country differences in level; the operational
   reason is that it also confounds it with currency.
2. **A minimum breadth condition per country-month, enforced as a hard filter.** At least 25
   eligible firms in that country that month, or the country-month is dropped for that anomaly
   (with narrow exceptions for firm-event signals that cannot be quintile-sorted). This is the
   discipline that keeps a quintile from being two names.
3. **A capitalisation floor applied before sorting**, set low ($10M lagged market equity) and
   justified as removing only "the smallest and most illiquid stocks" rather than as a liquidity
   screen.
4. **Local currency, dividend- and corporate-action-adjusted returns.** Currency conversion is
   deliberately *not* applied, so the measured effect is not contaminated by FX.
5. **Conservative, uniform accounting timing**: annually updated values on the
   Fama–French (1993) convention, chosen explicitly to avoid look-ahead and to be comparable
   across countries, rather than per-anomaly timing matched to each original paper.
6. **One method for every anomaly.** The authors deliberately do *not* reproduce each original
   paper's weighting, universe or statistic — they impose a common framework and say why: a real
   quantitative arbitrageur "may be more likely to consistently apply his own data screens and
   investment guidelines rather than to exactly follow the many different approaches described in
   the respective academic papers". This is the opposite choice from a reproduction study and the
   note above records that both choices are legitimate for *different* questions.
7. **Both equal- and value-weighted versions are reported**, with the rationale separated: value
   weighting estimates how economically important an effect is, equal weighting estimates how
   *widespread* it is. Conclusions below hold for both.
8. **Binary signals (about 15% of theirs) get an event-versus-non-event construction**, long (or
   short) the event firms offset by the portfolio of non-event firms, instead of a quantile sort.
9. **The neutral-quintile control.** To ask whether some property of the long or short leg changed
   over time, compute the same property for the **middle (third) quintile** — stocks the signal
   calls neither cheap nor expensive — and difference against it. The middle quintile absorbs
   currency moves, general time trends and rising global correlation, so what survives the
   difference is attributable to the signal. The authors use it to kill their own
   market-integration hypothesis.

## Robustness evidence (qualitative only)

Multi-market by construction (39 markets, two million anomaly-country-months) and multi-decade on
the baseline window. The authors apply the standard Datastream international-data hygiene from the
established references — non-missing identifier/return/market-cap, home-country trading, generic
industry and firm-name screens to exclude non-common equity, delisting identification via two
independent routes, return screens, and 0.1%/99.9% winsorisation of returns and market cap — which
matters because the credibility of any international anomaly result rests almost entirely on that
cleaning. Unconditional long-short predictability is reported as similar across most developed
markets, and the US/non-US difference survives their checks on general time effects, local risk
exposures and database issues.

They are explicit about residual subjectivity in three places (which anomalies are selected, which
sample period counts as "in-sample" when authors extend samples during revision, which date counts
as publication) and about the scale of the task — the average anomaly has far fewer in-sample
observations in the average developed market than in the US, so the non-US tests are intrinsically
noisier, which cuts *against* reading their non-US non-decay as a tight zero.

The honest weakness: the paper's preferred explanation — arbitrage capital concentrated in the US —
is the one it cannot measure, and it says so, calling for exactly that measurement as future work.
Both of its own tests of that explanation (standard arbitrage-cost proxies; market integration)
come back negative. So the *finding* is strong and the *mechanism* is inferred by elimination.

Costs are not modelled; these are gross long-short quintile spreads.

Lookahead status: sample ends 2015-12, so `validation_overlap: false`. `published_post_2018: true`.
No dated performance figure appears above; the recorded content is a construction convention, a
structural statement about cross-section width, and a negative result about which frictions explain
a market-level difference.

## Implementability here

**Not a book — a construction standard and two priors.** The 231 anomalies are overwhelmingly
accounting-, analyst- or event-based and are out of reach. What transfers is heavier than usual:

1. **Country-neutral is the literature's default for a multi-country panel, and this repo's panel
   is a multi-country panel.** Nine large-cap national indices plus ETFs, under protocol v2's
   `eligible` frame, is structurally the object this paper studies. The convention — **sort within
   country, aggregate after** — is not a refinement; it is how the only large multi-market study of
   these signals is built, and the reason given is the same confound (cross-country level
   differences, plus currency) that a USD-converted global sort here would carry. The lab has
   already found this empirically from the other direction: its one v2 measurement win was a
   **region-relative** illiquidity construction, i.e. a country demean. **This source is the
   external argument that the region-relative form is the correct default and the pooled form is
   the special case needing justification — not the reverse.**
2. **A minimum-breadth filter per country-month belongs in any cross-sectional candidate here, and
   25 names is the literature's number.** This panel's per-country cross-section is a large-cap
   national index, so several of the nine markets will be at or near that floor in parts of the
   sample. A quintile or tercile of a 20-name country is two to four names; a country whose
   eligible count falls below the floor should be dropped for that month rather than sorted. The
   lab has repeatedly measured de-concentration prices and tail-depth confounds on constructions
   whose effective breadth was never audited; this is the free audit, and it is a *pre*-filter
   rather than a post-hoc diagnostic.
3. **The thin-cross-section friction predicts a fatter left tail for exactly this panel's non-US
   books, and that prediction is testable on train without a trial.** The chain (few names →
   binding filters → failed neutrality → poor diversification → fat left tail) says that a
   cross-sectional construction run per-country on nine large-cap indices should show more
   left-tail risk in its non-US country legs than in its US leg, at matched construction. If the
   lab is going to carry per-country legs at all, that is the number to look at before the Sharpe.
   And it reframes the lab's recurring "real, correctly signed and out of reach" finding: part of
   what is out of reach here may be **breadth**, not **cost**, and the two are separable by this
   measurement.
4. **The strongest *discount* in the paper, and it cuts the other way on novelty.** Post-publication
   decay — the McLean–Pontiff haircut this folder applies as a standing discount to every published
   mechanism — is documented reliably in **one** market. Eight of this panel's nine markets are not
   that market. So the standing novelty discount for a *published* mechanism should be applied
   **per market**, not globally: on non-US legs the literature's own evidence is that the published
   effect did not reliably decay. This is a rare case where this folder's default discount is
   *too harsh* for most of the lab's panel, and it should be recorded as such rather than quietly
   left at full strength. Two cautions on using it: the non-US tests are noisier by construction
   (far fewer in-sample country-months), so "no reliable decline" is weaker than "no decline"; and
   the mechanism the authors infer — arbitrage capital concentrated in one market — is the thing
   they could not measure.
5. **The neutral-quintile control is a free operator and it is the right instrument for a question
   the lab asks often.** Whenever the lab wants to know whether something about a sorted
   construction changed — its comovement, its volatility, its cost, its breadth — the complete
   control is the **same construction's middle quantile**, which shares the panel, the currency,
   the calendar and the formation dates and differs only in carrying no signal. It is strictly
   better than an unconditional panel average, and it costs nothing. This is the same family of
   device as this folder's partition-placebo rule for calendar claims (`learnings.md`,
   2026-10-31/11-01): **the complete control is the rest of the partition, not a chosen
   comparison.**
6. **One pitfall.** The paper's arbitrage-cost proxies include the Corwin–Schultz high-low spread
   and the zero-return-day fraction — both computable from this repo's panel — and finds them
   *comparable* across developed markets. Do not read that as licence to skip cost modelling: it
   is a statement that the proxies do not *differentiate* these markets, in a study that charges no
   costs at all. Protocol v3's statutory taxes differentiate them sharply, and the proxies are
   silent about stamp duty by construction.

## Related

- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the US study this paper extends to 39
  markets, and the source of the standing decay discount that finding (4) above says to apply
  per-market rather than globally.
- `notes/2026-11-01-reproduction-versus-replication-open-source.md` — the opposite methodological
  choice on purpose (reproduce each original's method, same sample) versus this paper's (one
  uniform method, new samples). Read together they are the clean statement of why the replication
  debate has two answers.
- `notes/2026-08-25-hierarchical-bayesian-factor-replication.md` — cites this paper for the
  international decay result, and its own global model reaches the compatible conclusion that
  international evidence is largely corroborating but not independent. Its 2026-11-01 addendum has
  the region and size-group breakouts.
- `notes/2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — the microcap/breakpoint
  argument, and the source of the structural fact (cross-sectional dispersion is largest in the
  smallest names) that makes finding (2)'s breadth floor bind here rather than being cosmetic.
- `notes/2026-10-05-chl-spread-estimator-close-high-low.md` and
  `notes/2026-09-04-high-low-spread-estimator.md` — the Corwin–Schultz estimator this paper uses as
  an arbitrage-cost proxy, already covered here with its own accuracy caveats.
- `notes/2026-09-04-global-liquidity-proxy-horserace.md` — the zero-return-day proxy, likewise.
- `experiments/learnings.md`: the 2026-09-03 `lv_illiq_region_relative` result (a country demean)
  is the lab's own version of finding (1); the repeated tail-depth confound entries are what
  finding (2)'s breadth floor is aimed at.
