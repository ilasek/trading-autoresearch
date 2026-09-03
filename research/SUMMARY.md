# External Research — Overall Summary

Maintained by the nightly learning agent (see `research/README.md` for rules). Updated after
every research session. Strategy sessions: read this file for idea input; every claim here is
**literature-derived, not verified on this repo's data** — treat it as hypothesis fodder, and
never copy performance expectations from it. Entries flagged `validation_overlap` or
`published_post_2018` carry soft lookahead risk; discount their novelty accordingly.

> ## ⚠ Program change — 2026-08-29 (human-authorised, read before planning a session)
>
> `program.md`'s family list was replaced. The seven price-trend families this folder was
> built around are now **one** family (`price-trend`, legacy and capped), and seven others
> were opened: `statistical-learning`, `liquidity-volume`, `range-variance`,
> `seasonality-calendar`, `lead-lag-spillover`, `statistical-arbitrage`,
> `portfolio-learning`. **Six of the eight had zero notes below.**
>
> **Status after session 17 (2026-08-30): every `program.md` family now has coverage.**
> Sessions 16 and 17 between them took all six cold opens — `statistical-learning`,
> `liquidity-volume`, `range-variance`, `seasonality-calendar` (sections 8–11, session 16) and
> `lead-lag-spillover`, `statistical-arbitrage` (sections 12–13, session 17). **`research/README.md`'s
> "at least one note from a family with no coverage" rule is now spent** — no family is cold, so the
> rule no longer binds and future sessions should be aimed by the open questions below instead.
>
> **Status after session 18 (2026-08-31): the last *partial* gap is closed too.**
> `portfolio-learning` — previously covered only by analogy through the ensemble and
> forecast-combination material — now has its own section 14 and its own note, taking the
> "stacking half" the 2026-08-30 open question asked for. **Every `program.md` family now has
> dedicated coverage.** One *sub*-mechanism named in `program.md` still has none:
> **ETF-versus-constituent lead-lag** (see the 2026-08-31 open question), and it is the standing
> target for the next session absent a reopened family.
>
> **Status after session 19 (2026-09-01): that sub-mechanism is closed too — by the lab, not by
> this folder.** `experiments/learnings.md` (2026-08-31) screened ETF-versus-constituent lead-lag
> on 9 SPDR sector ETFs plus VNQ across 8 groups and found the ETF's residual of the existing
> member-median control a null at every horizon pair; the reachable side of the one asymmetry
> with the right sign is itself a null. **`program.md` now has no named family or sub-mechanism
> without coverage.** Session 19 was therefore aimed by the lab's own results rather than by
> breadth, and future sessions should be too — see the 2026-09-01 open questions below.
>
> Two constraints in this file's coverage assumptions are now wrong:
>
> - Strategies receive **full daily OHLCV** (open, high, low, volume, dollar volume), not
>   just closes. Ideas previously filed as needing volume or the daily range — Amihud
>   illiquidity, range volatility estimators, volume shocks — are in scope.
> - **scikit-learn and scipy are installed**; learned models are implementable, subject to
>   walk-forward fitting.
>
> The conclusion recorded under *Open questions* — "no `program.md` family is now
> uncovered" and "the marginal value of another strategy-family survey is now low" — was
> true of the old list and is **false of the new one**. `research/README.md` now requires
> at least one note per session from a family with no coverage while any remain.
>
> Nothing below is retracted: the mechanisms, screens and anti-candidates recorded here
> remain findings about `price-trend`. They should not be carried into a new family by
> analogy without being re-measured there.

## Key findings by strategy family

### 1. Cross-sectional momentum

**The champion's overlapping-tranche construction is the textbook Jegadeesh–Titman
overlapping-portfolio scheme — but the lab's explanation of *why* it works goes beyond the
source.** Jegadeesh–Titman (1993) form decile portfolios on J-month past return and hold for
K months by running K formation vintages simultaneously, recommitting 1/K of capital per
month — structurally identical to the champion's six monthly tranches. In the paper this is a
*statistical estimator* chosen for observation count and test power; the paper makes no claim
that the overlapped book earns more than a single-vintage book. The repo's own temporal-breadth
result is therefore a finding beyond the literature, not an import from it, and this source
should not be cited as support for it. What the source does supply is a **principled bound on
tranche depth without sweeping K**: momentum profits partially reverse over the two years after
formation, so signal age much past ~12 months holds a reversing signal rather than a decayed
one. K=6 sits well inside that bound. Tier A, `validation_overlap: false`.
→ `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md`

**The "intermediate-horizon echo" does not survive outside the US, and is a low-prior idea on
this repo's global universe.** Novy-Marx (2012) finds a t−12..t−7 sort beats t−6..t−2 in US
data and concedes no theory explains the term structure. Goyal–Wahal (2015) run the same
decomposition across 37 non-US countries and in pooled developed+emerging and regional
portfolios and find no robust echo anywhere, diagnosing the US result as short-term-reversal
carryover contaminating the recent-horizon leg. Since this repo's ~145 instruments are a global
pool, the applicable prior is Goyal–Wahal's. The mechanism-level claim common to both, and the
one worth keeping, is the duller one: **skip the most recent month, because it carries reversal
rather than continuation** — which the champion's 6-1/12-1 composite already does. Both tier A
(A− on unverified citation counts), `validation_overlap: false`.
→ `notes/2026-08-17-momentum-horizon-echo.md`

**Momentum's crash-risk literature is long-short-specific, and reading it carefully *confirms*
the lab's refutation of basket-own-vol trimming rather than challenging it.** Barroso–Santa-Clara
(2015) scale momentum by the inverse of its own trailing 126-day realized volatility to a 12%
annualized target; Daniel–Moskowitz (2016) condition on a market-level panic state (long-horizon
negative market return *and* elevated market volatility) and scale so conditional volatility is
proportional to conditional Sharpe. Both operate on winners-minus-losers, and the crash they
manage is generated by the **short leg**: after a large decline, past losers are deeply
out-of-the-money levered equity whose payoff is call-like, so shorting them is shorting a call
and the loss arrives on the market rebound. A long-only book never owns that convexity, and its
realized volatility is dominated by plain market beta — so it spikes in melt-ups as well as
crashes, exactly as the lab measured. The papers' mechanism does not survive dropping the short
leg. Additional hard constraint: both scale *up* when volatility is low, which gross leverage
≤ 1.0 forbids, so a long-only implementation gets only the return-costing half of the scalar.
Tier A, `validation_overlap: false`.
→ `notes/2026-08-17-momentum-crash-risk-management.md`

**[Added 2026-08-28] The international literature builds a global momentum book by ranking
*within* markets and pooling afterwards — this repo ranks one pooled global cross-section, and
that is the session's one construction lead.** Three tier-1 sources, spanning three decades of
publication and four independent samples, assemble global momentum the same way and none of them
ranks a single global pool: Rouwenhorst (1998) forms deciles against same-country stocks;
Fama–French (2012) use **each region's own momentum breakpoints even when building global
portfolios**, computed from that region's big stocks; Chui–Titman–Wei (2010) pool within-country
winner portfolios into a country-neutral global book. Rouwenhorst is the one who reports what the
change buys, and the shape matters: country-neutral ranking lowers the winner-minus-loser **mean
only slightly**, but raises the two legs' correlation (≈0.74 → ≈0.88) and cuts the spread's
**volatility by about 40%**, sharply raising its t-statistic. So this is a variance mechanism, not
an alpha mechanism — a large share of an unconstrained international momentum book's risk is
country-specific and is removable by construction rather than by adding names. The confound has a
name and a citation (large country-specific components in international stock returns,
Heston–Rouwenhorst / Griffin–Karolyi), which is exactly what candidate #5's group-neutralisation
screen demands and exactly what the lab's refuted *sector*-neutral z-score lacked. All tier A,
`validation_overlap: false`.
→ `notes/2026-08-28-international-momentum-country-neutral.md`,
`notes/2026-08-28-local-versus-global-factor-construction.md`,
`notes/2026-08-28-individualism-cross-country-momentum.md`

**[Added 2026-08-28] Four independent sources now put this repo's universe in the size bucket
where momentum is weakest, and one of them cannot distinguish it from zero.** Fama–French find
the winner-minus-loser spread larger for small stocks in every region they study except Japan,
with the difference exceeding two standard errors everywhere except Japan — and in their global
portfolios the **big-stock spread carries a t-statistic near 1.4**, i.e. pooled across 23
developed markets over two decades, large-cap momentum is not statistically distinguishable from
zero. Rouwenhorst's largest size group earns roughly half the smallest group's spread;
Chui–Titman–Wei report momentum profits negatively related to firm size across 41 countries;
Asness–Moskowitz–Pedersen state their results are conservative *because* their universe is the
largest names covering 90% of market cap. This does not contradict the lab's own measurements —
a concentrated long-only magnitude-weighted book on a survivorship-conditioned universe is a
different object from a value-weighted long-short factor — but it fixes where the external prior
should sit: **the bottom of the published range, not the middle.** Tier A, `validation_overlap:
false`. → `notes/2026-08-28-local-versus-global-factor-construction.md`,
`notes/2026-08-28-international-momentum-country-neutral.md`

**[Added 2026-08-28] Geography does not diversify a momentum book, and this is the outside
version of a result the lab has already measured.** Asness–Moskowitz–Pedersen find the average
single-market stock momentum strategy correlates ≈0.65 with the average momentum strategy in
*other* stock markets (and ≈0.37 with momentum in non-stock asset classes), a co-movement
*stronger* than that of passive exposures to the same markets — the strategies are market-neutral
within each class, so it cannot be the assets moving together. Consequence for a global pooled
book: adding names across regions raises nominal breadth `N` but adds little independent risk,
which is the fundamental-law point in published numbers and is consistent with the lab's own
finding that widening the basket from 25/15 to 35/20 left maximum drawdown essentially unchanged.
The source of the common factor is only partially explained — macro links are modest, funding
liquidity risk loads positively on momentum and negatively on value but accounts for a small
fraction of the premia by the authors' own accounting. Tier A, `validation_overlap: false`.
→ `notes/2026-08-28-value-momentum-everywhere-global-comovement.md`

**[Added 2026-08-28] The repo's magnitude weighting has its first outside construction match, and
the match is the *ordinal* version the lab converged on independently.**
Asness–Moskowitz–Pedersen weight securities by **cross-sectional rank of the signal** minus the
average rank, stating that ranks blunt outliers (raw-signal weights are similar and slightly
better), and report that such signal-weighted books beat coarse tercile-sort spreads for two
reasons: the weight is a positive linear function of the signal rather than a three-way
classification, and more names carry nonzero weight so the book is better diversified. That is
the lab's largest single measured construction gain and the lab's later refinement of it
(`learnings.md`: the information is "more ordinal than cardinal") arrived at from outside. The
boundary: their portfolio is dollar-neutral long-short, so rank-minus-mean produces negative
weights; the long-only analogue is the champion's and the equivalence remains the lab's
inference. Tier A, `validation_overlap: false`.
→ `notes/2026-08-28-value-momentum-everywhere-global-comovement.md`

### 2. Time-series momentum / trend following

**The best-known result in this family is contested in its own literature, and the version this
repo could actually build is not the version the evidence is about — so the lab's three refuted
trend overlays are consistent with the literature, not contradicted by it.** Moskowitz–Ooi–
Pedersen (2012, JFE) established time-series momentum — an instrument's *own* past return
predicting its *own* future return — on 58 futures across four asset classes: sign of the
trailing 12-month excess return, positions scaled by inverse own ex-ante volatility, portfolio
scaled to constant target vol. Hurst–Ooi–Pedersen (2017, JPM) extend it across a century-plus
sample and report the effect present in every decade and across varied macro environments, and
add the multi-horizon construction (1-, 3- and 12-month lookbacks run together rather than one
chosen). **But** Huang–Li–Wang–Zhou (2020, JFE) find asset-by-asset regressions show little
evidence of the effect in or out of sample; the large pooled-regression t-statistic falls below
both parametric and non-parametric bootstrap critical values; and — the finding that matters
most to an implementer — the TSM strategy's profitability is **virtually the same as a strategy
built on the historical sample mean, which requires no predictability at all**. Four structural
obstacles then stand between even the contested effect and this repo: the evidence is
**long-short** and the "crisis alpha" payoff comes entirely from the short leg (the second
documented case of a momentum mechanism living in the short leg); the evidence is **multi-asset
futures**, where most of the appeal is diversification across ~60 weakly-correlated trends,
whereas a long-only equity/ETF book is close to one repeated bet on a single common factor;
**inverse-vol sizing is intrinsic to the construction** and this lab has refuted it twice; and
gross leverage ≤ 1.0 makes the vol-targeting one-sided. Net: **family 2 is low-prior on this
universe** — not closed, but any candidate must state which of the four obstacles it escapes and
must not lean on MOP/HOP citation weight as if the evidence transferred. Evidence base tier A;
the *effect* is best described as contested, most recent peer-reviewed word sceptical.
`validation_overlap: false` for all three.
→ `notes/2026-08-17-time-series-momentum-evidence-and-replication.md`

**A fifth obstacle, from portfolio accounting rather than from replication statistics, and it
is the cleanest of the five.** Goyal–Jegadeesh (2018, RFS) show the difference between a
time-series and a cross-sectional rule is *the benchmark the past return is measured against*:
CS compares each asset to the **cross-sectional mean** (so the book is zero-net-investment by
construction), TS compares it to **zero** (so the book carries a time-varying net long
position). Algebraically `TS ≈ CS + NetLong_t × index return`, and that extra term splits into
a **risk-premium** piece (being net long on average) and a **market-timing** piece
(`cov(NetLong_t, index return)`). Empirically, on seven decades of non-micro-cap US stocks,
**the entire TS-versus-CS performance gap is that term** — give the CS strategy the same net
long position and the two are about equal across ranking/holding horizons from 1 to 60 months.
At long ranking horizons virtually all of it is the *static* risk premium; the market-timing
covariance is the smaller and weaker piece, and is larger only at short horizons. The
consequence for this repo is direct: a long-only trend overlay ("hold if own trailing return
positive, else cash") is a TS rule whose net long varies between 0 and 1, so against a
**fully-invested** cross-sectional book it cannot capture the risk-premium half at all — it can
only give some of it up — and everything it could add is the weak market-timing term, at the
horizon where that term is weakest. That is a mechanism-level prediction that long-only trend
overlays should cost return and add little, which is exactly what the lab measured three times.
Tier A, `validation_overlap: false`.
→ `notes/2026-08-17-cross-sectional-vs-time-series-construction.md`

**Most named trend rules are the same object, and there is a closed-form way to prove it before
spending a trial.** Zakamulin shows every moving-average-based indicator — crossovers,
price-minus-MA, envelopes, plain momentum — can be rewritten as a **weighted average of past
price changes**, so a rule's performance depends *exclusively on the shape of its return-
weighting function*, not on its name or framing. The practical yield is a free triage rule: write
a proposed trend/MA signal as its weight vector over past returns and compare shapes to what has
already been tested; near-identical shapes mean a re-parameterisation, not a new idea. Hard
boundary: the identity holds for *linear* filters only, so it says nothing about buffers,
hysteresis bands, thresholds or caps — which is exactly where the champion's live edge sits.
Tier B (the identity is algebra and cannot decay; the empirical window-robustness claims layered
on it are single-market and were unverifiable this session). `validation_overlap: false`.
→ `notes/2026-08-17-moving-average-rules-anatomy.md`

### 3. Vol targeting / risk parity

**The family's headline result is real in-sample, does not generalise across strategies, and
its investor-relevant version failed replication — and separately, the leverage cap here
removes the half of the rule that earns the money.** Moreira–Muir (2017, JF) scale a
portfolio's exposure by the inverse of its own **previous month's realized variance** (sum of
squared daily returns within the month, no parameter estimation), with a single constant
chosen so the managed book has the same unconditional volatility as the unmanaged one. The
mechanism is an asymmetry between two forecastability facts: variance is highly forecastable
at short horizons and expected return is not, so the mean-variance weight `μ/σ²` moves with
`1/σ²`. A corollary worth carrying: **the gain is a bet on the dispersion of the variance
process** — with constant volatility the managed and unmanaged books are identical and the
alpha is exactly zero. Cederburg–O'Doherty–Wang–Yan (2020, JFE) extend the test from 9 factors
to **103 equity strategies** and land three blows, none of which is "the data disagree":
volatility management *degrades and improves performance at about the same frequency* across
the 103 (the wins concentrate in the market, momentum and betting-against-beta factors — i.e.
exactly the ones prior papers had already singled out); the spanning-regression alpha implies a
combination portfolio whose weights are estimated **over the full sample** and is therefore not
a real-time strategy; and reasonable expanding-window versions earn **lower** certainty
equivalents and Sharpe ratios than simply holding the unmanaged portfolio, because the spanning
parameters are structurally unstable. The decisive implementability fact for this repo is
distributional, not performance-based: the implied position `c/σ̂²` has a **median near 1× but
a 99th percentile of roughly 4.5–8.6×** across the nine factors. Gross leverage ≤ 1.0 leaves
only `min(c/σ̂², 1)` — the de-risking half, which the source itself shows earns less. Tier A,
`validation_overlap: false`; the replication is `published_post_2018: true`.
→ `notes/2026-08-17-volatility-timing-managed-portfolios.md`

**The risk-parity half is now covered, and the theory hands the lab a free pre-trial screen
that reproduces both of its inverse-vol refutations — while correcting the lab's diagnosis of
why they failed.** Maillard–Roncalli–Teiletche derive the equal-risk-contribution (ERC)
portfolio — weights such that every component contributes the same share of total risk — in
closed form for the cases that matter. Four results. (a) For **two components, ERC is exactly
inverse-volatility and does not depend on their correlation at all**; so the lab's
`mom_etf_volweighted_blend` was not a crude approximation of risk parity, it *was* risk parity,
and there is no better-specified version of that trade waiting to be built. (b) With more
components, inverse-vol equals ERC **only under a constant correlation matrix**; in general
`x_i ∝ 1/β_i`, where `β_i` is the component's beta *to the portfolio*, so the scheme penalises a
component for high volatility **or** high correlation with the rest of the book. (c)
Consequently the honest generalisation of the lab's "unequal diversification" learning is a
statement about portfolio beta: any risk-balancing scheme overweights whatever is least
correlated with the book, and a diversified sleeve is least correlated almost by definition
regardless of what it earns — so moving from naive inverse-vol to *correct* ERC would push
further in the refuted direction, not back. (d) The decisive one: **ERC is the maximum-Sharpe
portfolio only under constant correlation AND equal Sharpe ratios across components**, with the
authors stating the converse explicitly. The lab's two sleeves differ by roughly a factor of two
in Sharpe, so its own theory predicted the loss. Separately, the ordering `σ_mv ≤ σ_erc ≤ σ_1/N`
means the family's product is a *lower-volatility* book, whose practitioner appeal depends on
levering it back up — the same one-sided-scalar truncation that gross leverage ≤ 1.0 already
imposes on the vol-targeting half. Tier A on the theory (closed-form algebra, cannot decay),
tier B on the paper's three illustrative backtests, which report ERC beating 1/N and are in
tension with both DeMiguel–Garlappi–Uppal and the lab's own sleeve result — a tension the
optimality condition in (d) resolves without anyone having to be wrong about the data.
`validation_overlap: false`.
→ `notes/2026-08-18-risk-parity-equal-risk-contribution.md`

_With this, **both halves of family 3 are covered and both verdicts are negative** — the
vol-targeting half on leverage, non-generality and real-time failure; the risk-parity half on a
provable optimality condition the lab's sleeves do not meet._

### 4. Short-term mean reversion

**The short-term reversal premium is the market-making spread seen from the other side, which
closes this family here for a better reason than the turnover gate.** Nagel (2012, RFS) shows
short-horizon reversal returns are a proxy for the **return to liquidity provision**: an
uninformed order pushes price away from fundamentals, the market-making sector is paid to
absorb the inventory, and price reverts as it is worked off. Two consequences. (a) The premium
is strongly time-varying and **predictable by the VIX**, rising faster than the strategy's own
volatility so conditional Sharpe ratios rise with stress — a liquidity-*supply* story
(constrained intermediaries demand more to warehouse risk), not a demand story. (b) It is not
confined to single stocks: a reversal strategy built from **value-weighted industry
portfolios**, which earns essentially nothing unconditionally, earns high returns and Sharpe
ratios when VIX is high — liquidity providers are paid for absorbing common, industry-level
order imbalances too. Lo–MacKinlay (1990, RFS) supply the necessary correction to the naive
reading: contrarian profits do **not** require overreaction and are largely driven by
**cross-autocovariances** (lead-lag relations between stocks), so a contrarian book is partly
harvesting cross-sectional lead-lag rather than own-stock mean reversion. Lehmann (1990, QJE)
is the base weekly result. The implementability verdict is a *sign* problem, not a magnitude
one: **the premium is compensation for supplying liquidity, and any implementation paying 15
bps/side is demanding it** — taking the losing side of the exact trade that pays. No band, no
slower cadence and no cost-mitigation technique fixes that. This is fully consistent with the
lab's two empirical reversal refutations. Tier A, `validation_overlap: false`.
→ `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`

### 5. Low-vol / quality tilts

**The gap `learnings.md` named is now filled from both sides, and the family should be treated
as closed rather than merely uncovered.** `learnings.md` left family 5 open pending "a genuinely
different vol construction (e.g. sector-neutralized, not raw trailing)". The literature's
dedicated treatment of exactly that construction is Asness–Frazzini–Pedersen (2014, FAJ), who
build betting-against-beta (BAB) factors **within each industry** and aggregate across them.
They find the industry-neutral version beats both the ungrouped BAB and a pure
across-industry BAB, positive in **every one of 49 US industries** and most of 70 global ones,
with low or negative value loadings — a real rebuttal of "low-risk is repackaged value". But the
construction is unavailable here for a reason that is the mechanism itself: **BAB's low-beta leg
is levered up to beta 1**, and the economic story is that the premium exists *because* harvesting
it requires the leverage most investors lack. An unlevered long-only low-beta basket is not a
weakened BAB — it is the asset BAB says the constrained investor already owns and which is
therefore cheap and low-returning. Worse for the specific gap: the paper's own explanation for
the industry-neutral variant being the *best* one is that it requires **more** notional per unit
of risk. Gross leverage ≤ 1.0 removes exactly what the recommended construction depends on.
Tier A, `validation_overlap: false`.
→ `notes/2026-08-18-low-risk-investing-industry-neutral.md`

**The skeptical literature then puts the premium in the part of the market this repo does not
trade, which is why the lab's two low-vol refutations were predictable in advance.** Two
Novy-Marx papers, one of them a tier-1 published replication challenge, attack from different
directions and converge. *Understanding Defensive Equity* shows volatility is strongly
negatively predicted by **operating profitability** (more strongly than by size), so a
volatility sort is an unintended profitability/size/valuation sort; defensive strategies
underweight unprofitable small growth, which is precisely the corner standard models misprice.
The conditional result is the one that decides it here: **defensive performance is concentrated
in small growth, and in large value the sign reverses — aggressive stocks significantly
outperform defensive ones.** *Betting Against Betting Against Beta* (Novy-Marx–Velikov, JFE)
reproduces BAB and then varies one construction choice at a time, finding three non-standard
procedures do the work: rank weighting is a back door to **equal weighting**, hedging-by-levering
is a back door to hedging with the **equal-weighted** market, and the FP beta is not a regression
slope but the identity `β_FP = [(σ_i,1y/σ_i,5y)/(σ_mkt,1y/σ_mkt,5y)] · β_i,5y` — a beta multiplied
by a short-to-long volatility ratio, whose time-series bias is argued to generate the paper's own
"beta compression" evidence. The size consequence: **for each dollar invested, BAB commits about
$1.05 to stocks in the bottom 1% of market capitalisation**, costs run around 60 bps/month, and
net of costs no significant five-factor alpha survives — what remains is compensation for
profitability and investment exposures. Both substitute causes are unavailable here: the repo
holds ~145 large, liquid global names, and has no fundamentals. A direct contradiction is
recorded rather than smoothed: AFP report the effect present in large caps, Novy-Marx reports it
reversing in large value. The disagreement is about the only end of the market this repo trades,
and even AFP's own size split shows large-cap alphas weaker in every column. Tier A;
`validation_overlap: false` for both (samples 1968–2015 and 1968–2017); `published_post_2018: true`
for the JFE replication.
→ `notes/2026-08-18-defensive-equity-replication-and-construction.md`

### 6. Regime switching
_Partially covered, now by two specifications. Daniel–Moskowitz's panic-state indicator (a
conjunction of long-horizon negative market return and elevated market volatility) remains the
one literature-grounded regime rule reviewed; ranked low — see candidate list. Added this
session: **VIX as a predictor of the liquidity-provision premium** (Nagel), which is the one
regime variable in anything read here that is documented to predict a *strategy's* expected
return rather than the market's. It is unusable as-is — the strategy whose return it predicts
is the one this repo structurally cannot trade — but it is the cleanest example of the shape a
sound regime signal takes: an external state variable predicting a specific premium, not a
trailing statistic of the book being de-risked.
→ `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`,
`notes/2026-08-17-momentum-crash-risk-management.md`_

### 7. Combinations / ensembles

**Averaging beats selecting, and the reason is estimation error in the selection — the same law
that governs portfolio weights, one level up.** Timmermann's handbook chapter gives three
distinct reasons a combination of forecasts of *one target* beats its components: error
diversification (imperfectly correlated errors partly cancel), robustness to structural breaks
(averaging over models of differing adaptability beats committing to one, and requires nobody to
detect the break), and mitigation of unknown-form misspecification. Smith–Wallis then explain the
**forecast combination puzzle** — why the simple arithmetic mean beats combinations using
*estimated* optimal weights — as finite-sample error in estimating the combining weights, worst
precisely when the true weights are near-equal; they recommend ignoring forecast-error
covariances when weighting. Rapach–Strauss–Zhou supply the finance instance: against the
Welch–Goyal benchmark where individual predictive regressions fail out-of-sample, combining the
individual forecasts delivers consistent out-of-sample gains, beats the kitchen-sink regression
that pools all predictors into one model, and works substantially by **shrinking toward the
benchmark** — i.e. combination is a variance-reduction technique applied to an estimator, not a
source of new signal. This directly explains a lab result: fixed-ratio blending beating
inverse-vol reweighting between sleeves, twice, is the combination puzzle exactly. Tier A,
`validation_overlap: false`.
→ `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`

**The lab's unexplained temporal-breadth result now has a named mechanism in the literature, and
it is an accuracy claim.** Pesaran–Timmermann (2007) show that when a model's parameters may
have shifted at an unknown date, choosing the estimation window is a **bias–variance trade-off**:
a short post-break window is nearly unbiased but high-variance, a longer window reaching back
before the break lowers estimation variance at the cost of stale-regime bias — and when the
objective is out-of-sample MSFE, **it is often optimal to include pre-break data**. Because the
optimal window depends on the break's unknown date and size, they and Pesaran–Pick–Pranovich
propose averaging rather than selecting: compute the forecast over a **range of estimation
windows and average the results** ("AveW"), whose advertised property is that no break-date or
break-size estimate is needed. The champion's six overlapping monthly formation tranches are
structurally this method — the same model at different estimation vintages, equal-weighted, held
simultaneously. This fills the gap flagged last session: Jegadeesh–Titman framed overlapping
portfolios as a *statistical estimator*, Hoffstein et al. framed tranching as *dispersion
reduction around an unchanged mean*, and neither claimed the tranched book earns more, whereas
**this literature does make an accuracy claim** (lower MSFE than any single-window forecast),
which is a claim about the centre. It does not prove the lab's result — the objective functions
differ and the break analogy is the lab's, not the authors' — but the result is no longer
mechanism-less. It also reframes the pruning diagnostic: masking each tranche to the currently-
endorsed held-set *is* the short-post-break window, which this literature predicts should lose.
Tier A, `validation_overlap: false`.
→ `notes/2026-08-17-averaging-over-estimation-windows.md`

**The lab's temporal-breadth result now has a *third* mechanism, and this one is the
unconditional accuracy claim the folder has been looking for since session 2 — plus a free
screen for when averaging can do nothing at all.** Breiman's bagging result is one line of
algebra: for a predictor `φ(x, L)` built by running a fixed procedure on a training set, the
aggregated predictor `φ_A(x) = E_L φ(x, L)` satisfies `e_A ≤ e` — **expected squared
prediction error always falls**, and the size of the fall is exactly the *variance of the
predictor across training sets*. Not dispersion around an unchanged mean: the centre moves.
Two conditions decide whether the effect is large or zero, and both are checkable on paper.
(a) **Instability.** If perturbing the data barely changes the fit, the two sides of the
inequality are nearly equal and aggregation buys nothing — Breiman's own control is bagging a
nearest-neighbour classifier, which produced *identical* error rates on six datasets, a literal
no-op. The unstable procedure he names as the canonical case is **subset selection**, where
"the variables are competing for inclusion and small changes in the data can cause large
changes" — structurally the champion's buffered top-N membership rule, where instruments
compete for slots. (b) **Nonlinearity.** Buja–Stuetzle's independent U-statistic analysis
adds the sharper version: **bagging leaves additive statistics unchanged**; the entire effect
lives in interaction terms of order ≥ 2. So averaging over vintages can only move a
construction to the extent that construction is nonlinear in the data — which is the general
form of the lab's own `#41`/`#42` finding that collapsing two lookbacks into one score *before*
selecting throws away the part that pays. Their analysis also supplies the honest counterweight:
in their framework squared plug-in bias *always* rises and variance only *usually* falls, MSE
improves only for large enough resamples, and the crossover is real — bagging a stable
procedure is mildly harmful, not neutral. Practical corollary the lab can use without a trial:
replicate counts saturate fast (most of Breiman's gain by ~10, nothing after ~25), so any future
proposal to deepen the tranche stack should pre-register a small effect. The one gap that must
not be glossed: this is an **MSE claim about a predictor**, not about portfolio return — the
bridge to realised Sharpe is the lab's inference. Tier A, `validation_overlap: false`.
→ `notes/2026-08-19-bagging-averaging-unstable-predictors.md`

**The same question answered in portfolio vocabulary, and it says the lab has been naming its
own mechanism with the wrong noun.** Grinold's fundamental law, `IR ≈ IC · √BR`, has been
revised three times, each revision relaxing an unrealistic assumption and each time lowering
the predicted IR. The generalisation that nests them (Ding–Martin, with the derivation readable
in the author's earlier working paper) is `IR = mean(IC) / sqrt(σ_IC² + φ/N)`, `φ ≥ 1`. Grinold
is the `σ_IC = 0` case, where breadth compounds without limit; Qian–Hua's **strategy risk**
limit is the `N → ∞` case, `IR → mean(IC)/σ_IC` — **an absolute ceiling no amount of breadth
can breach.** The consequence for this repo is a decomposition, not a strategy: adding *names*
at one date raises `N`, a `√N` lever already saturated on a ~145-instrument universe, whereas
averaging the same selection procedure across weakly-correlated *formation dates* averages
several draws of the realised IC and lowers **`σ_IC`** — the term that dominates once `N` is
moderate. The lab measured exactly that asymmetry (nominal breadth widening was a no-op;
decorrelated formation dates were the repo's strongest mechanism) and had no account of it;
here the two are different terms of one identity. It also gives the existing rank-correlation
gate a target rather than a threshold — `σ_IC` of a `K`-vintage average falls with the average
*pairwise* correlation of the vintages, and not at all if they are perfectly correlated. Third,
the long-only constraint acquires a number: Clarke–de Silva–Thorley's **transfer coefficient**,
`IR ≈ TC · IC · √BR`, with `TC` typically **0.3–0.8** under real constraints and long-only named
among the culprits — a multiplicative leak, categorically milder than the two cases where a
mechanism lives entirely in the short leg. Two warnings attach. The framework is
*benchmark-relative* (residual returns, tracking error), so **no IR figure here is comparable
to the repo's total-Sharpe gate** and "IR above 1.5 is rare" is not a comment on the champion.
And measuring an IC **scores returns**, so it is not covered by the lab's free holdings-only
diagnostic exemption. Mapping vintages to IC draws is the lab's inference; neither source
discusses tranching. Tier A on the algebra, B on the published paper's unread empirical study;
`validation_overlap: false`.
→ `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`

**And the boundary condition on the folder's own top principle: when estimated averaging
weights are provably right.** Hansen's Mallows model averaging chooses weights by minimising
an (asymptotically unbiased) estimate of the average squared error, and is asymptotically
optimal in its class — an apparent counterexample to "averaging beats selecting *because*
selection would have to be estimated". It is not a counterexample; it is a list of conditions.
Estimated weights win when there is an unbiased in-sample estimate of the loss actually being
minimised, the components form a nested ordered ladder, errors are conditionally homoskedastic
(the author states optimality fails without this), and the sample is large relative to the
weight count (smoothed-BIC beats MMA at small `n`). This repo fails all four — its loss is a
deflated Sharpe whose in-sample estimate is upward-biased *by construction*, returns are
heteroskedastic, its components are not one nested ladder, and the sample is short — so equal
weights remain correct here **for four stated reasons rather than as a taboo**. Two further
yields. Averaging beat the *infeasible optimal* single model in many parameterisations, so
"which vintage/window is best?" is the **wrong question**, not merely an unanswerable one — a
stronger claim than the folder previously recorded. And averaging over a *nested* ladder is
algebraically **shrinkage**: with orthogonal regressors the `j`th coefficient is multiplied by
`Σ_{m≥j} w_m`, monotonically downweighting what only the longest window sees. The lab's four
lookback windows are nested, so `#42` has a definite weighting shape over past returns — the
object candidate #3's closed-form triage rule operates on. Offered as a lens, not a result:
the windows are not orthogonal, and the lab averages *portfolios*, whose selection step is
nonlinear. Tier A, `validation_overlap: false`.
→ `notes/2026-08-19-model-averaging-mallows-weights.md`

---

## The families opened on 2026-08-29 (first coverage, session 16)

Sections 1–7 above are the seven families that `program.md` collapsed into the single legacy
`price-trend` family on 2026-08-29. The four sections below are the first coverage of the
newly-opened families. Everything in them is literature-derived and **unmeasured on this repo's
data**; `CLAUDE.md` explicitly forbids carrying `learnings.md`'s price-trend constants into these
families by analogy, and the same applies in reverse — nothing below has been re-measured here.

### 8. `statistical-learning`

**The reference comparative study of ML for cross-sectional return prediction ranks methods, and
the ranking is not the interesting part — the diagnostics behind it are.** Gu–Kelly–Xiu (2020,
RFS) run thirteen estimators from OLS to five-layer neural nets on one US dataset with one
out-of-sample protocol. Three results transfer, and one warning does.

*(i) The nonlinear gain is interactions, not curvature.* A generalized linear model with a
group-lasso penalty over **spline expansions of individual features** — arbitrary univariate
nonlinearity, no interactions — fails to improve on the purely linear models, despite selecting
more features than elastic net. The entire advantage of trees and neural networks therefore traces
to *predictor interactions*. A Monte Carlo confirms the direction in both senses: linear methods
dominate on simulated linear-additive data, trees and nets dominate on simulated interactive data.
**Corollary the lab can use before writing a candidate: if a proposed feature set has no
interaction story, a penalised linear model is the right estimator and a heavier learner is
predicted not to help.** *(ii) Dimension reduction beats variable selection* — PCR and PLS
outperform elastic net, which the authors read as characteristics being "partially redundant and
fundamentally noisy": combining them into low-dimension components averages out noise. That is the
folder's own averaging-beats-selecting result arriving from a third direction, now stated about
**features** rather than models. *(iii) Shallow beats deep* — three hidden layers is the peak, four
and five do not improve on it, attributed to the dearth of data and low signal-to-noise in asset
pricing. Also: **Huber loss beats squared loss** for every method where both were run, and the
fitted models are small — random forests grow trees one to five levels deep, boosted ensembles use
30–50 of the 920 available covariates. Tier A, `validation_overlap: false`,
`published_post_2018: true`. → `notes/2026-08-29-machine-learning-cross-section-comparative.md`

**All thirteen methods agree on a small dominant feature set, and its top three groups are three
`program.md` families in order.** Two independent importance measures correlate 84–98% within each
model, and the rank ordering of the top third of characteristics is stable across thirty successive
training samples. The order: **price trends** (five of the top seven — short-term reversal,
12-month momentum, momentum change, industry momentum, max return, long-term reversal), then
**liquidity** (turnover and turnover volatility, log market equity, dollar volume, Amihud `ILLIQ`,
zero-trading days, bid-ask spread), then **risk** (total and idiosyncratic volatility, beta, beta
squared), then valuation/fundamentals — the group this repo cannot express at all. Penalised linear
and dimension-reduction models are "highly skewed toward momentum and reversal"; trees and neural
nets are "more democratic". **This is the mechanism behind the lab's own observed result that
feeding a learner the incumbent's lookbacks reproduces the incumbent at higher correlation and lower
Sharpe** — a linear learner loads on trend because that is where the marginal signal is. If a
`statistical-learning` candidate exists to supply a *decorrelated* leg, the price-trend features have
to be excluded or orthogonalised deliberately.

**Two things the paper does not do, and the second is load-bearing here.** It does not model
transaction costs anywhere — every economic-gain figure in it is gross, with no turnover accounting
— and it does not ask its models for stable holdings. Predicting returns well and holding a
tradeable book are different objectives; the folder's dynamic-trading and parametric-portfolio notes
are the bridge. The lab's own first scout in this family paid roughly a third of its margin over the
equal-weight floor to a monthly full-cross-section re-rank, which is the same failure this paper
would never have detected. Its **protocol**, by contrast, transfers cleanly and cheaply: cross-
sectional rank of every feature mapped to `[-1,1]` as the only preprocessing; a fixed
train/validation/test split with **no cross-validation, to preserve temporal ordering**; refit
**annually** with an expanding training window and a rolling validation block; out-of-sample R²
benchmarked against **zero** rather than the historical mean (which the authors put at ~3pp of
inflation); Diebold–Mariano tests rather than eyeballed R² gaps, under whose Bonferroni-adjusted
version the neural nets are only *marginally* significant over penalised linear models.

**[2026-09-01] A second, independent route to "few predictors matter" — and it explains, for the
first time with an outside source, *why this universe in particular keeps producing nulls*.**
Freyberger–Neuhierl–Weber (RFS, Tier 1 venue, graded **B** here for being single-market and
modelling **no transaction costs** on a monthly extreme-decile book) rank each of 36
characteristics cross-sectionally, fit expected return as an **additive quadratic spline in the
ranks**, and select with an **adaptive group LASSO** (one group per characteristic, so it is in or
out as a unit). Of 36, 15 survive conditioning on the others across all stocks. **The
load-bearing table is the size cut**: restricting to progressively larger firms, characteristics
drop out in a specific order — **idiosyncratic volatility** goes first, then **lagged turnover and
momentum**, and at the largest size cut **only seven characteristics retain incremental power**,
of which only *closeness to the 52-week high*, *past-return predictors* and *standardized
unexplained volume* are computable without fundamentals. This is outside corroboration of three
things the lab measured on its own universe and recorded as puzzling: the `liquidity-volume`
volume nulls, the repeated failure of volatility-level sorts, and the difficulty of finding
anything outside `price-trend`. **A ~145-name large-cap universe is where this source predicts
most characteristics stop working.** The four survivors stable across every sample half, knot
count and size cut are size, closeness to the 52-week high, short-term reversal and standardized
unexplained volume. `validation_overlap: false`; `published_post_2018: true`.
→ `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md`

**The functional-form result is sharper than "nonlinearities matter" and it names the one learned
candidate this lab should build.** In their out-of-sample design the nonparametric model selected
**eight** characteristics and the linear model **twenty-one**, and the smaller model won. Two
diagnostics pin the cause: handing the *nonparametric* estimator the linear model's 21
characteristics improves out-of-sample performance, while handing the *linear* estimator the
nonparametric model's 8 produces a result identical to its own 21. **The gain is in the functional
form, not the characteristic count** — the linear model's extra characteristics are it overfitting
in sample. Against `learnings.md`'s standing rule that a learned candidate earns a trial only when
asked for something a sort cannot express, this names the something: **the shape of one
characteristic's relation to return**. A monotone rank sort is itself a functional-form assumption
and a probably-wrong one; a spline in the rank of a *single* characteristic is the minimal
departure, has a handful of parameters, and is walk-forward fittable. That is a far narrower
learned candidate than the ridge feature block the lab already ruled out.

**[2026-09-03] "How few predictors matter" has been asked in the wrong space, and the correction is
this family's most consequential single result.** Kozak–Nagel–Santosh (JFE, Tier **A**, 776
citations) show that **sparsity in the space of characteristics fails** — an L1 selection of a few
characteristics-based factors performs poorly out of sample, and even a dual L1+L2 estimator cannot
compress dozens of predictors into a handful without losing explanatory power, because there is not
enough redundancy among them. **Sparsity in the space of principal components of those same factor
returns succeeds**: a model containing a small number of *high-variance* PCs, with the L2 penalty at
its optimum, delivers the best out-of-sample cross-sectional fit, and zeroing the low-variance PCs
costs little. The asymmetry is economic, not numerical: absence of near-arbitrage implies a factor
earning a large premium must itself be a major source of variance or load on one, so most of the
SDF's variance should sit in high-eigenvalue PCs — whereas nothing implies that a few *observable
characteristics* should suffice. `validation_overlap: false`; `published_post_2018: true`.
→ `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`

**Two mechanics from the same source that transfer even if its headline does not.** (a) The
estimator is `b̂ = (Σ + γI)⁻¹ μ̄` — ridge applied to the mapping from **covariances to mean returns**,
not to a return-on-features regression, so the shrinkage is **unequal across PC directions by
construction** (low-eigenvalue directions are shrunk hardest). This is structurally different from a
uniform ridge on a feature panel, which is what `learnings.md` (2026-08-29) actually tested when its
penalised combiner "reproduced its own best input, worse" — that result is evidence about
ridge-on-features, not about this estimator, and the design rule drawn from it is aimed at a
different failure. (b) The penalty has an **economic unit**: γ maps one-to-one to `κ`, the root
expected maximum squared Sharpe ratio the prior considers plausible, which converts a
hyperparameter this repo cannot legally cross-validate into a stated prior. A third, smaller point:
they estimate Σ from daily returns and treat it as known, finding that **uncertainty in means
dominates uncertainty in covariances** — the shrinkage that matters is on expected returns.
**Caveat that must travel with the recipe:** their K-fold CV splits the whole sample and is
explicitly upward-biased; it is illegal here and must be replaced by walk-forward selection or an a
priori γ.

**[2026-09-03] And the deflationary half, which decides whether this family is worth trials at all
on this universe.** Avramov–Cheng–Metzker (Management Science, Tier **A**, 201 citations) take four
published learned methods — a deep network (GKX), a no-arbitrage network (CPZ), the linear IPCA, and
a conditional autoencoder — reproduce their headline results, then impose economic restrictions.
Excluding **microcaps** cuts the deep learners' risk-adjusted payoff by roughly half to
three-quarters; excluding **financially distressed** firms removes most of what is left, after which
none of the deep methods is significant at the 5% level. Traditional anomaly sorts deteriorate in
similar proportion, so this is about where cross-sectional predictability lives, not about neural
networks specifically. **The load-bearing result for this repo is the second one: IPCA, the linear
method, deteriorates only modestly on the cheap-to-trade subsamples.** The *incremental value of
nonlinearity* is what is concentrated in difficult-to-value, difficult-to-arbitrage names. A third
constraint binds independently: all four signals turn over at least ~87% and up to ~150% a month,
and the implied **break-even one-way cost** falls by roughly half once microcaps are excluded,
landing at or below plausible cost estimates. `validation_overlap: false`; `published_post_2018: true`.
→ `notes/2026-09-03-machine-learning-economic-restrictions.md`

**Two results in that paper cut the other way and should not be dropped when it is quoted.** Unlike
most individual anomalies — whose payoff is concentrated in the **short** leg — the learned signals
earn their risk-adjusted return in the **long** leg, with the short leg insignificant; that is
exactly the half a `max_leverage = 1.0` book can hold. And decomposing against an industry
benchmark, the **intra-industry** version (rank within peer group) outperforms both the
unconditional and the industry-rotation versions: the content is in **peer-relative** ranking, which
is a free rebuild of any existing leg and a different question from the regional-neutralisation
bracket the lab closed (that was about *weights*, this is about the *scoring benchmark*).

### 9. `liquidity-volume`

**Amihud's `ILLIQ` replicates cleanly, decays out of sample, and — this is the finding the lab
should act on — is not better than substantially simpler measures built from the same two data
series.** The *Critical Finance Review* commissioned a replication of Amihud (2002) and published
the author's reply in the same issue, a level of evidence almost nothing else in this folder has.
Harris–Amato reproduce the original "quantitatively very close and qualitatively the same" using
current CRSP data and Amihud's own filters. Applying the same methods after the original sample
ends, the cross-sectional relation is much weaker and **only the *unexpected* component of
illiquidity remains related to index returns**, where the original found both expected and
unexpected components priced; an independent citation reports a declining liquidity premium over
four decades. Amihud's reply does not contest any of this: he builds a volatility-controlled
illiquid-minus-liquid factor over a longer span and reports it positive and significant, **lower
after his 2002 paper but still positive and significant**. Tier A as a cluster,
`validation_overlap: false`. → `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`

**The horserace result, and why it is a cheap next trial rather than a footnote.** Against
alternatives computable from the same daily returns and volume — the *ratio of mean |return| to
mean dollar volume*, mean |return| alone, inverse mean volume, **log mean dollar volume**, and the
Kyle–Obizhaeva invariance measure — `ILLIQ` has among the **lowest** average R² in every subgroup
and both specifications, though its t-statistic is among the highest. The best proxies by R² are
the invariance measure and **log average dollar volume**. Further: the ratio of means is ~92%
correlated with `ILLIQ` and delivers essentially identical coefficients, and decomposing `ILLIQ`
into the ratio of means plus the residual shows almost all explanatory power sits in the ratio of
means — i.e. **the day-by-day pairing of |return| with volume, which is the entire motivation for
the measure's functional form, contributes nothing.** Taken alone, mean absolute return enters with
a negative, often insignificant coefficient that the authors call "simply a re-identification of
the low-volatility effect".

**The construction detail this lab most needs, and it is one line.** `ILLIQ` and return volatility
are positively correlated by construction — the numerator *is* an absolute return — so an
unconditional `ILLIQ` sort is partly a volatility sort. Amihud's own factor therefore **sorts
volatility first**: three trailing-volatility terciles, five `ILLIQ` quintiles within each,
capitalisation-weighted, and the spread taken across the volatility buckets. The lab has run an
unconditional single sort on trailing-quarter `ILLIQ` (`FAMILY_LEAD`, the most decorrelated
non-trivial result on the board) and has **separately refuted low-vol tilts on this universe** —
so the confound is consequential in both directions and the existing scout cannot tell which way it
runs. Also transferable: Amihud's day-level screens exist to stop near-zero-volume days dominating
the average (drop days with volume under 100 shares, drop the single largest daily `ILLIQ` each
year, require >200 valid days), which matters more here than in CRSP because **this repo's volume
panel is not forward-filled and is NaN on foreign holidays**.

**[Added 2026-08-31] The premium in `ILLIQ` is not in the price-impact numerator, and the volume
functional that carries it is not one the lab has tested.** Lou–Shu (2017, *RFS*, Tier A, read in
full; `validation_overlap: false`, `published_post_2018: false`) decompose the measure directly —
the paper `SUMMARY.md` has flagged as the natural follow-up since 2026-08-29. Their structural
observation is that `ILLIQ`'s denominator has ~100× cross-sectional dispersion against the
numerator's ~2×, so a "constant" measure `A_C = mean_d(1 / dollar_volume_d)` — the numerator
deleted — correlates 0.90 with the original, is priced about as strongly, and **the part of
`ILLIQ` orthogonal to `A_C` is not priced at all**. Since the |return| numerator is exactly what
makes the ratio a price-impact construct, the premium is not compensation for price impact. They
close the "then `A_C` is a better illiquidity proxy" escape too: high-frequency price-impact and
spread benchmarks correlate 0.74 with `ILLIQ` itself but only **0.35** with the component that
does the pricing, and decomposing `ILLIQ` into a fitted transaction-cost part and an orthogonal
residual leaves **the non-cost part priced and the cost part not**. Four conditioning tests then
favour mispricing over liquidity: the volume premium is absent in January while the liquidity
benchmarks are priced *only* in January; it is not larger after episodes of scarce aggregate
liquidity; it is larger after high sentiment **with the difference on the short leg**; and it is
concentrated in the three-day earnings-announcement window.
→ `notes/2026-08-31-amihud-volume-component-decomposition.md`

**This contradicts the lab's own 2026-08-30 measurement, and the escape hatch is a functional
form.** `learnings.md` concludes that "the family's live content is `ILLIQ`'s **price-impact
numerator** and not trading activity under any normalisation, which answers the Lou–Shu question
without the paper." Lou–Shu answer the opposite way on a five-decade cross-section. The clause
that does not survive is **"under any normalisation"**: the lab tested log *average* dollar volume
and relative volume, both functions of the mean of volume, while Lou–Shu's priced object is the
mean of the **reciprocal** — a Jensen-different statistic dominated by an instrument's *quietest*
days rather than its typical ones. See candidate #58: one free rank correlation decides which
reading holds, and the lab's own standard — "a null that passes its own identifying test rules out
the mechanism, not the measurement" — is what makes the distinction worth the check. Two further
discounts point the other way and belong in the same breath: the mispricing reading puts the
effect in hard-to-arbitrage small illiquid names (this universe is the opposite tail, and the
short-leg concentration is unreachable long-only), and **cross-market volume is not comparable** —
Lou–Shu drop an entire exchange from a single-country sample over a volume-reporting convention,
which is a strong prior that a raw volume sort across 15 regions is substantially a venue sort.

### 10. `range-variance`

**This family is a measurement result, not a premium, and the measurement gain is large, analytical
and free.** For a driftless Brownian motion the log range has **about one-quarter the standard
deviation of the log absolute return** as an estimator of log volatility (0.29 vs 1.11), and the log
range is **almost exactly Gaussian** (skewness 0.17, kurtosis 2.80) where the log absolute return is
badly not (−1.53, 6.93). These are theorems about Brownian motion — they do not decay, are not
subject to publication bias, and carry no sample. The range is also robust to bid-ask bounce in a
way high-frequency realised volatility is not: the spread adds at most one spread to high-minus-low
however many trades occurred. Tier A for the analytical results, B for the empirical estimator
ranking. `validation_overlap: false`.
→ `notes/2026-08-29-range-based-volatility-estimators.md`

**The estimator ladder, with efficiencies relative to the squared return (=1):** Parkinson 4.9,
Rogers–Satchell 6.0 at zero drift (>2 at any drift), Garman–Klass 7.4, Meilijson 7.7. Formulas, in
terms of `c = ln(C) − ln(O)`, `h = ln(H) − ln(O)`, `l = ln(L) − ln(O)` — **all measured from the
open, not the previous close**: `σ²_P = (h−l)²/(4 ln 2)`; `σ²_GK = 0.5(h−l)² − (2 ln 2 − 1)c²`;
`σ²_RS = h(h−c) + l(l−c)`. Garman–Klass reads as the minimum-variance combination of the Parkinson
estimator and the simple squared return. Zero drift is a very good approximation at the daily
frequency (mean daily return ≪ daily standard deviation) and stops being one at annual horizons.

**Being a good variance estimator does not make an estimator a good *denominator*, and only one of
them is.** Molnár standardises returns by each estimator: Parkinson is mechanically correlated with
the return it standardises (`|r|/σ_P` is bounded above by `sqrt(4 ln 2) ≈ 1.665`, correlation 0.79),
giving a **bimodal, tailless** distribution; Rogers–Satchell is catastrophic (standardised kurtosis
≈ 124 — its drift-generality works against it when the drift is in fact zero); Meilijson has
Parkinson's defect mildly. **Garman–Klass is the only one appropriate for standardising returns**,
because subtracting the squared return from the Parkinson term cancels most of the correlation with
`|r|` (0.79 → 0.36). Every construction that divides by a volatility estimate — vol targeting,
inverse-vol weighting, feature normalisation — is therefore an instruction to use Garman–Klass and
not the two more obvious choices. Two further facts: all these estimators are **unbiased for the
variance but not for the standard deviation** (the square root introduces a bias, which mostly
cancels cross-sectionally and mostly does not in a time-series vol target); and **all of them see
only trading-hours volatility**, missing the overnight gap entirely — a systematic, time-zone-
correlated under-estimate on a 15-region universe, and a confound for any cross-sectional
comparison of range volatility across regions.

**[2026-09-01] The family's first *asymmetric* mechanism, and it is the one direction in which
this universe's survivorship artifact works *for* the hypothesis instead of against it.** All
eight mechanisms the lab has screened here are functionals of the **width** of the daily return
distribution — Garman–Klass level, vol-of-vol, close-to-close/GK ratio, close-location value, the
overnight/intraday split, the within-name de-levelled range. `learnings.md`'s 2026-08-31 verdict
was "the level *is* the survivorship artifact; remove the level and nothing is left".
Bali–Cakici–Whitelaw (JFE, Tier A, 1756 citations) sort on a different functional of the same
bars: the **upper tail only** — `MAX(N)`, the average of the `N` largest daily returns of the past
month, with `MAX(5)` the authors' preferred and more powerful version. The story is lottery
demand: under-diversified investors over-pay for small probabilities of large payoffs, so
lottery-like stocks are over-priced and subsequently underperform. The prediction is therefore
**negative** — high `MAX` earns less — where the artifact makes high-volatility names here look
+19.4%/yr *better* on train. **A positive finding would be running against the artifact, which is
the opposite of every other sort this family has tried.** `validation_overlap: false`;
`published_post_2018: false`. → `notes/2026-09-01-max-lottery-extreme-positive-returns.md`

**The identifying test is free, it is two numbers, and it is exactly the test the lab's own
range-lottery screen did not run.** Volatility is symmetric; lottery demand is not. So the
authors sort on `MIN` (the negative of the month's smallest daily return), which is nearly as
correlated with volatility as `MAX` is (~0.75–0.76 with total and idiosyncratic volatility in
their sample): a volatility story predicts `MAX` and `MIN` carry the **same** sign, a
skewness-preference story predicts **opposite** signs, and the data side with the asymmetric one.
`learnings.md`'s 2026-08-29 screen found a range-based lottery proxy at −7.95%/yr, t = −4.30 and
dismissed it as "just low-vol" — note that this is a **significant effect with the predicted
sign**, dismissed on collinearity rather than on its own statistic, and that a *range* proxy is a
width measure, i.e. precisely the confounded object the `MIN` test exists to separate. The
sources do not contradict the lab's measurement; they say the lab measured the confounded
quantity and then used the confound to dismiss it. Same shape as #58's narrowing, and it should
be resolved the same way. The paper's other structural claim is that including `MAX` **reverses**
the idiosyncratic-volatility puzzle — conditional on `MAX`, idiosyncratic risk is *rewarded* —
which the cross-country companion (Cheon–Lee, *Management Science*, abstract only) restates as
the puzzle existing "only for stocks with high MAX", and which the `statistical-learning` note
above independently corroborates from the size-cut side.

**Two honest discounts, both large.** The authors state the effect "is certainly concentrated
among smaller stocks" — it survives dropping low-priced shares, restricting to NYSE-listed names
and excluding the bottom NYSE size quintile, but its magnitude and significance rise
monotonically as capitalisation falls, so a large-cap universe sees the weakest end of it. And
the cross-country evidence is real but partial: **26 of 42 countries**. One favourable asymmetry
against those: unlike `statistical-arbitrage`'s residual reversion and the ETF lead-lag, the
**profitable leg here is the reachable one** — the low-`MAX` decile is the high-return leg, so a
long-only book holds it directly, and the authors' own "would require shorting" caveat is about
capturing the full spread, not about which end pays.

### 11. `seasonality-calendar`

**A permanent cross-sectional seasonal, with a sign pattern sharp enough to be a genuine
prediction.** Heston–Sadka (2008, JFE): sorting stocks on their average return in the **annual
lags only** (t−12, t−24, … t−240) produces a positive winner-minus-loser spread at **every** annual
horizon out to twenty years, while sorting on the **non-annual** months of the same intervals
produces a **negative** spread at every horizon. The familiar Jegadeesh–Titman-then-DeBondt–Thaler
shape is a *contiguous-months* result; a periodic seasonal of the opposite sign is superimposed on
it. The pattern survives controls for size, industry, earnings-announcement months, dividend and
ex-dividend months, calendar effects and fiscal year, and the decile spreads have approximately
**zero loadings on the market and the Fama–French three factors** — the authors state plainly that
conventional systematic risk does not explain it, and do not claim to know what does. The
international companion reports it in Canada, Japan and twelve European countries, surviving size,
beta and value controls under **either global or local** risk factors, and — the most relevant line
for this lab — finds the strategies **not highly correlated across countries**. Tier A for the US
paper; the international companion is recorded from its **published abstract only** (`oa_status`
closed) and is tier B as recorded. `validation_overlap: false`.
→ `notes/2026-08-29-same-calendar-month-seasonality.md`

**The authors model the cost problem themselves, and it is the finding to lead with.** They draw
the distinction explicitly: momentum and contrarian strategies rebalance only part of the portfolio
every few months, "while seasonal strategies require rebalancing the **entire portfolio every
month**". Their own conclusion is that it "may not be generally profitable to incur round-trip
transaction costs" for a gain of this size, and that short-lived fluctuations in monthly expected
return "may not form an effective foundation for a long-term investment strategy" — noting further
that the periods where the raw effect is largest are periods where costs are documented to be
higher (they cite the same Korajczyk–Sadka this folder covers). `program.md` independently names the
turnover gate as the thing to watch in this family; a tier-1 source reaches the same conclusion from
the other direction, before the lab has to spend a trial discovering it. **Their constructive
suggestion is not to trade the signal but to use it as an execution overlay**: "it is relatively
simple to postpone the sale or purchase of a particular stock if it has a large positive or negative
expected return over the next month" — which adds no turnover, it *re-times* existing turnover, and
is structurally an asymmetric signal-conditional no-trade band rather than the symmetric one the
folder already holds.

**One construction fact that is about `price-trend`, not this family.** Within the one-year
interval, sorting on the **12-month lagged month alone** delivers better return-per-unit-risk than
sorting on all twelve months of the past year. Most of what a conventional twelve-month momentum
sort captures is available from the single month twelve months back — a claim about the composition
of the signal the champion is built on, checkable at no cost.

**[2026-09-02] The successor paper says the identifying test this lab pre-registered was the wrong
one, and supplies the right one.** Keloharju–Linnainmaa–Nyberg (2016, JF, Tier A) is the direct
descendant of Heston–Sadka, and its central claim is that the seasonal component of expected
returns **overwhelms** the unconditional cross-sectional component rather than opposing it in sign.
That predicts the lab's 2026-08-29 screen failure — annual +15.7%/yr and non-annual +12.8%/yr, both
positive — as the normal appearance of a universe with large persistent mean-return differences,
not as the absence of a seasonal. Their discriminating test is a fixed-effects contrast: the
annual-lag pattern survives **stock** fixed effects and disappears under **stock-calendar-month**
fixed effects, which is what rules out "stocks repeat their own past shocks" and rules in "each
stock has its own twelve monthly expected returns". The economic content is that a sort on past
same-calendar-month returns is a **noisy proxy for a bundle of characteristics whose premiums are
seasonal** — size, dividend-to-price and industry are named — so individual stocks *aggregate*
seasonalities across factors, which is why the effect looks strong in single names and weak in any
one factor. At least **two-thirds** of it is common-factor-borne (the strategy's variance is ~5x
what pure idiosyncratic risk would give), from which the authors draw the operational rule that
**seasonal strategies must stay exposed to systematic risk, because hedging it removes the
seasonality with it**. Construction: average same-calendar-month return over the prior **20 years**,
cross-sectionally demeaned, decile sorts re-formed monthly. Two facts make this the family's best
remaining lead here: seasonality strategies on **well-diversified characteristic- and
country-sorted portfolios** are about as profitable as single-stock ones (this repo has 42 ETFs
across 15 regions, and an ETF-level version dodges the survivorship objection), and seasonality
strategies in different corners of the market are **near-uncorrelated with each other** (≈0.17
between the small-stock and high-dividend-yield versions; negligible across asset classes), which
is a measured source of the orthogonal leg the live `portfolio-learning` question needs. Recorded
tension inside the cluster: the same authors' 2021 JFE companion (Tier 1, abstract only, 24
citations) reports **seasonal reversals** that sum to approximately zero over the calendar year and
reads them as temporary mispricing rather than risk — which cuts against the 2016 paper's own
factor framing. `validation_overlap: false`.
→ `notes/2026-09-02-return-seasonalities-common-factors.md`

**[2026-09-02] The `calendar` half now has a mechanism with a timing restriction it did not choose
— and one free number that settles the lab's structural closure either way.** Ogden (1990, JF,
Tier 1, abstract only) attributes the turn-of-the-month pattern to the **standardised monthly
payment cycle**: wages, pensions, dividends and interest cluster at the month boundary, releasing
investable cash. Etula–Rinne–Suominen–Vaittinen (2020, RFS, Tier 1, read in full) test the
institutional side and decompose the cycle into three windows with **different predicted signs**:
**T−8 to T−4 liquidity-motivated selling (negative)**, T−3 to T+3 positive reversal, T+4 to T+8
negative reversal. The window locations are **pinned by settlement conventions rather than fitted
to returns** — their identifying evidence is that the 1-day-settlement Treasury market's pressure
window sits later (T−2) than the 3-day equity market's (T−4), with corporate bonds hybrid. The
effect is stronger in countries with larger mutual-fund sectors, and reversals are significant in
22 of the countries studied. **This does not overturn `learnings.md`'s 2026-09-01 structural
closure of this half; it identifies one window the closing screen did not test.** That screen used
(before = 1, after = 3) — the source's *positive-reversal* window — and pooled the source's negative
pressure window into an undifferentiated complement measured at +11% to +14%/yr. The closure's own
instruction was "check the complement window's sign", and the sign of **T−8 to T−4 alone** is
unmeasured. It is free, and it either meets the closure's binding condition for a narrow overlay or
closes the family for good. `published_post_2018: true` for the RFS paper.
→ `notes/2026-09-02-turn-of-month-payment-cycle.md`

---

### 12. `lead-lag-spillover`

**The mechanism is gradual information diffusion, and it has an identifying restriction the lab
cannot run.** Hong–Torous–Valkanov (2007, JFE, Tier 1) build on Merton (1987) and Hong–Stein
(1999): attention and information-processing capacity are scarce, investors specialise, so news
originating in one asset market reaches investors in another only with a lag. Their model yields
two properties worth more than the empirical result. First, **own-serial correlation can be zero
while cross-serial correlation is non-zero** — each market's investors condition efficiently on
their own information and fail only on the other market's — so the signature of the mechanism is
cross-predictability that is *not* a restatement of own-lag predictability, and a construction
without an own-lag control has not tested it. Second, **the sign of the cross-prediction follows the
covariance of the two assets' payoffs and is not required to be positive**; their own leaders
include both signs. A long-only construction of the form "leader up ⇒ buy the laggard" is assuming a
sign the theory does not supply. Their identifying test is that an asset leads the market only if
it carries information about *fundamentals*, verified by relating each group's ability to predict
the market to its ability to predict industrial production — **which needs a macro series this repo
does not have and may not fetch.** A lead-lag candidate here therefore runs the symptom test
without the identification test, and should say so.
`validation_overlap: false`, `published_post_2018: false`.
→ `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md`

**The count, not the coefficient, is the object — and the count is not stable.** HTV handle multiple
testing by simulation: with 34 regressions one expects ≈3.4 significant leaders at the 10% level
under the null, and the test is whether the observed count is in the tail. That discipline is the
transferable part, and it is mandatory here rather than optional: 15 regions give 210 ordered pairs,
so a per-pair t-statistic means nothing. The count itself, however, is where the literature
disagrees. The authors' own posted replication package (2014, unrefereed, with two independent
replications of the main table) extends the sample by roughly a decade and reports predictability
persisting for a **smaller** subset of the original leaders, with rolling regressions showing a
stable core plus subsample-only leaders — a decay-and-instability finding from the authors
themselves. Tse (2015, *Journal of Empirical Finance*, recorded **from its published abstract
only** — closed access) extends the same decade with a finer 48-industry partition and reports only
a handful of leaders survive, that the original sample's results weaken after data revisions, that
there is evidence of the *reverse* direction, and reads the whole as consistent with market
efficiency. **This folder does not adjudicate that.** Record it as: the qualitative mechanism has
multi-market support (HTV replicate the count and the fundamentals relation in eight developed
markets on an independent vendor, seven of eight for the latter); the specific claim "N groups lead"
is sensitive to data vintage and partition choice.

**The construction that is actually implementable comes from the daily/weekly end of the family,
and it brings a per-instrument statistic that costs nothing.** Chordia–Swaminathan (2000, JF, Tier
A) show that **trading volume determines who leads and who lags**, over and above size: high-volume
portfolios lead low-volume portfolios of the same size, the asymmetry survives inside the largest
size quartile (so non-trading is not the explanation) and survives controlling for the follower's
own autocorrelation (so it is not a repackaged portfolio autocorrelation). The mechanism is
differential **speed of adjustment to common information**. Two things carry over. (a) Their volume
measure is **turnover** — shares traded ÷ shares outstanding — chosen because raw and dollar volume
correlate ≈0.78 with size while turnover correlates ≈0.15; the sort is designed to *not* be a size
ranking. This repo has no shares-outstanding panel, so turnover is not computable, and substituting
dollar volume reintroduces exactly the size ranking the design removes — which is the mechanism
behind the lab's measured null on log average dollar volume. The causal substitutes are relative
volume (each name's volume over its own trailing average, so the size level cancels) or (b) the
direct measure: **`DELAY`**, a logit of the ratio of summed lagged Dimson betas to the
contemporaneous beta, `DELAY = 1/(1+exp(−Σ₁₅βₖ/β₀))`, higher = slower adjustment. It needs **closes
only**, is the thing the volume sort proxies *for*, and nothing in this lab has used it. Note also
their diagnostic warning: **own-autocorrelation is not a valid speed-of-adjustment measure** (a
stock reacting to today's *and* yesterday's news shows positive own-autocorrelation while being the
faster adjuster); the screen must be a cross-quantity. `validation_overlap: false`.
→ `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md`

**Two cost verdicts, both from the sources' own authors, and they point the same way.** HTV report
their timing rule improves risk-adjusted return before costs and immediately caution that adding
industry information roughly **doubles the number of switches**; they do not model costs.
Chordia–Swaminathan state plainly that it is not clear the patterns are tradeable because
transaction costs are likely to overwhelm the profits — and offer that as the explanation for why
the effect is not arbitraged away. **Add this repo's own confound**: 15 regions with non-overlapping
sessions and unhedged USD conversion guarantee a mechanical daily "US leads Asia" cross-correlation
that is a time-zone artifact, not speed of adjustment. Any daily region-level lead-lag result here
should be assumed to be that artifact until a weekly version reproduces it. The engine's one-day
execution lag also eats most of a daily effect while costing a monthly one almost nothing — so the
family's two ends have opposite implementability profiles, and the middle (weekly) is where a
candidate has to live if it lives anywhere.

**[Added 2026-08-31] The grouping variable is the hypothesis, not a nuisance parameter — and the
grouping this family's strongest source endorses is one this repo probably cannot build.** Hou
(2007, *RFS*, Tier A on venue and 617 citations, but **recorded from its published abstract
only** — closed access, no repository mirror, SSRN bot-challenged) argues that slow diffusion of
**industry** information is the leading cause of the lead-lag effect, and that the big-firm →
small-firm effect is *predominantly an intra-industry phenomenon*, robust to the rival
determinants. Two further claims from the same abstract are directly usable: the effect is
**driven by sluggish adjustment to negative information** (a sign asymmetry, free to add to any
lead-lag construction), and it is stronger in **small, less competitive and neglected industries**
— the limited-attention signature. Its microfoundation is post-earnings-announcement drift in
small firms following big firms' earnings *within the same industry*.
→ `notes/2026-08-31-intra-industry-lead-lag-grouping.md`

**What this does to the lab's existing lead-lag results is discount them, not extend them.** If
pooled big→small predictability is largely an unmodelled industry channel wearing a size label,
then the lab's region→region and group→market scouts are the same manoeuvre with a *geographic*
partition substituted for the industry one, and nothing in this source suggests geography proxies
for industry — Hou's cross-sectional evidence attaches the effect to industry attributes
(competitiveness, neglect) that have no regional analogue. This repo has no sector taxonomy (no
fundamentals), so the free precondition is candidate #59's instrument-list check: if some of the
42 ETFs are sector funds, an industry-ish grouping is buildable from prices alone; if they are all
region and broad-market funds, **Hou's construction is unreachable here and that is a
family-scoping fact to record rather than to work around by analogy**. Either way the lab should
state which claim a failed lead-lag scout is evidence about — the mechanism, or the grouping.
Note the double discount even in the good case: the effect lives in small, neglected, thinly
covered industries, and ~145 large globally-known instruments sample the neglect-free end of every
one of those sorts. The **ETF-versus-constituent** sub-mechanism `program.md` names remains
uncovered after this session.

---

### 13. `statistical-arbitrage`

**The family's central empirical claim is about the factor count, and it is non-monotone.**
Avellaneda–Lee (2010, *Quantitative Finance*, Tier B — heavily cited, peer-reviewed, but single
market, single sample, no known independent replication) trade the residual of each stock against a
small factor set, modelled as an Ornstein–Uhlenbeck process. Their structural finding is that
whether mean reversion is *measurable* depends on how much systematic variation is removed first,
and the relationship has an interior optimum: remove too little (one market factor) and residuals
carry leftover common variation — slow estimated reversion, high residual volatility, worst results
of any configuration they test; remove too much (a 75% explained-variance target) and what remains
is noise whose reversion is real but smaller than costs, which they report as a **steady loss** and
name "noise trading". Their optimum on a US large-cap universe is ~15 factors or a ~55%
explained-variance target. `validation_overlap: false`, `published_post_2018: false`.
→ `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md`

**This is in direct tension with the lab's own declined screen, and the tension is worth stating
rather than resolving.** `learnings.md` records that residualising 5-day reversal made it
monotonically *worse* on the train split — raw beat one-factor beat PCA k=3 and k=5 — and the family
was declined on that basis. The source agrees about the low end (one factor is its worst
configuration too, for a stated reason) and the lab's tested range k ∈ {1,3,5} sits **entirely
inside the region this source also found worst**, with the reported optimum untested. Three reasons
that is not a refutation of the lab's result: (i) 15 factors on ~140 instruments is a very different
factor-to-name ratio than on many hundreds, so the noise-trading failure arrives at a lower count
here and the *explained-variance target*, not the count, is the transferable parameter; (ii) the two
measurements are of different objects — the lab measured an **unconditional cross-sectional IC**,
the source trades a **conditional excursion** (only names more than 1.25 equilibrium standard
deviations from equilibrium *and* whose estimated reversion speed clears a filter), and an
unconditional IC can be null while the conditional tail trade is not; (iii) the source pays 5 bps
per trade against this repo's 15, and its characteristic reversion time is on the order of a week —
the configuration it reports *losing money on* is the regime a 3×-more-expensive book starts in.

**What survives the long-only constraint — the question `SUMMARY.md` scoped this family to.** Every
position in the source is a stock against βᵢ dollars of its factors: the residual is what is traded,
and the factor leg is what makes it *tradeable* rather than merely *measurable*. A long-only book
capped at gross 1.0 holds only the cheap side, so what survives is **not** a market-neutral residual
portfolio but a long book whose cross-sectional weights are tilted by a residual signal, with
returns dominated by the market exposure it cannot remove. **Removing factor structure from the
signal does not remove it from the book** — which is the mechanism-level account of the lab's own
measurement that five long-only family leads from five different mechanisms correlate 0.75–0.85 with
each other. The honest framing for any candidate here is a *selection* question ("does a residual
s-score rank names better than a raw price rank?"), not a decorrelation claim.

**Four pieces port cleanly and cheaply, independent of whether the family is ever traded.** (a) The
**s-score**, `(X − m)/σ_eq` with `σ_eq = σ/√(2κ)` — a dimensionless, causal, better-specified
reversal signal than "trailing n-day return", whatever the factor count. (b) A **κ-filter**: only
take a mean-reversion bet where the estimated reversion time is short relative to the estimation
window (they require τ < half the window). This is a falsifiable admissibility condition and nothing
in this lab's reversal work has used one. (c) The **number of components needed for a fixed variance
share** is a free regime statistic for cross-sectional correlation concentration, computable from
the same eigendecomposition — `range-variance`-adjacent, costs nothing. (d) **Trading-time volume
rescaling**: `R̃ = R × ⟨δV⟩/ΔV` over a ~10-day trailing volume window, which shrinks moves made on
heavy volume and inflates those made on light volume — economically, *do not fade a move that came
with heavy trading*. It is a return *transformation* rather than a sort, which is a use of the
volume panel the lab has not tried, and it is testable on any reversal signal without the rest of
the apparatus. Two explicit **anti-candidates** from the same source: adding an estimated drift term
(equivalently a 60-day moving-average slope, a built-in momentum overlay) is reported to add
essentially nothing to a residual-reversion signal; and the "bang-bang" all-or-nothing sizing that
wins there is a turnover machine under a 15 bps/side cost model.

**[2026-09-03] The family has a second, much cheaper construction, and it is the one that tests the
half of the above tension the lab has not touched.** Gatev–Goetzmann–Rouwenhorst's **distance
method** (RFS, Tier 1 venue; graded **B** here — single-market in the version read, and the
cost-and-decay reexamination is second-hand) trades one stock against **one matched partner**, with
no factor model, no covariance estimation and no parameter beyond two window lengths and a trigger.
Partners are chosen by minimising the **sum of squared deviations between normalised cumulative
total-return series** over a 12-month formation window; a position opens when the pair's normalised
prices diverge by more than **two formation-window standard deviations** and closes at the **next
crossing**, over a 6-month trading window, with a **one-day execution delay** on every open and
close and **six overlapping monthly tranches** running concurrently. Three of those are already this
repo's conventions. `validation_overlap: false`; `published_post_2018: false`.
→ `notes/2026-09-03-pairs-trading-distance-method.md`

**What the source establishes beyond "it made money", which is the part that transfers.** (a) It is
**not** the bid-ask bounce and **not** one-day reversal: the one-day delay is imposed throughout and
monthly returns are *positively* autocorrelated, so the payoff accrues gradually over a holding
period measured in weeks. (b) It is **conditional** — most pairs hold nothing most of the time,
opening on the order of a couple of round trips per six-month window — which is precisely the
"conditional excursion versus unconditional IC" distinction this section already flagged as the gap
in the lab's declined screen, now reachable with a construction that estimates nothing. (c) It is
**not factor-neutral in practice**: market exposure is insignificant (partners comove by
construction) but size, value, default-premium and term-premium exposures are positive and
significant, so a matched pair removes the market and leaves the rest — and a long-only book, which
can hold only the cheap leg, keeps all of it. The honest framing is again a **selection** question
("does a partner-relative spread rank names better than an unconditional price rank?"), which is the
same diagnosis this section reached from Avellaneda–Lee by a different route. (d) The authors run a
**random-within-sector-partner bootstrap** as a placebo — the exact control `learnings.md`
(2026-09-02) concluded the lab had never run and most needed.

**The independent reexamination, recorded second-hand and flagged as such.** Do–Faff (FAJ 2010;
Journal of Financial Research 2012) re-run the rules over a longer sample with commissions, market
impact and shorting fees modelled. From their abstracts, verbatim: pairs trading "remains
profitable, albeit at much more modest levels", with what survives concentrated "among portfolios of
well-matched pairs that are formed within refined industry groups", and it "exhibits a lower risk
and lower return profile than a short-term reversal strategy that sorts stocks relative to their
industry peers". They also document **secular decay** — the McLean–Pontiff pattern for a heavily
published top-journal rule. Two directional lessons: **finer grouping in the matching step is where
the cost-surviving profit sits**, and the effect should be expected smaller than the original
literature implies. Neither Do–Faff paper could be read in full (SSRN 403; both publisher pages
closed), so nothing above rests on their internals.

---

### 14. `portfolio-learning`

**[First dedicated coverage 2026-08-31. This closes the last partial family gap — every
`program.md` family now has a section of its own.]** The folder's ensemble and
forecast-combination material (family 7, plus the bagging and model-averaging notes) covered this
family by analogy; what it never covered is the distinction that turns out to be the whole
question under a long-only constraint.

**There are two ways to combine signals into one book, they are not close substitutes when the
book is long-only, and the lab has measured exactly one of them.** Fitzgibbons–Friedman–Pomorski–
Serban (2017, *Journal of Investing*, Tier 3 practitioner, read in full) separate **portfolio
blending** — build one long-only portfolio per signal, then hold a weighted mix of the portfolios
— from **signal blending / integration** — combine the signals into one per-instrument score
first, then run portfolio construction *once*. The structural claim, which is arithmetic rather
than empirics and is not disputed by the rebuttal below: **the mix's return is bounded between its
components' by construction; the integrated book carries no such bound and can beat all of them.**
The mechanism is the long-only constraint itself. An unconstrained book expresses a view long *and
short*; a long-only book can only underweight, so most of its risk comes from the long side and
the short half of the view is discarded. A stand-alone signal-A portfolio has no way to use "this
name is bad on signal B" — so the mix holds names with strongly offsetting views, and gives them
real weight. Integration recovers part of that discarded half, which shows up as a materially
higher **transfer coefficient**: the mix pays the long-only distortion *once per signal*, the
integrated book *once in total*. → `notes/2026-08-31-signal-blending-vs-portfolio-blending.md`

**The same framework says when the choice does not matter, and that is the part the lab needs.**
The gap goes to zero as signal correlation → +1 (at perfect correlation the two constructions hold
the same names and are identical); goes to zero as target active risk → 0 (with a non-binding
long-only constraint there is no distortion to avoid); and widens with the number of signals
combined. A secondary and smaller benefit is **trade netting** — a mix can have one sleeve buying
what another sells — which scales with sleeve count and unconstrained turnover, so it is close to
nothing for a two-or-three-leg monthly blend and no candidate should rest its case on it.

**The empirical magnitude is contested in a peer-reviewed venue and should not be imported.**
Leippold–Rüegg (2018, *European Financial Management*, Tier 2, **abstract only** — every route to
the full text refused an automated client) re-examine the comparison with robust
performance-testing tools and report, verbatim: *"we demystify these findings as a statistical
fluke… We do not find any evidence favouring the integrated approach. What we do find is that the
integrated approach exhibits a higher sensitivity to the low-risk anomaly. However, this reduction
in risk does not lead to an improvement in performance."* That is why this cluster is Tier B. It
also hands the lab the right null hypothesis: averaging scores mechanically pulls a book toward
the centre of every signal's distribution and therefore *lowers its volatility*, and this lab has
already refuted low-vol tilts on this universe. **Any integrated candidate must be screened
against a plain low-volatility book before its result is attributed to information combination**,
or the lab will re-run a refuted trial under a new name.

**Net effect on `learnings.md`'s 2026-08-30 closure of this family: the scope narrows, the
arithmetic stands.** The lab priced equal-weight ensembles of the eight legs' *stored return
series* and found them monotone decreasing against the best single member. That is precisely the
**mix**, and this literature agrees the mix is bounded that way by construction. The integrated
construction is untested here and is not subject to that bound. See candidate #60 for the one free
diagnostic that decides it — and note that `SUMMARY.md`'s 2026-08-30 downgrade of the **HRP** half
is untouched and, if anything, corroborated: HRP is a risk allocator over finished books, i.e. a
mix, and no clustering allocator can escape a bound that binds on the whole class.

**[2026-09-01] The algebra behind the lab's mean-versus-max result, and it says the boundary is
exactly where the lab found it.** Novy-Marx (working paper, R&R at JFE, Tier B; 41 citations)
proves an **exact equivalence**: for a composite formed as a *linear* combination of signals, the
resulting signal-weighted strategy's return is **identical** to a portfolio of the single-signal
strategies held at the composite weights. Integration and mixing are the same object under
linearity. That is why `learnings.md`'s mean-operator ensembles were bounded by their legs
(2026-08-30) and why the closed-form tail-depth penalty `sqrt((1 + (n−1)ρ)/n)` (2026-08-31) holds:
the bound is not an empirical regularity, it is this equivalence plus Markowitz. **The max
operator is not a linear combination, so neither the equivalence nor the bound applies to it** —
the lab found the boundary empirically and this is the algebra for why it sits there.
`validation_overlap: false`. → `notes/2026-09-01-multi-signal-overfitting-critical-t.md`

**It also resolves the apparent conflict with the integration literature, and sharpens both.**
Fitzgibbons et al. argue integration beats mixing under a long-only constraint; Novy-Marx proves
they are identical for linear composites. Both are right, and the reconciliation is that
Fitzgibbons et al.'s entire gap comes from the **long-only truncation**, a nonlinearity applied
*after* the linear blend, while the equivalence is derived for untruncated signal-weighted books.
**Strip the nonlinearity and the integration advantage vanishes** — which predicts the advantage
should scale with how binding the constraint is, and makes Leippold–Rüegg's "much ado about
nothing" rebuttal what it looks like when the constraint is slack. It is also the general form of
the lab's own finding: the value of an aggregation operator is the value of its nonlinearity.

**The cost side, and it lands on the integrated candidate the lab just built.** The same paper is
the field's sharpest statement of what a multi-signal backtest is worth as *evidence* — see the
cross-cutting entry below. The short version for this family: the equivalence exonerates nothing
about inference, the selection of four family leads from a screened pool of order 20–30 sits in
the paper's `n^k` regime, and **a composite containing no mediocre legs is the paper's stated
signature of selection bias.** A composite of family *leads* is by construction exactly that.

---

### Portfolio construction & rebalance mechanics (cross-family)

Not a `program.md` family, but the axis `learnings.md` says is the lab's only live one and the
one `SUMMARY.md` flagged as the highest-value gap. Three legs: which trades to skip, when to
trade, how much to hold.

**The champion's membership buffer is the technique this literature ranks first among all
cost-mitigation methods, and for the reason the lab observed.** Novy-Marx–Velikov compare
three ways to cut cost drag — screen to cheap-to-trade names, rebalance less often (or
staggered-partially), and "banding" (a buy/hold spread: a stricter bar to enter a position
than to keep one). All three cut costs; the turnover-reducing ones damage gross performance
less than the liquidity screen, and **banding beats frequency reduction because it delivers
similar cost savings while preserving better exposure to the signal** — the trades it
suppresses are the low-information ones oscillating around the cutoff. The champion's
hold-25/enter-15 (and wider 35/20) band is exactly a buy/hold spread. Two structural
consequences for this repo: the liquidity-screen lever is already spent (a ~145-name large-cap
global universe at a flat 15 bps/side *is* the cheap-to-trade screen at its limit), and with
the learnings entry that turnover reduction is now worth ~0.019 Sharpe in total, **the
cost-mitigation literature should be treated as closed for idea supply here — explanatory
value only.** One tension recorded rather than smoothed over: this source models staggered
rebalancing as buying cost savings *at the price of signal staleness*, whereas the lab
measured no staleness tax at all (pruning stale tranche names hurt on every axis). They are
different objects — the paper's staggering is one book traded less often; the lab's overlap is
several formation vintages held at once — so the paper's ranking is not evidence against the
overlap. Tier A, `validation_overlap: false`.
→ `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`

**There is literature treating overlapping tranches as a portfolio improvement — but the
improvement it claims is lower outcome dispersion, not higher expected return.** Hoffstein and
co-authors define *rebalance timing luck* as the standard deviation of returns across
identically managed portfolios differing only in rebalance date, show it is an
uncompensated variance (neither date is better ex ante), and show that splitting capital into
N differently-dated tranches held in equal weight reduces it by a reported factor of 1/N. Its
drivers are turnover (↑), concentration (↑), holding count (↓) and rebalance frequency (↓
timing luck as frequency rises). This partly fills the gap flagged last session — that the
lab's overlap result had no literature behind its economic claim — but only partly: the lab's
finding that the six-tranche book *earns more* than a single-vintage book remains beyond this
source too. Its most useful contribution here is a **measurement caution**: every non-tranched
backtest is one draw from a timing-luck distribution while the tranched book sits near that
distribution's centre, so small Sharpe gaps between variants differing in rebalance mechanics
should be read as noise by default. Tier B (practitioner journal, US-only, self-built indices,
no independent replication found), `validation_overlap` assumed true, `published_post_2018:
true`. → `notes/2026-08-17-rebalance-timing-luck-tranching.md`

**Magnitude weighting sits outside the estimation-error trap that kills most "smarter"
weighting schemes — and that boundary is why it works where inverse-vol weighting failed.**
DeMiguel–Garlappi–Uppal find that across seven datasets and fourteen optimisation models
(shrinkage, moment restrictions and other error corrections included) none consistently beats
naive 1/N on Sharpe, certainty-equivalent return or turnover, because an optimiser amplifies
estimation error in its inputs: their calibration puts the estimation window needed to beat
1/N at ~3,000 months for 25 assets and ~6,000 for 50. The Kritzman–Page–Turkington rebuttal
locates the damage specifically in short-rolling-window estimates of *expected returns*, not in
optimisation as such. Net principle: **a weighting scheme's out-of-sample cost scales with how
many noisily-estimated parameters it needs.** The champion's z-score magnitude weighting
estimates none — it is a monotone transform of an observed cross-sectional score — while
inverse-vol and risk-parity weighting are in the expensive class, so the lab's two empirical
refutations of those and this literature's mechanism agree. The same source supplies the
standing caveat: 1/N is a hard benchmark, so beating it by a wide margin deserves scrutiny of
*how*, and the lab's own records (maxDD widening monotonically with each concentration step,
one validation year dominating the P&L) mark where to look. Tier A,
`validation_overlap: false`. → `notes/2026-08-17-naive-vs-optimized-weighting.md`

**The bridge session 6 said was missing is now built, and it says the champion's tranche
averaging is not a trick applied to a cost problem — under one standard cost model it *is* the
optimal cost-aware policy.** Gârleanu–Pedersen (2013, JF) solve in closed form for a
mean-variance investor with several return predictors of differing mean-reversion speeds and
quadratic trading costs. Three results and one corollary. (a) The optimal portfolio is **partial
adjustment**, `x_t = (1−a/λ)x_{t−1} + (a/λ)aim_t`, with the trading rate a scalar decreasing in
costs, increasing in risk aversion, and independent of the current book. (b) The target is not
the frictionless optimum but an **aim portfolio**, an exponentially weighted average of the
current and all future expected frictionless portfolios — higher costs put more weight on where
the target is going. (c) Signals are weighted **by persistence**: with diagonal decay the aim is
the frictionless portfolio with each signal `f^k` divided by `(1 + φ_k a/γ)`, so fast-decaying
signals are discounted harder, and the discount grows with the cost rate. Absent costs, alpha
decay plays no role at all — persistence weighting is purely cost-induced. **The corollary is
the one that answers the folder's standing question**: an investor following the policy holds
`x_t = Σ_{τ≤t}(a/λ)(1−a/λ)^{t−τ} aim_τ` — the optimal book is an exponentially weighted average
of *past target portfolios*. Every prior account here of the champion's six formation vintages
(estimator, dispersion, forecast MSE, information ratio) was a claim about a predictor; this one
is a claim about a portfolio held by a cost-paying investor, which is the currency the lab
measures in. Two boundaries travel with it. The policy is unconstrained and needs `B`, `Σ`, `Φ`
and `λ` estimated — screen #1's expensive class. And the authors state that under **proportional
or fixed** costs (this repo's flat 15 bps/side) the optimal policy is qualitatively different and
"exhibits periods of no trading" — i.e. a no-trade band, which is what the champion's hysteresis
buffer implements. So the two mechanisms the champion runs are the canonical answers to the two
standard cost specifications, and are complements by construction. Tier A on the theory (B on the
single-asset-class, admittedly in-sample empirical illustration), `validation_overlap: false`.
→ `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md`

**The same crossing attempted from the estimation side instead, and it lands on the lab's own
protocol concern.** Brandt–Santa-Clara–Valkanov (2009, RFS) skip return modelling entirely and
write the weight itself as a function of cross-sectionally standardised characteristics,
`w_i = w̄_i + (1/N)θᵀx̂_i`, fitting the short coefficient vector `θ` by maximising the **realised
sample utility of the portfolio's returns** — the "optimise the realised objective directly"
literature the folder went looking for. Its stated advantages are real (parameter count
independent of universe size; the fit implicitly prices variances, covariances and higher moments
without estimating any of them; any objective admissible, including Sharpe, tracking error or
drawdown control; long-only handled by truncate-and-renormalise). **The reading that matters here
is that the champion already *is* a parametric portfolio policy with `θ` hard-coded rather than
fitted**, which locates exactly the door the lab has kept shut: fitting `θ` to an in-sample
objective is the failure mode the deflated-Sharpe gate exists to punish, so BSV is not a
candidate to import but the *name* of a class of proposals to decline. Lamoureux–Zhang (2024,
RAPS) supply the critique, and its mechanism is the portable part: parsimony in `θ` does **not**
protect you, because the utility being maximised depends on every property of an unspecified
return distribution; and **overfitting is positively linked to the variance of the resulting
portfolio**, so the remedy is to *fit with a more concave loss than the one you care about*
(estimate at `γ* = γ + λ`, hold as the `γ` investor). That generalises past `θ` to any procedure
that picks a book by maximising a sample statistic — including selecting candidates on validation
Sharpe — and it predicts the exact shape `learnings.md` records under its ⚠ standing protocol
concern: a criterion with too little curvature picks the high-variance member of the candidate
set. Two further transferable facts: cross-sectional standardisation is load-bearing (it makes
the score distribution stationary across dates *and* makes weights sum to one), and BSV report
the long-only constrained version yielding materially smaller gains than the unconstrained one —
a third independent instance of "long-short results do not transfer by default", this time from
portfolio construction rather than from a momentum or beta mechanism. BSV tier B+
(`validation_overlap: false`); Lamoureux–Zhang tier B− (essentially uncited so far, and
`validation_overlap: true` — its evaluation window runs into 2021, so only its mechanism is
carried here, never its empirical conclusions).
→ `notes/2026-08-20-parametric-portfolio-policies.md`

**And a fourth cost-mitigation technique that last year's enumeration missed, with a closed form
attached.** DeMiguel–Martín-Utrera–Nogales–Uppal (2020, RFS) find transaction costs *increase*
the number of jointly significant characteristics — six without costs, fifteen with them —
because of **trading diversification**: legs held simultaneously rebalance by trading the same
underlying instruments, so a buy from one leg nets against a sell from another and only the
residual is executed. Proposition 3 gives the ratio of combined turnover to isolated turnover as
`√(eᵀΩe)/Σ_k√(Ω_kk)`, which for equal variances and equal pairwise trade correlation `ρ` is
**`√((1+ρ(K−1))/K)`**, and `1/√K` at `ρ = 0`. The free parameter is the correlation of
*rebalancing trades* — not of scores, not of weights, not of returns — which is computable from
holdings and prices with no returns scored, making this the folder's first **pre-trial,
holdings-only prediction of an averaging proposal's turnover**. It retro-predicts the champion:
the recorded six-vintage/single-vintage pair is 3.5x against 7.9x, ratio 0.44, against `1/√6 =
0.41`, with the vintages' positive trade correlation being exactly what lifts a ratio above
`1/√K`. It also carries a real **amendment to the folder's ensemble screen**: components
estimating *different* quantities still net their trades, so a second leg's contribution is
`(gross dilution) + (turnover saved) × (cost rate)` and the folder has only ever measured the
first term. That does not reopen the ETF-sleeve blend — total cost drag here is priced at ~0.019
Sharpe and the dilution tax at ~0.02 per 20% of capital, so the recoverable term is too small —
but "every extra leg costs turnover" is now known to be false in general, and the paper reports
cases where a leg's *marginal* contribution to turnover is negative. Tier A (costs central,
multiple testing handled by screen-and-clean, multi-decade), `validation_overlap: false`,
`published_post_2018: true`.
→ `notes/2026-08-20-trading-diversification-combining-signals.md`

**A constraint is not only a leak — it is also an estimator, and the folder had only recorded
the first half.** Jagannathan–Ma (2003, JF) prove that the constrained global minimum-variance
portfolio built from an estimated covariance `S` is the *unconstrained* minimum-variance
portfolio built from `S̃ = S + (δ1′ + 1δ′) − (λ1′ + 1λ′)`, where `λ` and `δ` are the Kuhn–Tucker
multipliers on the non-negativity and upper-bound constraints. Reading the entries: a binding
**no-short** constraint on asset `i` *reduces* its covariance with every `j` by `λ_i + λ_j`, and
a binding **cap** *raises* it by `δ_i + δ_j`. The economics is in where they bind — the no-short
constraint binds precisely on the assets with the largest estimated covariances (which is why
they wanted negative weights), and those are the estimates most likely to be upward-biased by
sampling error; the cap binds on the smallest, most likely downward-biased. Both edits are
shrinkage toward the mean, applied exactly where estimation error is worst, which is why a
constraint **false in the population** can still improve out-of-sample risk. Proposition 2
upgrades this from analogy to identity: `S̃` satisfies the first-order conditions of the
*constrained maximum-likelihood* problem, so imposing the constraint at the optimisation stage
and imposing it at the estimation stage are the same act. The empirical half is the part the lab
can use: once no-short is imposed, the plain monthly sample covariance produces minimum-variance
books about as good as factor models, Ledoit shrinkage or daily data, and adding a cap on top of
no-short changes realised variance essentially not at all (caps are for implementability, not
risk). **What does not transfer** must be said first, though: the theorem is about a
minimum-variance *optimiser*, and the champion's caps bind on whatever the signal likes, not on
whatever has the largest covariance — so this is not evidence that the repo's 25% cap improves
its returns. Tier A, `validation_overlap: false`.
→ `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`

**Diversification has a *return* consequence, not only a risk one, and the lab's concentration
measurements were already telling it so.** Willenbrock (2011, FAJ), formalising Booth–Fama
(1992), derives that for a portfolio rebalanced to **constant weights**,
`g_p ≈ Σ_i w_i [ g_i + ½(σ_i² − σ_ip²) ]`, so the book's geometric return exceeds the weighted
average of its constituents' geometric returns by `½ Σ_i w_i(σ_i² − σ_ip²)` — the
**diversification return**. Two clarifications carry the weight. (a) The source is **not**
variance reduction (necessary but not sufficient) but the **rebalancing itself**: holding
weights constant forces selling what rose in relative value and buying what fell, and that
contrarian act monetises fluctuation. Assets each with *zero* geometric return still make a
rebalanced book gain; unrebalanced it gains nothing. "Volatility return" is the author's own
alternative name. (b) A buy-and-hold book earns none of it, but has a *different, unrelated*
incremental return — winners becoming a larger share — bought at the price of a drifting risk
profile. The consequence here is a cost the folder has never priced: `σ_i² − σ_ip²` is large
only for positions whose volatility is idiosyncratic *to this book*, so a concentrated,
magnitude-weighted book that loads capital on the names that are simultaneously the most
volatile and the most mutually correlated has almost none of the term. The lab's own
holdings-only measurement (top name 17.2% of capital / 30.9% of variance; ~6 effective risk bets
against 13.3 by weight) is therefore also a statement that its diversification return is small.
Tier A on the identity (algebra), B on the applied claims — one worked application, no
transaction costs modelled anywhere, and the term is second-order in variance while this repo
pays 15 bps/side. `validation_overlap: false`.
→ `notes/2026-08-21-diversification-return-and-rebalancing.md`

**And the measurement axis itself: counting positions is not counting bets, with a specific
correction to a statistic the lab already runs.** Meucci's effective number of bets changes
basis before counting. Eigendecompose the covariance, `Σ = EΛE′`; the columns of `E` are
uncorrelated **principal portfolios**; re-express the book as `w̃ = E⁻¹w`; form the
**diversification distribution** `p_n = w̃_n²λ_n / Var(R_w)`, which is non-negative, sums to one,
and whose `n`-th entry is provably the **R² of a regression of portfolio return on the `n`-th
principal portfolio**; then report `N_Ent = exp(−Σ p_n ln p_n)`, which is 1 when all risk comes
from one direction and `N` when risk is spread evenly. Meucci's explicit criticism is of
weight-Herfindahl measures *and* of counts built on marginal risk contributions of correlated
assets — which is what the lab's "6.0 effective risk bets" is. The **conditional** version is
the one that matters for a fully-invested long-only book: the budget constraint alone pins the
exposure to the first principal portfolio (≈ the market), so the unconditional index is low for
a reason no candidate can change; dropping the first `K` masses and renormalising measures the
part the strategy controls. Polakow–Gebbie make the same point against the fundamental law
("independence is not separateness"; skill does not scale over breadth) and estimate effective
dimensionality as the count of correlation eigenvalues `≥ 1`, finding in their market that a
41-name universe supported no more than eight dimensions and that adding a whole extra asset
class raised that by about one. Tier C — Meucci's construction is algebra and cannot decay, but
neither source carries an empirical study meeting this folder's bar, the venues are tier 3, and
the Meucci article does not resolve in any citation index tried. `validation_overlap: false`.
→ `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`

**The decomposition session 8 asked for exists, is a theorem, applies to a signal-driven book, and
is computable from holdings with nothing estimated.** Fernholz–Karatzas's survey of stochastic
portfolio theory states, for *any* weight process — time-varying, path-dependent, signal-driven —
that `d log V^π = γ*_π dt + Σ_i π_i d log X_i`: a portfolio's log growth is the weighted average of
its holdings' log growth (the **selection term**) plus an **excess growth rate**
`γ*_π = ½(Σ_i π_i a_ii − π′aπ) = ½ Σ_i π_i τ^π_ii`, which for a long-only book is always
non-negative and is strictly positive unless the book holds one name. That is the continuous-time
generalisation of Willenbrock's identity to exactly the case the session-8 note could not cover, and
it closes open question 8(a) at the identity level. Two uses. (i) `γ*_π` is a **return-denominated,
holdings-only diagnostic** — realised covariance of what was held, times the weights actually held,
no forecasting — so a session can finally price what each concentration step costs on the axis the
gate reads, rather than only in risk breadth. The lab's documented ladder (equal-weight → rank
weight → magnitude weight, then the buffer deletion that moved 35.1 → 30.3 names and 7.8 → 6.0
effective risk bets) has been spending this term monotonically and has never measured it. (ii) For
the narrower class of **functionally generated** portfolios (weights a fixed function `G` of current
market weights) the master formula splits relative performance into a bounded positioning term
`log(G(μ_T)/G(μ_0))` and a cumulative drift `∫g dt` that can be recovered **without estimating any
covariance at all**. That shortcut does *not* apply to the champion, which is path-dependent, so
only the general identity transfers. Two hard boundaries: `γ*` is a term in **log growth**, not in
Sharpe, so the folder's standing accuracy-to-realised-return gap is not closed by it; and the
diversity-weighted portfolio the theory is famous for needs **market capitalisations**, which this
repo does not have, and its outperformance theorem carries an explicit long-horizon condition
(`T ≥ (2/pεδ)·log n`) and no transaction costs. Tier A on the identities (theorems), B on the
chapter's single uncosted US simulation. `validation_overlap: false`.
→ `notes/2026-08-22-excess-growth-and-return-decomposition.md`

**But the folder's framing of that term was wrong, and correcting it flips the sign of the
"give-away" on a momentum book.** `SUMMARY.md` recorded after session 8 that the rebalancing term is
"a quantity the champion is currently *giving away*". Cuthbertson–Hayley–Motson–Nitzsche show the
rebalancing literature systematically conflates two things. The **diversification return** — a
book's growth exceeding the weighted average of its constituents' growth — follows from
`E[GM] ≈ E[AM] − σ²/2` applied to a basket whose variance is below its constituents' average, and
they derive in generality that an **unrebalanced** book earns it too; rebalanced and buy-and-hold
books start with *identical* expected growth rates and diverge only as the buy-and-hold weights
drift toward being less diversified. The residual genuinely attributable to the rebalancing trades
is **zero in expectation under IID returns** — each trade swaps into an asset as likely to under- as
outperform — and is positive only where relative prices **mean-revert**, negative where they
**trend**. Two further correctives: the classic "buying on downticks" argument is an infinite-horizon
result (over horizons to 100 years the rebalanced book won under 70% of 100,000 simulated paths),
and **expected terminal wealth is higher for the unrebalanced book**, because it keeps an
ever-thinner, ever-longer right tail. Applied here: the part of the term that is real is *not* given
away — the champion earns it by being diversified at all — and the part specific to re-targeting has
**negative** expected value on a book that exists to bet on relative-price continuation. This
supplies the mechanism for the lab's own re-target-cadence bracket (weekly re-targeting lost;
unbounded weight drift lost worse) and a *new* justification for the membership buffer: a hold-band
suppresses contrarian trades a continuation signal does not want, which is a different claim from
the cost claim `learnings.md` retired. **Tension recorded rather than smoothed over:** Willenbrock's
algebra is not disputed, only its attribution; where the two disagree — whether the term is evidence
that rebalancing *pays* — this source is the more careful and should govern. Tier B (peer-reviewed
field journal, decisive algebra, but modest citations and no empirical content).
`validation_overlap: false`. → `notes/2026-08-22-rebalancing-return-attribution-critique.md`

**The counterweight session 8 asked for on constraints exists, and it dissolves the question rather
than answering it in either direction.** Brodie–Daubechies–De Mol–Giannone–Loris show that under a
full-investment constraint an `ℓ1` penalty `τ‖w‖₁` is *algebraically* a penalty on short positions
(`‖ρ1 − Rw‖² + 2τ Σ_{w_i<0}|w_i| + τ`), so **the long-only constraint is the `τ → ∞` endpoint of a
continuous shrinkage path**, with a critical `τ₀` above which the penalised solution simply *is* the
long-only optimum. Two findings follow. First, the crossover is real: on 48 industry portfolios the
best portfolio anywhere on the path had no short positions (the constraint cost nothing), while on
100 size × book-to-market portfolios the best portfolios did include shorts and beat both `1/N` and
the long-only optimum — the same method, the same sample, only the asset set changed. So **yes, a
binding constraint can cost more than the estimation error it suppresses** — but the paper states
**no general condition** for which side a universe falls on; `τ` is tuned on training data. The
standing statement should therefore be neither "constraints are good" nor "constraints leak signal"
but: *a constraint is a shrinkage intensity; cost and benefit both scale with how binding it is, and
which dominates is an empirical property of the universe.* Second, and not previously noticed in
that literature: long-only optima are **automatically sparse** (single-digit name counts on both
asset sets), so concentration is partly a consequence of the positivity constraint rather than an
independent stance — which reframes "few names" as the expected shape of a long-only solution here,
and any proposal to widen the book as a move *away* from where the constraint pushes. A third,
explanatory: a proportional per-side cost is literally an `ℓ1` penalty on `Δw`, so the repo's cost
model is itself a regulariser and a no-trade band's shrinkage effect is not separable from its cost
effect. Tier A (PNAS; multi-decade out-of-sample protocol) — but US-only, on constructed portfolios
rather than securities, and costs discussed rather than charged. `validation_overlap: false`.
→ `notes/2026-08-22-long-only-as-l1-regularization.md`

### The objective itself — growth, utility, and the gate's own statistic (cross-family)

Also not a `program.md` family. Session 9 left one thread open above all others: *every account this
folder imports is denominated in forecast MSE, information ratio or log growth, while the gate reads
net Sharpe on a six-year window.* Session 10 attacked that seam from both ends — the currency the
folder imports in, and the currency the lab is scored in. Both ends came back negative, and the
second one is the more important result.

**Maximising log growth is not an approximation to any risk-scored objective, and the error grows
with the horizon — which retires the premise under which `γ*` was imported.** Samuelson (1971)
grants the one true theorem — a max-geometric-mean strategy makes it "virtually certain" that over
a long enough sequence it ends with higher terminal wealth than any essentially different rule — and
then kills the corollary everyone draws from it, by noting that the horizon `M(x)` at which
dominance kicks in is **unbounded in the wealth level `x`**, so "almost certainly" never converts
into a statement about an expectation. His counterexamples cover the cases in turn: for
`u(x) = x^γ/γ` with `γ ≠ 0` the optimal uniform strategy differs from the log-optimal one and the
strict inequality holds **for every `T`, however large**; boundedness (Markowitz's proposed rescue)
does not help, because for `γ < 0` the log rule is *over*-risky and the near-ruin paths, which occur
at every `T` with positive probability, carry a prohibitive penalty. Merton–Samuelson (1974) convert
this into a magnitude: the initial-wealth equivalent of being made to follow the log rule instead of
one's own optimum is `Π₁₂(T) = λ(γ)^(T/γ)` with `λ > 1`, so **the compensation demanded grows
without bound in the horizon**, and for sufficiently risk-averse investors (`γ < −1`) the
log-optimal program is dominated by *holding only the riskless asset*. They then close the obvious
repair: treating `(mean-log, variance-log)` as an asymptotically sufficient pair and building a
frontier on it is an improper interchange of limits, and the discrepancy between the true expected
utility and the lognormal-surrogate one **goes to infinity, not zero, as `T → ∞`**. The one place a
log-moment frontier is legitimate is the continuous-time limit of a *fixed* horizon subdivided
finely — and even there the frontier is a different object from the Markowitz mean-variance
frontier. **Direct consequence for this folder:** session 9 ranked `γ*_π` its top measurement on the
stated grounds that it is "denominated in log growth and therefore on the gate's own axis." That
premise is false in general, not just awkward. `learnings.md` has since measured `γ*` on the
promotion ladder and found it a null; this is the reason it never could have been otherwise. Tier A
(theorems and counterexamples), `validation_overlap: false`.
→ `notes/2026-08-23-geometric-mean-maximization-fallacy.md`

**The growth school's own summary agrees on the mathematics, and hands over three things the folder
can use — including the only exact growth-to-Sharpe bridge in the literature, which turns out to be
narrower than it looks.** MacLean–Thorp–Ziemba list Samuelson's corollary under *"Fallacy"* and
state flatly that "the Kelly portfolio does not necessarily lie on the efficient frontier in a
mean-variance model." What they add is quantitative. (a) **The bridge**: in continuous time
`g_p = E_p − ½V_p`, and at the growth-optimal exposure `X* = (E_M − r_0)/σ²_M` the growth rate is
`g* = r_0 + ½·SR²`. Growth and Sharpe are monotone transforms of each other **at the optimum of a
leverage choice, and only there** — substitute a fixed exposure, as a leverage-capped book must, and
the two orderings come apart as soon as candidates differ in volatility. So the crossing session 9
asked for exists and does not transfer. (b) **The shape of the risk dial**: growth is a concave
parabola in exposure with roots at zero and `2X*`, so betting exactly twice Kelly earns the
risk-free rate — all the variance, none of the growth — and the penalty for overbetting is quadratic
while underbetting near the optimum costs only linearly. Their tabulated growth-security trade-off
makes the same point from the other side: 0.8× Kelly retains 96% of the growth, while full Kelly
accepts a one-in-three chance of halving before doubling. (c) **The estimation-fragility ordering**,
which re-weights this folder's screen #1 rather than repeating it: errors in *means* cost roughly
10× what errors in variances cost and 20× what errors in covariances cost — **and the multiple rises
as risk aversion falls** (their reproduced table runs 3.22 at risk tolerance 25, 10.98 at 50, 21.42
at 75 for means-vs-variances). Log utility sits at essentially zero risk aversion, so the
growth-optimal criterion is the *most* estimation-fragile point on the whole scale, which the
authors themselves give as the reason to bet less than Kelly. The Kelly rule itself is an
anti-candidate here for the now-familiar reason — it is a **leverage** prescription, and `X*` for a
book of this Sharpe is far above 1, so gross leverage ≤ 1.0 collapses it to "be fully invested,"
which the champion already is. Tier B+ on the survey (its two key tables are reproduced from
closed-access sources not read here); the propositions it collects are tier A and are theorems.
`validation_overlap: false`.
→ `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md`

**And the other end of the seam: the gate's own statistic has a sampling distribution, and on a
six-year window it is coarse relative to the increments the gate adjudicates.** Lo (2002, FAJ)
derives it. Under i.i.d. returns `SE(ŜR) ≈ sqrt((1 + ½SR²)/T)`, so higher Sharpe ratios are
estimated *less* precisely in absolute terms and the proportional error floors at `1/√(2T)`; the
share of the estimator's variance coming from the mean is `1/(1 + ½SR²)`, which falls from 97% at
`SR = 0.25` to 58% at `SR = 1.2` and 33% at `SR = 2.0` — on a good book, most of the noise has
migrated into the **volatility** estimate. Under stationarity alone he gives the GMM/HAC version.
And the annualisation result the paper is known for: `SR(q) = η(q)·SR` with
`η(q) = q / sqrt(q + 2Σ_{k=1}^{q−1}(q−k)ρ_k)`, which equals `√q` **only when every autocorrelation
is zero** — positive serial correlation pushes it below `√q`, negative above, and the gap is large
(for an AR(1) with monthly `ρ₁ = ±20%` the annual factor is 2.88 or 4.17 against `√12 = 3.46`).
Applied here with nothing but the formula and the sample length: at a Sharpe near the champion's
level over 1,562 validation days, `SE ≈ 0.40` (0.54 if estimated from six annual observations),
against a **total** recorded promotion ladder of 0.865 → 1.229. **The caveat must travel with the
number, and it is not optional:** that is the precision of one strategy's Sharpe against an unknown
truth, *not* the precision of the difference between two nearly-identical books measured on the same
six years, which is far tighter and which Lo does not derive. So this does not show the ladder's
steps are noise; it shows the gate is comparing point estimates whose individual precision is much
coarser than the differences being adjudicated. It also gives `learnings.md`'s train-column
observation a statistical reading: ~14,261 days against ~1,562 is roughly a **3× smaller standard
error**, which is what one would expect of the column that tracks the holdout better. Tier A,
`validation_overlap: false`.
→ `notes/2026-08-23-statistics-of-sharpe-ratios.md`

**The paired standard error session 10 said must not be quoted until it was derived is now derived,
in closed form, and it reproduces the lab's bootstrap floor from one number.** Jobson–Korkie (1981)
gave a delta-method standard error for the *difference* of two Sharpe ratios and Memmel (2003)
corrected it; the corrected expression is
`T·Var(Δ̂) = 2(1−ρ) + ½(Sh_a² + Sh_b²) − Sh_a·Sh_b·ρ²`, which for equal Sharpe ratios factorises to
`(1−ρ)·[2 + Sh²(1+ρ)]`. Against Lo's `T·Var(ŜR) = 1 + ½Sh²` this gives the exact relation
**`SE(Δ̂) = SE(ŜR)·√( (1−ρ)(2+Sh²(1+ρ)) / (1+½Sh²) ) ≈ SE(ŜR)·√(2(1−ρ))`** whenever `Sh² ≪ 2` in the
sampling frequency's own units — overwhelming at daily frequency. So the whole of "the paired error
is far smaller than `√2·SE(ŜR)`" is the factor `√(1−ρ)`, and **the gate's resolving power is set by
one number: how correlated the candidate is with the champion.** On `T` daily observations the
annualised paired SE is `≈ √(2·252·(1−ρ)/T)`, i.e. `0.568·√(1−ρ)` on a 1,562-day window: 0.031 at
`ρ=0.997`, 0.080 at 0.98, 0.172 at 0.909 — which lands on both of the ranges `learnings.md`
bootstrapped, with no resampling and before any candidate exists. **But Ledoit–Wolf (2008) is the
reason to treat that as a floor rather than a test**: the closed form assumes i.i.d. bivariate
normal returns, and their simulation across six data-generating processes shows it is *liberal*
under fat tails (≈2× the nominal rejection rate), under GARCH, and worse under both (≈3×). HAC
inference is asymptotically valid and also liberal in finite samples; what is close to nominal
everywhere is a **studentized circular-block bootstrap on the return pairs**, with a per-resample
standard error and a calibrated block length. The lab's own paired stationary-block bootstrap is
that family, and this source names the two free refinements it lacks (studentize inside the
resample; calibrate `b` rather than reporting a grid). One reframing worth keeping: because power
*rises* with `ρ` (Opdyke's correction to Jobson–Korkie's third error), consecutive ladder rungs
correlating 0.909–0.997 are the test's most favourable regime, so failing to separate there is a
stronger result than it looks; and testing against a *moving benchmark* is structurally lower-powered
than testing a Sharpe against zero, which is the question the gate asks by construction. Tier A,
`validation_overlap: false`.
→ `notes/2026-08-24-testing-differences-of-sharpe-ratios.md`

**The gate's own machinery is now covered, and it says the deflation bar is a property of the
*search*, not of the candidate — through two channels, one of which the lab had not noticed.**
Bailey–López de Prado's Deflated Sharpe Ratio is the Probabilistic Sharpe Ratio with its threshold
set to `E[max{ŜR_n}]` under the null, approximated by extreme-value theory as
`ŜR₀ = √V[{ŜR_n}]·((1−γ)Z⁻¹[1−1/N] + γ·Z⁻¹[1−1/(N e)])` with `γ` the Euler–Mascheroni constant, and
`DSR = Z[ (ŜR − ŜR₀)√(T−1) / √(1 − γ̂₃ŜR + ((γ̂₄−1)/4)ŜR²) ]`. Six inputs: the candidate's Sharpe,
sample length, skewness and kurtosis, plus **`N`, the number of *independent* trials, and
`V[{ŜR_n}]`, the cross-trial variance of Sharpe ratios** — the last two being properties of the
research programme rather than of the candidate. Channel one is the lab's own observation given a
source: the authors interpolate `N̂ = ρ̂ + (1−ρ̂)·M`, so a family of near-identical candidates counts
as almost one trial, which *is* "DSR clustering makes within-family tuning nearly free". Channel two
is new here and runs the other way: the threshold scales with **√(cross-trial dispersion)**, so a
single wild trial raises the bar for every later candidate by more than its increment to the count —
a reason to prefer well-motivated exploration that is independent of the trial-count argument
already on record. Two further yields. The paper's holdout critique ("holdout assesses the generality
of a model as if a single trial had taken place… apply it enough times and false positives are
expected") lands on this repo's design in a qualified way: the protocol here is *stronger* than the
criticism's target, because the holdout is never used for selection — and the number of holdout
evaluations is still a trial count of a second kind that nothing deflates. And the companion's
**CSCV/PBO** — partition the `T×N` matrix of trial P&L into `S` blocks, run all `C(S,S/2)`
half-splits, and report the fraction of splits where the in-sample winner lands below the
out-of-sample median — is computable from series this repo already stores, with the standing caveat
that it **scores returns** and re-uses the validation split. Tier B+ (tier-1 venue, derivation
numerically verified, but the operative input `N` is reached by interpolation and no independent
replication was found), `validation_overlap: false`.
→ `notes/2026-08-24-deflated-sharpe-ratio.md`

**And the rival correction, which disagrees with the folder's summary of the gate in one specific
and checkable way, and corrects a sentence this folder has been repeating.** Harvey–Liu build the
multiple-testing haircut on the identity `t = ŜR·√T`: convert Sharpe to t to p, adjust p for
multiplicity (Bonferroni, Holm — both FWER; Benjamini–Hochberg–Yekutieli — FDR, valid under
arbitrary dependence via `c(M)=Σ1/j`), convert back, and report
`hc = (ŜR − HSR)/ŜR`. Two results. (a) **The haircut is strongly nonlinear**: larger than 50% for
annualised Sharpe ratios below ~0.4, at most ~25% above 1.0 — so the industry's 50% rule is too
lenient for weak strategies and too harsh for strong ones, and a book near 1.0 sits where this
framework says the multiple-testing penalty should be *mild*. Recorded as a difference between two
published corrections, not as a claim about the repo's thresholds, which are frozen and a human's
decision. (b) **Under an FDR-controlling procedure the bar does not rise without limit with the trial
count.** Bonferroni- and Holm-implied thresholds are monotone in the number of discoveries; the
BHY-implied one fluctuates and then stabilises, because at fixed `α` the law of large numbers pins
the realised false-discovery rate. So "every trial permanently raises the bar" is a **family-wise-
error-rate statement, not a law of statistics** — and FDR is what these authors advocate for finance,
on the argument that an investor cares about the proportion of allocated strategies that are duds.
The companion (Harvey–Liu–Zhu, 313 published cross-sectional papers, 1967–2012) supplies the
threshold everyone quotes — a new factor needs `t > 3.0`, explicitly a **lower bound** because
unpublished failures are invisible — and the caution that it is defined on long–short, gross-of-cost,
benchmark-free factor tests and does not transfer to a long-only candidate compared against an
incumbent. The passage most relevant here is neither: their **in-sample-versus-out-of-sample**
section shows data splitting trades type-I against type-II error, because a shortened in-sample
window loses true discoveries that never reach the out-of-sample stage — the exact type-II mirror of
`learnings.md`'s ⚠ standing protocol concern, from an independent direction. Tier A,
`validation_overlap: false`.
→ `notes/2026-08-24-multiple-testing-haircut.md`

_With this, **the gate's own machinery is fully covered** — the statistic it reads (Lo), the deflator
it applies (Bailey–López de Prado), the rival deflator (Harvey–Liu), and the test it does not run
(Ledoit–Wolf). The folder's obligation to cover the scoring apparatus is discharged; all of it is
explanatory, since `engine/` is frozen._

**The last uncovered seam — a correction that knows *why* a trial was run — turns out to exist, to be
twenty years old, and to live in statistics rather than in finance. Its shape is not the shape the
question assumed: a prior discount is real, rigorous, and strictly zero-sum.** Session 11's open
question (c) asked for a prior-weighted or hierarchical multiple-testing correction, on the grounds
that both finance literatures gesture at one (Harvey–Liu–Zhu: "a factor derived from a theory should
have a lower hurdle") and neither supplies machinery. Genovese–Roeder–Wasserman supply it exactly.
Assign each hypothesis a non-negative weight `W_i` **before** seeing the data, divide its p-value by
its weight (`Q_i = P_i/W_i`), and run Benjamini–Hochberg on the `Q`'s: a weight above 1 relaxes that
hypothesis's threshold, below 1 tightens it. Their Theorem 4.1 controls FDR at `α·(1−a)·μ₀`, hence at
`α` whenever the weights average one, and Roeder–Wasserman give the family-wise analogues. The
authors state the striking part themselves: **"aside from this budget requirement, any set of
nonnegative weights is valid."** Validity does not depend on the weights being good, informative, or
related to the truth at all — only on their being fixed a priori and averaging one. So the answer to
"can a well-motivated candidate honestly face an easier test?" is *yes, and only by making the
others face a harder one*, in a budget that sums to zero. There is no version in which a good prior
buys a discount out of thin air; an unweighted protocol like this repo's is simply the `W ≡ 1` case,
which is the choice a lab makes when it declines to rank its ideas in advance. Three further yields,
each independent of the finance question. **(a) The power asymmetry.** Because the alternative's
p-value distribution is stochastically smaller than uniform, up-weighting a true alternative gains
more than down-weighting one loses, so informative weights buy a large power gain while wrong ones
cost very little — "the loss of power is not serious even if the weights are completely wrong". The
safe regime is *sparse*: few large weights with the minimum weight near 1, i.e. **betting the whole
prior budget on one pre-named candidate is robust, spreading modest tilts across many is fragile.**
**(b) The optimal weight is unimodal, not monotone.** `ρ_c(ξ) = (m/α)·Φ̄(ξ/2 + c/ξ)`, peaking at
`ξ = √(2c)` — down-weight the hopeless *and* the already-obvious, spend the budget on the **marginal**
hypothesis, formalised as the effect with power ½ at unit weight. That inverts the natural instinct
to back one's strongest conviction. **(c) The shortcut is closed at the mechanism level.** Splitting
the sample to *estimate* weights gains over unweighted testing of the held-out half but **does not
beat simply using the whole sample unweighted** — so no discount can be manufactured from the split
being scored on. The one estimated scheme that works is deliberately crude and *grouped* (partition
into clusters of ≥20–30, estimate per cluster, smooth toward the mean, renormalise), which preserves
error control because a single lucky test cannot up-weight itself — only its whole cluster can. Tier
A, `validation_overlap: false`. Recorded as candidate #31.
→ `notes/2026-08-25-prior-weighted-multiple-testing.md`

**The same question asked in a finance venue supplies the exchange rate the statistics answer lacks —
and finds the prior moves the bar by about one t-unit, in the direction opposite to the one a lab
would hope.** Harvey's presidential address gives the closed-form map from a prior to a required
threshold. Posterior odds = prior odds × Bayes factor; the **minimum Bayes factor**
`MBF = exp(−Z²/2)` is the lower bound over all specifications of the alternative, attained when the
prior mass sits exactly at the maximum-likelihood estimate — so it is **the most favourable reading
the evidence can ever receive**. For priors symmetric and descending about the null (the right default
when there is no directional conviction) `SD-MBF = −e·p·ln(p)`, always larger. The Bayesianized
p-value is `(MBF × prior odds)/(1 + MBF × prior odds)`, and inverting it gives the required statistic
as a function of the prior. The decisive number: at **even odds** — the most generous prior anyone
could claim — and under the MBF, the threshold for a 5% posterior probability of the null is
**t = 2.43**, rising to 2.94 at 4:1 against and 3.43 at 19:1; under the SD-MBF the even-odds figure is
2.93. **A prior never buys a bar below the naive frequentist 2.0; it only relocates the bar relative
to a long-shot default,** and moving from a 19:1 prior to even odds is worth about 1.0 in t-units.
That is the bound the folder's open question needed. Two further mechanisms travel with it. The
**base rate declines over time** for three structural reasons — true effects grow scarcer as
low-hanging fruit is picked, first-principles theories run out, and the security count is finite
against an unbounded characteristic space — so the same t is worth less later, which applies directly
to a lab that has worked one family hard. And the **choice space, not the reported result, is the
denominator**: his demonstration obtains `t = 3.23` with near-zero factor betas by searching ~25,000
long-short portfolios formed on *the first three letters of ticker symbols*, and he extends the count
to choices never exercised. He is also explicit that raising a threshold may *increase* data mining
rather than reduce it. **The counterweight that must travel with the whole idea: his conclusion runs
against the use a lab would most like to make of him** — the thesis is that finance's priors are long
shots and its thresholds too low. Tier A, `validation_overlap: false`. Recorded as candidate #32.
→ `notes/2026-08-25-bayesianized-p-values-prior-odds.md`

**And the empirical realisation of the same idea in finance, which reverses the multiple-testing sign
under one condition this repo fails — while narrowing the lab's own standing protocol concern to the
part of it that is real.** Jensen–Kelly–Pedersen model all factor alphas jointly and hierarchically:
`α_i = α_o + c_j + s_n + w_i` (a dogmatic zero global component, a theme-cluster component, a
characteristic component shared across regions, an idiosyncratic residual), with the prior `α ~ N(0,
τ²)` playing the role a frequentist correction plays — imposing conservatism and controlling the FDR.
Four mechanism-level results, all portable and none requiring their data. **(1) Shrinkage in units of
time.** `E(α|α̂) = κα̂` with `κ = 1/(1 + σ²/(τ²T))`; the prior is *exactly* equivalent to prepending
`σ²/τ²` periods of observed zero alpha to the sample, which turns an abstract prior strength into a
quantity anyone can argue about. **(2) Out-of-sample attenuation is the prediction, not the failure.**
Since `κ < 1` strictly, a Bayesian *always* expects future alpha below the in-sample estimate, so a
positive-but-lower out-of-sample result is correct learning rather than evidence of
non-replication — and the testable corollary (higher in-sample alpha still predicts higher
out-of-sample alpha cross-sectionally) holds in their data, with attenuation somewhat stronger than
their model predicts. **This lands directly on `learnings.md`'s ⚠ standing protocol concern and cuts
partly in the gate's favour:** the *level* drop from validation to holdout is the base case and
carries no information on its own. What survives, and should now lead every statement of the concern,
is the part that was always the real evidence — a **sign flip in the relationship** between the two
splits at an identified structural change, with the series moving monotonically in opposite
directions across a run of promotions. Attenuation is predicted; inversion is not. **(3)
Alpha-hacking is punished on two axes**: `E(α|α̂) = −κ₀ + κ_hacking·α̂` with `κ_hacking ≤ κ` because
search *inflates the variance*, plus a mean-bias intercept — so a searched estimate is discounted
even by someone who believes no bias was introduced. **(4) Correlated evidence is worth less, with a
knob**: `κ_g = 1/(1 + (σ²/τ²T)·(1+ρ)/2)` collapses to the single-source `κ` at `ρ = 1`, which is the
DSR-clustering observation (`learnings.md`'s 11 effective trials against 45 recorded) derived from
the other side and continuous instead of counted. The headline **reversal** — that under a joint
hierarchical model a large family of related tests is partly *evidence* rather than only a penalty,
because the common component is estimated more precisely — is real but conditional: it is borrowed
strength across **weakly-correlated** units, and their own Proposition 2 says the gain vanishes as
`ρ → 1`. The repo's ladder of near-identical variants is exactly the `ρ → 1` case, so **the reversal
is not available here**, and the hierarchical framing would treat this repo's *families* as the unit
and its within-family variants as one observation — the same conclusion DSR clustering already
reached. Their taxonomy (algorithmic clustering into a small number of themes with high within- and
low across-correlation) is the empirical form of the grouped weighting scheme the statistics note
requires. Tier A, but **`validation_overlap: true` and `published_post_2018: true`** — sample to 2020,
published 2023, so mechanism only. Recorded as candidate #33.
→ `notes/2026-08-25-hierarchical-bayesian-factor-replication.md`

**[2026-09-01] There is a bias in this repo's protocol that the trial count structurally cannot
see, and the lab's newest candidate class is made of it.** Every correction this folder holds —
deflated Sharpe, the multiple-testing haircut, publication decay, the hierarchical prior — counts
**trials**. Novy-Marx (Tier B, working paper, R&R at JFE) identifies a second, *distinct* bias
that lives **inside a single trial**: the **overfitting bias** created by the act of signing each
component signal so that it predicts positive in-sample returns. It is present even with **zero**
selection — a researcher who considers `n` signals and honestly employs every one of them is
still exposed — and in his simulations, built on real stock returns with **purely random** sorting
variables, it alone produces critical values above the familiar multiple-testing ones across the
whole range tested. **Combining random signals routinely backtests at `t` above 5; under some
constructions 5% significance requires `t` above 7.**
→ `notes/2026-09-01-multi-signal-overfitting-critical-t.md`

**The two biases multiply, and the multiplication is exponential.** Combining the best `k` of `n`
candidate signals carries a bias almost as large as selecting the single best of **`n^k`**
candidates — derived in a model and confirmed in simulation. Usable 5% critical `|t|` from that
simulation: ≈2.6 for the best 1-of-10 (pure selection, i.e. Bonferroni), ≈3.5 for the best 2-of-10,
>4 for the best 3-of-20, ≈5 for the best 4-of-40, rising to ≈7–8 when signals are weighted by
their own in-sample performance. **Weighting signals by how well they backtested is strictly
worse than equal-weighting them**, always: the equal-weighted composite's `t` is the scaled **L1**
norm of the employed legs' t-statistics (`= √k ×` their mean) and the performance-weighted one is
the **L2** norm, with `L1/√k ≤ L2` and equality only when the legs are identical. That inequality
is the entire cost of letting yourself choose weights, and it is one more derivation of the
parameter-counting screen (#1) this folder already applies.

**Two design flags that apply to this lab's own construction right now.** *(i)* For a typical
candidate set the backtest-maximising equal-weighted composite uses **roughly the best half** of
the signals and discards the rest — so **a multi-signal strategy containing no mediocre legs is
itself evidence that mediocre candidates were considered and dropped**, i.e. selection bias
stacked on overfitting bias, worth about 60% of extra expected `t`. A composite of four *family
leads* is by definition that object. *(ii)* Adding a signal stops improving the backtest `t` once
the new one is less than **half as good as the average of those already employed** — a
description of when an overfitter stops adding, not a target to aim at. **The author's
first-choice remedy is free here and is candidate #63**: price each leg's marginal alpha
*relative to all the others*, Bonferroni-corrected for the number of signals considered, rather
than reading the composite's own statistic. His closing rule is the one to carry: *combine
signals you believe in individually; never believe in a combination because it backtests well
together.*

_With this, **the scoring apparatus is covered on all four sides**: the statistic, the deflator, the
paired test, and now the question of whether a trial's motivation may enter the correction. The
answer to the last is yes in principle, zero-sum in practice, and worth about one t-unit at the
outside — and all of it is explanatory, since `engine/` is frozen._

### The universe itself — survivorship, constituent selection, and the return distribution (cross-family)

Not a `program.md` family. The axis `learnings.md` has carried as a permanent caveat since day one
and which no note here had ever sourced — session 12 named it the better of the two remaining
structurally-different targets, on the grounds that it is the largest unquantified discount this repo
applies to every stock-level result and has a large accessible literature. It does. The session's
shape is one **re-aiming** of the lab's caveat, one **magnitude** for the specific data construction
this repo uses, and one **distribution** that explains why that magnitude is large.

**The lab's permanent caveat is pointed at the smaller of the two problems it should name.**
`learnings.md` says the universe is today's constituents, so "single-stock alpha will look better
than it was" — a claim about the **level** of returns. Brown–Goetzmann–Ibbotson–Ross (1992, RFS)
show the level distortion is the forgiving half: in their calibration, survivorship moves average
risk-adjusted return by roughly 0.4–0.8% per year across 5–20% annual performance cuts. What
truncation does badly is corrupt **inference about persistence**. Conditioning a sample on realised
return reshapes the joint distribution of return and volatility among survivors — a high-residual-
risk asset needed a lucky draw to clear the bar, a low-risk one did not — which induces a spurious
volatility/return relation and, through it, apparent predictability where the generating process has
none. With only a **5%** annual cut, a cross-sectional regression of successive risk-adjusted
performance measures rejects the true null of no persistence **more than half the time**, mean and
median `t` above 2. Their own summary: *"even a small degree of truncation by survivorship will
induce an unacceptably high probability of false inference of persistence in performance."* The
authors extend the claim explicitly past fund performance to asset-pricing anomalies. **A
cross-sectional momentum strategy is a persistence claim and nothing else**, so this is the exact
inference at risk — the caveat's parenthetical "especially momentum" is right for a reason it does
not state. Two further results keep it honest. The **sign is set by the selection rule**: sequential
per-period survival review induces persistence, selection on whole-sample cumulative performance
induces *reversal*, and the authors state the net must be resolved empirically. And the obvious
correction is wrong in general — Stambaugh (2011, QJF) separates **survival bias** (`E[a|survived] −
α > 0`, real) from the **correct inference** (`E[α|a]`), and shows that with no commonality across
assets in prior parameter uncertainty `E[α|a] = a` exactly: once you condition on the survivor's
return series, the fact of survival adds nothing. The standard adjustment is right only in the
limiting case where all assets, dead and alive, share one completely unknown expected return. That is
**not** a licence to ignore survivorship here: this repo's ~145 large-cap global names share a
dominant market factor and high assumed commonality, which is precisely the regime where the near-full
adjustment is closest to correct. Brown–Goetzmann–Ross (1995, JF) is the time-series companion —
conditioning on the market surviving an absorbing barrier can turn an ex-ante premium of zero into a
large ex-post one — and is recorded **second-hand from its abstract only** (closed access, no
repository copy). BGIR tier A, Stambaugh tier B, `validation_overlap: false` for all.
→ `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`

**The bias with this repo's exact data construction has been measured, it is large, and it is not
the bias `program.md` names.** Daniel–Sornette–Wöhrmann (2009, JPM) write out the standard recipe
verbatim — take today's index constituent list, pull each name's history, backtest — and show step
one leaks the future. This is *not* ordinary survivorship: names that survived the entire window are
still selected, because a capitalisation-ranked index cannot contain a name that fell far behind over
the window being scored. Their matched-pair design (for each of eight consecutive decades, the 500
largest as of the window's **end** against the 500 largest as of its **start**) puts the overstatement
at **up to 8% per annum** across 1926–2006, with the ex-post book winning in all eight windows. The
shape matters more than the level and is uniformly flattering: return up, volatility **down**, and
peak-to-valley **drawdown understated** — three of `program.md`'s own gates, made easier than they
would be in real time. Three riders travel with it. The standard way of *sizing* such a bias (same
statistic on clean and biased databases, differenced) is itself biased toward understatement, because
a selected database has smaller covariance terms — "the bias is worse than one thinks it is when
reading the literature". The distortion has a **preferred victim**: inflated means and shrunken
covariances flip the ordering between naive 1/N and sample-based optimisation in the optimiser's
favour, so the folder's screen #1 is *understated* on this repo's data rather than overstated. And
their proposed remedy is not a correction but a **null**: benchmark against constrained random
long-only portfolios run on the same biased universe, matched on leverage, position count, holding
period and turnover — in their illustration, information-free random books on a look-ahead-selected
universe reached Sharpe ratios around 2 and beat the index comfortably. Cai–Houge (2008, FAJ) supply
the channel by which index membership selects on past return: membership is a **threshold on a
characteristic**, so crossings are large-past-return events, and they measure both signs in one
sample (names deleted from the top of the Russell 2000 averaged ≈ +69% over the prior year, from the
bottom ≈ −36%; entrants from the bottom ≈ +53%, from the top ≈ −28%), with top deletions continuing to
show short-term momentum into the following year. Both tier B (strong venues, single market,
unreplicated), `validation_overlap: false`. **One extrapolation is the lab's and not the sources':**
Cai–Houge study a two-sided small-cap index, whereas this repo's universe comes from **large-cap**
indices bounded from below only — so its additions are names growing *up* through the bar and its
deletions names shrinking *down* through it, which is the direction that flatters a cross-sectional
momentum book. That is a second, independent route to BGIR's sign.
→ `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md`

**And why the magnitude is large: the distribution being truncated is extraordinarily skewed, which
also prices a construction step the lab has taken repeatedly.** Bessembinder (2018, JFE), on all
25,332 US common stocks 1926–2016: fewer than half of monthly individual stock returns are positive,
the **modal lifetime return rounded to the nearest 5% is −100%**, median listing life is **seven and a
half years**, and the top **1,092 firms (4.31%)** account for *all* of the market's net dollar wealth
creation while the other 96% collectively match Treasury bills. The mechanism is compounding, provable
on IID normal draws: multi-period buy-and-hold returns are positively skewed even from symmetric
single-period returns, skewness rising in both horizon and `σ`, so **at unchanged mean the median
buy-and-hold outcome falls monotonically in `σ`** — at a ten-year horizon, from 81.94% riskless to
0.14% at `σ = 10%`/month to −85.28% at `σ = 20%`/month. The calibration that makes this bite: monthly
`σ` is **5.4%** for the value-weighted market, 7.3% equal-weighted, and **18.1%** for pooled individual
stocks, and concentration is the dial that moves a book from the first number toward the third. His
bootstraps then measure the consequence directly: annual-horizon skewness falls from 6.99 (one stock)
to 1.08 (five) to 0.10 (25), but **the fraction of draws beating the cap-weighted market is below 50%
at every `N`, costlessly** (48.7% / 45.4% / 36.8% at annual / decade / 90-year horizons for 25-name
books). Three consequences here. It is the folder's **fourth and first distributional** account of what
concentration costs, and it explains as one phenomenon two things `learnings.md` records separately —
drawdown widening monotonically along the concentration ladder, and one validation year dominating the
P&L. It says the **null distribution for a concentrated long-only book is not centred on a broad
benchmark**, independently of skill or costs. And it is the magnitude behind the other two notes: a
current-constituents universe is a draw from the right tail of *this* distribution, which is why the
selection is worth percent-per-year rather than basis points. Tier A, `validation_overlap: false`.
**Boundary, per the folder's own *check the currency* principle:** every statistic here is a
probability of beating a cap-weighted benchmark or a median buy-and-hold return, **not net Sharpe on a
costed constrained book**, and no exchange rate between them exists in the folder. The global
companion that would supply the multi-market leg (Bessembinder et al., FAJ 2023, ~64,000 stocks) is
closed access and is recorded **unread**, with the further note that its sample would carry
`validation_overlap`.
→ `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md`

_Net: the discount this repo applies to every stock-level result now has a **sourced mechanism and an
unambiguous direction**, and its **magnitude on this universe remains unmeasurable with the data the
repo has** — the matched-pair measurement needs point-in-time constituents, which `program.md` lists
under human-approval-gated future upgrades. That is a better statement than the caveat had, and it is
not a number._

**[2026-09-02] The size question the last three sessions kept circling now has a direct measurement,
and it retrodicts the lab's whole trial history.** Fama–French (2008, JF, Tier A, 1312 citations)
sort anomalies **separately within size groups** rather than aggregating, because an equal-weight
all-stock decile spread is largely a statement about the smallest stocks: tiny stocks are ~3% of
market capitalisation but ~**60% of the number of stocks**, and they have the largest cross-sectional
dispersion in anomaly variables, so they occupy **more than 60% of the names in the extreme
deciles**. Value-weighting is not the fix (it hands the answer to a few of the largest names); the
fix is to report all three groups and require the effect in each. Their result: **net stock issues,
accruals and momentum are pervasive across all size groups**, while **asset growth is absent among
big stocks** — the group holding more than 90% of market capitalisation — and profitability is
asymmetric (higher profitability pays among profitable firms; unprofitable firms are not unusually
bad). **This universe has no tiny or small group at all**, so every trial this lab has run is a
big-stock sort, and the reference class for any imported result is the big-stock column rather than
the headline. The consequence is uncomfortably tight: of the three predictors certified pervasive
there, **two require fundamentals this repo does not have, leaving momentum as the only one
computable from daily OHLCV** — and `price-trend` holds all 7 promotions while every family built on
a characteristic *level* has closed on measurement (`liquidity-volume` twice, `range-variance` four
times over nine mechanisms, `learnings.md`'s own diagnosis being that "the level *is* the
survivorship artifact"). This source supplies the prior that would have predicted that pattern in
advance, and the free screen in candidate #68 is how to spend it. It also **reconciles the folder's
three-source size tension rather than adding a fourth reading**: Gu–Kelly–Xiu (predictability
stronger among large stocks) and Freyberger et al. (fewer characteristics surviving among large
firms) are consistent once separated as *accuracy* versus *count* — **expect few live signals on
this universe, not weak ones**, which is what `research/README.md` already told the
`statistical-learning` family on general grounds and now has a measurement behind it. Single-market
(US) is the gap; the effect on ETFs and on non-US markets separately is outside its scope and must
not be extended there by analogy. `validation_overlap: false`.
→ `notes/2026-09-02-anomalies-by-size-group.md`

### What implementation costs — execution, price impact, and paper versus reality (cross-family)

Not a `program.md` family. The **last untouched cost-side vocabulary**: session 6 named it, session 7
answered from friction-aware portfolio choice instead, session 12 ranked it second, and session 13
left it as the only one of its two candidates remaining, with the explicit prior that it would *close*
rather than open. It closes. But the closure is more useful than "nothing here", because it grades a
number the repo has never had outside evidence for — the 15 bps/side charge itself — and it settles a
published dispute about whether this repo's champion family survives costs at all.

**The engine is charging the right quantity, and the level is conservative-to-fair.** Implementation
shortfall is `ret_theory − ret_actual`: the gap between a paper book priced at the decision price and
a real one priced at fills, split into an execution term and an opportunity-cost term for shares never
obtained (Perold 1988, recorded **unread** — paywalled at `pm-research.com`, no repository or mirror
copy found; its definition is used only as restated in the source that was read). Frazzini–Israel–
Moskowitz measure it on **$1.7tn of live institutional executions across 21 developed markets**, and
define the theoretical price as *"the closing price at the time the strategy's desired holdings and
trades are generated, which is typically the prior day's closing price"* — which is this repo's
signal-at-close-`t`, trade-at-`t+1` convention stated in the same words. On level, mean per-trade
implementation shortfall is **11.02 bps**, median 8.63, dollar-value-weighted 16.06, on trades
averaging **0.9% of daily volume**; large-cap trades average 8.90 bps against 18.95 for small caps.
The engine's **15 bps/side therefore sits above the live mean and just under the value-weighted mean**
for a manager trading a universe of comparable liquidity to this one. Combined with `learnings.md`'s
own accounting (0.45%/yr ≈ 0.019 Sharpe at 3.0× turnover), the conclusion is symmetric and final:
**cost is not where this repo's edge is hiding, in either direction** — the modelled rate is not
secretly too generous. Tier A on the measurement, `validation_overlap: false`.
→ `notes/2026-08-27-live-execution-costs-implementation-shortfall.md`

**Impact is concave in size and proportional to volatility, and the flat model misses exactly one
thing that points against this repo.** The cost function is `MI = a + b·x + c·√x` in `x` = trade size
as a percent of daily volume; an F-test rejects linearity in favour of the square-root term, and the
fitted log-log slope is ≈0.35. Independently, Almgren–Thum–Hauptmann–Li fit Citigroup brokerage
executions to `I = γσ(X/V)(Θ/V)^{1/4}` for permanent impact (linear in size, `γ = 0.314`) and
`ησ|X/(VT)|^{3/5}` for temporary (concave in the *trade rate*, `η = 0.142`), and **reject the
square-root exponent at 95% from the other side**. Two claims survive both datasets and are the
transferable ones: **concavity** (the exponent itself is calibration, not a constant — the two studies
bracket ½), and **cost is denominated in volatility** — the temporary function needs no stock-specific
correction at all once expressed as a fraction of `σ`. A flat bps charge is therefore
*volatility-blind*, and a cross-sectional momentum basket systematically holds the high-volatility
tail, so the engine under-prices the champion's book specifically, by a multiplier. **The magnitude
does not change a verdict**: even a 1.5× multiplier leaves the drag under ~0.03 Sharpe, inside the
paired standard errors session 11 derived. Recorded so the flat-cost caveat is stated correctly rather
than assumed neutral. Also from the split: patience reduces only the *temporary* term (as `T^{3/5}`)
while 85–90% of measured impact is **permanent**, so slower execution attacks the small half of the
cost — a declined idea with a mechanism. Tier A / B, no overlap.
→ `notes/2026-08-27-market-impact-functional-form-and-trade-rate.md`

**The published "momentum does not survive costs" verdict is correctly scoped, and its scope is not
this repo.** Two tier-1 papers of the same year reach opposite conclusions on the repo's own champion
family. Lesmond–Schill–Zhou show the signal **selects for expensive stocks** — winner and loser
portfolios run 18–61% and 30–75% above the untraded middle portfolio on four independent cost
estimators — and conclude the gross spread is bounded by the friction that prevents its arbitrage.
Korajczyk–Sadka, studying **long-only winner portfolios** (this repo's setting, chosen because they
decline to model short execution), reframe the question as **capacity**: proportional costs are
size-independent but price impact is not, so the output is a break-even fund size — roughly $200M
equal-weighted, $2bn+ value-weighted, $4.5–5bn liquidity-weighted (normalised to end-1999 market cap).
Post-impact the **pre-cost ranking of weighting schemes inverts**: value weighting beats equal
weighting because it trades liquid names. The two papers agree about equal-weighted micro-cap
momentum and disagree about generalisation, and the disagreement is entirely about the cost
function's shape and level — which the live-execution evidence adjudicates **against both, in the same
direction**: a linear TAQ-calibrated impact model (Korajczyk–Sadka's) overstates a patient trader's
cost by ~3× at 2% of daily volume and by nearly an order of magnitude at 10%, and Lesmond et al.'s
proportional estimates run higher still (their own spreads are 1.18×–5.55× Korajczyk–Sadka's).
**Two structural results survive the cost-level correction untouched**, and both cut against importing
published momentum magnitudes: the composition result above, and that **53–70% of the long-short
momentum spread comes from the short leg** — the side a long-only book cannot trade. Tier A on both,
US-only on both, no overlap.
→ `notes/2026-08-27-momentum-net-of-costs-debate.md`

_Net: the cost axis is **closed on both halves**. The rate the engine charges is right, so no
strategy fails here for a cost-model reason; and the literature's standing objection to momentum
net of costs is a claim about equal-weighted micro-cap books measured with estimators that overstate
a patient trader's cost. What the session adds that is not a closure is **one caveat and one
discount**: every Sharpe in this repo is a **small-fund Sharpe** with no term that degrades as
notional grows, and a long-only implementation of a published long-short momentum effect should be
expected to capture **roughly a third** of it before any other adjustment._

## Cross-cutting principles

**Published predictors decay by roughly half, and the surviving half lives largely where this
repo cannot trade.** McLean–Pontiff (2016), across 97 published cross-sectional predictors:
~26% lower returns out-of-sample but pre-publication (an upper bound on the data-mining
component) and ~58% lower post-publication (the extra ~32pp attributed to arbitrage capital
arriving once the result is public). Decay is *larger* for predictors with bigger in-sample
returns, and surviving predictability concentrates in high-idiosyncratic-risk, low-liquidity
stocks. Three consequences for this lab: (a) any performance expectation carried in from
literature deserves roughly a halving before it is a fair prior, more if the published effect
was spectacular; (b) a large slice of the published anomaly zoo is **structurally unavailable**
on a ~145-name universe of large liquid global stocks and ETFs — an instrument-set problem no
signal work fixes; (c) it is the external justification for the DSR gate, and a reason to take
seriously the learnings-file note that the recorded trial count understates the true number of
candidates attempted, i.e. realized selection bias here is somewhat worse than the deflator
assumes. Tier A. → `notes/2026-08-17-mclean-pontiff-publication-decay.md`

**Literature converges with the lab's own "signal definition is exhausted, construction is
open" conclusion.** The decayed, partly illiquidity-bound published-signal population is
exactly the pool the lab has been drawing from in its refuted re-scoring attempts (52-week-high
proximity, residual momentum ×2, information discreteness). Portfolio-construction and
rebalance-mechanics edges are *not* part of the population McLean–Pontiff study and do not
inherit its decay estimate — a real asymmetry in favor of the axis the lab is already working.

**Separate mean-shifting mechanisms from dispersion-shrinking ones before crediting a
construction change.** The construction literature contains both, and they look identical in a
single backtest. Tranching across rebalance dates is claimed by its own literature to shrink
the *spread* of outcomes around an unchanged mean; banding is claimed to raise the *net* mean
by suppressing low-information trades. The lab's overlap result is a mean claim, which neither
source establishes — it stands on the repo's own evidence (higher return at less than half the
turnover, and pruning stale names hurting on three axes at once). The practical rule: ask of
any construction change whether it is supposed to move the centre or narrow the distribution,
and remember that a single backtest of a discretely rebalanced strategy is one draw, so gaps
smaller than the timing-luck scale are not evidence.
→ `notes/2026-08-17-rebalance-timing-luck-tranching.md`,
`notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`

**Grade a weighting scheme by how many noisily-estimated parameters it needs.** This is the one
principle that unifies the lab's weighting results with the literature: schemes that estimate
nothing (equal weight; signal-proportional magnitude weight) carry no estimation error, while
schemes needing a covariance matrix or a return forecast per asset pay for it out-of-sample,
worse the more assets there are relative to sample length. It predicts, without any repo data,
both that magnitude weighting should survive and that inverse-vol/risk-parity weighting should
not — matching what the lab found twice. Any future weighting proposal should be triaged on
this axis before it costs a trial.
→ `notes/2026-08-17-naive-vs-optimized-weighting.md`

**Long-short results do not transfer to a long-only book by default — now with two independent
instances, which makes it a rule rather than an anecdote.** Nearly all the momentum literature's
headline objects are winners-minus-losers spreads. The first case found was crash-risk
management, where the entire mechanism lives in the short leg and the long-only translation is
not merely weaker but *differently signed in its diagnostics*. The second is time-series
momentum: its "crisis alpha" payoff requires flipping short as a decline develops, so long-only
the rule keeps the whipsaw cost and discards the reason to want it. Treat "which leg generates
this?" as a mandatory question for every momentum or trend source, asked before implementability.

**Second mandatory question, from the same drawer: which side of the spread does this strategy
sit on?** Some premia are compensation for *providing* a service to other traders, and a
cost-paying implementation takes the losing side of exactly the trade that pays. Short-term
reversal is the clear instance — its return is the market-making margin, so a book that
crosses the spread to trade it is buying the thing it is trying to sell. This is categorically
different from an expensive-but-viable strategy: no band, no slower cadence, no
cost-mitigation technique changes the sign. Ask it of any high-frequency, liquidity-flavoured
or contrarian source before asking whether the turnover is affordable.
→ `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`

**A published alpha is not a portfolio — check what the real-time investor would have to
estimate.** Two of the strongest results reviewed here are reported as regression intercepts
or as scaled series normalized with a full-sample constant. The volatility-timing case makes
the gap explicit: the spanning-regression alpha implies a combination of managed and unmanaged
legs whose weights are the regression coefficients, fitted on the whole sample; estimated from
past data only, the same strategy underperforms simply holding the unmanaged portfolio, and
the reason is structural instability in those very coefficients. The general rule: **translate
any headline result into the position an investor holds at each date, then count which inputs
of that position were unavailable at the time.** This is the same estimation-error law as the
weighting and combination results, arriving as a replication failure rather than as theory,
and it is a reason to prefer mechanisms whose parameters are set by construction over
mechanisms whose parameters are fitted.
→ `notes/2026-08-17-volatility-timing-managed-portfolios.md`

**A published factor's construction conventions are part of its result, and the lab's hardest-won
lesson has an independent tier-1 instance.** The lab spent four trials discovering that its
champion's "basket-own vol-spike trim" was silently reading an eleven-name legacy cohort, and
distilled it as *before crediting a component, check what its code actually reads*.
Novy-Marx–Velikov show the same failure at the scale of a famous factor: BAB's rank weighting is
a back door to equal weighting, its hedging-by-levering is a back door to hedging with the
equal-weighted market, and its beta estimator is algebraically a five-year regression beta times
a short-to-long volatility ratio rather than a beta. None of the three is signalled by the
component's name. The generalised screen is one line of algebra, not a backtest: **write down
what a construction actually computes in primitive terms, and compare it to what the source says
it computes.** Two live uses here — the FP-beta identity is a reminder that a
short-over-long realized-vol ratio is *its own signal* rather than a proxy for a level (the
champion's 21d/252d trim is the same shape), and any imported factor should be re-derived this
way before its citation weight is treated as transferring.
→ `notes/2026-08-18-defensive-equity-replication-and-construction.md`

**Group-neutralise a signal only when the signal is mechanically confounded with the grouping.**
The literature contains an apparent contradiction with the lab: Asness–Frazzini–Pedersen find
industry-neutral BAB *beats* ungrouped BAB, while the lab's sector-neutralized momentum z-score
lost badly (Sharpe 1.03 → 0.87, with turnover up). They are not in conflict, because the two
neutralisations remove different things. Beta is *mechanically* linked to industry membership —
utilities are low-beta as a category — so the industry tilt is a confound the raw sort picks up
for free, and removing it isolates the intended bet. A momentum z-score has no such mechanical
sector link, and the lab's own records show top-momentum names already span sectors; there the
group constraint removes information rather than confounding. The rule costs no trial: **before
neutralising, name the mechanism by which the signal would load on the group even if the effect
were absent.** If there isn't one, neutralisation is a diversification reflex, and the lab has
already priced it.
→ `notes/2026-08-18-low-risk-investing-industry-neutral.md`

**Ask what a signal's benchmark is — zero, or the cross-sectional mean — because the answer is
worth a market position.** A rule that compares an asset's past return to zero (time-series)
carries a time-varying net long in risky assets; a rule that compares it to the cross-sectional
mean (cross-sectional) does not. The gap between the two families' measured performance is
that position, and at long ranking horizons it is mostly the *static* premium of simply being
invested rather than any timing skill. A long-only, fully-invested book already holds that
position permanently, which means (a) it cannot gain the risk-premium half from any
time-series overlay, only lose it, and (b) any comparison between this repo's cross-sectional
construction and a published time-series result is apples-to-oranges until the net-long drift
is decomposed out. The same benchmark choice also determines what the signal can see at all:
a zero-benchmark rule is blind to short-horizon reversal, which is unambiguously present
cross-sectionally. → `notes/2026-08-17-cross-sectional-vs-time-series-construction.md`

**Averaging beats selecting, whenever the selection would have to be estimated.** This is the
same law already recorded for weighting schemes, and it now has three separate instances across
three literatures: portfolio weights over assets (1/N beats estimated-optimal), combination
weights over forecasts (simple mean beats estimated-optimal — the combination puzzle), and
estimation-window choice under breaks (averaging over windows beats locating the break and
trimming). In every case the estimator that estimates nothing beats the estimator that estimates
something noisy, and the advantage is largest exactly when the sophisticated answer would be
close to the naive one. The general form: **whenever a design choice would require estimating a
quantity from a short noisy sample, holding several values of that choice simultaneously at
equal weight dominates trying to pick the right one.** Applies to weights, to lookbacks, to
formation dates. It is also a warning about the shape of any future refinement — "weight the
recent tranches more", "weight the better sleeve more", "pick the right lookback" are all the
same mistake in three costumes.
**Strengthened and bounded 2026-08-19.** Two amendments, both from tier-1 sources. *Stronger:*
averaging does not merely beat *feasible* selection — in Hansen's Monte Carlo it beats the
**infeasible optimal** single model, chosen with oracle knowledge, in many parameterisations.
So "which vintage / which window is best?" is the wrong question, not just an unanswerable one.
*Bounded:* estimated weights are provably optimal when four conditions hold — an unbiased
in-sample estimate of the loss being minimised, a nested ordered ladder of components,
conditionally homoskedastic errors, and a sample large relative to the weight count. This repo
fails all four (a deflated-Sharpe objective whose in-sample estimate is upward-biased by
construction; heteroskedastic returns; components that are not one nested ladder; a short
sample). Equal weights stay correct here, now for stated and falsifiable reasons rather than as
a prohibition.
→ `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
`notes/2026-08-17-averaging-over-estimation-windows.md`,
`notes/2026-08-17-naive-vs-optimized-weighting.md`,
`notes/2026-08-19-model-averaging-mallows-weights.md`

**Averaging can only move what is nonlinear — so ask, before any ensemble or vintage
proposal, whether the per-component output is a nonlinear function of the data.** Bagging
leaves additive statistics unchanged: the entire effect of averaging perturbed fits lives in
interaction terms of order ≥ 2, and the size of the gain is the base procedure's *instability*
(the variance of the fit across perturbed datasets), which is zero for a stable procedure —
bagging a nearest-neighbour classifier is a measured, literal no-op. For a linear map from
score to weight, averaging the portfolios equals the portfolio of the averaged score, and the
whole idea collapses before it costs a trial; it is the **threshold** — buffer, top-N, cap,
trim — that makes the two operations different objects. This is the general form of the lab's
own finding that collapsing lookbacks into one score before selecting discards the part that
pays, and it is derivable on paper with no data. Corollary with the opposite sign, equally
useful: the crossover is real, so bagging a *stable* component is mildly harmful rather than
neutral — "average over more things" is not a free move to apply everywhere.
→ `notes/2026-08-19-bagging-averaging-unstable-predictors.md`

**Name which term of the risk-adjusted-return identity a design change moves, because they
have wildly different marginal value.** `IR = mean(IC)/sqrt(σ_IC² + φ/N)`, scaled by a transfer
coefficient `TC` for constraints. Four levers: better signal (`mean(IC)`, linear, the only
unbounded one); more independent bets (`N`, `√N` and saturating — worthless once `φ/N ≪
σ_IC²`); less *strategy risk* (`σ_IC`, the term that dominates once `N` is moderate and the one
that sets an absolute ceiling `IR ≤ mean(IC)/σ_IC`); and fewer binding constraints (`TC`,
0.3–0.8 under realistic long-only-style constraints). The repo's ~145-instrument universe has
already spent the `N` lever, which is why widening the basket was a no-op; averaging
weakly-correlated formation vintages acts on `σ_IC`, which is why it was not. Ask of any
proposal which term it touches before asking whether it is implementable. Caveat that must
travel with it: the framework is benchmark-relative, so **no IR number from it is comparable to
this repo's total-Sharpe gate**, and measuring an IC scores returns and is therefore not a free
diagnostic. → `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`

**But ensembling only applies to components that estimate the same quantity — mixing different
return streams is a different operation with a different sign.** Forecast-combination theory is
about multiple noisy estimates of *one* target; its variance reduction is free because the
components are interchangeable in expectation. Allocating capital across strategies with
*different* expected returns is not that, and the lab has measured the difference: blending 20%
into the ~0.5-Sharpe ETF sleeve cost roughly the same Sharpe whether the other leg was plain or
buffered momentum — a dilution tax that does not shrink as the core improves. So the standing
test before any ensemble candidate: **are the components estimates of the same thing, or are
they different things?** Six formation vintages of one signal pass. Momentum plus an ETF sleeve
fails. The literature endorses only the first, and the lab's own record already shows what the
second costs. → `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`
**Amended 2026-08-19 and again 2026-08-20.** The test above is right about the **gross** axis and
incomplete on the **net** one: legs that estimate *different* quantities still cancel each other's
rebalancing trades, so a second leg's true contribution is `(gross dilution) + (turnover saved by
trade cancellation) × (cost rate)`, and only the first term has ever been measured here. The
amendment does not overturn any verdict on this repo — the recoverable term is bounded by a total
cost drag of ~0.019 Sharpe against a dilution tax of ~0.02 per 20% of capital — but it retires the
blanket claim that an extra leg costs turnover.
→ `notes/2026-08-20-trading-diversification-combining-signals.md`

**Which cost model you assume decides which mechanism you get — and this repo's two best
construction mechanisms are the two canonical answers.** The frictions literature splits on the
shape of the cost function, and the split is not cosmetic. Under **quadratic** (market-impact)
costs the optimal policy is *partial adjustment every period* toward a target that is itself a
forward-looking average — no period of inaction, and the optimal book turns out to be an
exponentially weighted average of past targets. Under **proportional or fixed** costs the optimal
policy instead "exhibits periods of no trading" — a no-trade region, i.e. a band. This repo pays a
flat 15 bps/side, which selects the band branch; the champion's hold-25/enter-15 hysteresis buffer
is that band, and its six formation tranches are (structurally) the averaging that the other
branch derives. Two consequences. (a) The two are **complements by construction**, answers to
different questions, not two versions of one idea — so neither is redundant with the other, and
"simplify one away" is not a free move. (b) Before importing any friction-aware result, ask which
cost model produced it, because a partial-adjustment prescription and a no-trade-band prescription
do not substitute for each other.
→ `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md`,
`notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`

**Under costs, a signal is worth less than its gross alpha in proportion to how fast it decays —
so ask any proposed leg for its half-life before asking for its Sharpe.** Absent costs, alpha
decay is irrelevant: the investor re-optimises for free and only current expected returns matter.
With costs it becomes first-order, because the benefit of a trade must accrue for long enough to
amortise the trade. The closed form is a per-signal divisor `(1 + φ_k a/γ)` — persistent signals
shrunk least, fast ones most, and the *relative* penalty on the fast signal **growing with the
cost rate**. This is a free triage question that costs no trial, and it independently reproduces
the lab's record: reversal legs (half-life of days) kept subtracting value once turnover was fixed
directly, while momentum legs (half-life of months) did not. It arrives at the same place as the
liquidity-provision argument that closed family 4, by a completely different route. Boundary: the
formula's *prescription* — weight legs by persistence — requires estimating decay rates, a
covariance matrix and a cost matrix, so it is screen #1's expensive class and is **not** grounds to
reweight the champion's horizon legs by lookback length. The *question* is free; the answer's
implementation is not.
→ `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md`

**Selecting on a sample objective inherits that objective's curvature, and estimation noise
travels with portfolio variance — so a criterion with too little curvature systematically picks
the high-variance candidate.** The parametric-portfolio literature reaches this by a route the
folder has not previously recorded: overfitting in a weight-policy fit is *positively linked to the
variance of the resulting portfolio*, which makes the natural regularisation not a penalty on
parameters but **fitting with a more concave loss than the one you actually care about** —
estimate at risk aversion `γ* = γ + λ`, hold as the `γ` investor. Two uses here, neither of them a
candidate. First, it is a general warning about any in-sample-maximising selection step, and this
repo has one in a frozen file: promotion scores raw validation Sharpe, and `learnings.md`'s ⚠
standing protocol concern records validation rising monotonically while the holdout falls, with
the winners getting more concentrated and faster-rotating each step — the exact shape this
mechanism predicts. It is recorded here so the human reviewing that concern has the literature's
name for it and its stated remedy (*select on a more risk-averse criterion than your target*).
Second, it is the reason to keep declining "fit the weighting coefficients on the training split":
the source's own finding is that parsimony in the fitted parameter vector does **not** buy
protection, because the objective depends on properties of a return distribution that was never
modelled.
→ `notes/2026-08-20-parametric-portfolio-policies.md`

**A binding constraint is a zero-parameter estimator, which is why constraints keep beating
corrections — and the folder's long-only accounting has been one-sided.** Everything recorded
here about constraints until now priced them as *leakage*: the transfer coefficient
(`IR ≈ TC · IC · √BR`, `TC ≈ 0.3–0.8`), and three separate sources reporting their constrained
variant as materially weaker than the unconstrained one. Every one of those is a claim about
**signal transfer given a correct alpha**. There is a second, opposite-signed effect on the same
constraint: it is algebraically identical to shrinking the covariance estimate, in the direction
estimation error actually goes, at the cost of estimating nothing. Both are real and they run
against each other; which dominates depends on whether the binding constraint stands between the
book and a *good* estimate or a *noisy* one. This is the same law as 1/N-beats-optimisation and
simple-mean-beats-optimal-combination, arriving from a third direction — and it comes with a
boundary worth carrying: the same source finds that *once no-short is imposed*, the
sophistication of the covariance estimator largely stops mattering. So for any covariance-based
**diagnostic** the lab runs on a long-only book (risk contributions, effective bets,
diversification return), a plain trailing sample covariance is the right input and reaching for
a factor model or a shrinkage estimator is not warranted. It remains no licence for
covariance-based *objectives*, which stay closed by the ERC theorem and two trials.
→ `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`

**Separate the return a book earns from its signal from the return it earns from rebalancing —
they are different mechanisms and they want opposite things.** A rebalanced portfolio earns
`½ Σ_i w_i(σ_i² − σ_ip²)` over the weighted average of its constituents' geometric returns,
and it earns it for a *contrarian* act: constant weights force selling what rose in relative
value and buying what fell. A buy-and-hold book earns none of that, but earns a different
increment for the *opposite* behaviour — letting winners grow — at the price of a drifting risk
profile. A cross-sectional momentum book that resets to signal-proportional targets each month
does neither cleanly: it trims within the held set relative to price drift, then hands the term
back by chasing the signal with the targets themselves. Three consequences. (a) Concentration
now costs on two axes, not one: the folder had priced it only through drawdown, and
`σ_i² − σ_ip²` says a book whose risk collapses onto few directions also forgoes the
diversification return. (b) Turnover reduction is not free on the *gross* axis, so ask of any
such proposal whether it throttles **membership churn** (which forgoes little of the term) or
**weight resets** (which is where the term lives) — the folder's endorsement of banding survives
that split, but does not extend past it. (c) The term is an accounting decomposition, **not
alpha**: a book can have a large one and a poor total return, and nothing in the source models
transaction costs, so it is not a reason to rebalance more often.
→ `notes/2026-08-21-diversification-return-and-rebalancing.md`,
`notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`

**[AMENDED 2026-08-22 — the attribution above is half wrong, and the correction changes what the
lab should want.]** The identity survives; the sentence "a buy-and-hold book earns none of that"
does not. Cuthbertson et al. derive that an **unrebalanced** book also earns growth above the
weighted average of its constituents' growth, that rebalanced and buy-and-hold books begin with
**identical** expected growth rates, and that they diverge only as buy-and-hold weights drift toward
being less diversified. What the rebalancing trades themselves add is **zero in expectation under
IID returns**, positive only where relative prices mean-revert and **negative where they trend**. So
the corrected principle is: the return a diversified book earns over its constituents' average is a
*volatility-drag* effect available to any diversified holder, and the *incremental* effect of
resetting weights is a bet on relative-price mean reversion. **A cross-sectional momentum book is
short that bet.** Practical consequences, replacing (b) above rather than adding to it: throttling
**weight resets** is not forgoing a prize on this book — on a continuation signal it is removing
trades with negative expected value *and* a 15 bps/side charge, which is the strongest argument the
folder has yet recorded for a hold-band, and is a different argument from the cost one
`learnings.md` retired. Consequence (a) stands unchanged and is now doubly sourced: concentration
forgoes the diversification term, and Fernholz–Karatzas's `γ*_π` makes that forgone amount
measurable from holdings alone. Consequence (c) stands and is strengthened — the term is accounting,
not alpha, and this correction removes the last reading under which it looked like free money.
→ `notes/2026-08-22-rebalancing-return-attribution-critique.md`,
`notes/2026-08-22-excess-growth-and-return-decomposition.md`

**A constraint is a shrinkage intensity, not a verdict — grade it by how binding it is, not by
whether it exists.** The folder has accumulated a strong prior that constraints and equal weights
beat estimated corrections, and session 8 added the argument that a binding weight constraint *is*
covariance shrinkage. The missing half arrived with the `ℓ1` identity: under full investment,
long-only is the infinite-penalty endpoint of a continuous path, with a critical `τ₀` marking where
it starts to bind — and on one of two asset sets in the same study the endpoint was demonstrably
past the optimum, the constrained book beaten by one allowed a little shorting. Both directions are
therefore on record, and neither is a general law. The rule to carry: **cost and benefit of a
constraint both scale with how binding it is, so the question is always "how far past the
unconstrained optimum does this push, on this universe?" and never "are constraints good?"** This is
the explicit guard against the taboo risk session 8 flagged. Its corollary for this repo, where
long-only is not optional: the constraint is doing unpriced regularisation work *and* unpriced
leakage, the folder has only ever counted one of them at a time, and the one quantity that would
price the leakage — the transfer coefficient's 0.3–0.8 range — remains the only number available.
→ `notes/2026-08-22-long-only-as-l1-regularization.md`,
`notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`

**Check the currency before importing a quantity — and know that for log growth there is no
exchange rate.** Everything this folder has imported is denominated in one of four units: forecast
MSE (bagging, model averaging), information ratio (the fundamental law), log growth (stochastic
portfolio theory), or net Sharpe (the gate). Each crossing between them needs an argument, and the
folder has been building them one at a time — session 7 crossed the friction gap, session 9 the
growth-identity gap. **Session 10 establishes that the log-growth crossing does not exist.**
Maximising `E[log W]` is not an approximation to any other risk-scored objective at any horizon; the
wealth-equivalent cost of the substitution *grows* exponentially in the horizon rather than
shrinking; and the natural repair — treating `(mean-log, variance-log)` as a sufficient pair — is
itself a limit-interchange fallacy whose error also diverges. The one exact bridge on offer,
`g* = r_0 + ½·SR²`, holds at the growth-optimal *leverage* and nowhere else, so it is unavailable to
a book capped at gross leverage 1.0. Practical rule, free: **before importing a theoretical quantity
as a diagnostic, ask whether it is denominated in the unit the gate reads; if it is denominated in
log growth, it is an accounting split of a realised quantity and never a scoring axis.** This is not
a retraction of `γ*` as an identity — an accounting decomposition is true regardless of anyone's
objective — only of its promotion to an axis, which is the reading `learnings.md` then measured and
found null.
→ `notes/2026-08-23-geometric-mean-maximization-fallacy.md`,
`notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md`,
`notes/2026-08-22-excess-growth-and-return-decomposition.md`

**Grade estimated parameters by *type*, not only by count — means are ~10× variances and ~20×
covariances, and the multiple rises as the book gets more aggressive.** Screen #1 has always counted
noisily-estimated parameters. The capital-growth literature weights them: the certainty-equivalent
loss from errors in expected returns runs about an order of magnitude above that from errors in
variances and two orders above covariances, and the ratio is a **function of risk tolerance** —
roughly 3× at high risk aversion, 10× at moderate, 20× at low. Two consequences, both free. (a) The
folder's blanket "covariance-based objectives are the expensive class" is directionally right and
*understates* the ordering: a scheme that estimates expected returns is much worse than one that
estimates a covariance, and the champion estimates neither (its score is an observed
cross-sectional statistic, not a forecast of a mean) — a stronger endorsement than the parameter
count alone supplied. (b) The multiplier rising as risk aversion falls means **a more concentrated,
more aggressive book pays more for the same estimation error**, which is a second and independent
reason — beside drawdown — to read the repo's concentration ladder as raising fragility.
→ `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md`,
`notes/2026-08-17-naive-vs-optimized-weighting.md`

**Two literatures, arriving independently, say a six-year window cannot resolve differences of this
size — and the folder should stop quoting Sharpe gaps without an error bar.** From the estimator
side: `SE(ŜR) ≈ sqrt((1 + ½SR²)/T)`, which at the champion's Sharpe over 1,562 validation days is
≈ 0.40, against a total promotion ladder of 0.364. From the capital-growth side: two strategies
differing by 10pp of annual mean at 10% volatility separate at 95% confidence in five years, but
**doubling the better one's volatility pushes the requirement to 157 years**, and an edge of 1.0%
against 1.1% needs two million trials for an 84% chance of the better one dominating. Neither
statement is about this repo's data; both are computed from parameters and sample lengths. The rule
to carry: **quote a standard error alongside any Sharpe, and treat "candidate A beat candidate B on
validation" as a statement about a point estimate rather than about the two strategies.** The honest
counterweight, which must be stated whenever this is used: these are the precisions of *individual*
Sharpe ratios, and the difference between two nearly-identical books on the same window is estimated
far more precisely than `√2·SE` — neither source derives that paired standard error, so this is a
reason to attach uncertainty to the gate's readings, **not** a proof that its increments are noise.
**Amended 2026-08-24: the paired standard error is now derived and the counterweight is quantified.**
It is `SE(ŜR)·√(2(1−ρ))` to an excellent approximation at daily frequency, exactly
`SE(ŜR)·√((1−ρ)(2+Sh²(1+ρ))/(1+½Sh²))`, so the discount for pairing is precisely `√(1−ρ)`. The
discipline stands unchanged in shape and is now sharper in content: **quote the paired error bar,
computed from the candidate–champion correlation, never the single-strategy one.**
→ `notes/2026-08-23-statistics-of-sharpe-ratios.md`,
`notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md`,
`notes/2026-08-24-testing-differences-of-sharpe-ratios.md`

**Multiple-testing penalties are not one thing — the error rate being controlled is a *choice*, and
this folder has been quoting the consequences of one choice as if they were arithmetic.** Two
families exist. **FWER** procedures (Bonferroni, Holm; and any extreme-value threshold that grows in
the trial count, which includes the deflated Sharpe ratio's `E[max{ŜR_n}]`) control the probability
of even one false discovery, and their bar rises monotonically as trials accumulate. **FDR**
procedures (Benjamini–Hochberg–Yekutieli) control the *proportion* of discoveries that are false,
and their bar **stabilises** rather than diverging, because at fixed `α` the law of large numbers
pins the realised rate. The finance-specific recommendation in the literature is FDR, on the ground
that an investor cares about the share of allocated strategies that are duds, not about never
allocating to one. Two consequences, both free and both explanatory only. (a) `learnings.md`'s "every
trial permanently raises the bar" is true of the gate this repo has, and is **not** a general law —
it is a property of controlling family-wise error. (b) The penalty's dependence on the *level* of the
Sharpe ratio, not only on the trial count, is a real disagreement between the two published
corrections: the haircut framework savages Sharpe ratios below ~0.4 and leaves those above 1.0
roughly intact (≤ ~25%), while a `E[max]`-style deflator is driven by `N` and by the cross-trial
dispersion. Neither observation licenses anything: `engine/` is frozen and its thresholds are a human
decision. Both belong in the folder because the gate's machinery is now covered and its assumptions
should be legible.
→ `notes/2026-08-24-multiple-testing-haircut.md`, `notes/2026-08-24-deflated-sharpe-ratio.md`

**A prior may buy a lower bar, and it is strictly zero-sum — which is why "this idea is
well-motivated" is an argument a session may not make on its own behalf.** Weighted multiple testing
preserves error control under *any* non-negative a-priori weights whose mean is one; relaxing one
hypothesis's threshold is paid for, unit for unit, by tightening others. So the intuition the folder
has repeatedly bumped into — that a theory-derived candidate deserves an easier test than a knob
sweep — is correct and formal, and it is also a *budget*, not a dispensation. Three disciplines
follow, and they matter more here than the theorem does. (i) **A prior asserted after the result is
worth nothing**; the weights must be fixed before the data are seen, which is what makes
`CLAUDE.md`'s hypothesis-before-code rule load-bearing rather than decorative. (ii) **The size of the
concession is small**: from a long-shot prior to even odds is about 1.0 in t-units, and even at even
odds the required threshold is *above* the naive one — so a prior relocates a bar, it never removes
one. (iii) **A discount cannot be manufactured from the data being scored**: estimating weights by
splitting the sample does not beat using the whole sample unweighted. The general shape is the same
one this folder keeps rediscovering in other vocabularies — an estimated correction is only worth
what its information came from, and information from inside the sample is not new information.
→ `notes/2026-08-25-prior-weighted-multiple-testing.md`,
`notes/2026-08-25-bayesianized-p-values-prior-odds.md`

**Distinguish a predicted attenuation from an unpredicted inversion before calling an
out-of-sample result a failure.** Under any positive shrinkage — i.e. under any prior that the
effect might partly be luck — the expected out-of-sample estimate is strictly *smaller* than the
in-sample one. A candidate that scores lower on a later split than on the split it was selected on is
therefore behaving exactly as correct inference predicts, and the level drop on its own is not
evidence of anything. What *is* evidence is a change in the **relationship**: the two splits' rank
correlation flipping sign, or the two series moving monotonically in opposite directions. This is a
sharpening, not a softening: applied to `learnings.md`'s ⚠ standing protocol concern it removes the
half that any Bayesian would have predicted and leaves the half that nobody would.
→ `notes/2026-08-25-hierarchical-bayesian-factor-replication.md`

**A data-construction bias is not a level discount — ask which *claim* it corrupts, and by how much
more than the level.** The reflex on learning a sample is selected is to shade the expected return
down and carry on. That is usually the smallest of the available errors. Conditioning a cross-section
on realised return moves average risk-adjusted return by well under a percent a year in the canonical
calibration, but reshapes the joint distribution of return and volatility enough that a **5%** annual
truncation makes a test of "no cross-sectional persistence" reject more than half the time. The two
effects are not the same size and are not even the same kind: one is a bias in a moment, the other is
a bias in an *inference*. So the question to ask of any selected sample is not "how much should I
shade the mean?" but "**which of my claims is a claim about the thing this selection reshaped?**" —
and a strategy family whose entire assertion is that relative past performance predicts relative
future performance is maximally exposed. Two corollaries travel with it. The **sign is a property of
the selection rule** and must be derived, not assumed: sequential per-period survival induces
apparent persistence, selection on whole-sample cumulative performance induces apparent reversal.
And the correction is **an assumption you state, not a constant you apply** — the standard "subtract
the survival bias" adjustment is correct only in the limit where all units share one completely
unknown expected return, and is too severe otherwise. This generalises past survivorship to every
selected sample the lab reads, its own trial log included.
→ `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`,
`notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md`

**A "net of costs" verdict is a claim about an execution style, not about a strategy — so read the
cost estimator before reading the conclusion.** Two tier-1 papers reached opposite conclusions about
the same strategy family in the same year, and the entire difference was the cost function: one
applied a proportional estimate inferred from daily price behaviour, the other a linear price-impact
model calibrated to intraday trade-and-quote data. Measured against live institutional executions,
both overstate what a *patient* trader pays — the linear model by roughly 3× at 2% of daily volume
and by nearly an order of magnitude at 10%; the proportional family by more still. The reason is
structural rather than a calibration slip: aggregated market data measures the average participant,
who includes informed insiders, impatient traders and liquidity demanders, and a patient limit-order
book is by construction not that participant. **The rule.** When importing a net-of-cost result, ask
what produced the cost number, and apply the discount before the conclusion, not after: a verdict
built on a linear TAQ-calibrated impact model is measuring a different trader. This never invalidates
a paper's *gross* result or its *cross-sectional* patterns — those are untouched — only its net
verdict. Two riders that keep it from becoming a blanket dismissal of costs. First, the correction
runs the other way for **capacity**: the same concavity that makes flat and linear models overstate
small trades means they *understate* nothing, so a strategy declared dead on cost may be alive at
small size and dead at large, which is a break-even fund size rather than a verdict. Second, the
composition results these papers establish — *which* stocks a signal makes you trade — survive the
cost-level correction entirely, and are usually the more transferable half.
→ `notes/2026-08-27-live-execution-costs-implementation-shortfall.md`,
`notes/2026-08-27-momentum-net-of-costs-debate.md`,
`notes/2026-08-27-market-impact-functional-form-and-trade-rate.md`

## Candidate ideas for the strategy agent

Ranked, mechanism-only. Each links its note; tier and overlap flags shown. The top entries are
free — screening rules and interpretation rules that cost no trial — followed by actual
hypothesis fodder, then anti-candidates.

1. **Triage rule before any weighting-scheme trial: count the noisily-estimated parameters.**
   Schemes estimating nothing (equal weight, signal-proportional magnitude weight) carry no
   estimation error; schemes needing a covariance matrix or per-asset return forecast pay for
   it out-of-sample, and worse as the asset count rises relative to sample length (calibrated
   requirement: thousands of months of data at this universe's breadth). Applying this rule
   retrospectively reproduces both of the lab's weighting verdicts. Use it to kill
   risk-weighted proposals before they cost a trial. Tier A, no overlap.
   → `notes/2026-08-17-naive-vs-optimized-weighting.md`
   **Second half of the same screen, added 2026-08-18 and sharper because it is a theorem
   rather than a calibration: risk-balancing schemes are optimal only under constant
   correlation AND equal component Sharpe ratios.** Equal-risk-contribution weighting equals
   the maximum-Sharpe portfolio under exactly those two conditions and not otherwise. So any
   proposal to weight sleeves or legs by risk can be checked before it is built by asking
   whether its components have comparable Sharpe ratios — the lab's do not (≈1.1 momentum
   basket versus ≈0.5 ETF sleeve), which is why both inverse-vol trials lost. Two corollaries
   worth carrying: for **two** components ERC *is* inverse-vol regardless of correlation, so
   the lab's blend was correct risk parity and no better-specified version exists to try; and
   the general solution `x_i ∝ 1/β_i` (beta to the portfolio) means a *more* correct
   implementation would tilt further toward the diversified low-return leg, not back.
   → `notes/2026-08-18-risk-parity-equal-risk-contribution.md`
   **Boundary added 2026-08-21, and it cuts the other way for diagnostics only.** The screen
   grades a scheme by parameters estimated; a **hard constraint estimates none and does part of
   the same job**, because a binding weight constraint is algebraically a shrinkage of the
   covariance estimate in the direction estimation error actually goes. Corollary the lab can
   use: once no-short is imposed, the sophistication of the covariance estimator largely stops
   mattering, so every covariance-based *diagnostic* run on this long-only book (risk
   contributions, effective bets, diversification return) should use a plain trailing sample
   covariance — no factor model, no shrinkage estimator. Objectives built on a covariance stay
   closed. → `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`
2. **Design test before any ensemble trial: are the components estimates of the same quantity,
   or different return streams?** Forecast-combination theory endorses only the first — several
   noisy estimates of one target, equal-weighted — where the variance reduction is free. Mixing
   strategies with different expected returns is a different operation, and the lab has already
   priced it (the capital-dilution tax that does not shrink as the core leg improves). Six
   formation vintages of one signal pass this test; momentum-plus-ETF-sleeve fails it. Costs no
   trial and rules out a whole class of "blend it with something" proposals. Tier A, no overlap.
   → `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`
   **Two further free screens added 2026-08-19, same rank — both derivable on paper, both
   applying to vintage/ensemble/averaging proposals generally.**
   *(i) Is the per-component output nonlinear in the data?* Bagging leaves additive statistics
   unchanged; the whole effect of averaging perturbed fits lives in interaction terms of order
   ≥ 2, and its size is the base procedure's instability — zero for a stable procedure (bagging
   a nearest-neighbour classifier is a measured no-op). For a linear score→weight map,
   averaging portfolios *is* the portfolio of averaged scores, so the proposal is algebraically
   a no-op before it is a trial; it is the threshold (buffer, top-N, cap, trim) that makes them
   different objects. Same statement in reverse: the champion's membership rule is *subset
   selection*, the canonical unstable procedure, which is why averaging over its formation
   vintages should and does pay. Also bounds the `K` question without licensing a sweep —
   replicate counts saturate fast, so pre-register a small effect for any deeper stack.
   → `notes/2026-08-19-bagging-averaging-unstable-predictors.md`
   *(ii) Which term of `IR = mean(IC)/sqrt(σ_IC² + φ/N)` does the change move?* More names at
   one date raises `N` — a `√N` lever already saturated at ~145 instruments. Averaging
   weakly-correlated formation vintages lowers `σ_IC` (strategy risk), the term that dominates
   once `N` is moderate and that sets an absolute ceiling `IR ≤ mean(IC)/σ_IC`. Constraints
   multiply by a transfer coefficient, typically 0.3–0.8 with long-only named among the causes.
   Reproduces, from one identity, why breadth widening was a no-op and vintage decorrelation was
   not. Two attached warnings: the framework is benchmark-relative so **no IR figure from it is
   comparable to this repo's total-Sharpe gate**, and computing an IC scores returns, so it is
   *not* covered by the free holdings-only diagnostic exemption.
   → `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`
   **Sharpened 2026-08-21 — the `N` lever is unreachable rather than exhausted, and there is a
   free test of that.** The folder's reason for calling `N` saturated was "145 is a large
   number". The better reason is that what saturates is **effective dimensionality**, not the
   instrument count: `√N` counts *independent* bets, and the count of correlation eigenvalues
   `≥ 1` stops rising long before the name count does (in the one market studied, a 41-name
   universe supported no more than eight dimensions, and adding a whole extra asset class raised
   that by about one). Screen: if a proposed instrument set does not raise the eigenvalue count
   of the universe's correlation matrix, breadth widening is a no-op on paper — which
   retro-predicts both the lab's basket-breadth no-op and the buffer-band vintage axis killed at
   0.963 overlap. Honest counterweight, recorded rather than smoothed: if effective `N` here is
   genuinely small, then `φ/N` is **not** negligible against `σ_IC²` and the "saturated" claim
   is doing more work than the algebra supports. Neither reading opens a build — the instrument
   list is fixed — but prefer "unreachable" to "exhausted". Tier C sources.
   → `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`
   **A third free screen added 2026-08-20, and it is the first one that predicts the *cost* side
   of an averaging proposal rather than its return side.** *What is the correlation of the legs'
   rebalancing trades?* Legs held together trade the same instruments, so their trades partly
   cancel and only the residual is executed. Closed form for the turnover of a `K`-leg combination
   against the same legs traded in isolation: `√(eᵀΩe)/Σ_k√(Ω_kk)`, which under equal variances and
   equal pairwise trade correlation `ρ` is **`√((1+ρ(K−1))/K)`**, falling to `1/√K` at `ρ = 0`.
   The input is the correlation of `trade_{i,k} = w_{i,t+1,k} − w_{i,t,k}(1+r_{i,t+1})` — a
   holdings-and-prices statistic that scores no returns, so it is covered by the free-diagnostic
   exemption, unlike an IC. Retro-predicts the champion (recorded 3.5x vs 7.9x = 0.44 against
   `1/√6 = 0.41`, with positive vintage trade correlation being exactly what lifts the ratio).
   Use it to pre-register a turnover effect size before any vintage/ensemble trial, per
   `learnings.md`'s diagnose-first rule. Corollary that retires a folder assumption: a leg's
   marginal contribution to turnover can be **negative**, so "an extra leg costs turnover" is not
   a general truth. Tier A, no overlap.
   → `notes/2026-08-20-trading-diversification-combining-signals.md`
3. **Free closed-form triage for any proposed trend/moving-average signal: write it as its
   weight vector over past returns.** Every MA-based indicator — crossover, price-minus-MA,
   envelope, plain momentum — is algebraically a weighted average of past price changes, and its
   behaviour depends only on that weighting function's shape. Near-identical shape ⇒
   re-parameterisation, not a new idea ⇒ no trial. Cheaper and more decisive than the lab's
   existing rank-correlation diagnostic because it is derivable on paper with no data. Two
   immediate uses: check whether the refuted 200dma filter and the refuted SPY-trend switch are
   weight-shape duplicates (if so, two refutations are really one, and the lab has less evidence
   against trend overlays than it thinks), and express the champion's 6-1/12-1 composite in this
   form so any proposed extra ensemble component can be checked for real decorrelation before it
   is built. **Boundary: linear filters only** — says nothing about buffers, hysteresis, caps or
   the vol-spike trim, which is precisely where the champion's edge lives. Tier B, no overlap.
   → `notes/2026-08-17-moving-average-rules-anatomy.md`
4. **Triage rule for any imported result: which side of the spread does it sit on, and what
   would a real-time investor have to estimate?** Two independent screens that cost no trial.
   (a) *Spread side*: some premia are payment for providing a service — short-term reversal's
   return is the market-making margin — so a cost-paying implementation takes the losing side
   of the very trade that pays. This is a sign problem no band or cadence change fixes, and it
   is categorically different from "expensive but viable". (b) *Estimated inputs*: translate
   the published result into the position held at each date and count which inputs were
   unavailable then. Spanning-regression alphas and full-sample normalising constants both
   fail this, and the volatility-timing literature is the worked example — the in-sample alpha
   replicates across 103 strategies, the real-time portfolio built from it underperforms doing
   nothing. Tier A, no overlap.
   → `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`,
   `notes/2026-08-17-volatility-timing-managed-portfolios.md`
   **(c) Added 2026-08-18 — *what does the construction actually compute?*** Re-derive an
   imported factor's construction in primitive terms before granting it its citation weight.
   Novy-Marx–Velikov's worked example is one line of algebra showing the famous BAB beta is
   `[(σ_i,1y/σ_i,5y)/(σ_mkt,1y/σ_mkt,5y)] · β_i,5y` — a regression beta multiplied by a
   short-to-long volatility ratio — and that the factor's rank weighting and
   hedging-by-levering are undisclosed back doors to equal weighting. This is the lab's own
   "check what its code actually reads" lesson (which cost four trials) arriving independently
   at tier 1, and it applies to imported sources as well as to local code.
   → `notes/2026-08-18-defensive-equity-replication-and-construction.md`
   **(d) Added 2026-08-20 — *what is the signal's half-life, and which cost model produced the
   result?*** Two more one-line screens from the same drawer. *Alpha decay*: under trading costs a
   signal is discounted by `(1 + φ·a/γ)` in the optimal book — fast-decaying signals penalised
   hardest, and the relative penalty **growing with the cost rate** — while absent costs decay is
   irrelevant entirely. So ask any proposed leg for its half-life relative to the legs already
   held before asking for its gross Sharpe; this independently reproduces why reversal legs kept
   subtracting value here once turnover was fixed directly. *Cost model*: a friction-aware result
   derived under **quadratic** costs prescribes partial adjustment toward a target, while one
   derived under **proportional or fixed** costs prescribes a no-trade band. This repo's flat 15
   bps/side is the second; do not import a prescription from the first as if it substituted.
   Tier A, no overlap.
   → `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md`
5. **Design test before any group-neutralisation trial: name the mechanism by which the signal
   would load on the group even if the effect were absent.** The literature and the lab appear
   to disagree — Asness–Frazzini–Pedersen find industry-neutral BAB beats ungrouped BAB in
   every one of 49 US industries, while the lab's sector-neutralized momentum z-score lost 0.16
   of Sharpe and raised turnover. They are not in conflict: beta is *mechanically* tied to
   industry membership (utilities are low-beta as a category), so neutralising removes a genuine
   confound; a momentum z-score has no such mechanical tie, and the lab's own evidence says
   top-momentum names already span sectors, so the constraint only discards information. The
   screen costs no trial and rules out group-neutralisation, sector caps and similar
   "diversification reflex" proposals unless a confounding mechanism can be named first.
   Tier A, no overlap. → `notes/2026-08-18-low-risk-investing-industry-neutral.md`
6. **Interpretation rule before comparing anything here to a published time-series result:
   decompose the net-long drift out first.** A time-series rule benchmarks past returns against
   *zero* and therefore carries a time-varying net long position; a cross-sectional rule
   benchmarks against the *cross-sectional mean* and does not. `TS ≈ CS + NetLong × index`, and
   the whole measured gap between the families is that term — mostly the static premium of
   being invested, not timing skill, at long ranking horizons. Consequences: this repo's
   fully-invested long-only book already holds that position permanently, so a time-series
   overlay can only give it up; and any "TS beats CS" claim from the literature is not evidence
   about signal quality until the drift is removed. Also settles the standing question about
   magnitude weighting — MOP's sign-only rule answers a different question against a different
   benchmark, so it is not grounds to "correct" the champion. Tier A, no overlap.
   → `notes/2026-08-17-cross-sectional-vs-time-series-construction.md`
7. **Interpretation rule: a single backtest of a discretely rebalanced strategy is one draw
   from a rebalance-timing-luck distribution.** Timing luck is uncompensated dispersion driven
   by turnover (↑), concentration (↑) and holding count (↓); a tranched book sits near the
   distribution's centre, a single-vintage book does not. Consequence: Sharpe gaps between
   variants that differ in rebalance mechanics, if small, are not evidence. Does not threaten
   the overlap result (large, and corroborated by the pruning diagnostic), but should discipline
   how near-ties are read. Tier B, overlap assumed.
   → `notes/2026-08-17-rebalance-timing-luck-tranching.md`
8. **[BUILT — status updated 2026-08-19. Proposed session 3; the lab has since implemented it
   and explored its bracket across trials #41–#44, per `experiments/learnings.md`. Retained
   here for its mechanism, not as a live proposal.] Average over formation vintages that differ
   in lookback *length*, not only in end-date.** The champion's six tranches differ in *when* the
   signal was formed, at constant lookback; the AveW method the literature actually describes
   averages a model estimated over *different window lengths*, which brackets the unknown
   bias–variance optimum rather than sliding one window along. This is the single variant of the
   tranche family the lab has not built, and it is mechanism-motivated rather than knob-turning —
   it changes what is being averaged, not how much. Gate it behind the standard cheap diagnostic
   first: if the resulting score vectors rank-correlate as tightly as the 0.89 that killed the
   earlier inter-signal ensemble, it is a no-op and costs nothing to learn that. Equal weights
   are load-bearing — any "weight recent or better vintages more" refinement is the
   estimated-weight mistake this whole literature warns against. Tier A, no overlap.
   → `notes/2026-08-17-averaging-over-estimation-windows.md`
   **Post-build reading, added 2026-08-19.** The lab's own conclusion from that bracket —
   length-vintage and date-vintage diversity are *complements*, and the gain is coarse (it comes
   from having several windows at all, not from where inside the bracket they sit) — is what
   three separate literatures now predict jointly. Coarseness follows from the equal-weight
   optimality argument; complementarity follows from the fact that the two axes perturb
   different things (which data the fit sees vs. when it was fitted), so their instabilities are
   weakly correlated and the aggregation gain compounds; and both are bounded above by the
   post-formation reversal limit and by bagging's crossover, which say the same thing from
   different directions. **Net: this session opens no new build here and closes the spacing
   axis harder. What changes is the standing of the equal-weight choice — previously a
   convention defended by "don't estimate weights", now a positive result with four stated
   conditions under which it could be overturned, none of which this repo meets.**
   → `notes/2026-08-19-bagging-averaging-unstable-predictors.md`,
   `notes/2026-08-19-model-averaging-mallows-weights.md`
9. **Confirmation, not a new candidate — the membership buffer is the literature's
   top-ranked construction technique.** A buy/hold spread (stricter bar to enter than to hold)
   beats both slower rebalancing and liquidity screening, because the trades it suppresses are
   the low-information ones near the cutoff. The champion's hold-25/enter-15 band is exactly
   this. Recorded so nobody "simplifies" it back to a hard top-N cutoff. Tier A, no overlap.
   → `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`
10. **Standing caveat on the repo's best mechanism, not a candidate.** 1/N is a hard benchmark
    because deviations from it usually pay for themselves in estimation error, so magnitude
    weighting's wide margin over equal weight deserves scrutiny of *how* it wins — the lab's own
    records already flag where to look (maxDD widened monotonically with each concentration
    step; one validation year dominates the P&L). The square-root-dampening test is real evidence
    against the pure-variance-artifact reading, but explored one direction only. Tier A, no
    overlap. → `notes/2026-08-17-naive-vs-optimized-weighting.md`
11. **Confirmation, not a new candidate — the skip-month is load-bearing.** Both echo-literature
    sources agree the most recent month carries reversal. The champion's 6-1/12-1 composite
    already skips it. Recorded so nobody "simplifies" it to 6-0/12-0. Tier A, no overlap.
    → `notes/2026-08-17-momentum-horizon-echo.md`
12. **Free diagnostic before any re-scoring trial: rank-correlate the current composite against
    a 12-7 intermediate-horizon score** on this universe. Costs no backtest, scores no returns,
    touches no trial count — in the spirit of the learnings entry on cheap holdings-only
    diagnostics. If correlation is near the 0.89 that killed the earlier inter-signal ensemble,
    the echo idea dies without a trial. Note the prior is already against it (no echo in global
    pooled portfolios). Tier A, no overlap. → `notes/2026-08-17-momentum-horizon-echo.md`
13. **Tranche-depth reasoning, not a sweep.** If tranche count is ever revisited, the argument
    should run through two bounds and no parameter scan (which `learnings.md` correctly forbids):
    above, the post-first-year reversal bound (signal age past ~12 months holds a *reversing*
    signal — a bias term that grows without limit, unlike ordinary staleness); below, the
    bias–variance result that a fresh-only window does *not* minimise forecast error, which is why
    pruning to the current held-set lost on every axis. Six monthly vintages sits inside both with
    room; twelve sits at the upper edge. Tier A, no overlap.
    → `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md`,
    `notes/2026-08-17-averaging-over-estimation-windows.md`
14. **[Ranked low, listed for completeness] Market-level panic-state scaling.** Daniel–Moskowitz's
    indicator is a *conjunction* (long-horizon negative market return AND elevated market
    volatility) driving a *continuous* scale — mechanistically distinct from the three refuted
    single-variable/binary overlays. It is also style-orthogonal and market-level, the one
    property the lab found to work (the defensive-cohort trigger). **But** its two-year trailing
    market return is a slow, lagging state variable — structurally the same defect that sank the
    refuted drawdown brake — the leverage cap makes the scalar one-sided (de-risking only), and
    the crash it manages is short-leg optionality a long-only book does not own. Any hypothesis
    built on this must honor both cadence lessons (trigger faster than rebalance; release no
    slower than recovery) and should state the expected benefit as small. Tier A, no overlap.
    → `notes/2026-08-17-momentum-crash-risk-management.md`
15. **Anti-candidate — long-only trend-following overlays should carry a *lower* prior after
    reading family 2's literature, not a higher one.** The temptation is to read
    Moskowitz–Ooi–Pedersen and the century-of-evidence extension as proof the lab's three
    refuted trend overlays were botched implementations. They were not: the lab built the only
    version its constraints permit, and that version is not the object the evidence concerns.
    Four obstacles, any one of which is disqualifying on its own — the evidence is long-short and
    the payoff lives in the short leg; it is multi-asset futures where the appeal is
    diversification across ~60 weakly-correlated trends, whereas a long-only equity/ETF book is
    one repeated bet on a single factor; inverse-vol sizing is intrinsic to the construction and
    is refuted here twice; and leverage ≤ 1.0 makes vol targeting one-sided. On top of that, a
    tier-1 replication finds the effect absent asset-by-asset, the pooled t-statistic below
    bootstrap critical values, and the strategy's profits indistinguishable from a
    no-predictability sample-mean rule. **A fifth obstacle was added this session and is the
    cleanest of the five**: a long-only trend overlay is a time-series rule whose net long
    position varies between 0 and 1, and the measured advantage of time-series over
    cross-sectional rules *is* that net long position — mostly its static risk-premium
    component at long ranking horizons, not timing skill. A fully-invested cross-sectional book
    already holds that position, so the overlay cannot capture the part that earns the money;
    it can only surrender some of it, keeping only the weak market-timing covariance term.
    Any family-2 candidate must state which of the five obstacles it escapes.
    Tier A evidence base, effect contested, no overlap.
    → `notes/2026-08-17-time-series-momentum-evidence-and-replication.md`,
    `notes/2026-08-17-cross-sectional-vs-time-series-construction.md`
16. **Anti-candidate — do not revisit basket-own-vol trimming on this basis.** Barroso–Santa-Clara
    endorse scaling by the strategy's own realized volatility and might look like grounds to
    reopen a mechanism the lab refuted. It is not: their object is a long-short spread whose
    volatility tracks the short leg's convexity, not a long-only basket whose volatility tracks
    market beta. Recorded explicitly so the tension is resolved rather than rediscovered.
    Tier A, no overlap. → `notes/2026-08-17-momentum-crash-risk-management.md`
17. **Anti-candidate — the cost-mitigation family is exhausted, by enumeration.** The literature
    offers three techniques: liquidity screening (this universe already *is* the screen, at its
    limit), reduced/staggered rebalance frequency (applied), and banding (applied). Combined
    with the learnings entry putting total cost drag at ~0.019 Sharpe, there is no remaining
    trial worth spending on cheaper trading. Recorded so a future session does not rediscover
    no-trade bands or weight-change thresholds as if they were new. Tier A, no overlap.
    → `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`
18. **Anti-candidate — short-term mean reversion (family 4) is closed here, on mechanism
    rather than on turnover.** The premium is compensation for **providing** liquidity: an
    uninformed order pushes price away, the market-making sector is paid to absorb the
    inventory, and price reverts. A book paying 15 bps/side is demanding liquidity, i.e.
    taking the losing side of the trade the premium pays for — a sign problem, not a
    magnitude one, so no wider band and no slower cadence rescues it. Three further blockers:
    the mechanism lives at a 1–5 day horizon; all the evidence is zero-cost long-short, and
    long-only keeps only the "buy what fell" leg, which is a market-beta bet; and the one
    ETF-scale variant (reversal across industry portfolios) earns nothing unconditionally and
    pays only in high-VIX states, i.e. it is a regime overlay that would also have to clear the
    lab's two cadence lessons *and* trade when spreads are widest — exactly where a flat 15 bps
    assumption is least defensible. Consistent with the lab's two empirical reversal
    refutations; recorded so the family is not reopened as a turnover-tuning problem.
    Tier A, no overlap.
    → `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md`
19. **Anti-candidate — volatility-managed / vol-targeting overlays (family 3) do not become a
    candidate just because the family now has a dedicated source.** Three reasons, in order.
    (a) The rule's implied position runs to roughly 4.5–8.6× the base book at the 99th
    percentile with a median near 1×, so gross leverage ≤ 1.0 leaves only the de-risking half —
    the half the source itself shows earns less. (b) Extended from 9 factors to 103 equity
    strategies, volatility management helps and hurts at about the same rate, and the wins
    concentrate in the very factors earlier papers had already selected on. (c) The large
    in-sample gains come from spanning regressions whose implied portfolio needs full-sample
    coefficients; real-time versions underperform simply holding the unmanaged book, because
    those coefficients are structurally unstable. What *is* worth keeping is the mechanism-level
    precondition, usable as a free screen: **volatility timing pays only where conditional
    expected return does not rise with conditional variance**, and the 103-strategy split is
    evidence that for most equity strategies it does. Tier A, `published_post_2018: true` on
    the replication. → `notes/2026-08-17-volatility-timing-managed-portfolios.md`
20. **Anti-candidate — low-vol / quality (family 5) is closed on mechanism, and the
    sector-neutral escape hatch `learnings.md` left open does not rescue it.** The hatch was
    "a genuinely different vol construction (e.g. sector-neutralized, not raw trailing)". The
    literature's version of that construction is industry-neutral BAB, and it fails here for
    the mechanism's own reason: **BAB's low-beta leg is levered to beta 1**, and the premium is
    said to exist *because* harvesting it requires leverage most investors lack — so an
    unlevered long-only low-beta basket is not a weakened BAB, it is the asset BAB says is
    cheap to hold and therefore low-returning. The industry-neutral variant is the worst fit of
    all: the paper's own explanation for its superiority is that it needs **more** notional per
    unit of risk. Independently, the skeptical literature puts the premium where this repo
    cannot trade — concentrated in small growth with the sign **reversing in large value**, and
    with BAB committing ~$1.05 per invested dollar to the bottom 1% of market capitalisation at
    ~60 bps/month of cost — and puts the surviving post-cost return down to **profitability and
    investment** exposures, which need fundamentals this repo does not have. Both halves of the
    named gap are now filled and both point the same way; treat the family as closed rather
    than uncovered. The live disagreement (AFP find the effect in large caps; Novy-Marx finds it
    reversing in large value) is recorded rather than resolved — but it is a disagreement about
    the only end of the market this repo trades, and AFP's own size split has large-cap alphas
    weaker in every column. Tier A; `published_post_2018: true` on the JFE replication.
    → `notes/2026-08-18-low-risk-investing-industry-neutral.md`,
    `notes/2026-08-18-defensive-equity-replication-and-construction.md`
21. **Anti-candidate — risk parity / equal-risk-contribution weighting (family 3's second
    half) is closed by a theorem, not only by the lab's two trials.** ERC equals the
    maximum-Sharpe portfolio **only under constant correlation and equal component Sharpe
    ratios**; the lab's sleeves differ by roughly 2× in Sharpe, so the loss was predictable
    before either trial ran. Three further facts close the escape routes. (a) For two
    components ERC *is* inverse-vol, independent of correlation — so
    `mom_etf_volweighted_blend` was correct risk parity, and no better-specified version of
    that trade exists to try. (b) The general solution is `x_i ∝ 1/β_i` (beta to the
    portfolio), so a *more* correct implementation tilts further toward the diversified
    low-return leg — the refuted direction. (c) `σ_mv ≤ σ_erc ≤ σ_1/N` means the family's
    output is a lower-volatility book whose appeal depends on levering it back up, which
    gross leverage ≤ 1.0 forbids — the same one-sided truncation as the vol-targeting half.
    What survives is a **free diagnostic, not an objective**: the risk-contribution vector
    `x_i · ∂_{x_i}σ(x)` is a holdings-only statistic that scores no returns and costs no
    trial, and it answers the standing question the existing top-weight/HHI statistics only
    proxy — how much of the champion's variance the top name actually explains. Tier A on the
    theory, no overlap. → `notes/2026-08-18-risk-parity-equal-risk-contribution.md`
22. **Anti-candidate — do not fit the weighting or selection coefficients to an in-sample
    objective, and know the name of the thing you are declining.** "Parametric portfolio policies"
    is the published framework for writing weights as `w_i = w̄_i + (1/N)θᵀx̂_i` and choosing `θ`
    by maximising the realised sample utility of the resulting returns. The champion already *is*
    such a policy with `θ` hard-coded rather than fitted, so any proposal to "estimate the
    weighting coefficient on the training split", "fit the buffer widths", or "optimise the trim
    thresholds against validation Sharpe" is this framework, and the honest prior on it is the
    critique's: **parsimony in `θ` does not protect you**, because the objective depends on every
    property of an unspecified return distribution, so the effective dimensionality is not the
    parameter count. The critique's diagnosis is the reusable part — overfitting is positively
    linked to the *variance* of the fitted portfolio, so the remedy is to fit with a **more concave
    loss than the one you care about** (`γ* = γ + λ`), and a selection criterion with too little
    curvature will systematically pick the high-variance candidate. That generalises to any
    in-sample-maximising selection step, including this repo's own gate, which is why it is also
    recorded under cross-cutting principles for the human reviewing the ⚠ standing protocol
    concern. Note in passing that this framework is not useless here — the same source establishes
    that cross-sectional standardisation of the score is load-bearing (stationary score
    distribution, weights summing to one), which the champion already does. BSV tier B+, no
    overlap; the critique tier B− and `validation_overlap: true`, so only its mechanism is carried.
    → `notes/2026-08-20-parametric-portfolio-policies.md`
23. **Two free holdings-only measurements added 2026-08-21, both in the same class as the
    existing risk-contribution vector (no returns scored, no trial spent), and both aimed at
    the axis the lab is actually working.** They belong with the free screens at the top of this
    list; they are numbered here only to avoid renumbering.
    *(a) Effective number of bets, computed properly and conditionally.* `learnings.md`'s "6.0
    effective risk bets" is a Herfindahl-type count over **marginal risk contributions of
    correlated assets**, which the diversification literature specifically rejects as a count
    of anything uncorrelated. The measure that counts uncorrelated sources is
    `N_Ent = exp(−Σ p_n ln p_n)` over the diversification distribution
    `p_n = w̃_n²λ_n / Var(R_w)`, `w̃ = E⁻¹w` from `Σ = EΛE′` — each `p_n` provably the R² of the
    portfolio return on the `n`-th principal portfolio. Two practical points: the likely
    direction of the correction is **downward** (changing basis usually finds fewer independent
    bets than a contribution count), and for a fully-invested long-only book the **conditional**
    version (drop the first principal portfolio, renormalise) is the one to report, because the
    budget constraint alone pins the market exposure and the unconditional index is low for a
    reason no candidate can change. Decline the source's actual proposal — a
    *mean-diversification frontier* that optimises `N_Ent` is the most estimation-hungry object
    in this folder and is closed by screen #1.
    *(b) The diversification return of the current book,* `½ Σ_i w_i(σ_i² − σ_ip²)`. This is the
    return-side twin of (a): the term is large only where a position's volatility is
    idiosyncratic *to this book*, so a concentrated magnitude-weighted book gives most of it
    away. It puts a number on a cost of concentration the folder had priced only through
    drawdown, and it supplies the missing question for any turnover-reducing proposal — does it
    throttle **membership churn** (little of the term at stake) or **weight resets** (where the
    term lives)? Boundaries travel with it: it is an accounting decomposition and **not alpha**,
    it holds exactly only for constant weights, and the source models no transaction costs — so
    it is not a reason to rebalance more often. Tier A on the identity, C/B on the sources'
    empirical content.
    **[REVISED 2026-08-22 — measure it, but read it differently.]** Two changes. The
    *constant-weights* restriction is gone: `γ*_π = ½(Σ_i π_i a_ii − π′aπ)` is the same quantity
    for an arbitrary, path-dependent, signal-driven weight process, so it can be computed on the
    champion's actual sanitized weight matrix rather than on a constant-weight idealisation of it.
    The *interpretation* changes more: this term is **not** a prize the champion forgoes by not
    rebalancing enough — it accrues to any diversified holder, rebalanced or not, and the part
    genuinely created by re-targeting trades has zero expected value under IID returns and
    **negative** expected value when relative prices trend, which is the regime a momentum book
    bets on. So compute it as **the price of concentration** (it falls mechanically as weight
    collapses onto few correlated names, and it is denominated in growth rate, on the gate's own
    axis), and do **not** read a small value as an argument to reset weights more often.
    **[CLOSED 2026-08-23 — measured null, and the premise it rested on was wrong.]** The lab ran it:
    across the promotion ladder `γ*` is non-monotone, does not break where every other ladder
    statistic breaks, and is **highest for the narrowest book**, because it is dominated by
    `Σ_i π_i a_ii`, the weighted average variance of what is held — so on a momentum book that
    concentrates into high-volatility winners it *rises* with concentration. It is not a
    de-concentration statistic on this universe and should not be re-run. The clause above calling
    it "denominated in growth rate, **on the gate's own axis**" is now withdrawn outright: Samuelson
    and Merton–Samuelson establish that log growth is not an approximation to any risk-scored
    objective at any horizon, so a growth-denominated quantity was never on the gate's axis and no
    measurement could have made it so. See the *"check the currency"* principle and candidate #27.
    The identity stands as accounting; only its promotion to an axis is retracted.
    → `notes/2026-08-23-geometric-mean-maximization-fallacy.md`, `experiments/learnings.md`
    → `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`,
    `notes/2026-08-21-diversification-return-and-rebalancing.md`,
    `notes/2026-08-22-excess-growth-and-return-decomposition.md`,
    `notes/2026-08-22-rebalancing-return-attribution-critique.md`
24. **[Added 2026-08-22] Design test before crediting any construction change: which sign of
    relative-price autocorrelation is it implicitly long?** Constant-weight rebalancing is a
    contrarian overlay — it sells what rose in relative value and buys what fell — and its
    incremental return over buy-and-hold is positive only where relative prices mean-revert,
    zero under IID, negative where they trend. Letting weights drift is the opposite bet, and
    discards the signal. A cross-sectional momentum book that re-targets to signal-proportional
    weights is running both at once, and they partially cancel. Costs no trial, and it already
    reproduces the lab's own re-target-cadence bracket (weekly re-targeting lost; unbounded
    weight drift lost worse) as the predicted shape rather than as two unrelated results. Its
    live consequence: **the membership buffer's best remaining justification is neither cost nor
    risk breadth but expectation** — a hold-band suppresses contrarian trades a continuation
    signal does not want. That is a new argument, distinct from the cost claim `learnings.md`
    retired and from the risk-breadth claim that replaced it, and it is the one a proposal to
    reinstate or widen the band should now lead with. Tier B, no overlap.
    → `notes/2026-08-22-rebalancing-return-attribution-critique.md`
25. **[Added 2026-08-22] Interpretation rule, replacing a prior the folder was close to
    hardening into a taboo: grade a constraint by how binding it is, not by whether it exists.**
    Under full investment, an `ℓ1` penalty is exactly a penalty on short positions, so long-only
    is the `τ → ∞` endpoint of a continuous shrinkage path with a critical `τ₀` where it starts
    to bind. On one asset set the endpoint was the best point on the whole path; on another,
    allowing a little shorting beat both `1/N` and the long-only optimum. Both signs are on
    record and no general condition separates them — so the question is always *how far past the
    unconstrained optimum does this push, on this universe*, never *are constraints good*. Two
    riders specific to this repo. (i) Long-only optima are **automatically sparse** (single-digit
    name counts in the source's runs), so "few names" is the expected shape of a long-only
    solution here rather than an aggressive stance needing its own defence — and a proposal to
    widen the book is a move away from where the constraint pushes, which is a reason to state
    the mechanism, not a reason to decline. (ii) A proportional per-side cost is literally an
    `ℓ1` penalty on `Δw`, so the repo's own cost model regularises, and a no-trade band's
    shrinkage effect is inseparable from its cost effect. Explanatory only — every point on the
    path except the endpoint needs an estimated covariance and is closed by screen #1.
    Tier A, no overlap. → `notes/2026-08-22-long-only-as-l1-regularization.md`
26. **[Added 2026-08-23] The one free measurement this session recommends, and unlike last
    session's it is a check on the repo's headline statistic rather than a new statistic.**
    *Is every Sharpe ratio in this repo annualised correctly?* `SR(q) = η(q)·SR` with
    `η(q) = q / sqrt(q + 2Σ_{k=1}^{q−1}(q−k)ρ_k)`, and the familiar `√252` is the special case
    `ρ_k ≡ 0`. A book whose weight vector is held **exactly constant between the 88 emitted rows**
    (`learnings.md`'s own `sanitize_weights` finding: mean L1 change of 0.000000 across the 83
    inter-rebalance gaps) has every structural reason to produce serially correlated daily returns.
    Measure `ρ̂_1 … ρ̂_k` on the stored series in `experiments/trial_returns/` and compute `η(252)`:
    it re-runs no strategy, scores no new returns, touches no trial count, and answers whether the
    repo's headline number carries a systematic bias **and in which direction** — if `ρ̂_1 > 0`,
    every annualised Sharpe here is overstated. Pair it with the standard error
    `SE(ŜR) ≈ sqrt((1 + ½SR²)/T)` so that Sharpe values start being quoted with an error bar.
    Two boundaries. The i.i.d. formula is the wrong one for this book, so use the GMM/HAC version
    for the error bar even while the `η(q)` correction uses the sample autocorrelations. And the
    single-strategy standard error is **not** the standard error of a *difference* between two
    highly-correlated candidates — which is what the gate decides on, and which the source does not
    derive. Tier A, no overlap. → `notes/2026-08-23-statistics-of-sharpe-ratios.md`
27. **[Added 2026-08-23] Import screen, belongs with the free screens at the top and numbered here
    only to avoid renumbering: check the currency, and know that log growth has no exchange rate.**
    Before adopting any theoretical quantity as a diagnostic, ask which unit it is denominated in —
    forecast MSE, information ratio, log growth, or net Sharpe — and whether a crossing to the
    gate's unit has been established. For log growth it has **not**, and cannot be: maximising
    `E[log W]` is suboptimal for every non-log preference at every horizon, the wealth-equivalent
    cost of the substitution is `λ(γ)^(T/γ)` and therefore *grows* with the horizon, and the
    two-parameter `(mean-log, variance-log)` repair is a limit-interchange fallacy whose error also
    diverges. The one exact bridge, `g* = r_0 + ½·SR²`, holds at the growth-optimal **leverage** and
    is unavailable at gross leverage ≤ 1.0. This retires, on principle rather than by measurement,
    the class of proposals of the form "measure or optimise growth rate because it is a return
    quantity" — and it is the general form of the `γ*` null `learnings.md` recorded. Growth-rate
    identities remain valid **accounting**; what is refused is their promotion to a scoring axis.
    Tier A, no overlap. → `notes/2026-08-23-geometric-mean-maximization-fallacy.md`,
    `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md`
28. **[Added 2026-08-23] Anti-candidate — growth-optimal (Kelly) or fractional-Kelly position
    sizing, closed for the same structural reason as families 2, 3 and 5.** The prescription is a
    **leverage rule**: hold `X* = (E_M − r_0)/σ²_M` of the risky asset. For a book of this Sharpe
    `X*` is far above 1, so gross leverage ≤ 1.0 binds essentially always and the rule degenerates
    to "be fully invested," which the champion already is. This is the fourth mechanism in the
    folder whose economics live in the leverage the repo cannot use, and here the pattern is
    starkest — the rule has no de-risking half at all on an attractive book. What survives is the
    *shape* of the trade-off, usable without locating any optimum: growth is a concave parabola in
    exposure with roots at 0 and `2X*`, so exactly-double-Kelly earns the risk-free rate, the
    penalty for overbetting is quadratic while underbetting near the optimum costs only linearly,
    and security improves fast over the last stretch below the optimum (0.8× Kelly retains 96% of
    the growth; full Kelly accepts a one-in-three chance of halving before doubling). Any proposal
    that raises the book's effective risk exposure should be argued as a move along that parabola,
    with a claim about which side of the vertex the book is on. **What this does not license:**
    neither "Kelly says be aggressive" nor "Kelly says the book is overbet" can be asserted without
    estimating the book's expected return — the single most error-prone input on the list, on the
    shortest sample. Tier B+ survey over tier-A propositions, no overlap.
    → `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md`
29. **[Added 2026-08-24] Free pre-trial screen, and it belongs with #1 and #2 at the top: write the
    candidate's error bar down before building it, from one guessed correlation.** Memmel's corrected
    Jobson–Korkie standard error for a *difference* of Sharpe ratios is
    `T·Var(Δ̂) = 2(1−ρ) + ½(Sh_a² + Sh_b²) − Sh_a·Sh_b·ρ²`, which at daily frequency reduces to
    `SE(Δ̂) ≈ √(2(1−ρ)/T)` per period, i.e. **`≈ 0.568·√(1−ρ)` annualised on this repo's 1,562-day
    validation window** — 0.031 at `ρ=0.997`, 0.057 at 0.99, 0.080 at 0.98, 0.127 at 0.95, 0.172 at
    0.909. Equivalently `SE(Δ̂) ≈ SE(ŜR)·√(2(1−ρ))`. The screen: *state the effect you expect and the
    correlation with the champion you expect, and if the effect is inside that bar the trial buys a
    point estimate the data cannot resolve while permanently raising the DSR bar for every later
    candidate.* This is `learnings.md`'s own paired-bootstrap screen made closed-form and available
    **before** the candidate exists — it requires no series, no resampling, and no trial. **Two hard
    boundaries.** The formula assumes i.i.d. bivariate normal returns and is *liberal* under fat tails
    and volatility clustering (empirically ≈2–3× the nominal rejection rate), so it is a **floor** on
    the error bar: an effect inside it is certainly unresolvable, but a `|t| > 2` computed from it is
    **not** evidence of significance. And it is inference about a difference only — multiple-testing
    deflation is a separate correction that composes with it, never substitutes. Tier A, no overlap.
    → `notes/2026-08-24-testing-differences-of-sharpe-ratios.md`
30. **[Added 2026-08-24] Interpretation rule for the gate's own reading, replacing a sentence the
    folder has been repeating as if it were arithmetic.** The deflation bar depends on the *search*,
    not the candidate, through `N` (independent trials, reached by the interpolation
    `N̂ = ρ̂ + (1−ρ̂)·M`) and `√V[{ŜR_n}]` (cross-trial dispersion of Sharpe ratios), plus the
    candidate's skewness and kurtosis. Three usable readings. (a) *Clustering is cheap because the
    trials are nearly one trial* — the lab's local observation, now sourced. (b) *Dispersion is
    expensive*: a single wild trial raises the bar for every later candidate through `√V[{ŜR_n}]`,
    by more than its increment to the count — an argument for well-motivated exploration that is
    independent of the trial-count argument. (c) *"Every trial raises the bar" is a family-wise-error
    statement*, true of this gate and not of statistics in general; an FDR-controlling procedure's
    threshold stabilises instead of diverging, and the competing published correction also makes the
    penalty depend on the Sharpe **level** (>50% below ~0.4, ≤~25% above 1.0). **What this does not
    license:** nothing. `engine/` and `program.md` are frozen and the thresholds are a human decision;
    this is here so the gate's assumptions are legible, and so a session stops writing an
    error-rate-specific consequence as a law. Tier B+ / A, no overlap.
    → `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-08-24-multiple-testing-haircut.md`
31. **[Added 2026-08-25] Discipline rule, and the answer to the folder's longest-standing question
    about its own protocol: a prior discount is legitimate, and it is strictly zero-sum.** Weighted
    multiple testing controls FDR (and family-wise error) under *any* non-negative weights fixed
    before the data are seen, provided they **average one** — `Q_i = P_i/W_i`, then Benjamini–Hochberg
    on the `Q`'s. So "a better-motivated candidate deserves an easier test" is formally defensible,
    but only inside a budget: every unit of relaxation must be paid for by tightening elsewhere. Three
    consequences a session can use without any engine change. (a) **This does not license a session to
    treat its own hypothesis as pre-approved.** The lab has no mechanism that could spend such a
    budget — every trial faces the same bar — so the honest reading is that the protocol is the
    `W ≡ 1` case, and the part of it that *would* make a weight admissible (hypothesis written before
    the code, per `CLAUDE.md`) is already in place but is never recorded as a ranking before the run.
    (b) **If a ranking is ever recorded, back the plausible-but-marginal idea, not the strongest
    conviction.** The optimal weight function `ρ_c(ξ) = (m/α)·Φ̄(ξ/2 + c/ξ)` is unimodal, peaking at
    `ξ = √(2c)`: weight is wasted on what is already detectable at unit weight and on what no
    affordable weight can reach. Concretely, the ideas that deserve a discount are the ones landing
    *just* short of the bar for a stated mechanical reason. And spend it **sparsely** — one large
    weight with everything else near 1 is the robust regime; many modest tilts is the fragile one.
    (c) **The shortcut is closed:** deriving a candidate's "deserved" discount from the validation
    split itself (a pre-screen, a warm-up window, a first-half fit) is refuted at the mechanism level
    — estimating weights by data splitting does not beat using the whole sample unweighted — and would
    in any case score returns, outside the holdings-only exemption. Tier A, no overlap.
    → `notes/2026-08-25-prior-weighted-multiple-testing.md`
32. **[Added 2026-08-25] Free pre-trial calculation that composes with #29, plus the exchange rate for
    #31: what a prior is worth, in t-units.** `MBF = exp(−Z²/2)` (or `SD-MBF = −e·p·ln(p)` with no
    directional conviction) times stated prior odds gives a Bayesianized p-value; inverted, it gives
    the statistic required for a target posterior probability of the null. The composition is free and
    available **before** a candidate exists: #29's closed-form paired standard error turns a *predicted*
    Sharpe gap and a *predicted* correlation with the champion into a `Z`, and `exp(−Z²/2)` turns that
    into the strongest evidence the comparison could ever supply. The calibration to carry: at even
    odds and a 5% posterior-null target the required `t` is **2.43** (MBF) or **2.93** (SD-MBF), rising
    to 3.43 / 3.86 at 19:1 against — so **a prior never buys a bar below the naive 2.0**, and the whole
    range from long-shot to even-odds is worth about 1.0 in `t`. Three cautions, all pointing the same
    way: #29's closed form is a *floor* on the error bar so the `Z` is an upper bound; the MBF is the
    most favourable Bayes factor that exists; and the prior must be stated in the journal *before* the
    run or the exercise is circular. Two mechanisms attach that need no arithmetic — the **base rate
    declines over time** (scarcer true effects, exhausted first-principles theories, a finite security
    count), so the required `t` for the same confidence is rising in this repo's most-worked family for
    reasons independent of the trial count; and the honest denominator is the **choice space**, which
    includes lookback grids not swept and buffer widths chosen by convention, not just recorded trials.
    **What this does not license:** re-scoring the gate, which is frozen and a human's decision
    (session 11's item (d), unchanged). Tier A, no overlap.
    → `notes/2026-08-25-bayesianized-p-values-prior-odds.md`
33. **[Added 2026-08-25] Interpretation rule that narrows `learnings.md`'s ⚠ standing protocol concern
    to the half of it that is real — and makes that half harder to dismiss.** Under any positive
    shrinkage a Bayesian *always* expects out-of-sample alpha below the in-sample estimate
    (`E(α|α̂) = κα̂`, `κ < 1`), so a candidate scoring lower on holdout than on validation is the
    **predicted base case**, not evidence of anything. The concern's evidentiary weight therefore does
    not rest on the level drop and should stop being stated that way. What it does rest on is the
    shape: a **sign flip** in the validation/holdout relationship at one identified structural change,
    with the two series moving monotonically in opposite directions across a run of promotions.
    Attenuation is predicted; inversion is not. Two riders. The same source's `κ_g` formula shows
    correlated evidence is discounted continuously in `ρ` and is worth nothing at `ρ = 1`, which is the
    DSR-clustering observation from the other side — so the hierarchical "more related tests can be
    evidence rather than penalty" reversal is **not available for this repo's near-identical variant
    ladders**, only across weakly-correlated families. And search is shown to be punished on two axes,
    variance inflation as well as mean bias, so a heavily-searched estimate is discounted even by
    someone who believes no bias was introduced. Tier A but `validation_overlap: true` and
    `published_post_2018: true` — mechanism only, and no figure from it may be imported.
    → `notes/2026-08-25-hierarchical-bayesian-factor-replication.md`
34. **[Added 2026-08-26] Interpretation rule that re-aims the lab's oldest permanent caveat, at zero
    cost.** Survivorship's effect on the **level** of returns is the forgiving half (≈0.4–0.8%/yr in
    BGIR's calibration, and Stambaugh shows the standard adjustment for it is generally *too severe*).
    Its effect on **inference about cross-sectional persistence** is the severe half: a 5% annual
    performance cut is enough to make a test of no-persistence reject more than half the time. A
    cross-sectional momentum strategy asserts persistence and nothing else, so the champion's own
    mechanism is the one a current-constituents universe most readily fabricates. Two riders that keep
    this from being a blanket discount. The **sign follows the selection rule** — sequential
    (per-review) survival induces persistence, whole-sample cumulative selection induces reversal — and
    index membership, re-reviewed on a cadence with removal for sustained relative decline, is the
    first case. And the size of the discount is a **stated assumption about commonality**: maximal if
    you believe all instruments share one unknown expected return, zero if you believe their expected
    returns are independent draws. On ~145 large-cap global names sharing a dominant market factor,
    high commonality is the honest assumption, so the discount stays large — but it should be *stated*,
    not reflexive. **What this does not license:** any numerical adjustment to a measured Sharpe. No
    source read here bridges "persistence inference is corrupted" to a magnitude for a strategy's net
    Sharpe, and none can be taken from them. Tier A / B, no overlap.
    → `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`
35. **[Added 2026-08-26] The one buildable proposal this session found, ranked below the free rules
    because it is not free: a random-portfolio null on the same biased universe.** Generate many random
    long-only books on this repo's own universe, **matched to the strategy on gross leverage, position
    count, average holding period and turnover**, and report the champion's statistic as a quantile of
    that distribution rather than as a level. It is the correct control for a look-ahead-selected
    universe precisely because the same contamination applies to both sides, and it answers a question
    no statistic in this repo asks — how much of the measured edge is available to a book with no
    information at all. The matching is load-bearing; an unmatched random benchmark measures something
    else. Three costs put it in session 11's PBO category rather than in the free-diagnostic class: it
    **scores returns** (outside the holdings-only exemption), it would have to run on the validation
    split to be comparable to the gate's number (re-using a split, not supplying an independent look),
    and `CLAUDE.md` requires every strategy run to go through `run_experiment.py`, so **whether a null
    distribution counts as trials is a human decision, not a session's**. Recorded as a proposal to a
    human. Tier B, no overlap.
    → `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md`
36. **[Added 2026-08-26] A distributional price for the concentration ladder, computable from one
    number the repo already has.** At unchanged mean, the **median** buy-and-hold outcome falls
    monotonically in a book's `σ`, steeply and non-linearly, and the effect grows with horizon (ten-year
    horizon: 81.94% at `σ = 0` → 0.14% at `σ = 10%`/month → −85.28% at 20%). The relevant span is
    calibrated: **5.4%**/month for a value-weighted market book, 7.3% equal-weighted, **18.1%** for
    pooled individual stocks — and every rung of the lab's concentration ladder moves its `σ` along that
    span. Independently, a randomly drawn 25-name value-weighted book beats the cap-weighted market in
    **under half of draws at every horizon, with no costs deducted**, so the null for a concentrated
    long-only book is not centred on a broad benchmark. This is the folder's fourth account of what
    concentration costs and its first distributional one; it explains as a single phenomenon two things
    `learnings.md` records separately (drawdown widening monotonically along the ladder; one validation
    year dominating the P&L). **Two hard boundaries.** *Check the currency* (#27): these are
    probabilities of beating a benchmark and medians of buy-and-hold returns, **not Sharpe**, and no
    exchange rate exists — do not convert them into an expected validation Sharpe. And the bootstrap
    books are **randomly selected**, so every figure is a property of the null and none is evidence
    about a signal-selected book. The only free, holdings-only piece is the input: realised monthly `σ`
    at each rung, which the repo already computes. Tier A, no overlap.
    → `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md`
37. **[Added 2026-08-27] A discount to apply to every long-short momentum result this folder ever
    imports, and it is the most specific one here.** Using the untraded middle portfolio as the
    benchmark, **53% to 70% of the total long-short momentum spread comes from the loser leg**, across
    three published strategy definitions and robust to using the value- or equal-weighted market as
    benchmark instead; two independent studies cited alongside reach the same conclusion. The operative
    form: **a long-only implementation of a published long-short momentum effect should be expected to
    capture roughly a third of it, before any other adjustment.** This is not the quantity session 10
    retired after three failures (the long-only constraint's leakage as a function of signal
    dispersion) — it is narrower, family-specific, and obtained rather than estimated. It costs nothing
    and applies at hypothesis-writing time. Tier A, US-only, no overlap.
    → `notes/2026-08-27-momentum-net-of-costs-debate.md`
38. **[Added 2026-08-27] A caveat for `learnings.md`'s permanent list, not a build: every Sharpe in
    this repo is a small-fund Sharpe.** Real cost is `a + b·x + c·√x` in trade size as a fraction of
    daily volume; the engine charges the constant `a` alone. That is correct only in the small-`x`
    limit, so this repo's backtests are **capacity-blind** — valid at some notional and silently wrong
    above it, with no term that degrades. The vocabulary for the missing quantity is **break-even fund
    size**, and for a momentum book it is set by the *illiquid* names in the basket rather than the
    average one; published long-only momentum break-evens run from ~$200M (equal-weighted) to ~$5bn
    (liquidity-weighted), normalised to end-1999 market capitalisation. **Unmeasurable here**: the
    calculator needs dollar volume and market capitalisation, which `program.md` gates behind human
    approval, and no attempt should be made to proxy volume from adjusted closes. Ranked as a caveat
    because it changes how results are *stated*, not what is built. Tier A, no overlap.
    → `notes/2026-08-27-live-execution-costs-implementation-shortfall.md`,
      `notes/2026-08-27-momentum-net-of-costs-debate.md`
39. **[Added 2026-08-27] A free holdings-only diagnostic denominated in the unit the gate reads —
    the first since `γ*`, and unlike `γ*` its currency checks out.** Impact cost in basis points is
    proportional to the traded name's daily volatility (the temporary-impact function needs *no*
    stock-specific correction once expressed as a fraction of `σ`). The engine's flat charge is
    volatility-blind, and a momentum basket holds the high-volatility tail by construction, so the
    honest cost multiplier is the **turnover-weighted ratio of held names' trailing daily volatility to
    the universe median's** — computable from the stored weight matrix and prices, forecasting nothing
    and scoring nothing. Multiplied by the existing modelled cost drag it lands in annualised return
    and thence Sharpe, satisfying #27 (*check the currency*) rather than tripping over it. **State the
    expected size before running it**: at 3.0× turnover and 0.019 Sharpe of modelled drag, even a 1.5×
    multiplier stays under ~0.03 Sharpe, inside the paired standard errors of session 11 — so this is a
    correctness fix to a caveat, not a lever. **Caution that must travel with it:** a cost account,
    never an objective; a book can lower it by holding placid names and lose far more on selection.
    Tier A / B, no overlap.
    → `notes/2026-08-27-market-impact-functional-form-and-trade-rate.md`
40. **[Added 2026-08-28] The one construction change this session opens, and the first grouping the
    folder has found that passes candidate #5's screen: rank the momentum composite *within coarse
    regional groups* rather than in one global pool.** #5 requires naming the mechanism by which the
    signal would load on the group even if the effect were absent. For sectors the lab could not name
    one and the trial duly lost. For **countries/regions** the mechanism is documented and cited
    (large country-specific components in international stock returns): a globally pooled momentum
    sort mechanically overweights whichever *market* rose, so the book takes an unrequested country
    bet on top of its stock bets. Three tier-1 sources build global momentum this way and none ranks
    one pooled cross-section. **Predict the sign before running it, per #24: this is a variance
    mechanism, not an alpha one** — Rouwenhorst's country-neutral book keeps almost all of the mean,
    raises the legs' correlation (≈0.74 → ≈0.88) and cuts the spread's volatility ~40%. So the
    prediction is a Sharpe gain with a flat-to-slightly-lower numerator and a materially lower
    denominator; a version that raises the mean would be evidence the mechanism is *not* the one
    claimed. Three implementation pitfalls, all cheap to check first: per-group counts on ~145
    instruments make a three-way NA / Europe / Asia-Pacific split about the practical limit;
    the ETF sleeve's country and regional funds **are** regions rather than belonging to one, so
    the two legs must be grouped separately or the stock leg grouped alone; and this changes
    *ranking*, not weighting, so it composes with magnitude weighting rather than competing with it.
    Tier A, no overlap. → `notes/2026-08-28-international-momentum-country-neutral.md`,
    `notes/2026-08-28-local-versus-global-factor-construction.md`
41. **[Added 2026-08-28] The second buildable idea, and the first *signal* this folder has ever
    supplied that this repo could not already compute: the negative of the past 5-year return as a
    price-only value proxy.** Asness–Moskowitz–Pedersen use it as the value measure for every asset
    class without book values, and validate it in equities against book-to-market: it produces a
    value strategy correlating ≈ −0.48 with momentum, close to BE/ME's ≈ −0.53, and the negative
    value/momentum correlation survives lagging BE/ME's price by a year so the two signals share no
    price data. This repo has no fundamentals and has therefore never had a value signal; it now has
    one that needs nothing but daily closes. **Ranked below #40 and behind three caveats.** (i) The
    evidence is long-short, so #4 applies and the long-only half is the weaker half. (ii) #2's design
    test classes a value sleeve blended with a momentum sleeve as *mixing different return streams*,
    not averaging estimates of one quantity — so it pays the capital-dilution tax the lab has
    already measured, and the ≈ −0.5 correlation is what would have to beat that tax; the tax is
    known here and the correlation is not measured here. (iii) A 5-year lookback is the construction
    most exposed to this repo's survivorship conditioning — a name that collapsed five years ago and
    is still in today's universe is a selected survivor — so #34's re-aimed caveat bites hardest
    exactly here. Tier A, no overlap.
    → `notes/2026-08-28-value-momentum-everywhere-global-comovement.md`
42. **[Added 2026-08-28] Import discount, free: every momentum magnitude in the literature is an
    upper bound for this universe, and on large caps alone the published premium is not reliably
    different from zero.** Fama–French's *global* big-stock winner-minus-loser spread carries a
    t-statistic near 1.4 across 23 developed markets over two decades, while the small-stock spread
    exceeds 3; Rouwenhorst's largest size group earns about half his smallest group's spread;
    Chui–Titman–Wei find momentum profits negatively related to firm size across 41 countries; and
    Asness–Moskowitz–Pedersen call their own results conservative *because* their universe is the
    largest names covering 90% of market cap — the closest published universe to this repo's. Use it
    as #4 is used: not to doubt the lab's own measured Sharpe (a concentrated long-only
    magnitude-weighted book is a different object from a value-weighted long-short factor), but to
    place the *external* prior for any momentum-construction hypothesis at the bottom of the
    published range. Corollary for hypothesis writing under #31: "the literature reports a large
    momentum premium" is not a motivating prior for this universe; "the literature reports a premium
    that shrinks monotonically in size and is weakest where our universe sits" is.
    Tier A, no overlap. → `notes/2026-08-28-local-versus-global-factor-construction.md`
43. **[Added 2026-08-28] Interpretation rule, free: adding names across regions does not buy
    breadth.** The average single-market stock momentum strategy correlates ≈0.65 with the average
    momentum strategy in *other* stock markets — co-movement stronger than that of passive exposures
    to the same markets, on strategies that are market-neutral within each market, so it is not the
    assets moving together. A global momentum book therefore has one dominant common factor, and
    widening it geographically raises nominal `N` without raising the number of independent bets.
    This is the published version of the fundamental-law point already here, and it retro-explains
    the lab's own result that widening the basket 25/15 → 35/20 left maximum drawdown unchanged.
    Consequence: any future proposal whose stated benefit is "more names, more regions, more
    diversification" should be required to predict the effect on *risk* — and the prior for that
    prediction is ≈zero. Tier A, no overlap.
    → `notes/2026-08-28-value-momentum-everywhere-global-comovement.md`
44. **[Added 2026-08-28] Anti-candidate — do not exclude or down-weight a regional bloc on the
    cross-country-heterogeneity evidence.** The natural reading of Chui–Titman–Wei (momentum is
    stronger in more individualistic cultures; the Japanese exception is the stock example) is to
    drop or shrink low-individualism names from the basket. Three reasons not to, and they compose:
    the effect is measured on **within-country long-short** books, not on a long-only global basket;
    **Fama–French explicitly decline the explanation** — the psychological argument is reversible,
    and their Hotelling `T²` test fails to reject equality of expected momentum returns across the
    four regions at the 90% level, so the exception may be noise; and any such exclusion is a free
    parameter chosen from a disputed source whose sample ended long before this repo's data. Note
    the asymmetry with #40, which is the point: a regional grouping used for **neutralised ranking**
    is a variance argument with a named confound and is licensed; the same grouping used for
    **exclusion** is a mean argument resting on the disputed result and is not. Tier A, no overlap.
    → `notes/2026-08-28-individualism-cross-country-momentum.md`,
    `notes/2026-08-28-local-versus-global-factor-construction.md`

45. **[Added 2026-08-29] Free decomposition, and the cheapest informative trial in
    `liquidity-volume`: sort `ILLIQ` *within* trailing-volatility buckets, because the
    unconditional sort the lab has already run is partly a volatility sort.** `ILLIQ`'s numerator
    is an absolute return, so it is positively correlated with return volatility by construction —
    Amihud says so and builds his own illiquid-minus-liquid factor as a **three-volatility-tercile
    × five-`ILLIQ`-quintile** double sort for exactly that reason, following Fama–French's HML
    logic. This lab holds two facts that make the confound consequential in *both* directions: its
    `lv_amihud_illiquidity_tilt` scout is a single unconditional sort and is the most decorrelated
    non-trivial result on the board, and `learnings.md` records low-vol tilts as refuted on this
    universe. The unconditional scout cannot tell whether it is being helped or dragged by an
    unintended volatility tilt. **This is a decomposition, not a knob** — it is the one variant that
    separates two effects rather than adding a parameter, and it is the family's obvious second
    trial. Tier A, `validation_overlap: false`.
    → `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`

46. **[Added 2026-08-29] The companion trial to #45, and the one a tier-1 commissioned replication
    predicts will *win*: replace `ILLIQ` with log mean dollar volume, or with the ratio of mean
    |return| to mean dollar volume.** Harris–Amato's horserace finds `ILLIQ` among the **lowest**
    average R² of every simple measure built from the same daily returns and volume, with log
    average dollar volume and the Kyle–Obizhaeva invariance measure the best; and decomposing
    `ILLIQ` shows almost all its explanatory power sits in the **ratio of the two means**, not in
    the day-by-day pairing of |return| with volume that is the measure's entire motivation. The
    ratio of means is ~92% correlated with `ILLIQ` and delivers essentially identical coefficients.
    Practical consequences here, all favourable: `dollar_volume` arrives directly in the `aux`
    panel; a ratio of means is far smoother than a mean of ratios and so should turn over less; and
    it is immune to the NaN-and-infinity failure mode that a per-day `|R|/volume` hits on every
    foreign holiday, since this repo's volume panel is **not forward-filled**. If it wins, the
    family's signal is an activity/size proxy rather than price impact and the lab should say so;
    if it loses, that is a real disagreement with a published replication and worth recording as
    one. Tier A, `validation_overlap: false`.
    → `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`

47. **[Added 2026-08-29] Free measurement rule, and it changes an input to every existing
    volatility-based construction: use Garman–Klass, never Parkinson and never Rogers–Satchell,
    whenever a volatility estimate is a *denominator*.** Range-based estimators have 5–8× the
    efficiency of the squared return (Parkinson 4.9, Rogers–Satchell 6.0 at zero drift, Garman–Klass
    7.4, Meilijson 7.7), which is free accuracy from a panel this repo now receives. But efficiency
    is not the binding criterion when the estimate is a divisor: Parkinson is mechanically
    correlated with the return it standardises (`|r|/σ_P ≤ sqrt(4 ln 2) ≈ 1.665`, correlation 0.79)
    and gives a bimodal tailless standardised distribution; Rogers–Satchell gives standardised
    kurtosis ≈ 124 because its drift-generality works against it at zero drift; **Garman–Klass is
    the only one of the set that standardises returns to approximate normality**, because
    subtracting the squared return cancels most of the correlation with `|r|` (0.79 → 0.36). Costs
    no trial — it is a change of estimator inside constructions the lab already runs. **What it does
    *not* license**: reopening the vol-targeting and inverse-vol constructions `learnings.md` has
    refuted. Those failed on their construction, not visibly on their measurement, and `CLAUDE.md`'s
    rule against carrying a family's constants across by analogy cuts here too — if the lab wants to
    claim measurement was the binding constraint, it has to re-measure and say so. Tier A
    (analytical), `validation_overlap: false`.
    → `notes/2026-08-29-range-based-volatility-estimators.md`

48. **[Added 2026-08-29] Free diagnostic that can close or open `seasonality-calendar` before a
    trial is spent, plus the version of the signal to scout if it opens.** Heston–Sadka's result is
    a **sign prediction**, which makes it unusually cheap to pre-test: the cross-sectional
    winner-minus-loser spread should be **positive at every annual lag** (t−12, t−24, …) and
    **negative at the non-annual months of the same intervals**. Run that contrast as a
    holdings-free measurement on the training split — under `CLAUDE.md` diagnostic work that scores
    no returns is free and unlimited. If the sign pattern is absent on this universe, the family
    closes for one diagnostic and zero trials; if present, the scout is motivated by a measurement
    rather than a citation. **The version to scout is the single 12-month lag**, not the twenty-year
    ladder: it needs thirteen months of history instead of twenty-one years, is available for the
    whole universe rather than a survivor-selected subset (which is the severe case in
    `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`, since the claim being
    tested *is* a persistence claim), and is the version the paper reports as having the best
    return-per-unit-risk. Tier A, `validation_overlap: false`.
    → `notes/2026-08-29-same-calendar-month-seasonality.md`

49. **[Added 2026-08-29] The one *build* this session opens, and it is an overlay rather than a
    book: an asymmetric, signal-conditional no-trade band that defers trades the incumbent was
    going to make anyway.** This is the authors' own suggestion, not an inference — Heston–Sadka
    decline to recommend trading their signal (a seasonal strategy "requires rebalancing the entire
    portfolio every month", and they doubt the round-trip costs are worth it) and instead observe
    that "it is relatively simple to postpone the sale or purchase of a particular stock if it has a
    large positive or negative expected return over the next month." That **adds no turnover; it
    re-times existing turnover**, which is precisely the axis `learnings.md` says is the lab's live
    one. Structurally it is the banding/no-trade-region mechanism the folder already ranks first
    among cost-mitigation techniques, but with an **asymmetric, signal-conditional** band instead of
    a symmetric one — a combination this folder has never recorded and the lab has never tried.
    Ranked below the free rules because it is a real trial with a real design space. Tier A,
    `validation_overlap: false`.
    → `notes/2026-08-29-same-calendar-month-seasonality.md`,
    `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`

50. **[Added 2026-08-29] Free design screen for every `statistical-learning` candidate, at the top
    with #1, #2 and #29: does the proposed feature set have an *interaction* story? If not, use a
    penalised linear model and expect a heavier learner not to help.** Gu–Kelly–Xiu's cleanest
    diagnostic is that a generalized linear model over **spline expansions of individual features** —
    arbitrary univariate nonlinearity, no interactions — fails to beat the purely linear models
    despite selecting more features, so the entire tree/neural-net advantage traces to predictor
    interactions rather than to curvature; their Monte Carlo confirms it in both directions. Two
    riders that cost nothing and come from the same source: **dimension reduction beats variable
    selection** (PCR/PLS over elastic net, because characteristics are "partially redundant and
    fundamentally noisy" — the folder's averaging-beats-selecting result, now stated about features
    rather than models), and **Huber loss beats squared loss** for every method where both were run.
    Also free, and the mechanism behind a result the lab already measured: penalised linear models'
    variable importance is "highly skewed toward momentum and reversal", which is *why* feeding a
    learner the incumbent's lookbacks reproduces the incumbent at higher `rho` and lower Sharpe —
    **if the point of the candidate is a decorrelated leg, the trend features have to be excluded or
    orthogonalised deliberately, because the estimator will not do it for you.** Tier A,
    `validation_overlap: false`, `published_post_2018: true`.
    → `notes/2026-08-29-machine-learning-cross-section-comparative.md`

51. **[Added 2026-08-29] Import discount, free, and it applies to the whole
    `statistical-learning` literature rather than to one paper: every economic-gain figure in the
    reference ML asset-pricing study is *gross*.** Gu–Kelly–Xiu model no transaction costs
    anywhere, report no turnover, and ask their models for return accuracy rather than for stable
    holdings — the objective never penalises re-ranking the entire cross-section every period. The
    lab has already paid this bill once (its ridge scout's monthly full-cross-section re-rank cost
    roughly a third of its margin over the equal-weight floor). Two protocol details from the same
    paper point the cheap way out and are worth copying verbatim: **refit annually** with an
    expanding training window and a rolling validation block, and use **no cross-validation**, to
    preserve temporal ordering. One further caution on ambition: the out-of-sample R² values that
    separate thirteen estimators there are *fractions of a percent per month*, on a cross-section
    200× larger than this one — a trial spent ranking estimators here is a trial spent on noise, and
    the reachable question is which **feature groups** carry signal, which is what `program.md`
    says the interesting question is anyway. Tier A, `published_post_2018: true`.
    → `notes/2026-08-29-machine-learning-cross-section-comparative.md`
52. **[Added 2026-08-30] Free screen for every `lead-lag-spillover` candidate, and it is three
    conditions, not one.** All three come from the family's founding sources and all three are
    computable on the train split without a trial. *(i) Control for the follower's own lag.* The
    mechanism's signature is cross-predictability that is **not** a restatement of own-lag
    predictability — Hong–Torous–Valkanov's model gives zero own-serial and non-zero cross-serial
    correlation precisely because investors condition efficiently on their own market — and
    Chordia–Swaminathan's tests are built around the same separation. Without the own-lag control,
    `price-trend` shows up wearing a lead-lag costume, and the lab already has a measured case of a
    differently-motivated family arriving at rho ≈ 0.75 to a momentum champion. *(ii) Count the
    leaders against chance, do not t-test a pair.* HTV simulate the null count (≈3.4 of 34 expected
    at the 10% level) and test whether the observed count is in the tail. With 15 regions there are
    210 ordered pairs here, so per-pair significance is meaningless and the count framing is
    mandatory. *(iii) Require horizon decay.* The effect should be visible at one month and
    materially weaker by three; HTV treat the *absence* of long-horizon predictability as evidence
    the short-horizon result is not a regression artifact. A lead-lag signal flat across horizons is
    a slow-moving risk proxy. Tier A, no overlap.
    → `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md`
53. **[Added 2026-08-30] The one genuinely new *signal* this session opens, and it costs nothing to
    compute: `DELAY`, a closes-only per-instrument speed-of-adjustment statistic.** From a Dimson
    regression of instrument *i* on an equal-weight universe return with five leads and five lags,
    `x = (Σ_{k=1..5} β_k)/β_0` and `DELAY = 1/(1+e^{−x})`; higher means slower adjustment to
    common information. Chordia–Swaminathan show it separates the names that contribute most and
    least to cross-autocorrelation, and that it is what their turnover sort is a proxy *for* — so
    sorting on it is strictly closer to the hypothesis than sorting on the proxy. It needs no
    volume panel, which matters because **this repo cannot compute their actual sorting variable**:
    turnover is shares traded ÷ shares outstanding, chosen exactly because raw and dollar volume
    correlate ≈0.78 with size while turnover correlates ≈0.15, and there is no shares-outstanding
    panel here. Substituting dollar volume reintroduces the size ranking the design exists to
    remove — which is the mechanism behind the lab's own measured null on log average dollar volume.
    The causal alternative if a volume-based sort is wanted anyway is **relative volume** (each
    name's volume over its own trailing average), which cancels the size level by construction but
    measures "unusually active for this name" rather than "active relative to float"; say which one
    the hypothesis is about. Two riders before spending a trial: estimate `DELAY` walk-forward on a
    year of daily data (the source re-estimates annually), and check its overlap with a trailing-vol
    sort first — high-`DELAY` names in the source are smaller and *lower* volatility, and this lab
    has refuted low-vol twice. Tier A, no overlap.
    → `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md`
54. **[Added 2026-08-30] Free reframing that decides what a `statistical-arbitrage` candidate can
    honestly claim, and it removes the family's headline selling point.** In the reference
    construction every position is a stock against βᵢ dollars of its factors: the residual is what
    is traded and the factor leg is what makes it *tradeable* rather than merely *measurable*. A
    long-only book at gross ≤ 1.0 holds only the cheap side, so what survives is not a
    market-neutral residual portfolio but a long book tilted by a residual signal, dominated by the
    market exposure it cannot remove. **Removing factor structure from the signal does not remove it
    from the book** — which is the mechanism-level explanation for the lab's measured 0.75–0.85
    cross-correlations among five long-only family leads from five different mechanisms. The
    consequence is a scoping rule, not a build: a candidate here answers a *selection* question
    ("does a residual s-score rank names better than a raw price rank?") and must not be argued as a
    decorrelation play. Tier B source, no overlap.
    → `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md`
55. **[Added 2026-08-30] The one buildable idea in `statistical-arbitrage`, and it is the specific
    thing the lab's declined screen did not test.** The source's structural finding is that the
    factor count has an **interior optimum**: one factor is its *worst* configuration (leftover
    common variation ⇒ slow measured reversion, high residual volatility), a 75% explained-variance
    target loses steadily (residual real but smaller than costs — "noise trading"), and its optimum
    is ~15 factors or a ~55% variance target on a US large-cap universe. The lab's screen tested
    k ∈ {1,3,5} — entirely inside the region this source also found worst — measured an
    **unconditional cross-sectional IC**, and declined the family. The source trades a **conditional
    excursion**: only names whose residual is >1.25 equilibrium standard deviations from its mean
    (`s = (X−m)/σ_eq`, `σ_eq = σ/√(2κ)`) *and* whose estimated reversion speed clears a filter
    (τ = 1/κ shorter than half the estimation window). An unconditional IC can be null while the
    conditional tail trade is not, and the κ-filter is a falsifiable admissibility condition nothing
    in this lab's reversal work has used. **Ranked below the free rules and with two explicit
    discounts**: 15 factors on ~140 instruments is a very different factor-to-name ratio (so the
    variance *target*, not the count, is the transferable parameter, and noise-trading arrives at a
    lower count here), and the source pays 5 bps per trade against this repo's 15 with a
    characteristic holding period of about a week — the configuration it reports losing money on is
    the regime a 3×-more-expensive book starts in. If run: fix the factor count by variance target,
    add the κ-filter and the |s| threshold, rebalance monthly not daily, and report the
    gross-versus-net decomposition, per `learnings.md`'s standing turnover warning. Tier B,
    no overlap. → `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md`
56. **[Added 2026-08-30] A use of the volume panel the lab has not tried: rescale returns rather
    than sort on them.** "Trading time" replaces each return with `R̃ = R × ⟨δV⟩/ΔV`, where ΔV is
    volume over the interval and ⟨δV⟩ a trailing average (≈10 days in the source, deliberately not
    optimised). Moves made on heavy volume shrink; moves made on light volume inflate. Economically:
    **do not fade a move that came with heavy trading**, because it is more likely information than
    an excursion worth reverting. Reported to help ETF-based residual signals unequivocally and to
    do little for PCA-based ones. It is a return *transformation*, so it composes with any existing
    reversal or reversion signal without adding a sort, and it is testable on the train split on its
    own. One implementation trap: volume is not forward-filled and is NaN on foreign holidays, so
    the trailing denominator must skip those rather than treat them as zero volume — otherwise the
    rescaling explodes exactly where the panel is thinnest. Tier B, no overlap.
    → `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md`
57. **[Added 2026-08-30] Two anti-candidates and one confound, all free.** *(a) Do not bolt a trend
    term onto a residual-reversion signal.* The source extends its s-score with an estimated drift
    (algebraically the slope of a 60-day moving average — a built-in momentum overlay) and reports
    the effect on results is minor; its own reading is that stock returns carry negligible momentum
    after controlling for industry/size factors at this trading scale. *(b) Do not assume the
    lead-lag sign.* HTV's model makes the sign of a cross-prediction follow the covariance of the
    two assets' payoffs, and their own leaders include both signs; a long-only "leader up ⇒ buy the
    laggard" construction imposes a sign the theory does not supply, so estimate it. *(c) A daily
    region-level lead-lag on this universe is a time-zone artifact until proven otherwise.* Fifteen
    regions with non-overlapping sessions and unhedged USD conversion mechanically manufacture "US
    leads Asia" at the daily frequency. Both source papers' own screens point the same way — drop
    returns where the instrument did not trade at *t* or *t−1*, and move to weekly. Note the
    asymmetry this creates for the family: the engine's one-day execution lag eats most of a daily
    effect and costs a monthly one almost nothing, so the two ends have opposite implementability
    profiles and a candidate has to live in the middle. Tier A/B, no overlap.
    → `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md`,
    `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md`,
    `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md`

58. **[Added 2026-08-31] The highest-value item this session produces: one free rank correlation
    that either confirms or reopens the lab's `liquidity-volume` verdict, plus the build it gates.**
    Lou–Shu's priced object is the **"constant" Amihud measure**
    `A_C = mean_d( 1 / dollar_volume_d )` over the estimation month — the |return| numerator
    deleted. It correlates 0.90 with full `ILLIQ`, is priced about as strongly, and the residual of
    `ILLIQ` on it is not priced at all. **`A_C` is not any volume functional the lab has tested.**
    The 2026-08-29 and 2026-08-30 screens used log *average* dollar volume and relative volume,
    both functions of the **mean** of volume; `A_C` is the mean of the **reciprocal**, and by
    Jensen these have different cross-sectional orderings, with the gap growing in within-month
    volume dispersion. Economically, `A_C` ranks instruments by *how illiquid they get on their
    quietest days*, not by how much they trade on average. **The free diagnostic, first:**
    rank-correlate `log(A_C)` against `log(mean dollar volume)` in the cross-section. Near 1.0 and
    the family closes properly — the lab's null already covered this functional under another name,
    and "under any normalisation" is earned. Materially below 1.0 and the null was measured on a
    different object, and the build is worth a trial: monthly `A_C` per instrument, ≥10 valid days
    required, cross-section winsorized at 1/99 (a mean of reciprocals is unbounded as volume → 0,
    so this is not optional), logged, **normalised within region**, ETFs excluded or their split
    neutralised, sorted long-only on high `A_C`. Lag two months, per the source's own convention.
    Carry three discounts into any hypothesis: the mispricing reading puts the effect in
    hard-to-arbitrage small illiquid names and this universe is the opposite tail; the conditional
    variation the paper identifies sits on the **short leg**, which long-only cannot reach; and
    cross-market volume comparability is a live confound over 15 regions — Lou–Shu drop a whole
    exchange from a *single-country* sample over exactly this. Tier A, no overlap.
    → `notes/2026-08-31-amihud-volume-component-decomposition.md`
    **Free and separable from the above: the residual sort as a general instrument.** Regress any
    composite signal cross-sectionally on its suspected driver and sort on the residual. Lou–Shu
    use it to prove which half of a ratio carries a premium; the lab has a standing "is this signal
    a known signal in costume" problem (#52's own-lag control, #57c's confound) and this is cheaper
    than another trial.

59. **[Added 2026-08-31] Free precondition check that decides whether `lead-lag-spillover` has a
    buildable grouping at all, plus one free construction change.** Hou's claim is that the
    lead-lag effect is *predominantly intra-industry* — so the grouping variable carries the
    hypothesis, and a region grouping is not evidence about the industry channel. **The check:
    does the 42-ETF list include sector or industry funds?** If yes, that is the only
    industry-ish taxonomy reachable without fundamentals and a grouping can be built from prices
    alone. If no, record that Hou's construction is **unreachable here** as a family-scoping fact
    rather than substituting geography by analogy — and read every past and future region-grouped
    lead-lag null as evidence about *regions as a diffusion channel*, which is a different finding
    from evidence about lead-lag. **The free construction change, independent of that check:**
    condition the leader's signal on **negative** moves. Hou puts the effect in sluggish adjustment
    to bad news, so a symmetric construction averages a live channel with a dead one; and the
    asymmetry doubles as an identifying test, since momentum-in-costume should not care about the
    sign of the leader's move (it sharpens #52's screen (iii)). Expect a weak effect even when
    reachable: the source puts it in small, less competitive, **neglected** industries, and ~145
    large globally-known instruments are the neglect-free end of all three sorts. Tier A on venue
    and citations, but **abstract-only** — no construction detail, lookback, or robustness evidence
    was obtainable, so treat as strong prior, not verified.
    → `notes/2026-08-31-intra-industry-lead-lag-grouping.md`

60. **[Added 2026-08-31] The one measurement that decides whether `portfolio-learning` is actually
    closed — free, and it corrects a statistic the closure rests on.** `learnings.md` closed the
    family by pricing equal-weight ensembles of the eight legs' **stored return series** and
    finding them monotone decreasing against the best single member. That is the **portfolio mix**,
    which this literature says is bounded between its components *by construction*; the
    **integrated** construction — average the legs' cross-sectional *scores*, then build one
    long-only book in a single step — is not subject to that bound, and has not been measured here.
    The gap between them is governed by the **cross-sectional correlation of the signals**, and the
    0.68–0.98 the lab measured is the correlation of *realised return series of long-only books*,
    which shares a large common market component and sits far above the signal correlation
    underneath. **So: recompute the correlation matrix on cross-sectional signal ranks.** Still
    0.7–0.98 and the family closes on the literature's own terms, twice over, and the lab can say
    so. Materially lower and the closure was measured on a confounded statistic, and the integrated
    build is worth one trial: expose each lead's cross-sectional score, average the z-scores with
    **equal** weights (the parameter-counting screen, #1, forbids estimating them), construct once.
    Note this is a *different function* from `strategies/lib/blend.py`, which combines books — it
    needs a new file in `strategies/lib/`. **Mandatory screen if built:** check the integrated book
    against a plain low-volatility book first. The peer-reviewed rebuttal's specific finding is
    that integration's apparent edge is a low-risk tilt, averaging scores mechanically de-extremes
    the book, and the lab has already refuted low-vol tilts on this universe. Three standing
    discounts: the mechanism's gain → 0 as signal correlation → +1 and → 0 as active risk → 0;
    breadth enters directly, and a ~145-name cross-section holds few of the jointly-attractive
    names integration exists to find; and the solved required-leg-Sharpe bar (1.34–1.42 against a
    1.120 champion) is a separate constraint that none of this relaxes. Tier B — the mechanism is
    sound and general, the magnitude is contested in a peer-reviewed venue and must not be imported
    into a hypothesis. → `notes/2026-08-31-signal-blending-vs-portfolio-blending.md`

61. **[Added 2026-09-01] The free two-number screen that either opens `range-variance` or closes
    it for the fourth time — and it is the highest-priority item on this list because that family
    has zero recorded trials and `learnings.md` has flagged it to the human as unproposable on
    current evidence.** All eight mechanisms screened there sort on the **width** of the return
    distribution; the lottery mechanism sorts on the **upper tail only**. Compute, on train:
    `MAX(5)` = the mean of the five largest daily returns of the past month, and `MIN` = the
    negative of the smallest. Then read **two** things. *(i)* **Persistence** — the decile
    transition rate of `MAX(5)` month to month. The source's mechanism requires it (an investor
    must be able to buy lottery exposure in advance) and reports roughly one-in-three staying in
    the top decile; if `MAX(5)` does not persist here, stop. *(ii)* **The sign test** — the
    information coefficients of `MAX(5)` and `MIN`. **Same sign ⇒ it is volatility**, which this
    lab has refuted three ways, and the family closes properly on the source's own identifying
    test. **Opposite signs (`MAX` negative, `MIN` positive) ⇒ the asymmetric mechanism is present
    and `range-variance` has its first honest candidate.** Note what this screen fixes: the lab's
    2026-08-29 range-lottery reading (−7.95%/yr, t = −4.30) is a **significant result with the
    predicted sign**, dismissed as "just low-vol" — but a *range* proxy is a width measure, i.e.
    exactly the confounded object `MIN` exists to separate, so the confound was used to dismiss
    the effect it confounds. If the screen passes, the buildable version is `MAX(5)`
    orthogonalised **within trailing-volatility terciles** (the machinery exists — it is what
    settled the `ILLIQ` confound on 2026-08-29), used as a long-only **underweight or exclusion
    screen** rather than a spread trade, since the low-`MAX` leg is the high-return leg and is
    the reachable one. Mandatory second control: **within reversal terciles**, because `MAX(5)`
    is a formation-month statistic and raw 5-day reversal is the strongest thing on this universe
    (IC +0.0455, t = +4.49) — without it, any result is reversal in costume. Sort within the
    single-name subset only (ETFs are diversified by construction and cannot be lottery assets),
    and expect the **weakest end** of the effect: the source says plainly it is concentrated in
    small caps, and the cross-country companion finds it in 26 of 42 countries. The one favourable
    asymmetry is that this universe's survivorship artifact points the *wrong way* for the
    hypothesis, so a positive finding is unusually credible here and a null is uninformative.
    Tier A. → `notes/2026-09-01-max-lottery-extreme-positive-returns.md`

62. **[Added 2026-09-01] The one volume functional this lab has not screened, and it is a
    *residual* rather than a level — free, and it is the last thing standing between
    `liquidity-volume` and a clean third closure.** Every volume object screened here is a
    function of the volume **level** or of volume scaled by a price move: `ILLIQ`, ratio-of-means
    Amihud, constant-Amihud `A_C`, log average dollar volume, relative volume. **Standardized
    unexplained volume (SUV)** is none of those. Recipe, from Garfinkel (2009) via
    Freyberger–Neuhierl–Weber: over the trailing month, regress **daily volume** on a constant and
    on the absolute values of **positive and negative daily returns as two separate regressors**
    (volume may respond asymmetrically to up- and down-moves); SUV is the sum of the residuals,
    standardized by the residual standard deviation. It is trading activity **orthogonal by
    construction to the contemporaneous price move**. Two reasons it earns the slot: it is one of
    the **seven characteristics surviving at the largest size cut** in a Tier-1 nonparametric
    conditional selection, and one of only **four stable across every sample half, knot count and
    size cut**; and this repo's universe is the large-cap regime where that source predicts most
    other characteristics stop working — which it does, and which the lab has already observed
    without a reason. **Pre-register the closure rule before looking**, as `A_C` was: compute
    `spearman(SUV, log ADV)` and `spearman(SUV, |return|)` first — if either is ≈0.9, SUV inherits
    a measured null and the family closes for good; if both are low, measure its IC at 5/21/63 days
    and apply screen (iii) of #52. Pitfalls: volume is **not forward-filled** and is NaN on foreign
    holidays, so fix a minimum-valid-observations rule per name **before** seeing a result, or the
    signal is defined on a different number of days per region; and run the regression on **log**
    volume, since raw volume is a share count in native units. Tier B source (single market, no
    costs modelled). → `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md`

63. **[Added 2026-09-01] The audit the integrated max-of-z book needs before anything is built on
    it — free, no trial, no holdout read, computable from stored trial return series.** The lab's
    strongest non-`price-trend` result is a four-leg max-of-z integration quoted as a 0.88–1.01
    range. Novy-Marx's remedy, in his own order of preference, is to **evaluate each leg's
    marginal alpha relative to all the others**, Bonferroni-corrected for the number of signals
    *considered* (not merely employed), rather than reading the composite's own statistic. Run it.
    It answers the question the lab currently cannot answer about that book: **which legs are
    carrying it, and would any survive being priced against the other three** — and if the edge
    collapses onto one leg, that leg is the candidate and the integration is decoration. Three
    things to hold while reading the result. *(i)* The paper's **critical-value table does not
    transfer numerically** to a max operator: every value in it is derived for *linear* composites,
    and the max is precisely the construction that escapes his linearity equivalence. *(ii)* The
    **selection half transfers undiminished** — four legs chosen from a screened pool of order
    20–30 puts this squarely in the `n^k` regime. *(iii)* A composite of four **family leads**
    contains no mediocre legs, which is the paper's stated signature of selection bias on top of
    overfitting bias, worth roughly 60% of extra expected `t`; **expect the integrated book's edge
    over its legs to shrink out of sample for this reason alone**, independent of every other
    discount already recorded. This is a discount on inference, not on the mechanism: the same
    paper is explicit that combining signals you believe in individually is fine.
    → `notes/2026-09-01-multi-signal-overfitting-critical-t.md`

64. **[Added 2026-09-01] A refuted signal that was refuted as the wrong *kind* of thing, and the
    correction is cheap.** `learnings.md` records 52-week-high proximity as "tried and refuted",
    and reading the entry: it was swapped in as a **drop-in replacement for the champion's
    return-magnitude z-score inside the same buffer-band machinery**, and it failed because the
    bounded `(0,1]` ratio clusters near 1 and more than doubled turnover. That is a refutation of
    one construction, and the entry says so itself. Freyberger–Neuhierl–Weber find closeness-to-
    the-52-week-high surviving **conditional on momentum, short-term reversal and long-term
    reversal**, and among the four characteristics stable across every specification they run —
    i.e. as an **additional** signal, not a better momentum score, which is exactly the use the
    lab's refutation did not test. The turnover objection is construction-specific and has a known
    fix in this repo: **rank the signal and feed it to the max-of-z integration** rather than to a
    buffer band, where the clustering-near-1 problem becomes a rank problem and disappears. Cheap,
    and it re-opens one line rather than a family. Same Tier B source and the same caveat: a
    US-only shortlist, imported into a 15-region universe against this folder's standing
    local-versus-global warning.
    → `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md`

65. **[Added 2026-09-01] The narrowest learned candidate this folder has ever been able to
    justify, and it satisfies `learnings.md`'s own design rule for the first time.** That rule
    says a learned candidate earns a trial only when it is asked for **something a sort cannot
    express**. Freyberger et al. name the something, and it is not an interaction: it is **the
    shape of one characteristic's relation to expected return**. Their out-of-sample evidence is
    unusually clean on this point — the nonparametric model selected **eight** characteristics
    against the linear model's **twenty-one** and beat it; handing the *nonparametric* estimator
    the linear model's 21 characteristics **improved** out-of-sample performance, while handing
    the *linear* estimator the nonparametric model's 8 changed nothing. **The gain is in the
    functional form, not the characteristic count.** A monotone rank sort is itself a
    functional-form assumption and probably a wrong one. The minimal departure: a **quadratic
    spline in the cross-sectional rank of a single characteristic** — a handful of parameters,
    walk-forward fittable with `strategies/lib/walkforward.py`, cheap enough to refit monthly,
    and asked for exactly one thing a sort cannot do. **Do not import their shortlist as a feature
    block**: their selection consistency needs hundreds of thousands of observations and this
    cross-section is three orders of magnitude smaller, and #63 above is the reason a
    multi-characteristic composite is the wrong next object.
    → `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md`

66. **[Added 2026-09-02] The free test that replaces the seasonality screen this lab failed and
    then argued past — and the reason the failure was over-read.** On 2026-08-29 the lab
    pre-registered Heston–Sadka's *sign disagreement* (annual lags positive, non-annual negative),
    measured both positive, and concluded that "the contrast that separates a calendar seasonal
    from persistent cross-sectional mean-return differences is absent here". **Keloharju–
    Linnainmaa–Nyberg predict that failure**: their central claim is that the seasonal component
    *overwhelms* the unconditional cross-sectional component rather than opposing it in sign, so a
    positive non-annual coefficient is what a universe with large persistent mean-return
    differences should produce and does not by itself deny a seasonal. The discriminating test they
    use is a **fixed-effects contrast**: the annual-lag pattern survives stock fixed effects and
    **vanishes under stock-calendar-month fixed effects**; equivalently, rank the *same* assets over
    the *same* window on same-calendar-month history versus other-calendar-month history and check
    that only the former carries information. Both are free panel computations on train. This is
    a correction to a screen the lab is still carrying, and it costs no trial either way. Tier A,
    no overlap.
    → `notes/2026-09-02-return-seasonalities-common-factors.md`

67. **[Added 2026-09-02] One free number that either re-opens the `calendar` half of
    `seasonality-calendar` or closes it for good — and it is the number the lab's own closure asked
    for.** `learnings.md` (2026-09-01) closed the half structurally: long-only at
    `max_leverage = 1.0` can exploit a calendar effect only if the **complement window's return is
    at or below zero**, and the complement was measured at +11% to +14%/yr. But the window tested
    was **(before = 1, after = 3)**, i.e. T−1 to T+3, and its "complement" pooled ordinary mid-month
    days with the one window the mechanism says is *negative*. Etula–Rinne–Suominen–Vaittinen
    decompose the payment cycle into three windows with different predicted signs —
    **T−8 to T−4 liquidity-motivated selling (negative)**, T−3 to T+3 positive reversal, T+4 to T+8
    negative reversal — with the timing pinned by **settlement conventions rather than fitted to
    returns** (their identifying evidence: the 1-day-settlement Treasury market's pressure window
    sits later than the 3-day equity market's). **Measure the mean daily return of T−8 to T−4 alone
    on train.** At or below zero, the closure's own binding condition is met for a narrow overlay
    (~12 round trips a year against the 24 the closing screen priced at 3.60%/yr). Positive, and
    the family closes a second time and should be recorded as final rather than re-litigated. Note
    the settlement caveat: the recipe sits under a 3-day convention and US equity settlement
    shortened to 2 days in 2017, shifting the predicted last-sale day one day later — verify the
    offset, do not hard-code it. Tier A, no overlap, `published_post_2018: true`.
    → `notes/2026-09-02-turn-of-month-payment-cycle.md`

68. **[Added 2026-09-02] A free interpretation rule that applies retrospectively to every note in
    this folder, and which would have predicted the lab's entire empirical history.** Fama–French
    sort anomalies separately by size group and find that **net stock issues, accruals and momentum
    are pervasive in all size groups, while asset growth is absent among big stocks** — the group
    accounting for more than 90% of market capitalisation. The construction artifact behind the
    difference: tiny stocks are ~3% of market cap but ~60% of the *number* of stocks, and have the
    largest cross-sectional dispersion in anomaly variables, so they occupy more than 60% of the
    names in the extreme deciles of an equal-weight all-stock sort. **This universe is entirely
    "big"** — ~145 large-cap names plus 42 ETFs — so every trial this lab has run is a big-stock
    sort. Of the three predictors certified pervasive there, two need fundamentals this repo lacks,
    **leaving momentum as the only one computable from daily OHLCV** — and `price-trend` holds all
    7 promotions while every characteristic-*level* family has closed (`liquidity-volume` twice,
    `range-variance` four times). **The rule: before proposing a candidate from a source, ask
    whether that source reported the effect separately for big stocks and whether it survived
    there. If it reports only an all-stock equal-weight spread, discount hard regardless of tier or
    citation count.** Cheaper than a trial, and it makes the next characteristic-family null cheap
    to skip rather than merely cheap to interpret. Tier A, no overlap.
    → `notes/2026-09-02-anomalies-by-size-group.md`

69. **[Added 2026-09-02] The seasonal candidate that fits this universe's actual shape, and the
    most principled source of an orthogonal leg the live `portfolio-learning` question has been
    given.** Keloharju–Linnainmaa–Nyberg show seasonality strategies trading **well-diversified
    portfolios formed on characteristics such as size and industry** are about as profitable as
    those trading individual stocks, and document the same effect in the cross section of **country
    stock-market indexes** and in commodities. This repo has **42 ETFs across 15 regions** — exactly
    those diversified portfolios — and an ETF-only seasonal sort sidesteps the survivorship bias
    `program.md` warns inflates single-stock results, which is the standing objection to the lab's
    existing single-name seasonal leg. Two further reasons it is the right next object here:
    the authors measure seasonality strategies **in different corners of the market as
    near-uncorrelated with each other** (≈0.17 between the small-stock and high-dividend-yield
    versions; negligible across asset classes), which is a *measured* rather than hoped-for source
    of the "fifth maximally orthogonal leg" that `learnings.md`'s 2026-09-01 leg-count contrast
    needs; and their signal is the **average same-calendar-month return over the prior 20 years**,
    cross-sectionally demeaned. **Precondition, to run first and for free: count the available
    annual lags per instrument.** The store's history bounds how many the newest instruments have,
    and warmup shortens the eligible universe the way `learnings.md` has already recorded for other
    long-lookback constructions — the honest version of this signal may not fit, and that is itself
    a finding. Two riders carried from the source: **do not neutralise the systematic exposure**
    (the authors show the factor exposure is the effect's carrier — at least two-thirds of the
    seasonality is common-factor-borne, and hedging it removes the effect), and re-verify the
    month alignment against the corrected helper, since `learnings.md` records that the lib's
    `seasonal_same_month_return` once traded a month late. Tier A, no overlap.
    → `notes/2026-09-02-return-seasonalities-common-factors.md`

70. **[Added 2026-09-03] The free eigenvalue screen that decides whether a learned combiner is worth
    a trial here — and the correction to the design rule the lab drew from the one it already ran.**
    `learnings.md` (2026-08-29) fed a penalised linear combiner eleven features, got `rho` 0.774 to
    the champion at a lower Sharpe, then got `rho` 0.976 to a single one of four inputs, and
    concluded a learned candidate earns a trial only if no single feature already works alone. That
    trial regressed **returns on features with a uniform L2 penalty**. Kozak–Nagel–Santosh's
    estimator is a different object: `b̂ = (Σ + γI)⁻¹ μ̄`, ridge on the map from **covariances to mean
    returns**, whose shrinkage is **unequal across principal-component directions by construction**
    — low-eigenvalue directions are shrunk hardest, high-variance ones barely. The lab's result is
    therefore evidence about ridge-on-features, not about this estimator, and the rule derived from
    it targets the wrong failure. **The screen, which is free and is the paper's own identifying
    prediction:** build the lab's existing legs as rank-based zero-investment managed portfolios
    (`z = (rank/(n+1) − mean) / Σ|deviation|`, factor return `F = Z′R`), take the daily covariance
    matrix of those factor returns, and check whether **mean returns line up with the high-variance
    PCs** — report the eigenvalue spectrum next to each PC's mean and t-statistic. Line up, and the
    economic prior transfers and a KNS-form combiner is worth a trial; unrelated to the eigenvalue
    ordering, and the prior does not transfer and the idea closes without a trial. Either answer is a
    finding, and neither costs one. A second free gain regardless of the outcome: γ maps one-to-one
    to `κ`, the **prior root expected maximum squared Sharpe ratio**, so the regularisation constant
    this repo cannot legally cross-validate becomes a stated prior instead of a tuned parameter.
    **Hard caveat:** their K-fold CV splits the whole sample and is explicitly upward-biased —
    illegal here; select γ walk-forward or fix it a priori from `κ`. Tier A, no overlap.
    → `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`

71. **[Added 2026-09-03] A second free diagnostic, on the *benchmark a signal is scored against*
    rather than on the signal — and it is a question the lab has never asked separately from
    weighting.** Avramov–Cheng–Metzker decompose learned-signal payoffs against an industry
    benchmark into unconditional, **intra-industry** (long peer-group winners) and inter-industry
    (industry rotation) components, and find the intra-industry version outperforms both others: the
    content is in **peer-relative** ranking, not in picking groups. This is free to run on every leg
    the lab already has — rebuild each score as a deviation from its region or sector peer-group mean
    and compare the holdings and the train-decile spread against the unconditional version. Note
    carefully what it is *not*: `learnings.md` closed regional neutralisation by a bracket, but that
    was about **weights** (neutralising the book's regional exposure). This is about the **scoring
    benchmark** (what each name's score is measured relative to), which is a different operator and
    an untested one. Tier A, no overlap, `published_post_2018: true`.
    → `notes/2026-09-03-machine-learning-economic-restrictions.md`

72. **[Added 2026-09-03] The one new *mechanism* on this list, and it is the cheapest construction
    the `statistical-arbitrage` family has been given.** Gatev–Goetzmann–Rouwenhorst's distance
    method estimates nothing: match each instrument to the partner minimising the **sum of squared
    deviations between normalised cumulative total-return series** over a trailing 12 months, open
    when the pair diverges past **2 formation-window standard deviations**, close at the **next
    crossing**, 6-month trading window, **one-day execution delay**, **six overlapping monthly
    tranches**. The last three are already this repo's conventions, and the overlapping-tranche
    structure is the lab's own strongest recorded mechanism. **Long-only version:** hold the names
    most depressed relative to their own matched partner, capped and equal-weighted — a *selection*
    rule, since the hedge leg is unholdable and the book therefore keeps the common exposure the pair
    was built to remove (the same diagnosis this folder reached for residual reversion, from a
    different construction). It is the family's first genuinely **conditional** object, which is
    exactly the untested half of the tension `SUMMARY.md` recorded when the lab declined residual
    reversal on an *unconditional* IC. **Run two free things first, in this order.** (a) **Count the
    matching pool and the match-distance distribution per region.** ~145 names across 15 regions is
    thin; if the best available partner for most names is a poor match, the mechanism is absent by
    construction — the same precondition shape that killed #69, and the same honest outcome. Expect
    the ETFs to dominate the closest matches (broad index funds have little idiosyncratic variance,
    the same reason utilities dominated the source's top pairs), and decide their eligibility in
    advance. (b) **Screen the pair-spread z-score panel's forward-return spread on train** before
    spending a trial. **And specify the placebo with the candidate**: the source's own control is a
    random-within-group partner assignment traded by identical rules, which is one extra
    weight-matrix build and is what makes either result interpretable — the control `learnings.md`
    (2026-09-02) named as the lab's cheapest and least-used falsification. Riders: restrict matching
    within region (cross-region "substitutes" are currency and region factors); prefer **finer**
    grouping, which is where the independent cost-aware reexamination reports the surviving profit;
    expect decay, since this is a heavily published top-journal rule; and **measure turnover
    holdings-only** rather than assuming the source's low round-trip count survives a monthly
    long-only rebuild. Tier B, no overlap.
    → `notes/2026-09-03-pairs-trading-distance-method.md`

73. **[Added 2026-09-03] An anti-candidate with a measurement behind it, stacking with #68 into the
    folder's most general pre-trial discount.** Avramov–Cheng–Metzker measure where the *incremental
    value of nonlinearity* lives: deep learners beat the linear IPCA on an all-stock sample, but
    their advantage collapses on cheap-to-trade subsamples while IPCA's performance barely moves.
    Excluding microcaps cuts deep-learning risk-adjusted payoffs by roughly half to three-quarters
    and excluding distressed names removes most of the remainder, after which none is significant at
    the 5% level; turnover of ~87–150% a month drives the implied break-even one-way cost to at or
    below plausible cost levels. **This universe is the restricted subsample permanently** — no
    microcaps, no distress, everything rating- and analyst-covered. **The rule: a candidate proposing
    a tree ensemble, a boosted learner or a neural network on this cross-section should be expected
    to reproduce its penalised-linear counterpart at higher turnover, and can be declined on that
    prior without a trial.** State the model class's expected gain over linear *before* building, and
    if the answer is "the nonlinearity", say which names are supposed to supply it. Where this
    universe differs from the paper's restricted subsample is that its long leg is holdable and the
    learned signals' payoff there was the significant half — so the discount applies to *model
    class*, not to the family. Tier A, no overlap, `published_post_2018: true`.
    → `notes/2026-09-03-machine-learning-economic-restrictions.md`

## Coverage log

| Date | Focus | Sources covered (notes) |
|---|---|---|
| 2026-08-17 | Cross-sectional momentum: construction mechanics, signal horizon, crash risk; plus cross-cutting publication decay | Jegadeesh–Titman 1993 (`2026-08-17-jegadeesh-titman-overlapping-momentum.md`); Novy-Marx 2012 + Goyal–Wahal 2015 (`2026-08-17-momentum-horizon-echo.md`); Daniel–Moskowitz 2016 + Barroso–Santa-Clara 2015 (`2026-08-17-momentum-crash-risk-management.md`); McLean–Pontiff 2016 (`2026-08-17-mclean-pontiff-publication-decay.md`) |
| 2026-08-17 (session 2) | Portfolio construction & rebalance mechanics as its own literature — the gap flagged highest-value last session: which trades to skip, when to trade, how much to hold | Novy-Marx–Velikov 2016 (RFS) + 2019 (FAJ) (`2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`); Hoffstein–Sibears–Faber 2019 + Hoffstein–Faber–Braun 2020 (`2026-08-17-rebalance-timing-luck-tranching.md`); DeMiguel–Garlappi–Uppal 2009 + Kritzman–Page–Turkington 2010 (`2026-08-17-naive-vs-optimized-weighting.md`) |
| 2026-08-17 (session 3) | The two zero-coverage families: 7 (ensembles) — chased specifically to find the missing economic mechanism for the lab's temporal-breadth result — and 2 (time-series momentum / trend following), including its replication status | Timmermann 2006 (Handbook ch. 4) + Smith–Wallis 2009 (OBES) + Rapach–Strauss–Zhou 2010 (RFS) (`2026-08-17-forecast-combination-why-averaging-beats-selecting.md`); Pesaran–Timmermann 2007 + Pesaran–Pick–Pranovich 2013 (J. Econometrics) (`2026-08-17-averaging-over-estimation-windows.md`); Moskowitz–Ooi–Pedersen 2012 (JFE) + Huang–Li–Wang–Zhou 2020 (JFE, replication challenge) + Hurst–Ooi–Pedersen 2017 (JPM) (`2026-08-17-time-series-momentum-evidence-and-replication.md`); Zakamulin 2015/2017 (`2026-08-17-moving-average-rules-anatomy.md`) |
| 2026-08-17 (session 4) | The two remaining under-covered *strategy* families — 3 (vol targeting) and 4 (short-term mean reversion) — plus the open question flagged last session on cross-sectional vs time-series signal construction. First session with full text read directly for every source. | Moreira–Muir 2017 (JF) + Cederburg–O'Doherty–Wang–Yan 2020 (JFE, replication challenge) (`2026-08-17-volatility-timing-managed-portfolios.md`); Nagel 2012 (RFS) + Lehmann 1990 (QJE) + Lo–MacKinlay 1990 (RFS) (`2026-08-17-short-term-reversal-as-liquidity-provision.md`); Goyal–Jegadeesh 2018 (RFS) (`2026-08-17-cross-sectional-vs-time-series-construction.md`) |
| 2026-08-18 (session 5) | The last two uncovered axes named as open by session 4: family 5 (low-vol / quality), chased specifically at the *sector-neutralized* construction `learnings.md` named as the only thing that would reopen it, and the **risk-parity half** of family 3 (weighting within comparable-diversification sleeves). Full text read directly for every source. Both axes close negative; no family in `program.md` is now uncovered. | Asness–Frazzini–Pedersen 2014 (FAJ) (`2026-08-18-low-risk-investing-industry-neutral.md`); Novy-Marx 2016 (NBER WP 20591) + Novy-Marx–Velikov 2022 (JFE, replication challenge) (`2026-08-18-defensive-equity-replication-and-construction.md`); Maillard–Roncalli–Teiletche 2010 (JPM) (`2026-08-18-risk-parity-equal-risk-contribution.md`) |
| 2026-08-19 (session 6) | Not a strategy family — the seam session 5 named as the one worth chasing: **why averaging unstable predictors improves them**, hunted in the two literatures it named (bagging / bootstrap aggregation, and model averaging outside the break-detection framing), plus the finance-native version of the same question (breadth and strategy risk). First session to yield a mechanism that is an unconditional accuracy claim about the repo's own strongest mechanism. Full text read directly for Breiman, Buja–Stuetzle, Hansen and the fundamental-law derivation; partial (first two pages) for the published Ding–Martin. | Breiman 1996 (Machine Learning) + Buja–Stuetzle 2006 (Statistica Sinica) (`2026-08-19-bagging-averaging-unstable-predictors.md`); Grinold 1989 (JPM) + Ding–Martin 2017 (J. Empirical Finance) + Ding 2010 WP (`2026-08-19-fundamental-law-breadth-and-strategy-risk.md`); Hansen 2007 (Econometrica) (`2026-08-19-model-averaging-mallows-weights.md`) |
| 2026-08-20 (session 7) | Session 6's top-ranked open question (a): **the bridge from a forecast-accuracy or information-ratio claim to realised net return on a constrained, cost-paying book**, chased in the two vocabularies it named — friction-aware dynamic portfolio choice, and portfolio choice that optimises the realised objective directly rather than a predictive loss. Answered from three directions, with a fourth cost-mitigation mechanism found as a by-product. Full text read directly for all four sources. | Gârleanu–Pedersen 2013 (JF; NBER WP read in full) (`2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md`); Brandt–Santa-Clara–Valkanov 2009 (RFS) + Lamoureux–Zhang 2024 (RAPS, critique) (`2026-08-20-parametric-portfolio-policies.md`); DeMiguel–Martín-Utrera–Nogales–Uppal 2020 (RFS) (`2026-08-20-trading-diversification-combining-signals.md`) |
| 2026-08-21 (session 8) | Session 7's open questions (b) and (c), taken together as one theme: **what constraints actually do to a portfolio, and how to count diversification honestly.** Three sources, full text read directly for all three. The session's shape is one *correction* (constraints are estimators as well as leaks), one *closure* (the effective-number-of-bets axis, worth one session, now spent), and one genuinely uncovered axis found by accident (the diversification return, i.e. the part of a book's geometric return that comes from rebalancing rather than from its signal). | Jagannathan–Ma 2003 (JF; NBER WP 8922 read in full) (`2026-08-21-weight-constraints-as-covariance-shrinkage.md`); Meucci 2009 (Risk) + Polakow–Gebbie 2008 (J. Asset Management; arXiv preprint read in full) (`2026-08-21-effective-number-of-bets-diversification-measurement.md`); Willenbrock 2011 (FAJ; arXiv version read in full) + Booth–Fama 1992 (FAJ, second-hand via Willenbrock) (`2026-08-21-diversification-return-and-rebalancing.md`) |
| 2026-08-22 (session 9) | Session 8's two named open questions, taken in order: (a) the decomposition of a **signal-driven** book's geometric return into a strategic and a rebalancing term — the axis session 8 called the highest-value remaining thread — and (b) the counterweight to the folder's constraints-are-good prior. Three sources, full text read directly for all three. The session's shape is one *theorem* that closes (a) at the identity level, one *correction* that reverses the sign the folder had assumed for the rebalancing term on a momentum book, and one *dissolution* of (b) into a continuum. | Fernholz–Karatzas 2009 (Handbook of Numerical Analysis Vol. XV; INTECH-hosted PDF read in full), building on Fernholz–Shay 1982 (JF) (`2026-08-22-excess-growth-and-return-decomposition.md`); Cuthbertson–Hayley–Motson–Nitzsche 2016 (IJFE; City Research Online accepted version read in full) (`2026-08-22-rebalancing-return-attribution-critique.md`); Brodie–Daubechies–De Mol–Giannone–Loris 2009 (PNAS; arXiv:0708.0046v3 read in full) (`2026-08-22-long-only-as-l1-regularization.md`) |
| 2026-08-23 (session 10) | Session 9's open question (b), the last unpatched seam: **what the lab is actually scored on**, attacked from both ends. End one — the currency the folder imports in: the geometric-mean-maximisation / growth-optimal (Kelly) literature and its criticism, chased specifically to settle whether a log-growth quantity can ever be a scoring axis. End two — the currency the lab is scored in: the sampling distribution of the Sharpe ratio itself, which nothing in nine sessions had covered. Three notes, full text read directly for all three primary texts. The session's shape is one *closure* (log growth has no exchange rate to a risk-scored objective, which retires session 9's own top candidate and explains the lab's `gamma*` null), one *anti-candidate plus two re-weighted screens* (Kelly as a leverage rule; means >> variances >> covariances, with the multiple rising as the book gets more aggressive), and one *new free measurement* on the repo's headline statistic (the `eta(q)` annualisation check and a standard error). | Samuelson 1971 (PNAS; EuropePMC copy read in full) + Merton–Samuelson 1974 (JFE; MIT Sloan WP 623-72 read in full from MIT DSpace) (`2026-08-23-geometric-mean-maximization-fallacy.md`); MacLean–Thorp–Ziemba 2010/2011 (Quantitative Finance / World Scientific handbook chapter; authors' dated draft read in full from a Berkeley course page), with MacLean–Ziemba–Blazenko 1992 (Management Science) and Chopra–Ziemba 1993 (JPM) recorded **second-hand and flagged** — both closed-access, their tables reproduced in the text read (`2026-08-23-kelly-criterion-growth-security-tradeoff.md`); Lo 2002 (FAJ; course-page mirror read in full) (`2026-08-23-statistics-of-sharpe-ratios.md`) |
| 2026-08-24 (session 11) | Session 10's two named open questions, in its own priority order, and both close: (a) **the paired standard error of a difference of Sharpe ratios** — the quantity the gate adjudicates and the one session 10 forbade itself to substitute the single-strategy error for — chased in the vocabulary that session named (Jobson–Korkie / Memmel; Ledoit–Wolf); and (b) **the deflated Sharpe ratio itself**, the last uncovered piece of the gate's own machinery, together with the rival multiple-testing correction the DSR authors call complementary. Three notes; full text read directly for Ledoit–Wolf, Bailey–López de Prado, the Bailey–Borwein–López de Prado–Zhu companion, Harvey–Liu and O'Connor, and in part for Harvey–Liu–Zhu. The session's shape is one *closed form* that reproduces a number the lab had only bootstrapped (and grades the lab's bootstrap as the right method with two free refinements), one *coverage obligation discharged* on the gate's statistic, and one *correction to a sentence the folder repeats* — "every trial raises the bar" is a family-wise-error-rate property, not a law. | Ledoit–Wolf 2008 (JEF; UZH-hosted published PDF read in full), with Jobson–Korkie 1981 (JF) and Memmel 2003 (Finance Letters) recorded **second-hand** from two independent restatements of their formula, and Opdyke 2007 recorded **unread** (`2026-08-24-testing-differences-of-sharpe-ratios.md`); Bailey–López de Prado 2014 (JPM; author-hosted PDF read in full) + Bailey–Borwein–López de Prado–Zhu 2016 (J. Computational Finance; author-hosted PDF read in full), with the Notices-of-the-AMS companion recorded **unread** (`2026-08-24-deflated-sharpe-ratio.md`); Harvey–Liu 2015 (JPM; Duke-hosted PDF read in full) + Harvey–Liu–Zhu 2016 (RFS; Duke-hosted PDF read in part) (`2026-08-24-multiple-testing-haircut.md`) |
| 2026-08-25 (session 12) | Session 11's open question (c), the last unpatched seam in the scoring apparatus: **a multiple-testing correction that knows why a trial was run** — chased in the vocabulary session 11 named (prior-weighted, hierarchical and empirical-Bayes multiple testing), and answered from all three directions. Three notes; full text read directly for all four primary texts. The session's shape is one *machinery* that closes the question in statistics and immediately constrains it (a discount is zero-sum), one *exchange rate* in a finance venue that prices the discount at about one t-unit and finds it never falls below the naive bar, and one *narrowing correction* to `learnings.md`'s ⚠ standing protocol concern that removes its weaker half and sharpens the rest. | Genovese–Roeder–Wasserman 2006 (Biometrika; CMU Technical Report 811, the working version, read in full) + Roeder–Wasserman 2009 (Statistical Science; arXiv reprint read in full) (`2026-08-25-prior-weighted-multiple-testing.md`); Harvey 2017 (JF, Presidential Address; Duke-hosted PDF read in full) (`2026-08-25-bayesianized-p-values-prior-odds.md`); Jensen–Kelly–Pedersen 2023 (JF; CBS Research Portal published CC-BY version read in full) (`2026-08-25-hierarchical-bayesian-factor-replication.md`) |
| 2026-08-26 (session 13) | Session 12's open question (b), taking the better of the two structurally-different targets it named: **the statistical properties of the universe itself** — survivorship and constituent selection, which `learnings.md` lists as a permanent caveat and which no note here had ever sourced. Three notes, five sources; full text read directly for four, one recorded second-hand from its abstract. The session's shape is one *re-aiming* of the lab's oldest caveat (the level effect is the forgiving half; the persistence inference is the severe half, and a cross-sectional momentum book is a persistence claim), one *magnitude* for this repo's literal data-construction recipe together with the sign of the index-membership channel, and one *distribution* that explains why that magnitude is large — plus the folder's fourth and first distributional account of what concentration costs. | Brown–Goetzmann–Ibbotson–Ross 1992 (RFS; `terpconnect.umd.edu` mirror read in full) + Stambaugh 2011 (Quarterly Journal of Finance; the 2002 working version read in full from a Berkeley Haas upload), with Brown–Goetzmann–Ross 1995 (JF) recorded **second-hand from its published abstract only** — `oa_status: closed`, no repository copy found (`2026-08-26-survivorship-conditioning-and-spurious-persistence.md`); Daniel–Sornette–Wöhrmann 2009 (JPM; arXiv:0810.1922 read in full) + Cai–Houge 2008 (FAJ; author-hosted accepted version at `biz.uiowa.edu` read in full) (`2026-08-26-look-ahead-benchmark-bias-index-constituents.md`); Bessembinder 2018 (JFE; accepted-manuscript PDF read in full), with Bessembinder–Chen–Choi–Wei 2023 (FAJ, global) recorded **unread** (`2026-08-26-skewness-and-concentration-of-stock-returns.md`) |
| 2026-08-27 (session 14) | Session 13's open question (b), and the last vocabulary the folder had never opened: **execution and implementation shortfall**. Taken with the stated prior that it would close rather than open — which held, but the closures are load-bearing rather than empty. Three notes, five sources; full text read directly for four, one recorded **unread**. The session's shape is one *verification* of a number the repo has never had outside evidence for (the 15 bps/side charge, graded against $1.7tn of live institutional fills and found conservative-to-fair, with the engine's decision-price convention matching the source's definition word for word), one *shape correction* that identifies the single asymmetry in the flat cost model pointing against this repo (impact is denominated in volatility; a momentum basket holds the high-volatility tail) together with the arithmetic showing it does not change a verdict, and one *adjudication* of a published tier-1 disagreement about whether the repo's own champion family survives costs — which resolves in the repo's favour on level while leaving two structural results untouched, one of which (most of the momentum spread lives on the short leg) is the folder's most specific long-only discount to date. | Frazzini–Israel–Moskowitz 2018 (AQR/SSRN working paper; author-hosted PDF read in full), with Perold 1988 (JPM) recorded **unread** — paywalled, no repository or mirror copy found, its definition used only as restated in the source read (`2026-08-27-live-execution-costs-implementation-shortfall.md`); Almgren–Thum–Hauptmann–Li 2005 (Risk; authors' dated version read in full from a university course-reading directory) (`2026-08-27-market-impact-functional-form-and-trade-rate.md`); Lesmond–Schill–Zhou 2004 (JFE; a university PhD-course mirror served the typeset article) + Korajczyk–Sadka 2004 (JF; Kellogg faculty page) (`2026-08-27-momentum-net-of-costs-debate.md`) |
| 2026-08-28 (session 15) | Session 14's open question (a), taking the one of its three unopened directions it called "the best of the three and the only one that could change a construction choice": **international / global evidence on momentum construction**, chased because this repo's universe is global while almost every source in this folder is US-only. Four sources, four notes; full text read directly for all four, one of them in a working-paper rather than published version (flagged in-note). The session's shape is one **opened build** — the first grouping ever to pass candidate #5's neutralisation screen — one second build of a kind the folder has never supplied (a *signal*, price-only), two free discount/interpretation rules, one anti-candidate, and one unresolved disagreement between two tier-1 sources that is recorded rather than adjudicated. | Rouwenhorst 1998 (JF; Yale ICF working-paper depot served the February 1997 revision in full) (`2026-08-28-international-momentum-country-neutral.md`); Fama–French 2012 (JFE; the typeset article with volume and page headers from an author-adjacent faculty site, `johnhcochrane.com`) (`2026-08-28-local-versus-global-factor-construction.md`); Asness–Moskowitz–Pedersen 2013 (JF; the typeset article from an author's NYU Stern page) (`2026-08-28-value-momentum-everywhere-global-comovement.md`); Chui–Titman–Wei 2010 (JF; the **November 2004 working-paper version** read in full from a National Taiwan University conference-proceedings mirror, the published article not obtained — two of its findings taken from the published abstract and marked as such) (`2026-08-28-individualism-cross-country-momentum.md`) |
| 2026-08-29 (session 16) | **The first session under the rewritten `program.md`, and the first in this folder's history not aimed at a seam in the price-trend programme.** Six of the eight families had zero notes; the session took four of them, chosen so that two match the families the strategy agent has just scouted (`statistical-learning`, `liquidity-volume` — so the literature lands where trials already exist) and two are cold opens made reachable by the same-day constraint change (`range-variance`, `seasonality-calendar` — both need the OHLCV panel or were never cheap enough to justify). Four notes, eight sources; full text read directly for six, one recorded **second-hand** from a source that reproduces its derivations, one from its **published abstract only**. The session's shape is one *methodological transfer* that explains a result the lab had already measured but not understood (a linear learner loads on trend because that is where the marginal signal is), one *commissioned replication* that survives the replication and loses the horserace — the strongest "your family lead may be measuring the wrong thing" finding this folder has produced — one *free measurement improvement* that is analytical rather than empirical and that names the only estimator safe to divide by, and one *cost warning delivered by the source's own authors* against the family they discovered, together with the overlay they suggest instead. | Gu–Kelly–Xiu 2020 (RFS; NBER WP 25398, Sept 2019 revision, read in full) (`2026-08-29-machine-learning-cross-section-comparative.md`); Amihud 2002 (JFM; typeset article from a UPenn course reading directory) + Harris–Amato 2019 (CFR) + Amihud 2019 (CFR), the latter two read in full from the journal's own editor-hosted mirror `cfr.ivo-welch.info/published/papers/` (`2026-08-29-amihud-illiquidity-measure-and-replication.md`); Alizadeh–Brandt–Diebold 2002 (JF; author's UPenn page, typeset article read in full) + Molnár 2012 (IRFA; read in full as Chapter 2 of the author's 2020 habilitation thesis, which reproduces the article with its journal header), with Parkinson 1980, Garman–Klass 1980, Rogers–Satchell 1991 and Meilijson 2009 recorded **second-hand** — their formulas and efficiencies taken as restated with derivations in Molnár and cross-checked against ABD's independent restatement (`2026-08-29-range-based-volatility-estimators.md`); Heston–Sadka 2008 (JFE; the October 2006 working version read in full from NYU Stern's seminar archive), with Heston–Sadka 2010 (JFQA, the international companion) recorded from its **published abstract only** — `oa_status` closed, no repository copy found (`2026-08-29-same-calendar-month-seasonality.md`) |
| 2026-08-30 (session 17) | **The last two cold opens, taken together, which retires the README's zero-coverage rule.** `lead-lag-spillover` first, as `SUMMARY.md` instructed — two sources, one per horizon end (monthly group→market; daily/weekly volume-sorted) — then `statistical-arbitrage`, scoped to the single question the previous session posed for it: *what survives a long-only constraint*. Three notes, five sources; full text read directly for three primaries plus one authors' replication package, one recorded from its **published abstract only**, one further paper recorded **unread** from its abstract as a flagged follow-up. The session's shape is one *mechanism plus a three-part free screen* whose most useful clause is that a lead-lag construction without an own-lag control is momentum in costume, one *new closes-only signal* (`DELAY`) that arrives together with the finding that this repo cannot compute the source's actual sorting variable, one *tension recorded rather than resolved* (the lab's declined residual-reversion screen tested only the factor-count region the source also found worst, but three discounts stop that being a refutation), and one *scoping rule* that removes the long-only version of `statistical-arbitrage`'s decorrelation claim while leaving its selection claim intact. | Hong–Torous–Valkanov 2007 (JFE; the authors' 5 Dec 2005 draft read in full from `columbia.edu/~hh2679`) + the authors' October 2014 replication Note (read in full from `rady.ucsd.edu`), with Tse 2015 (Journal of Empirical Finance, the reexamination) recorded from its **published abstract only** — closed access, no repository copy — and Hou 2007 (RFS) recorded **unread** from its abstract as a flagged follow-up (`2026-08-30-industry-lead-lag-gradual-diffusion.md`); Chordia–Swaminathan 2000 (JF; typeset article read in full from a UPenn course-reading mirror) (`2026-08-30-volume-and-cross-autocorrelation-lead-lag.md`); Avellaneda–Lee 2010 (Quantitative Finance; the authors' June 2009 working version read in full from the first author's Courant page) (`2026-08-30-pca-residual-statistical-arbitrage-long-only.md`) |

| 2026-08-31 (session 18) | **Aimed entirely by `SUMMARY.md`'s own open questions rather than by breadth, and it takes all three of its top-priority items.** Two of them are papers this folder has flagged unread across multiple sessions (Lou-Shu, Hou); the third is the last partial family gap (`portfolio-learning`'s "stacking half"), which closes it and gives every `program.md` family a section of its own. Three notes, four sources; full text read directly for two primaries, two recorded **from their published abstracts only** (both closed access with no repository copy and every mirror bot-challenged). The session's shape is unusual and worth naming: **two of the three notes end by narrowing a conclusion `experiments/learnings.md` recorded as final, and in both cases the narrowing is one free measurement wide** - the `liquidity-volume` null was measured on the mean of volume where the priced functional is the mean of the *reciprocal*, and the `portfolio-learning` closure was measured on return-series correlation where the governing quantity is cross-sectional *signal* correlation. Neither lab result is wrong; both are one step narrower than stated, and candidates #58 and #60 are the zero-cost checks that settle them. The third note is a *discount* rather than a build: the strongest source on lead-lag says the grouping variable carries the hypothesis, and the grouping it endorses needs a taxonomy this repo probably does not have. | Lou-Shu 2017 (RFS; the authors' August 2016 working version read in full from an ICMA-hosted mirror, `icmagroup.org/assets/documents/.../Bond-Market-Liquidity-Library/`) (`2026-08-31-amihud-volume-component-decomposition.md`); Hou 2007 (RFS) recorded **from its published abstract only** - `oa_status: closed`, no repository fulltext, SSRN bot-challenged on both posted abstract pages, CORE and CiteSeerX resolved nothing; abstract read verbatim from the RePEc/IDEAS record (`2026-08-31-intra-industry-lead-lag-grouping.md`); Fitzgibbons-Friedman-Pomorski-Serban 2017 (Journal of Investing; the typeset article read in full from AQR's own hosting) paired with its peer-reviewed rebuttal Leippold-Ruegg 2018 (European Financial Management), the latter recorded **from its published abstract only** - SSRN, Taylor & Francis, the EFMA conference mirror and the Zurich Open Repository each refused an automated client (`2026-08-31-signal-blending-vs-portfolio-blending.md`) |
| 2026-09-01 (session 19) | **The session's aim was set by the lab, not by this folder: both of the diagnostics `SUMMARY.md` made its top priority (#58, #60) were run overnight, and the ETF-versus-constituent gap this log has flagged for two sessions was screened dead by the lab itself — so the standing question list was spent on arrival and the focus moved to what the lab's own results opened.** Three notes, four sources; full text read directly for three primaries, one recorded from its **published abstract only**. The shape is *one mechanism aimed at the only family with zero trials, one discount aimed at the lab's best new result, and one source that explains a pattern the lab has hit repeatedly without a reason.* `range-variance` gets its first **asymmetric** mechanism (upper tail rather than width) together with a free two-number test that decides it either way — and the reading that the lab's own range-lottery screen dismissed a significant, correctly-signed result *using the confound the test exists to separate*. `portfolio-learning` and the inference layer get the algebra behind the lab's mean-versus-max finding — a proof that linear composites are *exactly* equivalent to portfolios of their legs, which is why the mean is bounded and the max is not — plus a second bias, distinct from every correction this folder holds, that lives **inside a single trial** and that the trial count cannot see. And `statistical-learning` gets the size-cut result that predicts, from outside, that a ~145-name large-cap universe is where most characteristics stop working: it names the three daily-data survivors, one of which (`SUV`) is the single volume functional the lab has not screened. | Bali–Cakici–Whitelaw 2011 (JFE; the typeset article read in full from the corresponding author's NYU Stern page), with Cheon–Lee 2018 (Management Science) recorded **from its published abstract only** — closed access (`2026-09-01-max-lottery-extreme-positive-returns.md`); Novy-Marx 2016 (NBER WP 21329 / author's March 2016 draft, R&R at JFE per his posted CV; read in full from `mysimon.rochester.edu`) (`2026-09-01-multi-signal-overfitting-critical-t.md`); Freyberger–Neuhierl–Weber 2020 (RFS; the NBER working-paper draft read in full, including the appendix selection table and variable definitions) (`2026-09-01-nonparametric-characteristic-selection-large-stocks.md`) |
| 2026-09-02 (session 20) | **Aimed by `SUMMARY.md`'s own ranked open questions, both of which survived contact with the lab this time — and the session's shape is *two corrections to screens the lab is still carrying*, not two new mechanisms.** The 2026-09-01 nightly ran #61's `MAX`/`MIN` sign test and closed `range-variance` a fourth time, so the standing list's first item was spent on arrival and its second (`seasonality-calendar`, the **calendar** half) became the focus. That half had *also* been closed overnight, structurally — which turned the intended survey into an audit of the two screens the family now rests on. Both audits found the screen narrower than the conclusion drawn from it, and both end in a **free measurement that decides the family either way** (#66, #67). The third note takes the standing size-distribution tension, which asked explicitly for a source measuring predictability *by size group directly*. Three notes, five sources; full text read directly for three primaries (two via author/NBER working-paper versions of the published articles, one via a university mirror of the authors' working draft), two recorded **from their published abstracts only** (both closed access). Keloharju–Linnainmaa–Nyberg 2016 (JF) + 2021 (JFE companion) (`2026-09-02-return-seasonalities-common-factors.md`); Ogden 1990 (JF) + Etula–Rinne–Suominen–Vaittinen 2020 (RFS) (`2026-09-02-turn-of-month-payment-cycle.md`); Fama–French 2008 (JF) (`2026-09-02-anomalies-by-size-group.md`) |
| 2026-09-03 (session 21) | **The first session in three whose aim was not set by the lab overnight — every item on the standing list had been answered, all of them negatively, so the focus was chosen by asking which *live* families the lab could still act in.** The 2026-09-02 nightly ran #66, #67 and #69 and closed all three (the seasonal leg's identification repaired but the demeaning shown not to be what supplies it; the calendar half closed a second time on cost; the ETF-only seasonal dead on its own precondition — 5 of 42 ETFs reach a 20-year lookback), and declined `range-variance` a fourth time on the tail statistic its defence rested on. That leaves `statistical-learning` and `statistical-arbitrage` as the two families that are neither closed by the lab nor over-covered here, and the session took two notes in the first and one in the second. The shape is *one correction, one discount, one mechanism.* The correction: "how few predictors matter" has been asked in the wrong space — characteristic-space sparsity fails, PC-space sparsity works, and the estimator that exploits it shrinks unequally across eigenvalue directions, which is **not** what the lab's uniform ridge-on-features tested, so the design rule drawn from that trial targets a different failure (#70). The discount: the *incremental value of nonlinearity* was measured and found to live in microcaps and distressed names, which this universe does not contain — an anti-candidate for learned model classes that stacks with #68 (#73). The mechanism: the distance method, a relative-value construction that estimates nothing, whose execution lag, overlapping monthly tranches and total-return inputs are already this repo's conventions, and which comes with its own placebo control (#72). Three notes, five sources; **full text read directly for all three primaries**, two supporting sources recorded **from their abstracts only** (both closed access, SSRN 403 as documented). | Kozak–Nagel–Santosh 2020 (JFE; the authors' accepted manuscript read in full from Nagel's university page) (`2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`); Avramov–Cheng–Metzker 2023 (Management Science; the typeset INFORMS article read in full from the second author's own site) (`2026-09-03-machine-learning-economic-restrictions.md`); Gatev–Goetzmann–Rouwenhorst 2006 (RFS; the NBER WP 7032 version read in full) with Do–Faff 2010 (FAJ) and 2012 (Journal of Financial Research) recorded **from their published abstracts only** (`2026-09-03-pairs-trading-distance-method.md`) |

### Open questions for future sessions

- **[2026-09-03] The standing list was spent on arrival for the third session running — but this
  time every item came back *negative*, and that changes what this folder is for.** The 2026-09-02
  nightly ran #66 (the fixed-effects contrast: it corrected the lab, and the seasonal leg's
  demeaning turns out not to be what supplies its identification), #67 (the T−8..T−4 window: the
  sign test *passed* and the idea died anyway on cost — 12 round trips is still 12 round trips) and
  #69 (dead on its own precondition: only 5 of 42 ETFs reach a 20-year lookback), and declined
  `range-variance` a fourth time on the tail statistic. Four of the folder's last five proposals
  were answered for free and none opened anything. **The useful reading is not that the proposals
  were bad — three of the four were decided by the precondition or control the proposal itself
  specified, which is the format working as intended — but that the lab has now closed every family
  whose object is a cross-sectional characteristic *level*, and the folder should stop proposing
  them.** What is left live is `statistical-learning` (one screen run, and it tested a different
  estimator than the literature's — see #70), `statistical-arbitrage` (one screen run, and it
  tested the unconditional half of a conditional mechanism — see #72), and `portfolio-learning`
  (the leg-count threshold, which is the lab's own next measurement and needs nothing from here).
- **[2026-09-03] What should aim the next session, in order.**
  - **Check whether #70 and #71 were run before choosing anything else** — the same instruction
    the last three entries gave, for the same reason: both are free, both decide a live family, and
    both have been written so that either answer is a finding. #70 in particular is the first
    proposal here that says the lab's *own screen measured a different object than the one it
    concluded about*, and if the eigenvalue spectrum comes back unrelated to the PC means then
    `statistical-learning` closes on this universe with a reason rather than on a null.
  - **If #72's matching-pool precondition comes back thin, record `statistical-arbitrage` as
    unreachable on this universe rather than unexplored** — the same conclusion `range-variance`
    earned after five sessions, and worth reaching in one instead of five. ~145 names across 15
    regions is a small pool for exhaustive pairwise matching, and the honest failure mode is
    structural, not empirical.
  - **The inference and multiple-testing embargo stands** and was honoured again. So does the
    2026-09-02 embargo on further size/microcap sources: #73 is the fourth reading on that question
    and it now agrees with the other three, so the vein is spent.
  - **A gap this session opened rather than closed, and it is the honest next survey if the free
    screens above come back null:** every learned-model source in this folder studies **individual
    stocks with dozens to thousands of features**. The lab's actual learned object is a combiner over
    **a handful of its own legs** — a ten-input problem, not a high-dimensional one — and none of
    the three notes on `statistical-learning` is really about that regime. The relevant literature
    is small-*n* forecast combination and shrinkage toward equal weights, which this folder holds
    (Timmermann, Hansen, the bagging and model-averaging notes) but has never connected to the
    learned-combiner question. **Re-reading the folder's own material against that question may be
    worth more than a new source**, and would cost no external search.
- **[2026-09-03] A tension to hold open rather than resolve.** Gu–Kelly–Xiu report machine-learning
  predictability as *stronger* among large stocks; Avramov–Cheng–Metzker report that imposing
  large-stock and non-distress restrictions removes most of the deep learners' *advantage over a
  linear model*. Both can be true — forecast **accuracy** where the data is clean, versus where the
  extra **nonlinearity** pays — and #73 is written to the second reading only. If the lab ever runs
  a nonlinear candidate here, the discriminating question is not "did it beat the sort" but "did it
  beat the *linear* model built from the same features", which is a comparison neither the lab nor
  this folder has ever specified.
- **[2026-09-03] Access and index behaviour, for the recipe.** Three primaries read in full, all
  from **author- or co-author-hosted PDFs**, including a channel not previously used here: an
  **author's own site serving the typeset INFORMS article** complete with volume/issue/page headers
  and the publisher's download stamp — worth trying first for Management Science and Operations
  Research papers, whose publisher endpoint is closed. A university **`voices`/`wpmucdn` faculty
  blog host** served the accepted manuscript of a JFE article (and its Internet Appendix at the same
  path). **NBER working-paper PDFs** worked again, and for a 2006 RFS article the NBER version
  carried the complete methodology, the risk decomposition and the placebo bootstrap. Index
  behaviour, and it is a *fifth* instance of the standing "disbelieve a lone count" rule with a new
  tell: **Semantic Scholar's DOI endpoint returns "not found" for `10.1016/j.jfineco.2019.06.008`**
  — a 700-plus-citation JFE paper — extending the pattern previously recorded for Journal of Finance
  DOIs to JFE, so **for a top-three finance journal DOI, query Crossref and OpenAlex first and do not
  treat a Semantic Scholar miss as evidence the paper is unindexed.** Also inverted from the usual
  direction: for `10.1287/mnsc.2022.4449`, **Crossref reports 201 and Semantic Scholar 119** — the
  low count is the *Semantic Scholar* one this time, so the rule is symmetric and is about
  disagreement, not about which index. Limits hit as documented: **SSRN returned 403** on both
  Do–Faff papers, and the Wiley and Taylor & Francis landing pages serve no full text, so both are
  recorded from **abstracts obtained verbatim from a university research portal** and are flagged
  second-hand in the note and in the family section.

- **[2026-09-02] Both of this folder's standing priorities were closed by the lab before the
  session ran — for the second session in a row — and the useful response was to audit the
  closures rather than to survey somewhere else.** #61's `MAX`/`MIN` sign test was run and
  `range-variance` closed a fourth time (correctly, on the source's own identifying criterion); the
  **calendar** half of `seasonality-calendar`, this list's number-two item, was closed the same
  night on a structural argument. Neither closure is wrong. But **both rest on a screen narrower
  than the conclusion drawn from it**, and in both cases one free number decides it: the calendar
  closure tested the T−1..T+3 window and pooled the payment cycle's *negative* window (T−8..T−4)
  into an undifferentiated complement (#67), and the family's cross-sectional half is still
  carrying a **pre-registered screen its own successor literature predicts will fail** (#66). This
  is now a recognisable pattern worth naming: *the lab's free screens are fast enough that this
  folder's value has shifted from finding new mechanisms to checking that the lab's negative
  results measured what they claimed.* Three of the last six notes have ended that way.
- **[2026-09-02] What should aim the next session, in order.**
  - **Check whether #66 and #67 were run before choosing anything else**, exactly as the
    2026-08-31 and 2026-09-01 entries below instructed for their own diagnostics — the answers
    redirect the only family with a live, uncontested lead. If #67 comes back positive, record the
    `calendar` closure as **final** and stop proposing calendar overlays; if #66's fixed-effects
    contrast comes back null, the cross-sectional seasonal is a persistent mean-return sort rather
    than a seasonal and the whole family should be re-described, which matters because that leg is
    currently the lab's only one with reliable cross-sectional content.
  - **`seasonality-calendar` is still the thinnest live family and now has the folder's most
    specific untried candidate (#69, the ETF/country-index seasonal).** It is also the only
    proposal on the table that answers *two* open lab questions at once — the survivorship
    objection to single-name seasonality, and the "fifth maximally orthogonal leg" the
    `portfolio-learning` leg-count contrast needs — with the orthogonality **measured in the
    source** rather than assumed. Its precondition (count available annual lags per instrument) is
    free and should be run first; if the 20-year lookback does not fit this store, say so and
    record it, because a shortened-window version is a different object from the published one.
  - **Do not take another size/microcap source.** With #68 the folder has four readings on where
    this universe sits and they now reconcile (accuracy versus count; momentum pervasive among big
    stocks, characteristic levels not). The marginal note there is spent. The same standing
    embargo from 2026-09-01 on **multiple-testing and inference literature** remains in force and
    was honoured this session.
  - **`Goyenko–Holden–Trzcinka 2009 (JFE)` should now be dropped from this list entirely** rather
    than carried a fourth time. It has been deferred since 2026-08-29, `liquidity-volume` has since
    closed twice on the lab's own measurements, and #68 supplies the general reason a liquidity
    premium located in the illiquid tail is unreachable on an all-big-stock universe. Nothing a
    proxy horserace could say changes that.
  - **The one genuinely uncovered thing left, and it is a method rather than a family:** every
    remaining live question in this folder is now of the form *"the lab measured X and concluded
    Y ⊃ X"*. There is a real literature on pre-registration and specification-curve/multiverse
    reporting for exactly that failure. It was **not** taken this session because it sits under the
    inference-literature embargo, and it should only be taken if a session finds itself with no
    mechanism-note candidate in a thin family — which was not the case tonight and is unlikely to
    be next time either.
- **[2026-09-02] A tension carried forward, not resolved.** Keloharju–Linnainmaa–Nyberg's 2016 JF
  paper argues return seasonalities are **common-factor-borne and unhedgeable** (at least
  two-thirds from shared factors; hedging the exposure removes the effect), while the same authors'
  2021 JFE companion reports **seasonal reversals summing to roughly zero over the calendar year**
  and reads them as temporary mispricing. Both are Tier 1 and they are the same research team five
  years apart. The lab does not have to adjudicate it, but the two readings imply different
  answers to a question it *will* face: whether a seasonally-tilted long-only book that trades the
  same names around the year nets anything after a year of turnover. That is checkable for free on
  train and is the first thing to measure if #69 is built.

- **[2026-09-01] The three standing top-priority items were all resolved by the lab before this
  session ran, and that is the pattern to keep.** #58's diagnostic came back **confirming** the
  closure (`spearman(log A_C, −log mean dollar volume) = +0.993`; no Jensen gap on this universe),
  #60's came back **reopening** `portfolio-learning` but for a different reason than #60 gave, and
  ETF-versus-constituent lead-lag — flagged here as the top unread gap for two sessions running —
  was screened and is dead (the ETF's residual of the member-median control is a null at every
  horizon pair). **Every one of those was decided by a free measurement, none of them cost a
  trial, and in two of three cases the answer was not the one this folder predicted.** Keep
  writing candidates in that form. This session's #61, #62 and #63 are all of it.
- **[2026-09-01] What should aim the next session, in order.**
  - **Check whether #61's `MAX`/`MIN` sign test was run before choosing anything else.**
    `range-variance` is the only `program.md` family with zero recorded trials and `learnings.md`
    has escalated it to the human as unproposable on current evidence; #61 either gives it a
    candidate or closes it a fourth time on the source's own identifying test. If it closes, the
    honest conclusion is that this family is unreachable *on this universe* rather than
    unreachable, and that is a finding worth writing up rather than another survey.
  - **`seasonality-calendar` is the thinnest genuinely-live family and this folder has one note
    on it.** The gap is not the cross-sectional seasonal (covered) but the **calendar** half —
    turn-of-the-month, holiday and month-boundary effects, and specifically the standing skeptical
    literature on whether any of them survive costs and multiple testing. It matters more than it
    did: `learnings.md`'s 2026-08-29 entry found the lib's `seasonal_same_month_return` traded one
    month late, and the corrected alignment turns a null into +15.7%/yr (t = +5.16) on train. That
    is an unexploited live result inside the one family with a single note. Take it before any
    further inference/methodology material — this folder now holds a great deal of the latter.
  - **`Goyenko–Holden–Trzcinka 2009 (JFE)`** remains unread from the 2026-08-29 entry and should
    now be **dropped in priority, not carried forward again.** `liquidity-volume` has closed
    twice on the lab's own measurements and #62 is the last free check standing between it and a
    third; a horserace of low-frequency liquidity proxies against intraday benchmarks cannot
    change a null measured on this universe's own instruments.
  - **Do not spend a slot on more multiple-testing or inference literature.** With this session's
    note the folder holds six sources on the topic (deflated Sharpe, the haircut, testing Sharpe
    differences, Bayesianized p-values, the hierarchical prior, and now the multi-signal
    overfitting bias) against a lab that has one live candidate class. The marginal note there is
    now worth less than the marginal *mechanism* note in a thin family.
- **[2026-09-01] A tension this session created and did not resolve, recorded rather than
  adjudicated.** Freyberger et al. find **fewer** characteristics surviving among large firms;
  Gu–Kelly–Xiu (2026-08-29 note) find machine-learning predictability **stronger** among large
  stocks and say so explicitly to rebut the microcap-artifact reading. These are not formally
  contradictory — one counts independent predictors, the other measures forecast accuracy — but
  they are the second and third readings this folder has taken on the same question and they
  point a ~145-name large-cap universe in opposite directions. The 2026-08-29 entry below flagged
  the first version of this (Gu–Kelly–Xiu against the liquidity premium's illiquid-tail location);
  it is now a three-source disagreement about **where in the size distribution this universe
  sits**, which is the single most consequential unknown about the instrument set. If one source
  is taken next session, it should be one that measures predictability *by size decile* directly.

- **[2026-08-31] Two of this session's three notes end in a *free diagnostic the lab must run
  before the next session's literature is worth anything*, and that is the shape to keep.** Both
  #58 and #60 identify a case where the lab measured a real quantity and drew a conclusion one
  step wider than the quantity supports — `ILLIQ`'s volume content tested through the mean rather
  than the reciprocal; the blend bound measured on return-series correlation rather than
  cross-sectional signal correlation. Neither is an error, and in both cases the wider conclusion
  may well be right; but in both cases a zero-cost measurement settles it, and until it is run the
  literature cannot tell the lab anything more. **The next session should check
  `experiments/learnings.md` for whether #58's and #60's diagnostics were run before choosing a
  focus**, because the answers redirect two families. If both come back confirming the closures,
  `liquidity-volume` and `portfolio-learning` are genuinely finished and future effort belongs
  elsewhere; if either reopens, the follow-up literature is obvious and specific.
- **[2026-08-31] What is left unread, in priority order.**
  - **`ETF`-versus-constituent lead-lag remains the one `program.md` sub-mechanism with no
    coverage at all**, now flagged for the second session running. Hou did not touch it (he is
    group→group within industries) and neither did Hong–Torous–Valkanov or
    Chordia–Swaminathan. This repo is unusually well set up for it — 42 ETFs alongside
    constituent-adjacent single names — and it is the only remaining *named* gap in the
    `program.md` list. It should be taken next unless a diagnostic above reopens a family.
  - **Hou 2007 deserves a second attempt at full text.** This session's note is abstract-only:
    six sentences carrying four claims, with no lookback, no formation cadence, no industry
    granularity and no robustness evidence. The claims are load-bearing enough (they discount
    every region-grouped lead-lag result the lab has) that the construction detail is worth one
    more try through a route this session did not attempt — an interlibrary or course-packet
    mirror, or the citing literature's restatements (the paper has 617 citations; a well-cited
    successor restating its specification second-hand would be enough).
  - **Goyenko–Holden–Trzcinka 2009 (JFE)**, the low-frequency liquidity-proxy horserace, still
    unread from the 2026-08-29 entry — and now *more* interesting rather than less, because
    Lou–Shu use exactly its class of high-frequency benchmarks to show that `ILLIQ`'s genuine
    liquidity content and its return premium sit in different places. It is the source that
    would say how much of the "measures liquidity well" result survives that split.
  - **Hierarchical risk parity is now closed twice and should not be taken.** The lab's
    2026-08-30 arithmetic and this session's mix-bound mechanism agree, from different
    directions, that a risk allocator over finished long-only books cannot escape the bound.
    Recording this so a future session does not spend the last `portfolio-learning` slot on it.
- **[2026-08-30] The README's zero-coverage rule is spent; here is what should aim the next
  session instead.** Every `program.md` family now has at least one dedicated note. In rough
  priority order, and none of these is a family survey:
  - **`portfolio-learning`'s specific gap (HRP, stacking), but at a *lower* priority than the
    2026-08-29 entry below gave it.** That entry said to take it "before either of the two cold
    families if the strategy agent starts building blends". The blend route has since been
    measured and it is much narrower than it looked: `learnings.md`'s solved break-even table plus
    its resolution floor put the required *leg* Sharpe at 1.34–1.42 against a champion at 1.120,
    and five family leads from five mechanisms correlate 0.75–0.85 **with each other**, so an
    allocator over them is allocating over one thing. A clustering allocator cannot manufacture
    decorrelation that the long-only constraint forbids — see candidate #54 for the mechanism.
    Worth one note for the *stacking / meta-labelling* half (a learned combiner is a different
    object from a risk allocator, and `learnings.md`'s own design rule says a learned candidate
    earns a trial only when asked for something a sort cannot express); the HRP half should be
    taken with the explicit prior that it will close rather than open.
  - **The two follow-ups this session flagged but did not read**, both cheap and both aimed at
    open threads rather than at breadth: **Hou 2007 (RFS)**, "Industry Information Diffusion and
    the Lead-lag Effect in Stock Returns" — its abstract claims the lead-lag effect is
    predominantly *intra*-industry and that little cross-industry predictability survives once
    that channel is accounted for, which if right says the **grouping variable matters more than
    the lead-lag machinery**, and this repo's grouping choice (region vs ETF sleeve vs sector) is
    exactly the live design decision. Closed access; SSRN serves a bot challenge, so it needs a
    course or repository mirror. And **Lou–Shu 2017 (RFS)** plus **Goyenko–Holden–Trzcinka 2009
    (JFE)**, still unread from the 2026-08-29 entry below.
  - **The single most useful unread thing for the family this session opened**: nothing in either
    lead-lag source speaks to **ETF-versus-constituent** lead-lag, which is the one sub-mechanism
    `program.md` names and this repo is unusually well set up for (42 ETFs alongside their
    constituent-adjacent single names). Both notes here are group→group or group→market. That is a
    real gap inside a now-covered family.
- ~~**[2026-08-29] Two families still have zero coverage, and the README's rule is live for
  both**~~ — **both taken 2026-08-30 (session 17)**, and each closed differently from how this
  entry expected. The forecast that `lead-lag-spillover` would be "the better-suited of the two"
  held on universe fit and failed on horizon: the tension this entry told the session to check —
  that the engine's one-day lag sits exactly where lead-lag results live — resolves as an
  *asymmetry* rather than a blanket problem. The one-day lag eats most of a **daily** effect and
  costs a **monthly** one almost nothing, so the family's two ends have opposite implementability
  profiles and a candidate has to live in the middle; and the sharper obstacle turned out to be a
  different one this entry did not anticipate, namely that 15 non-overlapping trading sessions
  under unhedged USD conversion manufacture daily cross-correlation mechanically (candidate #57c).
  `statistical-arbitrage`, scoped as instructed to the long-only question, answers it negatively
  at the level of the *claim* (candidate #54) while leaving one buildable idea and one free
  transformation standing (#55, #56).
- **[2026-08-29] `portfolio-learning` is covered only by analogy, and the gap is specific.** The
  folder's ensemble/forecast-combination material (family 7 above, plus the bagging and
  model-averaging notes) is what `program.md` now calls `portfolio-learning`, so the family is not
  cold. But none of it covers the two named members: **hierarchical risk parity / clustering-based
  allocation**, and **stacking or meta-labelling over family leads**. `program.md` says this is
  "where scouted leads become a challenger", and the lab now has two family leads and a measured
  exchange rate for blending them (`learnings.md`'s required-gain table). A note on HRP and on
  stacking would land directly on a decision the lab is about to face, and it should be taken
  before either of the two cold families if the strategy agent starts building blends.
  **Priority revised down 2026-08-30** — see the first open question above: the blend route's
  required leg Sharpe has since been solved (1.34–1.42 against a 1.120 champion) and the five
  recorded leads correlate 0.75–0.85 with each other, so the HRP half should be expected to close.
  The stacking half is still worth a note.
- **[2026-08-29] One open question inside a family this session covered, and it is the most
  actionable thing here.** Harris–Amato find that `ILLIQ`'s day-by-day pairing of |return| with
  volume contributes essentially nothing over the ratio of the two means, and that log average
  dollar volume is among the *best* simple proxies. They cite **Lou–Shu 2017 (RFS), "Price Impact or
  Trading Volume: Why Is the Amihud (2002) Measure Priced?"** as reaching a similar conclusion by a
  different route. That paper is **unread** and is the natural follow-up: it is the source that
  decomposes the measure directly, and its answer determines whether the lab's `liquidity-volume`
  lead is a price-impact story or a trading-activity story — which is the difference between two
  quite different second trials. Also unread and relevant to the same question:
  Goyenko–Holden–Trzcinka 2009 (JFE), "Do liquidity measures measure liquidity?", the field's
  horserace of low-frequency liquidity proxies against intraday benchmarks.
- **[2026-08-29] A tension this session did *not* resolve, recorded rather than adjudicated.**
  Gu–Kelly–Xiu report that machine-learning predictability is **stronger among large stocks than
  small**, and say so explicitly to rebut the reading that it is a microcap-illiquidity artifact.
  Amihud/Harris–Amato's liquidity premium runs the other way — it lives in the illiquid tail, and
  McLean–Pontiff independently put surviving post-publication predictability in
  high-idiosyncratic-risk, low-liquidity names. These are not formally contradictory (one is about
  where a *forecast* is accurate, the others about where a *premium* is paid) but they point a
  ~145-name universe of large liquid global instruments in opposite directions, and the folder's
  standing pessimism about this universe's instrument set rests on the second reading. Worth
  chasing once, in either family.

- ~~Families 2, 5 and 7 have no coverage~~ — **all covered; family 5 done 2026-08-18 (session
  5), and the answer closes it.** The gap named in `learnings.md` was a genuinely different
  volatility construction, "sector-neutralized rather than raw trailing". That construction
  exists in the literature (industry-neutral BAB) and is reported to beat the ungrouped version
  in every US industry — but it is unavailable here because BAB's low-beta leg is *levered to
  beta 1*, and the industry-neutral variant is explicitly the most leverage-hungry of the set.
  The skeptical literature independently puts the premium in small growth (reversing in large
  value), in the bottom 1% of market capitalisation, and — post-cost — in profitability and
  investment exposures requiring fundamentals. Family 5 is now closed on mechanism, not merely
  on the lab's two empirical refutations.
- ~~Family 3 needs a dedicated risk-parity source~~ — **fully done 2026-08-18 (session 5).** The
  *vol-targeting* half was covered in session 4 (negative on leverage cap, non-generality across
  103 strategies, real-time failure). The **risk-parity half is now covered too**, and the
  requirement stated here — a source speaking to weighting *within comparable-diversification
  sleeves* — turned out to be the wrong question, which is the session's most useful correction.
  Maillard–Roncalli–Teiletche show that for **two** components ERC *is* inverse-volatility
  independent of correlation, so the lab's blend was correct risk parity with no better-specified
  version to try; that in general `x_i ∝ 1/β_i`, so a *more* correct implementation tilts further
  toward the diversified low-return leg; and that ERC is maximum-Sharpe **only under constant
  correlation and equal component Sharpe ratios**. The binding condition is therefore
  **comparable Sharpe ratios, not comparable diversification**, and it is checkable before any
  trial. Both halves of family 3 are negative, for independent reasons.
- **No `program.md` family is now uncovered** (as of 2026-08-18). Families 1–7 all have at
  least one dedicated source, and the honest tally across all five sessions is that the
  literature has **closed six directions and opened one** (candidate #8, lookback-length
  vintage averaging). That asymmetry is the folder's main product, and it is worth more than it
  looks given that every trial permanently raises the deflated-Sharpe bar. The implication for
  future sessions is a change of target: **the marginal value of another strategy-family survey
  is now low**, and the higher-value directions are (a) the cross-cutting methodological
  literature that grades the lab's *own* mechanisms, which has been the most productive vein so
  far, and (b) the specific open threads listed below rather than any family label.
- ~~Nothing yet on portfolio construction as its own literature~~ — **first pass done**
  (2026-08-17 session 2): cost mitigation / banding, rebalance timing luck / tranching, and
  naive-vs-optimised weighting. The axis is now covered at the level of *grading the lab's
  existing mechanisms*, and the honest summary is that the literature largely **confirms and
  closes** rather than supplies: banding is endorsed, cost mitigation is exhausted by
  enumeration, expensive weighting schemes are ruled out on estimation-error grounds. What
  remains genuinely open, and unaddressed by anything read so far, is the **economic mechanism
  behind the lab's temporal-breadth result** — that holding several formation vintages raises
  return rather than merely lowering cost or dispersion. Neither the momentum literature
  (estimator framing) nor the timing-luck literature (dispersion framing) makes that claim. A
  future session could look for it under different vocabulary: signal-averaging / ensembling
  over estimation dates, diversification across parameter or formation choices, or the
  strategy-ensemble literature (family 7, still uncovered). This is also the literature most
  likely to speak to the journal's own standing open item — *what supplies decorrelated
  formation dates without being a K sweep*. The timing-luck sources answer only with offsets
  inside the rebalance cycle, which the champion already uses; any other source of decorrelation
  (across parameter choices, across signals) would have to come from the ensemble literature.
- **The temporal-breadth question above is now answered at the mechanism level** (2026-08-17
  session 3), by the forecasting-under-structural-breaks literature rather than by anything in
  finance: averaging a model over several *estimation windows* lowers out-of-sample forecast
  error relative to any single window, and requires no break detection. That is an accuracy
  claim — about the centre of the distribution — which is exactly what the estimator and
  dispersion framings could not supply. Tranching now has a three-part account: estimator
  (Jegadeesh–Titman), dispersion (Hoffstein et al.), accuracy (Pesaran–Timmermann). **What
  remains open is narrower and sharper**: the literature's AveW averages over *window lengths*,
  while the champion averages over *window end-dates* at constant length. Whether those are
  equivalent in effect, or whether length-diversity supplies decorrelation that date-diversity
  does not, is unresolved in the sources read and is the one live build in the candidate list
  (#8). It is also the standing journal question — *what supplies decorrelated formation dates
  without being a K sweep* — in its most tractable form yet.
- ~~**New open question raised by session 3:** the time-series-momentum literature's canonical
  construction deliberately discards signal magnitude, while the lab's largest single Sharpe
  gain came from magnitude weighting~~ — **largely resolved** (2026-08-17 session 4), and the
  resolution is more structural than the guess was. Goyal–Jegadeesh show the two families
  differ in the *benchmark* the past return is measured against — zero for time-series, the
  cross-sectional mean for cross-sectional — and that the benchmark choice is worth a market
  position, not a signal refinement. So MOP's sign-only rule is not a verdict on magnitude at
  all; it is answering a different question. On heterogeneous multi-asset sets, like-for-like
  scaled **cross-sectional** strategies significantly outperform scaled time-series ones, which
  is the direction session 3 guessed. **The residual, still the lab's own inference:** the paper
  attributes that outperformance to asset-class composition and to better bond selection, *not*
  to magnitude comparability. So the ranking is now sourced; the stated reason is not. Do not
  cite Goyal–Jegadeesh as proof of the magnitude-comparability story.
- **New open question raised by this session:** the volatility-timing literature's precondition
  — *timing pays only where conditional expected return does not rise with conditional variance*
  — is a testable property of a book, and Cederburg et al. establish that for most equity
  strategies it fails. Nothing read here says which side of that line a **concentrated,
  magnitude-weighted long-only momentum basket** falls on, and the lab's own trials give an
  ambiguous answer (basket-own-vol trimming lost; a style-orthogonal defensive-cohort trigger
  won by a small margin). A source characterising the conditional risk-return trade-off of
  concentrated momentum baskets specifically would sharpen the lab's one surviving overlay from
  "measured to work by ~0.019 Sharpe" to something with a mechanism. Low priority — the prize is
  small — but it is the only remaining thread in families 3 and 6 that is not already closed.
- ~~**Family 5 (low-vol / quality) and the risk-parity half of family 3 are now the only
  uncovered axes**~~ — **both covered and both closed** (2026-08-18 session 5); see the two
  struck items at the top of this list. The honest summary across all seven families is
  unchanged and now final: the literature has been far better at **closing** directions than at
  supplying new ones — which is itself the most useful thing it has done, given that every trial
  permanently raises the deflated-Sharpe bar.
- **New open question raised by session 5, and it is the one worth chasing next.** Every
  candidate in this list above rank 8 is a *screen* — a rule for declining to spend a trial —
  and the folder now has eleven of them against one live build. That ratio is a signal about
  where to look, not a complaint: the productive vein has consistently been methodological
  literature that grades the lab's own mechanisms (estimation error, forecast combination,
  structural breaks, construction artifacts), not strategy-family surveys. The specific
  unexploited seam is **the lab's one unexplained mechanism**: temporal breadth now has an
  accuracy-level account (averaging over estimation windows), but the *portfolio* question —
  why holding several formation vintages raises return rather than only lowering turnover or
  dispersion — still rests on the repo's own evidence. Nothing read in five sessions makes that
  claim. Adjacent literatures not yet touched that might: the bagging / bootstrap-aggregation
  literature on why averaging unstable predictors improves them (Breiman and successors), and
  the model-averaging literature in economic forecasting outside the break-detection framing.
  If either supplies a mean-shifting rather than variance-shrinking argument, it would give the
  repo's strongest mechanism its first outside justification.

  **— ANSWERED 2026-08-19 (session 6), and the answer is yes, from both literatures plus a
  third.** Breiman's bagging inequality is exactly a mean-shifting claim: aggregating a
  procedure over perturbed datasets lowers *expected squared prediction error*, unconditionally,
  by an amount equal to the procedure's instability — not dispersion around an unchanged mean.
  It comes with two on-paper preconditions the champion demonstrably meets (its membership rule
  is subset selection, the canonical unstable procedure; its selection step is nonlinear, and
  bagging leaves additive statistics unchanged) and one honest gap (it is an MSE claim about a
  predictor, and the bridge to portfolio return is the lab's inference, not the source's).
  Independently, the fundamental-law literature supplies the same conclusion in portfolio
  vocabulary and adds the part the lab was missing: adding *names* raises `N`, a saturated
  `√N` lever, while averaging weakly-correlated *formation dates* lowers `σ_IC`, the term that
  dominates once `N` is moderate. And Hansen's model averaging beats even the *infeasible
  optimal* single model, which upgrades "you can't pick the best one" to "the best one isn't
  the target". **The repo's strongest mechanism now has three independent outside accounts and
  one measured precondition; it is no longer the folder's unexplained result.**
- **New open questions raised by session 6, in priority order.**
  (a) *The bridge that is still the lab's own.* Every one of the three new accounts is a claim
  about **forecast accuracy or information ratio**, and the lab's result is about **realised
  net return and Sharpe on a long-only book after costs**. Nothing read in six sessions makes
  the crossing explicit. A source that translates a reduction in forecast MSE (or in strategy
  risk) into a portfolio's realised return under a *constrained, fully-invested, cost-paying*
  implementation would close the last gap. Candidate vocabulary not yet searched:
  the "implementation shortfall / alpha decay" literature, and portfolio-choice work that
  optimises the realised objective directly rather than a predictive loss.
  (b) *Counting independent bets.* Both the fundamental-law sources concede that determining
  breadth in practice — how many of `N` nominal bets are independent — is unresolved, and the
  lab's own standing question about what supplies decorrelated formation dates is the same
  question. There is a methodological literature on the *effective* dimensionality of a
  correlation matrix (SVD/eigenvalue counting rules, entropy-based "effective number of bets")
  that was seen but not evaluated this session; if it holds up to the rubric it would turn the
  lab's rank-correlation gate into a single scalar computable from holdings alone. Worth one
  session, no more — the sources sighted so far look tier C.
  (c) *Deliberately not pursued, recorded so it is not rediscovered as an opportunity.* The
  natural experiment suggested by (a) — measure the per-vintage IC series and its volatility —
  **scores returns and is therefore not a free diagnostic**. It should be treated with the same
  discipline as a backtest, not slipped in under the holdings-only exemption.

  **— (a) ANSWERED 2026-08-20 (session 7), from three directions.** The crossing exists and it is
  strongest from the friction side. Gârleanu–Pedersen's Proposition 5 states that a cost-paying
  mean-variance investor's optimal book **is** an exponentially weighted average of past target
  portfolios — a portfolio-level equality, in the currency the lab measures in, not a claim about
  a predictor's MSE. The averaging structure is therefore not a variance-reduction device applied
  to a cost problem; under quadratic costs it is the optimum. Two boundaries came with it and both
  matter: the derivation is unconstrained and needs `B`, `Σ`, `Φ`, `λ` estimated (screen #1's
  class), and the authors state that under **proportional** costs — this repo's cost model — the
  optimal policy is instead a **no-trade band**, which is the champion's buffer. So the repo's two
  construction mechanisms turn out to be the canonical answers to the two standard cost
  specifications. From the estimation side, the "optimise the realised objective directly"
  literature exists (parametric portfolio policies) but resolves the *opposite* way for this lab:
  its method is precisely the in-sample-objective fitting the DSR gate exists to punish, and its
  own critique reports that parameter parsimony does not confer protection. And the by-product is
  the most immediately usable thing the session produced: **trading diversification** supplies a
  closed-form, holdings-only, pre-trial prediction of what any `K`-leg averaging proposal does to
  turnover. *The honest residual*: what is now sourced is that the optimal cost-aware book has the
  averaging *form*; what remains the lab's own is the claim that its particular equal-weight,
  fixed-`K`, long-only, buffered instance earns more than its single-vintage counterpart. Nobody
  read here derives a long-only constrained version, and the transfer coefficient (0.3–0.8) is the
  only quantification of what the constraint costs.

- **New open questions raised by session 7, in priority order.**
  (a) *The one measurement the folder now recommends and the lab has not made.* Every vintage,
  horizon and ensemble diagnostic run here so far has measured score rank-correlation or weight
  overlap; Proposition 3 says the statistic that governs the **cost** axis is the correlation of
  the legs' *rebalancing trades*, which is a different object and is free to compute. It is not a
  literature question — it is a note that the next construction proposal should carry a predicted
  turnover ratio, not just a predicted overlap.
  (b) *Session 6's question (b) is still untouched and still worth exactly one session*: the
  effective-number-of-bets / effective-dimensionality literature, which would turn the
  rank-correlation gate into one scalar computable from holdings. Sources sighted so far look
  tier C; the `√((1+ρ(K−1))/K)` form found this session is a reminder that the useful version of
  such a statistic is usually one that falls out of a closed form rather than one proposed as a
  metric.
  (c) *What a long-only constraint costs, quantitatively.* Three separate sources now report the
  constrained version of their result as materially weaker than the unconstrained one, and the
  only number the folder has is the transfer coefficient's 0.3–0.8 range. A source that
  characterises the long-only constraint's cost as a function of the signal's cross-sectional
  dispersion (rather than as a range) would price the single largest structural discount this repo
  applies to everything it imports. Low-to-medium priority: it would not open a build, but it
  would make every "this is long-short evidence" verdict quantitative instead of directional.
  (d) *Recorded as declined, not as an opportunity.* Lamoureux–Zhang's remedy — fit or select on a
  **more concave** objective than the target — would, applied here, mean changing the promotion
  criterion. That lives in a frozen file and is a human decision; it is written into the
  cross-cutting principles for the human reviewing the ⚠ standing protocol concern and must not be
  read as licence for a session to re-rank candidates on a self-chosen criterion.

  **— (b) ANSWERED AND CLOSED 2026-08-21 (session 8), with a correction and a downgrade.** The
  effective-number-of-bets literature exists, is exactly as tier-C as session 6 suspected, and
  yields two things and no more. The *correction*: the statistic the lab already reports
  ("6.0 effective risk bets") is a Herfindahl count over marginal risk contributions of
  correlated assets, which is not a count of uncorrelated sources; the measure that is one
  changes basis first (`N_Ent = exp(−Σ p_n ln p_n)` over the diversification distribution), and
  for a fully-invested long-only book must be computed **conditionally** on the first principal
  portfolio, whose exposure the budget constraint alone determines. The *screen*: `√N` counts
  independent bets, so the right test of whether breadth widening can help is whether it raises
  the count of correlation eigenvalues `≥ 1`, not the instrument count. Both are free and
  holdings-only. Two things this did **not** deliver, stated so the axis is not reopened: no
  closed form fell out of it (session 7's warning that "the useful version of such a statistic is
  usually one that falls out of a closed form" was right — the entropy index is proposed as a
  metric), and the sources' empirical content is too thin to support anything beyond direction.
  The axis is spent.

  **— (c) PARTLY ANSWERED 2026-08-21, from the opposite direction to the one requested.** The
  question asked for the long-only constraint's cost as a function of signal dispersion. What
  turned up instead is that the accounting had a **missing term of the opposite sign**:
  Jagannathan–Ma show a binding weight constraint is algebraically a shrinkage of the covariance
  estimate, applied where estimation error is worst, at the cost of estimating nothing. So the
  net effect of long-only is (signal leakage, `TC` 0.3–0.8) *minus* (estimation-error suppression,
  unquantified), and the folder has only ever counted the first. The originally-requested
  quantification — leakage as a function of cross-sectional dispersion — remains open, and the
  natural next place to look is the Grinold–Kahn long-short efficiency literature and
  Clarke–de Silva–Sapra, which were sighted this session but are closed-access and could not be
  read in full. Low priority still: it would make imports quantitative, not open a build.

- **New open questions raised by session 8, in priority order.**
  (a) *The one genuinely uncovered axis this session found, and it was an accident.* Nothing in
  eight sessions had distinguished the return a book earns from its **signal** from the return it
  earns from **rebalancing** — `½ Σ_i w_i(σ_i² − σ_ip²)`, paid for the contrarian act of holding
  weights constant, against the buy-and-hold increment paid for the opposite act of letting
  winners run. A cross-sectional momentum book that resets to signal-proportional targets is
  doing some of both and the two work against each other. The source found (Willenbrock, via
  Booth–Fama) settles the identity but models no transaction costs and does not treat a
  signal-driven book at all. **What would close it**: work that decomposes a
  characteristic-sorted portfolio's geometric return into a strategic term, a rebalancing term
  and a cost term — vocabulary not yet searched includes "rebalancing premium", "volatility
  return / variance drain", and the geometric-vs-arithmetic literature on portfolio choice.
  Highest-value remaining thread, because unlike every screen in the candidate list it names a
  quantity the champion is currently *giving away* and the size of the give-away is computable
  from holdings.
  (b) *The counterweight to the folder's own top principle, and it is now overdue.* Eight
  sessions have produced a strong prior that constraints and equal weights beat estimated
  corrections. Session 8 found the first source arguing a constraint is doing something
  *positive* rather than merely avoiding harm. That asymmetry should be probed rather than
  enjoyed: is there literature in which a **binding** constraint is shown to cost more than the
  estimation error it suppresses, and does the crossover have a stated condition? Without it the
  folder risks recording "constraints are good" as a taboo, exactly the failure mode session 6
  corrected for equal weights.
  (c) *Deliberately not pursued, recorded so it is not rediscovered as an opportunity.* Meucci's
  mean-diversification efficient frontier — maximise `N_Ent` subject to a return floor — is a
  buildable strategy and is declined, not unexamined. It optimises over the eigenstructure of an
  estimated covariance, which is screen #1's expensive class at its most extreme, and the ERC
  theorem already closes the milder version of the same idea.

  **— (a) ANSWERED 2026-08-22 (session 9), and the answer arrives with its own premise reversed.**
  The decomposition exists and is a theorem, not a special case: for *any* weight process,
  `d log V^π = γ*_π dt + Σ_i π_i d log X_i`, so a signal-driven book's log growth splits exactly
  into a selection term and a non-negative excess growth rate computable from holdings and realised
  covariance with nothing forecast. That closes the identity question and hands the lab a
  return-denominated, holdings-only price for every concentration step it has taken. **But the
  framing this question was asked in was wrong.** The rebalancing term is not "a quantity the
  champion is giving away": the part that is real accrues to any diversified holder whether or not
  it rebalances, and the part specific to re-targeting trades is zero in expectation under IID and
  **negative when relative prices trend** — the regime a cross-sectional momentum book exists to bet
  on. So the give-away the question anticipated does not exist, and its nearest real counterpart is
  the *cost of concentration*, which is measurable. What is still not closed is the same bridge as
  ever: this is a decomposition of **log growth**, not of Sharpe on a costed, constrained book.
  **— (b) ANSWERED 2026-08-22 by dissolving it.** There is literature in which a binding constraint
  costs more than the estimation error it suppresses — the same method, same sample, different asset
  set, with the long-only endpoint optimal on one and beaten on the other — but there is **no stated
  general condition** separating the two cases. What the source supplies instead is better than a
  condition: under full investment the long-only constraint is the infinite-penalty endpoint of a
  continuous shrinkage path, so "how binding" is a scalar and the question becomes empirical rather
  than doctrinal. The taboo risk session 8 flagged is now guarded against explicitly in the
  cross-cutting principles.
  **— (c) remains declined**, unchanged.

- **New open questions raised by session 9, in priority order.**
  (a) *The one measurement this session recommends, and it is the folder's first return-denominated
  free diagnostic.* Compute `γ*_π = ½(Σ_i π_i a_ii − π′aπ)` on the champion's stored weight matrix,
  and on the weight matrices of the concentration ladder's earlier rungs (equal-weight,
  rank-weight, magnitude-weight, buffered vs. hard top-15). It scores no returns and forecasts
  nothing — it is an accounting split of growth already realised — and it would convert the
  standing "concentration costs drawdown" statement into "concentration costs *this much annualised
  growth* as well". It is also the only free diagnostic in the folder denominated on the axis the
  promotion gate actually reads, which matters given the ⚠ standing protocol concern. **Caution
  that must travel with it:** a large `γ*` is not a good strategy — a book can buy it by holding
  volatile uncorrelated names and lose more on the selection term — so it is a cost account, never
  an objective.
  (b) *The bridge, narrowed once more and still open.* Every account the folder now has of its own
  strongest mechanisms is a claim about forecast accuracy, information ratio, or **log growth**;
  the gate reads net Sharpe on a constrained, cost-paying book. Session 7 closed the friction half
  of this from Gârleanu–Pedersen; session 9 adds a growth-rate identity but not a variance one.
  The specific unread vocabulary is the geometric-vs-arithmetic literature on portfolio choice and
  the growth-optimal / Kelly criticism literature, which argues precisely about when maximising log
  growth diverges from what a finite-horizon, risk-scored investor wants. Medium priority: it would
  not open a build, but it is the last unpatched seam between what this folder imports and what the
  lab is scored on.
  (c) *The quantification that has now been requested twice and refused twice.* What the long-only
  constraint costs as a function of the signal's cross-sectional dispersion is still unanswered:
  session 8 got the opposite-signed term instead (constraints as shrinkage), session 9 got the
  continuum instead (constraints as tunable intensity). Both were more useful than the thing asked
  for, which is worth noticing before asking a third time. The remaining named targets are unchanged
  and both closed-access (Grinold–Kahn 2000 FAJ; Clarke–de Silva–Sapra 2004 JPM), plus
  **DeMiguel–Garlappi–Nogales–Uppal 2009 (Management Science)**, whose entire subject is the
  constraint-tightness trade-off and which this session could not read in full — recorded as unread,
  not summarised second-hand. Low priority, unchanged.
  (d) *Recorded as declined.* Stochastic portfolio theory's actual strategy — diversity weighting,
  `μ_i^p / Σ_j μ_j^p` — is declined rather than unexamined. It is defined on market-capitalisation
  weights, which this repo does not have and cannot approximate from adjusted closes without
  collapsing the construction into equal weighting; its outperformance result carries an explicit
  long-horizon condition (`T ≥ (2/pεδ)·log n`) far beyond the evaluation splits; and the source's
  own simulation charges no transaction costs.

  **— (b) ANSWERED AND CLOSED 2026-08-23 (session 10), in the negative, which is the useful
  direction.** The question was whether the geometric-vs-arithmetic and growth-optimal/Kelly
  literature would supply the crossing from log growth to the risk-scored quantity the gate reads.
  It supplies the opposite: **there is no such crossing, and the error of pretending otherwise grows
  with the horizon.** Samuelson shows the max-geometric-mean rule is suboptimal for every
  non-logarithmic iso-elastic preference at *every* finite `T`, that boundedness does not rescue it,
  and that the "almost certainly wins eventually" theorem cannot be converted into a statement about
  an expectation because the horizon at which dominance begins is unbounded in the wealth level.
  Merton–Samuelson price the substitution at `Π₁₂(T) = λ(γ)^(T/γ) → ∞`, show that for `γ < −1` the
  log-optimal program is dominated by holding only the riskless asset, and kill the two-parameter
  `(mean-log, variance-log)` repair as a limit-interchange fallacy whose own error diverges. The
  growth school does not dispute any of it and adds the only exact bridge in the literature,
  `g* = r_0 + ½·SR²` — which holds at the growth-optimal **leverage** and is therefore unavailable
  under gross leverage ≤ 1.0. **Consequence for the folder, stated plainly because it reverses a
  session-9 recommendation:** `γ*` was ranked session 9's top measurement on the explicit grounds
  that log growth is "the gate's own axis." It is not, and `learnings.md` has since measured the
  null this predicts. The identity survives as accounting; the axis claim is withdrawn. Recorded as
  the *"check the currency"* principle and candidate #27.
  **— (c) ANSWERED OBLIQUELY AND NOW RETIRED 2026-08-23.** Asked a third time and answered a third
  time by something other than what was requested — which, as the question itself noted, is now the
  pattern. What arrived instead is a re-weighting of the estimation-error side: errors in *means*
  cost roughly 10× errors in variances and 20× errors in covariances, with the multiple rising as
  risk aversion falls. That does not price the long-only constraint's leakage, and the transfer
  coefficient's 0.3–0.8 remains the only number the folder has. Three sessions have now failed to
  obtain it and the named targets are unchanged and all closed-access. **Stop asking**; if it is ever
  wanted, it needs a source acquired by a route this folder does not currently have, not another
  session of searching.

- **New open questions raised by session 10, in priority order.**
  (a) *The one derivation this session could not obtain, and it is the difference between an
  interesting caveat and a decisive one.* The standard error of a **single** Sharpe ratio is
  `sqrt((1 + ½SR²)/T)`, ≈ 0.40 on this repo's validation window — larger than the entire promotion
  ladder. But the gate does not compare a candidate to an unknown truth; it compares two nearly
  identical books evaluated on the *same* six years, whose return series correlate near 1, and for
  which the paired standard error `SE(ŜR_A − ŜR_B)` is far smaller than `√2·SE(ŜR)`. Lo does not
  derive it. **Until that paired quantity is in hand, the single-strategy standard error must not be
  quoted as evidence that the ladder's steps are noise** — a discipline this folder should hold
  itself to, because the number is rhetorically tempting and the inference is invalid. The named
  vocabulary not yet searched: the Jobson–Korkie / Memmel correction for testing the equality of two
  Sharpe ratios, and Ledoit–Wolf's robust bootstrap version of the same test. This is the highest
  value remaining thread in the folder: it would turn `learnings.md`'s ⚠ standing protocol concern
  from a pattern-in-a-table into a hypothesis test, computable from series the repo already stores.
  (b) *The deflated Sharpe ratio has never been covered, and the gate uses it.* `program.md` requires
  `deflated-Sharpe probability ≥ 0.95` and `learnings.md` reasons about DSR clustering, trial-count
  understatement, and effective-versus-recorded trials — all from local observation, with no note in
  `research/` on the statistic's own source or its stated assumptions. Its literature
  (Bailey–López de Prado and successors) would say what the deflator assumes about the *distribution
  of the candidate set*, which is precisely what "clustering makes within-family tuning nearly free"
  is an informal claim about. Explanatory only — the engine is frozen — but the folder has an
  obligation to cover the gate's own machinery, and it is the last uncovered piece of it.
  (c) *Recorded as declined rather than unexamined.* Fractional-Kelly sizing, drawdown-constrained
  growth optimisation (Grossman–Zhou and successors), and every other member of the capital-growth
  family are declined for one reason stated once: they are leverage rules, and this repo's gross
  leverage cap truncates them to "be fully invested." Grossman–Zhou 1993 (Mathematical Finance,
  optimal investment under a drawdown constraint, 379 citations on Semantic Scholar) was sighted
  this session, is closed-access with no repository copy found, and was **not read** — it is
  recorded as unread, not summarised from abstracts.
  (d) *A discipline note, not a question.* Session 9's top recommendation was measured and returned a
  null, and this session found the recommendation's stated premise was false. Both facts were
  available on paper before the measurement — the premise was a claim about units, checkable by
  reading. **Before ranking any future measurement first, check that its output is denominated in
  the unit the gate reads.**

  **— (a) ANSWERED AND CLOSED 2026-08-24 (session 11), in closed form, and the discipline it demanded
  is discharged.** The paired standard error exists, was derived in 1981, corrected in 2003, and is
  `T·Var(Δ̂) = 2(1−ρ) + ½(Sh_a² + Sh_b²) − Sh_a·Sh_b·ρ²`. For equal Sharpe ratios it factorises to
  `(1−ρ)[2 + Sh²(1+ρ)]`, so against Lo's single-strategy `1 + ½Sh²` the pairing discount is exactly
  `√((1−ρ)(2+Sh²(1+ρ))/(1+½Sh²))` and, at daily frequency where `Sh² ≪ 2`, simply **`√(2(1−ρ))`**.
  Annualised on a 1,562-day window that is `0.568·√(1−ρ)`, which reproduces both of the ranges
  `learnings.md` bootstrapped (0.026–0.07 at `ρ > 0.98`; 0.13–0.17 at `ρ ≈ 0.9`) without resampling
  anything, and is available *before* a candidate is built. Three riders, all load-bearing. The
  closed form is **liberal** under fat tails and volatility clustering — Ledoit–Wolf measure ≈2–3×
  the nominal rejection rate across six data-generating processes — so it is a **floor** on the error
  bar and never evidence of significance. The method that is close to nominal is a **studentized**
  circular-block bootstrap on the return *pairs* with a calibrated block length, which is the family
  the lab already built, missing only the studentization and the calibration. And the power fact
  reverses the intuitive reading: power *rises* with `ρ`, so the ladder's near-identical rungs are the
  test's most favourable regime, and comparing against a moving benchmark is structurally
  lower-powered than testing against zero — the gate asks the low-power question by construction.
  Recorded as candidate #29.
  **— (b) ANSWERED AND CLOSED 2026-08-24, and the gate's machinery is now fully covered.** The
  deflated Sharpe ratio is the Probabilistic Sharpe Ratio with its threshold set to the
  extreme-value approximation of `E[max{ŜR_n}]`. What it assumes about the candidate set is exactly
  what `learnings.md` had been inferring locally: the deflation depends on the number of
  **independent** trials (`N̂ = ρ̂ + (1−ρ̂)M`, so a tight family is nearly one trial) and on the
  **cross-trial variance of Sharpe ratios** (so dispersion is expensive in a way the trial count alone
  does not capture — the one genuinely new fact). The rival correction, which the DSR authors
  themselves call complementary, adds two things a single-threshold framing cannot: the penalty is
  strongly **nonlinear in the Sharpe level** (>50% below ~0.4, ≤~25% above 1.0), and under an
  **FDR**-controlling procedure the bar **stabilises** instead of rising without limit — so "every
  trial raises the bar" is a property of controlling family-wise error, not a law. All of it is
  explanatory; `engine/` is frozen. Recorded as candidate #30.

- **New open questions raised by session 11, in priority order.**
  (a) *The one refinement the folder now recommends, and it costs nothing.* The lab's paired
  bootstrap is the right method but is not studentized: Ledoit–Wolf show that a bootstrap which
  reuses a single standard error, or does not studentize at all, buys no accuracy over asymptotic
  inference, and that all of their gain over HAC comes from recomputing a standard error inside each
  resample and taking the quantile of `|Δ̂* − Δ̂|/SE(Δ̂*)`. Their second refinement is to **calibrate**
  the block length against a fitted bivariate GARCH rather than report robustness across a grid.
  Neither is a literature question; both are notes that the next paired-error measurement should be
  studentized and calibrated. Low cost, and the only reason it is ranked first is that everything
  else on this list is optional.
  (b) *The one diagnostic this session found and did not rank first, deliberately.* CSCV/PBO is
  computable from the `T×N` matrix of stored trial return series and would answer, non-parametrically,
  whether this lab's **selection procedure** has been overfitting — a question no statistic in the
  repo asks. It is ranked second and hedged because it fails two of the folder's own tests: it
  **scores returns**, so it is not covered by the holdings-only exemption (session 6's item (c)), and
  it is computed on the validation split, so it re-uses the split the gate already reads rather than
  supplying an independent look. It also assumes its columns are configurations of one search, which
  this repo's cross-family trial log is not. Worth doing only as a deliberate, journalled
  measurement on one family's ladder, never as a free diagnostic. Session 10's discipline note (d)
  applies: check the unit first — PBO is denominated in *rank consistency*, not in Sharpe.
  (c) *The gap both deflators leave, and it is now the only unpatched seam in the scoring apparatus.*
  Every multiple-testing correction read here treats the trials as draws to be counted or
  correlation-discounted. None of them treats a trial that was **motivated by a prior**, and both
  literatures say in passing that they should: Harvey–Liu–Zhu state that "a factor derived from a
  theory should have a lower hurdle than a factor discovered from a purely empirical exercise" but
  offer no machinery for it, and the DSR authors' optimal-stopping aside assumes the candidate set is
  already restricted to the "theoretically justifiable". A source that formalises a *prior-weighted*
  or hierarchical multiple-testing correction would be the one thing that could distinguish this
  lab's hypothesis-first protocol from a parameter sweep of the same length. Named vocabulary not yet
  searched: Bayesian and hierarchical multiple testing (both sources gesture at it and decline it),
  and empirical-Bayes / local-FDR treatments of factor discovery. Medium priority, explanatory only —
  it would not open a build and could not change a frozen gate — but it is the only remaining
  question about the scoring apparatus that has an answer worth having.
  (d) *Recorded as declined, so it is not rediscovered as an opportunity.* The obvious use of
  everything in this session — recomputing the repo's own DSR under a different `N̂`, a different
  error rate, or the haircut framework, and reporting that the champion "would have passed/failed" —
  is **declined**. It is reinterpreting the promotion criterion, which lives in a frozen file and is a
  human decision, and it is the same failure mode session 7's item (d) recorded. The notes state the
  assumptions; they do not re-score anything.

  **— (c) ANSWERED AND CLOSED 2026-08-25 (session 12), from all three directions it named, and the
  answer arrives with a constraint the question did not anticipate.** The machinery exists
  (Genovese–Roeder–Wasserman's weighted BH), is rigorous, and is indifferent to whether the weights
  are any good: FDR and family-wise control hold for *any* non-negative weights fixed a priori,
  provided they **average one**. That budget is the whole finding. **A prior discount is legitimate
  and strictly zero-sum** — relaxing one candidate's threshold requires tightening others by exactly
  as much — so an unweighted protocol like this repo's is the `W ≡ 1` case, and nothing here licenses
  a session to treat its own hypothesis as pre-approved. Three riders make it usable anyway: the
  optimal weight is **unimodal**, so a recorded ranking should back the plausible-but-marginal idea
  rather than the strongest conviction, and should be **sparse**; weights estimated by splitting the
  scored sample **do not beat using the whole sample unweighted**, which closes the tempting shortcut
  at the mechanism level; and the finance-venue version prices the whole thing — moving from a 19:1
  long-shot prior to even odds is worth about **1.0 in t-units**, and even at even odds under the most
  favourable Bayes factor that exists the required `t` is 2.43, *above* the naive 2.0. So the answer
  to "can this lab's hypothesis-first protocol be distinguished from a parameter sweep of the same
  length?" is yes, quantitatively, and the honest size of the distinction is far smaller than the
  rhetorical weight it usually carries. The hierarchical branch adds the one genuine sign reversal in
  the literature — a large family of *weakly-correlated* related tests is partly evidence rather than
  only a penalty — and its own formula (`κ_g → κ` as `ρ → 1`) rules the reversal out for this repo's
  near-identical variant ladders. Recorded as candidates #31, #32, #33.

- **New open questions raised by session 12, in priority order.**
  (a) *The one thing this session recommends, and it is a journal convention rather than a
  measurement.* Everything above depends on a ranking or a prior being **recorded before the run**.
  The lab already writes its hypothesis first (`CLAUDE.md`), but never records where the candidate
  sits in its own prior ordering, so nothing in `trials.jsonl` or the journal distinguishes a
  theory-first trial from a post-hoc rationalisation — which is precisely the distinction all three
  sources say is worth something. The cheap fix is one line per trial: the prior odds the session
  would have stated, and which mechanical reason supports them. It costs nothing, requires no engine
  change, and is a precondition for any of #31/#32 ever being more than a lens. Ranked first because
  it is the only item here with a deadline: a prior recorded after the result is worthless.
  (b) *The seam the scoring apparatus no longer has, and what that implies for targeting.* With (c)
  closed, **the gate's machinery is covered on all four sides** — the statistic, the deflator, the
  paired test, and the motivation question — and the folder has no remaining question about how this
  lab is scored. Six sessions of methodological work have been the productive vein; that vein is now
  close to exhausted at the level of *scoring*. The honest implication is that session 13 should look
  somewhere structurally different rather than for a fifth angle on the same apparatus. Two
  candidates, both untouched in twelve sessions: the **execution / implementation-shortfall**
  literature, which is the only cost-side vocabulary the folder has never opened (session 6 named it
  and session 7 answered from friction-aware portfolio choice instead); and the **statistical
  properties of the universe itself** — survivorship bias and constituent selection, which
  `learnings.md` lists as a permanent caveat and which no note here has ever sourced. The second is
  the better bet: it is the largest unquantified discount this repo applies to every stock-level
  result, and unlike the long-only leakage question (retired 2026-08-23 after three failures) it has
  a large, accessible, multi-decade literature.
  (c) *Recorded as declined, so it is not rediscovered as an opportunity.* Constructing an actual
  weighted-BH or hierarchical correction over `trials.jsonl` and reporting what it says about the
  repo's own record is **declined**, for the reason session 11's item (d) already gave and for a
  second one specific to this session: it would require assigning retrospective priors to trials whose
  results are known, which is the one thing the weighting theorems forbid. The notes state the
  machinery; they do not apply it to this repo's history.

  **— (b) ACTED ON 2026-08-26 (session 13), taking the target it recommended, and the recommendation
  was right.** Session 12 judged the universe's own statistical properties the better of its two
  candidates because it is the largest unquantified discount the repo applies and has a large
  accessible literature. Both halves held. The literature is large, tier-1 and directly on point — one
  of the sources opens by writing out this repo's universe-building recipe step by step before showing
  it is a bias worth up to 8% per annum. And the yield is not another screen: it is a **correction to
  the lab's oldest permanent caveat**, which has been aimed at the *level* of single-stock returns
  (the forgiving half, and the half whose standard correction is provably too severe) rather than at
  *persistence inference* (the severe half, and precisely what a cross-sectional momentum strategy
  claims). Two things the session could **not** deliver, stated so they are not expected later. No
  magnitude for this repo: the matched-pair measurement that would size the bias needs point-in-time
  constituents, which `program.md` gates behind human approval, so the honest status is "mechanism
  sourced, direction unambiguous, magnitude unmeasurable with the data the repo has." And no bridge to
  the gate's currency: every statistic found is a probability of beating a benchmark, a median
  buy-and-hold return, or a rejection rate for a persistence test — none is net Sharpe on a costed
  constrained book, which is session 10's *check the currency* discipline biting for the third time.
  The other candidate session 12 named — the **execution / implementation-shortfall** literature —
  remains untouched and is now the only one of its two left.

- **New open questions raised by session 13, in priority order.**
  (a) *The one proposal that would change what the lab knows, and it needs a human.* The
  random-portfolio null (candidate #35) is the only control in the folder that is valid **on a
  contaminated universe**, because the contamination applies to both sides of the comparison. It is
  also the only proposal here that fails all three of the folder's own cheapness tests at once — it
  scores returns, it re-uses the validation split, and `CLAUDE.md` routes every strategy run through
  `run_experiment.py`, so whether a null distribution consumes trials is not a session's call. It is
  therefore ranked first as a **question to the human reviewer**, not as work a session may start.
  What makes it worth asking: the repo currently has no answer at all to "how much of the champion's
  edge is available to an information-free book on this universe", and the source's illustration shows
  that number can be large.
  (b) *The last untouched vocabulary session 12 named.* **Execution and implementation shortfall** is
  now the only cost-side literature the folder has never opened — session 6 named it, session 7
  answered from friction-aware portfolio choice instead, and session 12 ranked it second. The honest
  prior is that it will close rather than open: `learnings.md` prices total cost drag at ~0.019 Sharpe
  and the cost-mitigation literature was declared closed for idea supply in session 2. Worth one
  session at most, and only if nothing better presents itself.
  (c) *A target that did not exist before this session.* Three of the four sources read here are
  US-only, and two of the three are single-market with no replication. This repo's universe is
  **global**, and no note in the folder sources what constituent selection does outside the US, where
  index construction rules, delisting practice and the size distribution all differ. The one global
  source sighted (Bessembinder et al. 2023, ~64,000 stocks by its title) is closed access and was
  not read, and carries `validation_overlap` in any case. Medium priority, and it has a stated failure
  mode: it would supply robustness for a discount whose magnitude the repo cannot measure anyway.
  (d) *Recorded as declined, so it is not rediscovered as an opportunity.* Attempting to *correct* the
  repo's stored results for survivorship — re-scoring the champion under an assumed bias, or applying
  BGIR's residual-standard-deviation normalisation to the trial log — is **declined**, for session 11's
  item (d) reason and for a second specific one: BGIR offer that normalisation explicitly as a
  conjecture, not a result, and every magnitude in these notes belongs to a different universe than
  this repo's. The notes state the mechanism; they do not adjust anything.

  **— (b) ANSWERED AND CLOSED 2026-08-27 (session 14), and the prior attached to it was right about
  the direction but wrong about the value.** Session 13 predicted the execution literature would close
  rather than open, on the grounds that `learnings.md` already prices total cost drag at ~0.019 Sharpe
  and session 2 declared cost mitigation exhausted. It does close — nothing here opens a build — but
  "closes" turns out to mean three specific things the folder did not have. **(i) The 15 bps/side rate
  is now graded from outside, and it holds.** Against $1.7tn of live institutional executions across
  21 developed markets, mean per-trade implementation shortfall is 11.02 bps (median 8.63,
  value-weighted 16.06) at ~0.9% of daily volume, and the source defines its benchmark price as the
  prior close at which the model generated its trades — the engine's own convention, word for word. So
  the repo charges the right *quantity* at a level that is conservative-to-fair, and the drag is not
  secretly larger than modelled. Every previous statement about cost in this repo rested on the
  engine's own assumption; that assumption now has outside support. **(ii) The one asymmetry that
  points against this repo is identified and priced.** Impact is denominated in volatility; the flat
  charge is not; a momentum basket holds the high-volatility tail by construction. The correction is a
  multiplier, is a free holdings-only diagnostic (#39), and is small enough at 3.0× turnover that it
  moves nothing — which is worth having *because* it converts an unexamined assumption into a bounded
  one. **(iii) The literature's standing objection to this repo's champion family is adjudicated.**
  Two tier-1 papers disagree about whether momentum survives costs; the disagreement is entirely about
  the cost function's shape and level, and the live-execution measurement rules against both in the
  same direction. What survives the correction — momentum sorts toward expensive stocks, and 53–70% of
  the long-short spread lives on the short leg — is structural, transfers here, and is now candidate
  #37. **The discipline note session 13 would want recorded:** its prior ("worth one session at most,
  and only if nothing better presents itself") was correct as a *ranking* and would have been wrong as
  a *skip*. A vocabulary that only closes things is still worth one session when what it closes is a
  parameter every result in the repo is divided by.

- **New open questions raised by session 14, in priority order.**
  (a) *The folder has now covered every axis it named, and the honest consequence is that there is no
  obviously-correct target for session 15.* Fourteen sessions have closed: all seven `program.md`
  families; portfolio construction and rebalance mechanics; the objective and the gate's full scoring
  apparatus (statistic, deflator, paired test, motivation question); the universe's own statistical
  properties; and now the cost side, on both the level and the functional-form halves. The two
  candidates session 12 named as structurally different are both spent. **This should be stated as a
  finding rather than as a gap**: the marginal literature session is now worth materially less than
  the first ten were, and a session that finds nothing is a more likely outcome than at any prior
  point. The three directions that remain genuinely unopened, none of them compelling: the
  **cross-sectional-anomaly replication crisis literature at the level of individual predictors**
  (Hou–Xue–Zhang's *Replicating Anomalies* is cited throughout this folder as a rubric input but has
  never been read as a source); the **behavioural-finance mechanism literature** on why momentum
  exists at all, which would inform hypothesis *motivation* under the prior-weighting machinery of
  session 12 (#31) rather than construction; and **international/global evidence on momentum
  construction specifically**, which matters because this repo's universe is global and almost every
  source in this folder is US-only. The third is the best of the three and is the only one that could
  change a construction choice.
  (b) *The one thing this session recommends measuring, and it is cheap.* Candidate #39 — the
  turnover-weighted volatility ratio of the held book against the universe median — is free,
  holdings-only, and denominated in Sharpe once multiplied through the existing drag. It should be
  computed once and recorded, not because it will change a verdict (the arithmetic says it will not)
  but because it converts "the flat cost model is presumably fine" into a bounded statement, and the
  folder has twice been embarrassed by unexamined premises that were checkable on paper (session 10's
  discipline note (d)). Low value, near-zero cost.
  (c) *Recorded as declined, so it is not rediscovered as an opportunity.* The **LDV / zero-return-day
  cost estimator** is the one cost model in this literature that runs on daily closes alone, and is
  therefore the only externally-motivated per-instrument cost estimate this repo could actually build.
  It is declined for three independent reasons stated in full in the momentum-cost note: it is a fitted
  per-instrument parameter (screen #1's class) estimated on the same window as the signal; its input
  signal — zero-return days — is nearly absent in a global large-cap and ETF universe, so it would fit
  noise; and the live-execution evidence places its whole estimator family at the top of the
  overstatement ladder. **Buildable, and should not be built.**
  (d) *Also declined, with a mechanism.* Executing the rebalance more patiently over several days is
  the natural "free" cost idea and is priced by the permanent/temporary split: patience reduces only
  the temporary term, as `T^{3/5}`, while 85–90% of measured impact is permanent. It attacks the small
  half of the cost, and the engine's single one-day lag is frozen in any case.

  **— (a)'s third direction ANSWERED 2026-08-28 (session 15), and against session 14's own
  expectation it opened rather than closed.** Session 14 named three remaining unopened directions
  and predicted the marginal session was now worth materially less; it ranked
  **international/global momentum construction** best of the three because this repo's universe is
  global while almost every source in the folder is US-only. That ranking was right, and the
  session produced the folder's first *construction* lead in some time plus its first *signal*
  idea ever. The four findings, in the order they matter: **(i)** three tier-1 sources spanning
  three decades build a global momentum book by ranking **within markets and pooling afterwards**
  — Fama–French use each region's own momentum breakpoints even when constructing global
  portfolios — and none of them ranks a single global pool, which is what this repo does.
  Rouwenhorst reports what the change buys and the shape is the useful part: the mean is nearly
  unchanged, the legs' correlation rises and the spread's volatility falls ~40%. It is a
  **variance** mechanism with a **named, cited confound** (large country-specific components in
  international returns), which is precisely what candidate #5 demands and what the lab's refuted
  sector-neutral z-score lacked — the first grouping ever to pass that screen (#40). **(ii)** Four
  independent sources put this universe in the size bucket where momentum is weakest, and
  Fama–French's *global big-stock* spread carries a t-statistic near 1.4 — pooled across 23
  developed markets over two decades, large-cap momentum is not statistically distinguishable from
  zero (#42). **(iii)** Geography does not diversify momentum: ≈0.65 cross-market co-movement,
  stronger than passive exposures, on market-neutral strategies — the fundamental-law point in
  published numbers, and it retro-explains the lab's own basket-widening null (#43). **(iv)** The
  by-product, and the first thing this folder has ever supplied that the repo could not already
  compute: **the negative of the past 5-year return is a price-only value proxy**, used as such
  for every asset class without book values and validated against BE/ME, correlating ≈ −0.5 with
  momentum (#41). Two things the session deliberately did **not** do: it did not adjudicate the
  Chui–Titman–Wei / Fama–French disagreement about whether cross-market momentum differences are
  real (recorded in both notes, and the later source is the skeptical one), and it did not convert
  that disagreement into a regional exclusion rule (#44 is the anti-candidate).

- **New open questions raised by session 15, in priority order.**
  (a) *The one thing the lab can settle that the literature cannot.* Candidate #40 is now the
  folder's best-motivated buildable proposal, but every source supporting it measures a
  **long-short, single-asset-class, equity-only** book, and this repo's universe mixes global
  large-cap stocks with country and regional **ETFs** — instruments that *are* regions rather than
  belonging to one. Nothing read anywhere in fifteen sessions describes neutralising a grouping in
  a universe whose members include the groups themselves. That is not a literature gap a future
  session can fill by reading more; it is a design question for the strategy agent, and the note
  states the two options (group the legs separately, or group the stock leg alone). Recorded here
  so a future session does not spend itself looking for a source that will not exist.
  (b) *The residual on the currency axis, and it is genuinely open.* Both international sources
  compute momentum on returns converted to a single currency and **both state that exchange-rate
  risk is ignored rather than handled** — Fama–French say so explicitly and call it a potential
  problem in their inferences. This repo converts to USD unhedged and computes signals on the
  converted series, so its convention is the literature's convention *and* the literature's
  acknowledged approximation. What no source read here answers is whether the FX component inside
  the signal carries information, is noise, or is a country bet in disguise — which matters
  because #40's whole claim is that a pooled global rank takes an unrequested market bet. The
  vocabulary not yet opened: the international-asset-pricing literature on currency risk premia
  and hedging (Adler–Dumas, Dumas–Solnik are the names both sources cite for it). Medium priority
  with a stated failure mode: it may resolve into "hedging is unavailable here anyway", in which
  case it closes without changing anything.
  (c) *A source-quality debt this session incurred and should be paid before anything leans on it.*
  Chui–Titman–Wei is recorded from its **November 2004 working paper**; the published JF 2010
  article was not obtained, and two of the findings used here come from its published abstract
  only. Nothing in the current candidate list depends on a number from it — #44 uses it as the
  hypothesis being declined, and its construction details corroborate two other sources rather
  than standing alone — but if a future session ever wants its size or transaction-cost relation
  quantitatively, the published version must be read first.
  (d) *Recorded as declined, so it is not rediscovered as an opportunity.* The obvious next move
  after #41 — sweeping the reversal lookback (3-year, 5-year, 7-year) to find which value horizon
  pairs best with momentum — is **exactly the parameter-sweep spam `program.md` forbids and the
  deflated-Sharpe bar punishes**. If #41 is ever built, it is built once at the literature's
  stated horizon, and a horizon that disappoints is a result about the idea, not an invitation to
  search. The folder's own bracket discipline (`learnings.md`, horizon axis) says the same thing.

- **Tooling limitation — RESOLVED 2026-08-17.** Sessions 1–3 ran in an egress-restricted
  environment that permitted only package registries plus Anthropic hosts, so `WebFetch` failed
  for every domain probed, Crossref and Semantic Scholar returned 403 at the proxy tunnel, and
  web-search result summaries were the only literature channel — **no full text was ever read
  directly** for any note written in those sessions. The learning agent's schedule has since been
  moved to a full-egress environment; scholar APIs (Semantic Scholar, OpenAlex, Crossref), Google
  Scholar, arXiv PDFs, NBER and AQR are now all reachable, and full text can be read directly.
  See `research/README.md` → "Network access" for the working lookup recipe and the three
  remaining limits (Semantic Scholar title-search rate limits; OpenAlex's daily budget; SSRN and
  ScienceDirect serving Cloudflare bot challenges, which is the origin refusing an automated
  client, **not** an egress block).

  **Session 16 (2026-08-29) read full text directly for six of its eight sources**; one is recorded
  **second-hand** and one from its **published abstract only**. The session's access lesson is new to
  this folder and worth generalising: **a journal's own editor-hosted mirror can be a better channel
  than the publisher**, and **an author's later habilitation or PhD thesis reproduces their journal
  articles verbatim**, header and pagination included, which is the cleanest route yet found to a
  paywalled Elsevier article. Concretely: both *Critical Finance Review* papers (the commissioned
  Amihud replication and Amihud's reply) came from `cfr.ivo-welch.info/published/papers/` — the
  editor's own site — where Emerald would have refused; the directory has no index page and returns
  nothing to a listing request, but **the filenames follow `<firstauthor><year><keyword>.pdf` and one
  guess from that pattern found the replication on the second try**, which is a cheaper channel than
  another search once one file from a journal is in hand. And Molnár's *International Review of
  Financial Analysis* article, closed on ScienceDirect and 403 on SSRN, is reproduced in full as
  Chapter 2 of his 2020 habilitation thesis on a University of Economics in Prague server, complete
  with the IRFA volume-and-page running header. Other channels that worked first try, all previously
  recorded: an **author's own university page** (`sas.upenn.edu/~fdiebold/`) for the typeset JF
  article; a **university course reading directory** (`cis.upenn.edu/~mkearns/finread/`) — the same
  host *pattern* as session 14's Almgren find, and it served the typeset JFM article; **NBER working
  paper PDFs** for the RFS article; and a **business school's seminar archive**
  (`w4.stern.nyu.edu/finance/docs/pdfs/Seminars/`), new to this list, which served the full working
  version of a JFE article. One guessed URL failed silently in the documented way (a
  `dachxiu.chicagobooth.edu` path returned no file at all rather than a 404 page), and one NHH
  open-access repository link returned nothing to `curl` on either the query-string or the bare
  form. Index behaviour, and it extends the folder's standing rule rather than contradicting it:
  **Semantic Scholar's DOI endpoint does not resolve `10.1093/rfs/hhaa009`** — a 2,323-citation RFS
  article — while resolving four other DOIs the same session on the first try, so the "go to Crossref
  first" rule now has an **RFS** instance alongside its JF ones. The session's citation-count anomaly
  runs the folder's usual way: **Crossref reports 292 for Heston–Sadka 2008 against Semantic
  Scholar's 97**, a third-of-the-true-value undercount on a tier-1 JFE article, and a further
  instance of "disbelieve a lone low count". OpenAlex was not needed and was not queried, leaving its
  daily budget untouched. Two sources are recorded as less than fully read and are flagged in-note
  and above: the four range-estimator primaries (Parkinson, Garman–Klass, Rogers–Satchell, Meilijson)
  are taken **second-hand** from Molnár's restatement-with-derivations, cross-checked against an
  independent restatement in Alizadeh–Brandt–Diebold — the same two-independent-restatements standard
  session 11 used for Jobson–Korkie — and Heston–Sadka 2010 (JFQA, the international companion) is
  `oa_status` closed with no repository copy and is used only at the level of its published abstract.

  **Session 15 (2026-08-28) read full text directly for all four of its sources**, one of them in a
  working-paper rather than published version (Chui–Titman–Wei, flagged in-note and in the coverage
  log). The session's access lesson is that **a web search naming the paper plus `pdf` still beats
  guessing filenames on faculty hosts** — three of the four PDFs came straight out of search
  results, and the two guessed paths tried (a Houston PhD-course mirror and a Semantic Scholar PDF
  mirror) returned 403 and an empty 202 respectively. New channels that worked first try and are
  worth the list: **a business school's working-paper depot** (`depot.som.yale.edu/icf/papers/…`)
  served the full pre-publication version of a 1998 *Journal of Finance* article, complete with
  abstract, tables and the SSRN stamp; **a co-author-adjacent academic's personal site**
  (`johnhcochrane.com/s/…`) served the typeset *JFE* article, which is a reminder that the host
  need not belong to an author of the paper; **an author's NYU Stern page**
  (`pages.stern.nyu.edu/~lpederse/papers/`) served the typeset *Journal of Finance* article with
  volume and page headers; and — new to this folder — **a conference-proceedings mirror on a
  foreign university's finance department server** (`fin.ntu.edu.tw/~conference/…`) served the
  full working paper of an article whose published version is paywalled on both Wiley and SSRN.
  Index behaviour, and this session **narrows** the folder's standing rule rather than confirming
  it: Semantic Scholar's DOI endpoint does not resolve `10.1111/0022-1082.95722` (a 1,357-citation
  1998 *Journal of Finance* article), but it resolved the **other two JF DOIs** it was given this
  session on the first try. With sessions 12 and 13 missing and session 14 hitting, the honest form
  of the session-12 rule is weaker than "JF DOIs miss": **go to Crossref first for a JF DOI,
  because a Semantic Scholar miss there is common enough not to be evidence the paper is
  unindexed** — and the misses skew old (1995, 1998) while recent JF DOIs resolve. The sharper
  anomaly this session is elsewhere: Semantic Scholar reports **361** citations for Fama–French
  2012 against Crossref's
  **1,431** — another instance of session 7's "disbelieve a lone low count", and a wide one for a
  paper whose venue and vintage make a four-figure count unsurprising. Crossref answered every lookup, including two DOIs recovered by
  `query.bibliographic` after a plausible-looking DOI failed. OpenAlex was not needed this session
  and was therefore not queried, leaving its daily budget untouched. One count is worth flagging
  in the *agreeing* direction for balance: for Asness–Moskowitz–Pedersen the two indices land
  within 2% of each other (2,078 vs 2,041), which is the exception in this folder's experience.

  **Session 14 (2026-08-27) read full text directly for four of its five sources**; the fifth was not
  obtainable by any route and is recorded **unread**, its one contribution (a definition) taken only as
  restated inside a source that was read. The session's access lesson is that **a university course's
  reading-list directory is a searchable index, not just a link** — a guessed filename for the
  Almgren *Risk* article hit a `~faculty/finread/` directory on a CS department server, and fetching
  the **parent directory** and grepping its `href`s turned up the correct file immediately, the same
  trick that worked on Duke's `Published_Papers/` in sessions 11 and 12 but applied to a course page
  rather than an author page. Channels that worked first try: a **Kellogg faculty page** served the
  typeset *Journal of Finance* article; a **PhD-course mirror on a business-school server**
  (`bauer.uh.edu/rsusmel/phd/`) served the typeset *JFE* article complete with journal header and
  pagination; and an **S3 offload bucket behind a university faculty WordPress site**
  (`spinup-…-wp-offload-media.s3.amazonaws.com/faculty/…`) served an 88-page AQR working paper that
  SSRN would have refused — a host pattern worth remembering, since the faculty page linking it is
  indexed but the bucket is where the file actually lives. Limits hit, all as documented and two of
  them hard: **OpenAlex's daily budget was exhausted before the session's first query**
  (`Insufficient budget`), and **Semantic Scholar's title-search endpoint returned 429 on four
  consecutive attempts spread across the session** while its DOI endpoint answered every DOI lookup
  it was given, including — for the third time in four sessions the exception rather than the rule —
  a *Journal of Finance* DOI. One index consequence to record: **Almgren–Thum–Hauptmann–Li 2005 has
  no registered DOI** (*Risk* magazine does not assign them for that vintage), Crossref finds it under
  neither DOI nor bibliographic query, and with both remaining indices unavailable it is recorded as
  `citations: not indexed by any channel reachable this session` rather than estimated. Per the rubric
  that is not on its own grounds to downgrade; its tier rests on venue, sample and the independent
  confirmation of its central claim. Also worth noting for the "disbelieve a lone low count" list in
  the *opposite* direction from usual: for both 2004 articles here, **Semantic Scholar's count exceeds
  Crossref's by roughly a third** (684 vs 502; 611 vs 461), which is the normal relationship and is
  recorded so the several sessions of Crossref-over-Semantic-Scholar anomalies are not read as a rule.

  **Session 13 (2026-08-26) read full text directly for four of its five sources**; the fifth is
  recorded from its abstract. The session's access lesson is that **a citing paper's reference list is
  a search channel, not just a bibliography** — the source that turned out to be the session's best
  counterweight (Stambaugh) was found only because a targeted web search for a *different*, closed
  paper surfaced a Berkeley Haas-hosted working paper that cites it, and that working paper was itself
  the source. Channels that worked first try: a **university faculty FTP-style directory**
  (`terpconnect.umd.edu/~wermers/ftpsite/`) served a 1992 RFS article complete with journal header and
  pagination; **arXiv q-fin** again carried the full content of a JPM article; an **author's own
  department page** (`biz.uiowa.edu/faculty/<name>/`) served the accepted version of an FAJ article;
  and a **plain document-mirror host** served the JFE accepted manuscript when the publisher and SSRN
  would not. Limits hit, all as documented: **Semantic Scholar's DOI endpoint returned 429 on the
  fifth consecutive call** and does not resolve `10.1111/j.1540-6261.1995.tb04039.x` (a 300-citation
  1995 *Journal of Finance* article) — a third consecutive session in which a JF DOI misses in
  Semantic Scholar, so the session-12 rule stands: **for a Journal of Finance DOI, go to Crossref
  first**. A **BYU ScholarsArchive** link advertised by Semantic Scholar's own `openAccessPdf` field
  returned **403** with an HTML body, which is worth remembering — an index's OA link is a claim, not a
  guarantee, and `file` on the download catches it. One new index anomaly for the "disbelieve a lone
  low count" list, this time in the opposite direction from the usual: **OpenAlex reports 1 citation**
  for the 2009 JPM article against Crossref's 19. Two sources are recorded as **not read** rather than
  summarised from abstracts beyond what is flagged: Bessembinder et al. 2023 (FAJ, global) is
  `oa_status: closed` with no repository copy, and Brown–Goetzmann–Ross 1995 is likewise closed and is
  used only at the level of its published abstract, marked as such in both the note and this file.

  **Session 12 (2026-08-25) read full text directly for every primary source**, and the session's
  access lesson is that **an author's or department's own technical-report series is the reliable
  route to a closed-access statistics journal article**. Concretely: the Biometrika paper is
  `oa_status: closed` in OpenAlex with no repository copy listed, and its authors' own publications
  page does not link it — but a web search surfaced `stat.cmu.edu/tr/tr811/tr811.html`, whose sole
  content link (`tr811.pdf`) is the full 31-page working version including both theorems and their
  proofs. The generalisation worth adding to the recipe: when a paper is closed and the author page
  fails, **try the department's numbered technical-report series before concluding it is unobtainable**
  — it is a different host from the author page and is indexed separately. Also confirmed: **arXiv
  reprints of Institute of Mathematical Statistics journals** carry the full typeset article with
  volume and page headers (the *Statistical Science* review), a **university green-OA research portal**
  served the CC-BY published version of a paywalled *Journal of Finance* article complete
  (`research-api.cbs.dk/ws/portalfiles/…`, the fastest route found so far to a recent JF paper), and
  the **Duke `Published_Papers/` directory** worked first try again, as it did in session 11. Index
  behaviour, and it is now a pattern rather than an anomaly: **Semantic Scholar's DOI endpoint failed
  to resolve both `10.1111/jofi.12530` and `10.1111/jofi.13249`** — two of the most-cited papers in
  the field, in the field's top journal — while resolving a 2006 Biometrika DOI and a 2009
  *Statistical Science* DOI on the first try. Combined with session 11's `hhv059` failure, the working
  rule is now: **for a Journal of Finance DOI, go to Crossref first and do not treat a Semantic
  Scholar miss as evidence the paper is unindexed.** Crossref answered every lookup this session.

  **Session 11 (2026-08-24) read full text directly for five of its six sources** and in part for the
  sixth. Channels that worked first try: **university department PDF mirrors of published journal
  articles** (`econ.uzh.ch/dam/jcr:…` served the typeset *Journal of Empirical Finance* article
  complete with volume and page headers, after the author's own `ledoit.net` copy failed to
  download and the older `wp_iew` working-paper path 404'd), an **author's personal site**
  (`davidhbailey.com/dhbpapers/`, which serves the SSRN-stamped versions of both López de Prado
  papers), and a **faculty directory listing** — when a guessed filename 404'd, fetching the parent
  `Published_Papers/` directory and grepping its `href`s found the correct one immediately, which is
  a faster route than another search and worth adding to the recipe. Limits hit, all documented:
  **ams.org returned 403** on the Notices PDF (the paper containing the formal backtest-overfitting
  proof is therefore recorded as **unread**, with the two claims that depend on it flagged
  second-hand), and **Semantic Scholar's rate limit bit on the third consecutive call** while its DOI
  endpoint stayed reliable when calls were spaced by several seconds. Index behaviour: `hhv059`
  resolves in **neither Semantic Scholar** (the DOI endpoint returns "not found" for a
  2,000-citation RFS article) nor usefully in OpenAlex's default path, and `10.21314/jcf.2016.322`
  returns **`cited_by_count: 0`** from OpenAlex against Crossref's 51 — a fifth and sixth instance of
  session 7's "disbelieve a lone low count", this time with a *zero* and a *not-found* as the tells.
  Crossref's `query.bibliographic` search again resolved both. One methodological note worth keeping:
  two sources whose primary text could not be read (Jobson–Korkie, Memmel) were recovered by finding
  **two independent restatements of their formula** that agree algebraically, which is a better
  standard than a single second-hand summary and is how the closed form in this session's top
  candidate was verified before use.

  **Session 10 (2026-08-23) read full text directly for every primary source**, and the session's
  access lesson is that **course-page and reading-list mirrors are now the most reliable channel for
  paywalled journal articles**, ahead of author pages. Concretely: the FAJ article was 404 on the
  author's own MIT page but served complete, with AIMR pagination and copyright line intact, from a
  university student-organisation reading list; the World Scientific handbook chapter served from a
  UC Berkeley course page. Also confirmed working — **EuropePMC's `?pdf=render` endpoint**, which is
  the fix when a PNAS scan of a pre-1980 article extracts as empty text (the publisher's own
  `pnas.org/doi/pdf` path returned 403 and the alternative mirror was an image-only scan yielding 4
  characters); and **MIT DSpace**, which 429s on first request and succeeds on a retry a few seconds
  later, redirecting to a signed CDN URL. Index behaviour: Semantic Scholar's DOI endpoint answered
  every lookup on first try, but its record for a 1974 JFE article reports **year 2017** and a
  citation count of 70, which for a paper of that vintage and venue is a visible undercount — a
  fourth instance of session 7's "disbelieve a lone low count" warning, this time with a corrupted
  year field as the tell. One DOI guessed from a journal-name search resolved in neither Semantic
  Scholar nor Crossref; a Crossref `query.bibliographic` search found the correct DOI immediately and
  is worth reaching for before concluding a paper is unindexed. Three sources relevant to this
  session's notes are **closed-access and recorded as unread or second-hand rather than summarised
  from abstracts**: Chopra–Ziemba 1993 (JPM) and MacLean–Ziemba–Blazenko 1992 (Management Science),
  whose tables are reproduced verbatim in a text that *was* read and are flagged in-note as
  second-hand, and Grossman–Zhou 1993 (Mathematical Finance), which is cited nowhere in the notes.

  **Session 9 (2026-08-22) read full text directly for every source**, and hit none of the three
  documented limits — Semantic Scholar's DOI endpoint and Crossref both answered every lookup on
  first try, and OpenAlex answered the one query it was asked. Two channels worked and are worth
  adding to the reliable list: an **author's firm-hosted PDF** (`intechinvestments.com`) served a
  full Elsevier handbook chapter that the publisher endpoint would have refused, and a **university
  green-OA repository** (`openaccess.city.ac.uk`, found via Semantic Scholar's `openAccessPdf`
  field) served the accepted version of a Wiley article. `arxiv.org/pdf/<id>` served a preprint
  carrying the full content of a PNAS article. Limits confirmed as documented: **SSRN returned 403**
  on its delivery endpoint, and a UC3M author page returned 403 on directory listing. One source
  could not be obtained by any route tried — DeMiguel–Garlappi–Nogales–Uppal 2009 (Management
  Science) is `oa_status: closed` in OpenAlex with no repository copy, and Semantic Scholar's
  `openAccessPdf` for it points back at SSRN — so it is recorded as **unread** in the note that
  cites it rather than summarised from abstracts. One metadata note: Crossref's
  `is-referenced-by-count` again ran well below Semantic Scholar's for the same DOIs (389 vs 578;
  71 vs 220), consistent with session 7's warning to disbelieve a lone low count.

  **Session 8 (2026-08-21) read full text directly for every source**, and hit two of the three
  documented limits within the same hour. Channels that worked first try: **NBER working-paper
  PDFs** again (Jagannathan–Ma's w8922 carries the full published argument and both
  propositions), **arXiv q-fin/physics preprints** of published FAJ and practitioner-journal
  articles (Willenbrock's arXiv copy carries the FAJ volume/page header; Polakow–Gebbie's
  preprint predates the *Journal of Asset Management* version), and a **conference-site mirror**
  (`top1000funds.com`) that served the SSRN version of a *Risk* article whose SSRN and
  university-hosted copies both returned 403. That mirror channel is new and worth remembering:
  when SSRN and an institutional PDF both refuse, a practitioner conference or investor-education
  site has often re-hosted the same file. Limits hit: **OpenAlex's daily budget was already
  exhausted** at the start of the session (`Insufficient budget`), and **Semantic Scholar's title
  search returned 429 on every attempt** while its DOI endpoint stayed reliable throughout — so
  one source (Meucci 2009, a *Risk* magazine article whose only DOI is its SSRN preprint's)
  resolves in **no index at all** and is recorded as unindexed rather than estimated. Per the
  rubric that is not on its own grounds to downgrade, but the note is tier C anyway on venue and
  sample. Two closed-access sources relevant to a standing open question (Grinold–Kahn 2000 FAJ;
  Clarke–de Silva–Sapra 2004 JPM) could not be read beyond a CFA Digest summary, and are recorded
  as unread rather than summarised second-hand.

  **Session 7 (2026-08-20) read full text directly for every source**, and hit none of the three
  documented limits. Three channels worked first try and are worth adding to the README's reliable
  list: **NBER working-paper PDFs** (`nber.org/system/files/working_papers/wNNNNN/wNNNNN.pdf`) for
  the working-paper versions of two published tier-1 articles; **institutional green-OA
  repositories** — an LBS Research Online PDF served the full published RFS article that
  ScienceDirect-style publisher endpoints would have refused, and OpenAlex's `open_access.oa_url`
  field is the fastest way to find one; and **arXiv PDFs** for a recent working-paper version. One
  index anomaly to record: for `10.1093/rfs/hhz085`, **Semantic Scholar's DOI endpoint returns 24
  citations while OpenAlex returns 193 and Crossref 177** — a clear undercount, not a low-impact
  paper. The rubric's "try both indices" advice should be read as "and disbelieve a lone low count
  that disagrees with the venue". Separately, a very recently published critique
  (`10.1093/rapstu/raae006`) resolves in **neither** Semantic Scholar nor, usefully, anywhere but
  Crossref, whose `is-referenced-by-count` is 0; recorded in-note as provisional weight rather than
  used to downgrade or inflate the source.

  **Session 6 (2026-08-19)** read full text directly for Breiman (author-hosted Berkeley tech
  report), Buja–Stuetzle (author-hosted Wharton PDF), Hansen (author-hosted Wisconsin PDF) and
  the fundamental-law derivation (an author's working paper mirrored on a university page), and
  only the first two pages of the published Ding–Martin. Three access notes to add to the
  README's list: **Project Euclid** serves a bot challenge like SSRN (so Bühlmann–Yu was
  unreadable and its result is recorded second-hand, flagged in-note); **eScholarship** returns
  403 to an automated client even for green open-access copies; and a **CC-BY open-access
  Elsevier article is still unreachable** through ScienceDirect, which 403s the PDF endpoint
  Unpaywall points at — the workaround that succeeded was a `pdfs.semanticscholar.org` mirror,
  which carried only the article's first pages. Author-hosted PDFs remain the reliable channel.
  Both index limits bit in the same session: **OpenAlex's daily budget was exhausted**
  (`Insufficient budget`, resets midnight UTC) and **Semantic Scholar's title-search endpoint
  429'd repeatedly** while its DOI endpoint stayed reliable; one source (Ding–Martin) resolves
  in **neither** index and its count is recorded from Crossref's `is-referenced-by-count`, a
  third fallback worth adding to the rubric's list. One source (Buja–Stuetzle) has **no
  registered DOI** and was resolved only by title search.

  **Session 5 (2026-08-18) also read full text for every source**, and added one practical
  finding now written into `research/README.md`: `WebFetch` cannot parse PDFs (it returns the
  binary and says so), and `Read`'s PDF path needs `pdftoppm`, which is absent. The working
  recipe — `pip install --target` a scratchpad copy of `pypdf`, extract to `.txt`, and decode
  the literal `/xHH` escapes some LaTeX PDFs produce — is in the README's network section.
  Author-hosted PDFs (NBER, AQR, `mysimon.rochester.edu`, `thierry-roncalli.com`) all served
  cleanly; SSRN and ScienceDirect again did not. One citation count (Novy-Marx–Velikov 2022)
  resolved on OpenAlex but not on Semantic Scholar's DOI endpoint, so both indices remain worth
  trying before recording a source as unindexed.

  **Session 4 (2026-08-17) is the first session in which full text was read directly for every
  source**, via NBER/author-hosted PDFs, and the three limits above all behaved as documented
  (SSRN and the Arizona repository returned 403 bot challenges; Semantic Scholar's DOI endpoint
  and OpenAlex both worked). One session-4 source, Lehmann (1990), resolved only as a scanned
  image PDF with no extractable text; its claims in that note are attributed to its published
  abstract and flagged in-note as second-hand rather than silently upgraded.

  **Citation counts have been backfilled** for all notes as of 2026-08-17 and are no longer
  the folder-wide gap they were. Two residual gaps from the restricted era remain and still
  warrant a re-check against full text before anything leans on them: (a) sample periods are
  recorded as unverified where the abstract did not state them (Rapach–Strauss–Zhou's exact span,
  Zakamulin's sample, the Hoffstein sample end that drives its `validation_overlap` flag); and
  (b) one quantitative detail — whether the tranching 1/N factor applies to the timing-luck
  standard deviation or its variance — is flagged as unconfirmed in its note. Nothing was ever
  estimated from memory to fill these gaps. The one tier consequence the backfill did surface:
  the rebalance-timing-luck note is now the weakest-evidenced source here (tier-3 venue, 4
  citations, JII article unindexed) and is flagged in-note as a candidate for tier C.
