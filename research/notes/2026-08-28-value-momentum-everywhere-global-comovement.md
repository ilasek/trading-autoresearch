---
title: "Value and Momentum Everywhere"
authors: Asness, Moskowitz, Pedersen
year: 2013
venue: The Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/jofi.12021
citations: 2078 (Crossref `is-referenced-by-count`, checked 2026-08-28); 2041 (Semantic Scholar DOI endpoint, same date) — the two indices agree closely here, which is the exception in this folder's experience
sample_period: January 1972 – July 2011 (Europe and Japan stocks from 1974; all 27 commodities available after 1995)
markets: four equity markets (US, UK, continental Europe, Japan) restricted to the largest names accounting for 90% of each market's cap, plus 18 country equity index futures, currencies, government bonds and commodity futures
tier: A
validation_overlap: false
published_post_2018: false
read: full text, typeset Journal of Finance article with volume and page headers (`pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf`)
---

## Mechanism

The paper's thesis is a **correlation structure**, not a premium: value in any one market is
positively correlated with value everywhere else, momentum with momentum everywhere else, and
value with momentum negatively — within and across asset classes — and this structure is
*stronger than the correlation of passive exposures to those same asset classes*. Since the
strategies are market-neutral within each class, that co-movement cannot be the assets moving
together; it points at common global factors that the strategies load on.

On the source of that structure: macroeconomic links (business cycle, consumption, default risk)
are modest at best. **Liquidity risk** loads positively on momentum and negatively on value
globally, and the primary link is **funding** rather than market liquidity — consistent with a
story in which levered arbitrageurs unwind positions when funding tightens, hitting the crowded
recent-winner book and helping the value book. The authors are scrupulous about the size of this
explanation: liquidity risk accounts for only a small fraction of the premia and co-movement, an
equal-weighted value+momentum combination is essentially immune to it, and value's premium
becomes a *deeper* puzzle under it, not a shallower one. The honest summary is that the common
factor is documented and only partially explained.

Two methodological points from the paper are mechanism-level and matter here more than the
finance:

- The correlation structure is **only visible across many markets at once**. Single-market
  analysis lacks the power to reveal these factor exposures. The authors repeat the theme:
  average the return series first, then correlate — averaging diversifies the market-specific
  noise that hides the common component.
- The structure is **not a prediction of the standard behavioural models** (DHS, BSV,
  Hong–Stein), which are about single-market investor psychology. It is the strongest available
  argument for treating momentum as a compensated exposure rather than a pure mispricing.

## Construction recipe

- **Universe filter, and it is the interesting one.** In each equity market, stocks are ranked by
  beginning-of-month market cap and the universe is the names that cumulatively account for
  **90% of total market capitalisation** — on average the largest 13–26% of firms per market,
  a few hundred to ~700 names in the US. The stated purpose is a liquid, tradeable, low-cost
  set comparable to the futures and currency legs. This is very close in spirit to how this
  repo's ~145-instrument global universe is drawn.
- **Momentum signal**: cumulative return over the past 12 months **skipping the most recent
  month** (`MOM2–12`), identically across all eight asset classes. The skip is applied even where
  microstructure reversal is not a concern (index futures, currencies), purely for uniformity.
  The authors note Novy-Marx's 7-12 alternative and state the difference is negligible in US
  stocks, and that they prefer `MOM2–12` as the established out-of-sample-tested measure.
- **Value signal for non-equity classes, and as an equity robustness check: the negative of the
  past 5-year return.** For assets with no book value this is the value proxy, and in equities it
  produces a value strategy correlating with momentum at roughly −0.48, close to what BE/ME gives
  (−0.53). Lagging the price in BE/ME by a year so the two signals share no price data still
  leaves them negatively correlated (≈ −0.28). Long-horizon reversal and book-to-market are
  measuring much the same thing.
- **Portfolio weights**: securities are weighted in proportion to their **cross-sectional rank**
  of the signal minus the average rank, scaled to one dollar long and one dollar short. Ranks
  rather than raw signals are used to blunt outliers; the authors state raw-signal weights give
  similar and slightly better results. They also report that these signal-weighted portfolios
  **outperform coarse tercile-sort spreads**, for two stated reasons: weights are a positive
  linear function of the signal rather than a three-way classification, and more securities carry
  nonzero weight so the book is better diversified.
- **Rebalance**: monthly; rebalancing back to equal weights annually rather than monthly gives
  similar results for the non-stock legs.
- **Combining across markets**: strategies are built **within** each market or asset class and
  then averaged across them, weighted by inverse in-sample volatility for the multi-class
  composite. Again: rank locally, combine globally.
- **Currency**: all returns denominated in USD.

## Robustness evidence (qualitative only)

- Nearly four decades, eight markets and asset classes on three continents, with value and
  momentum defined uniformly rather than tuned per market — the authors state explicitly that
  they use the most standard measures rather than the best predictors, to minimise data snooping,
  and that this likely *understates* achievable gross returns.
