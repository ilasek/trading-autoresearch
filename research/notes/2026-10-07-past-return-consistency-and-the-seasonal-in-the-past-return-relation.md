---
title: "What Do We Really Know About the Cross-Sectional Relation Between Past and Expected Returns? — consistency, season, and tax regime"
authors: Grinblatt, Moskowitz
year: 2004
venue: Journal of Financial Economics 71(3), 541–579 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/s0304-405x(03)00176-4
citations: "339 (Crossref `is-referenced-by-count`, checked 2026-10-07); 482 (OpenAlex, checked 2026-10-07); 438 (Semantic Scholar, checked 2026-10-07)."
sample_period: "CRSP monthly returns 1963-08 to 1999-12. In-sample estimation 1966-08 to 1995-07; genuine out-of-sample extension 1995-08 to 1999-12 using the in-sample coefficients unchanged."
markets: "US — all NYSE, AMEX and NASDAQ-NMS firms with the required history; 20 two-digit-SIC industry portfolios; institutional-ownership and turnover panels on shorter sub-samples"
tier: A
validation_overlap: false
published_post_2018: false
read: "Full text, NBER Working Paper 8744 (January 2002), `nber.org/system/files/working_papers/w8744/w8744.pdf`, which carries the abstract, all seven sections, the table discussion and the reference list of the article published in JFE 2004. **Access note:** `pdftotext -layout` returned the title page and abstract in clear text but the entire body **uniformly shifted by −29 in ASCII** (so `Introduction` extracts as `QWURGXFWLRQ`); decoding by +29 while preserving whitespace recovers clean prose **with digits intact**, but parentheses and the `fi`/`ff`/`ffi` ligatures are dropped by the extractor and do not come back. See the access section of `research/SUMMARY.md`."
---

## Mechanism

The paper's organising claim is that the relation between past returns and expected returns is not
one effect per horizon but a **joint** object, and that two conditioning variables nobody was using
change it materially: the **consistency** of the past return path (as distinct from its magnitude)
and the **season/tax-regime** in which the return is earned.

**The consistency result is the part with no tax story in it, and it is the most transferable thing
in the paper.** Alongside the usual past-return regressors at non-overlapping horizons, the authors
add dummies for being a *consistent* winner or loser — a count of how many of the months in the
formation window had a positive return, not how large the cumulative return was. The result is a
sharp asymmetry: **every consistent-winner coefficient is positive, at all three horizons and in
all three seasonal subperiods as well as overall, and most are statistically significant, while the
consistent-loser coefficients have little effect.** The authors argue the asymmetry is what rules
out the obvious alternative reading, that consistency is a proxy for low volatility: low volatility
would show up with opposite sign on both tails, and it does not. So consistency is carrying
something about the *path* of the past return that its sum does not.

Because the horizon regressors are non-overlapping, the coefficients are marginal effects holding
the other horizons fixed, and the authors report that estimating each horizon separately gives
almost identical coefficients — i.e. the short-, intermediate- and long-horizon effects are
substantially **independent** of one another, which is an argument against the class of behavioural
models that derive long-term reversal *from* intermediate-term momentum.

**The seasonal result.** Decomposing the strategy's profitability into January, February–November
and December reveals that the turn-of-the-year months dominate, and that the horizons behave
differently in them:

- The **three-year reversal effect is almost entirely a January phenomenon**, driven by long-term
  losers; the three-year *winner* effect is absent in January. Outside January there is no
  distinction between three-year winners and losers at all.
- In **December the three-year loser coefficient flips sign to persistence** — the long-horizon
  strategy becomes a momentum strategy in December, and the loser term is large relative to the
  winner term.
- The one-month reversal effect, the horizon the authors themselves flag as liquidity- and
  microstructure-contaminated, is most negative in January and somewhat more negative in December.
- Intermediate-horizon (one-year) momentum, by contrast, is present throughout the calendar year.

**The tax-regime result, and how the authors identify it.** Rather than assuming the seasonality is
tax-driven, they classify years by whether the maximum short-term capital-gains rate at the start of
the year is at least 20% above or below the average of the two surrounding years, and interact that
classification with January and December dummies. The pattern they find: the strategy's
turn-of-the-year profitability is a **high-tax-regime phenomenon**, and in low-tax years neither the
turn-of-the-year seasonal nor average profitability is reliably different from zero. Pushing further,
they verify the effect shows up where a tax story requires it to — concentrated in the loser decile,
in **December on the downside and January on the upside**, and strongest among **small-cap stocks
with low institutional ownership**, i.e. the names most likely to be held by taxable individuals.
Among large caps, institutional ownership makes essentially no difference, which is what a tax
explanation predicts rather than something it has to explain away.

