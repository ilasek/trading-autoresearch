---
title: "Do Industries Lead Stock Markets?" (with the authors' replication Note and a published reexamination)
authors: Hong, Torous, Valkanov; Hong–Torous–Valkanov (Note); Tse
year: 2007
venue: Journal of Financial Economics (Tier 1); the Note is an author-posted replication package (unrefereed); Tse is Journal of Empirical Finance (Tier 1/2)
url: https://doi.org/10.1016/j.jfineco.2005.09.010
citations: 616 (Semantic Scholar, DOI:10.1016/j.jfineco.2005.09.010, checked 2026-08-30); Tse reexamination 20 (Semantic Scholar, DOI:10.1016/j.jempfin.2015.10.003, checked 2026-08-30)
sample_period: 1946–2002 (US); 1973–2002 (eight non-US markets); extended to 1946–2013 in both the authors' Note and Tse
markets: US, 34 (Tse: 48) industry portfolios; plus Japan, Canada, Australia, UK, Netherlands, Switzerland, France, Germany
tier: A for the primary result, with a recorded and unresolved tier-1-venue disagreement about whether it survives sample extension and data revision
validation_overlap: false
published_post_2018: false
---

Primary text read in full: the authors' 5 December 2005 draft, author-hosted at
`columbia.edu/~hh2679/industry-12-05-05.pdf`. The authors' October 2014 replication Note
(`rady.ucsd.edu/_files/faculty-research/valkanov/Note_10282014.pdf`) read in full. Tse's
reexamination recorded **from its published abstract only** — closed access, no repository
copy found.

This is the first note in this folder on `lead-lag-spillover`.

## Mechanism

The claim is *gradual information diffusion across asset markets*, built on Merton (1987)
and Hong–Stein (1999). Information that originates in one asset market reaches investors in
another market only with a lag, because attention and information-processing capacity are
scarce and most investors specialise. An investor who trades the broad index does not watch
the metals or real-estate complex, so news that first shows up in those prices is
incorporated into the index late.

The paper states the mechanism as a two-market model and derives two properties worth
carrying over, because they are what makes the family *identifiable* rather than just
another autocorrelation:

1. **Own-serial correlation can be zero while cross-serial correlation is non-zero.** Each
   market's investors condition efficiently on their *own* information, so the price is
   efficient with respect to it. What they cannot process is the *other* market's
   information. The signature of gradual diffusion is therefore predictability *across*
   assets that is not a restatement of predictability *within* an asset. A construction that
   does not control for own-lag predictability has not tested the mechanism.
2. **The sign of the cross-prediction follows the covariance of the two assets' payoffs**,
   so it is not required to be positive. Some leading groups forecast the follower
   negatively. The paper's own estimates include leading industries with negative
   coefficients (metals, petroleum) alongside positive ones (real estate, retail,
   financials). **A long-only construction that assumes "leader up ⇒ follower up" is
   assuming a sign the theory does not supply.**

Two auxiliary predictions matter for whether an observed lead-lag is the mechanism or noise:

- Predictability should survive controls for time-varying risk and liquidity proxies. The
  paper controls with lagged own market return, inflation, default spread, dividend yield
  and lagged market volatility.
- **An asset should lead the market only if it carries information about market
  fundamentals.** This is the paper's identifying restriction, and its central test: it
  regresses each industry's ability to predict the market against the same industry's
  ability to predict indicators of real economic activity (industrial production growth) and
  finds the two propensities positively related. This is the closest thing the family has to
  a pre-registrable screen, and it is a *cross-sectional* restriction across leaders rather
  than a claim about any one leader.

Note that the mechanism also allows the arbitrage-limits version: even with arbitrageurs
trading both markets, some cross-predictability survives in equilibrium as long as arbitrage
is limited. That is the standard reason the effect is not expected to be fully competed away
— and equally the standard reason it is expected to be *small* and cost-sensitive.

## Construction recipe

The paper's own construction is a **timing** construction, not a cross-sectional one:

- Monthly frequency. For each candidate leading group *i*, run a predictive regression of
  the aggregate market's excess return in month *t* on the group's return in month *t−1*
  plus a control vector (lagged market return, inflation, default spread, dividend yield,
  market volatility). Newey–West standard errors with 3 monthly lags; the industry
  regressions are stacked into a GMM system so cross-industry residual correlation enters
  the joint Wald test.
- **Horizon.** Statistical significance is concentrated at one month ahead, weakens
  substantially at two, and is essentially gone at longer horizons. The authors read the
  decay as information being fully absorbed in about two months, and treat the *absence* of
  long-horizon predictability as evidence that the short-horizon result is not a mechanical
  regression artifact. Useful as a specification check: a lead-lag signal that predicts
  equally well at 1 and 6 months is more likely a slow-moving risk proxy than a diffusion
  effect.
- **Multiple testing is handled explicitly and by simulation**, not by a rule of thumb. With
  34 regressions one expects ≈3.4 significant coefficients at the 10% level under the null.
  The authors simulate the joint distribution and report the fraction of simulations in
  which as many leaders appear by chance; the count they observe is far into the tail. The
  Note restates the same arithmetic. **Take the counting discipline itself as the recipe:
  the object being tested is "how many groups lead", scored against its null, not "does this
  particular group lead".**
- **Trading it.** The market-timing exercise is a rolling (expanding-window) regression: fit
  on an initial decade, forecast one month ahead, re-estimate each month, and hold the
  market when the forecast exceeds the risk-free rate, otherwise hold the risk-free asset.
  This is a binary in/out allocator, not a cross-sectional weighting.
- **Cost caveat supplied by the authors themselves.** They report the timing rule improves
  risk-adjusted return *before* costs, and immediately caution against reading it as a
  profitable strategy: adding industry information roughly doubles the number of switches
  between the risky and risk-free asset relative to using the macro predictors alone. They
  do not model costs.

The international leg uses the same specification on each of eight non-US markets, with a
reduced control set (no dividend yield or default spread available), and reports (a) the
*count* of leading industries per country against the chance threshold, (b) the joint F-test
per country, and (c) the leader-versus-fundamentals relation per country. The count and
joint tests come out similarly to the US in all eight; the leader-versus-fundamentals
relation holds in seven of eight (the exception is Japan, and it weakens toward zero once
industries with fewer than four years of data or fewer than five firms are dropped).

## Robustness evidence (qualitative only)

**In favour.**
- Multi-market: the pattern replicates in eight developed markets outside the US on an
  independent data vendor, which is the paper's own defence against data mining.
- Robust to outlier handling: dropping thin industry portfolios and winsorising returns
  leaves the fundamentals-relation intact or slightly stronger.
- Explicit chance-baseline simulation rather than a per-test t-statistic.
- The authors later posted data, code and output, had the main table independently
  replicated by two other researchers, and re-ran it on a sample extended by roughly a
  decade. On the extension they report predictability persists, but for **a smaller subset**
  of the original leaders, with rolling regressions showing a stable core plus a set of
  industries that lead only in some subsamples. That is a *decay-and-instability* finding
  reported by the authors themselves, not a clean confirmation.

**Against.**
- Tse's published reexamination extends the sample by the same decade, uses a finer industry
  partition (48 rather than 34), and reports that only a small number of industries retain
  significant predictive ability — and that even on the *original* sample and industry
  count the results are weaker after data revisions. He also reports evidence of the
  reverse direction (market predicting industries) and that the market predicts economic
  growth better than the industries do, and reads the whole as consistent with market
  efficiency.
- The two accounts are **not adjudicated here.** They differ in industry partition, data
  vintage and specification, and this folder has no basis to prefer one. Record it as: the
  qualitative mechanism has multi-market support; the specific claim "N industries lead the
  market" has a documented sensitivity to data vintage and partition choice large enough
  that a count is not a stable quantity.
- Related but distinct: Hou (2007, RFS, "Industry Information Diffusion and the Lead-lag
  Effect in Stock Returns", **unread here** — closed access, SSRN behind a bot challenge;
  575 citations, Semantic Scholar DOI:10.2139/SSRN.463005, checked 2026-08-30) argues from
  its published abstract that the big-firm-leads-small-firm effect is predominantly
  *intra*-industry, and that little cross-industry predictability survives once the
  intra-industry channel is accounted for. If that is right, the grouping variable matters
  more than the lead-lag machinery does. Flagged as a follow-up, not used as evidence.

## Implementability here

**What fits.** The universe is ~145 instruments across 15 regions with 42 ETFs. Regions and
ETF sleeves are exactly the kind of "asset market with its own specialist investor base"
the mechanism is about, and the repo's breadth is a genuine advantage here rather than the
survivorship liability it is elsewhere — the ETF sleeve in particular is not
survivorship-conditioned on stock-picking.

**What does not fit, stated plainly.**

1. **The engine's one-day execution lag is not the binding problem; the monthly horizon
   is.** This paper's effect lives at a one-month horizon, so a one-day lag costs little of
   it. The binding problem is the opposite one: at monthly frequency the effect is small
   relative to what a 15 bps/side book can pay for.
2. **The paper's construction is a timing rule, and this book is long-only with a
   ~1.0 gross cap.** The in/out allocator maps here to "hold the market sleeve or hold
   nothing", i.e. a cash position. That is expressible but it is a different animal from the
   incumbent's cross-sectional sort, and the authors' own switching-count caveat is the
   thing to price first.
3. **The fundamentals screen is unavailable.** The identifying test — does a group's ability
   to predict the market track its ability to predict industrial production — needs a
   macro series this repo does not have and is not permitted to fetch. Without it, a
   lead-lag candidate here is running the paper's *symptom* test without its *identification*
   test. Say so in the hypothesis rather than implying the mechanism is established.
4. **The sign is not free.** See Mechanism (2). A cross-sectional construction of the form
   "buy the laggards of groups whose leaders rose" imposes a positive sign on every group.
   The theory does not, and the paper's estimates include both signs.

**Concrete adaptations, in order of how much of the paper's discipline they keep.**

- *Cross-sectional, region-level, sign-estimated.* For each region (or ETF sleeve), estimate
  on the train split whether its lagged monthly return predicts other regions' next-month
  returns, keeping the sign as estimated rather than assumed, with own-lag return as a
  control so the signal is a genuine cross-effect and not a repackaged own-momentum. Then
  form long-only monthly weights from the predicted cross-sectional ranking. The own-lag
  control is the single most important carry-over: without it, `price-trend` will show up
  wearing a lead-lag costume, and this lab already has a measured example of a
  differently-motivated family arriving at rho ≈ 0.75 to a momentum champion.
- *Count-based pre-registration.* Before trading anything, run the paper's own test: how
  many of the candidate leader→follower pairs are significant, against the chance count for
  the number of pairs tested. This is a free train-split screen and it is exactly the shape
  of screen `learnings.md` says to treat as an answer rather than a hurdle to argue past.
- *Horizon-decay check, also free.* Require the effect to be visible at one month and
  materially weaker at three-plus. A lead-lag signal that is flat across horizons is a
  slow-moving risk proxy.

**Known pitfalls.** (a) The number of testable ordered pairs grows as the square of the
number of groups — with 15 regions there are 210 ordered pairs, so a per-pair t-statistic is
meaningless and the count-against-chance framing is mandatory, not optional. (b) Non-US
instruments here are USD-converted and unhedged, so a "region leads region" result can be an
FX result; the paper's markets are studied in local terms. (c) The lab's existing
`lead-lag-spillover` scout compared holding the laggard *half* of leading groups against
holding all of it and found the ranking flipped between gross and net — a turnover artifact,
per `learnings.md`'s standing warning that outside `price-trend` turnover differences
dominate mechanism comparisons. Any follow-up should hold turnover fixed by design.

## Related

- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — the same family at the
  daily/weekly horizon, with an implementable sorting variable (turnover) and a per-instrument
  `DELAY` statistic. Read together: this note supplies the mechanism and the multiple-testing
  discipline; that one supplies the construction.
- `notes/2026-08-17-cross-sectional-vs-time-series-construction.md` — the timing-versus-
  cross-section distinction that decides which of the two shapes above a candidate is in.
- `notes/2026-08-28-local-versus-global-factor-construction.md` and
  `notes/2026-08-28-international-momentum-country-neutral.md` — the folder's existing
  region-level material; the regional grouping this note wants is the one those two graded.
- `notes/2026-08-24-multiple-testing-haircut.md` — the counting discipline above is the
  same object the lab's deflator implements, applied inside a single trial.
- `experiments/learnings.md` — the recorded `lead-lag-spillover` scout, and the standing
  finding that mechanism diversity does not buy return decorrelation on a long-only book.
