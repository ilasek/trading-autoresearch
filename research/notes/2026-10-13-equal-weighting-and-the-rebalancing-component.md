---
title: "Equal or Value Weighting? Implications for Asset-Pricing Tests — earlier and more pointedly titled: Why Does an Equal-Weighted Portfolio Outperform Value- and Price-Weighted Portfolios?"
authors: Plyakha, Uppal, Vilkov
year: 2012 (working paper), 2014 (revised working paper), 2021 (book chapter)
venue: "Chapter 9 in Zopounidis, Benkraiem, Kalaitzoglou (eds), *Financial Risk Management and Modeling*, Springer (Risk, Systems and Decisions series) — venue tier 2/3: an edited-volume chapter, peer-reviewed at the volume level but not a journal of the JF/JFE/RFS/JFQA/ManSci/JPM tier. Circulated for roughly a decade as an EDHEC-Risk / SSRN working paper"
url: https://doi.org/10.1007/978-3-030-66691-0_9 · working-paper record https://ssrn.com/abstract=1787045 · author-hosted abstract https://www.vilkov.net/research.html
citations: "56 (Semantic Scholar, DOI endpoint on the chapter DOI, checked 2026-10-13); 5 (Crossref is-referenced-by-count on the same chapter DOI, checked 2026-10-13); a separate Semantic Scholar record for the SSRN working-paper DOI 10.2139/ssrn.1787045 reports 16. The three counts are splits of one paper across three identifiers, and the Crossref count is low because a 2021 book chapter inherits none of the working paper's decade of citations — grade this on the 56 and on the fact that an unrelated Tier-2 journal article (see the companion note tonight) builds its whole contribution on it"
sample_period: "approximately four decades of US data ending around 2010 — the working-paper abstract says 'the major U.S. equity indices over the last four decades'. The exact window was NOT verified: the full text was not obtained (see Access)"
markets: US only; the constituents of the major US large-cap indices (S&P 500 chief among them)
tier: "B — well cited for its vintage, the mechanism is checkable against independent algebra the folder already holds, and it is the direct literature on the object protocol v3 grades against; but single-market, single-decade-vintage, no transaction costs in the headline comparison, no independent replication of the *decomposition* located, and **the full text was not read** (abstract-level only)"
validation_overlap: false
published_post_2018: false
---

## Access — read at abstract level only, and this closes a standing pointer

`research/SUMMARY.md`'s open questions have carried this source for two sessions as **"the
highest-value unread item this folder knows of"**, with four channels already spent (SSRN 403,
the EDHEC registration wall, the closed Springer chapter, one third-party mirror unreachable at
the transport layer). Five more were spent tonight and the full text is still not obtained:

1. **`vilkov.net` (the third author's own site) is reachable and is a metadata win, not a
   full-text one.** `https://www.vilkov.net/research.html` returns a 42 KB HTML page listing
   every paper with its **verbatim published abstract inline** — but every link on it goes to
   `ssrn.com/abstract=…` or to a publisher DOI. There is no self-hosted PDF directory. This is
   worth recording as a *category*: a prolific author's site can be a reliable abstract source
   while hosting no files at all, which is the opposite of the 2026-09-18 faculty-page lesson.
2. **The third-party mirror reset again.** `trevcan.duckdns.org/...` died with
   `curl: (35) Recv failure: Connection reset by peer` — a **transport failure, not an origin
   refusal**, confirming what `SUMMARY.md` recorded, and the second host after `web.archive.org`
   and `api.fatcat.wiki` with that exact signature.
3. **EDHEC's publication pages carry the full abstract in a `<meta name="description">` tag.**
   `climateinstitute.edhec.edu/publications/<slug>` is a Drupal 11 page with **no `.pdf` href
   anywhere in the body** (the registration wall `SUMMARY.md` recorded), but the meta
   description holds the working-paper abstract verbatim, and the cover thumbnail
   (`/sites/default/files/styles/cover/public/old/<slug>.jpg.webp`) proves a PDF exists behind
   the wall. **Reading a page's meta tags is worth one grep before concluding it holds nothing.**
4. **Two path guesses off that thumbnail 404'd** (`/sites/default/files/old/<slug>.pdf` and the
   old `risk.edhec.edu/sites/risk/files/…` form), each returning HTTP 404 with a ~56 KB HTML body.
5. **Semantic Scholar's title-endpoint 429 blocked the one remaining abstract source**, exactly
   as `research/README.md` warns; `www.semanticscholar.org` itself returns 403 to `WebFetch`.

So what is recorded below comes from: the **verbatim published abstract** of the 2021 chapter
(author-hosted), the **verbatim abstract** of the 2012 working paper (EDHEC meta description),
and the exposition of this paper in **Hanke, Keswani, Quigley, Stolin & Zagonov (2019)**, which
*was* read in full tonight (see the companion note). Anything attributed to the paper's body
rather than its abstract is flagged. The honest status is: **the pointer is now resolved to
abstract level and should stop being carried as unread, but the body is still unobtained, and
one claim circulating in secondary summaries is explicitly marked unverified below.**

