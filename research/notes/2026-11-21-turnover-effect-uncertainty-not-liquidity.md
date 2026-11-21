---
title: "Turnover: Liquidity or Uncertainty? — the turnover effect is an uncertainty effect, its alpha sits on the high-turnover leg, and the sort it runs is implicitly an idiosyncratic-volatility sort"
authors: Barinov
year: 2014
venue: "Management Science 60(10), 2478–2495 — Tier 1 (peer-reviewed, named in this folder's rubric)"
url: https://doi.org/10.1287/mnsc.2014.1913
citations: 82 (Crossref `is-referenced-by-count`, checked 2026-11-21); Semantic Scholar's title endpoint returned HTTP 429 on the first call (checked 2026-11-21) and was not retried, per the README's rate-limit note
sample_period: "1964-01 to 2010-12 for the turnover effect itself; 1986-01 to 2010-12 for the sections that need the VIX-mimicking factor; untabulated subperiod checks reach back to 1926"
markets: "US only — CRSP/Compustat/IBES, with the NASDAQ turnover double-counting adjustment of Gao–Ritter applied; portfolio sorts exclude stocks priced below $5 at formation"
tier: "A on venue, construction care and subperiod robustness. Downgraded **in use here to C**, for three reasons that are about this panel and not about the paper: the signal needs shares outstanding, the alpha is on the leg a long-only book cannot hold, and the effect localises to low-institutional-ownership names this universe excludes by construction."
validation_overlap: false
published_post_2018: false
read: "Full text of the accepted manuscript (47 pages, 98 KB of extracted text, 925 instances of `\" the \"`, zero `( )` dropout, abstract and all seven sections plus eleven table captions intact), served by the author's own faculty page, `faculty.ucr.edu/~abarinov/Turnover%20(MS%20R4).pdf`, HTTP 200 on the first try."
---

## Access

**The author's own faculty page served the accepted version of a Tier-1 article on the first
request**, which is the [2026-09-18] faculty-page lesson behaving exactly as recorded. Two channel
notes worth keeping. `file -b` reported the PDF as **"6 page(s)"** for a document `pypdf` read as
**47 pages** — the thirteenth instance of the standing lesson that a page count from `file` is not a
completeness check, and the first in which it under-reported rather than over-reported. And the
search result that led here was titled "Turnover: Liquidity or Uncertainty? **Abstract**", which is
the file's own first heading and not a description of its contents — **a search-result title
beginning or ending in "Abstract" is not evidence that the file is abstract-only.**

## Mechanism

The paper's object is the **turnover effect**: the long-established negative cross-sectional
relation between a stock's share turnover (trading volume divided by shares outstanding) and its
subsequent returns. The literature it argues against had read that relation as a **liquidity
premium** — high turnover means liquid, liquid means a lower required return.

The paper's claim is that this reading is wrong on its own terms, and it establishes that before
proposing anything:

- Turnover is **not** positively related to liquidity. Higher-turnover firms have *higher*
  effective spreads (Gibbs, Roll, and the Corwin–Schultz high–low estimator), and the link to the
  price-impact measures (Amihud, Pástor–Stambaugh gamma) is "ambiguous and unreliable".
- Turnover is **unrelated** to liquidity *risk*: the loadings on three traded liquidity factors are
  essentially flat across turnover quintiles, and adding those factors does not explain the effect.
- Turnover **is** strongly related to firm-specific **uncertainty** — idiosyncratic volatility,
  analyst forecast dispersion, analyst forecast error, and the variability of earnings and cash
  flows all shift turnover with t-statistics above 3.

The positive story is a real-options one. High-uncertainty firms hold more option-like equity;
an option's value rises with, and becomes less sensitive to, uncertainty about the underlying.
Since firm-specific uncertainty comoves with aggregate volatility, high-uncertainty — hence
high-turnover — firms are a **hedge** against aggregate volatility risk, so they rationally earn
less. Empirically the factor-mimicking portfolio for VIX changes carries a loading that runs
monotonically from strongly negative in the lowest turnover quintile to strongly positive in the
highest, and that spread is large enough to absorb the effect: no turnover quintile retains a
significant alpha once it is included.

**The sentence this lab should read twice** is the author's own summary of the sort: *"sorting
firms on turnover will implicitly strongly sort them on firm-specific uncertainty, and ... the
sorting on turnover/uncertainty will not produce sorting on liquidity or liquidity risk (in fact,
it will produce an inverse sorting on liquidity)."* A turnover sort is an uncertainty sort wearing
a volume label.

