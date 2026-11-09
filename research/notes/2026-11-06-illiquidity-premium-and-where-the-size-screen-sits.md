---
title: "The illiquidity premium: International evidence"
authors: Amihud, Hameed, Kang, Zhang
year: 2015
venue: Journal of Financial Economics 117(2), 350–368 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2015.04.005 · full text read from https://web2-bschool.nus.edu.sg/wp-content/uploads/media_rp/publications/HPeeM1422257215.pdf
citations: 314 (Crossref `is-referenced-by-count`, checked 2026-11-06)
sample_period: 1990–2011 (22 years)
markets: 45 countries, developed and emerging, split into Asia-Pacific / America / Europe regions; Datastream data
tier: A — tier-1 venue, three-figure citations, 45 markets over two decades, four independent estimation methods, and a volatility control built into the sort rather than bolted on afterwards
validation_overlap: false (sample ends 2011)
published_post_2018: false
read: full text, author-hosted working paper via NUS Business School (1.4 MB PDF → 163 KB of clean text, 965 instances of `" the "`, zero `( )` dropout, title and author block verified)
---

## Access

`web2-bschool.nus.edu.sg/wp-content/uploads/media_rp/publications/<opaque-id>.pdf` served the
complete working paper first try. Two things to record. It is another instance of the flat
`/wp-content/uploads/` shape this folder keeps rediscovering (after `burns-stat.com` 2026-10-15 and
`robjhyndman.com/papers/` 2026-10-13), now on a **business school's research-publications tree** —
so the pattern extends to institutional hosts and is worth trying for any paper with a co-author at
a school that runs its own site. And the filename is a wholly **opaque id**, derivable neither from
the title nor the authors, so it must come from a search result.

**DOI.** A DOI guessed from the JFE 2015 pattern resolved to a different JFE article of the same
year. The correct one came from **enumerating the journal-year** with
`api.crossref.org/journals/0304-405X/works?filter=from-pub-date:2015-01-01,until-pub-date:2015-12-31&query.bibliographic=<words>`.
That is now **two guessed-Elsevier-DOI failures and two journal-year rescues in one session** (see
also `2026-11-06-investability-frictions-and-the-microcap-screen.md`), which promotes the
2026-10-07 lesson from a caution to a rule: *never guess an Elsevier DOI; enumerate the
journal-year.*

## Mechanism

The illiquidity premium is compensation for expected trading costs: an investor who will have to
pay a price impact to get out demands a higher expected return to get in. The measured object is
the cross-sectional return difference between illiquid and liquid stocks.

This note is filed for tonight's aim rather than for the premium itself — the folder already holds
the Amihud measure and its replication status
(`2026-08-29-amihud-illiquidity-measure-and-replication.md`). What this source supplies is a clean
answer to **what a size screen does to a measured cross-sectional effect**, because the paper
contains the screen as an explicit robustness test, states where the threshold sits, and reports
what happens to the estimate when it is applied.

The answer, in one line: **the measured premium is a function of where the screen is set, and the
paper and its principal challenger disagree about the answer because they set it in different
places.** Amihud et al. remove the smallest **10%** of firms by market capitalisation and find the
risk-adjusted premium remains positive and significant, with a point estimate that is "naturally
lower". The challenger (recorded below as unobtained) is reported to apply a far more aggressive
microcap screen and to find nothing. These are not contradictory claims about one quantity; they
are two readings of a **monotone relationship between screen severity and measured premium**, and
the lab's interest is in where its own panel sits on that curve.

A second mechanism point, and it is the one most directly aimed at this lab. The paper argues the
premium's **commonality across countries** is distinct from commonality in illiquidity itself, is
greater in globally-integrated markets, and survives controls for global return factors. So the
effect the illiquidity sort picks up is partly a **global** one, not purely a within-country
mispricing — which matters for a repo whose panel spans nine markets and whose one measured win in
this family was a *country demean*.

Third, and structurally important for how this folder reads its own results: the authors treat
**volatility as a confound to be designed out, not controlled for after the fact.** Because Illiq
is positively correlated with return volatility and volatility is itself known to affect expected
return, they pre-sort on volatility and sort on illiquidity *within* volatility buckets. The
reported premium is therefore volatility-neutral by construction.

