---
title: "The Long-Run Performance of Initial Public Offerings (with Barry–Brown's 'period of listing' effect as the opposing claim)"
authors: Ritter (primary); Barry, Brown (second source, not read)
year: 1991 (Ritter); 1984 (Barry–Brown)
venue: Journal of Finance (Tier 1); Journal of Financial Economics (Tier 1)
url: https://doi.org/10.1111/j.1540-6261.1991.tb03743.x ; https://doi.org/10.1016/0304-405X(84)90026-6
citations: Ritter — 3787 (Semantic Scholar by DOI, checked 2026-09-13), 1766 (Crossref, same date), 3429 (OpenAlex, same date). Barry–Brown — 536 (Semantic Scholar), 370 (Crossref), 550 (OpenAlex), all checked 2026-09-13
sample_period: Ritter — US IPOs of 1975–1984, tracked three years past listing. Barry–Brown — not read; the abstract does not state a sample period
markets: US — NASDAQ and AMEX/NYSE common stock
tier: A for Ritter (read in full); Barry–Brown is recorded **unread**, abstract only, and nothing below rests on it beyond what its abstract states in its own words
validation_overlap: false
published_post_2018: false
---

**Ritter read in full.** The article is a **text-layerless scan** — `pypdf` extracts 24 characters
from 25 pages — so it was rendered with `pymupdf` at 130 dpi and read as page images, the recipe
this folder added on 2026-09-08. Access route worth recording: a guessed
`site.warrington.ufl.edu/ritter/files/2016/09/…` path 404'd, and fetching the author's
**`/published-articles/` index page and grepping its `href`s** produced the correct (undated,
non-`/files/YYYY/MM/`) URL immediately. That is the parent-directory trick from sessions 11, 12 and
14, applied to an author's own publication list rather than a directory listing, and it is now four
for four.

**Barry–Brown is closed everywhere reachable**: OpenAlex reports `oa_status: closed` with no
repository copy, Semantic Scholar returns `CLOSED` with the abstract field explicitly *elided by
the publisher*, and ScienceDirect refuses an automated client. Its published abstract was recovered
verbatim from an institutional research portal (`research.monash.edu`) and is the only thing taken
from it. It is recorded as **not read**.

This note exists to answer one question the previous two notes leave open: *if the length of a
name's listing history conditions continuation, does it also predict returns on its own?* The
answer the literature gives is **two answers with opposite signs**, and that is the finding.

## Mechanism

**Claim A — young listings should earn more (Barry–Brown, estimation risk).** Where less
information is available about a security, investors' parameter estimates are noisier; if that
estimation risk is not diversifiable it must be compensated, so less-known securities carry higher
required returns. The paper's own words, from its abstract: it uses "period of listing as a proxy
for quantity of information" and finds "an association between period of listing and security
returns that cannot be accounted for by firm size and which is not diminished by an elimination of
January returns data" — naming the result the **"period of listing" effect**. The sign is not stated
in the abstract; the estimation-risk model it is offered as a test of predicts higher returns for
the less-informed (shorter-listed) names, and this is how the later literature — including Zhang's
uncertainty paper, which cites Barry and Brown for exactly this premise — restates it.

**Claim B — young listings should earn less (Ritter, over-optimism and windows of opportunity).**
Newly listed firms are sold into a market that is periodically over-optimistic about the earnings
potential of young growth companies, and issuers time their offerings to those windows. The
implication is that the first aftermarket price is too *high*, not that the offer price is too low,
and that the correction shows up as underperformance against comparable seasoned firms over the
following few years.

**The two claims are about the same observable and point in opposite directions.** Both use age at
or near listing as a proxy for "how little is known"; one prices it as a risk premium, the other as
a sentiment premium that unwinds. Ritter's own reading of his age results is that age proxies for
**ex ante uncertainty and investor optimism simultaneously**, which is precisely why the sign cannot
be settled by measuring the variable.

## Construction recipe

Ritter's design, which is the one with enough detail to reproduce:

- **Event time, not calendar time.** Month 0 is the initial-return period (normally one day, offer
  price to first close); the aftermarket period is the following 36 months, defined as successive
  21-trading-day blocks from the listing date. Wherever the initial return period runs longer than
  a day, month 1 is truncated accordingly.
- **Two performance measures, deliberately both.** (i) Cumulative average adjusted returns with
  monthly rebalancing against four benchmarks — a value-weighted broad index, a value-weighted
  listed-exchange index, an index of the smallest size decile, and matched firms; (ii) three-year
  **buy-and-hold** returns for the new listings and for their matched firms. The gap between the
  two measures is itself informative: rebalanced-CAR and buy-and-hold answer different questions,
  which is the same distinction this folder's rebalancing-attribution note makes.
- **Matching, and its honest accounting.** Matched firms are exchange-listed securities matched on
  three-digit SIC industry and market value, each usable once. The paper reports plainly that only
  about a third of matches land in the same three-digit industry and that matches are on average
  larger, and it reports the sensitivity: restricting to same-two-digit-industry matches *moves the
  result toward zero but does not remove it*, which it interprets as new listings underperforming
  their own industries, which in turn underperform the market.
