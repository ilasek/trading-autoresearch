---
title: "Industry Information Diffusion and the Lead-lag Effect in Stock Returns"
authors: Hou
year: 2007
venue: Review of Financial Studies (Tier 1 peer-reviewed)
url: https://doi.org/10.1093/revfin/hhm003
citations: 617 (OpenAlex, DOI:10.1093/revfin/hhm003, checked 2026-08-31; Semantic Scholar's DOI endpoint did not resolve this DOI)
sample_period: not established from the sources obtained — the published abstract states no sample window, and the full text was not reached
markets: US equities (CRSP-style cross-section, big-firm/small-firm portfolios within industries)
tier: A
validation_overlap: false
published_post_2018: false
---

**Recorded from the published abstract only.** `oa_status: closed` (OpenAlex, checked
2026-08-31); no repository holds a full text, SSRN serves a Cloudflare bot challenge on both
posted abstract pages, and neither CORE nor CiteSeerX resolved a mirror. The abstract was read
verbatim from the RePEc/IDEAS record for RFS 20(4), 1113–1138. Every claim below that is
attributed to Hou comes from those six sentences; **no construction detail, no lookback, and no
robustness evidence beyond the abstract's own wording is available**, and the *Construction
recipe* section is explicitly marked as reconstruction rather than as the paper's recipe.

`validation_overlap` is set false on the strength of the publication year — a 2007 RFS article
cannot have a sample touching 2018–2023 — not because a sample window was verified.

This is the follow-up `SUMMARY.md` flagged on 2026-08-30 as the session's highest-value unread
item, on the grounds that if its claim is right then **the grouping variable matters more than
the lead-lag machinery**, and this repo's grouping choice is exactly the live design decision.
The abstract confirms the claim. It also, read carefully, tells the lab that the grouping the
claim endorses is one this repo cannot currently build.

## Mechanism

The lead-lag effect — big firms' returns predicting small firms' returns — had been explained
by several competing stories: differential speed of adjustment to *market-wide* news, thin
trading, size-related frictions generally. Hou's argument is that the effect is not about size
per se and not about market-wide information. It is about **industry** information diffusing
slowly *within* an industry.

The four claims in the abstract, in the abstract's own terms:

1. **The lead-lag effect between big and small firms is predominantly an *intra*-industry
   phenomenon.** Big firms lead small firms in the same industry. This is the load-bearing
   claim: it says the cross-sectional predictability that a naive big→small construction picks
   up is mostly a within-industry channel wearing a size label.
2. **It is driven by sluggish adjustment to *negative* information.** The effect is asymmetric
   in the sign of news. A construction that treats up-moves and down-moves symmetrically is
   averaging a live channel with a dead one.
3. **It is robust to alternative determinants of the lead-lag effect** — i.e. the industry
   channel survives controls for the rival explanations, rather than being a restatement of
   them.
4. **Cross-sectionally, the effect is stronger in small, less competitive, and neglected
   industries** — the standard limited-attention/slow-diffusion signature. Fewer eyes on an
   industry, slower the common information propagates from the followed names to the ignored
   ones.

The abstract also links the effect to **post-earnings-announcement drift**: small firms drift
following the earnings releases of big firms *within their industry*. That is the microfoundation
— the information event is a big firm's earnings, its industry-relevant content is not fully
impounded into industry peers, and the peers drift.

The economic story is limited attention plus costly information processing: investors track
industry leaders, and the industry-common component of a leader's news reaches the followers
with a lag proportional to how little attention the industry attracts.

## Construction recipe

**Reconstruction, not the paper's recipe** — the full text was not obtained, so lookbacks,
portfolio-formation cadence, industry classification granularity and control specifications are
all unknown. What the abstract determines is the *shape* a faithful construction must have:

- Partition the universe into **industries**, then within each industry into leaders and
  followers by size. The predictive regression is follower return on lagged leader return
  **within the same industry**, not pooled across the market.
- **Control for the cross-industry channel**, since the claim is comparative: the intra-industry
  term should survive the inclusion of a cross-industry or market-wide lagged term, and the
  latter should weaken. Without both terms in the same specification the claim is untested.
- **Condition on the sign of the leader's move.** The predictable component is concentrated in
  negative leader returns.
- **Condition on industry characteristics** — size, concentration/competitiveness, and
  analyst/press coverage ("neglect"). The effect is expected in the small, concentrated,
  neglected industries and to be weak elsewhere.
- The horizon is whatever horizon industry news takes to diffuse — the PEAD link points at
  weeks-to-a-month rather than days, but the abstract does not name one and this note will not
  invent one.

## Robustness evidence (qualitative only)

Not assessable beyond the abstract. What can be said: the paper is in a Tier 1 journal, is
heavily cited for its age (617 by 2026), and the abstract asserts robustness to alternative
determinants of the lead-lag effect. The mechanism is the same limited-attention family as
Hong–Torous–Valkanov, already in this folder, and the two are mutually reinforcing rather than
independent — a shared prior, not two draws.

**No replication status established.** Tier A is assigned on venue and citation weight; on
methodology-honesty and sample-robustness evidence this note is empty, and the strategy agent
should treat its claims as strong-prior rather than verified. The folder's precedent for
abstract-only sources (Heston–Sadka 2010, Brown–Goetzmann–Ross 1995, Tse 2015) applies.

## Implementability here

The claim is directly relevant and the recipe is directly out of reach, and it is worth being
precise about why.

**What Hou says the grouping variable should be:** industry. **What this repo has:** 15 regions
and a stock/ETF split (`program.md`), with no fundamentals and therefore no sector or industry
classification. The lab's `lead-lag-spillover` scouts to date have grouped by region.

So the honest reading of this note is a **discount on the lab's existing lead-lag results
rather than a new build**. Hou's finding is that big→small predictability pooled across a
market is largely an artefact of an unmodelled industry channel; the lab's region→region and
group→market constructions are the same manoeuvre with a geographic partition substituted for
the industry one, and there is no evidence in this note that a geographic partition proxies for
the industry one. If anything the reverse: Hou's cross-sectional result attaches the effect to
*industry* attributes (competitiveness, neglect) that have no regional analogue.

Three things the lab can actually do:

- **Check whether the 42 ETFs include sector or industry funds.** If they do, they are the
  closest thing to an industry taxonomy this universe contains, and a sector-ETF-defined
  grouping is buildable from prices alone. If they are all region/broad-market funds, the
  honest conclusion is that **Hou's construction cannot be built here**, and that should be
  recorded as a family-scoping fact rather than worked around by analogy. This is a free check
  on the instrument list; it costs no trial and it decides whether anything below is reachable.
- **Add the sign asymmetry to any lead-lag candidate, since it is free.** Conditioning the
  leader's signal on negative moves is a one-line change to an existing construction and Hou's
  abstract puts the effect there. It also interacts usefully with `SUMMARY.md` #52's screen
  (iii): a mechanism that is real should show the asymmetry, and one that is momentum in costume
  should not care about the sign of the leader's move.
- **Treat "grouping choice" as the thing being tested, not a nuisance parameter.** If the lab
  runs a lead-lag candidate on regions and it fails, Hou says that is evidence about *regions as
  a diffusion channel*, not about lead-lag. Those are different findings and the journal entry
  should say which one it is claiming.

Pitfalls:

- **The universe is far too coarse for the cross-sectional half.** "Small, less competitive,
  neglected industries" is where the effect lives; ~145 large, globally-known instruments is
  the neglect-free end of every one of those sorts. Even with a sector grouping, this universe
  samples the region of the cross-section where Hou's effect is weakest.
- **Breadth.** Partitioning ~103 single names into industries leaves a handful of names per
  industry and a leader/follower split inside that. The lab already measured a lead-lag
  construction computable for a mean of only 57 names per date and found it thin; an industry
  partition is thinner still.
- **The PEAD microfoundation is unreachable.** No earnings dates, no fundamentals. The lab can
  build the return-based shadow of the mechanism but cannot condition on the event that drives
  it, which removes the paper's sharpest identification.
- **Do not import the size framing.** The abstract's whole point is that the big→small framing
  is the wrong axis. A candidate that sorts by market cap proxy and calls it lead-lag is
  building the construction Hou argues against.

## Related

- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` — Hong–Torous–Valkanov, the
  group→market version of the same diffusion mechanism. That note flagged this paper as the
  follow-up; this is the follow-up, and it sharpens that note's grouping question from "which
  grouping" to "the grouping is the hypothesis".
- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — Chordia–Swaminathan, the
  speed-of-adjustment reading at the daily/weekly end.
- `notes/2026-08-28-international-momentum-country-neutral.md` — the folder's other result
  about grouping variables, and the only grouping to have passed the lab's neutralisation
  screen. Worth reading against this one: that note validates a *regional* grouping for a
  momentum construction, which is not the same as validating it as a *diffusion channel*.
- **Standing gap this note does not close.** `SUMMARY.md`'s 2026-08-30 open question named
  **ETF-versus-constituent** lead-lag as the one sub-mechanism `program.md` calls for and no
  source in this folder addresses. Hou is group→group within industries; that gap remains open
  after this session.
