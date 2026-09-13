---
title: "Information Uncertainty and Stock Returns"
authors: Zhang, X. Frank
year: 2006
venue: Journal of Finance (Tier 1)
url: https://doi.org/10.1111/j.1540-6261.2006.00831.x
citations: 1563 (Crossref by journal DOI, checked 2026-09-13); 1758 (Semantic Scholar, which resolves the paper only under its SSRN DOI 10.2139/ssrn.535783 — the journal DOI returns "not found"); 1916 (OpenAlex, checked 2026-09-13)
sample_period: January 1983 – December 2001
markets: US — NYSE, AMEX and Nasdaq common stocks (CRSP), with I/B/E/S coverage required for the analyst-based proxies
tier: A
validation_overlap: false
published_post_2018: false
---

Read **in full** from the typeset *Journal of Finance* article (vol. LXI no. 1), served by a
university course reading-list directory (`cis.upenn.edu/~mkearns/finread/`) — the same channel
session 14 found by grepping a parent directory's `href`s, here reached directly.

Why this source, tonight: the lab's 2026-09-12 nightly measured that **removing names with less
than five years of price history costs its momentum leg**, recorded the number with a clean
t-statistic and a passing placebo, and filed it as *survivorship bias* and an anti-candidate. This
folder had no note anywhere on what the length of a name's listing history is supposed to do to
returns — `firm age`, `listing age`, `age effect` and `new list` all returned **zero** across the
prior 94 notes. This is the source that defines the variable and states the mechanism, and its
prediction has the **same sign as the lab's measurement from a cause that is not bias at all**.

## Mechanism

The paper's subject is not a characteristic; it is a **conditioning variable on underreaction**.

The premise is the standard underreaction account of short-horizon continuation: prices adjust too
slowly to firm-specific news, so past winners keep winning and past losers keep losing. The
paper's contribution is to ask what makes the adjustment slower, and to answer: **ambiguity about
what the news means for value**. If continuation is underreaction, then where the implication of a
signal is harder to assess, the initial reaction should be more incomplete and the subsequent drift
larger. The paper calls that ambiguity *information uncertainty* and is explicit that it is a
property of the signal's interpretability, not of the firm's riskiness.

The identification is the part worth carrying, because it is what separates this from a risk story.
Uncertainty is made to predict returns **with opposite signs conditional on the direction of the
news**: higher expected returns following good news, *lower* expected returns following bad news.
A cross-sectional risk factor cannot do that — a risk premium is signed one way regardless of what
the firm just announced. The paper states this as its own conclusion: the evidence "is inconsistent
with the notion that information uncertainty is a cross-sectional risk factor."

**Firm age enters as one of six proxies for that uncertainty**, with the rationale taken from Barry
and Brown: firms with a long history have more information available to the market, and older firms
also tend to sit in more mature industries, so age additionally picks up industry-level volatility.
The paper notes that the role of firm age in predicting future returns had not been documented
empirically before it.

## Construction recipe

**The uncertainty proxies** (six, used one at a time, not combined):

1. `MV` — market capitalisation at the formation date. Used first but distrusted by the author for
   the obvious reason: it captures many other things.
2. **`AGE` — the number of years since the firm was first covered by CRSP.** Note the definition
   carefully: it is *the length of the return history in the database*, not the founding date.
3. `COV` — number of analysts covering the firm in the prior year.
4. `DISP` — standard deviation of analyst forecasts, scaled by the prior year-end price.
5. `SIGMA` — standard deviation of weekly market-excess returns over the year ending at the
   formation date. Weekly returns are measured Thursday-to-Wednesday, explicitly to blunt
   nonsynchronous trading and bid-ask bounce.
6. `CVOL` — standard deviation of operating cash flow over the past five years (minimum three).

The uncertainty variable is entered as its **reciprocal** for the size/age/coverage proxies, so
that "high" always means "more uncertain" across all six.

**The news proxies** (two, used separately): the sign of the analyst forecast revision, and — the
one available without analyst data — **past return from `t−11` to `t−1`**, i.e. an eleven-month
formation window that stops one month before the formation date.

**The sort.** Each month, sort into five quintiles on the news proxy first; then, *within each news
quintile*, sort into five groups on the uncertainty proxy. This is a **sequential (non-independent)
sort**, deliberately so, and the paper reports that results survive independent sorts and survive
reversing the order (uncertainty first, then momentum).

**Holding and weighting.** One-month holding period, equal-weighted portfolio returns, monthly
rebalance. The one-month holding is a deliberate choice and the paper says why: the usual K-month
overlapping convention averages across K implementation dates and dilutes exactly the short-lived
effect being measured.

**Screens.** Price below $5 at formation excluded (following Jegadeesh–Titman 2001, to keep the
result off small illiquid names and bid-ask bounce); firms with **fewer than 12 months of past
return data excluded**, explicitly to avoid a confound with recent listings. That second screen is
worth noting: the paper measures an age effect while deliberately discarding the very youngest
cohort.

**The persistence test, and it is the most load-bearing construction detail for a long-only book.**
Repeat the whole design but wait `L` months after formation before assigning to portfolios, for
`L = 1…6`. As the lag grows and uncertainty resolves, the high-minus-low uncertainty return
differential shrinks. It does so **asymmetrically**: the differential following bad news persists
for roughly half a year, while **the differential following good news is gone after about one
month**. The paper attributes the asymmetry on the bad-news side to short-sale restrictions.

