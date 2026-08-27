---
title: "The illusory nature of momentum profits" + "Are Momentum Profits Robust to Trading Costs?"
authors: Lesmond, Schill, Zhou (2004); Korajczyk, Sadka (2004)
year: 2004 (both)
venue: Journal of Financial Economics 71(2), 349–380 (tier 1); The Journal of Finance 59(3), 1039–1082 (tier 1)
url: https://doi.org/10.1016/S0304-405X(03)00206-X (read in full at https://www.bauer.uh.edu/rsusmel/phd/Lesmond_et%20al%20_2004_JFE.pdf) ; https://doi.org/10.1111/j.1540-6261.2004.00656.x (read in full at https://www.kellogg.northwestern.edu/faculty/korajczy/htm/korajczyk%20sadka.jf2004.pdf)
citations: LSZ 684 (Semantic Scholar by DOI, checked 2026-08-27), 502 (Crossref, same date); KS 611 (Semantic Scholar by DOI, checked 2026-08-27), 461 (Crossref, same date)
sample_period: LSZ 1980-01 – 1998-12 (cost estimation begins 1978-07; spread and commission series only cover 1994–1998); KS 1967-02 – 1999-12, with price-impact coefficients estimated from TAQ 1993-01 – 1997-05
markets: LSZ — CRSP US ordinary common shares (NYSE/AMEX, and NYSE/AMEX/Nasdaq in two of three replications); KS — NYSE, then NYSE/AMEX/Nasdaq
tier: A on both, on venue, citation count and sample length. The pair is recorded as one note because neither is interpretable alone: they study the same object, reach opposite verdicts, and the disagreement is the finding.
validation_overlap: false
published_post_2018: false
---

## Mechanism

Two tier-1 papers published the same year ask whether momentum survives trading costs. One
says no. The other says yes, above a break-even fund size in the billions. This note records
what each actually shows, why they disagree, and which parts of each transfer to a long-only
book of ~145 liquid global instruments.

### The bear case (Lesmond–Schill–Zhou): momentum trades where trading is dear

The argument is not that costs are high in general. It is that **the momentum signal selects
for expensive stocks**, so a market-average cost estimate is the wrong benchmark:

1. **Composition.** Winner and loser portfolios are drawn disproportionately from small,
   low-priced, off-NYSE stocks. In the replications run, the extreme-performer portfolios have
   an order of magnitude smaller median market capitalisation than the middle portfolio, much
   lower share prices, and a far smaller fraction of their names on the NYSE. That is a
   mechanical consequence of sorting on extreme past returns, not a sample artifact.
2. **Cost, measured on exactly those stocks.** Estimated round-trip costs for the winner
   portfolio run **18–61% above** the untraded middle portfolio's, and for the loser portfolio
   **30–75% above**, significant at the 1% level and consistent across four independent cost
   estimators and three published strategy definitions. Only one of twelve comparisons fails.
3. **Turnover.** Only a minority of positions survive from one formation period to the next —
   in the strategies studied, between roughly a seventh and two fifths — so a round trip in a
   large fraction of the book is paid every period.
4. **Arithmetic.** A long-short strategy needs four trades per holding period. Divide the gross
   spread by four and you get the per-trade cost budget the strategy can afford; the estimated
   costs of the stocks it actually trades exceed it. Charged at full turnover, the after-cost
   returns of the replications are not reliably distinguishable from zero and two of three are
   negative; charged at *actual* turnover they come back to small and mostly insignificant.
5. **The cross-sectional clincher.** Sorting stocks by trading cost, the gross momentum spread
   is *increasing* in trading cost. Where the strategy earns most is where it costs most. The
   authors read this as no-arbitrage holding: the effect is bounded by the friction that
   prevents its removal. They also show that a well-known information-diffusion explanation
   (analyst coverage) largely loses its explanatory power once trading cost is controlled for,
   since coverage and cost are strongly negatively correlated.

**Their estimator matters for what follows.** Their most comprehensive measure is the
Lesmond–Ogden–Trzcinka **limited-dependent-variable (LDV)** model, which infers round-trip
cost from the *incidence of zero-return days* in daily data: if trading is costly, information
must accumulate longer before anyone trades, so zero returns are more frequent. It requires
daily closes and nothing else, and it implicitly bundles spread, commission, immediacy and
some price impact into one proportional number.

**The one structural fact in this paper that a long-only book must not skip.** Using the
untraded middle portfolio as the benchmark, **53% to 70% of the total long-short momentum
spread comes from the short leg** across the three strategy definitions, and the result
survives using the value- or equal-weighted market as benchmark instead. Independent work
cited by the other paper here reaches the same conclusion from two other directions.

### The bull case (Korajczyk–Sadka): the right question is capacity, not yes/no

Same object, different framing, and — importantly — **they study long-only winner portfolios**,
explicitly declining to model the short leg because short execution carries costs their impact
measure does not capture. That makes their setting far closer to this repo's than LSZ's is.

1. **Costs are not proportional.** Proportional costs (spread, commission) reduce returns by a
   fixed amount independent of how much money is deployed. **Price impact does not** — it scales
   with the size of the trade, so a strategy's viability is a function of fund size. The right
   output is therefore a **break-even fund size**, not a verdict.
