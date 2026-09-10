---
title: "Global Currency Hedging" — read for the decomposition of a USD-converted foreign holding into a hedged local return and a currency excess return, and for what the currency component covaries with
authors: Campbell, Serfaty-de Medeiros, Viceira
year: 2010
venue: The Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.2009.01524.x
citations: 249 (OpenAlex, checked 2026-09-10); 221 (Crossref `is-referenced-by-count`, same date). Semantic Scholar's DOI endpoint returns "not found" for this DOI while resolving two other DOIs the same session — the `jofi` miss pattern sessions 11–15 record, again.
sample_period: 1975–2005, quarterly (with 1975–1989 / 1990–2005 subsamples reported separately by the authors)
markets: seven developed equity and bond markets and their currencies (US, Euroland, Switzerland, UK, Japan, Canada, Australia)
tier: A
validation_overlap: false
published_post_2018: false
read: full text of NBER Working Paper 13088 (May 2007, revised January 2009 — i.e. the revision immediately preceding the published article), `nber.org/system/files/working_papers/w13088/w13088.pdf`, served first try. The published JF tables were not read; nothing below is taken from them.
---

## Mechanism

This repo's prices are USD-adjusted closes of instruments that mostly do not trade in USD. Every
non-USD instrument's return, as this lab sees it, is two things added together:

    USD return  =  local-currency return  +  currency return   (plus a small cross term)

The paper's formal version writes the log excess return of a global portfolio as a **fully
hedged** component (local asset returns, no currency exposure) plus a **pure currency exposure**
component (the vector of currency excess returns, weighted by net exposures) plus a Jensen
correction. The decomposition is exact enough to reason with and it makes the point that matters
here: **a cross-sectional score computed on USD closes is computed on a sum, and part of what it
ranks is currencies.**

The economics of the currency half is the paper's subject. If currency returns were uncorrelated
with equity returns, currency exposure would be pure added variance with no compensating premium,
and the risk-minimizing answer would be to hold none of it — a full hedge. They are not
uncorrelated. Some currencies tend to **appreciate when world equity markets fall**, which makes
exposure to them variance-reducing for an equity investor even at a low average return; others
tend to depreciate at the same time, which makes exposure to them variance-*adding* on top of the
equity risk already held. The paper's own summary of which is which — reserve currencies in the
first group, a commodity-linked currency most strongly in the second — is a property of its
sample and the paper itself documents that the ordering moved between its two subsamples, so it
should be treated as a mechanism ("currencies carry signed equity exposure") and not as a list to
import.

The structural reading is that a currency is not a neutral units-conversion. It is a risk factor
with a beta on global equity, and converting a foreign price into USD adds that factor to the
return being measured.

## Construction recipe

**The risk-minimizing currency exposure.** For a given asset portfolio, the vector of net
currency exposures that minimizes the variance of the portfolio's excess return is

    Psi_RM  =  - Var( currency excess returns )^-1 · Cov( hedged portfolio return, currency excess returns )

i.e. **the vector of multiple-regression coefficients of the portfolio's return on the currency
excess returns**, negated. Currency excess return for currency `c` is the change in the log spot
rate plus the foreign short rate minus the domestic short rate. The exposures are constrained to
sum to zero (they are the weights of a zero-investment bill portfolio), so the domestic
currency's exposure is determined once the foreign ones are.

The interpretation the paper attaches to the regression is the part worth memorising, because it
is a sign rule and needs no numbers:

- **zero correlation** between asset returns and the exchange rate → hold no currency exposure
  (hedge fully): the exposure is uncompensated variance;
- **positive correlation** (the foreign currency falls when the market falls) → *over*-hedge:
  short the currency beyond the holding;
- **negative correlation** (the foreign currency rises when the market falls) → *under*-hedge:
  keep the exposure, it is a hedge in itself.

**A property worth knowing.** For a given asset portfolio the optimal currency demands are
**invariant to the investor's base currency**, provided a riskless real asset exists in each base
currency and the available currency set is unchanged. The currency question separates from the
"who am I" question — which is why a USD-based lab can read a literature written for investors of
every domicile.

**Conditioning.** The authors test whether these exposures should be moved around in response to
interest-rate differentials — the natural carry-style conditioning variable — and find little
evidence for it in the *risk-management* component. The risk-minimizing exposure is a covariance
object, not a yield object.

**Robustness of the construction itself.** Varying the investment horizon between one and three
months changes little; at six- and twelve-month horizons the composition of the optimal currency
portfolio changes materially. Equal-weighted and value-weighted global equity portfolios give
qualitatively and quantitatively similar answers, as does a home-biased portfolio. Bond
portfolios are a different animal: currency returns are close to uncorrelated with bond returns,
so a near-full hedge is the risk-minimizing answer there and demands are economically small.

## Robustness evidence (qualitative only)

- Multi-decade sample across seven major developed markets, with the authors reporting each of
  their two subsamples separately rather than only the full-sample answer.
