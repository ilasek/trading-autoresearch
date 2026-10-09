---
title: "The Disappearing Index Effect — with the asymmetry debate: The Price Response to S&P 500 Index Additions and Deletions (Chen–Noronha–Singal) and its 2023 challenge (Kumar–Lawrence–Prakash–Rodríguez)"
authors: Greenwood & Sammon; Chen, Noronha & Singal; Kumar, Lawrence, Prakash & Rodríguez
year: 2022 (working paper, read); published Journal of Finance 2025. Chen et al. 2004; Kumar et al. 2023
venue: NBER Working Paper 30748, published as Journal of Finance 80(2), 657–698 (venue tier 1); Journal of Finance 59(4), 1901–1930 (tier 1); Journal of Banking & Finance 154, 106976 (tier 2)
url: https://doi.org/10.3386/w30748 (read in full) ; https://doi.org/10.1111/jofi.13410 (published version, not read) ; https://doi.org/10.1111/j.1540-6261.2004.00683.x (NOT read — closed, see below) ; https://doi.org/10.1016/j.jbankfin.2023.106976 (NOT read — closed)
citations: "Greenwood–Sammon: 40 for the published article (Crossref is-referenced-by-count, checked 2026-10-09; Semantic Scholar returns `not found` for 10.1111/jofi.13410, the folder's standing JF-DOI failure), 10 for the NBER working paper (Crossref, same date). Chen–Noronha–Singal: 488 (Crossref, checked 2026-10-09); 607 (OpenAlex, same date). Kumar et al.: 2 (Crossref, checked 2026-10-09)"
sample_period: "Greenwood–Sammon: S&P 500 additions and deletions 1980–2020 (index-fund tracking data 1990–2020). Chen–Noronha–Singal: S&P 500 changes 1962–2000 (per secondary descriptions; not verified against the paper). Kumar et al.: not verified"
markets: US equities — S&P 500 index changes, with explicit discussion of the Russell and of non-US national indices as an open question
tier: "A for Greenwood–Sammon (top-tier venue, full text read, forty-year sample, five competing explanations tested against each other rather than one confirmed). B for Chen–Noronha–Singal on venue and citation count, recorded **second-hand** — the paper was not read. C-equivalent weight for Kumar et al.: tier-2 venue, two citations, not read, recorded only as evidence that the asymmetry is contested"
validation_overlap: true
published_post_2018: true
---

