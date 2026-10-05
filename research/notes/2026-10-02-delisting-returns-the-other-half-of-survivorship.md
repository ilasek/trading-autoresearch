---
title: "The Delisting Bias in CRSP Data — with: The Delisting Bias in CRSP's Nasdaq Data and Its Implications for the Size Effect; and Delisting Returns and Their Effect on Accounting-Based Market Anomalies"
authors: Shumway; Shumway & Warther; Beaver, McNichols & Price
year: 1997; 1999; 2007
venue: Journal of Finance 52(1), 327–340 (Tier 1); Journal of Finance 54(6), 2361–2379 (Tier 1); Journal of Accounting and Economics 43(2–3), 341–368 (Tier 1)
url: https://doi.org/10.1111/j.1540-6261.1997.tb03818.x ; https://doi.org/10.1111/0022-1082.00192 ; https://doi.org/10.1016/j.jacceco.2006.12.002
citations: "Shumway 1997: 1,072 (Crossref is-referenced-by-count, checked 2026-10-02); 1,131 (Semantic Scholar DOI endpoint, checked 2026-10-02). Shumway–Warther 1999: 483 (Crossref, checked 2026-10-02); 512 (Semantic Scholar, checked 2026-10-02). Beaver–McNichols–Price 2007: 231 (Crossref, checked 2026-10-02); Semantic Scholar returns `not found` for the DOI. OpenAlex not consulted — free daily budget already exhausted at session start."
sample_period: "Shumway 1997: CRSP delistings from 1962 onward, with over-the-counter prices after delisting. Shumway–Warther 1999: CRSP's NASDAQ file (NASDAQ enters CRSP in 1973). Beaver–McNichols–Price 2007: not read, sample window not claimed here. Context count read from Hou–Xue–Zhang's Appendix B: 16,745 delistings of nonfinancial NYSE/Amex/NASDAQ firms 1925–2016, of which 86% have an available delisting event return."
markets: US equities — NYSE/Amex (Shumway 1997), NASDAQ (Shumway–Warther 1999), US accounting-anomaly samples (Beaver–McNichols–Price)
tier: "A for all three on venue, citation count and the fact that each is a data-construction result rather than a return estimate — there is nothing in a measurement convention to decay. **But coverage here is partial:** none of the three was read in full (see Access). Treat every sentence attributed to them below as abstract-level unless it is explicitly sourced to Hou–Xue–Zhang's Appendix B, which was read in full."
validation_overlap: false (no sample reaches 2018)
published_post_2018: false
---

## Access

**None of the three was read in full, and this is the third session to fail on the first two.**

- **Shumway 1997 and Shumway–Warther 1999.** Unpaywall, OpenAlex and Semantic Scholar all report
  exactly one OA location for each, and it is the same host: `scholarsarchive.byu.edu`. It is
  Cloudflare-challenged on **every** PDF endpoint — `context/facpub/article/<id>/viewcontent/<file>.pdf`
  and `cgi/viewcontent.cgi?article=<id>&context=facpub` alike, HTTP 403 with a ~6 KB "Just a moment…"
  body, with and without a browser user-agent and a matching referer. This re-confirms the 2026-10-01
  finding. **New tonight: the bepress *landing* pages are not challenged** (`/facpub/9278`,
  `/facpub/9279` both return 200), and they carry the publisher abstract in a `meta name="description"`
  tag. That is how the abstracts below were obtained, and it is a cheap trick worth reusing: when a
  bepress PDF is blocked, the landing page's meta description is still an authoritative abstract.
  Routes that also failed tonight: `deepblue.lib.umich.edu` (Michigan's repository — **also
  Cloudflare-challenged**, HTTP 403, and Shumway was at Michigan when both papers were written);
  `ideas.repec.org` (indexes both, hosts neither); `academicnewsletter.sufe.edu.cn` (connection reset).
