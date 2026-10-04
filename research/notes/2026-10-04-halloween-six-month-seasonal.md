---
title: "The Halloween Indicator, 'Sell in May and Go Away' — the original puzzle and its 108-market, three-century replication"
authors: Bouman, Jacobsen (anchor, NOT read); Jacobsen, Zhang (replication, read in full)
year: 2002; 2021 (working-paper version 2012)
venue: American Economic Review 92(5), 1618–1635 (Tier 1, peer-reviewed); Journal of International Money and Finance 110, 102268 (Tier 1/2, peer-reviewed)
url: https://doi.org/10.1257/000282802762024683 ; https://doi.org/10.1016/j.jimonfin.2020.102268
citations: "Bouman–Jacobsen: 295 (Crossref `is-referenced-by-count`, checked 2026-10-04); 430 (OpenAlex, checked 2026-10-04); Semantic Scholar returns a clean `Paper with id DOI:… not found` for this real, twice-indexed DOI — the **fifth** instance of the failure mode first recorded [2026-10-01] (checked 2026-10-04). Zhang–Jacobsen: 25 (Crossref) / 33 (OpenAlex), checked 2026-10-04."
sample_period: "Bouman–Jacobsen: January 1970 – August 1998 (restated by the replication, not verified at first hand). Jacobsen–Zhang: 1693–2011, 55,425 monthly country-index observations."
markets: "Bouman–Jacobsen: 37 countries. Jacobsen–Zhang: 108 countries — 24 developed, 21 emerging, 31 frontier and 32 unclassified, across 16 African, 20 Asian, 12 Middle Eastern, 39 European, 3 North American, 16 Central/South American and 2 Oceanian markets."
tier: "A for the cluster. The anchor is a top-5 journal article with ~300–430 citations but was **NOT read** (see Access); everything attributed to it below is restated from the replication, which shares an author with it, and is flagged at each use. The replication was read in full in its working-paper form and is the note's actual evidentiary basis: 108 markets, multi-century, and explicitly built to answer the methodological objections raised against the anchor."
validation_overlap: false
published_post_2018: true
---

## Access

**Jacobsen–Zhang was read in full; Bouman–Jacobsen was not, and the routes are recorded so the next
session does not repeat them.** The AER article is closed: Unpaywall reports `is_oa: false`, and
OpenAlex's `oa_status: green` resolves to **SSRN 76248, which returned HTTP 403 with an 896 KB
Cloudflare body** — a fresh instance of the [2026-10-01]/[2026-10-02] lesson that a `GREEN` flag is
no promise of reachability, and the opposite of the [2026-10-03] mirror case. The Erasmus Pure record
(`pure.eur.nl`) **served the publisher metadata and a truncated one-line abstract at HTTP 200**, and
named a RePub handle (`hdl.handle.net/1765/53883`) which resolved to `repub.eur.nl/pub/53883` — a
200 landing page carrying **no bitstream link at all**. So: an institutional repository can hold a
*record* without holding a *file*, and the handle in a Pure record is not evidence of full text.

**The replication was reached through a third-party mirror and the identity was verified before use.**
`bnains.org` served a 3.4 MB, 55-page PDF with a live text layer; its title page, author affiliations
(both Massey University), abstract and the SSRN stamp (`abstract=2154873`) match the RePEc/Crossref
record for the working-paper version of the JIMF article. Recorded as a channel with the obvious
caveat: a third-party mirror has no provenance guarantee, so the file was checked against the
indexed metadata rather than trusted. **The published JIMF version is closed** (`oa_status: closed`,
no repository copy on any index), so the version read is the pre-publication one and section numbers
below refer to it.

**Two access reversals worth more than this note.** (1) **`econstor.eu` is now behind Anubis** —
`econstor.eu/bitstream/10419/100871/1/wp2002-13.pdf` returned HTTP 200 with a 7.9 KB
`Making sure you're not a bot!` body from `within.website/x/xess`. `research/README.md` still
describes econstor as "a reliable channel and worth trying early" (added 2026-09-07); **that is no
longer true tonight**, and it is the third Anubis host after Frankfurt [2026-09-30] and AUEB
[2026-10-03]. (2) **`utoronto.scholaris.ca` is a new and strong channel** — it served the typeset
published PDF of a closed AER article on the first try (see
`2026-10-04-sad-daylight-seasonal-mechanism.md`), which is the [2026-10-03] "author's institutional
library" lesson landing a second time at a different university.

## Mechanism

There is no agreed mechanism, and the replication says so in as many words: *"we still lack a proper
explanation on what causes the effect."* That is the honest headline and it should be carried into
any hypothesis — this is the rare case in this folder where a large, widely-replicated regularity has
**no economic story this folder can grade**. The candidate stories in the literature, as the
replication frames them:

