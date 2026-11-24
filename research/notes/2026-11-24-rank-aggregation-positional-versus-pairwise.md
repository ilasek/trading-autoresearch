---
title: "Aggregating several rankings of the same items — Kemeny optimality and why it is NP-hard, the footrule relaxation that is a bipartite matching, the theorem that no positional rule can be Condorcet, and local Kemenization as a cheap post-process that makes any aggregation prefix-stable"
authors: Dwork, Kumar, Naor, Sivakumar
year: 2001
venue: "Proceedings of the 10th International World Wide Web Conference (WWW10), 613–622. Peer-reviewed top-tier CS conference; in this folder's rubric a heavily-cited refereed CS conference paper is graded on citations + replication + methodology like any other source, not discounted for not being a finance journal."
url: https://doi.org/10.1145/371920.372165
citations: "1045 (Crossref `is-referenced-by-count`, checked 2026-11-24); 2209 (Semantic Scholar by DOI, same date). The two indexes differ by ~2x, which is the usual CS-conference indexing gap, not a disagreement about the paper."
sample_period: "n/a — the theory is distribution-free rank arithmetic. The empirical section uses top-100 result lists from seven web search engines for 38 queries, collected 2001. No market data anywhere."
markets: "None. The objects ranked are web pages. Transfer to this lab is by construction, not by evidence."
tier: "A. Peer-reviewed, very heavily cited, the canonical reference for the problem; every construction is stated as an algorithm with a complexity bound and the two hardness claims are proved in its appendix. The one gap that keeps it from being unqualified: its empirical comparison has no ground truth (see Robustness), so it ranks methods by agreement with their own inputs, and it is a single-domain study."
validation_overlap: false
published_post_2018: false
read: "Full text, the typeset WWW10 proceedings PDF (10 pp., 288 KB) from `archives.iw3c2.org/www10/cdrom/papers/pdf/p577.pdf`, HTTP 200 on the first request, `pdftotext -layout` → 81 KB of clean text, 392 instances of `\" the \"`, `( )`-dropout check zero, no ASCII shift. The appendix proofs (NP-hardness of Kemeny for k=4, the positional-rule impossibility, uniqueness of local Kemenization) were NOT read line by line; they are recorded as claims of the paper with their statements quoted."
access_note: "The IW3C2 proceedings archive (`archives.iw3c2.org/www10/cdrom/papers/pdf/p<id>.pdf`) is nominated as a channel: it serves the typeset early-WWW proceedings with no challenge, and the paper id came straight out of a web search result. The authors' own abstract page at `wisdom.weizmann.ac.il/~naor/PAPERS/` was not needed."
---

## Why this source is here

The [2026-11-23] primary aim for this session: *the literature on aggregating several rankings of
the same items into one ranking or one selected subset.* `#513` ends at "use the composite to decide
membership" and none of the three sources behind it examines the composite. The composite all of
them use — the arithmetic mean of normalised ranks — is a **positional scoring rule**, i.e. a Borda
count, and fixed-string greps over all 318 notes returned zero for `Borda` in that sense, `Kemeny`,
`Condorcet`, `Copeland` and `rank aggregation`. This paper is the canonical statement of the problem
and it meets all four admission criteria: (i) it is exactly about combining several complete or
partial rankings of the same items; (ii) it proves that **no** positional rule can satisfy the
Condorcet criterion and names the alternatives; (iii) it treats partial and top-*d* lists as the main
case rather than an afterthought; (iv) everything in it is rank arithmetic with nothing estimated.

One framing detail from the paper is worth lifting verbatim because it is this lab's exact situation
and the opposite of the voting literature's: *"in contrast to the social choice scenario where there
are many voters and relatively few candidates, in the web aggregation scenario we have many
candidates (pages) and relatively few voters (the search engines)."* The lab has ~1,000 eligible
names and two to five leads.

## Mechanism

**The problem.** Given lists τ₁…τ_k, each a ranking of some subset of a universe U, produce one full
list σ over the union that is "closest" to the inputs. "Closest" requires a distance, and the choice
of distance is the whole substance:

