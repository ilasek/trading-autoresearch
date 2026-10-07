---
title: "Price Momentum and Trading Volume — the momentum life cycle, and why its profit sits on the leg this lab cannot trade"
authors: Lee, Swaminathan
year: 2000
venue: The Journal of Finance 55(5), 2017–2069 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1111/0022-1082.00280
citations: 1095 (Crossref `is-referenced-by-count`, checked 2026-10-05); 1561 (OpenAlex, checked 2026-10-05); Semantic Scholar returns a clean `not found` for this real DOI (checked 2026-10-05)
sample_period: "1965-01 to 1995-12 (NYSE/AMEX), with a Nasdaq-NMS holdout 1983–1996"
markets: US only — NYSE and AMEX common stocks, equal-weighted; Nasdaq deliberately excluded because dealer double-counting inflates its reported volume
tier: "A on venue, citation count and construction care. Downgraded **in use here to C**, for one reason that has nothing to do with the paper: its state variable is share turnover, which this repo cannot compute, and every substitute for it has already been measured to null on this universe."
validation_overlap: false
published_post_2018: false
read: "Full text of the typeset JF article (volume/issue/page headers intact), served by `johnhcochrane.com/s/lee_swaminathan_returns_volume_JF.pdf`."
---

## Access

**A new channel shape: a faculty page hosting *someone else's* paper.** OpenAlex, Crossref and
Semantic Scholar all report this DOI closed with `any_repository_has_fulltext: false`, and there is
no repository copy. The typeset JF article came from **John Cochrane's own site**
(`johnhcochrane.com/s/<author>_<topic>_JF.pdf`) at HTTP 200 on the first try. The
[2026-09-18] faculty-page lesson says to try *the author's* page; this extends it: **a prolific
author's site often hosts a reading-list or course library of other people's canonical papers, and
those files are typeset versions of record.** Worth trying for any much-taught Tier-1 article whose
own authors' pages come up empty.

Semantic Scholar's clean `not found` for a real, indexed DOI recurred — the **seventh** recorded
instance, and the second tonight. Crossref answered first; OpenAlex second.

## Mechanism

The paper's object is not momentum and not volume separately; it is the **joint** distribution of
future returns conditional on both. Its organising idea is the **momentum life cycle (MLC)**: stocks
pass through phases of investor favouritism and neglect, and **turnover locates a stock within that
cycle** — high turnover means currently in favour, low turnover means currently neglected.

Two predictions follow, and they are about *persistence*, not about level:

- **"Late stage"** — high-volume winners and low-volume losers. Their momentum is nearer its turning
  point and reverses sooner.
- **"Early stage"** — low-volume winners and high-volume losers. Their momentum has further to run.

The authors are explicit that the diagram is "an intriguing possibility that merits further
research", that it implies more regularity than the evidence warrants, that it holds at the
portfolio and not the firm level, and that it **does not explain** one of their own central findings
(that the Year-1 momentum spread is larger among high-volume stocks). That candour is worth
preserving: **the MLC is a mnemonic for a set of conditional correlations, not a model.**

**The paper's own rejection of the obvious alternative reading is the part most often dropped when
it is cited.** Turnover here is explicitly argued **not** to be a liquidity proxy, on three grounds
stated in the conclusion: high-volume firms earn *lower* future returns but earned *higher* past
returns (a liquidity premium has no such time reversal); turnover is not highly correlated with firm
size or with the relative bid-ask spread; and the volume effect is independent of the size effect.
Their positive reading is instead about **mispricing of earnings prospects** — low-volume stocks
look under-valued and high-volume stocks over-valued on contemporaneous valuation multiples, and the
subsequent earnings surprises run the matching way over the following eight quarters. They also
dispatch both folk theories: volume "fuels" momentum **only for losers**, and aids information
"diffusion" **only for winners**, so neither one-directional story fits.

## Construction recipe

**The state variable.** `Volume` = **average daily turnover over the formation window**, where daily
turnover is shares traded that day divided by shares outstanding at the end of that day. Not share
volume, not dollar volume — a *normalised* activity rate.

