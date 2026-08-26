---
title: "Do Stocks Outperform Treasury Bills?"
authors: Bessembinder
year: 2018
venue: Journal of Financial Economics 129(3), 440–457 (tier 1)
url: https://doi.org/10.1016/j.jfineco.2018.06.004
citations: 254 (OpenAlex, checked 2026-08-26; Semantic Scholar DOI endpoint 209; Crossref is-referenced-by-count 204 — three indices in agreement, so the count is taken at face value)
sample_period: 1926–2016 (CRSP monthly, 25,332 firms), plus IID simulations with no historical sample
markets: All US common stocks listed on NYSE, Amex and Nasdaq
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The third leg of session 13's theme: having established *that* the universe is selected (the other
two notes) this one describes **what the selection is selecting from**, and the answer is a
distribution so skewed that the selection's magnitude follows from it.

**The distributional fact.** Over the full CRSP history, most individual common stocks have lifetime
buy-and-hold returns below one-month Treasury bills. Fewer than half of all monthly individual stock
returns are positive, and only 47.8% exceed the same month's T-bill rate. **The modal lifetime
return, rounded to the nearest 5%, is −100%.** Median listing life is **seven and a half years**;
only 36 of 25,332 firms were present for the full sample. Ranked by lifetime dollar wealth creation,
the top **1,092 firms — 4.31% of the total — account for all of the net wealth creation** of the
entire US stock market over the sample, with the remaining 96% collectively matching Treasury bills.

**The mechanism is compounding, not a market pathology, and it is provable on IID normal draws.**
Multi-period buy-and-hold returns are positively skewed even when single-period returns are symmetric
— the point traces to Arditti–Levy (1975). The author's own simulation holds the monthly mean fixed
at 0.5% and varies only the monthly standard deviation `σ`:

- Skewness of buy-and-hold returns is positive at every multi-period horizon whenever returns are not
  riskless, and **increases in both horizon and `σ`**. At `σ = 2%`/month it runs from 0.188 (1-year)
  to 0.667 (10-year); at `σ = 20%`/month, 2.306 (1-year), 23.814 (5-year), 53.323 (10-year).
- Consequently the **median** buy-and-hold return falls monotonically in `σ` **at unchanged mean**.
  One-year horizon: 6.17% riskless → 0.48% at `σ = 10%`/month → −15.55% at `σ = 20%`/month. Ten-year
  horizon: 81.94% → 0.14% → **−85.28%**.

The calibration that makes this bite is three monthly standard deviations from the same data: **5.4%
for the value-weighted market portfolio, 7.3% equal-weighted, and 18.1% for the pooled distribution
of individual stock returns.** A book's `σ` is the dial in the table above, and concentration is what
moves it from the first number toward the third.

**The consequence for concentrated books, measured directly.** Bootstrap simulations select `N`
stocks at random each month, value-weight within the month, chain the returns, and repeat 20,000
times. Two results:

- *Skewness collapses with `N`.* At the annual horizon, the standardised skewness coefficient falls
  from **6.99** for single stocks to **1.08** at 5 names, **0.10** at 25, and turns slightly negative
  (−0.09, −0.21) at 50 and 100. Diversification eliminates the positive skewness of short-horizon
  individual stock returns; it does not eliminate it at long horizons.
- *The probability of beating a cap-weighted benchmark is below one-half at **every** `N`.* Rates of
  beating T-bills improve steeply with diversification (decade horizon: 47.8% at one stock, 72.3% at
  five, 86.7% at 25, 93.1% at 100). But the fraction of outcomes exceeding the accumulated
  value-weighted market return "is always less than fifty, even without any deduction for fees or
  trading costs". For 25-stock books: 48.7% at the annual horizon, 45.4% at a decade, 36.8% at 90
  years. A single-stock strategy underperformed the value-weighted market in **96%** of simulations
  over the full sample and underperformed T-bills in 73%.

That is the paper's stated explanation for why poorly diversified active strategies underperform
market averages more often than not — before any consideration of skill, fees or costs. It is an
arithmetic property of a right-skewed distribution: the mean is carried by a tail the median draw
does not contain.

## Construction recipe

Not a strategy. The transferable objects are two, both free of estimation:

1. **A concentration price expressed as a probability.** For a book holding `N` names drawn from a
   right-skewed universe, the quantity to state is not expected return but the *fraction of draws
   beating the cap-weighted aggregate*, which falls as `N` falls and as the horizon lengthens. It
   requires no forecast and no parameter — only `N` and the universe's skewness.
2. **A median-versus-mean check at fixed mean.** The table above says how far the median buy-and-hold
   outcome sits below the mean as a function of `σ` and horizon alone. Any construction step that
   raises a book's realised `σ` without raising its mean moves the median outcome down by a knowable
   amount, and the step from a diversified book's ~5–7%/month toward the individual-stock 18%/month
   is where the effect turns from second-order to dominant.

## Robustness evidence (qualitative only)

Tier-1 venue, three indices agreeing on a healthy citation count for a 2018 paper, and a 90-year
single-market sample covering all listed US common stocks rather than a screened subset. Costs are
explicitly *not* deducted anywhere, which the author uses in the strong direction — the
underperformance rates are what a costless book achieves. Multiple testing is not an issue because
nothing is being searched over. The compounding half is a simulation of a stated IID process and is
therefore a mathematical result that cannot decay.