- **Kendall tau distance** `K(σ,τ)` — the number of pairs the two lists order oppositely (the
  bubble-sort distance). Computable in `n log n`.
- **Spearman footrule distance** `F(σ,τ) = Σ_i |σ(i) − τ(i)|` — the L1 distance between the two rank
  vectors. Computable in linear time; normalised by `|S|²/2` to land in [0,1].

Both extend to k lists by averaging. The minimiser of total Kendall distance is the **Kemeny optimal
aggregation**, "in a precise sense the geometric median of the inputs".

**Why Kemeny is the privileged target, and the price.** Three reasons are given. (1) A maximum-
likelihood reading: if there is an underlying correct order σ and each input is σ with pairs swapped
with probability below ½, a Kemeny optimal aggregation is one maximally likely to have produced the
observed lists — so Kemeny aggregation "has the property of eliminating noise from various different
ranking schemes". (2) Kemeny optimal aggregations are "essentially the only ones" that simultaneously
satisfy neutrality, consistency and the Condorcet property (the authors attribute this to Young and
Levenglick 1978 — see the companion note). (3) They satisfy the extended Condorcet criterion. The
price: **computing a Kemeny optimal aggregation is NP-hard, and remains NP-hard with only k = 4
input lists** (proved in the appendix). With two or three leads the lab is formally below that
threshold; at four it is not.

**The impossibility that answers criterion (ii) directly.** Borda's method is *positional*: it
assigns a score from the position a candidate occupies in each list and sorts by the total. The
paper's statement is unusually strong — it is not that Borda in particular fails, it is that the
whole class does: *"they cannot satisfy the Condorcet criterion. In fact, it is possible to show that
no method that assigns a weight to each position and then sorts the results by applying a function
to the weights associated with each candidate satisfies the Condorcet criterion."* So mean-of-ranks,
sum-of-z-scores, any monotone reweighting of positions, and any convex transform applied to the
per-list positions are all in the same class and all fail it. What they buy in exchange: linear
time, and anonymity, neutrality and consistency.

**The positional family is wider than the mean.** Borda is "sorting the candidates by the L1 norm of
the k-element position vector", and the paper notes the obvious siblings: sort by L_p for p > 1, by
the **median** of the k positions, or by their **geometric mean**. The median is not an arbitrary
variant — see the footrule proposition below.

**Footrule as the tractable relaxation.** Footrule-optimal aggregation approximates Kemeny-optimal
(elsewhere in this literature: footrule bounds Kendall within a factor of 2, so the footrule optimum
is a 2-approximation to the Kemeny optimum). Two propositions make it operational:

- *Proposition 3.* Given full lists, **if the median positions of the candidates form a permutation,
  that permutation is a footrule-optimal aggregation.** Sorting by median rank is therefore the
  footrule optimum whenever it happens to be tie-free — a one-line change from sorting by mean rank.
- *Proposition 4.* Footrule-optimal aggregation of full lists is computable in polynomial time as a
  **minimum-cost perfect matching** in the bipartite graph of candidates × positions with weight
  `W(c,p) = Σ_i |τ_i(c) − p|`.

**Partial lists break the tractability and the fix is the scaled footrule.** Footrule-optimal
aggregation of *partial* lists is NP-hard — "equivalent to the NP-hard problem of computing the
minimum number of edges to delete to convert a directed graph into a DAG" (minimum feedback arc
set). The replacement keeps the matching formulation and changes the weight to the **scaled footrule
distance**, `W(c,p) = Σ_i |τ_i(c)/|τ_i| − p/n|`, where each list's ranks are divided by that list's
own length. This is **scaled footrule aggregation (SFO)**. The paper also warns off the obvious
alternative: the suggestion that Borda be extended to partial lists by apportioning the excess score
equally among unranked candidates is rejected, and generally — *"for any method of assigning scores
to unranked candidates, there are partial information cases in which undesirable outcomes occur."*

