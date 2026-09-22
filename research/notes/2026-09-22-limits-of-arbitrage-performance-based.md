---
title: "The Limits of Arbitrage"
authors: Shleifer, Vishny
year: 1997
venue: Journal of Finance 52(1), 35–55 — Tier 1 (top peer-reviewed)
url: https://doi.org/10.1111/j.1540-6261.1997.tb03807.x
citations: 5189 (Semantic Scholar, DOI lookup, checked 2026-09-22); 4344 (Crossref
  is-referenced-by-count, same DOI, checked 2026-09-22). OpenAlex reports 565 on this DOI
  because the work is split across the JSTOR (10.2307/2329555) and NBER (10.3386/w5167)
  records; per the folder's standing rule the lone low count is the one to disbelieve.
sample_period: n/a — theory paper; no estimation sample. Illustrative discussion draws on
  US equity evidence available to 1996.
markets: n/a (model); discussion covers US equities, bonds, FX
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The paper replaces the textbook arbitrageur — many, diversified, trading their own capital —
with the one that actually exists: a small number of **specialists trading other people's
money**, whose capital is allocated to them on the basis of their own past returns. The
authors call that allocation rule **performance-based arbitrage (PBA)**.

Two consequences follow, and both are structural rather than empirical.

1. **A specialist cares about total risk, not systematic risk.** Because the arbitrageur is
   undiversified by construction — the whole point of specialisation is to concentrate in a
   few assets — the risk that deters them is the volatility of *their own trade*, including
   its idiosyncratic part. This is the paper's single most transferable claim, and it is a
   claim about which risks should be priced: "Idiosyncratic risk as well deters arbitrageurs,
   whether it is fundamental or noise trader idiosyncratic risk."

2. **Arbitrage is weakest exactly where mispricing is largest.** Under PBA, an adverse price
   move both deepens the mispricing and triggers withdrawals, forcing liquidation into the
   move. The paper's Propositions 3–4 formalise this: at the fully-invested equilibrium the
   price response to a further noise-trader shock is *amplified* (`dp₂/dS < −1`), so the
   market loses its resiliency precisely in the states where a rational trader would most
   want to add. There is no third party to step in, because "arbitrage markets are
   specialized, and arbitrageurs typically lack the experience and reputations to engage in
   arbitrage across multiple markets with other people's money."

The economic story for why an anomaly survives is therefore not a hidden risk factor. It is
that **the trade required to remove the anomaly is idiosyncratically volatile, and a
career-constrained specialist will not carry it at size**. The paper's own summary: "we
expect anomalies to reflect not some exposure of securities to difficult-to-measure
macroeconomic risks, but rather, high idiosyncratic return volatility of arbitrage trades
needed to eliminate the anomalies."

Two riders the paper is careful about, and both matter here:

- **The horizon argument.** Where fundamental uncertainty is high and resolved slowly, the
  long-run ratio of expected alpha to volatility may be high while the ratio "over the
  horizon of a year may be low". A manager judged annually will decline a trade whose
  multi-year reward-to-risk is attractive. So the *surviving* anomalies are ones whose
  payoff horizon exceeds the evaluation horizon of the people who could arbitrage them.
- **The counter-intuitive volatility result.** Higher volatility does *not* by itself deter
  entry: if alpha scales with noise-trader volatility, the arbitrageur halves the position
  and is indifferent. Volatility deters arbitrage only when **expected alpha does not rise
  in proportion to it** — i.e. when a large share of the volatility is fundamental rather
  than sentiment-driven. This is a sharper prediction than "mispricing lives in volatile
  names" and it is the version worth carrying.

The paper also draws an explicit line against Merton (1987), which is the rival explanation
for any idiosyncratic-volatility effect. In Merton, segmentation and information costs make
high-idiosyncratic-risk stocks *rationally* earn **higher** expected returns. In
Shleifer–Vishny, idiosyncratic risk deters arbitrage, so some high-idiosyncratic-variance
names are **overpriced** and earn **lower** expected returns. Same regressor, opposite sign
— which means an idiosyncratic-volatility sort cannot by itself distinguish the two stories,
and the discriminating evidence has to come from somewhere else (see
`2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md`, which supplies it).

## Construction recipe

This is a theory paper and there is no portfolio in it. What it supplies is a **two-step
procedure for deciding where to look for an effect**, stated by the authors as the
replacement for the efficient-markets approach to anomalies:

1. **Identify the source of the noise-trader demand** that would create the mispricing —
   sentiment, or an institutional restriction on holdings. Without a named demand there is
   no reason for a price to be wrong.
2. **Price the cost of the arbitrage that would remove it**, and specifically "the total
   volatility of arbitrage returns" — the volatility of the long-minus-hedge position, not
   the volatility of the underlying name. Transaction costs enter here too (the paper cites
   Pontiff 1996).

An effect is expected to persist only when step 1 supplies a demand and step 2 supplies a
large number. Both legs are required; a large arbitrage cost with no noise-trader demand
predicts nothing.