- **Delisting handling**, and this is the detail a survivorship-conscious lab should take: for
  issues delisted before the three-year anniversary the aftermarket window is **truncated at the
  last available price** rather than dropped. Names that move between exchanges are kept.
- **The age variable**: age at listing = offer year minus founding year, bucketed (0–1, 2–4, 5–9,
  10–19, 20+ years). It is a *founding-date* age, not a history-length age — the opposite
  measurement choice from Zhang's.
- **The age result, direction only**: aftermarket performance rises **monotonically** across the age
  ladder, and the initial return falls monotonically across the same ladder. The two monotone
  patterns run in opposite directions, and the paper argues the age cut separates the data more
  cleanly than the industry cut does. Robustness reported: excluding the two industries with the
  most extreme results preserves the monotone age pattern.

## Robustness evidence (qualitative only)

- **Ritter**: one market, one listing cohort decade, one author; the paper itself flags two of its
  own limits — that it cannot say whether the underperformance continues past the three-year window,
  and that generality requires a longer sample. Industry composition is shown to matter a great
  deal, and the result is reported as present in all but three of fourteen industry groupings. The
  effect has generated a very large follow-up literature — including, notably, a long methodological
  argument about whether long-horizon abnormal-return tests of this shape are well specified at all
  (the benchmark/skewness critiques). That argument is a reason to treat the *magnitude* as
  unsettled; the age **ordering** within the sample does not depend on the benchmark choice, since
  it is a comparison across buckets that share one.
- **Barry–Brown**: not read. Its abstract claims the effect is not explained by firm size and does
  not disappear when January is removed — i.e. it survives the two obvious confounds of its era.
  This folder has found no evidence that the "period of listing" effect was independently replicated
  or that it appears in the modern replication inventories, and **absence of a note is not absence of
  evidence** — record it as an unverified 1984 result, not as an established regularity.
- **The two together are the honest summary**: a widely cited Tier-1 source says short-listed names
  earn *more*; another widely cited Tier-1 source says newly listed names earn *less*. They are not
  strictly contradictory (different measurement of age, different horizon, different populations),
  but nothing in the literature this folder has read resolves the sign of a listing-age tilt.

## Implementability here

**As a tilt: no, and this is an anti-candidate.** Three independent reasons, any one sufficient:

1. **The sign is contested between two Tier-A sources**, and the folder's standing rule is that a
   mechanism whose direction the literature does not agree on is not hypothesis fodder — it is a
   reason to expect a coin flip and to spend a permanent deflated-Sharpe increment on one.
2. **Neither paper's age variable is measurable here.** Ritter's is founding-date age and needs
   offer dates and a pre-listing record; this repo has neither. Zhang's history-length age is
   measurable, but it is a *different variable*, and in a store built from a free vendor's
   histories it is partly a vendor artifact (see the previous note).
3. **In a current-constituents universe the young cohort is the maximally selected slice.** Every
   short-history name in `data/store/` both listed recently and survived to be in today's index —
   the exact conditioning the folder's survivorship note says manufactures persistence. A tilt built
   on it is measuring the selection.

**As a caveat: yes, and it is load-bearing.** The lab's 2026-09-12 nightly measured that removing
names with short histories costs its momentum leg, with a passing placebo, and filed it as
survivorship bias. Zhang's mechanism predicts **the same sign from a cause that is not bias**
(young = high information uncertainty = stronger continuation), and Ritter's predicts the same sign
again through a third channel (young listings drift down, so they populate the loser end and
sharpen the momentum spread from the untradeable side). **The lab's measurement is therefore
consistent with at least three distinct causes and identifies none of them.** That does not weaken
the caution — a caution that holds under three mechanisms is stronger, not weaker — but it does mean
the number should not be reported as *the size of the survivorship bias*, which is how a single
t-statistic invites it to be read.

**One free screen that would separate them**, offered as a diagnostic and not as a book (it needs no
trial, no new lib file, and both outcomes are findings):

> Measure the momentum leg's band excess conditioned on **history length** and, on the same dates and
> the same pool, conditioned on **trailing volatility** (Zhang's `SIGMA`, the second of his six
> proxies this repo can build), with a hash-based pseudo-age as the placebo. If the conditional
> gradient has the same sign on both, the pattern is an uncertainty-conditioning effect that happens
> to correlate with history length. If it appears only on history length, it is about how names
> entered this universe, and the survivorship reading stands. Pre-commit the reading before running
> it; and note that the pool count in the short-history band must be checked first, because this
> universe's age distribution is compressed and the band may be too thin to read.

The *level* leg of that screen — does a short-history tilt earn anything on its own — should also be
printed while the machinery is up, because it costs one extra line and it is the direct test of the
"period of listing" effect on this universe. Expect nothing from it; record whatever comes.

## Related

- `notes/2026-09-13-information-uncertainty-and-price-continuation.md` — the conditioning use of the
  same variable, with the measurable definition and the construction.
- `notes/2026-09-13-analyst-coverage-and-the-speed-of-bad-news.md` — the third mechanism that
  predicts the same sign through information flow rather than through age.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` and
  `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the bias this variable is
  entangled with in a current-constituents universe.
- `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the rebalanced-CAR versus
  buy-and-hold distinction Ritter's two measures embody.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` — the return-distribution
  reason long-horizon abnormal-return tests of Ritter's shape are contested.
