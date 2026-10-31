---
title: "Quarter-end NAV inflation outside the US — a second-market test, and the incentive sign that flips with the local flow–performance relation"
authors: Shackleton, Yan, Yao
year: 2020 (published; the accepted manuscript read is dated November 2018)
venue: European Financial Management (Tier 2 — peer-reviewed finance journal)
url: https://doi.org/10.1111/eufm.12207
citations: 7 (Semantic Scholar by DOI and Crossref `is-referenced-by-count` agree, both checked 2026-10-31)
sample_period: 2004-01-02 – 2013-12-31
markets: China only — SHSE/SZSE tradable A-shares; up to 276 active equity funds plus closed-end funds
tier: B
validation_overlap: false
published_post_2018: true
---

Read **in full** from the Lancaster University green open-access accepted manuscript
(`eprints.lancs.ac.uk/128402/1/NAV_Inflation_and_Impact_on_Performance_in_China.pdf`, 704 KB, CC
BY-NC; `pdftotext -layout` → 100 KB of clean text, `" the "` count 531, no shift artifact). The
publisher version is Wiley and was not attempted. **Access lesson worth keeping: a Lancaster
`eprints` record names its accepted-version PDF path in full and served it on the first try** —
this is a green-OA channel the folder's README has not recorded.

This is the non-US leg of tonight's quarter-boundary session, taken because the lab's
pre-committed criterion required the vein to be abandoned if the quarter-end effect turned out to
be "a US-institutional artefact". It is not a US artefact. It is also not reachable here, for the
same reason as in the US.

## Mechanism

The paper runs the Carhart–Kaniel–Musto–Reed design (see
`notes/2026-10-31-quarter-end-marking-the-close.md`) on a second, structurally different market and
reaches the same conclusion about **where** the effect sits in the calendar and **what** conditions
it in the cross-section:

- Equity funds' returns are abnormally high at **quarter-ends and especially year-ends**, with a
  reversal at the turn, and the effect at **month-ends that are not quarter-ends is almost
  insignificant**. That is an independent-market replication of the month-versus-quarter contrast,
  which is the single most load-bearing fact for this folder's purposes — the quarter boundary is
  a distinct object, not a relabelling of the month boundary, in two markets now.
- The stock-level test sorts stocks by **mutual-fund ownership ratio** into quintiles and finds the
  price-inflation pattern in the **highest-ownership quintile and almost nowhere else**. Again the
  conditioner is holdings.
- Closed-end funds show it too, which matters because closed-end funds have no flow to attract:
  the authors use this to argue the behaviour is not purely a flow-chasing phenomenon.

**The genuinely new mechanism finding, and the one with transfer value beyond this family:** the
*direction* of the cross-sectional incentive is not a property of the calendar but of the **local
flow–performance relation**, and it flips across markets.

| Market | Which managers inflate | Why |
|---|---|---|
| US | the **best** performers | flow–performance relation is convex, so one more basis point of rank is worth a lot |
| Australia, China | the **worst** performers | flows respond weakly to performance rank; the live incentive is instead the inverse relation between past performance and the probability of being replaced, so the manager under threat of dismissal is the one who pumps |

The authors report little evidence of best-performing Chinese funds inflating, explicitly
inconsistent with the US evidence, and attribute it to Chinese fund flows being far less sensitive
to performance ranking. So "leaning for the tape" and "pumping to keep your job" are two different
incentive channels producing the same calendar footprint with **opposite cross-sectional
signatures**. A researcher who imports the US sign into another market gets the sign wrong.

## Construction recipe

Essentially the companion note's recipe, re-run, with two additions worth recording:

- **Same joint period-end dummy set** — `YEND`, `YBEG`, `QEND`, `QBEG`, `MEND`, `MBEG` — with the
  market return as the single explanatory variable alongside, so the dependent variable is a
  market-adjusted fund or portfolio return. The month-end dummies again exclude quarter-ends. This
  is the second paper tonight to use exactly this specification; treat it as the standard form for
  any period-end test.
