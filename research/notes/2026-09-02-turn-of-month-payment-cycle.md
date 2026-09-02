---
title: "The turn-of-the-month effect as a payment-cycle liquidity phenomenon — Ogden's hypothesis and its institutional test"
authors: Ogden (1990); Etula, Rinne, Suominen, Vaittinen (2020)
year: 1990; 2020
venue: Journal of Finance (Tier 1); Review of Financial Studies (Tier 1)
url: https://doi.org/10.1111/j.1540-6261.1990.tb02435.x — https://doi.org/10.1093/rfs/hhz054
citations: 263 for Ogden (Semantic Scholar by DOI, checked 2026-09-02); 61 for Etula et al. (OpenAlex by DOI, checked 2026-09-02; the Semantic Scholar DOI endpoint returns "not found" for this DOI)
sample_period: 1969–1986 (Ogden); 1980–2013 international, with weekly mutual-fund flow data July 1995 – December 2013 (Etula et al.)
markets: US stock index returns (Ogden); G10 plus other industrialized countries — equities, Treasuries and corporate bonds, ~30 country equity markets (Etula et al.)
tier: A
validation_overlap: false
published_post_2018: true
---

Etula et al. read **in full** from the authors' working-paper version (28 December 2017,
`wp.lancs.ac.uk/fofi2018`), published as RFS 33(1), 75–111. Ogden recorded **from its published
abstract only** (closed access at Wiley; abstract read verbatim from the publisher's landing page
for the DOI) — it is used here for the hypothesis it names, which the second source tests directly.

This note takes the **calendar half of `seasonality-calendar`**, which `SUMMARY.md` has had as its
top-priority gap. That half was closed by the lab on 2026-09-01, on a structural argument, and the
note is written against that closure: it exists because the closure's own stated precondition is
one this literature says can be met, in a window the lab's screen did not test.

## Mechanism

Ogden's hypothesis is that the turn-of-the-month return pattern is not a calendar rule but a
**payment-cycle** phenomenon: payments in the US economy — wages, pensions, dividends, interest —
are standardised to cluster at the turn of each calendar month, which produces a surge of
investable cash and a corresponding surge in stock returns at that point in the month. Two
auxiliary predictions come with it, and they are what make it a mechanism rather than a
description: the effect should be **greater following December**, and it should **vary inversely
with the stringency of monetary policy** (tighter money, less liquidity released into the cycle).
That second prediction is the reason to prefer this account over a bare calendar dummy — a calendar
dummy has no conditioning variable.

Etula et al. test the institutional side of the same cycle and sharpen it into something with a
**timing restriction imposed by settlement conventions rather than fitted to returns**. Institutions
(pension funds, mutual funds, corporate treasuries) must have cash *in hand* on the payment date.
Under the 3-day settlement convention prevailing over their sample, an institution needing cash on
the morning of the last business day of the month (T) must sell **by the close of T−4**. So the
cycle decomposes into three windows, in this order:

1. **T−8 to T−4 — liquidity-motivated selling.** Institutions raise cash. Price pressure is
   *negative*; this is the window returns are depressed in.
2. **T−3 to T+3 — positive reversal.** Selling pressure eases and newly cleared money is
   deployed. This is the window conventionally labelled "the turn-of-the-month effect".
3. **T+4 to T+8 — negative reversal.** The cycle completes.

The authors verify the causal link rather than asserting it: the **Treasury market, with a 1-day
settlement convention, permits liquidity-driven selling until the close of T−2**, and its yield
pattern is correspondingly shifted later than the equity market's, which peaks around T−4.
Corporate bonds, on a 3-day convention, show hybrid behaviour they attribute to arbitrage against
Treasuries. They also exploit differences in when the 3-day convention was adopted across
countries. The pressure window's location is therefore **predicted by a market's settlement rule**,
which is an identifying restriction, not a free parameter.

Two further mechanism-level findings:

- **The pattern is stronger in countries with larger mutual-fund sectors** — a cross-sectional
  prediction about *which markets*, tied to who bears the month-end liquidity need.
- **Limits to arbitrage are real and asymmetric.** The hedge-fund sector as a whole did not
  mitigate the pattern on average; it contributed to it, plausibly because hedge-fund vehicles face
  the same month-end flow conventions. Liquidity provision appears only when conditioning on hedge
  funds' own funding conditions. So the mechanism has a reason to persist that does not depend on
  it being unknown.

## Construction recipe

- **Index the calendar in business days relative to the month boundary**, not in calendar days:
  T = last business day of the month, with T−8 … T+8 the trading days around it. Holiday calendars
  differ by market, so the indexing must be per-instrument, computed from that instrument's own
  observed trading days.
- **The three windows above are the unit of construction.** The selling window (T−8 to T−4), the
  positive-reversal window (T−3 to T+3) and the negative-reversal window (T+4 to T+8) are separate
  objects with different predicted signs. A single "turn-of-the-month" dummy pools the first two
  and destroys the contrast.
- **Offset the windows by the market's settlement convention.** The recipe as published sits under
  a 3-day convention; US equity settlement shortened to 2 days in 2017, which shifts the predicted
  last-sale day one day later (T−3 rather than T−4). Treat the offset as a parameter to verify
  against the data, not as a constant to hard-code — this is the source's own logic applied
  forward.
- **The identifying test is the cross-market one**: instruments in markets with shorter settlement
  cycles should show the pressure window closer to the month end. With 15 regions in this universe
  that is checkable.
- Ogden's conditioning variable — monetary stringency — is a second identifying test, but needs a
  policy-rate series this repo does not have.

