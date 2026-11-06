---
title: "S&P 500 Index Additions and Earnings Expectations"
authors: Denis, McConnell, Ovtchinnikov, Yu
year: 2003
venue: Journal of Finance 58(5), 1821–1840 (venue tier 1)
url: https://doi.org/10.1111/1540-6261.00589
citations: 295 (Crossref `is-referenced-by-count`, checked 2026-11-06)
sample_period: 1987–1999 (S&P 500 additions)
markets: US equities — S&P 500 index additions, with I/B/E/S analyst forecast coverage
tier: A — tier-1 venue, three-figure citations, full text read from the version of record, and the design is a test of somebody else's *premise* rather than a hunt for a new effect
validation_overlap: false (sample ends 1999)
published_post_2018: false
read: full text, typeset JF version of record (21-page JSTOR scan with a text layer → 69 KB of clean text, 464 instances of `" the "`, zero `( )` dropout, title and page headers verified)
---

## Access

Read from **`typeset.io/pdf/<title-slug>-<id>.pdf`**, which served the typeset JSTOR version of
record — journal name, volume, issue and page headers intact — on the first try. Worth recording as
a channel: it is an aggregator rather than an author or institutional host, and this folder had not
used it. The obvious institutional alternative, the authors' own `docs.lib.purdue.edu` bepress
repository, returned **HTTP 403 with a 5.6 KB Cloudflare body**, exactly as `research/README.md`'s
2026-10-01 bepress entry predicts. One caution for reuse: the `typeset.io` path carries an opaque
id that cannot be derived from the title, so it has to come out of a search result.

**DOI.** A DOI guessed from the JF 2003 pattern resolved to a different article in the same issue.
The correct one came from **enumerating the journal-year** —
`api.crossref.org/journals/0022-1082/works?filter=from-pub-date:2003-01-01,until-pub-date:2003-12-31&query.bibliographic=<words>`
— which returned DOI, volume, pages and citation count in one call. Third confirmation of the
2026-10-07 lesson that *a journal's year is a better key than an article's title*, now on a Wiley
DOI rather than an Elsevier one.

## Mechanism

This folder has several notes on what happens to a stock's **price** when it joins an index. This
note is about something else: **what joining an index says about the stock**, and therefore what a
panel built from index membership is selected on.

The paper exists to test a premise, and the premise is the interesting object. Two decades of
index-effect studies rested on the claim that index inclusion is an **"information-free event"** —
that it conveys nothing about a company's prospects, which is what licenses reading the price jump
as evidence about demand curves. The premise has an apparently solid foundation: the index provider
says so itself. The authors quote S&P directly: "Company additions to and deletions from an S&P
equity index do not in any way reflect an opinion on the investment merits of the company."

The authors' insight is that the disclaimer answers the wrong question. The disclaimer is about the
direction **information → inclusion**: S&P is saying it does not use private information to pick
members. But the premise that index-effect studies need is about the direction **inclusion →
information**, and nothing in the disclaimer speaks to it. If membership *itself* changes a firm's
prospects — through greater investor scrutiny and monitoring, or through a larger reputational cost
to a manager who lets an index member flounder — then the inclusion announcement is informative
even though the provider revealed nothing.

The test: track analysts' earnings forecasts and subsequently realised earnings for added firms
against matched non-added firms. The finding: added firms experience significant increases in
earnings-per-share forecasts and significant improvements in realised earnings relative to
benchmarks. **Index inclusion is not an information-free event.**

For this lab the load-bearing consequence is not the causal story. It is the structural one:
**membership status is correlated with subsequent fundamental improvement**, whichever way the
causality runs. A point-in-time index-membership panel therefore admits a name at a moment that is
systematically followed by improving fundamentals, and drops it at a moment that is not. That is a
selection on something close to the dependent variable, applied name by name, at entry.

## Construction recipe

There is no strategy here. What this note supplies is the **anatomy of the selection rule**, which
is what tonight's aim asked for.