- **Ownership-quintile portfolios, value-weighted within quintile**, where the ownership ratio is
  (shares held by funds × price) / total market value of the stock, ranked at each semiannual
  disclosure. The regression above is then run on each quintile's return series. The *contrast
  across quintiles* is the test; the level in any one quintile is not.
- **Fund-performance quintiles for the incentive test**, with the prediction stated in advance of
  the sort (US: top quintile; here: bottom quintile). The authors also check the middle quintiles
  explicitly to rule out a free-rider reading — if only one group pumped and others merely benefited
  from the price impact, the middle quintiles would look like the pumpers. They do not.

## Robustness evidence (qualitative only)

A decade-long sample in a market with a rapidly expanding fund industry, with the result shown on
open-end funds, on closed-end funds, and on the held stocks themselves — three partly independent
cuts, which is the same multi-channel corroboration strategy as the US source. The paper is
refereed in a credible journal. Against it: **one market**, a **low citation count** (single digits
in both indices), a **post-2018 publication date** (so the standard novelty discount applies), and
a market whose microstructure, retail share and regulatory regime differ sharply from this repo's
panel. The authors themselves raise and partly address the possibility that the fund-return pattern
is *reporting* manipulation rather than price manipulation — the holdings-based price test is their
answer to it, and it is a good one, but it is also the test whose signal this repo cannot compute.

Taken with the US sources, the fair qualitative statement is: **the quarter-end NAV-inflation
phenomenon replicates across markets; its incentive direction does not.**

## Implementability here

1. **This source settles the criterion's abandonment clause in the vein's favour and the rest of the
   criterion against it.** The quarter-end effect is *not* a US artefact, so the vein cannot be
   dismissed as parochial. But in the second market the signal is again **fund ownership**, and in
   the second market the price-only cross-section is again where the effect is *absent* — low- and
   mid-ownership quintiles show almost nothing.
2. **The market studied is at the opposite end of the panel's spectrum, which weakens the transfer
   further rather than strengthening it.** This repo's nine indices are large-cap developed-market
   (and Hong Kong) constituents; the A-share market in this sample is retail-dominated with a
   measured size premium. Evidence that pumping is detectable there is weak evidence that it is
   detectable in the Nikkei 225 or the SMI. The folder's own README rule applies: a mechanism whose
   literature localises it to retail-held or thinly traded names is excluded from this panel **by
   construction**, so a null here would be uninformative.
3. **The transferable finding is the sign rule, and it is free.** *The cross-sectional direction of
   an agency-driven calendar effect is set by the local flow–performance relation, not by the
   calendar.* Two consequences for this lab, both cheap: (i) any future candidate that conditions on
   an agency mechanism must not assume one sign across a nine-market panel — the sign is a
   market-level parameter, and pooling markets with opposite signs averages the effect toward zero,
   which is a *predicted* null rather than an informative one; (ii) more generally, this is a
   worked instance of a pattern this folder has recorded for other mechanisms — **a mechanism can
   replicate while its construction does not**. Add it to the standing list of reasons a
   cross-market pooled test can be uninformative.
4. **No trial proposed, and no screen either.** Unlike the momentum-seasonality note, there is no
   free measurement that would settle anything, because the conditioning variable does not exist in
   this repo's data at all. The right outcome is to record the vein as closed on evidence and to
   stop spending nights on it.

## Related

- `notes/2026-10-31-quarter-end-marking-the-close.md` — the design this paper re-runs; its
  capitalisation gradient and this paper's ownership gradient are the two cross-sectional facts that
  between them close the price-only route.
- `notes/2026-10-31-tape-painting-buying-versus-selling.md` — the trade-level decomposition, and the
  window-dressing rejection.
- `notes/2026-10-31-quarter-ending-month-momentum-seasonality.md` — the only price-only construction
  in the vein, and the free screen that would close it on this panel.
- `notes/2026-09-02-turn-of-month-payment-cycle.md` — the month boundary, whose insignificance at
  non-quarter month ends this paper independently confirms in a second market.
- `research/README.md` — the "large-cap national indices" clause, which is what makes point 2 a
  structural exclusion rather than a sampling complaint.