Two subsample facts the author reports himself and which any use of this must carry. The
underperformance-versus-T-bills result is **concentrated in below-median-capitalisation stocks and
in stocks that entered the database since the mid-1960s** — the median lifetime return is negative
for entry cohorts from every decade since 1977, which he attributes to a documented shift in the type
of firm brought to public markets. The underperformance-versus-the-**market** result, by contrast, is
reported as pervasive across the whole cross-section. So the T-bill headline is the more
size-dependent of the two and the less applicable to a large-cap universe; the market-comparison
result is the one that transfers.

The single-market limitation is real. A global companion by the same lead author covering ~64,000
stocks across many countries exists (*Long-Term Shareholder Returns: Evidence from 64,000 Global
Stocks*, Financial Analysts Journal 2023, 21 Crossref citations) and would supply the multi-market
leg. It is **closed access with no repository copy found and was not read**; it is recorded here as
unread, nothing is claimed from it, and its sample would in any case run into this repo's validation
window, so it carries `validation_overlap` risk and only its existence is noted.

## Implementability here

**(a) It prices a step the lab has taken repeatedly and has never priced in this currency.** The
recorded concentration ladder — equal weight → rank weight → magnitude weight, then the buffer
deletion that moved the book from ~35 to ~30 names and 7.8 to 6.0 effective risk bets — raises the
book's `σ` at each rung. The folder has three accounts of what that costs (excess growth rate `γ*`,
the effective-number-of-bets index, the diversification return) and all three are risk-side or
growth-side. This one is distributional: **at unchanged mean, raising `σ` lowers the median outcome,
steeply and non-linearly, and the effect grows with horizon.** That is why `learnings.md` records
maximum drawdown widening monotonically with each concentration step and one validation year
dominating the P&L — those are the signature of a right-skewed outcome distribution, not two
unrelated observations.

**(b) A 15-name long-only book starts behind a cap-weighted benchmark, with zero skill assumed.**
The bootstrap says a randomly drawn 25-name value-weighted book beats the value-weighted market in
under half of draws at every horizon, costless. This repo's basket is more concentrated than 25 and
pays 15 bps/side. The correct reading is *not* "the champion is probably luck" — the champion is not
a random draw, it is a signal-selected book, and the gate scores it against a fixed incumbent rather
than against an index. The correct reading is that **the null distribution for a concentrated
long-only book is not centred on the index**, so any comparison of this repo's book to a broad
benchmark starts with a structural handicap that has nothing to do with the signal. It is the same
lesson as the random-portfolio null in
`notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md`, arrived at from the distribution
rather than from the universe selection.

**(c) It supplies the reason the other two notes' bias is *large*.** A universe of today's index
constituents is a sample from the right tail of exactly this distribution — the 4% of firms that
created all the net wealth are disproportionately the firms still in a large-cap index. The
look-ahead benchmark bias is big not because index rules are unusual but because **the distribution
being truncated has a modal lifetime return of −100% and a median listing life of 7.5 years**. That
last number is the sharpest single fact in this session for reading the repo's own splits: the train
split runs from 1962 on today's constituents, a span over which the median listed US common stock did
not survive one seventh of the way. `learnings.md` already records that "survivorship bias is worst
there"; this is the magnitude behind that sentence.

**(d) `program.md`'s escape hatch is confirmed on this axis.** "ETF-level strategies suffer least" is
right here for a reason this note makes explicit: an ETF *is* the diversified aggregate whose median
draw the individual-stock distribution's skewness does not damage, and its monthly `σ` sits at the
5–7% end of the calibration rather than the 18% end. That is a mechanism for the caveat, not merely
a restatement of it.

**Two boundaries, stated before any use.** First — the folder's own *check the currency* principle
(session 10, candidate #27) applies squarely: the statistics here are **probabilities of beating a
cap-weighted benchmark** and **medians of buy-and-hold returns**. Neither is net Sharpe on a
constrained cost-paying book, which is what the gate reads. A book can have a poor median
buy-and-hold outcome and a fine Sharpe, and the exchange rate between them is not supplied by this
paper or by anything else in the folder. Do not convert these numbers into an expectation about a
validation Sharpe. Second — the bootstrap books are **randomly selected**; every number here is a
property of the *null*, and none of it is evidence about a signal-selected book. Using it as such
would be the mirror of the error the folder has warned about since session 6.

**Not a proposed measurement.** Estimating this repo's own median-versus-mean gap or its
outperformance frequency against a benchmark scores returns, so it sits outside the holdings-only
exemption alongside session 11's PBO item and this session's random-portfolio null. The one thing
that *is* free and holdings-only is the input to the table above: a book's realised monthly `σ` at
each rung of the concentration ladder, which the repo already computes.

## Related

- `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the selection; this note is
  the distribution it selects from. Point (c) is the join.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the inference side.
- `notes/2026-08-22-excess-growth-and-return-decomposition.md`,
  `notes/2026-08-21-diversification-return-and-rebalancing.md`,
  `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the folder's three
  prior accounts of what concentration costs; this is the fourth and the only distributional one.
- `notes/2026-08-23-geometric-mean-maximization-fallacy.md` — the source of the *check the currency*
  boundary invoked above, and the reason the median-outcome framing is not a scoring axis.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — 1/N as a hard benchmark; the same
  diversification argument seen from the estimation-error side rather than the skewness side.
