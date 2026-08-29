---
title: "Seasonality in the cross-section of stock returns (US, and the international evidence)"
authors: Heston, Sadka
year: 2008 (JFE); 2010 (JFQA)
venue: Journal of Financial Economics 87(2), 418–445 (venue tier 1); Journal of Financial and Quantitative Analysis 45(5), 1133–1160 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2007.02.003 · https://doi.org/10.1017/s0022109010000451
citations: 2008 paper — 292 (Crossref `is-referenced-by-count`, checked 2026-08-29); Semantic Scholar's DOI endpoint reports only 97 for the same DOI, a further instance of this folder's "disbelieve a lone low count" rule, here with Crossref as the high side. 2010 paper — 62 (Crossref, checked 2026-08-29)
sample_period: 2008 paper — returns measured January 1965 to December 2002 (formation data back to 1963, and to 20 annual lags); 2010 paper — international, sample period not verified from full text
markets: 2008 — NYSE/AMEX-listed CRSP firms; 2010 — Canada, Japan and 12 European countries
tier: A for the 2008 paper (tier-1 venue, multi-decade, extensive controls, costs discussed honestly by the authors themselves); B for the 2010 paper as recorded here, since only its published abstract was read
validation_overlap: false
published_post_2018: false
read: 2008 paper — full text of the October 2006 working version from NYU Stern's seminar archive (`w4.stern.nyu.edu/finance/docs/pdfs/Seminars/063f-sadka.pdf`), which carries the abstract, all sections and tables of the article published in JFE 2008. 2010 paper — **abstract only**, from the Cambridge Core landing page; `oa_status` closed, no repository copy found. Its claims below are flagged as such.
---

## Mechanism

The claim is a **permanent cross-sectional seasonal in expected returns**: a stock that has
historically earned relatively high returns in a particular calendar month tends to keep earning
relatively high returns in that same calendar month. The pattern is not a one-year echo. Sorting
stocks on their average return in the *annual lags only* (months t−12, t−24, …, t−240) produces a
positive winner-minus-loser spread at **every** annual horizon tested, out to twenty years; sorting
on the *non-annual* months of the same intervals produces a **negative** spread at every horizon.
The two signs sit side by side in adjacent months of the same formation window.

That structure is what makes the effect interesting rather than a relabelling of momentum. The
authors show that the familiar shape — Jegadeesh–Titman continuation over the past year, DeBondt–
Thaler reversal over years two to five — is a *contiguous-months* result, and that a periodic
seasonal component of the opposite sign is superimposed on it. Their reading is that the annual-lag
sort is picking up a stationary, stock-specific seasonal component of expected returns, and that the
long horizon (still present at twenty annual lags) rules out a temporary-autocorrelation explanation
in favour of a permanent one.

They are candid that they do not identify the cause. The pattern is shown **not** to be explained by
size, industry, earnings-announcement months, dividend-announcement or ex-dividend months, calendar
effects, or fiscal-year timing, and the decile spreads have approximately **zero loadings on the
market and on the Fama–French three factors**, so risk-adjusted returns are close to raw returns —
"we do not find that conventional measures of systematic risk are successful in explaining seasonal
variation in expected returns". Volume and volatility exhibit similar seasonal patterns but do not
explain the return seasonality. The authors' own closing speculation is that transaction costs and
illiquidity must play a role in why it persists, which is a hypothesis about the *survival* of the
effect rather than about its origin.

## Construction recipe

- **Signal.** For a formation interval expressed in *annual lags* — e.g. lags {12, 24, 36, 48, 60}
  for the "years 2–5" version — take each stock's **average monthly return across exactly those
  lagged months** and rank the cross-section on it. The distinguishing feature is that the
  formation months are **non-contiguous**: you are averaging the same calendar month from several
  past years, not a block of consecutive months.