## Construction recipe

- **Signal.** Turnover = shares traded / shares outstanding. The headline measure is **quarterly**:
  the average monthly turnover over the previous quarter, following Datar–Naik–Radcliffe. The paper
  states the results are **robust to measuring turnover at frequencies from one month to one year**
  — which is the only persistence statement it makes about the signal, and it is a statement about
  the *measurement* window, not about rank stability.
- **Sort.** Quintiles on turnover, re-formed monthly, equal- and value-weighted, excluding stocks
  priced below $5 at formation. All control variables are converted to within-month **ranks scaled
  to [0,1]** before entering any regression — a normalisation choice worth copying for anything
  cross-sectional and unit-dependent.
- **Controls, when turnover is the regressand.** Signed past return split into its positive and
  negative parts (for the disposition effect and short-sale constraints); market-to-book, firm age,
  analyst count and market cap as visibility controls; price and market cap again as microstructure
  controls; 60-month market beta and leverage as risk controls.
- **The explanatory factor.** FVIX: regress daily VIX changes on daily excess returns of five
  portfolios sorted on past VIX-change sensitivity, take the fitted part less the constant,
  cumulate daily to monthly. Robust to swapping the base assets for ten industry or six
  size/book-to-market portfolios.
- **Conditioning variables that sharpen the effect**: market-to-book and other growth-option
  measures (effect **stronger**), credit rating and leverage-driven option-likeness (effect
  **weaker** with better ratings), institutional ownership orthogonalised to size (effect stronger
  when low), residual analyst coverage (stronger when low), and the Hou–Moskowitz price-delay
  statistic (**no relation** — see below).

## Robustness evidence (qualitative only)

- **Subperiod stability is genuinely good.** The Fama–MacBeth estimate of the effect is of the same
  order — roughly 65 to 76 bp per month — in each of three non-overlapping multi-decade
  subperiods spanning 1926 onward, and dropping sub-$5 stocks does not change that. The author also
  checks that no single episode inside the shorter VIX-era sample drives it.
- **Not subsumed by its own best proxy, but heavily overlapped.** In a head-to-head Fama–MacBeth
  horse race, controlling for idiosyncratic volatility cuts the turnover effect from about 76 to
  about 50 bp per month, while controlling for turnover cuts the idiosyncratic-volatility discount
  from about 1.23% to about 1.1% per month. **Roughly a third of the turnover effect is the ivol
  effect and roughly two thirds is not** — so "it is just ivol" is an overstatement, and the honest
  reading is that the two are distinct but strongly correlated sorts of the same underlying
  quantity.
- **Where the effect lives, and this is the decisive robustness fact for a long-only book.** The
  spread is *"driven primarily by the negative alphas of the highest turnover quintile."* The
  low-turnover leg is not where the premium is; the high-turnover leg's deficit is.
- **It localises to exactly the names this panel excludes.** The effect is materially stronger in
  the bottom institutional-ownership quintiles, stronger among low residual-analyst-coverage firms,
  stronger among firms expensive to short, and consistently larger in **equal**-weighted than in
  **value**-weighted returns (roughly 50–75 bp/month equal-weighted against 35–40 bp/month
  value-weighted at the quintile spread). The paper's own explanation of the institutional-ownership
  pattern is mechanical and worth noting: institutions avoid both tails, so the extreme turnover
  cells are over-represented among low-IO names and the sort simply gets a wider spread there.
- **Single market.** US only. No independent replication is cited in the paper, and this folder has
  not located one; the non-US check it does have is the Tokyo working paper filed tonight, which
  reaches the same sign by a different route and with a different shape.
- **Methodology honesty is high**: costs are not modelled (it is an explanation paper, not a
  strategy paper) and it says so by omission, but the alternative explanations are tested rather
  than dismissed, the untabulated results are described rather than hidden, and the author states
  plainly where the data do not exist (shorting fees "impossible to obtain" for a broad
  cross-section).

## Implementability here

**The signal is not computable on this panel, and three further obstacles stand behind that one.**

