---
title: "The Common Factor in Idiosyncratic Volatility (CIV) — a factor structure in what is left over after the factors"
authors: Herskovic, Kelly, Lustig, Van Nieuwerburgh
year: 2016
venue: Journal of Financial Economics 119(2), 249–283 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2015.09.010
citations: 344 (Semantic Scholar by DOI, checked 2026-10-06); 438 (OpenAlex by DOI, same date); 381 (Crossref `is-referenced-by-count`, same date)
sample_period: 1926–2010 for the volatility facts; January 1963 – December 2010 for the pricing tests; 1975–2010 for the cash-flow-volatility panel; 1978–2011 for the household-income comparison
markets: United States only — more than 20,000 CRSP common stocks (share codes 10/11/12), with CRSP/Compustat for fundamentals
tier: B
validation_overlap: false
published_post_2018: false
read: full text of NBER Working Paper 20076 (April 2014, revised December 2014) from `nber.org/system/files/working_papers/w20076/w20076.pdf`, served first try, parsed cleanly with `pdftotext -layout` (217 KB, `( )` grep clean, display equations intact). The published JFE version was not fetched (Elsevier is closed to this client as `research/README.md` records); the working paper's abstract and the published abstract agree on all three headline claims used below.
---

## Mechanism

**The empirical fact first, because it is the part that does not depend on believing the model.** Take
a panel of stocks, strip each one's returns of common factors by regression, and measure the volatility
of what is left. Those *idiosyncratic* volatilities — one per name per period — are supposed to be the
part that has nothing in common. They are not: they move together, strongly, and a **single factor
explains about a third of their time variation** across a very large and very long panel. The authors
call that factor **CIV**, common idiosyncratic volatility.

The obvious objection is that this is just an omitted factor: if returns load on a factor whose
volatility moves, residual volatility inherits it, and the "common" part of idiosyncratic volatility is
really a mis-specified factor model. **The paper closes that off and this is its best argument.** They
saturate the first-stage regression with up to ten principal components, verify the resulting residuals
are virtually uncorrelated across names, and find the residual volatilities *still* co-move exactly as
much. Co-movement in second moments survives the removal of co-movement in first moments, which is the
point: it is not a factor in returns, it is a factor in risk.

They then show the same factor structure in the volatility of firm **fundamentals** (quarterly sales
growth), with the fundamental and return volatility factors sharing a high correlation and the same
low-frequency shape — which rules out a pure discount-rate or sentiment story and locates the thing in
cash-flow risk.

**The economic mechanism, which is the paper's own theory and is why the sign is predicted rather than
fitted.** In an incomplete-markets model with heterogeneous households, households' consumption risk
inherits the factor structure of firms' idiosyncratic cash-flow risk — an entrepreneur or an
under-diversified employee bears their own firm's idiosyncratic shock, and if those shocks get more
volatile *together*, the cross-sectional dispersion of household consumption growth rises and the
average household's marginal utility rises with it. So **CIV is a priced state variable**, and the
price of CIV risk is **negative**: a stock that pays off when CIV rises is a hedge against bad times
for the average household, so it is expensive and earns a *low* average return. A stock that loses when
CIV rises is the opposite. The authors support the household link directly, reporting that CIV
innovations correlate with the dispersion of individual earnings growth from administrative data, with
employment growth, and with dispersion in wage and house-price growth.

**Which end pays, stated plainly because it decides whether this is reachable in a long-only lab.**
Average returns are **decreasing in CIV-beta**. The *lowest* CIV-beta names — those that fall when
common idiosyncratic volatility rises — are the **high-return** leg. A long-only book therefore holds
the profitable end directly, and the authors' long-short spread is negative precisely because the
reachable side is the long side. This is the same favourable asymmetry the folder recorded for the
`MAX` lottery sort and the opposite of the residual-reversion and lead-lag cases where only the cheap
side is tradeable.

## Construction recipe

Two objects: the factor, and the exposure to it.

**The factor, monthly version (this is the one their pricing tests use).**

1. For each name, each month, regress its **daily** excess returns on a factor set within the month
   and keep the residuals. Three first-stage specifications are used and all give qualitatively
   identical answers: (i) the market return alone, (ii) the three Fama–French factors, (iii) **the
   first five principal components of the cross-section of returns**, estimated within the same window.
   Ten PCs give quantitatively similar results; GARCH residuals change nothing.
