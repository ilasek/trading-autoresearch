---
title: "Tax-Loss Trading and Wash Sales — investor-level evidence that the turn-of-the-year flow is real, naive, and size-dependent"
authors: Grinblatt, Keloharju
year: 2004
venue: Journal of Financial Economics 71(1), 51–76 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/s0304-405x(03)00180-6
citations: "80 (Crossref `is-referenced-by-count`, checked 2026-10-07); 105 (OpenAlex, checked 2026-10-07); 22 (Semantic Scholar, checked 2026-10-07) — and Semantic Scholar also reports the year as **2000**, a corrupted year field alongside a visible undercount. A further instance of this folder's standing \"disbelieve a lone low count\" rule, with the same tell recorded [2026-08-23]."
sample_period: 1994-12-27 to 2000-05-26
markets: "Finland — daily holdings and trades of all Finnish households and institutions in virtually all Finnish stocks, from the Finnish Central Securities Depository register (≈97% of Finnish market capitalisation at the start of the sample)"
tier: A
validation_overlap: false
published_post_2018: false
read: "Full text, NBER Working Paper 8745 (January 2002), `nber.org/system/files/working_papers/w8745/w8745.pdf`, which carries the abstract, all five sections, the tables' discussion and the reference list of the article published in JFE 2004. Extracted with `pdftotext -layout`; body text not font-shifted and no `( )` math dropout."
---

## Mechanism

Everything in the turn-of-the-year literature before this paper inferred tax-loss selling from
returns or from aggregate volume. This paper observes the trades. The dataset is the central
shareholding register for an entire national market, at daily frequency, per investor, with purchase
prices — so for every sale it knows whether the seller was sitting on a gain or a loss, and whether
they bought the same stock back.

Finland is the right laboratory for a specific institutional reason: **it has no wash-sale
restriction.** A Finnish investor can sell to crystallise a loss and repurchase the identical stock
the same day. That removes the main confound in US data, where the 30-day wash-sale rule forces any
tax-motivated seller either to wait or to buy something else, and it lets the authors separate "I
sold because I wanted out" from "I sold for the tax deduction and immediately re-entered".

Three findings, in the order they build:

1. **The tax motive temporarily overrides the disposition effect.** Measured with Odean's ratio —
   the propensity to realize gains divided by the propensity to realize losses, both conditioned on
   the investor selling *something* that day — Finnish investors behave like US investors for most
   of the year, realizing gains more readily than losses. That ratio then **declines, virtually
   monotonically, over the last ten trading days of December**, and jumps sharply upward at the turn
   of the year. The behavioural default (hold losers) is reversed by the tax deadline and snaps back
   immediately after it.
2. **The selling is accompanied by immediate repurchase of the same stock, and the repurchase rate
   is conditional in exactly the way a tax motive predicts.** Sales in the final handful of trading
   days of December are repurchased within the following weeks at a rate roughly double that of
   sales in the other windows examined, and markedly higher than for sales made just after the turn
   of the year — a difference the authors reject at high significance with a binomial
   difference-of-proportions test. The repurchase rate rises with **the size of the capital loss** on
   the position and with **proximity of the sale to the end of December**. Both gradients are
   signatures of tax-crystallisation rather than of a view on the stock.
3. **The resulting flow is one-sided in time, and its calendar shape matches the known calendar
   shape of returns, most strongly in small caps.** Netting repurchases-of-prior-sales against
   sales-that-will-themselves-be-repurchased gives a measure of **net tax-loss buying pressure** — a
   purely temporal shift in demand, by construction unrelated to news about the firm. Its calendar
   profile is small or slightly negative at the end of the tax year and clearly positive in the first
   days of the new one. The daily correlation between net tax-loss buying pressure and daily returns
   is positive, and significantly so **for small firms**; small firms also show by far the most
   extreme turn-of-the-year change in repurchase behaviour.

The payoff for the preceding theory note is precise. Constantinides' price channel needs sellers who
are naive about the price seasonality; the authors' own footnote concedes that the observed
end-of-December concentration of realizations is **not** optimal tax timing by Constantinides'
standard — there is no reason to wait for the last days of the year, yet that is what happens. So the
naivety precondition is empirically met in this market. What the paper *adds* to Constantinides is
that the price-relevant quantity is not a one-sided supply shock but a **temporal shift in demand**:
the same investors sell and buy back, so the flow is a displacement of buying from late December
into early January rather than a net liquidation.

The authors are careful about what this does and does not establish: one small market, one sample
period, and the results "do not conclusively prove that tax-loss selling causes the January return
anomaly". What they claim is that *if* the Finnish behaviour is typical, the return pattern is
plausibly partly or wholly tax-driven.

## Construction recipe

Nothing here is a portfolio. What is reusable is a **set of measurement definitions**, and two of
them are reachable from a daily OHLCV panel without investor-level data:

- **Realization-propensity ratio (needs holdings — not reachable here).** Numerator: realized gains
  ÷ (realized gains + paper gains). Denominator: realized losses ÷ (realized losses + paper losses).
  Paper gains/losses are the positions an investor still holds on a day they sold something else,
  signed by purchase price versus that day's close. Recorded for completeness; this repo has no
  holdings data.
- **Net tax-loss buying pressure (needs trade-level data — not reachable here).** On day *t*:
  repurchase events on *t* matched to sales in the prior 25 trading days, minus sales on *t* that are
  repurchased within the following 25 trading days, scaled.
- **Reachable proxy 1 — the volume shape.** The mechanism's testable implication for a volume panel
  is a rise in turnover concentrated in the final trading days of the tax year, in names carrying
  large losses over the tax year, with an abrupt stop after the turn. This is the same prediction
  Constantinides derives from theory, measurable from `volume`/`dollar_volume` with no returns.
