---
title: "Stock Return Seasonalities and the 'Tax-Loss Selling' Hypothesis — the a-priori objections, and a market whose tax year ends in June"
authors: Brown, Keim, Kleidon, Marsh
year: 1983
venue: Journal of Financial Economics 12(1), 105–127 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/0304-405x(83)90030-2
citations: "258 (Crossref `is-referenced-by-count`, checked 2026-10-07); 270 (OpenAlex, checked 2026-10-07); 387 (Semantic Scholar, checked 2026-10-07)."
sample_period: "March 1958 to June 1981 (Australia), with a January 1974 – June 1981 subperiod reported separately because it contains more small firms"
markets: "Australia — a merged file of 1,924 ordinary shares from three monthly databases (industrial, mining/oil, and the AGSM Share Data File); ten equal-weighted size-decile portfolios rebalanced monthly on market value two months prior; 281 to 937 names with available returns depending on the month. US evidence discussed from the then-current literature, not re-estimated."
tier: A
validation_overlap: false
published_post_2018: false
read: "Full text, MIT Sloan School working paper 1378-82 (July 1982, last revised November 1982), read as the Internet Archive's OCR text layer (`stockreturnseaso00mars_djvu.txt`, 72 KB, located via `archive.org/metadata/stockreturnseaso00mars` and fetched from the `server`/`dir` the metadata names). This is the working version of the JFE 1983 article; it carries all six sections, the data description, the Australian tax discussion and the conclusions. OCR noise is present in headers and marginalia (occasional interleaved garbage lines) but the body prose is clean; **table values were not relied on**, and nothing below rests on a number read out of the OCR."
---

## Mechanism

This is the paper that states the preconditions for the tax-loss-selling explanation and then tests
the one prediction that distinguishes it from everything else: **if the seasonal is caused by the
tax year, it should move when the tax year moves.**

**The hypothesis as the authors reconstruct it.** Tax law encourages holders to sell names that have
declined so the loss can be offset against taxable income. Small-cap names are the likely
candidates, because higher return variance means a higher probability of a large decline. Crucially
the argument **requires that investors wait until the tax year-end** to sell their losers; the
year-end selling pressure depresses those prices, the pressure disappears after the year-end, and
prices rebound — producing high small-firm returns at the start of the new tax year.

**The four a-priori objections, which are the durable content.** The authors' "analysis of the
arguments" section is independent of their data and transfers to any universe:

1. **Realization is not a demand shift.** Even granting heavy tax-related selling in a name, that
   does not imply a price decline. A price-pressure effect requires the individual stock's demand
   curve to slope downward — i.e. the stock to be *unique*. If securities with similar risk
   characteristics are close substitutes (the authors cite Scholes), the demand curve is essentially
   horizontal and tax-related selling moves no price at all.
2. **The proceeds have to go somewhere.** A sale made purely for tax reasons, as opposed to a desire
   to liquidate, is followed by reinvestment, and portfolio requirements make a
   similar-characteristic replacement the natural destination. Even where wash sales are barred,
   brokers publish lists of substitutes to facilitate "tax exchanges", which weakens any price
   pressure. The authors quote Sharpe's textbook conclusion directly: year-end volume in names with
   large price moves is high, but **no major fall in prices appears to result**, because buyers
   recognise the sellers are motivated by the tax code and not by undisclosed bad news.
3. **The predicted December price decline is not there.** If one-sided pressure were real, small-cap
   prices should fall generally in December absent any detrimental information — and the contemporary
   US evidence the authors cite reports general price *increases* for those shares in December.
4. **The low price is trivially avoidable and exploitable.** Anyone selling slightly ahead of the
   rush avoids the pressure loss, and anyone not forced to sell stands to earn large excess returns
   by buying. And the premise itself is weak: why concentrate at the year-end rather than realize
   losses as they occur? The authors cite Constantinides' result that investors have an incentive to
   realize losses immediately, which would leave only a fraction of the flow at the deadline.

**The test, and its outcome.** Australia's tax year runs 1 July to 30 June. Australian taxpayers
classified as "share traders" (which includes all taxpaying financial institutions automatically)
pay ordinary rates on all realized gains and may **deduct all realized losses regardless of holding
period** — with no equivalent of the US annual cap on loss deduction. So for that class the
tax-loss incentive is, if anything, stronger than in the US, and the hypothesis predicts a July
small-firm effect at least as pronounced as the US January one. (Taxpayers classified as
"investors" are largely outside the capital-gains net on shares held a year or more, which is the
reason the prediction is about traders.)