- **Seasonal variation in risk aversion.** Something makes the marginal holder less willing to bear
  equity risk over one half of the calendar year and more willing over the other, so the required
  return differs between the halves. Daylight-driven mood (SAD) is the best-developed version of
  this; it has its own note, `2026-10-04-sad-daylight-seasonal-mechanism.md`, and it is contested
  there.
- **Seasonal variation in the composition or attention of the marginal trader** — vacation timing
  concentrated in the Northern summer, with the summer's thinner participation lowering the
  willingness to take risk rather than raising it.
- **Nothing: a multiple-testing artifact.** A six-month window is one of a modest number of
  partitions of the calendar, so the search space is small, but it is not one — which is exactly
  what the replication was built to settle by expanding the cross-section and the sample rather than
  by arguing about the original one.

What is worth noting structurally is what the effect is *not*. It is **not a dispersion effect**: the
replication reports the two six-month windows have very similar return standard deviations, with
November–April's "if anything" the lower of the two. A seasonal in the mean with no matching seasonal
in the variance is the same signature this folder has now catalogued four times for a *bias*
([2026-10-02], [2026-10-03]) — which is a reason for suspicion, not a finding, and the suspicion is
addressed below under Robustness rather than waved away.

## Construction recipe

The whole construction is one dummy and the sources do not dress it up:

**Signal.** `H_t = 1` if the month falls in **November through April**, `0` otherwise. Nothing is
estimated, nothing is fit, and the window is the same calendar window in every market — including
Southern-Hemisphere markets. That last point is a *construction fact about these papers*, not an
oversight, and it is the hinge of the companion note.

**Test.** `r_t = μ + α·H_t + ε_t` on continuously compounded monthly index returns, with Newey–West
standard errors; `α` is the difference between the two six-month windows' mean returns. The
replication's robustness battery re-runs this (i) at **semi-annual** frequency, where the dummy is
negatively autocorrelated by construction and the Powell-et-al. persistent-regressor objection
therefore cuts the *conservative* way, (ii) under **GARCH(1,1)** for volatility clustering, and
(iii) under **Huber M-estimation** for outliers — all on 100-year rolling windows of the three-century
UK series.

**Trading form, as the sources state it.** A two-state switch: hold the index November–April, hold
the short-term risk-free asset (3-month Treasury bills, local currency) May–October. **Two boundary
crossings per year.** On costs the cluster is split and the split should be stated plainly: the
anchor is restated by the replication as reporting outperformance *"even after taking transaction
costs into account"* — a claim this folder has **not** verified at first hand, since the anchor was
not read — while the replication's own out-of-sample table reports gross returns and the phrase
"transaction cost" appears exactly once in its text, inside that restatement. So the cluster's cost
treatment is an assertion inherited from an unread source, and re-pricing it against this lab's
15 bps/side is the single most important thing to do before believing any of it.

**Effect size, deliberately limited.** On the pooled 108-market panel the unconditional six-month
mean is **6.93%** in November–April against **2.41%** in May–October, i.e. a **~4.5 pp/yr**
difference; the cross-sectional count is **81 of 108 countries positive, significant in 35, against
2 significant in the opposite direction**. Per this folder's anti-lookahead policy the sources'
*strategy-level* performance claims (outperformance frequencies at stated holding horizons,
subperiod magnitudes) are **omitted on purpose** — the undated full-panel mean difference is recorded
because the cost arithmetic below cannot be done without an effect size, and nothing else is.

## Robustness evidence (qualitative only)

**The cross-sectional breadth is the strongest part and it is unusual.** 81 of 108 markets share the
sign; restricted to markets with over ninety years of data — Lakonishok and Smidt's own standard for
believing a monthly seasonal — the effect is significantly present in 14 of 17 countries plus the
world index, with two insignificantly positive and one insignificantly negative. A regularity that
survives that restriction is not a thin-sample artifact.

**It is weaker outside developed and emerging markets.** The replication reports the effect stronger
in developed and emerging than in frontier and unclassified markets, and more prevalent in Europe,
North America and Asia than elsewhere; it reports the effect **absent** in Israel, India and the
Central/South American markets. For this lab that is a *universe-composition* caveat: the regions
where it is reported absent are regions this universe holds.

**No post-publication decay is reported — the opposite.** The replication's rolling-window estimates
on the three-century UK series are positive at **every** window under OLS and under GARCH, and the
authors' own summary is that the effect has strengthened rather than weakened over the modern portion
of their sample, with the explicit demand that *"plausible explanations of the Halloween effect should
be able to allow for time variation in the effect"*. This is the McLean–Pontiff pattern **failing to
appear**, which is a mark in the effect's favour and simultaneously the thing that makes it suspect:
an anomaly that grows after publication is either structural or mismeasured.