> **Access note.** The **NBER working-paper version was read in full** and is the source of every
> claim attributed to Greenwood–Sammon below; the published *Journal of Finance* version was not
> read. **Chen–Noronha–Singal (2004) was not obtained**: OpenAlex reports it green-OA at a
> bepress repository (`stars.library.ucf.edu`), which `research/README.md` records as
> Cloudflare-challenged on every endpoint, and the two UCF records are faculty-bibliography
> entries rather than files. Its claims below come from Greenwood–Sammon's and Petajisto's
> citations of it plus the published abstract, and are flagged in-text. **Kumar et al. (2023)
> was not obtained** either — `oa_status: closed`, `any_repository_has_fulltext: false`, and the
> one repository record (Queen's University Belfast Pure) holds no file. It is recorded here as a
> *pointer to a live disagreement*, not as a source relied on.

## Mechanism

This is the paper that asks what happened to the 1986 effect, and its answer is not the one the
mechanism predicts. If price impact is (demand shock) ÷ (demand elasticity), and the demand shock
has grown steadily for four decades as passive assets grew, then price impact should have grown
too. **It did the opposite.** The abnormal return to being added to the S&P 500 rose early in the
sample and then fell steeply, ending the sample at a level statistically indistinguishable from
zero; deletions followed the same path with the opposite sign. *(Per this folder's anti-lookahead
rule the decade-by-decade figures are deliberately not recorded here; the shape — rise, then
decay to economically negligible by the end of the sample — is what transfers, and the sample's
late end overlaps this repo's validation window, hence `validation_overlap: true`.)*

Greenwood and Sammon test **five** explanations against each other. The discipline of the paper
is that it does not stop at the first one that works:

1. **Changing composition of additions and deletions.** Added and deleted firms have shrunk
   relative to total index capitalisation, and the size of the event firm is strongly related to
   the magnitude of the effect. A Fama–French-style regression reweighting on volatility, trading
   volume and relative size shows composition accounts for **some** of the decline but **cannot**
   account for all of it.
2. **The whole market got more liquid.** Value-weighted bid–ask spreads fell by roughly an order
   of magnitude over the sample and institutional implementation shortfall fell substantially.
   Real, but **not sufficient**, and — the decisive detail — **the timing is wrong**: the fall in
   trading costs *predates* the disappearance of the announcement effect.
3. **Migrations: the net demand shock is smaller than it looks.** This is one of their two
   headline answers. An increasing majority of S&P 500 additions are names simultaneously
   *leaving* the S&P MidCap index — so forced buying by large-cap trackers is matched, name for
   name and day for day, by forced selling from mid-cap trackers. Migrations went from a large
   minority of additions early in the sample to the great majority of them late, with the same
   trend among deletions. The returns split accordingly: migration and non-migration additions
   behaved alike when the mid-cap index had few trackers and diverged sharply once it had many,
   with migrations the weaker of the two. They speculate — explicitly as speculation — that the
   index committee may prefer migrations precisely because they minimise rebalancing impact.
4. **Index changes became more predictable, so arbitrageurs front-run them.** Evidence is
   **mixed**. A larger share of the total move now occurs *before* the announcement rather than
   after it, and a naive "largest eligible non-member" rule has become a better predictor of
   future additions. But the authors refuse to over-read it, for a reason that is the most
   important single sentence in the paper for this repo (see below): **the pre-announcement
   run-up is endogenous — non-member stocks that go up are more likely to be added in the first
   place** — so "additions are better anticipated" and "the provider has got better at adding
   recent winners" fit the same data.
5. **Event-specific liquidity provision.** Their other headline answer. Dedicated index-trading
   desks grew; trading volume became far more concentrated on the effective date itself; most
   large ETFs track indices that pre-announce rebalances and trade in the closing auction, which
   lets everyone else coordinate on supplying liquidity at a known time. The clinching
   observation: although index trackers now buy a substantial single-digit percentage of an added
   name, **total institutional ownership barely moves around index changes** — active
   institutions are selling to the passive buyers in roughly equal measure.

Their summary verdict: the decay is driven **primarily by migrations and by improved liquidity
provision**, with predictability not ruled out as a contributor. The framing they offer is
McLean–Pontiff's, generalised: *when a demand shock becomes regular, repeated and pre-announced,
a competitive market adapts to minimise its price impact.* The anomaly did not need a change in
the demand shock to disappear; it needed only to be well known.

**The asymmetry debate, recorded second-hand.** Chen–Noronha–Singal (2004) argued that the price
response is **asymmetric**: added firms show a permanent increase, deleted firms no permanent
decline. Their proposed mechanism is **investor awareness** in Merton's sense, which is
intrinsically one-way — investors learn of a stock when it joins a prominent index and do not
unlearn it when it leaves — and they report a Merton-style awareness proxy improving after
additions while barely moving after deletions. That asymmetry is **not settled**: Kumar et al.
(2023) claim to resolve it in the opposite direction, reporting a permanent response on *both*
sides once abnormal returns are computed differently, outliers are handled, and names *migrating*
between index tiers are separated from true entries and exits. Neither paper was read here. Note
how the 2023 challenge's stated fix — separate migrations from true additions — is the same
variable Greenwood and Sammon identify as the dominant driver of the decay; the two literatures
are converging on the same partition from different directions.

## Construction recipe

There is no strategy to implement, but there are four measurement constructs worth lifting:

**Partition index changes before measuring anything.** The useful partition is *true entry /
true exit* versus *migration between tiers of the same index family*. Two independent strands
now say the pooled average of the two is not a meaningful quantity. A membership panel that
records only "member / not member" of a single index cannot make this split and will pool them.

**Measure the pre-event leg separately, and distrust it.** Their Figure-8 construction is the
cumulative market-adjusted return from 100 trading days before announcement to 10 days after.
The total distance travelled over that window is roughly stable across the sample while the
*share of it occurring before the announcement* has risen. Two readings fit — better
anticipation, or a provider that increasingly picks recent winners — and the paper does not
pretend to separate them. For anyone using a membership panel as a universe, both readings have
the same consequence: **a name that has just become a member has just gone up a lot.**

**The post-event reversion test.** Cumulative market-adjusted return from one day before
announcement to 100 days after the change. Early in the sample this shows a clear peak within
about a week and a meaningful give-back over the following weeks, then a flat line; late in the
sample it shows a small peak and essentially no reversion at all. Note what that implies: *the
reversion the price-pressure hypothesis predicts has faded alongside the effect itself*, so the
1986 Harris–Gurel reading is not simply the "right" one that beat Shleifer's — it was a
description of a market structure, and the structure changed.

**The predictability yardstick.** Rank all non-member ordinary shares by market capitalisation
each month and look at where the names that are later added fall. Theirs is an imperfect proxy
(no float adjustment, no profitability or liquidity screens), and the answer is instructive:
added names sit at an average rank in the tens outside the index with an interquartile range
spanning tens of ranks, so size alone narrows the field a long way without coming close to
identifying the addition. "Predictable in distribution, not in name."

## Robustness evidence (qualitative only)

- **Forty years, one index, one country.** The sample length is a genuine strength and the single
  market is the genuine weakness. The authors say so and name the open question themselves:
  whether the same decay has happened in the Russell and MSCI families and in **nationally
  important indices such as the TOPIX and the Nikkei 225**. They cite related work finding the
  Russell 1000/2000 effects declining, and leave the non-US case open.
- **Five explanations tested against each other, with two rejected as insufficient on their own
  terms** (composition; general liquidity improvement — the latter on a timing argument rather
  than a magnitude one, which is the stronger form of rejection). Multiple-hypothesis discipline
  at the level of *mechanisms* is rarer than it should be and is why this is Tier A.
- **The decay finding is corroborated**: the authors credit prior work with first noting the
  decline in the inclusion effect on a shorter window and a narrower question.
- **The asymmetry between additions and deletions is contested**, with a tier-1 paper on one side
  and a lightly-cited tier-2 paper on the other, and neither read here. Treat the direction of
  the asymmetry as **unknown** rather than as established in either direction, and note that
  Petajisto's two-index evidence (companion note) found the asymmetry's *sign flipping between
  indices* in the same country and years — which is at least consistent with it being a property
  of the index's maintenance rules rather than of stocks.
- **The decay has a published mechanism, which is what distinguishes it from ordinary anomaly
  decay.** McLean–Pontiff-style decay is usually attributed to arbitrage capital arriving. Here
  two of the three surviving explanations are *structural* — index families adding tiers whose
  flows offset, and rebalances moving into a pre-announced closing auction — and would not
  reverse if arbitrage capital left.

## Implementability here

**This note mostly closes a vein, and that is its value.** The seasoning screen motivated by the
two companion notes rests on there being something to avoid at index entry. This paper is the
best evidence available that, in the one index family where the question has been studied over
four decades, **there is progressively less to avoid** — and that the reasons are structural
rather than cyclical. Any candidate built here on "freshly added names are mispriced" would be
building on a mechanism whose own literature documents its decay, in a direction the lab cannot
check without spending validation.

But three things survive, and two of them are free:

- **The pre-entry run-up is not an anomaly and does not decay.** It is the index provider's
  selection rule: providers add names that have risen and delete names that have fallen.
  Greenwood–Sammon document the total pre-announcement distance as roughly stable across the
  sample even as the announcement-day effect vanished, and Petajisto flags the same selection
  confound on the deletion side. **This is a fact about the lab's panel, not about the market.**
  A name's column becomes eligible shortly after a large positive market-adjusted move, and
  stops being eligible shortly after a large negative one. Every cross-sectional score the lab
  computes is computed on a panel whose entrants are recent winners and whose leavers are recent
  losers, and `program.md` warns that pre-2009 coverage of the eight non-US indices is thin —
  so the composition of that distortion is not even stable across train and validation. This is
  free to measure and nobody has.
- **The migration partition has a direct analogue here and it cuts the other way.** The decay's
  largest single driver is that most large-cap index additions are now offset by a simultaneous
  mid-cap index deletion. The nine indices in this panel are **large-cap national** indices, and
  for the eight non-US ones there is no tracked sibling index in the panel at all — a name
  entering the DAX or the Nikkei 225 is not leaving some other index *that this panel records*.
  Whether a mid-cap sibling with meaningful tracked assets exists in those markets is not
  something this repo's data can answer and not something this literature answers. So the
  dominant reason the US effect faded **cannot be assumed to apply to eight of the nine indices
  here**, and the authors name exactly this as their open question. That is an argument for
  measuring the panel's entry/exit return signature directly rather than importing the US
  conclusion — in either direction.
- **The one trading-relevant structural fact is unreachable.** Volume concentrating into a
  pre-announced closing auction on the effective date is a microstructure story about *when*
  within a day liquidity appears. This repo has daily bars and, under v3, fills at each name's
  next real close. There is no construction here that can express it.

**What not to do, stated plainly.** Do not build an index-addition event trade. The panel does
not carry announcement dates, v3 fills a day late on a one-day event, the US evidence says the
event is now small, and the non-US evidence does not exist. The reachable object is the
**seasoning of the panel's columns as a screen and as a diagnostic**, not the event.

**One question for whoever is allowed to read `engine/`** (this folder is not): when a name
becomes eligible and its column appears in `prices`, **does the column carry that name's price
history from before its first eligible date, or does it begin at eligibility?** The answer
decides whether a lookback feature on a fresh entrant is computed on a real pre-entry window —
in which case it is reading precisely the provider-selected run-up documented above — or on a
short, mostly-NaN window, in which case the entrant silently drops out of every long-lookback
score and the composition effect runs the other way. Both are consequential and they are
opposite. This belongs on the standing engine-read list alongside the two questions
[2026-10-08] raised about the equal-weight pool.

## Related

- `2026-10-09-index-inclusion-demand-curves-vs-price-pressure.md` — the effect whose decay this
  note documents, and the Shleifer-versus-Harris–Gurel permanence tension this note partly
  dissolves: both were describing a market structure, and the structure moved.
- `2026-10-09-index-premium-and-the-index-turnover-cost.md` — the premium *p* that enters that
  note's cost formula is the quantity this note says has decayed in the one index where it has
  been tracked. Read the two together before costing the v3 pool's membership drag.
- `2026-08-17-mclean-pontiff-publication-decay.md` — the general decay result this paper's
  authors invoke. The contrast is worth keeping: McLean–Pontiff's channel is arbitrage capital
  arriving after publication; two of the three channels surviving here are changes in how index
  families and exchanges are *organised*, which do not unwind if capital leaves.
- `2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — point-in-time membership removes
  selection on end-of-period rank. It does not remove the fact that entries and exits are
  themselves decisions taken on past returns.
- `2026-10-08-benchmark-portfolios-have-alpha-of-their-own.md` — the v3 equal-weight eligible
  pool inherits the panel's entry and exit signature in full.
- `2026-10-01-survival-conditioning-induced-drift.md`,
  `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — the lab's covered treatments
  of conditioning on a name's *end*. Index deletion is a third kind of ending, distinct from both:
  the firm survives, the price series usually continues, and only the panel's permission to hold
  it stops.
