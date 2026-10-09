---
title: "The Index Premium and Its Hidden Cost for Index Funds — with: Why Do Demand Curves for Stocks Slope Down?"
authors: Petajisto
year: 2011; 2009
venue: Journal of Empirical Finance 18(2), 271–288 (venue tier 2 — solid peer-reviewed field journal, below the JF/JFE/RFS tier); Journal of Financial and Quantitative Analysis 44(5), 1013–1044 (venue tier 1)
url: https://doi.org/10.1016/j.jempfin.2010.10.002 ; https://doi.org/10.1017/S0022109009990317
citations: "2011 paper: 93 (Crossref is-referenced-by-count, checked 2026-10-09). 2009 paper: 118 (Crossref, checked 2026-10-09)"
sample_period: 1990–2005 (both S&P 500 and Russell 2000 index changes); the 2009 theory paper is a calibration, not a sample
markets: US equities — S&P 500 and Russell 2000 index changes
tier: B — the empirical paper is careful, cost-aware, multi-index and explicit about its own standard errors, but it is one country, one decade and a half, a tier-2 venue and a two-digit citation count, and no independent replication of its *index turnover cost* construct was found
validation_overlap: false
published_post_2018: false
---

## Mechanism

Petajisto (2011) does three things the founding pair of 1986 could not. It measures the index
premium on **two indices with different selection rules**, it estimates **what the premium
implies about the slope of the demand curve**, and — the part that matters most here — it turns
the premium into a **recurring cost borne by anyone who mechanically tracks an index**, with a
closed form. The 2009 JFQA companion supplies the equilibrium model that makes a steep demand
curve consistent with rational agents at all.

**The premium and its shape.** Measured from announcement to effective day, additions and
deletions both move sharply, and the path has structure worth knowing. For S&P 500 additions,
roughly a percent accumulates in the last few days *before* announcement; the largest jump is
immediately after announcement; and then — the finding Petajisto himself calls surprising —
a drift of about half a percent to a percent *per day* continues between announcement and
effective day, peaking on the effective day. About 2% reverses over the following three days,
and nothing further reverses over the next two weeks. Deletions behave similarly with more
pre-announcement anticipation, and Petajisto flags a confound in their pre-event leg that is
central to this repo: **part of the negative pre-announcement return of a deletion is selection,
not price impact — the provider deletes names that have just fallen hard.** He notes the
asymmetry in that confound: because extreme negative returns are more common than extreme
positive ones, and because all index changes are prompted by a deletion, the same selection
story is much weaker for additions.

**The implied elasticity.** Price impact divided by the size of the mechanical demand shock is
an estimate of the price elasticity of demand for an individual share. With a shock of about
10% of the index and an averaged premium of about 12%, he obtains an elasticity of about
**−0.84 for S&P 500 changes** — close to the unit elasticity implied by the 1986 result at a
time when indexation was an order of magnitude smaller — and about **−0.43 for the Russell
2000**, i.e. Russell 2000 names have roughly half the demand elasticity of S&P 500 names. Two
caveats he states himself: the share of "indexers" in the denominator is the noisiest input, and
benchmark-hugging active money is not mechanical but behaves partly as if it were.

**What makes a stock's demand curve steep.** This is the cross-sectional half, tested on the
Russell 2000 where hundreds of changes a year give power. Using Fama–MacBeth across annual
cross-sections with a 10 × 5 size × idiosyncratic-risk control-portfolio grid:

- **Idiosyncratic risk raises price impact**, strongly (t ≈ 10 univariate, ≈ 8 with size
  controlled). The mechanism is limits-to-arbitrage: an arbitrageur who sells to a forced buyer
  carries the name's idiosyncratic variance, and will not do it cheaply. The 2009 companion
  derives this as an equilibrium implication rather than assuming it.
- **Size lowers price impact** (t ≈ −3 to −6 with idiosyncratic risk controlled). Bigger names
  have more elastic demand.
- In a CAPM world the idiosyncratic-risk coefficient should be essentially zero. It is not.

**The index turnover cost — the construct that matters here.** A mechanical tracker *always buys
at the premium and always sells without it*. Petajisto compares it to an **index-neutral** fund
that holds a fraction *s* of the same pool of large stocks without caring whether a given name
is currently in the index. Writing *p* for the premium, *a* and *d* for the fraction of index
market value added and deleted per year (*a > d* because mergers remove names without a
replacement sale), the tracker's one-year drag relative to the index-neutral portfolio is

    index turnover cost  =  p·[ s(a − d) + d ] / (1 + p)                     ... premium permanent
    index turnover cost  =  p·( a + d ) / (1 + p)                            ... premium fully reversed