**The sort.** At the beginning of each month, rank all eligible names **independently** on (i)
return over the previous `J` months and (ii) average daily turnover over **the same `J` months**.
Ten return deciles × three turnover terciles → 30 intersection portfolios. `R1` is the loser decile,
`R10` the winner decile; `V1` is lowest turnover, `V3` highest.

**The holding.** Monthly return for a `K`-month holding period is the equal-weighted average of the
portfolios formed this month and in the previous `K − 1` months — i.e. **overlapping tranches,
roughly `1/K` of the book recommitted per month**, exactly Jegadeesh–Titman's device and exactly the
construction this lab's own champion uses. `J, K ∈ {3, 6, 9, 12}`.

**A one-week lag** is imposed between the end of the formation window and the start of the holding
window, explicitly to keep bid-ask bounce and short-horizon reversal out of the result. (This repo's
engine already applies a one-day execution lag; the point generalises — the paper's authors did not
believe their own result at a zero lag.)

**The two strategies the MLC names**, both long–short:

    early stage = R10·V1  −  R1·V3      (low-volume winners  minus  high-volume losers)
    late  stage = R10·V3  −  R1·V1      (high-volume winners minus low-volume losers)

**Universe screens**, which are substantive rather than cosmetic: NYSE/AMEX only (Nasdaq excluded
because dealer double-counting inflates its volume and would make the turnover ranking incomparable
across venues); exclude primes, closed-end funds, REITs, ADRs and foreign companies; exclude names
delisted within five days of formation; exclude price below one dollar; require two years of prior
data. Returns equal-weighted.

## Robustness evidence (qualitative only)

Sample is a single market over three decades, so read all of this as one country's evidence.

- **Conditional on past returns, low-turnover names beat high-turnover names over the following
  year, in essentially every `(J, K)` cell.** The sign is consistent; the authors treat it as
  confirming Datar–Naik–Radcliffe while rejecting that paper's liquidity *interpretation*.
- **The momentum spread `R10 − R1` is larger among high-turnover names, and this is driven almost
  entirely by the loser decile.** Low-turnover losers rebound strongly in the following year;
  high-turnover losers do not. The winner side shows the same ordering but small and mostly
  insignificant in Year 1.
- **Beyond Year 1 the winner side separates and the sign is the same**: low-turnover winners beat
  high-turnover winners by a low-single-digit annual margin over Years 2–5 (measured 1965–1995).
- **Momentum reverses over Years 2–5 for all formation windows, and the reversal strengthens
  monotonically as the formation window `J` lengthens** — a genuinely useful shape result and one of
  the few monotone claims in the paper that is reported across all four settings rather than
  asserted.
- **Subperiod and venue checks**: results are reported across subperiods, and the Nasdaq-NMS holdout
  shows the volume effect *stronger* — which the authors read as an illiquidity worry rather than a
  confirmation, and say so.
- **No independent replication is recorded in this folder**, and the paper predates the modern
  replication audits. Treat its magnitudes as unconfirmed.

## Implementability here

**The headline is negative and it should be stated first: the paper's state variable does not exist
in this repo, and its known substitutes have already been measured to null on this universe.**

Turnover needs **shares outstanding**, which is a fundamental. `program.md` grants `volume` (a share
count in native units) and `dollar_volume`, and no share count. The lab already tried the obvious
substitutes and recorded both outcomes:

- `experiments/learnings.md` [2026-08-29, nightly]: **log average dollar volume is a clean null**
  here (IC +0.0010, t = +0.11), with the stated cause that on ~140 mega-caps a volume ranking is a
  pure size ranking with no illiquid tail.
- `experiments/learnings.md` [2026-08-31, nightly]: the **relative-volume** substitute built
  specifically for "the uncomputable turnover sort" did what it was designed to do — it decorrelated
  from log ADV (`spearman = +0.045` against the ≈0.78 a volume level gives) — **and predicted
  nothing** at any horizon. That entry's conclusion is that the family's live content is Amihud's
  price-impact *numerator*, not trading activity under any normalisation.