- **Reachable proxy 2 — the conditioning variables.** The gradients the paper establishes are in
  **size of the loss** and **proximity to the tax year-end**. A candidate that conditions on
  prior-tax-year return and on a window of a few trading days around the year-end is using exactly
  the two variables the investor-level evidence identifies, and nothing else.
- **The window is days, not months.** The behavioural shift is concentrated in roughly the last
  eight to ten trading days of the tax year and the first several of the new one — not "December"
  and "January" as calendar months. Any construction that uses month-ends as its grid will average
  the effect away with three weeks of ordinary December.

## Robustness evidence (qualitative only)

The identification is strong and the external validity is weak, and the authors say so. Strengths:
a complete national register rather than one brokerage's clients; daily rather than monthly; the
wash-sale-free institutional setting that makes the repurchase test possible at all; and multiple
independent gradients (loss size, year-end proximity, firm size) all pointing the same way, which
is harder to produce by chance than a single mean difference. Weaknesses: a single small market, a
short sample, a flat capital-gains tax rate throughout (so no within-sample tax-regime variation —
that variation is what the companion cross-sectional paper exploits instead), and the final step
from flow to price is a correlation, not an experiment.

The correlation-with-returns result is explicitly conditional on firm size, which is the one place
this paper, Constantinides' theory and the Australian evidence all agree: **whatever is happening is
a small-firm, thin-market phenomenon.**

## Implementability here

**This is a precondition note, and it both helps and hurts a turn-of-the-tax-year candidate on this
repo's universe.**

What it gives:

- **A sharper window than the calendar month.** If the lab tests this at all, the formation/holding
  grid must be *trading days around the tax year-end*, roughly `[-8, -1]` and `[0, +5]`, not
  December and January as months. The repo's engine forward-fills sparse weight rows and applies a
  one-day execution lag, so a two-row-per-year weight schedule placed on specific trading days is
  mechanically easy and **adds about two rebalances a year** — which is the opposite of the cost
  problem Heston–Sadka's monthly seasonal has (`notes/2026-08-29-same-calendar-month-seasonality.md`,
  where the authors' own conclusion is that full monthly portfolio turnover may not be worth paying).
  Turnover is the thing `program.md` names as the risk in this family, and a two-window overlay is
  the cheapest construction the family admits.
- **A free, trial-free volume screen.** The repo now receives `volume` and `dollar_volume`. The
  prediction — turnover concentrated in the final trading days of the tax year in large-loss names,
  stopping abruptly after — is testable on train with no return data. If the volume signature is
  absent on this universe, every return-side construction built on this mechanism is unmotivated and
  the family's remaining budget is better spent elsewhere.
- **A pre-registered interaction, not a bare sort.** The lab already computes Amihud `ILLIQ` and has
  a dollar-volume panel. The mechanism says the effect is monotone in illiquidity. So the honest
  construction is a *loss × illiquidity* interaction within the eligible panel, and the
  pre-registered prediction is that the effect is concentrated in the least-liquid quintile
  available.

What it costs:

- **Finland is not this universe, and the direction of the discrepancy is adverse.** Protocol v2's
  pool is ~1,400 names that were ever members of nine large-cap indices plus 42 ETFs. The one
  conditioning variable the paper finds significant for the return link is **small size**. Large-cap
  index members are the far end of that gradient. A null here is weak evidence about the mechanism.
- **Non-US tax years are an input this repo does not have.** The gradient is to *the investor's* tax
  year-end, and the universe spans fifteen regions whose personal tax years do not all end on
  31 December. The lab cannot read that from its data store, and **writing a per-region tax-year
  calendar into a candidate file is a judgement call that must be declared in the hypothesis**, not
  slipped in as a constant. It is not a hindsight-guard violation (no stock is named, and tax-year
  ends are public, pre-dated institutional facts), but it is an unverified external input and the
  Australian evidence is that the alignment prediction fails anyway.
- **Wash-sale rules differ by jurisdiction, and they change the predicted sign of the January flow.**
  The Finnish mechanism is a *demand displacement* that works because repurchase is unconstrained.
  Where a wash-sale rule binds, the repurchase is delayed past the rebound or redirected into a
  substitute, which per Constantinides weakens or eliminates the price effect. So the mechanism does
  not transfer uniformly across this universe's regions, and a pooled global construction mixes
  regions in which the channel should and should not operate.

## Related

- `notes/2026-10-07-tax-trading-theory-and-the-price-pressure-condition.md` — the theory this paper
  supplies the missing behavioural precondition for, including the authors' own concession that the
  observed timing is not optimal.
- `notes/2026-10-07-tax-year-end-alignment-and-the-australian-test.md` — the counterweight: a market
  with a mid-year tax year-end whose seasonal does not move to match it.
- `notes/2026-10-07-past-return-consistency-and-the-seasonal-in-the-past-return-relation.md` — the
  cross-sectional, tax-regime-conditioned version of the same claim, by one of the same authors.
- `notes/2026-09-19-v-shaped-selling-propensity.md` and
  `notes/2026-09-19-capital-gains-overhang-reference-price.md` — the folder's existing literature on
  when holders sell, driven by the reference price. This paper is the **calendar** override of that
  schedule, and the Odean-ratio result is the two mechanisms competing within one month.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`,
  `notes/2026-08-31-amihud-volume-component-decomposition.md` — the illiquidity interaction the
  mechanism requires, already built in this lab.
- `notes/2026-09-07-high-volume-return-premium.md` — the other place this folder treats a volume
  shock as the signal rather than the control.