A third condition is stated in passing and is easy to miss: the approach assumes **only a
small number of specialists understand the anomaly**. As an effect becomes widely
understood, more investors tilt toward it, and — the subtler channel — arbitrageurs start
being **benchmarked against their peers** rather than against the market, which removes the
withdrawal pressure that made the trade dangerous in the first place. The paper's own
conclusion from this is that its framework is "clearly more appropriate for
difficult-to-understand new arbitrage opportunities than it is for well-understood
anomalies".

## Robustness evidence (qualitative only)

- The model is analytic; there is nothing to replicate in the usual sense. What has been
  replicated is the *empirical programme* it launched — arbitrage-cost proxies as
  cross-sectional conditioning variables — and that programme has independent support in
  every note in tonight's cluster.
- The specific prediction that idiosyncratic volatility deters arbitrage and therefore
  *permits* mispricing is taken up directly and tested by
  `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` (multi-decade US, Tier A) and is the
  organising idea of `2026-09-22-arbitrage-risk-substitute-portfolios.md` (Tier A), which
  supplies an independent measurement of the same quantity.
- The asymmetry the paper notes only in passing — that margin calls and forced liquidation
  bear harder on short positions than on unlevered long ones — was later made the centre of
  a separate literature; see the same two notes.
- **Known limit, stated by the authors**: the framework is weaker for anomalies that have
  been publicly documented and widely understood, which is most of what this repo tests.
  That is a discount on every hypothesis derived from it, and it points the same way as
  `notes/2026-08-17-mclean-pontiff-publication-decay.md`.

## Implementability here

Nothing in this paper is a candidate. What it is, is a **model of why this lab has been
finding nulls**, and it is worth stating plainly because it is falsifiable on this repo's
own data.

- **The universe is, by construction, the low-arbitrage-cost end of the world.** ~145 large
  global names and liquid ETFs, all current survivors, all cheap to trade and easy to hedge.
  Under Shleifer–Vishny, a surviving anomaly requires an arbitrage trade that a specialist
  will not carry. On this universe that trade is about as carryable as it gets. **The theory
  predicts thin cross-sectional mispricing here — which is what twelve sessions have
  measured.** That is a mechanism for the 2026-09-20 nightly's own conclusion that
  "monthly-horizon cross-sectional prediction may simply have very little signal outside the
  trend the incumbent already holds", and it is a better explanation than "the universe is
  empty" because it says *which* universe would not be.
- **The horizon rider cuts the same way and is cheap to act on.** The paper's argument is
  that the surviving effects are the ones whose payoff horizon exceeds the arbitrageur's
  evaluation horizon. This lab rebalances monthly and scores at a monthly horizon — the
  horizon at which an arbitrage-constrained specialist is *most* willing to trade, hence the
  horizon at which the least mispricing should survive. This is an argument for looking at
  longer holding periods, not for looking harder at the same one.
- **The direct tension with this lab's strongest measured fact, recorded rather than
  smoothed over.** `experiments/learnings.md` (2026-09-06 onward, fourteen mechanism screens)
  identifies the **volatility level** as this universe's dominant survivorship artifact:
  high trailing volatility predicts high forward return here, with the largest |IC| of any
  score in the repo, because the constituents are current survivors. Shleifer–Vishny say
  that idiosyncratic volatility is the arbitrage-cost variable that tells you *where*
  mispricing survives. **These two claims put the same regressor on both sides of the
  table.** On this universe, "condition on high idiosyncratic volatility" and "tilt into the
  survivorship artifact" are the same instruction, and the lab's own evidence for the second
  reading is stronger than the literature's for the first. Any construction from this vein
  must therefore vary something *other* than the volatility level — which is exactly what
  `2026-09-22-arbitrage-risk-substitute-portfolios.md` supplies, in the form of a
  scale-free **fraction**.
- **What is genuinely reachable**: the two-step procedure as a *discipline* on hypothesis
  writing. Before a candidate is coded, the note asks for a named noise-trader demand and a
  named arbitrage cost. Most of the behavioural scores this lab has refuted (52-week-high
  proximity, information discreteness, overnight sentiment, `VSP`, `ST`) supply the first and
  never the second. That is a free filter and it costs no trial.

Pitfalls:

- Do **not** read "idiosyncratic risk deters arbitrage" as "buy high-idiosyncratic-risk
  names". The paper says the opposite: among the names arbitrage has failed to reach, some
  are overpriced and earn *lower* returns. The sign depends entirely on which side of the
  mispricing the name sits, which this repo cannot observe directly.
- Do not import the model's "extreme circumstances" results at all. They are statements
  about specific market episodes and the anti-lookahead policy forbids event narratives;
  they are also unreachable without leverage, which `program.md` caps at 1.0.

## Related

- `2026-09-22-arbitrage-risk-substitute-portfolios.md` — the same quantity, measured, with a
  construction recipe and the un-hedgeable-fraction variable that escapes this repo's
  volatility-level artifact.
- `2026-09-22-anomaly-profits-short-leg-asymmetry.md` — which side of an anomaly the profit
  lives on, and therefore what a long-only lab can expect to capture.
- `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` — the Merton-versus-Shleifer–Vishny
  discrimination, resolved by conditioning on relative mispricing.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the "widely understood anomaly"
  rider, measured.
- `experiments/learnings.md`, 2026-09-06 onward — the volatility level as this universe's
  survivorship artifact; the tension above.