- **Horizons tested.** Year 1 (a single annual lag, t−12), years 2–5 (lags 24–60), years 6–10,
  years 11–15, years 16–20. Each is run three ways: on **all** months in the interval, on the
  **annual-lag** months only, and on the **non-annual** months only. The three-way split is the
  identifying design and should be preserved in any adaptation — the contrast between the annual
  and non-annual legs is the result.
- **Portfolios.** Decile portfolios, **equal-weighted**, formed on the signal and held for **one
  month**, rebalanced monthly.
- **A construction fact worth its own line.** Within the one-year interval, sorting on the
  **12-month lagged month alone** delivers a *better return-per-unit-risk* than sorting on all
  twelve months of the past year — a higher t-statistic on a smaller raw spread. Most of what a
  conventional twelve-month momentum sort captures is available from the single month twelve months
  back. That is a claim about the *composition* of the momentum signal this lab's champion family
  is built on, and it costs nothing to check.
- **Data requirement.** The long-lag versions need up to twenty years of prior returns per name.
  The authors note that fewer than 30% of their firms have twenty years of history, and accept the
  resulting attrition rather than backfilling.
- **International variant** (2010, from the abstract): rank stocks on their past performance
  **relative to their own domestic market** in a given calendar month; the continuation runs for up
  to five years. Abnormal returns survive controls for size, beta and value using **either global or
  local risk factors** — the same local-versus-global construction question the folder covered in
  `2026-08-28-local-versus-global-factor-construction.md`.

## Robustness evidence (qualitative only)

- **Multi-decade**: the 2008 paper's return measurement spans 38 years, and the effect is described
  as present across it rather than concentrated in a subperiod.
- **Multi-market**: the 2010 companion reports the pattern in Canada, Japan and twelve European
  countries. **Recorded from the published abstract only.**
- **Not a risk premium in any conventional sense**: near-zero loadings on the market and the three
  Fama–French factors, in both the US paper and (per its abstract) the international one.
- **Cross-country decorrelation** — from the 2010 abstract, and the single most relevant robustness
  claim for this lab: the seasonal strategies "are not highly correlated across countries", which
  the authors offer as evidence against a global systematic-risk explanation. A signal whose legs
  are weakly correlated across regions is structurally different from a global momentum book, whose
  comovement is the subject of `2026-08-28-value-momentum-everywhere-global-comovement.md`.
- **The authors model the cost problem themselves, and it is the finding to lead with.** Section 5.5
  of the 2008 paper draws the distinction explicitly: momentum and contrarian strategies "require
  rebalancing only a part of the portfolio every few months, while seasonal strategies require
  rebalancing the **entire portfolio every month**". Their own conclusion is that "it may not be
  generally profitable to incur round-trip transaction costs" for a gain of this size, and that
  "the existence of short-lived fluctuations in monthly expected return may not form an effective
  foundation for a long-term investment strategy". They also note that the periods where the raw
  effect is largest are periods where transaction costs are documented to be higher, citing Sadka
  (2001) and Korajczyk–Sadka (2004) — the same Korajczyk–Sadka this folder covers in
  `2026-08-27-momentum-net-of-costs-debate.md`. Their constructive suggestion is not to trade the
  signal but to use it as an **execution overlay**: "it is relatively simple to postpone the sale or
  purchase of a particular stock if it has a large positive or negative expected return over the
  next month."
- **Multiple testing**: not formally addressed. The design is unusually well protected against it
  by construction — the annual/non-annual contrast is a sign prediction made in advance, tested at
  five independent horizons, and confirmed at every one — but no haircut is applied.

## Implementability here

**In scope on closes alone, cheap to compute, and mechanically unrelated to the incumbent** — which
is what `program.md` says makes `seasonality-calendar` worth a scout. Three things follow.

