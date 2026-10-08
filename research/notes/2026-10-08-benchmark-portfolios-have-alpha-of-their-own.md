---
title: "Should Benchmark Indices Have Alpha? Revisiting Performance Evaluation"
authors: Cremers, Petajisto & Zitzewitz
year: 2013 (published); NBER WP 18050, 2012 (version read)
venue: Critical Finance Review 2(1), 1–48 (venue tier 2 by this folder's rubric — peer-reviewed, editor-refereed finance journal, below the JF/JFE/RFS/JFQA/ManSci/JPM tier-1 list but well above a working paper; the paper carries the EFA Best Paper award of the Commonfund Institute, the FMA Europe Best Paper award and the Q-Group's Roger F. Murray Prize)
url: https://doi.org/10.1561/104.00000007 ; full text read from the NBER working paper, https://www.nber.org/system/files/working_papers/w18050/w18050.pdf
citations: "261 (OpenAlex, checked 2026-10-08; Crossref is-referenced-by-count 187 for the published version, plus 90 on the NBER working paper DOI 10.3386/w18050 — the two are the same paper, so the folder's standing rule applies and the total is the honest figure)"
sample_period: 1980–2005 for the main index and decile tests, extended to 1927–2005 for the size/book-to-market decile portfolios
markets: US equities — S&P, Russell, Dow Jones Wilshire index families; CRSP size and book-to-market decile portfolios; a mutual-fund panel for the performance-evaluation application
tier: "A. Peer-reviewed and multiply awarded, 261 citations, a 26-year main sample extended to 79 years, the central finding established on two independent families of test portfolios (commercial indices and CRSP deciles), three distinct causal channels identified and each separately remedied, and the remedies validated out of the setting that motivated them (on a mutual-fund panel). The one gap keeping it short of a textbook A is that the evidence is single-market (US)."
validation_overlap: false
published_post_2018: false
---

## Mechanism

Protocol v3 replaced the statistic this lab deflates. Under v1 and v2 the test asked whether a
candidate beat the best of N zero-Sharpe strategies; v3 states plainly why that was wrong — "a
long-only book with no skill has the market's Sharpe, so it mostly asked 'is this long equity?'
(the equal-weight pool itself scored 0.81)" — and now deflates **skill**: "validation Sharpe
minus the equal-weight eligible pool's on the same days" (`program.md`, Protocol v3). The lab's
own v3 audit draws the moral: "**beating the null is not beating the pool**"
(`experiments/learnings.md`, Protocol v3).

That is a large improvement and it creates a new exposure. Every v3 number is now a *difference
against one specific portfolio*, so the equal-weight eligible pool has become the most
load-bearing object in the lab — and it has never been studied here. A grep across all 170 prior
notes returns **zero** for `benchmark index` and `Zitzewitz`; `equal-weight` appears in 77 notes
but always as a *weighting choice for a candidate*, never as the reference a result is measured
against. This note is about the benchmark as an object.

The paper's finding is the one every v3 reader needs: **standard benchmark models assign
economically and statistically significant non-zero alphas to portfolios that are, by
construction, passive.** From the abstract: "Standard Fama-French and Carhart models produce
economically and statistically significant nonzero alphas, even for passive benchmark indices
such as the S&P 500 and Russell 2000." It is not a small-sample curiosity: they "can reject the
joint null hypothesis that the true alphas are zero and that the deviations from zero arise
through chance (with p-values that are always less than 0.1% even when we allow for clustering of
returns within time periods)", and the evidence "strengthens when we extend the analysis to the
1927–2005 period". The sign is systematic rather than random — large-cap portfolios get positive
alphas, small-cap portfolios negative ones, more extreme among growth stocks.

They identify **three causes**, and the first two are the ones with no coverage in this folder:

1. **The benchmark's weighting scheme is itself an exposure bet.** "The Fama-French (FF)
   methodology equal-weights the 2x3 size-by-BM portfolios when constructing the small-minus-big
   (SMB) and high-minus-low (HML) factors, **even though these portfolios contain very different
   amounts of market cap.** Relative to value-weighting — the approach taken by indices and
   (necessarily) by investors collectively — the FF approach overweights stocks in the small value
   portfolio". The mechanism is pure arithmetic: equal-weighting sub-pools of very unequal size
   silently overweights whichever sub-pool is smallest, and whatever that sub-pool did then shows
   up as everyone else's alpha, with the sign flipping depending on the sign of the test
   portfolio's loading. They trace the consequence in both directions — the value-weighted
   Russell 2000, with a positive SMB loading, underperforms its FF benchmark, while the S&P 500,
   with a negative loading, outperforms. Their conclusion: "an equal-weighted SMB distorts alphas
   in two ways. First, overweighting value creates an artificially high average return for an
   equal-weighted SMB factor. Second, the equal-weighted SMB factor distorts portfolio weights in
   large stocks in a way that induces an offsetting HML loading."