2. **Under proportional costs alone, the strategies survive**, and equal-weighted beats
   value-weighted, as the momentum literature reports.
3. **Under price impact the ranking inverts.** Equal weighting concentrates trading in small,
   illiquid names; value weighting concentrates it in liquid ones. Post-impact, value-weighted
   dominates equal-weighted, and the longer-formation/shorter-holding strategy dominates the
   shorter-formation/longer-holding one. Break-even sizes (normalised to end-1999 market
   capitalisation): roughly **$200M for equal-weighted**, **$2bn+ for value-weighted**, and
   **$4.5–5bn for a liquidity-weighted or half-liquidity/half-value construction**. These are
   capacity scales, not performance claims.
4. **A liquidity-weighted rule falls out of the impact model.** Under a linear impact
   specification, the weight that maximises net expected return is proportional to the stock's
   market value **divided by its price-impact coefficient** — tilt toward names that are cheap
   to trade, in proportion to how cheap. The authors are candid that its optimality holds only
   under fairly restrictive conditions and that the version they apply under a second impact
   model is ad hoc.
5. **Widening the universe raises capacity.** Adding smaller exchanges cuts both ways — the new
   names are less liquid, but a fund of given size can spread across more of them and trade less
   in each. Empirically the second effect wins and break-even sizes rise.
6. **Their own reconciliation with LSZ.** They agree the *equal-weighted* strategies LSZ studies
   are unprofitable, and note that their spread estimates are **1.18× to 5.55× smaller** than
   LSZ's for the same object. Their conclusion is that costs do not explain winner persistence,
   which "remains an important puzzle" — and they list several reasons their own break-even
   sizes are likely understated, chiefly that their impact coefficients assume the entire
   month-end rebalance is executed within a 30-minute window (or a single trade) with no
   patience at all.

### Adjudication

Three things are settled, and the third is why this note is written alongside the live-cost
note.

- **They do not actually disagree about equal-weighted small-cap momentum.** Both find it
  unprofitable at any meaningful size. LSZ's verdict is correctly scoped to the construction
  the academic literature standardised on.
- **They do disagree about whether that generalises**, and the disagreement is entirely about
  the cost function's *shape and level*: LSZ apply a proportional cost from a daily-data
  estimator to every trade regardless of size; KS apply a **linear** price-impact model
  calibrated to TAQ data.
- **The live-execution evidence adjudicates against both, in the same direction.** Measured
  against $1.7tn of actual institutional fills, a **linear** TAQ-calibrated impact model —
  precisely KS's `Δp/p = λ·Δq` — overstates a patient trader's cost by roughly 3× at 2% of
  daily volume and by almost an order of magnitude at 10%; and cost estimators of LSZ's
  proportional family run higher still. KS's own stated suspicion that their break-even sizes
  are conservative because they assume impatient execution is therefore **confirmed from
  outside**, and LSZ's cost level is the most overstated of the three.

The honest summary: **momentum's cost problem is real, is a capacity constraint rather than a
binary verdict, and is smaller than either of these papers estimated** — but the *composition*
result (momentum selects expensive stocks) and the *short-leg* result (most of the published
spread is on the side a long-only book cannot trade) are structural, are not touched by the
cost-level correction, and both cut against importing published momentum magnitudes.

## Construction recipe

What is implementable from the pair, as opposed to merely informative:

- **Liquidity-tilted weighting** (KS): `w_i ∝ MVE_i / λ_i`, `λ_i` the price-impact coefficient.
  Needs market cap and an impact estimate; unavailable here. Its *direction* — within a
  momentum basket, shift weight from the expensive-to-trade names toward the cheap ones — is
  the transferable part.
- **The LDV cost estimator** (LSZ): estimate a stock's round-trip cost from the frequency of
  zero-return days in its daily series by maximum likelihood on a limited-dependent-variable
  model of returns against a market factor. This is the one cost estimator in the literature
  that runs on **daily closes alone**. See the caution below before considering it.
- **Formation/holding cadence** (KS): under impact, longer formation with shorter holding beat
  the reverse. This is a cost-driven ranking of two cadences, both of which this repo has
  already explored on return grounds.

## Robustness evidence (qualitative only)

- Both use multi-decade CRSP samples; KS's is the longer at ~33 years. Both replicate across
  several published momentum definitions and both check alternative formation and holding
  periods. Both are heavily cited in the field's top two journals, and both have been absorbed
  into the standard reading of the anomaly rather than overturned.
- **Both are US-only.** Neither offers out-of-country evidence, which matters for a global
  universe. The live-execution note's 20 non-US markets is the only cross-market cost evidence
  this folder has.
- **Both are of the pre-decimalisation-and-after era**, and both report costs falling over the
  sample. The level they measure is therefore an upper bound on any later level, which
  reinforces the direction of the adjudication above.
