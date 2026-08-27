---
title: "Direct Estimation of Equity Market Impact"
authors: Almgren, Thum, Hauptmann, Li
year: 2005
venue: Risk 18(7), 58–62 (venue tier 3 — practitioner magazine — but the standard empirical reference for the impact function, cited as such by tier-1 work)
url: https://www.risk.net/risk-magazine (no registered DOI; full text read at https://www.cis.upenn.edu/~mkearns/finread/costestim.pdf, the authors' 2005-05-10 version)
citations: see the note on indexing below
sample_period: 2001-12 – 2003-06 (19 months)
markets: US equities, Citigroup brokerage executions restricted to S&P 500 constituents; 682,562 orders before filters, 29,509 usable data points
tier: B — a large, genuinely proprietary dataset and a clean derivation, but one broker, one market, large caps only, a short sample, and a practitioner venue with no peer review. Its central qualitative claim (concavity) is independently confirmed on a far larger and more global dataset, which is what carries the weight here.
validation_overlap: false
published_post_2018: false
---

**Indexing note.** This article has **no registered DOI** — *Risk* magazine does not assign
them for this vintage. Crossref has no record; a `query.bibliographic` search returns
unrelated work. Semantic Scholar's title-search endpoint returned **HTTP 429 on four
consecutive attempts** across the session, and its DOI endpoint is unusable without a DOI.
OpenAlex's daily budget was **already exhausted** at the start of this session
(`Insufficient budget`, resets midnight UTC), so its title filter could not be run either.
Recorded therefore as **`citations: not indexed by any channel reachable this session
(Crossref by DOI and by bibliographic query; Semantic Scholar title search, rate-limited;
OpenAlex, out of budget) — checked 2026-08-27`**. Per the rubric this is *not* grounds to
downgrade on its own; the tier above rests on venue, sample and replication status instead.
The source read is the authors' own dated version of the article, complete with figures,
tables and coefficient standard errors.

## Mechanism

The companion note on live execution costs establishes *how large* costs are. This one
establishes *what shape the cost function has*, and adds the dimension that note does not
have: **how fast you trade**, separately from how much.

**The two-component decomposition.** Write a parent order of `X` shares executed at a
constant rate `v = X/T` in *volume time* (`T` is the fraction of an average day's volume that
passes during execution, so `v` is the participation rate). The price process is

```
dS = S₀·g(v)·dτ  +  S₀·σ·dB
```

so `g` is the **permanent impact** function — a drift the trader adds to the price, which does
not revert — and separately the price actually received is `S̃(τ) = S(τ) + S₀·h(v)`, where `h`
is the **temporary impact** function, the concession paid for demanding liquidity in each
interval. Integrating gives the realised cost `J` of the program in terms of `I = T·g(X/T)`
(total permanent move) and `h`:

```
J  =  I/2  +  h(X/T)  +  (noise of order σ√T)
```

The `I/2` is the load-bearing piece of accounting: **you pay only half your own permanent
impact**, because your earlier trades have already moved the price against your later ones but
not against your earlier ones. `I` itself is not a cost — it is the net price move — and the
cost actually borne on the order is `J`.

**The fitted functional forms.** With `g(v) = ±γ|v|^α` and `h(v) = ±η|v|^β`, and `Θ` the shares
outstanding, `V` the average daily volume, `σ` the daily volatility:

```
I  =  γ · σ · (X/V) · (Θ/V)^{1/4}                (α = 1, δ = 1/4)
J  =  I/2  +  sign(X) · η · σ · |X/(V·T)|^{3/5}   (β = 3/5)
γ  =  0.314 ± 0.041      η  =  0.142 ± 0.0062
```

Four things in that, in descending order of how much they matter here:

1. **Cost is proportional to volatility.** Both terms carry a factor of `σ`. The authors state
   the stronger version explicitly: the temporary cost function needs *no* stock-specific
   modification at all — "liquidity cost **as a fraction of volatility** depends only on shares
   traded as a fraction of average daily volume". Volatility is not one determinant among
   several; it is the unit in which impact is denominated.