## Robustness evidence (qualitative only)

Multi-decade and explicitly multi-market: the authors report the reversal patterns across a broad
set of industrialized countries and state that the reversals are statistically significant in
**22** of them, which is unusually wide cross-market corroboration for a calendar effect. The
mechanism is corroborated by three independent channels rather than by the return pattern alone —
settlement-convention differences across asset classes, the timing of institutional trades in
trade-level data, and mutual-fund flow data. The turn-of-the-month effect itself is one of the
oldest documented calendar regularities and has a long prior literature, which cuts both ways: it
is well replicated, and it is exactly the sort of effect the data-snooping critique of calendar
rules targets. Neither source is a replication study in the Hou–Xue–Zhang or Jensen–Kelly–Pedersen
sense, and neither reports post-publication decay for this effect; the RFS paper is post-2018
published, so the usual novelty discount applies to it.

## Implementability here

**The honest headline: the lab has already closed this half of the family, and this source does not
overturn the closure — it identifies one window inside it that the closing screen did not test.**

`learnings.md` (2026-09-01) closed the calendar half structurally: a long-only book with
`max_leverage = 1.0` whose only alternative is cash can exploit a calendar effect **only if the
complement window's return is at or below zero**, and the screen found the complement still earning
+11% to +14%/yr, so sitting it out forgoes more than concentration gains. The screen tested
turn-of-month as **(before = 1, after = 3)** — that is, the window T−1 to T+3.

That is window 2 above. The lab's in-window is the source's *positive reversal*, and the lab's
"complement" pools the source's **negative-pressure window (T−8 to T−4)** with all the ordinary
mid-month days. The source's claim is precisely that those are not the same object: the pressure
window is where the *depressed* returns are, and the correlation structure the authors report is
that the positive-reversal returns are, in significant part, reversals of the preceding days' price
pressure. So:

1. **The pre-registered test, stated before any data is touched.** Measure the mean daily return of
   the **T−8 to T−4 window alone** on train, per the lab's own stated precondition ("check the
   complement window's sign before proposing any timing overlay here"). If it is at or below zero,
   the closure's binding condition is met for a *narrow* overlay — hold cash for ~5 business days a
   month rather than for the whole complement — and the cost arithmetic changes because the
   overlay's turnover is ~12 round trips a year against the 24 the closing screen priced at
   3.60%/yr of drag. **If T−8 to T−4 is positive on this universe, the family closes a second time
   and the closure should be recorded as final rather than re-litigated.** This is a free
   measurement and it decides the question either way.
2. **The always-invested form is the one that dodges the closure entirely, and it is available
   here.** The structural argument binds only because the alternative to being in the market is
   cash. It does not bind on a **cross-sectional** tilt: the source predicts the effect is stronger
   in markets with larger mutual-fund sectors and that the pressure window's *timing* differs by
   settlement convention. A fully-invested book that rotates **between regions** across the month —
   overweighting markets whose pressure window has passed, underweighting those in it — never holds
   cash, so `max_leverage = 1.0` is not binding on it. With 42 ETFs across 15 regions this is
   reachable and it is the form the lab has not tried.
3. **Turnover is the thing that kills the cross-sectional form, and it should be priced before it
   is built.** A book that re-sorts on a within-month day index rotates several times per month.
   `learnings.md`'s existing cost measurements put a 24x-annual overlay at 3.60%/yr; a
   multiple-times-per-month regional rotation is worse. The realistic version is a **low-intensity
   tilt** — a modest weight adjustment on an existing book — not a full rotation, and it should be
   specified as an overlay on a champion book rather than as a standalone leg.
4. **The 1-day execution lag matters more here than anywhere else in the folder.** These are
   windows of 3–5 business days. The engine's lag consumes a fifth to a third of a window, which is
   the asymmetry the 2026-08-30 lead-lag session recorded in general terms and which bites hardest
   at exactly this horizon. Any window-based construction must be defined so that a signal computed
   at the close of day d is *acted on* at d+1 and still lands inside the intended window.
5. **The daily-frequency seasonality result in the companion note is the cleaner cousin.**
   Keloharju–Linnainmaa–Nyberg find daily-frequency seasonality that is *uncorrelated* with the
   monthly kind. If a within-month day-index effect is real on this universe, it is a candidate
   orthogonal leg for the live `portfolio-learning` question — but only after (1) settles whether
   there is anything here at all.

**Tension recorded rather than resolved.** This source's mechanism is genuinely strong — settlement
conventions give it a testable timing restriction that almost no calendar effect has — and the lab's
closure is genuinely correct about what it tested. They do not contradict each other. What would
contradict the closure is a negative T−8-to-T−4 window on this universe, and that is unmeasured.
Do not treat this note as a reason to re-open the family; treat it as one free measurement that
either re-opens it or closes it for good.

## Related

- `experiments/learnings.md` 2026-09-01 — the structural closure of the calendar half, and the
  source of the pre-registered test in point 1. Its own instruction ("check the complement window's
  sign") is what this note is answering.
- `notes/2026-09-02-return-seasonalities-common-factors.md` — the cross-sectional half of the same
  family; its daily-frequency and country-index results are referenced in points 2 and 5.
- `notes/2026-08-29-same-calendar-month-seasonality.md` — Heston–Sadka, for the turnover argument
  that applies to any monthly-rebalanced seasonal.
- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` and the 2026-08-30 session's finding
  that the engine's one-day lag costs a daily effect most and a monthly effect least — the reason
  for point 4.
- `notes/2026-08-27-live-execution-costs-implementation-shortfall.md` — for pricing the overlay
  turnover in point 3.