1. **Turnover needs shares outstanding, which this repo does not have.** `aux` carries `volume` (a
   share count) and `dollar_volume`; the denominator is a fundamental. This folder already recorded
   the same obstacle in `2026-10-05-turnover-and-the-momentum-life-cycle.md`, and this source
   confirms the denominator is not decorative: the paper's own measure is a *rate*, and the raw
   share count differs across this universe's markets by orders of magnitude in share-unit
   convention alone. A **ratio of the same name's volume at two different times** does cancel shares
   outstanding and is computable — see the companion note on persistence for why that version is
   the *weaker* one.
2. **The alpha is on the leg a long-only book cannot hold.** v3 grades a fully-invested long-only
   book against the equal-weight eligible pool. A mechanism whose spread comes from the *negative*
   alpha of its top quintile offers a long-only portfolio only the **attainable underweight** —
   dropping ~20% of the pool — which the `#373`–`#380` vein has already priced as a small and
   breadth-limited lever. This is the fourth mechanism in a row to fail on this axis, and it is
   becoming the folder's most reliable single screen.
3. **The effect localises to low-IO, low-coverage, expensive-to-short, equal-weighted names.** The
   panel is nine large-cap national indices — high institutional ownership, heavy analyst coverage,
   cheap to short, and the kind of name a value-weighted number describes. Per the README's rule, a
   mechanism whose own literature localises its effect to small, thinly traded or neglected names is
   excluded by this panel **by construction**, so a null here would be uninformative rather than
   evidence against the paper.
4. **The explanation is unreachable even if the signal were.** FVIX needs the VIX; the conditioning
   variables that sharpen the effect (market-to-book, credit rating, institutional ownership,
   analyst coverage) are all fundamentals or holdings data.

**What is worth taking from it anyway, and it is not a book.**

- **A free pre-trial screen, and the most transferable thing in the paper: any volume-based sort
  proposed here should first be checked for how much of it is an idiosyncratic-volatility sort.**
  The paper measures this overlap directly and finds roughly a third. The lab can run the same
  check with no trial and no holdout: compute the cross-sectional rank correlation, within date,
  between the proposed volume score and trailing idiosyncratic (or even total) volatility. The lab
  has reproduced "Sharpe is flat in beta" and the absence of a low-volatility premium on this panel
  five times; if a candidate volume score correlates strongly with volatility rank, most of its
  content is an object already measured to null here, and the candidate should be re-specified
  before it costs a trial.
- **The rank-to-[0,1] normalisation** is the right default for any cross-sectional regressor on a
  panel whose units differ by market, and it is cheaper than winsorising.
- **One cross-check the lab now has for its own cost model.** The paper finds turnover *positively*
  related to effective spread — i.e. the more actively traded names were not the cheaper ones on
  that measure, in that sample. v3 assigns liquidity tiers from trailing median **dollar volume**
  alone, and `#422` already records a signed error in that tier. This is independent evidence that
  a volume-only liquidity proxy and a spread-based one can disagree in sign, which strengthens the
  case for the Corwin–Schultz-style high–low check the folder already holds rather than settling it.

**Pitfall if anyone implements the volume-ratio substitute.** Volume is not forward-filled on this
panel, so a quarter's "average monthly volume" is an average over a region-dependent number of
observations; and the back-adjustment factor behind five `amihud126` nulls is piecewise-constant in
time, changing at corporate actions, so a short-window-over-long-window volume ratio cancels it
**except** in windows containing a split. Require a minimum observation count and treat windows
spanning a share-count discontinuity as missing rather than as a signal.

## Related

- `notes/2026-10-05-turnover-and-the-momentum-life-cycle.md` — Lee–Swaminathan, the same uncomputable
  denominator, and the same conclusion that the profit sits on the leg this lab cannot trade. This
  source **agrees with that paper that turnover is not a liquidity proxy** and disagrees with its
  mispricing reading, attributing the pattern to aggregate volatility risk instead.
- `notes/2026-11-21-turnover-persistence-and-the-concave-premium-tokyo.md` — the non-US check, the
  signal's measured persistence, and the finding that the long-horizon version is weaker.
- `notes/2026-11-21-price-delay-and-the-investor-recognition-friction.md` — the attention statistic
  this paper tests the turnover effect against and finds unrelated to it.
- `notes/2026-09-07-high-volume-return-premium.md` — the *shock* version of a volume signal, which
  needs no shares outstanding and is the one volume object this panel can compute cleanly.
- `notes/2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` and the record's five reproductions of
  "Sharpe is flat in beta" — the object the turnover sort partly is.
- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md` — why obstacle 2 is
  fatal rather than merely inconvenient.