2. **Temporary impact is concave in the trade rate**, with `β` strictly below 1. The
   square-root model `β = 1/2` is **rejected at the 95% level** in favour of `β = 3/5`. Relative
   to square-root this gives slightly *lower* costs on small trades and slightly *higher* costs
   on large ones. The direction of the disagreement with the live-execution evidence (which
   fits ≈0.35 and rounds to 1/2) is worth noting and is discussed below.
3. **Permanent impact is linear in size and independent of speed.** `α = 1` cannot be
   rejected and is adopted for tractability. Linearity means the total permanent move depends
   on `X` alone, not on `T` — trading patiently does not reduce it. Only the temporary term
   responds to slowing down. This is the theoretical justification (Huberman–Stanzl) for the
   linear form: any other exponent on permanent impact admits price manipulation.
4. **The liquidity factor is turnover, not market cap.** The stock-specific correction to
   permanent impact is `(Θ/V)^{1/4}` — the inverse of the fraction of the company traded per
   day. A stock with more shares outstanding relative to its daily volume has *higher* impact
   for the same `X/V`, because a given fraction of that day's flow is a smaller fraction of the
   company. The authors tested market capitalisation and the bid-ask spread as alternative
   conditioning variables and found the price effect too weak and the spread effect absent.

**The trade-off this sets up, which is the whole point of the execution literature.** Slowing
execution (`T` up at fixed `X`) lowers the temporary term as `T^{3/5}` but leaves the permanent
term untouched and raises the *volatility risk* of the unexecuted remainder as `σ√T`. So there
is an interior optimum in trading speed, and it depends on the trader's risk aversion. Impact
costs are not a fee schedule; they are one side of a risk/cost frontier.

## Construction recipe

Not a strategy recipe — a cost-estimation recipe, and the inputs are the point:

- Compute `X/V`: order size as a fraction of the stock's average daily volume.
- Compute `T`: the fraction of a day's volume that will pass during execution — i.e. `X/V`
  divided by the participation rate you intend.
- Look up `σ`, the stock's daily volatility, and `Θ/V`, its inverse turnover.
- Permanent: `I = 0.314·σ·(X/V)·(Θ/V)^{1/4}`; you pay `I/2`.
- Temporary: `0.142·σ·|X/(V·T)|^{3/5}`.
- Total expected cost `J` is the sum. Realised cost on any single order is dominated by
  volatility noise — the regressions' `R²` is **under 1%**, which the authors correctly present
  as expected rather than as a failure: the model predicts the *mean* of a distribution whose
  spread is set by price volatility during the trade, not the outcome of any one order.

Worked scale from the paper's own example: a large-cap name at ~1.6% daily volatility, trading
10% of daily volume, pays ~20 bps of permanent impact and 8–22 bps of temporary impact
depending on whether the order is spread over half a day or a tenth of one — a realised cost of
roughly 18–32 bps. A more volatile name at the same participation pays proportionately more.

## Robustness evidence (qualitative only)

- **The concavity claim replicates and is the part to trust.** An independent dataset three
  orders of magnitude larger, spanning 21 markets and 19 years rather than one broker and 19
  months, fits the same concave shape and formally rejects linearity. Two independent
  proprietary datasets agreeing on the *shape* is as close to replication as this literature
  gets.
- **The exponent does not replicate exactly**, and the disagreement runs the informative way.
  This source rejects `β = 1/2` in favour of `3/5` on US large-cap broker orders; the live
  institutional data fits ≈0.35 and rounds *up* to 1/2. Both are concave; they bracket the
  square root from opposite sides. The honest reading is that **the exponent is not a universal
  constant** — it plausibly depends on execution style, and the patient-limit-order manager
  sits at the flatter end while a broker's mixed order flow sits at the steeper one. Take
  concavity as established and any specific exponent as calibration.
- **Known weaknesses, several stated by the authors.** One broker, one market, S&P 500 names
  only, and thin data at both extremes (small caps and very large trades). Orders are
  restricted to those completed within a single day, with VWAP, market-on-open and
  market-on-close orders excluded — so the fitted function describes *active intraday
  scheduling* and does not cover the patient multi-day execution the live-cost note documents.
  Residuals are visibly fat-tailed, with the Gaussian a reasonable fit only in the centre; the
  reported `t`-statistics assume the Gaussian model and should be read as indicative.
