---
title: "Factor momentum — signing a portfolio's weight by its own past return (and whether the timing adds anything to holding all of them)"
authors: "Ehsani, Linnainmaa (primary); Fan, Li, Liao, Liu (the reexamination); Arnott, Clements, Kalesnik, Linnainmaa (the working paper read for the one-month claim)"
year: "2022 (JF; NBER WP 2019) / 2022 (Financial Review) / 2018 working paper, published 2023 (RFS)"
venue: "Journal of Finance (Tier 1); The Financial Review (Tier 2 — peer-reviewed, mid-tier, low citation count); Review of Financial Studies (Tier 1) but read only as its January 2018 working paper"
url: "https://doi.org/10.1111/jofi.13131 (read as https://www.nber.org/system/files/working_papers/w25551/w25551.pdf) ; https://doi.org/10.1111/fire.12300 (read in full, open access via pureadmin.qub.ac.uk) ; https://doi.org/10.1093/rfs/hhad006 (NOT read; the January 2018 working paper https://ssrn.com/abstract=3116974 was read via rodneywhitecenter.wharton.upenn.edu)"
citations: "Ehsani–Linnainmaa 230 (OpenAlex by DOI, checked 2026-09-17; Crossref 214; Semantic Scholar's DOI endpoint returns 'not found' for this DOI). Fan et al. 11 (Semantic Scholar by DOI, checked 2026-09-17); 12 (OpenAlex, same date). Arnott et al. 83 (OpenAlex/Crossref by DOI, checked 2026-09-17; Semantic Scholar 40). Gupta–Kelly 129 (OpenAlex by DOI, checked 2026-09-17) — not read, see below."
sample_period: "Ehsani–Linnainmaa: US factors Jul 1963–Dec 2015, global (developed ex-US) factors Jul 1990–Dec 2015. Fan et al.: Jul 1964–Dec 2015 (22-factor sample) and Jan 1967–Dec 2020 (187-factor sample). Arnott et al. working paper: Jul 1963–Dec 2016."
markets: "US equity factors (15) plus developed-ex-US global factors (7) in Ehsani–Linnainmaa; 22 and 187 US factor series in Fan et al."
tier: "A for the mechanism (Ehsani–Linnainmaa, JF, heavily cited, decomposition given in closed form). B for the verdict on whether the timing is worth trading (Fan et al. is peer-reviewed and directly on the question but has few citations and no independent replication of its own)."
validation_overlap: "true — but only through Fan et al., whose 187-factor sample runs to Dec 2020 and therefore touches 2018–2020. Ehsani–Linnainmaa and the Arnott et al. working paper both end before 2018 (validation_overlap false for those two)."
published_post_2018: true
---

**What was read, and what was not.** Ehsani–Linnainmaa was read in full as NBER working paper
w25551 (February 2019); the Journal of Finance version (2022) was not read, and this note cannot say
what the referees changed. Fan et al. was read in full from the publisher's version of record
(open access, Creative Commons). The Arnott et al. paper was read only as its **January 2018
working paper**, whose author list (four) differs from the published 2023 RFS version (three) — it is
used here for one claim only, and the tier reflects that. **Gupta–Kelly, "Factor Momentum
Everywhere" (JPM 2019, DOI `10.3905/jpm.2019.45.3.013`), was not read**: `pm-research.com` refuses an
automated client and `papers.ssrn.com` returned HTTP 403 for its delivery URL. Nothing in this note
rests on it; it is named only so a future session does not re-hunt it.

## Mechanism

**The claim.** A factor — meaning the return series of a long/short portfolio sorted on some
characteristic — is **positively autocorrelated in its own past return**, at a formation horizon of
roughly one month to two years. Ehsani–Linnainmaa's central regression is deliberately crude and
worth copying for that reason: regress a factor's month-`t` return on a **0/1 indicator** for whether
that factor's own return over `t−12 … t−1` was positive. Pooled across their twenty non-momentum
factors the slope is large and strongly significant, and — the part that matters economically — the
*intercept* is indistinguishable from zero. Read literally: **the average factor earns nothing
following a down year and earns its whole premium following an up year.** Individually, most factors'
slopes are positive and about half are significant on their own; the exception is the momentum factor
itself, whose slope is ~zero (see the tension section).