The two expressions bracket the answer because the cost depends on whether the premium survives:
if it is permanent the index-neutral fund *earns* it on the names it already held that later get
added, and only the deletion leg is a pure loss; if it fully reverses, both legs are losses. For
the S&P 500 over his sample the cost is **21–28 bp per year** depending on which end you believe,
rising to **65–82 bp** in the sample's peak year; for the Russell 2000 it is **38–77 bp per year**
and reaches several hundred bp in the peak year, because that index's turnover is far higher.
Petajisto's framing is that these are **lower bounds**, and that they are large next to the
explicit fees of the index funds themselves.

## Construction recipe

**Index turnover cost, as a diagnostic you can run on any membership panel.** The inputs are all
countable from an eligibility matrix plus one premium estimate: *a* = value share of the index
added per year, *d* = value share deleted per year, *s* = the share of the comparable pool the
index covers, *p* = the premium. Because the formula is linear in *p* and the bracket term is
pure accounting, **the turnover half can be computed with no return data at all**, and the whole
thing becomes "how big is the premium?" times a number you already know.

**The index-neutral portfolio.** Hold a fixed fraction of a *broader* pool of comparable names,
chosen without reference to index membership, and do not trade on membership changes. This is
the benchmark against which the cost is defined, and the construction is deliberately minimal —
Petajisto's point is that the two portfolios have "essentially identical" risk and return
characteristics and differ only in whether they pay the membership tax.

**The cross-sectional conditioners.** Estimate idiosyncratic risk as the root-mean-squared error
of a regression of the name's daily excess returns on a small factor set, over a window that
**ends before the event's anticipation window opens** (he uses November 1 – April 30 for a June
event, deliberately stopping two months short). Measure size at the same pre-anticipation date.
Sort sequentially rather than independently — size and idiosyncratic risk are strongly negatively
correlated — and run Fama–MacBeth across annual cross-sections rather than pooling, because all
of an index's changes land on the same dates and the abnormal returns are heavily
cross-correlated within a year.

**Horizon findings, which are index-specific and should not be averaged.** For S&P 500
additions, about half the alpha reverses within four months and a few percent remains at six
months; S&P 500 deletions reverse fully within about two months. For the Russell 2000 the
asymmetry runs the *other way*: additions reverse fully within about two months while deletions
stay put for six. Petajisto is careful that standard errors grow with horizon and that the
long-horizon inference is weak in both cases — but the direction of the asymmetry flips between
two indices in the same country over the same years, which is the useful fact.

## Robustness evidence (qualitative only)

- **Two indices, different rules, same qualitative result**: a large, highly significant
  announcement-to-effective price impact in both, with the smaller-cap index showing the less
  elastic demand. That is the prediction the size result makes, measured across indices rather
  than within one.
- **The premium rises and then falls across the sample**, tracking first the growth of indexation
  and then, in Petajisto's reading, the arrival of arbitrage capital. He explicitly entertains
  that market efficiency in this specific context improved late in his sample. The companion
  note on the decay literature takes this much further and reaches a stronger conclusion.
- **Four-factor alphas and plain market-adjusted returns give nearly the same answer** (8.1% vs
  8.8% for S&P additions; −14.7% vs −15.1% for deletions), so the result is not a factor-model
  artifact.
- **The permanence question is left open by this paper too**, deliberately: he reports both the
  no-reversal and full-reversal versions of the cost rather than picking one, and says lack of
  statistical power prevents a sharper long-term inference. That is the honest treatment, and it
  is the same impasse the 1986 pair reached.
- **Known weaknesses**: single country; the share-of-indexers input is acknowledged as the
  dominant noise source in the elasticity estimates; the index-turnover-cost construct appears
  to have attracted little independent replication (he names one concurrent attempt), which is
  why this note is Tier B despite how useful the construct is.

## Implementability here

**The single most important line in this note.** Protocol v3 deflates **skill against the
equal-weight eligible pool**. That pool is, by construction, *a mechanical tracker of nine
maintained indices* — it holds every eligible name and nothing else, so it acquires each name at
whatever price index addition left it at and drops each name at whatever price index deletion
left it at. Petajisto's index turnover cost is exactly the drag such a portfolio pays, and it is
**a property of the benchmark, not of any candidate measured against it**. The lab has never
counted it.

