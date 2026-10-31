---
title: "Tape painting decomposed — excessive buying versus depressed selling at the quarter boundary, and the window-dressing test that fails"
authors: Hu, McLean, Pontiff, Wang
year: 2014 (published); working paper read dated November 2008
venue: Review of Financial Studies (Tier 1)
url: https://doi.org/10.1093/rfs/hht057
citations: 91 (Crossref `is-referenced-by-count` by DOI, checked 2026-10-31; the Semantic Scholar DOI endpoint returns `not found` for this DOI and for the SSRN preprint 10.2139/ssrn.1786078, so no second index agrees or disagrees)
sample_period: 1999–2005 (seven years of institutional trade data, >300 institutions per year, 7–10% of CRSP dollar volume)
markets: US only — institutional equity trades (Abel Noser Solutions)
tier: A
validation_overlap: false
published_post_2018: false
---

**Access note, flagged rather than glossed.** The published *Review of Financial Studies* version
is closed (`oa_status: closed` on OpenAlex, no repository copy in its `locations` list). What was
read **in full** is the authors' own earlier working paper, *"Tape Painting: Excessive Buying versus
Depressed Selling"*, November 2008 draft, from the EFMA 2009 Milan programme
(`efmaefm.org/.../EFMA2009_0587_fullpaper.pdf`, 179 KB; `pdftotext -layout` → 102 KB of text, no
shift artifact, zero `( )` dropout). Same four authors, same data, same tests. **One substantive
difference between the versions is recorded explicitly below**: the published abstract's emphasis
("year-end price inflation derives from a *lack of institutional selling* rather than institutional
buying", and "no evidence of window dressing") is stronger than the working paper's, which reports
both channels. Where the two differ, this note follows the published framing and says so, because
that is the refereed statement.

## Mechanism

This is the trade-level counterpart to `notes/2026-10-31-quarter-end-marking-the-close.md`. That
paper infers marking-up from NAVs and prices; this one looks at who actually traded. The finding
that matters is a **decomposition of the period-end flow into two channels with the same price
effect and very different detectability**:

- **Excessive buying** — buying more of what you already own, into the close. This is the channel
  the earlier literature described. The authors find it is **atypical**: the average institution
  does not buy abnormally at the boundary. It appears **only** where the institution holds a large
  position, measured as *overweight* — the stock's weight in the institution's own portfolio minus
  the stock's weight in the market-value-weighted set of that institution's holdings.
- **Depressed selling** — *not* selling what you would otherwise have sold, so no sell-side price
  pressure arrives at the boundary. This is **pervasive**: it shows up whether or not the
  institution is overweight the name. The authors argue it dominates because it is cheaper on two
  counts — no transaction cost is paid to not trade, and an absence of selling is far harder for a
  regulator to detect than a burst of buying.

Both channels inflate prices, both are followed by **trade reversals in the following quarter**
(the suppressed sells arrive late, the excess buys are unwound), and both therefore produce
temporary inflation rather than a persistent level shift.

Two mechanism-level facts with direct consequences for this repo:

1. **The window-dressing hypothesis is tested separately and does not survive.** Window dressing —
   buying past winners and selling past losers so the *disclosed holdings list* looks good — is a
   different practice from tape painting, and it is the only one of the two whose signal is a
   **price** variable. The published version states that institutions are **not** more likely to buy
   high-past-return stocks or to sell low-past-return stocks at quarter- or year-end. In the
   working paper, past return (size- and book-to-market-adjusted three-month buy-and-hold) enters
   the buy/sell logits as a control while the *overweight × period-end* interaction carries the
   result. Either way the conditioning variable that works is **holdings**, and the conditioning
   variable that would be computable from prices does not.
2. **The mix is not stable, and shifted toward the harder-to-detect channel after the behaviour
   attracted regulatory and press scrutiny.** The authors report the two moves roughly cancelling
   in the aggregate buy ratio. Recorded here as a statement about the channel's **nature** — a
   deterrable, partly illegal practice whose observable form adapts — not as a dated event. The
   consequence for research is that the *form* of any surviving period-end flow is a moving target,
   so a construction calibrated to one form is not safe to carry forward.

## Construction recipe

- **Overweight is the cross-sectional conditioner, and it is defined inside each holder's own
  portfolio**: `OW = W − M`, where `W` is the stock's value share of the institution's portfolio and
  `M` is the stock's share of the *market* values of the same set of stocks. `OWD` is the indicator
  that `OW > 0`. The tested object is the **interaction** `OWD × QEND` (and `× YEND`) in a logit for
  the probability of buying, and the same with the sign reversed for selling. The level effects
  (`QEND`, `YEND` alone) are the aggregate behaviour; the interaction is the mechanism.
- **The period-end dummies are the same joint set as in the companion note** (`YEND`, `QEND` for
  non-fourth quarters, `MEND` for non-quarter month ends), and the sample is restricted to the last
  trading day of each month so the comparison is boundary-against-boundary rather than
  boundary-against-mid-month.
- **Errors clustered on the institution**, since the same holder appears in many stock-days.
- **The reversal test is the identification device worth transplanting**: if a boundary trade is a
  reporting artefact rather than information, the *same holder's* flow should reverse in the next
  period. A boundary effect with no subsequent reversal in the same units is not this mechanism.
  For a price-only lab this translates into: **require the next-period reversal as part of the
  hypothesis, not as a robustness check** — the round-trip statistic in the companion note is the
  price version of the same requirement.

## Robustness evidence (qualitative only)

Large sample for its type (seven years, several hundred institutions per year, a high single-digit
to low double-digit percentage of market dollar volume), published in a Tier-1 journal, and the two
channels are each shown on several cuts (large and small institutions alike). The decomposition is
corroborated by the reversal tests rather than asserted. Limits: **one market**, one data vendor
whose coverage is a selected set of institutions that chose to use a transaction-cost analysis
service, and no replication study in the Hou–Xue–Zhang or Jensen–Kelly–Pedersen sense. The
instability of the channel mix, documented by the authors themselves, is the clearest internal
evidence of decay risk in this vein — and it is decay in *form*, which is worse for a strategy than
decay in size, because it invalidates the construction rather than just shrinking the payoff.

## Implementability here

**This source is the reason to close the quarter-boundary flow vein rather than merely discount
it.** It is the one paper in the vein that asks, with trade data, whether the price-only signal
exists — and answers no.

1. **The admission criterion's clause (c) fails on the evidence, not on data availability.** It is
   tempting to read "we cannot see holdings" as a mere data gap that a proxy might bridge. This
   paper removes that hope from the other side: the proxy variable a price-only lab would use
   (past return, the window-dressing signal) is tested directly and does not drive period-end
   institutional trading. There is no partial-credit version of the construction here.
2. **The dominant channel is an absence of trade, which has no price-space signature this repo can
   see.** Depressed selling shows up as *missing* sell pressure. In a close-only panel, missing
   pressure is indistinguishable from nothing happening; it is visible in trade data and not in
   returns. Even the dollar-volume panel v2/v3 supplies is the wrong instrument — the authors'
   finding is that period-end volume effects are concentrated at the very end of the session, which
   a daily volume total cannot isolate.
3. **If a human ever wants a free screen rather than a trial**, the transferable one is the
   **reversal requirement**: any quarter-boundary effect this lab measures should be required to
   show the next-period reversal in the same units before it is treated as flow. The lab's
   2026-10-09/10 measurement (a higher return in the month *after* a quarter-end) is a one-sided
   window statistic with no reversal leg, so it is currently consistent with both a flow story and a
   mid-month drift story. Measuring the round-trip version costs no trial and would settle which.
4. **Carry the instability as a general prior, not as a fact about this family.** A mechanism that
   is (i) partly illegal, (ii) detectable, and (iii) executed by agents who can switch to a
   less detectable form is a mechanism whose *construction recipe* expires. This is a stronger
   reason to down-weight an institutional-gaming source than the usual McLean–Pontiff
   publication-decay discount, and it applies to every member of this vein.

**No trial proposed.** The honest summary of the pair of US sources: the quarter boundary is real
and distinct from the month boundary, and the part of it that could be traded from prices alone is
the part the evidence says is not there.

## Related

- `notes/2026-10-31-quarter-end-marking-the-close.md` — the NAV- and price-level source this one is
  the trade-level test of; its section IV.C holdings result and this paper's `OWD × QEND`
  interaction are the same finding from two data types.
- `notes/2026-10-31-quarter-ending-month-momentum-seasonality.md` — **direct tension**: that source
  attributes a quarter-ending-month return pattern to window dressing, which this source's own
  window-dressing test rejects in trade data. The tension is recorded there rather than resolved.
- `notes/2026-10-31-nav-inflation-outside-the-us-china.md` — a second market where the holdings
  conditioner again carries the effect and the price-only cross-section again does not.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the standard decay discount, which this
  note argues is the *weaker* of the two decay arguments available in this vein.
- `experiments/learnings.md` 2026-10-09/10 and 2026-10-15/16 — the lab's quarter-boundary
  measurement and the closure of its fully-invested form on turnover.