- **The index provider's stated selection criteria, named in the paper and sourced to S&P's own
  methodology documents, are three**: *industry group classification*, *market value*, and *trading
  activity*. That is the rule — a sector-representativeness criterion, a size criterion and a
  liquidity criterion. It is a committee applying stated criteria, not a mechanical percentile cut.
- **The matched-benchmark construction, which is the reusable recipe and is built to mimic the rule
  exactly**:
  - Sort every candidate firm into one of the **12 Fama–French industry portfolios**.
  - Split each industry into **3 market-capitalisation groups**, one third of firms each.
  - Within each industry × size cell, split into **3 liquidity groups**, where liquidity is the
    **five-year average of annual trading volume divided by shares outstanding** (i.e. average
    annual turnover, not a dollar-volume or price-impact measure).
  - This yields **108 portfolios** (12 × 3 × 3). Each added stock is matched to its own cell.
  - The authors call this the **industry, size and liquidity (ISL) matched** benchmark, and run it
    alongside a cruder "all other companies" benchmark.
- **Sample hygiene worth copying**, because it is a catalogue of the ways an index-membership series
  contains non-events. From the raw addition list the authors remove additions arising from
  **spinoffs** from an already-included parent (39 cases), from **mergers** where the acquirer
  replaces an included target (35 cases), and from **name changes** (3 cases), leaving 236 genuine
  additions. A membership file read naively treats all of these as new members.
- **Attrition is then severe and is reported**: of 236 additions, 205 survive to the current-year
  forecast test and only 139 to the one-year-ahead test, because I/B/E/S coverage is incomplete.

## Robustness evidence (qualitative only)

- **The central result survives matching on the entire stated selection rule.** This is the point
  that makes the paper admissible under tonight's criterion and it deserves stating precisely: the
  ISL benchmark matches added firms on industry, on size and on turnover — *all three* of the
  criteria S&P says it uses — and added firms still show relatively improving forecasts and
  realised earnings. **The rule's observable screens do not exhaust what membership selects for.**
  Matching on size and liquidity is therefore not sufficient to construct a control group for an
  index-membership panel.
- Robustness includes re-running the matching with alternative size partitions and alternative
  matching schemes (firm-level rather than portfolio-level matching); the authors report these as
  leaving the conclusion intact.
- **Single market, single index, thirteen years.** This is a US S&P 500 study. The paper itself
  raises no evidence about the other eight national indices in this repo's panel, and the committee
  structure, disclaimer and stated criteria of those providers are not interchangeable with S&P's.
  The multi-market rubric row is **open** for this source.
- **Replication status.** No independent large-scale replication of this specific result was found.
  The surrounding literature on whether the index effect is permanent and why has been heavily
  worked since, and this folder already holds that strand
  (`2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md`), which bears on the
  *price* premise rather than the *information* premise and does not re-test this paper's finding.
- **Methodology honesty**: the authors state their sample attrition at every test, report both
  benchmarks rather than the more favourable one, and frame the result as refuting a premise rather
  than as establishing a mechanism — they explicitly offer two causal stories and do not claim to
  distinguish them.

## Implementability here

**Protocol v3, v2 panel.** Nothing here is a candidate. It is a statement about the panel every
candidate is measured on, and about the benchmark every v3 skill number is measured against.

1. **This repo's panel is built from exactly the object this paper studies.** The v2 universe is the
   ever-members of nine tracked indices, point-in-time: "a name is buyable only on dates it was an
   index member". So the panel's admission rule *is* an index inclusion rule — nine of them — and
   this paper says such a rule is not informationally neutral about its members' prospects.
2. **The specific bias has a direction, and it is the uncomfortable one.** A name enters `prices`
   at the moment a committee judged it to have become one of its market's leading companies, and
   that moment is followed by relative fundamental improvement. A name leaves when the converse
   happens. So the panel, at every date, over-represents firms on a recently-improving trajectory.
   The standing phrase this folder has leaned on — "this panel is large-cap and liquid by
   construction" — is **incomplete**: it is large-cap, liquid, *and selected at a favourable moment
   in each member's own history*.