## Mechanism

The question is the one protocol v3 made structural for this lab: **what does an equal-weighted
portfolio of an index's members earn, and where does it come from?** Under v3 every candidate is
scored as *skill* — its Sharpe minus the equal-weight eligible pool's Sharpe on the same days —
so the benchmark's own return generator is no longer background. It is the thing being subtracted.

The paper's answer splits that return in two.

1. **A systematic part, which is a factor tilt and nothing more.** Weighting the members of a
   large-cap index equally rather than by capitalisation mechanically overweights the smaller
   and cheaper members. The abstract: *"this is partly because the equal-weighted portfolio has
   higher exposure to value and size factors"* — the 2012 version adds market exposure to that
   list. This part is not a puzzle and not an edge; it is a long position in known factor
   premia, available passively.
2. **A part that survives those factors, and the authors attribute it to the rebalancing
   itself.** The chapter abstract: *"we show that a considerable part (42%) comes from
   rebalancing to maintain constant weights."* The decomposition share is theirs and belongs to
   their sample; what transfers is the **existence of a second channel that a four-factor model
   does not absorb**, located in the act of restoring fixed weights rather than in the weights.

Two further mechanism-level claims, both important here, and of different evidentiary status:

- **Equality is not the active ingredient; constancy is.** Secondary summaries of the paper
  report its finding that *choosing the constant weights to be equal is not crucial* — any
  fixed-weight target that is rebalanced behaves the same way. This is consistent with the
  algebra in `notes/2026-08-21-diversification-return-and-rebalancing.md`, where the
  diversification-return identity requires **constant** weights and says nothing about their
  being equal. Status: abstract/secondary, not verified against the body.
- **The rebalancing channel is contrarian.** Secondary summaries attribute the residual to the
  monthly rebalance acting as a contrarian trade with exposure to reversal and to idiosyncratic
  volatility. **This specific wording is NOT verified against the paper's text** and is recorded
  here as a pointer, not a claim — but note that it is the *only* economic story under which the
  channel can exist at all, for a reason the folder already owns: see the tension below.

## The tension with a refutation this folder already holds — and how it resolves

`notes/2026-08-22-rebalancing-return-attribution-critique.md` (Cuthbertson, Hayley,
Motson & Nitzsche, 2016) is a direct, pre-existing contradiction of the
*attribution* above, and `research/README.md` requires it be stated rather than ignored.
Cuthbertson et al. derive that:

- excess growth is **not** created by rebalancing — an unrebalanced basket earns the same
  `E[GM] ≈ E[AM] − σ²/2` benefit;
- rebalanced and buy-and-hold books start with **identical** expected growth and diverge only as
  the buy-and-hold weights drift and the book de-diversifies;
- **under IID returns the rebalancing trades have exactly zero expected value**, and they are
  profitable *only* where relative prices mean-revert and lose where relative prices trend.

Taken together with Plyakha–Uppal–Vilkov, the two sources are **not inconsistent — they are a
conditional and its antecedent**, and reading them together is more informative than either:

> A fixed-weight rebalanced book's advantage over the drifting version of itself is **not** an
> arithmetic entitlement. It is a bet that relative prices among the members mean-revert at the
> rebalance horizon. Plyakha–Uppal–Vilkov's residual channel, if real, *is* that bet paying on
> monthly US large-cap data; Cuthbertson et al. say there is no other way for it to pay.

That resolution is what makes the channel a **tradeable-mechanism claim** rather than an
accounting artifact — and therefore something v3's fill rule can interact with (below).

## Construction recipe

Minimal and fully specified by the abstracts plus the companion paper:

1. **Universe:** the members of a broad large-cap index, point-in-time.
2. **Weights:** `w_i = 1/N` over the members eligible on the rebalance date (or any other fixed
   target vector; constancy is the ingredient).
3. **Cadence:** restore the target **monthly**. The comparison portfolios are the
   capitalisation-weighted and price-weighted versions of the same universe, which need no
   rebalancing by construction.
4. **Decomposition:** regress the EW−VW return difference on market, size, value and momentum;
   the fitted part is the tilt, the intercept is the channel in dispute. (The published
   equal-weight index version of this construction rebalances **quarterly** and its reported
   annual turnover sits in the mid-20-percent range — see the companion note.)
5. **What to vary to test the mechanism rather than the label:** the same universe held
   **buy-and-hold from an equal-weight start** (isolates rebalancing from the weights) and a
   **non-equal fixed-weight target** rebalanced on the same grid (isolates constancy from
   equality).

## Robustness evidence (qualitative only)

- Multi-decade and multi-index **within the US**; no international evidence in this paper.
- The four applications the chapter title points at (CAPM tests, SDF spanning, the
  characteristics–returns relation, the pricing of idiosyncratic volatility) are *inference*
  robustness, not return robustness: the authors' broader claim is that asset-pricing test
  conclusions change with the weighting of the test portfolios. For this lab that is a warning
  about reading any external sorted-portfolio result, not a strategy.