What the data show is **more complex than the hypothesis predicts, in a specific way**: pronounced
seasonals in raw returns occur in **both December–January and July–August**, with the largest and
roughly equal effects in **January and July**. Meanwhile the Australian small-firm premium itself is
large and **roughly constant across months**, in contrast to the US pattern where a large share of
the annual size effect is concentrated in January.

**The integration escape, and why it is self-defeating.** The obvious rescue is that a US
tax-induced January effect leaks into Australian prices through integrated capital markets. The
authors close it with an argument whose structure is worth keeping: the tax-loss hypothesis
*itself* depends on the **absence** of arbitrage by investors not forced to sell. A market
integrated enough to transmit a US January seasonal into Australian penny stocks cannot
simultaneously be segmented enough to let the original US mispricing form. The escape and the
mechanism cannot both hold.

And the residual puzzle survives either way: if January and July are the two tax year-ends, **what
causes the December and August premiums?** A continuous or non-trading-lagged tax effect might
explain August as a spillover from July, but then the absence of any February seasonal in either
market, and the December effect, are unexplained.

The authors' summary: the Australian evidence is difficult to reconcile with tax-loss selling; the
original hypothesis is *consistent with* the US January premium but the story becomes much more
complicated once Australia is included; and it is more promising to look for **equilibrium** causes,
perhaps by comparing the relative timing of events other than tax years across the two countries.
They reinforce this with the then-available finding that the US January effect is significant in
almost every year over a half-century span including pre-war periods when personal tax rates were
low and the loss-offset benefit smaller — i.e. **the magnitude of the January effect does not appear
sensitive to variation in the tax rate.**

## Construction recipe

No portfolio. The reusable constructions are the test design and the size-portfolio mechanics:

- **The alignment test.** Pick markets whose tax year-ends differ. Form size-decile portfolios
  within each market. Ask whether the small-firm premium is concentrated in the month following
  *that market's* tax year-end. The prediction is sharp, directional, and pre-registerable; the
  hypothesis survives only if the window **moves with the jurisdiction**.
- **The segmentation consistency check.** Before accepting a cross-border transmission explanation
  for any frictional effect, ask whether the transmission channel requires more market integration
  than the original friction requires to be absent. If so, the explanation is self-undermining and
  should be rejected on logic rather than tested.
- **Size portfolios.** Ten deciles on market value of equity, updated monthly, ranked on the value
  **two months prior** rather than the previous month (a lag that avoids using a price
  contemporaneous with the return being measured), equal-weighted within decile. The authors also
  report a subperiod chosen for containing more small firms, and use Dimson betas as a robustness
  variant given thin trading.
- **Raw returns, not risk-adjusted, for the seasonal claim.** The seasonal pattern is reported in
  raw returns; the authors treat beta adjustment as a separate robustness exercise, partly because
  thin trading makes betas unreliable in exactly the decile where the effect lives.

## Robustness evidence (qualitative only)

Strengths: a multi-decade sample in a market with an institutional feature (a mid-year tax year-end,
plus an uncapped loss deduction for one taxpayer class) that makes the test possible at all; a
second market's size-decile construction built to match the US studies it is arguing with; a
subperiod split chosen on a data-availability ground rather than a results ground; and — unusually —
the paper's central argument is *a priori* and survives independent of its own estimates. The
authors' conclusion is a negative result about a popular explanation, reported plainly, which is the
kind of source this folder should weight highly.

Limits: one additional market, so the alignment test has an *n* of two tax regimes; thin trading in
the small deciles, which the authors handle with Dimson betas rather than resolve; and the Australian
tax treatment is split across two taxpayer classes, so the fraction of the market actually facing
the tax-loss incentive is an assumption rather than a measurement. The paper also predates the
investor-level evidence that the flow exists at all, which does not rescue the price step but does
establish the volume step (see Related).

**The tension in this cluster, stated rather than resolved.** Three sources here find the
behavioural flow is real, is concentrated at the tax year-end, and correlates with returns in small
caps; this one finds the cross-country *return* pattern does not line up with tax years and that the
effect's magnitude is insensitive to tax rates. Both can be true: the flow can exist and still not
be what moves prices, which is exactly the gap Constantinides' theory identifies. Graded by the
folder's [2026-10-04] sign-versus-magnitude rule, this is **not** a sign disagreement — nobody
disputes that losers are sold in the final days of the tax year. It is a disagreement about whether
that flow **has a price consequence**, i.e. about objection (1): whether the demand curve is flat.
That makes the arbitrating evidence *substitutability*, not more seasonality data — and
`notes/2026-09-22-arbitrage-risk-substitute-portfolios.md` is the folder's existing note on exactly
that question.