## Construction recipe

Fully specified, and implementable on this repo's data as it stands.

- **Illiquidity measure.** `Illiq[i,t] = (1/N[i,t]) · Σ_d ( |r[i,d,t]| / vol[i,d,t] )`, where
  `vol` is **dollar** volume (shares traded × closing price), `|r|` the absolute daily return, and
  `N` the number of trading days **with non-zero volume**. This is Amihud (2002), applied
  country by country.
- **Estimation window.** A **non-overlapping three-month** window spanning months `t-3` to `t-1`.
- **Inclusion filters.** At least **10 valid daily observations** (both return and volume) in the
  three-month window, and at least **3 valid daily observations in month `t-1`**. Stock-days with
  zero volume are excluded from the average.
- **The sort, which is the part worth copying.** At the beginning of month `t`:
  1. Sort into **3 volatility terciles** on the standard deviation of daily return over `t-3`
     to `t-1`.
  2. Within each tercile, sort into **5 Illiq quintiles** over the same window.
  3. This gives **15 portfolios** with equal numbers of stocks. The "illiquid" quintile is the
     union of the three high-Illiq cells across volatility levels, and likewise for "liquid".
  - `IML` = illiquid-quintile return minus liquid-quintile return.
- **Holding and skip.** **Skip month `t`** entirely — the month immediately following formation —
  to avoid contamination by short-term reversal, then hold over months `t+1`, `t+2`, `t+3`.
- **Weighting — three schemes, reported side by side, and the choice is itself a screen.** (i)
  *return-weighted*, which is the Blume–Stambaugh / Asparouhova et al. correction for the upward
  bias that noisy prices induce in the expected returns of less-liquid stocks; (ii) *value-weighted*;
  (iii) *volume-weighted*. The authors are explicit that value-weighting "emphasizes more the
  evidence from large firms", quoting Hasbrouck: because capitalisation and liquidity are inversely
  related, value-weighted averages "tend to suppress variation in effective cost."
- **Cross-sectional alternative.** Fama–MacBeth regressions of returns on lagged `Illiq` and
  volatility (both over the rolling three-month window to `t-2`), with book-to-market and lagged
  returns over `t-2` to `t-4` and `t-5` to `t-13` as controls. The two estimators — portfolio
  spread and regression coefficient — are reported together throughout.
- **Data cleaning.** Datastream international equity data is cleaned following Ince–Porter (2006);
  the UK requires an extra filter for stocks with a high proportion of zero returns alongside
  positive volume (trades at the midpoint of a wide spread), per Lee (2011). The sample
  deliberately **retains stocks that ceased to exist during the period**.

## Robustness evidence (qualitative only)

- **Four estimation methods agree in sign**: the portfolio spread `IML`, its risk-adjusted version
  `αIML` against local and global factors, and the two Fama–MacBeth coefficients (plain and
  weighted). The average premium across countries is positive and significant in all of them.
- **Survives the 10% microcap screen, weakened.** Removing the smallest decile by market
  capitalisation — and, separately, by stock price — leaves the risk-adjusted premium positive and
  significant across all three weighting schemes, at a lower point estimate. The cross-sectional
  regression coefficients are likewise reported as robust to the same removal. **This is the central
  fact for tonight's purpose and it needs its qualifier kept attached: the screen tested is the
  smallest decile, which is a mild screen.**
- **Volatility is designed out rather than regressed out**, so the premium is not a repackaged
  volatility effect by construction. Momentum and reversal factors are reported as insignificant
  when added to the US `IML` regression.
- **Multi-market and multi-decade**: 45 countries, 22 years, developed and emerging, with the
  premium present in both groups and larger in emerging markets. Delisted stocks retained.