2. **CIV_t = the equal-weighted cross-sectional average of firm-level residual return *variance* in
   month `t`.** Equal-weighted, and a variance rather than a standard deviation.
3. **CIV shocks = first differences of CIV.** The state variable that is priced is the innovation, not
   the level.
4. In parallel, **MV_t** = market variance from daily value-weighted market returns in the month, and
   **MV shocks** = its first differences. MV is carried through every test as the rival.

**The annual version** used for the long-sample volatility facts: idiosyncratic volatility is the
standard deviation of a name's daily residuals **within the calendar year**, with the factor model
re-estimated using only that year's observations. A firm-year enters only if the name has **no missing
daily returns in the year**.

**The exposure.**

5. For each month, regress each name's **monthly** excess returns on **CIV innovations and MV
   innovations jointly** over a **trailing 60-month window**. The coefficient on CIV innovations is the
   name's **CIV-beta**; the coefficient on MV innovations is its MV-beta. Including MV in the same
   regression is not optional — it is how CIV-beta is separated from plain market-variance exposure.
6. Sort into quintiles on CIV-beta each month, **equal-weight** within quintile, hold **one month**.
   Value-weighting gives similar results; they report equal-weighted throughout.
7. The controlled version, which produces larger spreads: sort first on MV-beta, then within each
   MV-beta quintile sort into CIV-beta groups, then collapse across the MV dimension — giving CIV-beta
   portfolios with essentially equal MV-betas.

**One useful distributional fact that makes the whole thing cheap**: the cross-sectional distribution
of estimated firm volatility is close to **lognormal**, so the entire cross-sectional distribution is
summarised by two numbers per period (the cross-sectional mean and standard deviation of *log*
volatility). It also means the averages above are not being driven by a few extreme names.

## Robustness evidence (qualitative only)

- **The volatility fact is very strong**: a very large panel, a sample spanning most of a century,
  present across size quintiles and across industry groups, and robust to the first-stage
  specification (market, FF3, 5 PCs, 10 PCs, GARCH residuals). The fundamentals corroboration is an
  independent data source pointing the same way. This part is Tier A quality.
- **The pricing fact is weaker and is why the note is Tier B.** It is **one market**. It is present in
  both halves of the pricing sample and **stronger in the later half**, which is honest reporting but
  also the direction that worries a replication-minded reader. **Transaction costs are not modelled
  anywhere.** **Multiple testing is not acknowledged.** No out-of-sample-country evidence is offered.
- **The discriminating tests are good, though, and there are several.** Double sorts hold the CIV-beta
  spread after controlling for market beta, size, **stock-level idiosyncratic variance**, VIX-beta and
  the Pástor–Stambaugh liquidity beta. The **asymmetry against MV is the most persuasive single
  result**: controlling for CIV-beta, the MV-beta spread is not distinguishable from zero in any
  CIV-beta group, while controlling for MV-beta the CIV-beta spread survives and widens. So this is not
  market-variance exposure in costume — and the authors say so on the basis of a test designed to be
  able to come out the other way.
- **It is not the idiosyncratic-volatility puzzle.** The relevant double sort uses stock-level
  idiosyncratic variance (standard deviation of daily market-model residuals each month) and keeps a
  significant CIV-beta spread in every bucket, while the variance direction's own spreads are not
  significant once CIV-beta is controlled.
- **Replication status: none independent that this folder can point to.** The CIV-beta sort postdates
  *Replicating Anomalies*' main sweep, it is a factor **beta** rather than a characteristic so it is
  outside the usual characteristic-zoo replications, and one of its authors is a co-author of the
  largest replication study — which is a reason to be careful rather than reassured. Treat the pricing
  claim as unreplicated.
- **Anti-lookahead**: all return spreads, alphas, t-statistics and correlation magnitudes attached to
  dated windows are deliberately omitted. The sample ends in 2011 at the latest, so none of it reaches
  this lab's validation window, and the sign and the ordering — which is what a hypothesis needs — are
  recorded without the magnitudes.

## Implementability here

**Reachable, but as a `statistical-learning` or `range-variance` scout and only after one free check.**
Every input is a daily close-to-close return. Nothing needs fundamentals, intraday data or volume. The
first-stage factor model can be the **5-PC version**, which this repo can compute and which the authors
report is equivalent to FF3 — that matters, because this lab has no Fama–French factors and would
otherwise have to proxy them.