- **Beaver–McNichols–Price 2007.** `oa_status: closed`, no OA location anywhere. The SSRN working
  version (`10.2139/ssrn.949601`) is behind SSRN's bot challenge. `gsbpreserve.stanford.edu` offers a
  download for the record which turns out to be **a 88 KB placeholder thumbnail PDF labelled
  "off-site-publication"** — a twelfth refusal shape, and one that returns HTTP 200 with a real zip
  archive, so it passes every "did I get a file?" check and contains nothing. The abstract below is
  the authoritative one, read from **Stanford GSB's own publication page**
  (`gsb.stanford.edu/faculty-research/research/publications/delisting-returns-their-effect-accounting-based-market`),
  which carries the full publisher abstract in the page body. RePEc's record for this article says
  "No abstract is available for this item."
- **What *was* read in full** is Appendix B of Hou–Xue–Zhang (2020, RFS)
  (`2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md`), which implements
  Beaver–McNichols–Price's delisting adjustment step by step and cites both Shumway papers for why
  the adjustment is necessary. The construction recipe below is read from there, not from the
  originals.

## Mechanism

[2026-10-01] covered what conditioning a sample on survival does to **the names that stay**:
`dp* = (μ + σ²·π_p/π)dt + σ dz`, drift added in proportion to variance, variance unchanged. This note
is the other half — **the returns of the names that leave** — and it is the half a point-in-time
membership fix has to supply separately, because knowing *who was in the index in 1998* does not by
itself tell you *what the ones that disappeared returned on the way out*.

**Three mechanisms, in increasing order of usefulness to this lab.**

**1. The omitted return is large, negative, and a surprise (Shumway 1997).** Delistings for bankruptcy
and other negative reasons "are generally surprises," and the correct delisting return "is not
available for most of the stocks that have been delisted for negative reasons." Using
over-the-counter prices observed *after* the delisting, Shumway shows the omitted returns are large.
Two things follow. First, a panel that silently drops the final observation of a negatively-delisted
name is missing a large negative number, so the sample's measured mean return is biased upward — the
same sign as the survival-conditioning drift, arriving through a different door. Second, because the
delisting is a *surprise*, the missing return cannot be forecast from the name's own prior
information set; it is not a predictable component that a causal model could have anticipated.

**2. The correction is a venue-specific constant, and it is big (Shumway–Warther 1999).** On CRSP's
NASDAQ file the missing returns are "large and negative on average," delisted stocks suffer "a
substantial decrease in liquidity," and the authors estimate that **replacing a missing
performance-related delisting return with −55% corrects the bias.** Their application is the sharpest
statement in the cluster of what the bias can do to a *cross-sectional* result: after the correction,
"there is no evidence that there ever was a size effect on NASDAQ," and they note this is inconsistent
with most risk-based explanations of the size effect. An entire published cross-sectional premium, in
one market, turns out to be the delisting bias wearing a size label.

**3. The sign of the induced bias in a sorted book is not fixed — it is set by which decile the
leavers occupy (Beaver–McNichols–Price 2007).** This is the mechanism that generalises, and it is the
reason this note matters more than its two predecessors. Their result, from the abstract:

> "We show that tests of market efficiency are sensitive to the inclusion of delisting firm-years.
> When included, trading strategy returns based on anomaly variables can increase (for strategies
> based on earnings, cash flows and the book-to-market ratio) or decrease (for a strategy based on
> accruals). This is due to the disproportionate number of delisting firm-years in the lowest decile
> of these variables. Delisting firm-years are most often excluded because the researcher does not
> correctly incorporate delisting returns, because delisting return data are missing or because other
> research design choices implicitly exclude them."

Read it as a rule rather than as four findings: **exiting names are not spread evenly over a sort.
They crowd one end of it, and which end decides the sign.** If a strategy is *short* the decile the
leavers crowd, including their large negative returns *raises* its measured spread; if it is *long*
that decile, including them *lowers* it. The direction is therefore a property of the pairing between
the score and the exit hazard, not of the delisting bias as such — which is why "survivorship bias
inflates results" is only half a sentence, and why the lab cannot sign its own artifact without
asking which end of its score the near-exit names sit at.

The third sentence is the practical one. Delisting firm-years are usually dropped **not by decision
but by construction** — a missing final return, a research-design filter that requires 12 months of
subsequent data, a complete-case merge. This folder has a separate note on exactly that failure mode
(`2026-09-12-missing-data-and-complete-case-pools.md`); this is its most consequential instance.