**The extended Condorcet criterion (ECC), and what it is for.** Condorcet's own criterion: an
alternative that beats every other in pairwise simple-majority voting should be ranked first.
Truchon's extension, adopted here: if there is a partition (C, C̄) of the items such that for every
x ∈ C and y ∈ C̄ a majority of the lists prefers x to y, then every x must be ranked above every y.
Kemeny-optimal aggregations satisfy it; so do *locally* Kemeny-optimal ones; the Markov-chain methods
below need not. The paper's use for it is spam resistance, and the argument transfers cleanly: an
item boosted by **fewer than half** the voters is a Condorcet loser and the ECC pushes it into the
bottom partition, whatever its position in the one list that loves it. The honest limit is stated
too: *"the extended Condorcet criterion gives no guidance within a partition"*, and if a majority of
the voters are fooled, no aggregation can help — "garbage in, garbage out".

**Local Kemenization — the cheap operator, and the one with the property this lab wants.** A full
list σ is *locally Kemeny optimal* for τ₁…τ_k if no single transposition of an **adjacent** pair
reduces the total Kendall distance. Every Kemeny optimal aggregation is locally Kemeny optimal; the
converse is false; but local Kemeny optimality already implies the ECC and is computable in
**O(k n log n)**. The paper's headline recipe is therefore a post-process on anything:

> Given τ₁…τ_k, use your favorite aggregation method to obtain a full list μ. Output the (unique)
> local Kemenization of μ with respect to τ₁…τ_k.

and it comes with three stated properties: (1) Condorcet losers get low rank and Condorcet winners
high rank; (2) the output disagrees with the initial aggregation μ on a pair (i,j) **only if a
majority of the lists expressing an opinion on (i,j) disagrees with μ**; (3) **for every d, the
length-d prefix of the output is a local Kemenization of the top d of μ** — i.e. the operator is
prefix-consistent, which is the top-K property the [2026-11-23] entry asked a source to have.

**Markov-chain methods (MC1–MC4).** A general way to aggregate partial lists: build a chain whose
states are the candidates, with transitions derived from the available pairwise information, and
order by the stationary distribution. The motivation is that connectivity lets unobserved pairs be
compared transitively, and that it weights a win by the strength of the opposition ("more wins
against good players is even better" — explicitly the HITS/PageRank intuition). Three of the four are
generalisations of positional rules, which is the useful taxonomy: **MC2** generalises sorting by the
geometric mean of ranks, **MC3** generalises Borda (one step from a uniform start orders items by
Borda score), and **MC4** generalises **Copeland's rule** — sort by the number of pairwise majority
contests won. MC4's transition: from P, pick Q uniformly from the union of ranked items and move to Q
if a majority of the lists that ranked both prefers Q.

## Construction recipe

Everything below is rank arithmetic; nothing is estimated and nothing is fitted.

1. **Inputs.** For each lead ℓ and each rebalance date t, a ranking `τ_ℓ,t` of the names that lead
   scores — complete over the eligible set if the lead scores everything, a **top-d list** if the
   lead only ranks its own selection (the latter is the lab's actual case whenever a lead is defined
   as a filter).
2. **Baseline (what the lab already does).** Borda: `B(c) = Σ_ℓ (number of names ranked below c in
   τ_ℓ)`, sort descending. Equivalent to sorting by the mean of normalised ranks. Linear time.
3. **Free sibling.** Sort by the **median** rank instead of the mean (Proposition 3: the footrule
   optimum when the medians are a permutation), and by the geometric mean of ranks as the third
   member of the family. One line each.
4. **Copeland / MC4.** Build the pairwise majority matrix `M[i,j] = 1` iff a majority of the leads
   that rank both i and j put i ahead. Copeland score = row sum of M. For k complete rankings over
   the same n names this is `k` outer comparisons of a rank vector — `O(k n²)` and vectorisable.
5. **Scaled footrule (SFO) when the lists are partial.** Min-cost maximum matching on candidates ×
   positions with `W(c,p) = Σ_ℓ |τ_ℓ(c)/|τ_ℓ| − p/n|`. `scipy.optimize.linear_sum_assignment` is
   exactly this solver; at n ≈ 1,000 the cost matrix is 10⁶ entries, which is affordable once per
   rebalance date but not once per name.
6. **Local Kemenization, applied to whichever of 2–5 produced the initial list μ.** Inductive
   insertion: having Kemenized the top ℓ−1, insert item ℓ at the **lowest** permissible position —
   just below the lowest-ranked y such that no majority of the τ's prefers ℓ to y and, for every
   successor z of y, a majority prefers ℓ to z. In words: try to insert at the bottom and bubble up
   while a majority insists. `O(k n log n)`; the result is unique.
7. **The practical truncation, from the paper itself.** Project the τ's onto the **top d of μ** and
   Kemenize only that: "if μ is an initial meta-search result, and we have some faith that the top,
   say, 100 elements of μ contain enough good pages, then we can build a locally Kemeny optimal
   aggregation of the projections of the τ's onto the top 100 elements in μ." For the lab, d is the
   book's selection breadth plus a margin.
8. **Membership.** Take the top K of the final list and equal-weight (or deconcentrate per `#513`).
   The aggregation touches membership only; no weight is a function of any score.

## Robustness evidence (qualitative only)

**The replication status of the ideas, not of a number.** Kemeny's rule, Borda's rule, Copeland's
rule and the Condorcet criterion are two-centuries-old objects with an independent axiomatic
literature (see the companion note on Young 1988), so the *mechanisms* here are not one paper's
claims. What is this paper's own is the complexity map (Kemeny NP-hard at k = 4; footrule-optimal
polynomial for full lists and NP-hard for partial; local Kemenization O(k n log n) and unique) and
the local-Kemenization operator.

