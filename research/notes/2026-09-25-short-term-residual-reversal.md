---
title: "Short-Term Residual Reversal"
authors: Blitz, Huij, Lansdorp, Verbeek
year: 2013
venue: Journal of Financial Markets 16(3), 477–504 — Tier 1 (peer-reviewed field journal)
url: https://doi.org/10.1016/j.finmar.2012.10.005
citations: 41 (Crossref, JFM DOI, checked 2026-09-25); 35 (Semantic Scholar, which indexes only the SSRN preprint record `10.2139/ssrn.1911449`, checked 2026-09-25)
sample_period: 1926–2008 (the trading-cost analysis is run on the 1990–2008 subsample only, because the cost model's parameters are estimated from 1991–1993 institutional data)
markets: US common stocks (NYSE/AMEX/Nasdaq) above the NYSE median market cap; robustness on the 500 and 100 largest names
tier: B
validation_overlap: false
published_post_2018: false
---

**Text read**: the EFMA-symposium working-paper version, in full, from
`http://www.efmaefm.org/0EFMSYMPOSIUM/2012/papers/017_update.pdf` (47 pages: the analytics of
Section 2, the empirical design, the cost model, the double sorts and the tables). The published
JFM article was not read — Elsevier's endpoint is closed to an automated client — so anything
below that depends on a *number* is stated qualitatively, and the algebra is the working paper's
own. Note the author list: Semantic Scholar and several search snippets give the fourth author as
van Vliet; Crossref, RePub and the paper's own title page give **Verbeek**.

## Mechanism

The paper's contribution is **analytic, not empirical**, and the analytic part is what transfers.

Take the textbook contrarian weight (Lehmann 1990; Lo–MacKinlay 1990 — see
`notes/2026-09-05-contrarian-profit-decomposition.md` for the profit identity):

```
w_i,t = -(1/N) * ( r_i,t-1 - r_bar_t-1 )
```

Assume a K-factor return model `r_i = mu_i + sum_k beta_i^k f_t^k + eps_i,t` with `f` the factor
return in excess of its own expectation. Then the book's **expected loading on factor j**,
conditional on what factor j did in the formation period, is

```
E[ sum_i w_i,t beta_i^j | f_t-1^j ]  =  - sigma2_beta^j * ( mu^j + f_t-1^j )
```

where `sigma2_beta^j` is the **cross-sectional variance of the loadings** on factor j. Two
readings, and both are mechanisms rather than findings:

1. **A static leg.** A contrarian book is *unconditionally* short every factor that carries a
   positive expected return, in proportion to how dispersed the universe's loadings on it are.
   Nothing about reversal causes this; it falls out of sorting on total return.
2. **A dynamic leg.** The book's loading on factor j moves one-for-one with **minus** the
   factor's demeaned return over the formation window. When the market rose last month, high-beta
   names were mechanically the winners, the contrarian rule sells them, and the book carries a
   *negative* market beta into the next month. A conventional short-term reversal strategy is
   therefore a **factor-timing bet the researcher did not choose**, re-struck every rebalance,
   with size set by `sigma2_beta`.

The same algebra says what the variance of reversal profits is driven by: more extreme lagged
factor returns and more dispersed loadings both raise it. So the dynamic leg adds risk as well as
an unintended bet.

The fix is to sort on the **residual** instead. With `w_i,t = -(1/N)(eps_i,t-1 - eps_bar_t-1)`
the loading on every modelled factor is **zero by construction**, because the residuals are
orthogonal to the factors by the definition of the fitting regression. The claim is not that
residual returns revert more strongly than total returns; it is that the residual sort *isolates*
reversal while the total-return sort bundles it with a factor-timing overlay and a volatility
tilt.

A second, separable mechanism explains **which names reach the extreme buckets**. Sorting on raw
past return, the probability of landing in the top or bottom decile rises with a name's
volatility, because a volatile name's monthly return is a draw from a wider distribution. The
extreme deciles of a conventional reversal sort are therefore systematically the more volatile,
smaller, lower-priced names — a *selection* effect, not a signal. Standardising each residual by
its own trailing residual volatility removes it, and the paper reports that the residual sort's
extreme deciles do not show the volatility/size/price tilt that the conventional sort's do.

## Construction recipe

Monthly, with monthly returns throughout:

1. For each name, estimate factor loadings by OLS over the **preceding 36 months `[t-36, t-1]`**
   on the chosen factor set (they use Fama–French 3; the algebra is agnostic about which factors).
   Names must have a complete 36-month history to be included.
2. The **signal is the residual of the most recent month**, `eps_i,t-1`, from that regression.
3. **Standardise**: divide the residual by the standard deviation of that name's residuals over
   the same preceding 36 months. (The paper states the conclusions are not materially affected by
   the standardisation, so treat it as a second, separable node rather than part of the signal.)
4. Sort into deciles; long the lowest standardised-residual decile, short the highest;
   **equal-weighted**; rebalance monthly.
5. **Skip-day variant**: drop the first trading day of the new month from the holding period.
   This is the standard defence against bid-ask bounce and non-synchronous pricing contaminating
   a one-month-formation reversal, and it costs a meaningful part of the gross spread.
6. Cost model: Keim–Madhavan (1997), which prices buy- and sell-initiated orders separately as a
   function of log size, log price and a Nasdaq dummy, and includes commission plus price impact.

Construction facts worth carrying (not performance figures): the monthly turnover of both the
conventional and the residual decile books is on the order of **160–180% per month**, i.e. the
two constructions are equally expensive to run, so any difference between them is a difference in
gross signal rather than in trading intensity.

Two diagnostics the paper runs that are cheap to re-run anywhere:

- **Double sort.** Sort into quintiles on total return, then within each into quintiles on
  residual return, and then the reverse. The paper's finding is directional and qualitative:
  residual return retains its ordering inside every total-return quintile, while total return
  loses its ordering once residual return is controlled for. If that holds, the residual signal
  *subsumes* the raw one rather than complementing it — which is a claim about redundancy, not
  about size.
- **Industry version.** Rank on total and on residual return *within* each of ten industries, to
  check the residualisation is doing more than an industry demean.

## Robustness evidence (qualitative only)

- Multi-decade US sample, and the design is checked on progressively narrower large-cap subsets
  (above-median, 500 largest, 100 largest) rather than only on the full cross-section — the
  direction of the result is reported as surviving that narrowing, which matters for a lab whose
  universe is ~145 very large names.
- The costed comparison is honest in shape: both books are priced with the same model, the
  break-even cost level is reported for each, and the skip-day variant is shown alongside. The
  authors' own summary is that the conventional book does not survive costs on the broad
  cross-section while the residual book does by a wide margin; the *relative* ordering, not any
  number, is what is recorded here.
- **Single market, single research group, no independent replication under this name.** It is
  not in Hou–Xue–Zhang's sweep and does not appear in Jensen–Kelly–Pedersen's factor set under
  this construction. Its sibling result — *residual momentum* (Blitz, Huij, Martens 2011) — has
  been replicated more widely and this folder already holds it
  (`notes/2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md`).
- Multiple testing is **not** addressed. The paper tests one construction against one benchmark,
  which is the cheap case, but there is no accounting for the search that produced the 36-month
  window or the standardisation.
- Tiered **B**, not A, on exactly those two gaps (one market, no replication), not on the venue
  or the analytics, which are sound and checkable by hand.

## Implementability here

**In scope, cheaply.** Everything needed is daily USD closes: compound to monthly, regress on a
factor set the repo can build (market = equal- or cap-weighted universe return; PCA factors from
the correlation matrix; the repo's own seated `E/Var` neighbourhood construction is a related
"mimicking portfolio" idea), take the last month's residual, standardise by 36-month residual
volatility, rank.

**The long-only problem, stated precisely.** The paper's book is zero-investment and its whole
point is that the *factor loading is zero by construction*. A fully-invested long-only book
cannot reproduce that: the weights sum to one, so the market leg is always held, and the
`sigma2_beta * (mu^j + f^j)` term survives on whatever the long-only weights' loading happens to
be. What a long-only book **can** keep is the second mechanism — the *selection* fix. Sorting on
standardised residuals rather than raw returns changes **which names are held**, and that part is
fully available under the constraint. So the transferable claim here is narrow and should be
written that way in a hypothesis line: *residualising changes the membership of the held set away
from the high-volatility tail; it does not deliver factor neutrality in a long-only book.*

**The tension with this lab's own measurement, which is the reason this note exists.**
`experiments/learnings.md` [2026-08-30] records the family's premise tested directly and refuted
in the wrong direction: on 5-day reversal, **raw** beat one-factor residual beat PCA k=3 ≈ PCA
k=5 (IC +0.0455 → +0.0375 → +0.0331 / +0.0336), monotone in the amount of structure removed. This
source says the opposite about monthly reversal. Four differences, in the order a session should
check them:

1. **Horizon.** The lab measured a 5-day signal; this paper's is a one-month formation with a
   36-month estimation window. The lab's own finding is that its reversal effect decays to a null
   by 21 days — so the two are not measuring the same object, and the monthly version may simply
   be absent on this universe. This is the cheapest thing to check and the most likely resolution.
2. **Standardisation.** The lab residualised but (per the learnings entry) did not divide by
   trailing residual volatility. That step is where the *selection* mechanism lives, and it is the
   only part of this construction that is reachable long-only. A residualisation without it keeps
   the volatility tilt in the extreme buckets while removing the factor signal — plausibly the
   worst of both.
3. **And this is the sharp one: on this universe the tilt the paper removes is a tilt the lab has
   measured as paying.** `learnings.md` records a high-minus-low volatility spread of **+19.4%/yr
   on train** as this universe's survivorship bias observed directly. A raw reversal sort loads on
   volatility by the selection mechanism above; residualising and standardising removes that load.
   **So "residualising hurts" is exactly what you would predict here if the raw sort's edge were
   the survivorship artifact rather than reversal.** That is a testable reconciliation, not a
   defence of either side: the prediction is that the raw-minus-residual IC gap should shrink or
   vanish once the comparison is run *within* volatility buckets, and should not shrink if the gap
   is real reversal. Run it on train, free, no trial.
4. **Factor set.** PCA k ∈ {1,3,5} on ~140 names is a different object from FF3 on thousands.
   `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` already records that the
   lab's tested range sits inside the region Avellaneda–Lee also found worst.

**Pitfalls.** (i) 36 months of monthly data is 36 observations per regression — the loadings are
noisy, and on a 140-name universe with 15 regions the FF3 analogue does not exist; use the repo's
own factors and say so. (ii) The skip-day step is not optional here for the wrong reason: the
engine already imposes a 1-day execution lag, which supplies roughly the same protection, so do
not stack a second skip on top without checking what it removes. (iii) Monthly turnover near 170%
at 15 bps/side is ~25 bps/month of cost, which is a large fraction of any plausible monthly edge —
the long-only version is much cheaper (one leg, and membership changes rather than reversals), and
that asymmetry should be priced before the trial, not after.

## Related

- `notes/2026-09-05-contrarian-profit-decomposition.md` — Lo–MacKinlay's identity. This paper's
  Equation (3) is the *loading* analogue of that profit decomposition: same weight vector, one
  asks what the book earns, the other what it is exposed to.
- `notes/2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — the same
  residualisation operator at the momentum horizon, by an overlapping author group.
- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` — Avellaneda–Lee; the factor
  count question, and the lab's declined screen.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — the competing mechanism, and
  the reason a 15-bps-a-side book is on the wrong side of the reversal premium.
- `experiments/learnings.md` [2026-08-30] — the refutation this note is in tension with, and the
  +19.4%/yr volatility spread that supplies the reconciliation hypothesis.