## Robustness evidence (qualitative only)

- **Six proxies, one picture.** The six uncertainty measures are constructed from four unrelated
  data sources (prices, listing history, analyst counts, accounting cash flows) and all produce the
  same monotone pattern in the same direction. That is the paper's own robustness argument and it
  is a good one: a construction artifact would have to be shared by all four.
- **The monotonicity is across the full uncertainty quintile ladder**, not a spread between
  extremes, which is the stronger shape (cf. the folder's monotonicity-test note).
- **Direction, stated without magnitudes** (the folder's standing rule): within past *winners*, the
  highest-uncertainty group earns more than the lowest, and the differential is significant at
  conventional levels; within past *losers*, the differential runs the other way and is **larger in
  magnitude** than the winner-side differential. The tradeable half for a long-only book is the
  smaller half.
- **Single market, single sample, one author.** No independent replication is recorded in the
  paper, and this folder has not found one. Published 2006 — old enough that
  McLean–Pontiff-style post-publication decay applies to whatever part of it is real; the folder's
  standing discount for a widely-read, easily-computed conditioning variable applies here.
- The paper also reports that on an expanded sample the size effect is significantly negative and
  the **effect of firm age is insignificant** on its own — i.e. the age variable is offered as a
  *conditioner*, not as a standalone predictor. See the companion note on the level effect.

## Implementability here

**`AGE` is the only one of the six proxies this repo can build exactly as defined, and it is free.**
"Years since first covered by CRSP" translates with no loss to *years since the first non-missing
close in `data/store/` for that instrument*. `SIGMA` is the second buildable one — a trailing
volatility of weekly returns, which `strategies/lib/features.py` already supports in range and
close-to-close forms. The other four (`COV`, `DISP`, `CVOL`, and `MV` in its accounting sense)
need analyst or fundamental data and are out of scope.

**What the construction implies for a candidate here**, node by node:

- The news proxy `t−11 → t−1` is the champion's own family of signal, so the interaction is a
  *conditioning* of an existing leg, not a new leg. It costs one trial, not a family.
- The sequential sort (news first, uncertainty within) is the cheap shape: it can be expressed as
  ranking on momentum and then re-ranking the top band on age, which is one extra operator on a
  book the repo already builds.
- **The one-month holding period is a cost problem, not a detail.** The paper chose it because the
  good-news-side differential decays within about a month; at 15 bps per side and a 1-day execution
  lag, a monthly-rebalanced conditioned book pays for exactly the horizon where the effect lives.
  The repo's own cost arithmetic should be applied before the trial, not after.
- **The long-only constraint removes the larger half of the effect.** The bad-news side — where the
  uncertainty differential is bigger and more persistent, and where the paper's own explanation is
  short-sale constraints — is unreachable here. That is the same discount the folder's long-side
  share note records for anomalies generally, and it is unusually explicit in this source.

**Four pitfalls, and the first two are specific to this repo's universe:**

1. **`AGE` here is a data-vendor artifact as much as a firm attribute.** In CRSP it is the listing
   date; in `data/store/` it is whichever date the free vendor's history starts, and for the 42
   ETFs it is fund inception, which has nothing to do with the information environment of the
   underlying. Any age construction should probably be built on the stock sleeve only, or with the
   ETF sleeve as an explicit separate group.
2. **In a current-constituents universe, "young" is the most selected slice there is.** A name with
   a short history that is *in today's index* both entered recently and survived. The lab's own
   overnight measurement of the age tilt therefore does not, on its own, separate this source's
   mechanism from survivorship — see the "Related" section for what would.
3. **This universe is 140 large global names**, so the age distribution is compressed relative to a
   CRSP cross-section and the young tail is thin. Check the pool count in the "young" band before
   reading anything into a spread built from it; the repo's own dilution rule (only the *marginal*
   profile locates a band, never the cumulative) applies.
4. **`SIGMA` as a conditioner is not the low-vol bet this repo already refuted.** `learnings.md`
   closes the low-vol/inverse-vol family as a *level* signal on this universe. Zhang uses volatility
   as an interaction with news direction, which is a different object and predicts a different sign
   pattern. That is a tension worth stating out loud rather than letting the closed family silently
   veto the interaction — but it is also not a licence to reopen the family; the interaction has to
   be graded on the interaction, i.e. as a difference of conditional slopes.

## Related

- `notes/2026-09-13-analyst-coverage-and-the-speed-of-bad-news.md` — the same conditioning idea
  with an information-flow mechanism and an explicit size gradient; the two papers are each other's
  closest neighbours and the coverage paper is the one Zhang's `COV` proxy comes from.
- `notes/2026-09-13-listing-age-as-a-level-effect.md` — the contested *level* sign of the same
  variable, and why the tilt is an anti-candidate even though the conditioning is not.
- `notes/2026-09-02-anomalies-by-size-group.md` — where in the size distribution this universe sits;
  the two notes answer the same question from different sides (which predictors survive among big
  stocks vs. which conditioners make a predictor stronger).
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the bias that the age
  variable is entangled with here.
- `notes/2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — the right statistic for a claim of
  the form "the effect rises across the uncertainty ladder".
- `notes/2026-09-06-long-side-share-of-anomaly-profits.md` — the standing discount this paper's
  winner/loser asymmetry makes concrete.