## Construction recipe

Read from Hou–Xue–Zhang's Appendix B, which implements Beaver–McNichols–Price's procedure. Written out
here because it is the recipe a point-in-time cutover in this repo would need, and because the
causality property of the imputation is the part that is easy to get wrong.

**The delisting-adjusted monthly return.** For a delisting on day `d` strictly before the last trading
day of month `t`:

    DR_t = (1 + pmr_dt)(1 + der_dt) − 1

where `pmr_dt` is the partial-month return from the start of month `t` to the delisting day, and
`der_dt` is the delisting *event* return. The partial-month return is recovered in whichever of three
ways is available, in order of preference:

1. If the delisting date equals the delisting payment date, the monthly delisting return *is* the
   partial-month return: `pmr_dt = mdr_t`.
2. If the delisting date precedes the payment date, back it out:
   `pmr_dt = (1 + mdr_t)/(1 + der_dt) − 1`.
3. Otherwise accumulate daily returns from the start of the month to the delisting day:
   `pmr_dt = Π_{i=1..d}(1 + ret_it) − 1`.

**For a delisting on the last trading day of month `t`,** HXZ take `DR_t = ret_t` (the ordinary full
month) and push the event return into the next month, `DR_{t+1} = der_dt`. They depart from
Beaver–McNichols–Price here deliberately, and the reason is a causality argument worth keeping:
delisting generally occurs after the close, delisting events are surprises, and the payoff cannot be
determined immediately (they cite Shumway 1997). **Booking a last-day delisting return inside the
month it was announced is a one-day peek.** The lab's own protocol applies a 1-day execution lag for
the same reason; this is that discipline applied to a corporate event.

**Imputing a missing event return.** 14% of delisting event returns are unavailable in the count HXZ
report. Two conventions, and they are not equivalent:

- **Static (Shumway–Warther):** substitute a single constant, −55%, for a missing
  performance-related NASDAQ delisting return.
- **Rolling and conditional (HXZ, extending Beaver–McNichols–Price):** substitute the average of the
  *available* delisting returns with the same **stock exchange** and **delisting type** (1-digit
  delisting code) over the **trailing 60 months**. HXZ condition on exchange and type because average
  delisting returns differ materially across both; they add the 60-month window — which
  Beaver–McNichols–Price do not — because the averages also move over time.

**The second convention is the one to prefer in this lab, and not because it is newer.** A trailing
60-month conditional mean uses only information available before the event, so it survives a causality
check; a single global constant fitted over a whole sample is a full-sample statistic applied
backwards, which is exactly the shape `causality_check` is built to catch. If a cutover here imputes
anything, it should impute from a trailing window.

## Robustness evidence (qualitative only)

The three results have held up in the strongest available way: **they were adopted as standard
practice.** HXZ apply the Beaver–McNichols–Price adjustment to all 452 anomalies in a Tier-1
replication and cite both Shumway papers as the reason omission is not an option; the convention
appears in the data sections of the modern cross-sectional literature generally. Citation counts
(1,072 / 483 / 231 on Crossref) are consistent with that. None of this is a replication of the
*magnitudes* — the −55% constant in particular is one market, one data vendor, one era, and nothing
read here re-estimates it.

**What is not established, and must not be assumed.** No source read tonight gives a non-US delisting
correction, and nothing read gives a correction for an **ETF** that closes or merges. This repo's
universe is global and 42 of ~145 instruments are ETFs; both gaps are live.

## Implementability here

**The lab's situation is more severe than CRSP's, not less.** CRSP has the delisted names and may be
missing their final return. This repo's store has **no delisted names at all** — the universe is
today's constituents, so a name that exited is absent for its entire history, not just for its last
month. There is nothing to impute, because there is no row. That makes the delisting-return convention
above a recipe for the *fix* rather than a patch for the current store, and it is the half of the fix
that `origin/survivorship-pit-v2` would still owe even if its membership history is perfect: a
point-in-time constituent list says who was in, and says nothing about what the ones who left earned
on the way out. **If that branch's re-scoring treats an exited name as simply ending, it is still
omitting the large negative return, and its corrected numbers are themselves optimistic.** That is a
reading to put to the human, not a verdict on the branch, which this folder has not seen.