The three conditioning axes — consistency, season, tax regime — are therefore separable: the
consistency asymmetry holds in every subperiod including February–November, while the long-horizon
sign flips are specific to the turn of the year and to the tax regime.

## Construction recipe

**Horizon definitions (non-overlapping, with deliberate gaps).** The "one-year" return is measured
from *t*−12 to *t*−2, i.e. **eleven months with the most recent month skipped** — the skip is there
to kill microstructure contamination and to keep the regressor near-orthogonal to the one-month
term. The "three-year" return is *t*−36 to *t*−13, i.e. twenty-four months with the most recent year
skipped, again for orthogonality.

**Consistency dummies, which are the free idea here.** Both are pure sign counts over the same
window as the corresponding return regressor:

- One-year **consistent winner** = 1 if the monthly return was positive in **at least 8 of the 11
  months** of the one-year window; one-year **consistent loser** = 1 if negative in at least 8 of 11.
- Three-year **consistent winner** = 1 if positive in **at least 15 of the 24 months** from *t*−36
  to *t*−13; consistent loser = negative in at least 15 of 24.
- At the one-month horizon, "consistent winner" degenerates to simply having had a positive return,
  and the loser dummy must be dropped to avoid perfect collinearity.

**The thresholds are not tuned — they are calibrated to the binomial null.** Under equal
probability of a positive or negative month, P(≥8 of 11) ≈ P(≥15 of 24) ≈ 10%. The authors say
plainly that the cut-offs are arbitrary but were chosen to capture the **top decile of consistent
performance under the null**, and that the two definitions have approximately matching tail
p-values. That is why the same construction transfers to a different panel without re-fitting: the
rule is "take the names in the top decile of a coin-flip null for sign-run consistency", not "take
8 of 11 because 8 worked".

**Dependent variable.** Returns are **hedged**: each stock's month-*t* return less the month-*t*
return of its matched benchmark portfolio, where benchmarks are the 25 intersections of independent
size and book-to-market quintile sorts (NYSE breakpoints for size, full-universe breakpoints for
BE/ME), value-weighted within each cell, with industry handled separately. The point is to strip
size, value and industry so the coefficients are the marginal effect of the past-return attribute
itself.

**From regression to portfolio.** Fama–MacBeth cross-sectional regressions produce a coefficient
vector; stocks are then scored with it, sorted into deciles, and **value-weighted within decile**.
The authors stress two cost-driven construction choices: value-weighting rather than equal-weighting
(equal-weighting both emphasises small illiquid names and generates extra rebalancing turnover), and
a **minimum share price screen**, which they report barely changes the result because value-weighting
already gives low-priced names little weight.

**Tax-regime classifier (for completeness).** A year is "high tax" if its maximum short-term
capital-gains rate is ≥20% above the average of the two adjacent years' maxima, "low tax" if ≥20%
below, and otherwise inherits the prior year's classification; a January is assigned to the year of
its **adjacent December**.

**Turnover discipline the authors impose on themselves.** Any ranking that weights the past one-month
return heavily turns over nearly the whole portfolio monthly, because this month's extreme names are
rarely next month's; they therefore report a variant that **forces the one-month coefficients to
zero** and treat it as the economically serious specification.

## Robustness evidence (qualitative only)

The out-of-sample design is unusually honest for its vintage: the scoring coefficients estimated on
the earlier window are applied, **unchanged**, to several years of data that accrued after the prior
draft of the paper was written, and the authors frame this explicitly as a test against the
data-snooping objection — if the specification had been reverse-engineered from the literature, it
should fail there. The qualitative outcome they report is that the spreads are **about the same or
larger** out of sample across the specifications, including the low-priced-stock-excluded variants.
No dated performance figure from either window is recorded here.

Other supports: the horizon effects survive the hedging against size, value and industry; the
consistency asymmetry holds in every seasonal subperiod; the results are not attributable to a
small-growth-firm artifact given value weighting inside hedged deciles; and the coefficients are
stable whether horizons are estimated jointly or separately. Known limits: one country, one
database, and the tax-regime test rests on a small number of qualifying Januaries, which the authors
acknowledge by noting the low-tax January estimate is economically notable but statistically
insignificant on so few observations. The multiple-testing issue is addressed by the out-of-sample
extension rather than by a formal haircut.