- **Known decay, and it is recorded in this folder already as a tension rather than imported here**:
  `2026-08-29-amihud-illiquidity-measure-and-replication.md` records Ben-Rephael–Kadan–Wohl (2015)
  reporting a *declining* liquidity premium over four decades, a McLean–Pontiff-shaped result. That
  note also flags, as an open worry, whether the family's signal is "a size/activity proxy, not
  price impact". Tonight's source **bears directly on that open worry and does not settle it**:
  removing the smallest decile does not kill the premium, which argues against the pure-size
  reading, but a decile is not a large-cap screen.
- **The principal challenger, recorded as a named pointer and NOT relied upon.**
  Cakici & Zaremba, *"Liquidity and the cross-section of international stock returns"*, **Journal of
  Banking & Finance 127, 106123 (2021)**, DOI `10.1016/j.jbankfin.2021.106123`, **42 Crossref
  citations (checked 2026-11-06)**; reported sample 45 countries, 1990–2020, which would make it
  `validation_overlap: true`. **The body was not obtained and nothing in it is summarised here.**
  Every channel failed or is already on `research/README.md`'s dark list: OpenAlex reports
  `is_oa: false, oa_status: closed, any_repository_has_fulltext: false` with **no repository
  location at all**, ScienceDirect and SSRN are the known Cloudflare refusals, and no author-hosted
  or institutional copy was found. What *is* on the record is that the publisher's own indexed
  keyword list for the article includes "microcaps" alongside Amihud's measure, turnover, bid-ask
  spread and zero-return days — i.e. the article demonstrably tests the microcap question with
  several liquidity proxies. **The direction of its conclusion is known here only from search-engine
  paraphrase and must be verified against the body before anything leans on it.** Per
  `research/README.md`'s rule, this is a pointer for a later session, not a finding.

## Implementability here

**Protocol v3, v2 panel.** The recipe above is implementable on this repo's data: `aux` supplies
`dollar_volume` and the daily range, `features.py` already has Amihud-style illiquidity helpers,
and the three-month window with a skipped month and a three-month hold is a cheap, low-turnover
cadence that v3's per-name cost model and charged drift can survive.

1. **The honest reading of this source for this panel is pessimistic, and it inverts the
   comfortable one.** The temptation is to read "survives the microcap screen" as reassurance. It is
   not. The screen tested removes the smallest **decile**; this repo's panel is the ever-members of
   **nine large-cap national indices**, which removes vastly more than a decile and sits far out on
   the severe end of the screen-severity curve — beyond anything this paper measured, and plausibly
   at or past where the challenger is reported to find nothing. **This source therefore provides
   little support for an illiquidity book on this panel, and should not be cited as if it did.**
2. **It collides with the lab's own measured result, and the collision should be stated rather than
   resolved.** `experiments/learnings.md` records `lv_illiq_region_relative` (2026-09-03) as a
   measurement win, and that candidate is a **country demean** of an illiquidity score. This paper
   is the best available external support for the *construction*: it finds the premium country by
   country, it finds genuine cross-country commonality in the premium, and its own estimates are
   within-country. So the region-relative form is the form the literature would have predicted.
   But the lab's win was measured under an earlier protocol, and `learnings.md` separately records
   that **both v2 family leads score zero skill under v3**. The two facts together mean the
   external literature supports the *shape* of that candidate while saying nothing about whether it
   survives v3 costs — and v3 is precisely where an illiquidity book should be expected to suffer,
   because the names it selects are the ones in the expensive liquidity tiers.
3. **The cost interaction is adverse and specific under v3, and it is sharper than it was under
   v2.** An illiquidity sort deliberately buys the names with the lowest trailing dollar volume.
   Under v3 those are exactly the names assigned the **30–40 bps per side** tiers rather than 15,
   so the long leg of an illiquidity sort is systematically drawn from the dearest part of the cost
   schedule. Any candidate in this family must be scored against that, and the paper's own
   value-weighted estimates — the ones that lean on large firms and "suppress variation in effective
   cost" — are the conservative column to compare with, not the return-weighted ones.