**Three stated caveats that are real.** (i) Under Huber M-estimation the UK rolling point estimates
**do turn negative** in part of the twentieth century, while OLS and GARCH do not — so the effect's
persistence is partly carried by influential observations, which is precisely the sensitivity
`2026-09-11-influential-observations-winsorization-versus-robust-regression.md` was written about, and
it is the one place the replication's own battery disagrees with itself. (ii) The indices are **price
indices without dividends**; the authors argue dividends are not seasonally clustered and cite
Gultekin–Gultekin, but it is an argument, not a measurement, and the sign of the bias is unknown.
(iii) Sample sizes are wildly unequal across the 108 markets (10 countries with under ten years), so
the cross-sectional count is a count over heterogeneous precision — which is the
`2026-10-02`/`2026-10-03` lesson about pool weighting applied to a *count of significances* rather
than to a mean.

## Implementability here

**The lab has already measured this effect on this universe, and already closed the obvious form of
it. Read that first.** `experiments/learnings.md` [Measured 2026-09-01] records **Nov–Apr at
+6.18 bps/day (t = +3.58)** on this panel — the sources' regularity, present and significant here —
and then closes it structurally: with `max_leverage = 1.0` a long-only book cannot *overweight*
in-window, so the only available form is hold-in-window / cash-out, and the May–October complement
**still earns +11% to +14%/yr** on this universe, so sitting it out forgoes more than it saves. The
[Measured 2026-09-02] entry closed the `calendar` half a second time on cost, with the general rule
that **a monthly calendar overlay here must find a window losing more than ~3.6%/yr**. Nothing in
these sources overturns either closure, and this note does not propose that it does. The sources'
own ~4.5 pp/yr difference is a *difference between two positive windows*, which is exactly the
configuration the lab's sign condition rules out.

**What the closures do not cover, and it is one specific construction.** Both closures are about an
overlay that **exits to cash**, and both derive their cost from monthly boundary crossings. A
**rotation between instruments** is neither: it holds gross 1.0 at all times, so the no-leverage
constraint never binds, and it crosses the window boundary **twice a year**, so at 15 bps/side it
pays roughly **2 × 2 × 15 bps ≈ 0.6%/yr** of turnover cost against the lab's measured 3.6%/yr for a
monthly overlay — six times cheaper, and the first calendar construction this folder has described
whose cost is plausibly below its effect. The rotation needs somewhere to rotate *to*, and the only
candidate the literature supplies is the hemisphere flip predicted by the SAD mechanism. **That
prediction is contested, the contest is the subject of the companion note, and it is resolvable here
for free.** Do not build the rotation before running that free screen.

**Three pitfalls specific to this universe.**

1. **The universe is global and the window is not.** A Nov–Apr dummy applied to a 15-region,
   140-instrument panel is a *single global calendar bet*, not a cross-sectional one, so it has no
   breadth in the Fundamental-Law sense (`2026-08-19-fundamental-law-breadth-and-strategy-risk.md`):
   two independent bets per year. Treat any Sharpe it produces as having correspondingly enormous
   standard error, and expect the deflated-Sharpe bar to be the binding constraint rather than the
   gates.
2. **The regions where the sources report the effect absent are in this universe.** If a rotation or
   a tilt is built, the sources' own cross-section says to expect nothing from the Central/South
   American and Indian legs — which makes a *pre-registered* regional split a falsifier rather than a
   fishing expedition.
3. **Price-index evidence, total-return implementation.** The sources measure on dividend-excluding
   price indices; this lab's panel is dividend-adjusted. The seasonal distribution of dividends on
   *this* panel is measurable for free and is the honest precondition for importing the effect size.

## Related

- `2026-10-04-sad-daylight-seasonal-mechanism.md` — the one developed mechanism for this effect, its
  refutation, and the free screen that decides whether the rotation above is worth a scout trial.
- `2026-08-29-same-calendar-month-seasonality.md`, `2026-09-02-return-seasonalities-common-factors.md`
  — the *cross-sectional* seasonality literature, which is a different object: those rank instruments
  against each other on own-history, this ranks two halves of the calendar against each other for
  every instrument at once. The lab's seasonal leg comes from the former and is alive; the latter is
  what is closed.
- `2026-09-02-turn-of-month-payment-cycle.md` — the other calendar window the lab priced and refused;
  the boundary-crossing cost rule was measured there.
- `2026-08-17-mclean-pontiff-publication-decay.md` — the decay pattern this effect is reported to
  violate.
- `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the robust-vs-OLS
  disagreement in the replication's own rolling windows is an instance of it.
- `experiments/learnings.md`, [Measured 2026-09-01] and [Measured 2026-09-02] — the two closures this
  note is in explicit tension with, and does not claim to overturn.