**Why this is not the same claim as "factors have premia".** Ehsani–Linnainmaa call the strategy
*model-free*: if a factor is autocorrelated, you can harvest the autocorrelation **without knowing
which leg of the factor is supposed to pay**. You take the long side of the spread after the spread
has been positive and the short side after it has been negative. So the mechanism does not require
believing any particular characteristic is priced — it requires only persistence in whatever the
sort produces. That is a genuinely different epistemic position from factor investing, and it is the
strongest reason to care about it.

**The economic story is admitted to be missing.** The authors say so in as many words ("for reasons
we do not yet understand"). The behavioral candidate is slow diffusion of factor-level information;
the structural candidate is persistence in factor-level risk premia or in the flows chasing them.
Treat the mechanism as an empirical regularity with no settled cause — which by this folder's usual
standard is a reason to discount it, not a reason to skip it.

**What momentum in individual assets then is.** Their headline is a *reduction*, not a new strategy:
individual-stock momentum is an aggregation of the autocorrelations of all the other factors, so
momentum "is not a distinct risk factor". Stock momentum profits when factor autocorrelations hold
and crashes when they break down. For this lab the reduction is the interesting half, because the
incumbent is a momentum book: **if the champion works because factors are autocorrelated, then a
factor-momentum construction is not a new family but a more direct expression of the family the lab
is already in.** Do not treat it as diversification without measuring the correlation.

**The decomposition, which this folder already half-owns.** They apply Lo–MacKinlay (1990) /
Lewellen (2002) to weights proportional to demeaned past factor returns and get three additive
sources for the *cross-sectional* version:

    E[π_XS] = (1/F)·Tr(Ω) − (1/F²)·1'Ω1 + σ²_μ

where `Ω = E[(r_{−t} − μ)(r_t − μ)']` is the autocovariance matrix of factor returns and `σ²_μ` is the
cross-sectional variance of the factors' unconditional mean returns. The three terms are (1) own
autocorrelation, (2) minus the cross-serial covariances, (3) the spread in unconditional means. **The
third term is the trap**: it is Conrad–Kaul, it contains no predictability at all, and it means a
cross-sectional "factor momentum" number can be entirely an artifact of some sorts simply being
better than others on average. A time-series construction (sign each factor against zero, not against
the cross-sectional median) does not collect that term, and Ehsani–Linnainmaa show the time-series
version **spans** the cross-sectional one while the reverse does not hold. This connects directly to
`notes/2026-09-05-contrarian-profit-decomposition.md` and
`notes/2026-09-05-cross-serial-correlation-as-restatement.md`, which are the same algebra applied to
assets rather than factors.

## Construction recipe

Ehsani–Linnainmaa's time-series version, which is the one to copy:

1. **Build `F` factor return series.** Monthly. Each is a long/short characteristic sort (they use
   published factors; a lab without a factor library builds its own sub-portfolios — see
   *Implementability*).
2. **Formation signal**: the factor's own cumulative return over the prior 12 months (`t−12 … t−1`),
   compared **to zero**, not to other factors. Sign the position: long the factor if positive, short
   if negative.
3. **Weighting across factors**: equal weight. The number of long and short factors floats (in their
   sample the strategy is long about eleven and short about six on average) — this is a feature, not
   a defect, and it is what makes the time-series version diversify better than the balanced
   cross-sectional one.
4. **Holding period: one month. This is not a free parameter.** Their appendix grid runs formation
   1/3/6/12/18/24 months against holding 1/3/6/12/18/24 months. Every formation length works at a
   one-month holding period, and **every one of them degrades as the holding period lengthens** —
   their stated reason is that a longer hold cannot rebalance away from a factor whose premium has
   turned. Formation length is robust; holding length is not.
5. **Exclude the momentum factor from the set** if you intend to compare against stock momentum,
   to avoid a mechanical correlation.

The Arnott et al. working paper adds one construction claim: the effect is **strongest at the
one-month formation horizon** (paralleling Moskowitz–Grinblatt on industries), and a factor-momentum
strategy on a *randomly chosen* subset of factors performs nearly as well as one on all of them — in
their sample even two randomly selected factors typically gives a significant result. If that holds,
the choice of factor set is not a tuning knob. **Fan et al. dispute exactly this** (below).

## Robustness evidence (qualitative only)

- **Present across factor families and in both the US and developed-ex-US sets** in
  Ehsani–Linnainmaa, at the level of a pooled regression and for most individual factors. They also
  report it at formation horizons from one month to two years.
- **The reexamination (Fan et al.) reaches a materially weaker verdict, and it is the one a
  long-only lab must read first.** On both a 22-factor and a 187-factor sample they find:
  - Factor momentum is **weak at the individual-factor level**. Only about a quarter of factors
    show significant own return continuation, and *those* factors dominate the whole strategy's
    profit. A strategy restricted to them beats the strategy on all of them — but that restriction
    is chosen after seeing which factors continued, so it is a selection, not a recipe.
  - **The factor-momentum strategy does not beat buy-and-hold of the same factors** — not on mean
    return and not on Sharpe ratio, in either sample. This is visible in Ehsani–Linnainmaa's own
    table too, if you read the row nobody quotes: the equal-weighted portfolio of all their factors
    has a **higher** Sharpe ratio than the long/short time-series factor-momentum spread. What is
    higher than the equal-weighted portfolio is the **winners-only leg**. (Orderings only; no
    numbers are recorded here.)
  - The single largest contributor to the profit in their sample is the betting-against-beta factor,
    and they attribute its continuation to its **rank-weighting scheme** rather than to its stock
    selection — every other factor in their set is value-weighted. They raise, without settling,
    the question of whether factor momentum is a property of the *weighting scheme*.
  - The Momentum group of factors shows a weak effect; the Value-Growth group a stronger one.
- **Replication status of the underlying object is asymmetric.** The autocorrelation regression is
  a simple, robust statistic and nobody disputes it. The *tradeable* claim — that signing factors on
  their own past return produces something you would want to own — is what Fan et al. contest, and
  no third party has adjudicated that contest. There is no Hou–Xue–Zhang or
  Jensen–Kelly–Pedersen row for "factor momentum" because it is a strategy over factors rather than
  a characteristic sort over stocks.
- Costs: Ehsani–Linnainmaa's main tables are gross. Fan et al.'s comparison is also gross, which
  makes their negative verdict *conservative* — a monthly-rebalanced timed book pays more than
  buy-and-hold of the same series.

## Implementability here

**The object exists in this repo, but it has to be manufactured.** This lab has no factor library.
The reachable analogue is: inside one candidate file, build `F` characteristic-sorted sub-portfolios
from daily OHLCV (e.g. 12-month price trend, 1-month reversal, Amihud illiquidity, range volatility,
volume shock, dollar-volume rank), compute each one's own realized monthly return series *causally*,
sign each on its own trailing 12-month (or 1-month) return, and hold the equal-weighted combination.
Every input is already in scope and `strategies/lib/features.py` supplies most of the sorts.

**The binding constraint, and it is the whole ballgame: long-only.** The literature's object is a
long/short spread. This repo cannot hold the short leg. That matters in two specific ways:

1. **The mechanism's clean form is unreachable.** "Sign the factor by its own past return" becomes
   "hold the factor's long leg when its spread was positive, and hold *cash or the equal-weighted
   universe* when it was negative." What you can express is the winners-only leg plus an exit — and
   the winners-only leg is, by the orderings above, the part with the better Sharpe ratio, so the
   long-only restriction bites less here than usual. Cross-reference
   `notes/2026-09-06-long-side-share-of-anomaly-profits.md` before assuming that transfers.
2. **A long-only sub-portfolio's return is mostly the market.** Its own autocorrelation is therefore
   mostly the market's own autocorrelation, and the factor-momentum literature's signal lives in the
   *spread*. Any implementation must form the signal on a **market-neutralised or
   universe-demeaned** sub-portfolio return (long-leg return minus equal-weighted universe return)
   even though the *book* is long-only. Skipping that step measures the wrong series.

**Then the comparison that decides it, and it should be run before any trial is spent.** Fan et al.'s
finding says the honest benchmark for a factor-momentum book is not the champion — it is
**buy-and-hold of the same sub-portfolios, equal-weighted, untimed**. If the timed version does not
beat the untimed one on the train split, the idea is dead and it cost nothing. That is a free screen
of exactly the kind this folder's top-ranked items are made of, and it is the first thing to do.

**Other pitfalls:**

- **Holding period is fixed at one month by the source.** This collides with the champion's
  overlapping-formation-tranche machinery, which deliberately lengthens the effective holding period
  (`experiments/learnings.md`: overlapping tranches are the strongest mechanism in the repo). The two
  mechanisms pull in opposite directions; do not assume the repo's tranche overlay improves a
  factor-momentum book, and if it is applied, report the un-overlaid version too.
- **Turnover.** Monthly re-signing of `F` sub-portfolios at 15 bps per side. The lab's own repeated
  finding is that outside `price-trend`, turnover differences dominate everything
  (`learnings.md`, 2026-08-29). Price the turnover before the Sharpe.
- **Factor count.** Arnott et al. say the set barely matters; Fan et al. say a quarter of the factors
  carry it. **Pre-register `F` and the list of sorts before looking at anything**, because "which
  sorts continued" is precisely the selection Fan et al. caught, and this lab has its own note on
  what a selected maximum is worth (`notes/2026-09-15-inference-on-winners-post-selection-estimation.md`).
- **Do not import the 0/1 indicator specification as though it were the only one.** It is a
  strategy-analogous specification, chosen for that reason; the continuous-slope version is in their
  appendix and gives the same sign.
- History requirement: 12 months of formation on top of whatever the sub-portfolio sorts need.

## Tensions with this lab's own results — stated, not smoothed over

1. **`experiments/learnings.md`: "Blending beats switching."** The lab has refuted regime-timing an
   allocation (SPY trend switch, drawdown braking, vol gates) and found always-on blends better.
   Factor momentum *is* a switching rule. The distinction that keeps it alive is that every refuted
   overlay timed the book on an **external state variable**, whereas factor momentum times each
   component on **its own past return** — a different object, and one the lab has never screened.
   That distinction is a hypothesis, not a finding; if a factor-momentum book loses, "blending beats
   switching" gets stronger and more general, which is itself a result worth having.
2. **The 2026-09-16 nightly found negative own autocorrelation in 20 of 21 group portfolios.** That
   measurement was daily own-autocorrelation of **long-only** group portfolios, whose returns are
   dominated by a common market component with a daily bounce. Factor momentum is monthly
   autocorrelation of a **spread**. The nightly result therefore does not refute this mechanism — but
   it is a warning that the demeaning step in *Implementability* point 2 is load-bearing, and it
   predicts that the un-demeaned version will read as a null or worse.
3. **Ehsani–Linnainmaa's own exception is the momentum factor**, whose own-return slope is ~zero in
   both their US and global sets. The incumbent here is a momentum book. Taken at face value, the
   mechanism says the one factor you should *not* expect to time on its own past return is the one
   this lab already owns.

## Related

- `notes/2026-09-05-contrarian-profit-decomposition.md`, `notes/2026-09-05-cross-serial-correlation-as-restatement.md`
  — the same Lo–MacKinlay decomposition applied to assets; the `σ²_μ` term is the shared warning.
- `notes/2026-09-06-long-side-share-of-anomaly-profits.md` — what survives dropping the short leg.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
  `notes/2026-09-08-stacked-regressions-nonnegative-weights.md` and
  `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` — the "untimed equal-weight benchmark"
  that Fan et al. say factor momentum fails to beat is exactly the forecast-combination baseline this
  folder already argues is hard to beat; and the blending note is where the long-only
  signal-versus-portfolio distinction is already worked out.
- `notes/2026-09-08-meta-labeling-and-the-value-of-a-filter.md` — a factor-momentum sign rule is a
  filter on an existing book, which is the object that note prices.
- `notes/2026-09-15-inference-on-winners-post-selection-estimation.md` — for the
  quarter-of-the-factors selection.
- `experiments/learnings.md` — "Blending beats switching"; "De-risking overlays on momentum reliably
  backfire"; the overlapping-tranche entries.