**The free, holdout-free diagnostic this note makes available, and it is the useful output.**
Beaver–McNichols–Price's rule says the sign of the omission bias on a sorted book is set by **which
end of the score the near-exit names occupy.** The lab cannot observe its own exited names — but it
can observe the *proxy* for exit hazard among the names it has, and it already computes every
ingredient:

1. Build a near-exit proxy on the train split from panels the lab already has — some combination of
   realised volatility level, maximum drawdown depth, price level, and Amihud illiquidity. Each is a
   documented component of distress in this folder's own notes
   (`2026-09-29-funding-liquidity-and-margin-spirals.md`, `2026-09-22-limits-of-arbitrage-performance-based.md`).
2. Measure the cross-sectional rank correlation between that proxy and **the champion's own score**.
3. Read the sign. If the book **buys** the high-hazard end, the omission of exited names flatters it,
   and the flattery is largest exactly where the book is most concentrated. If it **avoids** that end,
   the omission works against the measured result and the artifact story is weaker than
   `learnings.md` currently assumes.

This is a `price-trend`-free, trial-free, train-split-only measurement, and it pairs directly with
[2026-10-01]'s **#179**: that item predicts the artifact should be linear in `σ²` and concentrate in
the near-exit tercile; this one predicts the artifact's **sign on the book** follows the score/hazard
alignment. Together they are a two-sided test of the same theory, and either outcome is informative.

**The prediction it already makes, stated so it can be wrong.** `learnings.md` records, across
fourteen mechanism screens, that on this universe the volatility *level* is the survivorship artifact
and that a long-only book tilting toward high-volatility survivors is rewarded. Exit hazard rises with
volatility, with illiquidity, and with drawdown depth. So the lab's artifact should be **largest for
scores that buy the high-volatility end and smallest or reversed for scores that buy the low-volatility
end** — and the recently seated low-beta-flavoured `range-variance` book should therefore show *less*
of it than the volatility-level screens did. If that ordering does not hold, the
"which-decile-do-the-leavers-occupy" mechanism is not what is driving this repo's artifact and
something else is.

**Pitfalls.**
- Do not carry the **−55%** constant into this universe. It is NASDAQ, one vendor, performance-related
  delistings only. `CLAUDE.md`'s rule about not importing constants by analogy applies with full force:
  there is no non-US estimate in anything read here.
- Do not treat ETF closures as delistings of this kind. An index ETF that closes returns NAV; a
  bankrupt operating company does not. The ETF half of this universe is genuinely less exposed, which
  is the documented basis for `program.md`'s "ETF-level strategies suffer least".
- A delisting *event* return is not a delisting *month* return, and the three-way recovery of
  `pmr_dt` above exists precisely because conflating them is the common error. If a cutover here
  computes the leavers' returns, the last-day case must push the event return into the following
  month or it peeks.
- The near-exit proxy is a proxy. Nothing in this repo's store can validate it, because the names it
  would be validated against are the ones that are missing. Report it as a proxy and never as a hazard
  estimate.

## Related

- `2026-10-01-survival-conditioning-induced-drift.md` — the other half: what conditioning does to the
  survivors. Read as a pair; neither is complete alone.
- `2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — Appendix B of that paper is the
  construction primary for this one, and its microcap mechanism is the same "the extreme bucket fills
  with the pool's most extreme members" shape.
- `2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — selection on end-of-period
  rank, and the folder's first pass at this axis.
- `2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the *entry* channel (today's
  constituents were selected into the index), which is the third of three and the one this repo's
  universe suffers most directly.
- `2026-09-12-missing-data-and-complete-case-pools.md` — the general form of
  Beaver–McNichols–Price's third sentence: rows dropped by construction rather than by decision.
- `2026-09-13-listing-age-as-a-level-effect.md` — the other end of an instrument's life.
- `experiments/learnings.md` — "the level *is* the survivorship artifact", the claim this note gives a
  signable, testable refinement of.