- **Momentum co-moves strongly across equity markets**: the average single-market stock momentum
  strategy correlates ≈ 0.65 with the average momentum strategy in the *other* stock markets, and
  ≈ 0.37 with the average momentum strategy in non-stock asset classes. Value shows the same
  pattern (≈ 0.68 across stock markets). Value and momentum are negatively correlated everywhere:
  ≈ −0.53 between a stock market's value strategy and other stock markets' momentum, and −0.13 to
  −0.28 across the various stock/non-stock combinations. Correlations are computed on quarterly
  returns to blunt non-synchronous trading across time zones, and joint significance is tested.
- The paper is candid that its universe restriction makes it **conservative**: value and momentum
  premia are larger among smaller and less liquid securities over the sample studied.
- Costs are not modelled — these are gross factor returns on a deliberately liquid universe. The
  authors' defence of implementability is the universe filter, not a cost model.
- Replication status: this is one of the most-cited papers in the modern factor literature and
  its momentum result is the same effect Jensen–Kelly–Pedersen and Hou–Xue–Zhang adjudicate
  elsewhere; its *distinctive* contribution — the cross-asset correlation structure — is much
  less independently replicated than the premia themselves, and the funding-liquidity link is the
  weakest-supported part by the authors' own accounting.

## Implementability here

- **The result with the sharpest consequence for this repo is the cross-market momentum
  correlation.** Geography does not diversify a momentum book. If single-market momentum
  strategies correlate ≈ 0.65 with momentum elsewhere, then spreading a momentum basket across
  regions adds names but not much independent risk — which is the portfolio-level version of the
  fundamental-law point already in this folder: `N` counts nominal bets, not independent ones. It
  also explains, without any appeal to the lab's own data, why the lab measured that widening the
  basket from 25/15 to 35/20 left maximum drawdown essentially unchanged. **A global momentum
  book has one dominant common factor, and adding global names does not dilute it.**
- **This is the folder's first outside support for magnitude weighting, and it is support with a
  correction.** The lab's largest single Sharpe gain came from weighting by signal magnitude, and
  `learnings.md` later concluded the information in it is "more ordinal than cardinal". This
  paper independently weights by **cross-sectional rank of the signal** — ordinal magnitude
  weighting, exactly — states that it does so to control outliers, and reports that rank-weighted
  books beat coarse sort spreads both because the weight is a linear function of the signal and
  because more names carry weight. The lab's mechanism and the lab's own refinement of it are
  both the published construction. Note the boundary: their portfolios are dollar-neutral
  long-short, so "rank minus average rank" produces negative weights; the long-only analogue is
  the champion's, and the equivalence is the lab's inference, not the source's.
- **A genuinely new build idea, and it is price-only.** The negative of the **past 5-year return**
  is a value signal that requires nothing but daily closes, is used as such in this paper for
  every non-equity class and validated against BE/ME in equities, and is **negatively correlated
  with momentum** (≈ −0.5) by construction and in measurement. This repo has no fundamentals and
  has therefore never had a value signal; it now has one it can compute. Three caveats before
  anyone builds it: (i) it is long-short evidence, so candidate #4's screen applies and the
  long-only half is the weaker half; (ii) candidate #2's design test says a value sleeve blended
  with a momentum sleeve is *mixing different return streams*, not averaging estimates of one
  quantity, so it pays the capital-dilution tax the lab has already measured — the negative
  correlation is what would have to beat that tax, and the tax is known and the correlation is
  not measured here; (iii) a 5-year lookback on a survivorship-conditioned universe is the
  construction most exposed to the folder's own survivorship notes, because a name that fell 80%
  five years ago and is still in today's universe is a selected survivor.
- **Universe comparability is unusually good.** Their equity universe (largest names covering 90%
  of market cap, a few hundred per market, explicitly chosen for tradeability at 15-bps-ish cost
  levels) is closer to this repo's ~145 global large caps than anything else in this folder. That
  makes their *conservatism* statement the most directly applicable version of the size discount:
  a large-liquid universe understates the premia in the broader academic samples.
- **What does not transfer**: the funding-liquidity factor (no funding-spread data here, and the
  authors say it explains little anyway), the multi-asset-class breadth (this repo has ETFs, not
  futures, and cannot short), and inverse-volatility weighting across sleeves, which the lab has
  refuted twice and which candidate #1's second half rules out on comparable-Sharpe grounds.

## Related

- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the breadth machinery this
  note's correlation result feeds directly; ≈0.65 cross-market momentum correlation is a
  quantitative bound on how much geography can raise effective `N`.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the same question
  measured from holdings rather than from published correlations.
- `notes/2026-08-28-local-versus-global-factor-construction.md` — the rank-locally-combine-globally
  construction, reached independently.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — the *short*-horizon reversal
  family the lab closed; the 5-year reversal signal here is a different horizon and a different
  mechanism, and should not be filed under family 4.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — why the 5-year
  lookback is the signal most exposed to this repo's permanent universe caveat.