**The adaptation, and the two places it is likely to break.**

- **Universe size is the first problem and it is serious.** CIV is a cross-sectional *average* over
  more than 20,000 names. Here it would be an average over ~140, of which 42 are ETFs whose
  "idiosyncratic" residual is a portfolio residual and not a name's. The averaging that makes CIV a
  clean aggregate is doing much less work at `N = 100`-ish, and the ETFs should almost certainly be
  excluded from the factor's construction even if they are eligible to be held. State the pool rule in
  the hypothesis.
- **History is the second.** CIV-beta needs a **60-month trailing window of monthly returns** before
  the first sort, on top of whatever the store's start date is. If the train split cannot supply
  60 months plus a usable sorting period, the construction has to shorten the window — which is a
  departure from the source and must be declared, not quietly adopted.
- **Turnover should be low, which is the one structural advantage.** A beta estimated on 60 months of
  monthly returns moves slowly, so monthly re-sorting on CIV-beta should produce far less turnover than
  a monthly re-sort on a 1-month signal. That is a prediction to check before the trial, not an
  assumption: it is cheap to compute the rank autocorrelation of CIV-beta across adjacent month-ends.
- **Survivorship cuts against this one, and in the usual direction.** The universe is current
  mega-cap constituents. A CIV-beta sort is a sort on *sensitivity of a surviving name's return to a
  panel-wide risk state*, and the names that would have had the most negative CIV-betas are
  disproportionately the ones that are not in the panel. Expect the spread to be compressed here
  relative to the source; if it comes back *larger*, suspect the artifact rather than the effect.
- **One honest reason the long leg here may not be the paper's long leg.** The reachable high-return
  end is the *low*-CIV-beta quintile — names that fall when common idiosyncratic risk rises. On a panel
  of 140 surviving mega-caps plus regional ETFs, the low-CIV-beta end may be dominated by a region or
  by the ETF sleeve rather than by a risk characteristic, in which case the sort is a regional bet. The
  check is the folder's standard one — read the composition before reading the return, and run a
  region-demeaned version alongside the raw one
  (`notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md`).

**The free pre-check that should come before any trial**, and the reason it is free: CIV as defined is
a panel-level time series, and on this universe it may be near-collinear with plain **market variance**
or with the **equal-weighted average of Garman–Klass range variance** the lab already computes. The
paper's own identifying result is that CIV beats MV; that result was established on 20,000 names, and
on 140 it may simply not hold. One correlation of `ΔCIV` against `ΔMV` and against the lab's existing
range-variance aggregate settles whether there is a distinct state variable here at all. See candidate
**#206**; the trial it gates is **#207**.

## Related

- `notes/2026-10-06-betaless-variance-decomposition-and-average-correlation.md` — the `FIRM` component
  of that decomposition is, up to the residualisation choice, the object this paper finds a factor
  structure in; that note's leakage term (`CSV(β) × market variance`) is also the cleanest statement of
  why a betaless residual's co-movement might be mechanical rather than real, which is the objection
  this paper answers with 10 PCs.
- `notes/2026-10-06-absorption-ratio-eigenvalue-concentration.md` — a co-movement state variable built
  on *first* moments; CIV is one built on *second* moments. Both are panel-level time series and the
  pair is the natural horse race.
- `notes/2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` and
  `notes/2026-09-01-max-lottery-extreme-positive-returns.md` — the idiosyncratic-volatility puzzle and
  the lottery sort, both of which this paper's double sorts are designed to be distinct from.
- `notes/2026-09-21-panel-volatility-models-and-risk-targeting.md` — pooling a volatility model across
  instruments, i.e. the estimation-side version of "volatilities have a common factor".
- `notes/2026-09-26-virtue-of-complexity-return-prediction.md` and
  `notes/2026-08-29-machine-learning-cross-section-comparative.md` — the family this would be scouted
  under if it enters as a feature rather than as a sort.
- `experiments/learnings.md` [2026-09-17] — "blending beats switching" and the finding that every
  refuted overlay timed the book on an external state variable. CIV-beta is **not** such an overlay: it
  is a cross-sectional sort, always-on, gross 1.0 throughout. That is the structural reason it is worth
  a scout where the absorption ratio's timing rule is not.