**The empirical comparison, and the reason to read it narrowly.** On seven search engines' top-100
lists over 38 queries, measured by Kendall, induced-footrule and scaled-footrule distance from the
aggregate to the inputs: MC4 was best on all three, SFO and MC3 were on a par with each other,
MC1/MC2 were the weakest chains but still ahead of Borda, and Borda was the worst of everything
tried — the authors call it "very interesting since Borda's method is the usual choice of
aggregation, and perhaps the most natural". Local Kemenization improved every method slightly
(1–3% on the distance measures) and it is proved never to worsen Kendall distance.

**The gap that matters, and it is not a small one.** Those numbers measure **agreement with the
inputs**, not correctness: the paper says so plainly — there is no ground truth for web relevance,
which is the stated reason it uses inter-list distances at all. So the finding "MC4 beats Borda" is
*"MC4 lands closer to the consensus of the voters than Borda does"*, which is a statement about the
aggregation operator's fidelity, **not** evidence that a Copeland-type book would out-predict a
mean-of-ranks book. Nothing in this paper licenses a performance expectation, and under this
folder's anti-lookahead policy none is recorded.

**Overlap on item sets is thin and that is the realistic case.** Across seven engines' top 100s, the
average number of pages present in all seven was under 2, while ~285 appeared in exactly one. The
methods are designed for, and tested on, inputs that mostly disagree about *membership* rather than
about order — which is the regime the lab is in when two leads select different names.

## Implementability here

**Fits the constraints with no new data.** This is arithmetic on ranks the lab already computes.
Nothing is estimated, so the `#1` triage screen (count the noisily-estimated parameters) scores it at
zero, the same as equal weighting. It is a *selection* operator, so it composes with `#513`'s
filter-then-deconcentrate and with the engine's 25% cap, and it never puts a score into a weight.

**Runtime.** The protocol calls `generate_weights` about seven times a trial and wants a call under
~60 s on the ~1,000-name panel. Per rebalance date: Borda is trivial; the pairwise majority matrix is
`k` vectorised outer comparisons on a 1,000-vector (about 10⁶ booleans per lead); SFO is one
`linear_sum_assignment` on a 10⁶-entry matrix. Monthly rebalances over train+validation are ~300
dates, so budget by measuring one date and multiplying — and prefer the paper's own truncation
(aggregate fully, Kemenize the top few hundred) to keep the Python insertion loop off the full
panel. A daily-rebalanced version of any of this is not affordable and is not wanted anyway
(`#512`).