- **No peer review, no post-publication decay literature, no McLean–Pontiff-style tracking.**
  This is a market-microstructure measurement rather than a return anomaly, so the decay
  question does not really apply — but neither does the reassurance that a replicated anomaly
  gets. What can and did change is the *level*, which both this source and the live-cost source
  report as trending down with market structure and technology.

## Implementability here

**Nothing here is a strategy, and nothing here can be run on this repo's data.** `X/V`, `Θ/V`
and the participation rate all require volume and shares-outstanding fields the store does not
have and `program.md` gates behind human approval. What the note supplies is three
recalibrations of how the repo should *read* its own cost line.

**1. The one asymmetry in the repo's flat cost model that actually points the wrong way.**
Impact in basis points is proportional to the traded name's volatility. The engine charges 15
bps per side regardless of what is being traded. A cross-sectional momentum basket is not a
random draw from its universe: it systematically holds the recent-extreme-return, higher-volatility
tail, and this repo's own concentration ladder has pushed further into that tail with each
promotion (`learnings.md` records the drawdown cost of exactly that). So the flat charge
**under-prices the champion's book specifically**, by roughly the ratio of the held names'
volatility to the universe median's — a multiplier, not an additive term.

The size of the correction is what decides whether this matters, and it is small.
`learnings.md` prices the champion's total cost drag at 0.45%/yr ≈ 0.019 Sharpe at 3.0×
turnover. Any plausible volatility multiplier — even 1.5× — leaves the drag under ~0.03 Sharpe,
which is inside the noise of a single promotion step and far below the paired standard errors
the folder derived in session 11. **So the scaling law is real, the direction is against this
repo, and the magnitude does not change a verdict.** Recorded so that the flat-cost caveat is
stated correctly rather than assumed neutral, not as a reason to revisit anything.

**2. A free, holdings-only diagnostic, and it is denominated in the right unit.** The
turnover-weighted ratio of held names' trailing daily volatility to the universe median's is
computable from the weight matrix and the price data already stored, forecasts nothing, and
scores no returns. Multiplied by the existing modelled cost drag it converts to annualised
return and thence to Sharpe — the unit the gate actually reads, which is session 10's *check
the currency* discipline satisfied rather than tripped over. It is cheap enough to carry
alongside the existing HHI and turnover-decomposition diagnostics. **Caution that must travel
with it:** it is a *cost account*, never an objective. A book can lower it by holding placid
names and lose far more on the selection term, exactly as `γ*` could be gamed in session 9.

**3. The permanent/temporary split closes a question the repo could otherwise ask.** A natural
"free" idea for a cost-paying book is to trade more patiently — spread the monthly rebalance
over several days. This source prices that precisely: patience reduces only the **temporary**
term, as `T^{3/5}`, and leaves **permanent** impact untouched, while adding volatility risk on
the unexecuted remainder as `σ√T`. The live-execution evidence puts 85–90% of measured impact
in the permanent component. So execution patience attacks the small half of the cost, and this
repo cannot express it anyway (the engine's single one-day lag is frozen). **Recorded as a
declined idea with a mechanism, so it is not rediscovered as an opportunity.**

**4. What it says about the no-trade band.** The champion's hysteresis buffer is the correct
response to *proportional* costs (Gârleanu–Pedersen's branch), and this note does not disturb
that. It does add a second, independent argument for the same device from a different premise:
under concave impact, cost per share falls with size, so **a few larger trades cost less in
total than many small ones of the same aggregate size**. Banding and concavity push the same
way. That is a coincidence of direction, not new evidence, and should not be re-tested.

## Related

- `notes/2026-08-27-live-execution-costs-implementation-shortfall.md` — the same function
  estimated on 21 markets and live institutional executions; confirms concavity, disputes the
  exponent, and supplies the level.
- `notes/2026-08-27-momentum-net-of-costs-debate.md` — where the linear-vs-concave distinction
  decides a published disagreement.
- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — the optimal policy
  under quadratic costs, and its own statement that proportional costs give a no-trade band.
  This note supplies the empirical shape that sits between the two idealisations: neither
  linear nor quadratic, but concave with exponent below one.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the mitigation
  techniques this cost function is what one mitigates against.