- **The turnover gate is the whole problem, and the authors say so before the lab has to discover
  it.** A signal recomputed monthly over a full cross-section re-ranks the entire book every month.
  This lab's own first `statistical-learning` scout hit exactly this and paid roughly a third of its
  margin over the equal-weight floor to 15.4× annual turnover; a monthly seasonal decile sort has
  the same shape. `program.md` names the turnover gate as the thing to watch in this family, and a
  tier-1 source independently reaches the same conclusion from the other direction. **A candidate
  here should be designed turnover-first**: hysteresis on basket membership (the buffering
  mechanism that is already the strongest lead in the repo), a small active tilt against a stable
  base rather than a full re-sort, or a fixed-fraction overlay.
- **The overlay framing is the authors' own and is under-explored.** Rather than a standalone
  seasonal book, use the seasonal expectation to **defer trades** a trend or liquidity book was
  going to make anyway — postpone a sale when next month's seasonal expectation is high, postpone a
  purchase when it is low. That adds no turnover; it *re-times* existing turnover. It is
  structurally the same idea as the banding/no-trade-region literature the folder already holds
  (`2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`) but with an *asymmetric,
  signal-conditional* band instead of a symmetric one. This lab has the machinery for it and, as
  far as the journal records, has never tried it.
- **The data horizon is the binding constraint on the pure version.** Twenty annual lags need
  twenty-one years of history per instrument. Whatever this repo's store actually spans, the
  long-lag versions will either be unavailable or will be available only for a survivor-selected
  subset — and that subset is exactly the one
  `2026-08-26-survivorship-conditioning-and-spurious-persistence.md` warns is the severe case,
  because the claim being tested *is* a persistence claim. The **year-1 single-lag version (rank on
  the return in month t−12 alone)** needs only thirteen months of history, is available for the
  whole universe, and is the version the paper reports as having the best return-per-unit-risk. It
  is the obvious first scout, and it is nearly free: it is one column of the return panel.
- **A cheap diagnostic that scores no returns and is therefore unlimited under `CLAUDE.md`.**
  Before spending a trial, run the annual-versus-non-annual contrast as a pure measurement on the
  training split: is the cross-sectional autocorrelation of returns at lags 12, 24, 36 positive
  while it is negative at neighbouring non-annual lags, on *this* universe? If the sign pattern is
  absent here, the family is closed for one diagnostic and no trials. If it is present, the scout is
  motivated by a measurement rather than by a citation.

**Known pitfalls.** (a) The universe is 42 ETFs plus ~100 large global stocks. The paper's effect is
about *firm-specific* seasonal components; an ETF has no fiscal year and no earnings month, so the
mechanism, whatever it is, plausibly does not apply to nearly a third of this universe. Consider
scoping the signal to the stock sleeve and saying so. (b) A single-lag signal is one monthly return
— an extremely noisy estimate, and on a 145-name cross-section the sort is thin. The paper averages
across several annual lags precisely to average out that noise, so the trade-off between data
horizon and signal noise is real and should be stated in the hypothesis, not discovered afterwards.
(c) Nothing here licenses a magnitude expectation, and `CLAUDE.md` forbids importing one. The
transferable content of this note is a **signal definition, a sign prediction, and a cost warning.**

## Related

- `2026-08-17-jegadeesh-titman-overlapping-momentum.md`,
  `2026-08-17-momentum-horizon-echo.md` — the annual-echo structure in momentum, which this paper
  reframes as one instance of a twenty-year periodic pattern. The horizon-echo note and this one are
  about the same observation from opposite ends.
- `2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the machinery for the overlay
  framing the authors themselves propose.
- `2026-08-27-momentum-net-of-costs-debate.md` — Korajczyk–Sadka, cited by this paper for the point
  that costs are highest where the raw effect is largest.
- `2026-08-28-local-versus-global-factor-construction.md`,
  `2026-08-28-value-momentum-everywhere-global-comovement.md` — the local-versus-global control
  question the 2010 companion runs both ways, and the comovement result this effect's cross-country
  decorrelation contrasts with.
- `2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — why the long-lag versions are
  the exposed ones on this repo's universe.