**What to build first, and it is not Kemeny.** The cheapest informative change to the lab's current
composite is the **local Kemenization post-process** on the existing mean-of-ranks ordering, because
(a) it is `O(k n log n)`, (b) it only ever reverses a pair when a majority of the leads disagrees
with the composite on that pair, so it is a conservative edit of a construction the lab already
trusts, and (c) its prefix property means the top-K it yields is the top-K of a locally-Kemeny list,
not an artefact of where the cut landed. The second cheapest is sorting by **median** rather than
mean rank. Full Kemeny optimisation is NP-hard and is not worth a trial.

**The free pre-trial measurement this source implies.** Before building anything, compute at a
handful of rebalance dates: the Borda top-K, the Copeland (MC4) top-K and the locally-Kemenized
Borda top-K, and report (a) how many names the three sets share and (b) whether any **ECC partition**
exists at the cut — i.e. whether there is a set C of names each of which a majority of leads prefers
to every name outside C. If the three sets agree on nearly every name, the aggregation rule is not a
live design axis for this lab and the question is closed for free; if a majority-partition exists and
the Borda top-K violates it, that is the exact failure the ECC describes and the size of the
violation is the expected size of the effect.

**The discount that has to be applied, and it is the biggest caveat in this note.** Every
majority-based rule treats the k lists as k judges. The lab's leads are not independent judges:
`learnings.md` records an inter-signal ensemble killed for free because the candidate scores
rank-correlated at **0.89**, and two legs of a measured blend rank-correlating at 0.66. A pairwise
"majority of leads" over three near-duplicate leads is one opinion counted three times, and Copeland
or Kemeny over such a set inherits that lead's ordering while *looking* like a consensus. So: run the
aggregation literature's rules only over leads that the lab's own decorrelation screen has already
separated (and prefer the top-K agreement measure in the Fagin note to a full-ranking correlation for
that screen), and treat "a majority of leads prefers i to j" as meaningless when k = 2.

**Pitfalls.**
- With **k = 2** leads there is no majority; pairwise rules degenerate and the ECC is vacuous except
  where the two agree. Most of this machinery only starts paying at k ≥ 3 genuinely distinct leads.
- The ECC says nothing about order *within* a partition, and the Markov-chain methods do not even
  guarantee it. Satisfying the ECC is a floor, not a ranking.
- The paper's distance measures for partial lists "are not necessarily metrics" — do not use them as
  if they were (and see the Fagin note, which is about exactly this).
- `eligible` changes the item set between dates. A positional composite's ordering of retained names
  can move because of entries and exits alone; that is the local-stability problem and it belongs to
  the Young note.

## Related

- `notes/2026-11-24-when-a-positional-rule-is-the-right-aggregator.md` — Young (1988): the MLE and
  axiomatic answer to *when* Borda is right and when it is not, and the local-stability property that
  Borda lacks. Read the two together; this paper's claim that Kemeny is "essentially the only" rule
  with the good properties is a citation to that literature.
- `notes/2026-11-24-top-k-distance-measures-and-the-equivalence-class.md` — Fagin, Kumar &
  Sivakumar (2003): how to *measure* agreement between two top-K lists properly, by the same IBM
  Almaden group, and the source for the claim that top-K agreement is not the same measurement as
  full-ranking correlation.
- `#513` (`notes/2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md`) — the
  construction this note supplies the missing half of: the composite decides membership, and this is
  the literature on what the composite should be.
- `#514`, `#515` — the two free holdings/score screens from the same vein; the measurement proposed
  above sits beside them and uses the same stored lead scores.
- `experiments/learnings.md` — the 0.89 rank-correlation screen that killed an inter-signal ensemble,
  which is the binding constraint on every majority-based rule here.