3. **The consequence for protocol v3's benchmark is direct and is the most consequential item here.**
   Under v3, skill is Sharpe minus the **equal-weight eligible pool's** Sharpe. The eligible pool is
   the set of current index members. This paper implies that pool is not a neutral basket of large
   liquid stocks but a basket assembled by a selection rule that favours improving firms —
   equal-weighted, which raises the weight on the smaller and more recently-added members, i.e. on
   exactly the names whose addition was most recent. That makes the v3 benchmark a **harder and
   more structured opponent** than "the market", and it is a second, independent reason for the
   observation already recorded as `#393`: a candidate drawn from this panel is highly correlated
   with the pool because both are products of the same selection.
4. **It also sharpens a known caveat about the pre-2009 era, in the direction of more caution.**
   `research/README.md` already warns that index-member coverage is far thinner before 2009, so
   train numbers stay optimistic. This paper adds *why* that thinness is not merely noisy: a sparse
   early panel is a panel of names selected by this rule and nothing else, with no surrounding
   cross-section to dilute it. The S&P 500 is the only one of the nine tracked from 1996, so the
   whole 1997–2008 train sub-period reported by a v3 trial runs on a single committee's selection.
5. **The spinoff/merger/name-change taxonomy is a free audit this lab could use and has not.** The
   paper's three categories of pseudo-addition are generic to membership files, not specific to
   S&P. A `prices` column that appears because its name was spun off from an existing member, or
   because an acquirer replaced its target in the index, is a new *column* without being a new
   *company*. The membership files are off-limits to a strategy session by protocol, so this is not
   a candidate screen — it is a question for a human about how the panel was built, and it belongs
   on the standing list rather than in a trial.
6. **What is not implementable.** The paper's instrument is analyst earnings forecasts. This repo
   has no fundamentals and no analyst data and cannot fetch any, so the finding can be *reasoned
   with* but not *measured* here. Any candidate that tries to proxy "recently added to the index"
   from the panel would be reading membership structure, which protocol v2 refuses outright. Do not
   write one.

**Known pitfalls.** (a) Do not convert this into a hypothesis that index members outperform; the
paper compares added firms to matched non-added firms on *earnings*, says nothing about a tradeable
return effect, and the price side of the question is a different literature this folder already
holds. (b) Do not treat S&P's criteria as the other eight providers' criteria — DAX, CAC 40, FTSE
100, SMI, AEX, Euro Stoxx 50, Nikkei 225 and Hang Seng have their own rules, several are
free-float-weighted with explicit turnover thresholds, and at least one is famously
non-capitalisation-weighted; this folder has **no** source on any of them and should not assume the
US rule generalises. (c) The disclaimer-versus-premise distinction is the transferable reasoning,
not the earnings result: **an institution's statement that it uses no private information does not
make its selection uninformative.**

## Related

- `2026-11-06-investability-frictions-and-the-microcap-screen.md` — the size half of the same
  question: what a capitalisation screen does to a measured effect. This note is the half that
  survives after size and liquidity have been matched away.
- `2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` and
  `2026-10-09-index-premium-and-the-index-turnover-cost.md` — the price side of index membership,
  which tonight's aim explicitly excluded as already covered; this note is admissible precisely
  because it is about the selection rather than the price response.
- `2026-10-08-benchmark-portfolios-have-alpha-of-their-own.md` — Cremers–Petajisto–Zitzewitz. Read
  together with point 3 above: that note says a standard index carries factor-model alpha of its
  own, and this one says the membership rule generating it is not neutral. Both land on the v3
  benchmark.
- `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — the exit side of panel
  membership, where this note is about the entry side.
- `2026-08-28-local-versus-global-factor-construction.md` — Fama–French (2012), whose international
  portfolios are built from "big" stocks on a percentile rule rather than an index rule; the
  contrast with a committee rule is the gap this note fills.