2. **The benchmark's *composition* — which instrument types it contains — biases it.** The CRSP
   value-weighted market factor "includes not only U.S. common stocks, but also non-U.S. firms,
   closed-end funds, real estate investment trusts (REITs), and other securities such as shares of
   beneficial interest (SBIs)." Those other security types behaved materially differently from US
   common stocks over the sample — the residual slice carried a large, statistically significant
   negative four-factor alpha of its own (magnitude not recorded here, per this folder's
   anti-lookahead rules) — which made the whole index "a downward-biased benchmark for U.S.
   stocks". Part of that gap is structural rather than sample-specific: closed-end-fund returns
   "reflect underwriting and management fees", so that component "might be expected to persist".
   A benchmark that mixes
   instrument types inherits the mix's behaviour, and anything measured against it inherits the
   negative of that.
3. **Index reconstitution drags the index's own return down.** Stocks being added outperform
   stocks being deleted ahead of the effective date and reverse after, "lowering the returns on
   the index itself"; about half of the Russell 2000's negative alpha falls in the two
   reconstitution months. **This folder already covers this channel** — see
   `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` (Cai–Houge on Russell 2000
   rebalancing) — so it is recorded here only for completeness and because it is one of the three
   legs of this paper's argument. Note that the authors are careful that it is not the whole story:
   the Russell 2000's alpha is also significantly negative in the other ten months, and small-cap
   portfolios with negligible reconstitution effects show it too.

**The distinction that makes the finding usable**, and the one worth carrying as vocabulary:

> "These sources of nonzero alphas represent a combination of **ex-ante and ex-post biases**. For
> instance, the outperformance of small value and underperformance of non-U.S. common stocks
> included in CRSP during our time period need not persist out-of-sample. In contrast, the
> underperformance of closed-end funds, whose returns reflect underwriting and management fees,
> might be expected to persist. Even the ex-post biases we document are undesirable, however, in
> that they affect performance evaluation in the time period commonly studied, and they indicate a
> general lack of robustness, which could lead to **biased alphas (in either direction) in future
> time periods.**"

So a benchmark bias is either *structural* (a fee, a known cost, a construction asymmetry — it
persists and can be corrected for) or *realized-sample* (whatever that slice of the market
happened to do — it need not persist, and may reverse). The second kind is the dangerous one for
a lab with a fixed validation window, because it cannot be signed in advance.

## Construction recipe

There is no strategy here. There is a **diagnostic** and a **remedy principle**, both concrete.

**The diagnostic — a holdings-space weight comparison, and it is the most transferable thing in
the paper.** Any benchmark model implies a benchmark *portfolio*: "the sum of the product of the
Fama-French-Carhart factor portfolios and the estimated betas. This particular benchmark portfolio
(i.e., the 'fitted' or explained return) in turn implies specific weights on the portfolios in the
3x4 size-BM space, which can be quite different from the actual average weights of the benchmark
on these portfolios". Compare the two weight vectors. Their empirical result on that comparison is
the payoff:

> "We find that models producing close portfolio weight matches also produce smaller index alphas."

That is a cheap, holdings-only, returns-free test of whether a measured alpha is an artifact of
benchmark construction: **project both the benchmark and the thing under test onto the same grid
of characteristic cells, and look at the weight mismatch.** A large mismatch predicts a spurious
alpha; a small one predicts an honest number. It needs no new data and no return series.

**The remedy principle.** Their three fixes all follow one rule — make the benchmark resemble what
the evaluated portfolio could actually have held:

- Value-weight the factor sub-portfolios instead of equal-weighting them, and restrict the market
  factor to the security type under evaluation ("thereby bringing the FFC methodology closer to
  the practices of the asset managers it is used to evaluate").
- Or replace constructed factors with **tradable index-based factors** (S&P 500 for the market;
  Russell 2000 minus S&P 500 for size; Russell 3000 Value minus Growth for value), "which are
  value-weighted and exclude most of the underperforming securities included in the CRSP
  value-weighted index".
- Or allow the effect to differ across the size range, since "one value factor and one size factor
  are not enough to span historical returns across the size-value grid: there seems to be a
  separate value effect for small and large stocks".

Both remedy families "reduce index alphas significantly", and the index-based models performed
best in their mutual-fund application. The general rule: **a benchmark should be a portfolio the
evaluated strategy could have bought, weighted the way an investor would have had to weight it.**

## Robustness evidence (qualitative only)

- **Two independent families of test portfolios** — commercial indices (S&P, Russell, Dow Jones
  Wilshire) and CRSP size/book-to-market deciles — give the same conclusion, so it is not an
  artifact of one index provider's methodology.
- **Sample extension rather than sample mining**: the decile evidence strengthens on the long
  1927–2005 window, and the authors explicitly flag a sub-period where an index's alpha was
  approximately zero, reporting it as evidence of "a lack of robustness for the benchmark model"
  rather than hiding it. That is the methodology-honesty signal the rubric asks for.
- **Each channel is separately identified and separately remedied**, and the remedies are then
  tested on a *different* object (actively managed funds) from the one that motivated them.
- **Inference is conservative** — the joint test allows for clustering of returns within time
  periods, which is the right correction for test portfolios that share constituents.
- **Negative results reported**: they looked for a flows-based explanation ("whether flows into
  index funds or institutional portfolios benchmarked to the various indices are related to
  benchmark alphas") and "did not find any robust associations".
- **Known gaps.** Single market (US). The specific magnitudes are properties of the 1980–2005 CRSP
  universe and the authors say so, which is precisely their ex-post/ex-ante point; the *mechanisms*
  are arithmetic and transfer, the *magnitudes* do not. No independent replication of this
  particular paper was found by this session, though its three channels are each corroborated
  elsewhere in this folder's coverage.
- **Multiple testing**: acknowledged implicitly through the joint-null framing rather than through
  a formal haircut; this is a diagnostic paper, not an anomaly paper, so there is no factor zoo to
  deflate.
- **Costs**: not modeled, and they do not need to be for the argument — but see Implementability
  item 3, where cost treatment of the benchmark is exactly the open question for this lab.

## Implementability here

**Which panel.** The protocol v3 panel: ~1,400 stocks that were ever members of nine indices
(S&P 500 from 1996; DAX, CAC 40, FTSE 100, SMI, AEX, Euro Stoxx 50, Nikkei 225, Hang Seng from
2009) plus 42 ETFs, point-in-time, ~1,000 eligible on a typical validation date. Nothing in this
note is a candidate; all of it is about how to read a v3 number.

The paper's three channels map onto the v3 benchmark one for one, and the first two are open
questions rather than findings — this agent cannot settle them, because doing so means reading
`engine/`, which a strategy session may do and this one may not.

1. **Channel 1 applies directly, and arithmetically: the equal-weight eligible pool equal-weights
   nine indices that contribute wildly different numbers of names.** The S&P 500 leg contributes
   on the order of 500 eligible names; SMI, AEX and CAC 40 contribute tens each. An equal-weight
   pool across the union therefore assigns **country weights equal to name counts** — neither
   capitalisation weights nor anything an investor could hold or would choose. This is *exactly*
   CPZ's "equal-weights the sub-portfolios even though they contain very different amounts of
   market cap", one level up: the sub-pools here are countries rather than size-value cells. The
   consequence is the same and runs in both directions: a candidate that happens to tilt toward
   the under-represented small-index countries is measured against a benchmark that underweights
   them, and the difference shows up as skill or its absence with **no signal content whatever**.
   The lab's v3 audit already notes that the collapsed v2 books were "71%-non-US"; this note says
   that the pool's own regional composition is the other half of that comparison and has not been
   characterised.
2. **Channel 2 applies too, and this one is cheap to check: the pool mixes instrument types.**
   Forty-two ETFs equal-weighted alongside ~1,000 single stocks puts roughly 4% of the benchmark
   in ETFs, and that share *drifts mechanically* as index membership grows over the sample (the
   42 ETFs are fixed; the stock count grows, and `program.md` notes coverage before 2009 is far
   thinner). An ETF is a diversified basket, so equal-weighting one next to a single stock is a
   risk-weight mismatch of the kind CPZ found biased CRSP-VW. Whether it biases this benchmark up
   or down depends on what the 42 are, which this agent has not read and should not assert. **The
   checkable question is: does the pool's ETF weight share change materially between the train and
   validation windows?** If it does, the benchmark is not the same object across splits, and
   train-vs-validation skill comparisons inherit that.
3. **The question this folder keeps having to defer, now with a second reason: is the equal-weight
   pool charged costs, and on what rebalance grid?** Protocol v3 charges candidates realistic
   per-name costs including transaction taxes (see tonight's companion note). An equal-weight pool
   of ~1,000 point-in-time index members is **not** a passive buy-and-hold: it must trade to
   maintain equal weights and to track membership changes, so it has turnover and, on the FTSE,
   CAC and Hang Seng legs, stamp duty. If the pool's Sharpe is computed gross while candidates are
   charged, skill is biased *downward* by the pool's un-charged turnover and every v3 skill number
   is too pessimistic by a constant. If the pool is charged, the comparison is fair but the pool's
   own cost drag becomes a function of index-membership churn, which channel 3 above says is not
   return-neutral. **Either answer is fine; not knowing which is not.** This is `SUMMARY.md`'s
   standing item **#188(a)** — "one look at `engine/` by someone allowed to take it" — which has
   been the top-ranked item for six nights. It was already the right call; under v3 it is strictly
   more urgent, because v1/v2 numbers were deflated against zero and needed no benchmark at all,
   whereas every v3 number is a difference against this specific portfolio.
4. **A free diagnostic the lab can run tonight, and the best thing in this note: the weight-match
   test.** CPZ's finding that "models producing close portfolio weight matches also produce
   smaller index alphas" gives a holdings-only, returns-free, train-only check. Partition the
   eligible panel into cells on axes the lab already has — **listing region × liquidity tier ×
   tax status** are the natural ones under v3, since the engine computes all three — then compare
   a candidate's average cell weights against the equal-weight pool's. A large mismatch says the
   measured skill is substantially a cell-exposure difference; a small mismatch says it is more
   likely signal. This is the same genre as the cheap holdings-only diagnostics `learnings.md`
   already credits with "killing ideas before they cost a trial" (HHI, position counts, the
   entry/exit vs re-sizing turnover decomposition), it needs no trial and no holdout, and it is
   arguably a *reporting* rule rather than a one-off: any v3 skill number would be easier to read
   next to its candidate-vs-pool cell-weight mismatch.
5. **An anti-candidate, stated so nobody builds it.** The temptation this note creates is to
   design a candidate that *exploits* the pool's construction — e.g. tilt toward whichever
   region or instrument type the equal-weight pool under-weights. That would raise measured skill
   without any claim about returns, and it is gaming the statistic rather than finding an edge.
   It is also exactly what CPZ warn about in reverse. If the pool's construction is biased, the
   remedy is to fix or characterise the benchmark (items 1–4, and a human's call on the engine),
   never to build a candidate whose edge is the benchmark's flaw. Flag it in the journal if a
   candidate's skill turns out to be mostly cell mismatch; do not harvest it.

**Pitfalls.** (a) Do not import CPZ's magnitudes — they are 1980–2005 US CRSP properties and the
authors are explicit that the ex-post component need not persist. The arithmetic channels transfer;
the numbers do not. (b) "The benchmark has alpha" is not an argument that the v3 statistic is worse
than the v1/v2 one; it is plainly better, and the right reading is that v3 moved the uncertainty
from the null to the benchmark, where it is at least characterisable. (c) The weight-match
diagnostic is about *average* weights and will miss a candidate whose cell exposures move over
time; it is a screen, not a proof.

## Related

- `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — Daniel–Sornette–Wöhrmann
  and Cai–Houge. **Covers CPZ's third channel already** (Russell reconstitution), which is why this
  note leads on the first two. Read together, the two notes cover all three of the paper's legs.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal on equal weighting
  as a *strategy*. The contrast is the whole point of this note: that literature asks whether 1/N
  is a good portfolio to *hold*; this one asks what happens when 1/N is the thing you *measure
  against*. A portfolio can be an excellent choice and a poor benchmark simultaneously.
- `notes/2026-08-21-diversification-return-and-rebalancing.md` and
  `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the equal-weight pool must
  rebalance to stay equal-weighted, so whatever those notes conclude about the rebalancing/
  diversification return applies to **the benchmark**, not only to candidates. Note the live
  tension between them (one treats the rebalancing return as real, the other disputes the
  attribution); under v3 that tension is no longer academic, because it is a dispute about the
  benchmark's own expected return. **Not resolved here and not resolvable from the literature —
  it depends on how the engine computes the pool.**
- `notes/2026-10-08-securities-transaction-taxes-turnover-and-holding-period.md` (tonight) —
  item 3's cost question in its tax-specific form: an equal-weight pool spanning the FTSE, CAC and
  Hang Seng legs pays stamp duty on its own maintenance turnover, if it is charged at all.
- `notes/2026-09-23-mean-variance-spanning-and-intersection.md` and
  `notes/2026-09-23-spanning-under-short-sales-and-costs.md` — the formal machinery for asking
  whether a candidate adds anything to a benchmark, which is the hypothesis-testing version of
  what the v3 skill statistic estimates informally.
- `experiments/learnings.md`, Protocol v3 section — "beating the null is not beating the pool" is
  the lab's own statement of why the benchmark now matters. This note's contribution is the next
  step: the pool is not a neutral object either, and there is a cheap diagnostic for how far it is
  from neutral for any given candidate.