Three concrete consequences:

1. **Sizing it is nearly free.** The bracket term `s(a − d) + d` needs only entry and exit counts
   from the `eligible` matrix, weighted by whatever size proxy the panel supports. The lab can
   compute the panel's annual eligibility turnover for train and for validation separately in a
   few lines, with no returns and no trial. If the panel's annual turnover is small, the whole
   vein closes immediately and cheaply; if it is not, the next question is what *p* is on these
   nine indices, which the literature does not answer (see the decay note).
2. **The index-neutral portfolio is unbuildable on this panel, and that is itself the finding.**
   Petajisto's escape route is to hold comparable names *outside* the index. Under protocol v2/v3
   the panel contains only names that are or have been index members, and the engine zeroes
   weight on a name on any date it is not eligible. **So the lab is structurally confined to the
   mechanical-tracker side of his comparison**: it is forced to sell on deletion (the leg that is
   a pure loss under either permanence assumption) and it cannot pre-position in a name before
   addition (the leg that pays the index-neutral fund). The one piece of the cost a candidate can
   decline is *overpaying on entry* — not buying a name while it is freshly eligible. That is the
   seasoning screen the companion note proposes, and this note is what sizes its upside.
3. **A candidate that merely declines the entry leg will show positive skill against the pool for
   a reason that is not forecasting.** That is not a reason to avoid it — v3's objective is skill
   against the pool and this is a real, repeatable source of it — but it must be *declared* as a
   benchmark-composition effect rather than reported as a cross-sectional edge. This is the
   [2026-10-08] Cremers–Petajisto–Zitzewitz point arriving a second time through a different
   door, and with a formula attached.

**The cross-sectional conditioners transfer only partly.**
- **Idiosyncratic risk** is directly computable from the daily close panel (residual RMSE against
  a market proxy or the pool, over a window that stops short of the event). This is the stronger
  of his two conditioners and the one with a mechanism behind it.
- **Size is not available.** There are no shares outstanding in this repo, so market cap cannot be
  formed. Trailing dollar volume is the obvious proxy and it is *not the same variable* — it
  conflates size with turnover, and the lab's own v2 work already found a liquidity tilt doing
  real work in a reversal book, so the proxy is entangled with an effect the lab has measured
  separately. Say "dollar-volume tier", not "size".
- Note also that under v3 the cost model already charges illiquid names more (the 15/20/30/40 bps
  tier), so the names with the steepest demand curves are the names the protocol charges most to
  trade. Any construction that tilts toward high price impact to harvest a premium is paying for
  the tilt twice.

**Panel-specific cautions.**
- His demand-shock denominator is *the share of the index held by mechanical trackers*. For the
  S&P 500 that number is knowable; for the eight non-US indices in this panel it is not in any
  data the lab holds, and the literature covered here does not supply it. Any elasticity
  arithmetic on those indices would be an import, not a measurement.
- His event windows are built around announcement dates. The panel has eligibility, which is at
  or after the effective date — so the entire announcement-to-effective drift he documents has
  already happened before the lab can see anything. What survives into the panel's reach is the
  *post*-effective behaviour, which in his S&P sample is a ~2% reversal over three days and then
  nothing for two weeks, and in his Russell sample is a full reversal over two months. Under v3's
  next-real-close fills, a three-day window is unreachable; a two-month one is not.

## Related

- `2026-10-09-index-inclusion-demand-curves-vs-price-pressure.md` — the founding pair, the
  permanence tension this paper inherits and does not settle, and the seasoning screen.
- `2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — what the premium *p* in
  this note's cost formula has done since, which is the input that decides whether any of this
  is worth anything.
- `2026-10-08-benchmark-portfolios-have-alpha-of-their-own.md` — the general version of this
  note's point 3: the v3 statistic is a difference against one specific portfolio, and that
  portfolio's own construction is a term in every number the lab reports.
- `2026-10-08-no-trade-bands-under-proportional-costs.md` — the other half of "what a mechanical
  rebalance costs". That note is about trades the candidate chooses to make; this one is about
  trades the *universe definition* forces on it.
- `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md`, `2026-09-22-limits-of-arbitrage-performance-based.md`
  — the idiosyncratic-risk-as-arbitrage-cost channel this paper's cross-sectional result and its
  2009 companion rest on.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md` — the lab's covered measure of price
  impact per dollar, which is the empirical stand-in for "steep demand curve" when the demand
  shock itself is unobservable.
