---
title: "An Evaluation of Alternative Equity Indices — Part 1: Heuristic and Optimised Weighting Schemes"
authors: Clare, Motson, Thomas
year: 2013
venue: "Cass Business School (Centre for Asset Management Research) report, circulated via SSRN — venue tier 3 (credible academic-practitioner research, sponsored by a consultancy, not peer reviewed). Read as the version of record in the City St George's institutional repository"
url: "https://doi.org/10.2139/ssrn.2242028 · full text read at https://openaccess.city.ac.uk/id/eprint/16844/1/Heuristic%20and%20Optimised%20Weighting%20Schemes.pdf"
citations: "5 (Crossref is-referenced-by-count, checked 2026-10-15); 19 (OpenAlex, checked 2026-10-15). Both undercount a sponsored industry report with no journal home; the result is widely re-cited under the 'monkey portfolio' label and is cited as a primary by Bachelard et al. (see Related)"
sample_period: 1968–2011 (annual rebalancing; monthly total returns)
markets: "US only — the 1,000 largest US stocks by market capitalisation at each year-end with five full years of prior return history, NYSE/Amex/NASDAQ, ETFs and ADRs excluded"
tier: "B — a long multi-decade sample, a construction described in enough detail to reimplement exactly, and the central claim rests on ten million simulations rather than on a single sort. The gaps are real: one market, not peer reviewed, sponsored, no formal inference (the simulations are described by their quantiles rather than tested), and the headline framing is about cap weighting rather than about the random draw itself"
validation_overlap: false
published_post_2018: false
---

## Access

First try, via `openaccess.city.ac.uk` — the third confirmed read from that host
(`research/README.md` records it as a channel for Elsevier accepted manuscripts; this is a
repository-hosted *report*, which widens what it is good for). HTTP 200, 1.3 MB, `pdftotext
-layout` → 135 KB of clean text, 729 instances of `" the "`, `( )`-dropout check zero. Figures are
not extractable, so every number below that would have come from a chart is deliberately absent;
the prose restates the quantiles that matter.

**The famous sibling source was NOT obtained.** Arnott, Hsu, Kalesnik & Tindall, "The Surprising
Alpha From Malkiel's Monkey and Upside-Down Strategies", *Journal of Portfolio Management* 39(4),
91–105 (2013), `doi:10.3905/jpm.2013.39.4.091` — 32 (Crossref) / 35 (Semantic Scholar) / 58
(OpenAlex) citations, all checked 2026-10-15 — is the better-known primary and is **venue tier 1**
on this folder's rubric. Two channels were spent and both failed exactly as
`research/README.md` predicts: OpenAlex reports `oa_status: green` with
`doi.org/10.2139/ssrn.2165563` as the location, and `papers.ssrn.com` returned **HTTP 403 with a
5.5 KB Cloudflare body**; the firm's own PDF library answered with **HTTP 200 and a 70 KB
"ResearchAffiliates.com — Choose your destination" page**. So `is_oa: green` was again not a
promise the file is fetchable, and that paper's claims appear below **only where Bachelard et al.
quote them verbatim**, marked as second-hand. It stays a named unobtained pointer.

## Mechanism

The folder reached this source looking for what the lab's random-selection null *earns*, and the
answer is structural rather than empirical: **a randomly weighted portfolio is a noisy perturbation
of the equal-weighted portfolio, so the entire "monkeys beat the index" literature is a statement
about the gap between equal and capitalisation weighting, and not about randomness at all.**

The construction makes this unavoidable. At each year-end the computer draws a name at random from
the 1,000 available, assigns it 0.1%, **replaces it in the pool**, and repeats 1,000 times; a name
drawn twice gets 0.2%, a name never drawn gets zero. The weight vector is therefore
multinomial(1000, 1/1000) — mean weight exactly `1/n`, dispersion `O(1/√n)` around it. Ten million
such indices were generated for every year in the sample. The authors note the consequence
themselves when reading their own distribution: the equal-weighted index's performance is
"understandably almost equivalent" to the **modal** random draw.

Three further mechanism-level readings, each of which has a direct analogue in the lab's own
measurements:

1. **The draw controls dispersion, not location.** Because the weight vector is a perturbation of
   `1/n`, the random distribution is centred on the equal-weighted portfolio and what the sampling
   scheme moves is its width. The authors test this directly: suspecting that 1,000 draws of 0.1%
   each could never produce a concentrated book and might therefore be rigged against cap weighting,
   they **re-ran the whole experiment with 100 draws of 1% each** — which lets a name reach a 10%
   weight on ten draws instead of a hundred — and the conclusion was unchanged.