4. **The volatility pre-sort is the directly transferable construction idea, and it addresses this
   folder's single most-repeated confound.** `experiments/learnings.md` holds that the volatility
   level is this universe's survivorship artifact, and `SUMMARY.md` records five separate
   behavioural scores collapsing into momentum plus the volatility level. This paper's answer is
   structural: **sort within volatility terciles rather than regressing volatility out
   afterwards.** That is cheap, causal, needs only the daily closes, and makes the resulting score
   orthogonal to the volatility level *by construction* rather than by assumption — which is a
   stronger claim than any post-hoc control can make. It is worth applying to any candidate in any
   family that this folder suspects of being a volatility bet in costume, not only to illiquidity.
5. **The skip-month is not optional and the reason is specific.** Month `t` is skipped to avoid
   short-term reversal. Under protocol v3 fills already move to the next *real* close, which the
   program notes killed same-close reversal edges "by design" — so a candidate that does not skip is
   exposed to the residual of exactly the effect v3 was changed to remove. Keep the skip.
6. **Do not import the premium's magnitude, and note what is deliberately omitted here.** The
   paper's `αIML` point estimates are period-specific performance figures for 1990–2011 and are
   left out of this note under `research/README.md`'s anti-lookahead rule; only the sign, the
   significance and the *direction of change* under the size screen are recorded. The emerging-
   versus-developed ordering is likewise recorded as an ordering, not as a pair of numbers — and it
   is of limited use here regardless, since eight of this panel's nine indices are developed-market
   and the ninth is Hong Kong.

**Known pitfalls.** (a) `volume` in this repo's `aux` is a share count in native units and is **not**
forward-filled, so it is NaN on foreign holidays; the paper's own filters (≥10 valid days per
quarter, ≥3 in the final month, zero-volume days dropped) are the right shape for that and should be
reproduced rather than reinvented. (b) `dollar_volume` is `close_usd × volume`, which already matches
the paper's dollar-volume definition — do not rebuild it. (c) The paper's universe includes
microcaps and delisted names; this panel includes neither in any comparable proportion, so the
estimate is not transportable even in sign without the caveat in point 1. (d) The challenger is
unread: do not cite its conclusion.

## Annotation added 2026-11-09 — the threshold's location is the right question, and this panel has no threshold

This note's central finding is that **where the size screen sits decides the answer**. `#416`
(`notes/2026-11-08-the-mechanical-counterfactual-index-and-its-tracking-error.md`) says the lab's
`eligible` panel was not produced by a screen with a location: about **28%** of a committee index's
names fall outside the mechanical top-*N* by capitalisation, a comparable count of mechanical names
falls outside the index, and **the median excluded name is slightly larger than the median
constituent** (significant at 1%). No size threshold recovers membership.

Two consequences for reading this note against the lab's panel:

- The sensitivity analysis here — move the breakpoint, watch the premium move — has **no analogue**
  on `eligible`, because there is no breakpoint to move. A null measured on this panel is therefore
  not a reading at any particular point on the size axis; it is a reading on a differently-shaped
  selection, and `research/README.md`'s standing caution that a mechanism localised to small or
  thinly-traded names is excluded **by construction** is the relevant one, not a threshold argument.
- The illiquidity premium's own measurement on this panel inherits the same problem from the other
  side: the names that a size screen would have excluded and the names the committees excluded are
  **different sets with overlapping middles**, so neither this note's attrition arithmetic nor its
  value-share arithmetic transfers.

## Related

- `2026-08-29-amihud-illiquidity-measure-and-replication.md` — the measure itself and its
  replication record, including the declining-premium result; this note answers, partially, the
  open worry recorded there about whether the family's signal is a size proxy.
- `2026-11-06-investability-frictions-and-the-microcap-screen.md` — the same screen seen from the
  implementation side, with the 20th-NYSE-percentile convention and the
  one-fifth-of-names-versus-3%-of-value fact. Read together, the two sources say the screen removes
  most of the names, almost none of the value, and a substantial share of the measurable effect.
- `2026-11-06-index-membership-is-not-an-information-free-selection.md` — the third leg: what the
  screen selects *for*, beyond size and turnover.
- `2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — the demean operator this
  paper's within-country estimation supports.
- `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — relevant because this paper
  deliberately retains stocks that ceased to exist, which most of this folder's sources do not.
