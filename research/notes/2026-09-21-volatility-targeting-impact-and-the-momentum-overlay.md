---
title: "The Impact of Volatility Targeting"
authors: Harvey, Hoyle, Korgaonkar, Rattray, Sargaison, van Hemert
year: 2018
venue: The Journal of Portfolio Management 45(1), 14–33 (venue tier 1 by this folder's rubric — JPM is listed tier 1 — though in character it is practitioner research from Man Group with an academic lead author)
url: https://doi.org/10.3905/jpm.2018.45.1.014
citations: 76 (Semantic Scholar, checked 2026-09-21); 47 (Crossref `is-referenced-by-count`, checked 2026-09-21)
sample_period: US equities from July 1926; credit and 50 futures/forwards from 1988; all series end 2017
markets: 60+ assets — US equities (market, three 30-year subsamples, 10 industry portfolios), credit, and 50 liquid futures and forwards across equities, fixed income, currencies, commodities
tier: B — tier-1 venue, very long and genuinely multi-market sample, costs modeled, and the central claim is a *negative* one the authors had no incentive to find; held below A because there is no independent replication of it and the authors are the manager of exactly this kind of strategy.
validation_overlap: false
published_post_2018: true
read: full text, the typeset JPM article with journal header and pagination, from the lead author's Duke faculty page — `people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf`. Found by fetching the directory index and grepping its hrefs (the documented channel).
---

## Mechanism

This note exists as the counterweight to the two forecasting notes filed alongside it. Those say a
volatility forecast can be made much better. This one says **what a better forecast is worth is
asset-specific, and on equities a large part of it is not a risk effect at all.**

The paper's three-step argument:

**1. The Sharpe-ratio benefit of volatility scaling is confined to risk assets.** Scaling exposure
by the reciprocal of a conditional volatility estimate raises risk-adjusted returns for equities
and credit, and for portfolios with a large allocation to them (a 60–40 balanced portfolio, a
risk-parity portfolio). For bonds, currencies and commodities the effect on the Sharpe ratio is
negligible. The authors state plainly that extrapolating the equity result to other assets is a
mistake — which is notable, because the equity result is the one everyone cites.

**2. The reason is the leverage effect, and it is confined to the same assets.** Equities and
credit display a negative contemporaneous correlation between returns and changes in variance
(Black's debt-to-equity explanation; Bekaert–Wu's volatility-feedback story runs the causality the
other way). Other asset classes do not display it. The paper shows this directly across the 60+
assets and the 10 industry portfolios.

**3. Therefore volatility scaling on a risk asset is partly a time-series momentum overlay.** If
negative returns tend to be followed by higher volatility, then `1/σ̂` shrinks the position after
losses and grows it after gains — which is, mechanically, trend-following. The authors make this
concrete: they correlate the reciprocal of the volatility estimate with past 1-, 3-, 6- and
12-month returns, and only risk assets show a consistently positive correlation (for other assets
it is predominantly negative, i.e. volatility scaling there is a *mean-reversion* bet). Then they
close the loop: regress each asset's Sharpe-ratio improvement from volatility scaling on this
"momentumness" statistic, and it explains about half the cross-sectional variation, more when the
volatility estimate is slower. **The instrument is the one-month horizon** — short-term momentum is
what matters, not 12-month.

**4. The one effect that is not asset-specific.** Across every asset and asset class, volatility
targeting reduces the volatility of volatility and thins both tails — the left tail in particular —
and reduces maximum drawdown for the balanced and risk-parity portfolios. The authors argue this is
worth having on its own terms for an investor whose objective is not solely the Sharpe ratio. This
is the part of the result that does not depend on the leverage effect and therefore does not depend
on the momentum channel.

## Construction recipe

    r_t^scaled = r_t × k × σ_target / σ̂_{t-2}

- **Conditional volatility estimate**: the standard deviation of **daily** returns with
  exponentially decaying weights, computed **with a stated zero mean** (i.e. from squared returns)
  rather than demeaned — deliberately, so that a badly estimated short-window mean does not enter
  the risk estimate. The authors report similar results from an equal-weighted rolling window and
  from 3- or 5-day overlapping returns. Half-lives from 10 to 90 days are examined; 20 days is the
  default.
- **Lag**: the estimate uses returns up to `t−2`, so the position is known a full 24 hours ahead.
  This is a deliberate anti-look-ahead margin, stronger than a 1-day lag.
- **Warm-up**: 270 trading days required before any scaled return is formed, so that even the
  90-day half-life has at least three half-lives of data.
- **Target**: 10% annualised throughout, with a constant `k ≈ 1` chosen so the *ex post* full-sample
  realized volatility hits the target exactly. That constant is a comparability device — it makes
  scaled and unscaled series equal-volatility so the Sharpe comparison is clean — and it is
  full-sample, so **it is not implementable as stated and must not be copied into a live rule.**
- **Volatility, not variance.** The authors scale by `1/σ̂`, noting that Moreira–Muir's `1/σ̂²` form
  performs about equally and that the volatility form has **lower turnover**. For a 15 bps/side
  universe that is the version to prefer.
- **Turnover** is reported as annual round-trips of the mean exposure: mean absolute daily exposure
  change, annualised, divided by twice the mean exposure. An unscaled position has zero turnover by
  construction — the entire cost of the overlay is the overlay.
- **Evaluation at the monthly frequency** (21 weekdays or 30 calendar days, overlapping), not
  daily, with the mean and turnover of notional exposure evaluated daily. The statistics reported
  are the Sharpe ratio gross and net, the volatility of volatility, and mean shortfall/exceedance —
  a tail pair rather than a single risk number.

Where intraday data is available the authors also build the volatility estimate from 5-minute
realized variance and note, citing Bollerslev–Hood–Huss–Pedersen, that adding the squared overnight
return makes the estimate *less* persistent.

## Robustness evidence (qualitative only)

- **Nine decades of US equity data, three 30-year subsamples, 10 industry portfolios, and 50
  futures and forwards across four asset classes.** The sample is the paper's main strength: the
  asset-class split is not one market's quirk.
- **Costs are modeled** at per-asset estimates and the paper reports Sharpe ratios gross and net.
  This is the load-bearing caveat for this repo: the cost estimates are ~1 bp for equities, 0.5 bp
  for bonds, up to 3.5 bp for copper — an order of magnitude below this repo's 15 bps per side. The
  authors say the effect is "very similar on a net basis" *at those costs*, which is not a claim
  about a costlier universe.
- **The headline finding is a limit on prior work rather than a new effect**, which is the kind of
  result least likely to be a multiple-testing artifact. There is no formal replication study of it
  in this folder's sources; a contemporaneous paper (Dachraoui 2018) is cited as independently
  arguing the leverage-effect link.
- The authors are explicit that the precise relation between returns, volatility and the Sharpe
  ratio of scaled returns is unresolved and "a topic of ongoing research" — they do not oversell
  the decomposition.
- **Known gaps.** Sharpe improvements are reported against an unscaled benchmark forced to the same
  full-sample realized volatility, which is an ex-post normalisation; no multiple-testing
  correction is discussed for the cross-asset comparisons; and the whole analysis is
  unfunded/leveraged (futures and excess returns), which is exactly the case this repo is not in.

## Implementability here

**Read this note before building anything from the other two.** Its findings interact with this
lab's measured history in a specific and useful way.

**The tension, stated explicitly (per `research/README.md`'s rule).** `experiments/learnings.md`
records that de-risking overlays on the champion "reliably backfire out-of-sample" — three distinct
attempts, including inverse-vol basket weighting with volatility targeting, cut train-period
drawdown and lost more validation Sharpe than they saved — and that true inverse-vol risk parity on
an ETF sleeve did **worse** than equal weight. Tonight's literature does not contradict that; read
carefully, **it predicts it.** The paper's own decomposition says that on risk assets roughly half
the Sharpe benefit of volatility scaling is a short-horizon time-series momentum overlay. This
repo's champion is already a price-trend book. **An overlay whose principal mechanism is trend,
applied to a book that already holds trend, should be expected to add turnover and dilute rather
than to add.** That is the same shape as the 2026-09-18 overnight finding: the lab's null is what
the literature predicts, not a refutation of it.

**What follows from that, in order:**

1. **The part of the effect that is *not* the momentum overlay is the tail, and this repo has never
   measured it on its own terms.** The paper's one unconditional finding is thinner tails, lower
   volatility-of-volatility and smaller drawdowns across every asset class — a result that does not
   depend on the leverage effect. `program.md`'s gates and this lab's promotion rule are Sharpe-led,
   so a scaling overlay that trades a little Sharpe for a materially thinner left tail is scored as
   a loss here even if it is what the literature says the overlay actually buys. Any future
   volatility-scaling proposal should state up front which of the two effects it is claiming, and a
   tail claim should be tested on tail statistics (mean shortfall / exceedance, vol-of-vol), not on
   Sharpe.
2. **A "momentumness" pre-screen is available and it is free.** The paper's own instrument —
   `corr(past 21-day return, 1/σ̂_t)`, computed per instrument and per candidate volatility
   estimator — is computable on this repo's data with no trial and no champion comparison. If that
   correlation is strongly positive across this universe, the overlay is trend in costume here
   (the lab's standing screen) *and the paper says so in advance*, so the trial need not be spent.
   If it is near zero or negative, the overlay is doing something else and the null in
   `learnings.md` is a different result than it looks.
3. **The leverage cap makes this a partial mechanism here.** `program.md` caps gross leverage at
   1.0. `σ_target/σ̂` is two-sided; a long-only book capped at 1.0 can only scale *down* into cash.
   That removes the lean-in half — which, note, is also the half that is most momentum-like on the
   way up. Whether de-levering alone retains the tail benefit is not answered by this paper and
   would have to be measured.
4. **The zero-mean, exponentially weighted estimator is the right default** for any risk estimate
   in this repo: no demeaning (short-window means are noise), exponential weights, a stated
   half-life, and a hard warm-up requirement of several half-lives before the estimate is used.
   That is a cheap correctness standard independent of any strategy.
5. **The `k` constant is not implementable.** It is a full-sample ex-post scalar. Copying it would
   be a look-ahead of exactly the kind `causality_check` is built to catch.

**Universe caveat.** The paper's equity evidence is index-level and industry-portfolio-level. This
repo's single-name results are survivorship-biased (`learnings.md`, permanent caveats), and its
trailing volatility is the identified artifact — high trailing volatility predicts high forward
return here. The leverage effect the paper relies on is a *negative* return–volatility relation; the
artifact is a *positive* one in the cross-section. These are not the same statistic (one is
time-series and contemporaneous, the other cross-sectional and predictive) and they can coexist, but
the coexistence is worth checking rather than assuming, and the ETF-level subset of this universe is
the trustworthy place to check it.

## Related

- `2026-09-21-har-rv-volatility-cascade.md` and
  `2026-09-21-panel-volatility-models-and-risk-targeting.md` — the forecast; this note is what the
  forecast is worth once it sizes a position.
- `2026-08-17-volatility-timing-managed-portfolios.md` — Moreira–Muir and the Cederburg et al.
  replication challenge. This paper is the third leg of that debate and the one that localises the
  effect by asset class.
- `2026-08-17-momentum-crash-risk-management.md` — Barroso–Santa-Clara and Daniel–Moskowitz, cited
  here as the risk-managed-momentum precedents; the same "is it just trend?" question applies.
- `2026-09-17-downside-beta-and-the-volatility-confound.md` — the other note in this folder about a
  measure that reduces to the volatility level on this universe.
- `experiments/learnings.md` — "De-risking overlays on momentum reliably backfire out-of-sample"
  (three attempts) and "Standalone diversified ETF sleeves cap out well below the champion"
  (inverse-vol risk parity below equal weight). Both are the tension this note reconciles rather
  than overturns.