**Tension with this lab's own record, stated rather than smoothed over.** `experiments/learnings.md`
puts the lab's `price-trend` family at exhaustion and prices a decorrelated challenger's required
gain at +0.438 Sharpe. Nothing in this paper contradicts that — but the lab's momentum work has, as
far as the journal of record shows, sorted on the **magnitude** of a past return (and on functionals
of the price path: 52-week-high proximity, information discreteness, capital-gains overhang).
A **sign count** is a different functional of the same data, it is unit-free, its threshold is fixed
by a coin-flip null rather than fitted, and the published asymmetry says the content is on the
**winner** side, which a long-only book holds directly. That makes it a candidate for the family's
remaining capped budget rather than a repeat of a refuted idea. The folder's existing
information-discreteness note (`notes/2026-09-28-information-discreteness-frog-in-the-pan.md`) is the
nearest relative and is *not* the same statistic — discreteness is about the distribution of the
path's magnitudes, consistency is a count of its signs.

## Implementability here

**Three items, in decreasing order of how much this repo can trust them.**

*1 — Consistency as a signal, and it is the session's strongest buildable item.* Monthly returns come
straight from daily closes. The construction needs nothing the repo lacks: for each eligible name,
count positive monthly returns over *t*−12…*t*−2 and flag ≥8 of 11. It is a **binary, unit-free**
score, which matters here — `experiments/learnings.md` records that this lab has no principled common
scale across heterogeneous scores, and a dummy sidesteps that problem entirely. The long-only
version is direct: hold the consistent winners, which is the side the paper's asymmetry says carries
the effect. Expect **low turnover** relative to a magnitude-ranked momentum book, because a sign
count over eleven months changes slowly; measure the rank autocorrelation of the flag across adjacent
month-ends on train before spending a trial. Two cautions. The paper's coefficients come from
*hedged* returns with size/value/industry removed; this repo has no book-to-market and its only
grouping axis is region, so the lab is measuring a different object and should run a region-demeaned
variant alongside the raw one (`notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md`).
And the 10% binomial calibration implies a **narrow** book — on an eligible panel of roughly a
thousand names the top-decile-under-the-null rule is a strong screen, not a tilt, so the 25%
position cap and the concentration gate are the constraints to check first.

*2 — The December/January sign flips as free train-only screens.* Three pre-registered, zero-trial
checks, each a directional claim the lab can read off a regression it already knows how to run:
(a) the long-horizon (*t*−36…*t*−13) reversal coefficient should be concentrated in January and
absent in February–November; (b) it should **flip to persistence in December**; (c) the one-year
momentum coefficient should be roughly flat across the calendar. Any of these failing on this
universe is informative, and all three are diagnostics, which `program.md` makes free and unlimited.

*3 — The tax-regime interaction does not transfer, and this is the honest limit.* The identification
is **US short-term capital-gains rate changes**, interacted with a US December/January tax year. This
universe is fifteen regions; its personal tax years do not all end in December; and the repo has no
tax-rate panel. Worse, the paper's own conditioning says the effect lives in **small caps with low
institutional ownership**, and protocol v2's pool is ~1,400 names that were ever members of nine
large-cap indices plus 42 ETFs — the opposite end of both gradients, and institutional ownership is
precisely where the paper finds the effect vanishes. **So the tax-conditioned seasonal should be
treated as not implementable here, and a null on it should not be read as evidence against the
mechanism.** The consistency result, which needs none of that machinery, is the part to build.

A cost note in the lab's favour: the authors' own turnover discipline — zero weight on the one-month
term, value-weight within the book, screen out the lowest-priced names — points the same way the
repo's 15 bps/side and 25% cap already force. The variant they consider economically serious is the
low-turnover one, so there is no conflict to adjudicate between the source's preferred construction
and this repo's constraints.

## Related

- `notes/2026-10-07-tax-trading-theory-and-the-price-pressure-condition.md` — the theory behind the
  tax-regime half, and the reason its price channel is conditional.
- `notes/2026-10-07-tax-loss-trading-and-wash-sales-investor-level.md` — the same author's
  investor-level evidence that the December flow exists and is naive; note the window there is
  trading days around the year-end, not the calendar month this paper uses.
- `notes/2026-10-07-tax-year-end-alignment-and-the-australian-test.md` — the multi-market evidence
  against reading the seasonal as tax-caused.
- `notes/2026-08-29-same-calendar-month-seasonality.md`, `notes/2026-09-02-return-seasonalities-common-factors.md`
  — the other seasonal-in-the-cross-section literature here. Those sort on the *same calendar month*
  in past years; this paper conditions a *past-return* effect on the current month. Different
  signals, and the folder has no measurement of their overlap.
- `notes/2026-09-28-information-discreteness-frog-in-the-pan.md` — the nearest relative to the
  consistency dummy and demonstrably a different statistic (magnitude distribution versus sign count).
- `notes/2026-08-17-momentum-horizon-echo.md`, `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md`
  — the horizon structure this paper re-estimates jointly, and its finding that the horizons are more
  independent than the behavioural models assume.
- `notes/2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md` — relevant because the
  consistency dummy is the extreme case: it discards magnitude entirely.