- **The instability is documented by the authors, not discovered against them**, and it is the
  single most important robustness fact for anyone tempted to import a currency ranking: the
  relative attractiveness of the currencies changed between the two subsamples, and the paper
  offers a structural reason (a currency's growing acceptance as a reserve currency) rather than
  claiming a constant. **Signed equity exposure of currencies is a mechanism; the sign for any
  named currency is not a constant.**
- The equity-versus-bond contrast is itself corroborating evidence for the mechanism: the
  currency-equity covariance is what drives the result, and where that covariance is absent
  (bonds) the model correctly returns "hedge fully".
- The result that interest differentials do not usefully condition the risk-management demand is
  a *negative* result inside the paper, reported as such.
- Not independently replicated as far as this note establishes; its tier rests on venue, sample
  length, the internal subsample reporting and the transparency of the negative results, not on a
  replication study.

## Implementability here

**Start with what is out of scope, because most of this paper is.** The lab cannot trade
currencies, forwards or bills; `CLAUDE.md` forbids trading outright and the mandate is long-only
equity/ETF weights. The paper's actual recommendation — a currency overlay — is **not a candidate
and should never be written as one.** What transfers is the decomposition and the covariance
fact behind it.

1. **The universe is already split by currency, and it is nearly the same partition as region.**
   `experiments/learnings.md` (2026-09-04) records **13 non-USD regions** and a clean
   USD-quoted-names subset, and the repo has no country field so region groupings are *built from
   listing currency* (`notes/2026-08-28-international-momentum-country-neutral.md`). That means
   the lab's region demean is, to a first approximation, **a currency demean** — and this note
   names one specific thing it is removing.
2. **The free measurement is the variance share.** For each non-USD name, the USD return is the
   local return plus the currency return. The lab cannot observe the local return directly, but it
   can regress USD returns on a currency-group return (or on the equal-weighted return of the
   USD-quoted names, as the "no-FX" control) and read off how much of the cross-sectional
   dispersion it is ranking is currency. This is a train-split diagnostic; it scores no candidate.
3. **The USD-quoted subset is a ready-made placebo, and the lab has already used it once.** The
   2026-09-04 Corwin–Schultz screen tested the FX-artifact escape by restricting to USD-quoted
   names, where no FX enters at all, and found the estimator's failure survived. That is exactly
   the right control design for any question in this note: run the score on USD-only names, where
   the currency component is identically zero, and compare.
4. **A currency tilt is not a diversifying tilt.** The paper's central covariance fact means an
   unhedged foreign position's currency component is *correlated with global equity*, in a sign
   that differs by currency. So if a cross-sectional score is partly ranking currencies, the
   resulting bet is partly a levered or de-levered global equity bet, not an orthogonal one. That
   is a specific prediction about the leg's `rho` to the champion — the number
   `experiments/leaderboard.json` already carries and the one every blend decision here is priced
   on.
5. **It predicts where an FX artifact shows up and where it cannot.** Any statistic built from
   more than one day's USD prices absorbs the currency move; a statistic built inside one day's
   bar largely cancels it. The lab discovered exactly this asymmetry in the two-day-range term of
   the Corwin–Schultz estimator. The general form: **the longer the window and the more the
   statistic is a difference of prices at different times, the more currency it contains.**

**Pitfalls.**

- **Do not import which currencies are defensive.** The paper's own subsamples disagree, and any
  such ranking would be a period claim of exactly the kind this folder must not record. What is
  recorded is the sign rule and the fact that the sign exists.
- **Interest rates are not in this repo**, so the currency *excess* return of the paper cannot be
  formed exactly; only the spot component is observable through the USD conversion. For a
  cross-sectional demeaning use that is harmless — the short-rate differential is a slow-moving
  group-level constant — but it means the paper's regression cannot be reproduced literally here,
  and any claim that it was would be false.
- **Region and currency are nearly but not exactly the same partition**, and the exceptions are
  the interesting ones (names quoted in a currency other than their region's dominant one, and
  every ETF). Decide the mapping explicitly before measuring.
- **Nothing here licenses a new book.** As with its two companions tonight, this is a measurement
  mechanism about what a score contains. The lab's standing message (2026-09-08) is that its
  bottleneck is not idea supply, and this note deliberately does not add one.

## Related

- `notes/2026-09-10-country-industry-global-return-decomposition.md` — the covariance-model reading
  of the same partition; a region demean is the restricted, unit-loading version of a regional
  beta.
- `notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — the other half of
  what a region demean removes, and the argument that it is priced.
- `notes/2026-09-04-high-low-spread-estimator.md` — the estimator whose FX escape the lab tested
  and closed; the concrete precedent for the USD-only control recommended above.
- `notes/2026-08-29-range-based-volatility-estimators.md` — the other place FX contaminates a
  multi-day price statistic here.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md` — the *other* thing that goes wrong
  when a global universe is observed on one clock.
- `experiments/learnings.md` (2026-09-04) — the 13 non-USD regions, and the USD-quoted-names
  control in its original use.