- **Neither models a patient execution algorithm.** KS say so explicitly and flag it as the
  main reason their numbers are conservative. LSZ's LDV measure is inferred from price
  behaviour rather than from any execution, so the question does not arise for them — but the
  same inference means their estimate is of the cost that *deters* the marginal trader, which
  is not the cost a patient large trader pays.
- **Multiple testing**: LSZ note, unprompted and to their credit, that studying the strategy the
  literature converged on means testing a specification already selected for in-sample
  performance, and argue this stacks the deck against their own finding. Neither paper applies
  a formal multiple-testing correction.

## Implementability here

This is the folder's most direct external challenge to the repo's champion family, and it must
be recorded as a tension rather than smoothed. `learnings.md` records a buffered, multi-horizon,
magnitude-weighted long-only cross-sectional momentum book as the strongest thing this lab has
found. LSZ's title says such profits are illusory. Four things decide how much of that transfers.

**1. Universe. The largest discount, and it runs in this repo's favour.** LSZ's result is
driven by the small, low-priced, off-NYSE tail — their own middle-portfolio median market
capitalisation is in the tens of millions of dollars. This repo's universe is ~145 *current*
global large-cap stocks and ETFs. The composition mechanism (momentum sorts toward the
expensive tail) still operates *within* that universe, but the tail it sorts toward is the
liquid end of the global market, not the CRSP micro-cap end. LSZ's magnitudes do not transfer;
their direction does. **Note the interaction with the folder's oldest caveat**, though: the
same survivorship-conditioned, current-constituent universe that inflates single-stock alpha
(session 13's note) is also what makes LSZ's cost objection weak here. The two biases point
opposite ways and neither cancels the other.

**2. Weighting. The one place where the literature's post-cost ranking contradicts a repo
finding, and the contradiction is only apparent.** KS find that post-impact, value weighting
beats equal weighting — the reverse of the pre-cost ranking — because value weighting keeps
trading in liquid names. `learnings.md` records within-basket **magnitude weighting** as a
major Sharpe lever over equal weighting. These are not in conflict: KS's mechanism is *liquidity*,
not *signal strength*, and magnitude weighting is orthogonal to liquidity. But the transferable
warning is real and general: **a weighting scheme's pre-cost ranking is not its post-cost
ranking, and the sign can flip.** In this repo that flip is already priced — the engine charges
costs before the gate reads Sharpe — so no re-test is implied. What is implied is that any
future proposal to concentrate *further* should state its expected turnover, not just its
expected return, which is a discipline the folder has already recorded twice.

**3. The short leg. A partial, oblique answer to a question this folder retired.** Session 10
retired the request for a quantification of what the long-only constraint costs, after three
sessions failed to obtain it. This note supplies a different and more specific number for the
momentum family alone: **53–70% of the published long-short momentum spread comes from the
loser leg**. That is not the constraint's leakage as a function of signal dispersion — the
quantity that was asked for and abandoned — but it is a concrete, sourced, tier-1 discount to
apply whenever a long-short momentum result is used to motivate a long-only candidate here.
The operative form: **a long-only implementation of a published long-short momentum effect
should be expected to capture roughly a third of it, before any other adjustment.** Recorded
as a screen, not as a reason to revisit the retired question.

**4. Capacity, and the one caveat this adds to `learnings.md`'s permanent list.** KS's central
methodological point is that a strategy's viability is a function of fund size and that a
proportional cost model cannot express this. This repo's engine charges a flat 15 bps/side, so
every result it has ever produced is a **small-fund result** with no term that degrades as
notional grows. The companion live-cost note reaches the same conclusion from the cost function's
shape; this one supplies the vocabulary (break-even fund size) and the observation that for a
momentum book the break-even is set by the *illiquid* names in the basket, not the average one.

**Declined, with a mechanism, so it is not rediscovered.** The LDV estimator is the one cost
model in this literature that runs on daily closes alone, so it is superficially the one thing
here this repo could actually build — a per-instrument cost estimate from zero-return frequency,
used to tilt weights away from expensive names. It is declined for three independent reasons.
(a) It is **not free**: it is a fitted per-instrument parameter from the price history, i.e. the
noisily-estimated-input class that `SUMMARY.md` screen #1 exists to kill, and it would be
estimated on the same window the signal is. (b) Its **input signal is nearly absent in this
universe** — zero-return days are a micro-cap phenomenon, and a global large-cap and ETF
universe has few of them, so the estimator would be fitting noise. (c) The live-execution
evidence puts this whole estimator family at the top of the overstatement ladder, so even a
well-estimated version would be tilting weights on the wrong numbers. The idea is buildable and
should not be built.

## Related

- `notes/2026-08-27-live-execution-costs-implementation-shortfall.md` — the measurement that
  adjudicates between these two papers, and the source of the cost-estimator screen applied here.
- `notes/2026-08-27-market-impact-functional-form-and-trade-rate.md` — why a *linear* impact
  model is the wrong shape, which is the technical core of KS's overstatement.
- `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the strategy both papers are
  testing, and the overlapping-portfolio construction whose turnover is at issue.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the opposite-signed
  universe bias; see point 1 above for why the two do not cancel.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — banding and rebalance
  frequency as the responses to exactly the turnover problem LSZ measure.