## Implementability here

**This note's job is to stop a trial, and to say what would have to be true for one to be worth
spending.**

- **It kills the cheapest version of the idea.** A candidate that tilts toward prior-year losers in a
  December/January window on a global universe is, on this evidence, betting on a mechanism whose
  one distinguishing prediction has failed a direct test, and whose magnitude is reported insensitive
  to the tax rate that supposedly drives it. It is not refuted — but it is Tier-A-contested, and
  `program.md` caps this family's budget tightly enough that a contested mechanism should not be the
  first thing bought.
- **It gives the lab a test it can actually run, because this universe has the required variation.**
  The repo spans fifteen regions and nine national indices. The alignment prediction is therefore
  testable *within* one panel, which is better than the paper's own *n* of two: does each region's
  loser-reversal window track that region's own tax year-end, or do all regions show the same
  calendar window? A common window across regions with differing tax years is evidence against the
  tax mechanism; region-specific windows are evidence for it. **This is free and train-only** — it
  scores no portfolio — and it is the discriminating measurement the whole cluster turns on. Two
  caveats to declare up front: the per-region tax-year calendar is an external input the repo does
  not hold, and USD conversion books an FX factor into any region-level return
  (`notes/2026-09-10-currency-component-in-usd-converted-returns.md`), so the region effect must be
  measured on demeaned or FX-aware returns.
- **Objection (1) is the binding one here and it bites harder on this universe than on the paper's.**
  Protocol v2's pool is ~1,400 names that were ever members of nine large-cap indices plus 42 ETFs.
  Close substitutes — same region, same index, similar beta — are abundant by construction, which is
  the flat-demand-curve case. The effect the whole literature locates in small, thinly traded names
  is precisely what a point-in-time large-cap index universe excludes.
- **One transferable detector, worth more than the seasonal itself.** The integration argument
  generalises: *a frictional or behavioural explanation that must travel across a border to fit the
  data is self-undermining, because the transmission requires the integration whose absence the
  friction requires.* This folder has already met this exact shape once, in the SAD exchange
  (`notes/2026-10-05-sad-weather-exchange-and-the-integration-escape.md`), where market integration
  is likewise both the rescue and the refutation. Two independent Tier-A literatures reaching for the
  same escape and hitting the same wall makes it a rule rather than a coincidence: **when a candidate
  is motivated by a local friction and the lab's universe is global, check whether the motivating
  story needs segmentation that the universe does not have.**

## Related

- `notes/2026-10-07-tax-trading-theory-and-the-price-pressure-condition.md` — Constantinides, whose
  theoretical objections are nearly identical to this paper's objections (1), (2) and (4), reached
  independently and from an optimising model rather than from a priori reasoning.
- `notes/2026-10-07-tax-loss-trading-and-wash-sales-investor-level.md` — the investor-level evidence
  this paper could not have had, which establishes the volume step and the naivety condition but not
  the price step.
- `notes/2026-10-07-past-return-consistency-and-the-seasonal-in-the-past-return-relation.md` — the
  US cross-sectional evidence on the other side, including a tax-rate-regime interaction that is in
  direct tension with this paper's "magnitude insensitive to the tax rate" point.
- `notes/2026-10-05-sad-weather-exchange-and-the-integration-escape.md` — the folder's other
  instance of the integration escape, and the reason it is now a detector.
- `notes/2026-09-22-arbitrage-risk-substitute-portfolios.md` — the literature that arbitrates
  objection (1): whether arbitrage flattens demand curves, and where it fails to.
- `notes/2026-10-04-halloween-six-month-seasonal.md`, `notes/2026-10-04-sad-daylight-seasonal-mechanism.md`
  — the other calendar mechanisms whose cross-country structure is the evidence, not a robustness
  check.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md` — the thin-trading problem this paper
  handles with Dimson betas, and which this repo's 15-region daily panel has in its own form.
- Tension with `experiments/learnings.md` [2026-09-01]: that entry closes the *timing* half of
  `seasonality-calendar` for a long-only book. This note closes something different and
  complementary — the *motivating mechanism* for the cross-sectional half — and it does so on
  Tier-A contested evidence rather than on a structural argument, so it is a discount on the
  mechanism's prior, not a proof.