2. **The percentile of a fixed strategy against a random distribution is a statement about one
   window and nothing more.** Measured on rolling multi-year windows, the proportion of the ten
   million draws that a *single fixed* weighting scheme beats sweeps essentially the whole 0–100%
   range, with windows in which it beats every one of ten million draws and windows in which it
   beats almost none. The ranking is not a property of the scheme.
3. **What beat the random distribution was risk weighting, and the only thing that beat all of it
   was variance minimisation.** Of the eight alternative weighting schemes they grade, the ones
   closest to equal weighting (equal weight itself, diversity weighting, risk clustering) sit at or
   below the middle of the random Sharpe distribution, every scheme that explicitly targets *risk*
   (inverse volatility, equal risk contribution, maximum diversification, "risk efficient") sits
   above most of the draws, and the minimum-variance construction produced a Sharpe ratio higher
   than that of **any** of the ten million draws. The pattern is that what separated a scheme from
   the random book was **how it set weights against the covariance structure**, not how cleverly it
   re-weighted on price or size.

The authors' own headline is the less interesting half — that cap weighting fared badly — and they
say as much: "it is not so much that these alternative indices are well designed … Instead, the
most important result of this paper is that [the] market-capitalisation weighted index has proved
to be a relatively unsuccessful investment strategy."

## Construction recipe

- **Pool.** At each year-end, the 1,000 largest names by market capitalisation that have five full
  years of prior return history. Point-in-time by construction; the five-year history requirement
  is a mild survival screen and the authors do not quantify it.
- **Random-weight draw.** `n` draws with replacement from the `n`-name pool, each worth `1/n`;
  equivalently, a multinomial weight vector. A coarser variant (`n/10` draws at `10/n` each) gives a
  materially more concentrated book and leaves the conclusion intact.
- **Rebalance.** Annually, at year-end, with the weights held for the year.
- **Reading the result.** Report the full distribution of the statistic over the draws (terminal
  wealth and Sharpe ratio were both used) and locate each candidate construction inside it as a
  quantile. No formal test is run; the quantile is read descriptively.
- **A liquidity consequence of any non-cap weighting, worth separating from the return claim.**
  Every one of their alternative schemes — the heuristic ones and the optimised ones alike — is
  substantially **underweight the highest-traded-volume decile** relative to cap weighting, and the
  optimised ones carry sizeable overweights to the lowest volume deciles. Deviating from cap
  weights buys a thinner book, mechanically.

## Robustness evidence (qualitative only)

- **Multi-decade, single market, point-in-time pool.** Four-plus decades of US large caps; nothing
  outside the US, and nothing about whether the pattern holds where the index composition is
  maintained differently.
- **Construction robustness is the strongest part**: the headline survives a tenfold change in the
  granularity of the random weighting, which is the one sensitivity that could have made the result
  an artifact of the sampler. It is *not* shown to survive a change in rebalance frequency, in pool
  size, or in the history screen.
- **Independent agreement on the central fact.** Bachelard et al. (2024, see Related) locate the
  cap-weighted portfolio far in the left tail of a random-portfolio return distribution and cite
  both this paper and Arnott et al. for the same finding over comparable multi-decade US samples;
  and they attribute the effect, quoting Arnott et al. verbatim and therefore **second-hand here**,
  to the fact that "value and size arise naturally in non-price-weighted strategies and constitute
  the main source of their return advantage", concluding that "a simple performance measure becomes
  an unreliable gauge of skill". The same source supplies the rejoinder that keeps this from being
  an economic claim: by Sharpe's arithmetic of active management, *that random portfolios beat the
  cap-weighted index does not imply most strategies do*, because a random portfolio samples the
  **name** space uniformly while cap weighting samples the **capital** space.
- **No inference.** The paper reports quantiles, not tests, and does not correct for anything. Read
  it for the construction and the location of the distribution, not for significance.
- **Costs.** Addressed descriptively (turnover and traded-volume exposures by decile) rather than
  charged. Treat every performance ordering in it as gross.

## Implementability here

This is the structural explanation of two things the lab has already measured, and it opens one
hypothesis the lab has never tested.