**The tension with this source, recorded rather than glossed.** Lee–Swaminathan's own argument is
that turnover is **not** a size or spread proxy — they report it is not highly correlated with
either, and that the volume effect is independent of the size effect. The lab's measured explanation
for its null is precisely that activity here *is* size. These are not actually in conflict, and
naming why is the useful part: their panel is **equal-weighted NYSE/AMEX including small names over
three decades**, where turnover has a genuine cross-sectional spread that is not collinear with
size; this panel is **~140 global mega-caps plus 42 ETFs**, where it is. **The source's own
identifying claim therefore predicts its own failure here**, which is a much stronger reason not to
re-test it than "we tried a proxy and got a null". **Do not spend a trial on a turnover-shaped
signal on this universe.**

**What does transfer, and the first item is the one worth acting on.**

1. **The long-only half of the result points the opposite way from the long–short half, and this lab
   only has the long half.** The famous finding — momentum pays more among high-turnover names — is
   driven by the **short leg** (high-turnover losers staying weak while low-turnover losers rebound).
   On the **long** leg the ordering is reversed and strengthens with horizon: **low-turnover winners
   beat high-turnover winners**, small in Year 1, clearly in Years 2–5. A long-only book that
   imported "volume improves momentum" would therefore tilt its winners **exactly the wrong way**.
   This is a new, concrete instance of the asymmetry this folder already has twice
   (`2026-09-06-long-side-share-of-anomaly-profits.md`,
   `2026-09-22-anomaly-profits-short-leg-asymmetry.md`) — and it is the sharpest instance, because
   here the two legs disagree in *sign*, not merely in share. **Generalise it as a reading rule:
   before importing any double-sort result, ask which leg the interaction lives on, because a
   long-only lab inherits only one of them.**
2. **A reason not to lengthen the formation window, with a mechanism attached.** The reversal of
   momentum over Years 2–5 strengthens monotonically in `J`. The lab's champion already runs four
   horizons with overlapping tranches and `experiments/learnings.md` records that six-month-stale
   signals still carry information; this source says the *stale* end of a long window is where
   reversal accumulates. That is a mechanism-level argument for the lab's existing horizon ceiling
   rather than a new candidate, and it should be used to **stop** a "try a 24-month formation window"
   idea rather than to start one.
3. **The overlapping-tranche construction is a published Tier-1 precedent for what the lab already
   does**, including the explicit rationale that it permits simple t-statistics on monthly returns.
   Worth citing in a journal entry the next time tranching is questioned.
4. **The one-week formation-to-holding lag is a design choice, not a technicality.** The authors
   impose it because they do not trust a zero-lag result at these horizons. The lab's one-day
   execution lag is shorter. If a short-horizon candidate ever looks strong, the gap between one day
   and one week is a cheap sensitivity to run — and `experiments/learnings.md` already records that
   raw 5–10 day reversal is the strongest measurable signal here and is structurally untradeable, so
   the contamination this lag exists to exclude is demonstrably present on this panel.

**What to ignore.** All of the valuation, earnings-surprise, analyst-coverage and book-to-market
evidence — it needs fundamentals and I/B/E/S. That is most of the paper's identification, so what
remains reachable here is a fragment, and this note should not be cited as support for the MLC as
such.

## Related

- `2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — Chordia–Swaminathan, the same second
  author on the short-horizon version of the volume question; this paper deliberately works at three
  months and longer to get away from the microstructure channel that one lives in.
- `2026-09-07-high-volume-return-premium.md`, `2026-08-29-amihud-illiquidity-measure-and-replication.md`,
  `2026-08-31-amihud-volume-component-decomposition.md` — the rest of this family's coverage, and the
  decomposition that located its live content away from activity.
- `2026-10-05-chl-spread-estimator-close-high-low.md` — the companion note from the same session: a
  `liquidity-volume` construction that needs **no** volume at all, which is why it is the live
  candidate and this one is not.
- `2026-09-06-long-side-share-of-anomaly-profits.md`, `2026-09-22-anomaly-profits-short-leg-asymmetry.md`
  — the long/short asymmetry this paper supplies a sign-flipping instance of.
- `2026-08-17-momentum-horizon-echo.md`, `2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the
  horizon structure and the overlapping-tranche device.
- `experiments/learnings.md`, [2026-08-29, nightly] and [2026-08-31, nightly] — the two measured
  nulls that make the direct construction a non-starter here.