- **Costs are absent from the headline comparison.** The channel in dispute is paid for with
  monthly turnover on the small end of a large-cap index, which is exactly where v3's liquidity
  tiers bite hardest. One secondary source reports the ranking surviving a 50 bps cost charge;
  that is a citation, not a verified result, and it is a flat charge rather than a tiered one.
- **Independent replication of the decomposition: none located.** The companion note's authors
  cite and rely on it but do not re-estimate it. The *mechanism* (diversification return,
  fixed-weight rebalancing) has an independent and partly adversarial literature, which the
  folder already holds in full.

## Implementability here

- **This is not a candidate. It is a description of the benchmark**, and that is why it matters:
  under v3 the lab is not graded against zero or against a cap-weighted market, but against the
  equal-weight eligible pool — i.e. against a portfolio that, on this literature's reading,
  already contains (a) a size/value tilt over its own universe and (b) a fixed-weight
  rebalancing channel whose only possible source is short-horizon relative mean reversion.
  **A candidate must beat both to show positive skill.** Every pre-v3 learning in
  `experiments/learnings.md` calibrated against a different null, and this is a second,
  independent reason — alongside `SUMMARY.md` #234's — not to carry those constants forward.
- **The lab cannot build the other side of this axis at all.** The EW-vs-VW comparison needs
  market capitalisations; the panel has no fundamentals and no share counts. `dollar_volume` is
  **not** a capitalisation proxy — it is price × traded shares, a liquidity measure the folder
  has three notes about (`notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`,
  `notes/2026-08-31-amihud-volume-component-decomposition.md`) — and substituting it would test
  a different hypothesis under a borrowed name. So the only usable content here is about the
  benchmark, not about a rival weighting.
- **The question this sharpens, and it is `SUMMARY.md` #217's, not a new one.** #217 asks for one
  look at `engine/` by someone allowed to take it. This note adds a fifth question to its list,
  with a predicted sign in each direction, and it is the highest-consequence question tonight:
  **on what grid, at what fills, and at what cost is the equal-weight pool itself maintained?**
  - If the pool is **rebalanced to equal weight on a grid and charged v3's costs**, then the
    benchmark is paying for the rebalancing channel, and a candidate's measured skill is the
    *net* of that channel — a harder bar, but a coherent one.
  - If the pool is **rebalanced free of cost**, the benchmark is receiving a channel nobody pays
    for, and every candidate is short an unpriced contrarian position.
  - If the pool is rebalanced **at each date's own close** while candidates fill at the next real
    close (v3's rule, which exists precisely to kill same-close mean reversion), then the
    benchmark holds a reversal bet that **no candidate is permitted to replicate**. That
    asymmetry would be worth knowing about before another trial is designed against it.
  - If the pool **drifts** (buy-and-hold from an equal-weight start), it has no rebalancing
    channel at all, and — by Cuthbertson et al.'s result 2 — it de-diversifies over the split,
    which a candidate that merely rebalances to equal weight would beat **for free**.
  This is a reading of `engine/`, not a research task, and this agent may not take it: a learning
  agent writes only inside `research/`. Recorded as a question with its four answers.
- **A free diagnostic that needs no holdout and no candidate file, for whoever runs the census
  pass.** On the train split only, compute the equal-weight pool's return two ways — restored to
  equal weight on the protocol's grid, and held from an equal-weight start — and difference them.
  That difference *is* the rebalancing channel on this panel, measured rather than imported, and
  its sign answers whether relative prices among eligible large caps mean-revert at the rebalance
  horizon here. It slots into the single census pass `SUMMARY.md` already schedules (#220, #214,
  #227, #233, #239, #240) and shares that pass's machinery.
- **Do not import the decomposition share.** 42% is a US large-cap number from a pre-2010 sample
  under free trading. The folder's standing rule about carrying constants across panels and
  protocol versions (`CLAUDE.md`, "The learnings file is mostly about one family, and none of it
  is v3") applies to external constants with at least equal force.

## Related

- `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the pre-existing refutation of
  this paper's *attribution*, and the source of the conditional that makes its residual channel a
  mean-reversion bet rather than an entitlement. Read the two together or neither.
- `notes/2026-08-21-diversification-return-and-rebalancing.md` — the identity that requires
  constant weights and is silent on their equality, which is why "equality is not the active
  ingredient" is the prediction to expect.
- `notes/2026-08-22-excess-growth-and-return-decomposition.md` — the continuous-time version of
  the same object; note that the lab has already measured `γ*`, the excess growth rate, as **a
  null on this universe** (`experiments/learnings.md`), which is a third, *internal* reason to
  expect the channel here to be small.
- `notes/2026-10-13-equal-minus-value-as-a-performance-evaluation-factor.md` — tonight's
  companion, which turns this paper's finding into a factor, was read in full, and shows the tilt
  is pervasive in professionally managed money.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the `1/N` literature, which asks whether
  equal weighting beats *optimisation*; this paper asks what equal weighting earns against
  *capitalisation*. Different questions, routinely conflated.
- `research/SUMMARY.md` candidate ideas #217 (the `engine/` read, now with a fifth question),
  #234 (anchoring compresses the measured statistic), and the census pass.