**What it explains.** (a) `experiments/learnings.md` [2026-10-07]: the random-selection null's 90%
quantile is nearly flat across a twenty-fold range of book size (`p90` +0.566 at K=10 to +0.636 at
K=200, `sd` 0.094 → 0.013), so "the gate reduces to beat pool + 1.28·sd(K) and cannot be gamed by
widening or concentrating the book". That is exactly the prediction of a null whose *centre* is the
equal-weighted pool by construction and whose *width* is the only thing cardinality moves. The lab
derived it from 600 train draws; this source derives it from ten million and from the algebra of a
multinomial weight vector. (b) The 2026-10-14/15 F8 finding that the null "collapses against a
near-full-pool equal-weight book" is the `m = n` case of the same construction — when the draw
covers the whole pool at equal weight there is nothing left for it to randomise.

**What it means for every imported result.** v3 benchmarks skill against the **equal-weight
eligible pool**, so the premium this whole literature documents — the monkey's alpha — is *inside
the lab's benchmark*, not available to its candidates. Any published result whose benchmark is a
cap-weighted index is therefore discounted here by the entire equal-weight-minus-cap-weight gap
before it is read as skill, and the folder's measurement of that gap is
`notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md`. This is the same conclusion
`#256` reaches from the cost side, by a wholly independent route: the lab's run of near-zero skill
numbers is what a correctly specified benchmark produces, not evidence that the search is broken.

**The one new hypothesis, stated with its counter-evidence attached.** The only construction here
that exceeded the whole random distribution risk-adjusted was the one that **minimised variance**,
and the risk-weighted constructions came next; note that every scheme they grade re-weights the
*same* thousand names, so the paper says nothing about selection either way — its axis is weighting
alone, which is precisely why it is informative about a null that permutes names. v3's
null copies the candidate's *weight vector* onto region-matched replacement names, so a variance
reduction achieved by **which** names are held is inside the null's reach, while one achieved by
setting weights **against the covariance structure of the names actually held** may not be — the
permuted book inherits the shape of the weight vector but not its fit to the names. If that is
right, the variance axis is the lab's least-explored lever against this specific gate. Three riders,
all of which must be in the journal before this is written: (i) the lab has one observation
pointing the other way — `rv_arbrisk_peer_neutral` ran at 0.92× the pool's volatility and still
landed at the 0th percentile; (ii) a minimum-variance construction at ~1,000 eligible names needs a
covariance estimate the folder has already shown is not available in the obvious form (see
`notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md`), so the
implementable version is the risk-parity-flavoured one (inverse volatility, equal risk
contribution) rather than the optimised one; (iii) all of these orderings are gross, and the
thinner-book consequence recorded above means the v3 per-name cost tiers and the UK/HK/FR/IT/ES
transaction taxes fall on exactly the names a non-cap weighting overweights. A low-volatility
*weighting* is also not a low-volatility *selection*: the folder already holds the lab's finding
that its range-variance lead was "equal-weight the low-beta 37% of the universe", which is the
selection version and is refuted; this is the weighting version and is a different object.

**Pitfall.** The sampler's granularity is a free parameter of the *null*, not of the candidate, and
this paper's own sensitivity check is the model for how to treat it: change it by an order of
magnitude and see whether the verdict moves. The lab cannot do that (the engine is frozen, rightly
— see the sister note on why a dial-able null is dangerous), so the honest version is to read the
gate's verdict as conditional on the engine's draw scheme and to say so.

## Related

- `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — the method whose null this
  paper's construction instantiates, and its p-value and matching rules.
- `notes/2026-10-15-random-portfolio-inference-concentration-of-measure.md` — the algebra behind
  "random weights converge on equal weights", and the argument that the resulting distribution is
  too narrow to test against.
- `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` — what the lab's benchmark
  earns against cap weighting, i.e. the premium this paper measures, decomposed into a tilt and a
  rebalancing channel (the lab has since measured the second at zero on its own panel).
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` and
  `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md` — why the
  optimised end of this paper's ladder is not reachable at this panel's width, and what is.
- `notes/2026-10-13-equal-minus-value-as-a-performance-evaluation-factor.md` — the formal version of
  "an equal-weighted reference is itself a tilt", which is why the reference-point question in the
  sister note is not pedantry.
- Unobtained pointer: Arnott, Hsu, Kalesnik & Tindall (2013), JPM, `doi:10.3905/jpm.2013.39.4.091`
  — see Access. Worth one more channel in a later session (the co-authors' institutional pages were
  not enumerated tonight).
