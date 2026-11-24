---
title: "When a positional scoring rule IS the right aggregator — Borda as the maximum-likelihood pick when the judges are individually weak, Kemeny as the maximum-likelihood RANKING for any judge quality, the maximin rule when judges are strong, and the local-stability property that only the pairwise rule has"
authors: Young
year: 1988
venue: "American Political Science Review 82(4), 1231–1244. Peer-reviewed flagship journal of its field (tier 1 within political science/social choice); the result it reports and extends, Young & Levenglick (1978), is in SIAM Journal on Applied Mathematics."
url: https://doi.org/10.2307/1961757
citations: "473 (Crossref `is-referenced-by-count`, checked 2026-11-24); 859 (Semantic Scholar by DOI, same date). The companion characterization paper, Young & Levenglick (1978), `10.1137/0135023`: 316 (Crossref) / 568 (Semantic Scholar), same date."
sample_period: "n/a — a probability model and an axiomatic theorem. The worked examples are arithmetic illustrations with invented voting matrices, not data."
markets: "None. The judges are voters and the items are candidates; transfer to this lab is by construction."
tier: "A. Peer-reviewed, heavily cited, and the content is theorems plus a fully worked derivation rather than an empirical finding, so there is no sample to be fragile. Two honest limits: the probability model's assumptions (identical judge competence, independence across pairs AND across judges) are strong and the author flags the last of them himself, and the uniqueness theorem is Young & Levenglick (1978), which was NOT obtained in full and is recorded here second-hand through this paper's own statement of it."
validation_overlap: false
published_post_2018: false
read: "Full text, 14 pp., 432 KB PDF via `typeset.io/pdf/condorcet-s-theory-of-voting-1r508yu416.pdf`, HTTP 200 first request, `pdftotext -layout` → 62 KB of text, 338 instances of `\" the \"`, `( )`-dropout check zero, no ASCII shift, title line verified. The extraction mangles subscripts and exponents in the displayed likelihood expressions (`p25(1-p)16` reads as `pZ5(1- p)\"`), so every algebraic claim below was taken from the running prose, which restates each one in words, and the specific numbers quoted (the 117/105/78 Borda scores of the six-alternative example) come from prose sentences, not from the exponent strings."
access_note: "`pubs.aeaweb.org` and `www.aeaweb.org` both answered the PDF endpoint for the author's related *Journal of Economic Perspectives* survey (`10.1257/jep.9.1.51`) with **HTTP 403 and a 5.5 KB Cloudflare body** — the standard refusal mode this folder records, now also observed on the AEA's own open-access journal. `resolve.cambridge.org` holds the APSR record without the text. The `typeset.io/pdf/<slug>.pdf` form served the complete typeset article and is nominated as a channel for closed society-journal articles, with the caveat that it is an aggregator and its copy should be checked for the title line and a plausible character count (both done)."
---

## Why this source is here

The [2026-11-23] aim's criterion (ii) was that a source must say **when a positional scoring rule is
and is not the right aggregator**, and name a concrete alternative with the property that
distinguishes them. The Dwork et al. companion note answers the "is not" half as an impossibility
(no positional rule can be Condorcet). This paper answers the question the lab actually faces, which
is the other half: *under what conditions is the mean-of-ranks composite the right thing to use, and
what exactly do you lose by keeping it?* It is the sharpest answer available because it is derived,
not asserted: Young reconstructs Condorcet's 1785 probability model, states it as a maximum-
likelihood problem, and solves it in three regimes.

It also supplies the one property the lab's situation makes unavoidable — the eligible item set
changes between rebalances — and the only rule class that has it.

## Mechanism

**The model (Condorcet's, as Young formalises it).** There is a true ordering of the alternatives,
unobservable. Each voter, on each **pair**, judges correctly with a fixed probability `p`, with
`1/2 < p < 1`, the same `p` for every voter. Each voter's judgment on each pair is independent of
their judgment on every other pair, and independent of the other voters' judgments — Young appends
"(a significant assumption)" to that last one in the text itself. Let `n_ij` be the number of
pairwise votes `i` receives over `j`. Then:

**Result 1 — the maximum-likelihood RANKING is the Kemeny ranking, for every `p`.** "A ranking R has
maximum likelihood if and only if it maximizes Σ n_ij, the sum over all pairs ij such that a_i R a_j.
That is, the maximum likelihood ranking is the one that agrees with the maximum number of pairwise
votes, summed over all pairs of candidates." The exponent of `p` in a ranking's likelihood is the
number of pairwise votes agreeing with it and the exponent of `(1−p)` the number disagreeing, so the
argmax **does not depend on the value of `p`** as long as all judges share it and it exceeds a half.
This rule is Kemeny's rule (Kemeny 1959; Kemeny & Snell 1960), and in the statistics literature it is
the **median procedure**.

**Result 2 — the maximum-likelihood single BEST alternative depends on `p`, and in the weak-judge
limit it is the BORDA winner.** This is the finding that matters most here and it cuts against the
paper's own protagonist. Substituting `p = 1/2 + ε` into the posterior probabilities and dropping
powers of ε above the first, the relative probability of each candidate being best becomes a constant
plus ε times *(all pairwise votes for the candidate minus all pairwise votes against it)*. Since the
total number of pairwise votes is the same for every candidate, that coefficient is maximised by the
candidate with the most pairwise votes overall — "This is precisely the Borda candidate. The reason
is that the Borda score of a candidate in each individual voter's list is equal to the number of
candidates ranked below it, that is, the number that it beats. So a candidate's total Borda score is
its row sum in the voting matrix." Young states it generally: *"For any number of voters and any
number of alternatives, if p is sufficiently close to 1/2, then the candidate with the highest
probability of being best is the one that receives the most pairwise votes."* And he draws the
conclusion rather than burying it: *"The critical case is precisely when p is near 1/2, and then
Borda's rule is definitely optimal."* A Condorcet winner — a candidate beating every other by simple
majority — therefore "does not necessarily have the strongest claim to being the best candidate; the
Borda winner may be stronger."

**Result 3 — in the strong-judge limit the answer is neither, it is maximin.** If `p` is close to 1,
the controlling term is the exponent of `(1−p)`, so "the most probable candidate will be the one
whose weakest comparison is as strong as possible" — rank by each candidate's **minimum** pairwise
vote count and take the maximum (Young's note 11 attributes this minimax rule to Kramer 1977). In his
worked example the three regimes give three different winners: maximin picks `c`, Borda (weak-judge
MLE) picks `b`, and they are not the same candidate.

So the complete answer to criterion (ii), in one sentence: **the positional rule is the right
aggregator when the question is "which items are best" and the individual rankers are barely better
than coin flips; the pairwise/Kemeny rule is the right aggregator when the question is "what is the
whole ordering"; and a maximin rule is right when the rankers are individually very good.**

**Result 4 — local stability, and the example that shows a positional rule failing it.** Independence
here means: *if the set of alternatives shrinks, the remaining alternatives should be ranked in the
same way as they were inside the larger ranking.* Young's reasons for wanting it are the two the lab
cares about — the ranking cannot be manipulated by introducing extraneous alternatives, and "it
allows sensible decisions to be made without requiring an evaluation of all possible decisions."
Full independence is impossible (Arrow), but a restricted version is attainable: `F` is **locally
stable** if for every **interval** `B` of the output ranking `R` (a contiguous block), re-running `F`
on `B` alone returns `R` restricted to `B`.

- **Borda fails it, and the failure can be a complete reversal.** In a six-alternative, 100-voter
  example, the Borda scores over the full set imply the ranking `c a b d e f`. Restricted to just
  `{a,b,c}` — i.e. after dropping three alternatives that *every* one of `a`, `b`, `c` beats by a
  majority — the Borda scores are 117 for `b`, 105 for `a`, 78 for `c`, giving `b a c`: "the reverse
  of how the electorate would have ordered them in the context of all alternatives. Introducing the
  inferior alternatives changes the outcome from b to c."
- **The pairwise rule satisfies it.** A Kemeny ranking's ordering of any interval is unchanged by
  restricting attention to that interval, because otherwise the interval could be rearranged to agree
  with more pairwise votes, and that rearrangement would also improve the full ranking — a
  contradiction. Dropping any bottom segment, any top segment, or any interval leaves the rest in
  place.

**Result 5 — the characterization (second-hand, see tier).** "It follows from a theorem of myself and
Arthur Levenglick (1978) that Condorcet's rule is the unique ranking rule that satisfies anonymity,
neutrality, unanimity, reinforcement, and local stability. Note that Borda's rule satisfies all of
these properties except local stability." *Reinforcement* is the consistency condition: if two
separate groups of voters each approve a ranking, pooling their votes must also approve it.
Y&L (1978) itself was not obtained; this is the folder's standard second-hand provenance, and the
statement above is quoted from the author of the theorem restating his own result.

## Construction recipe

There is no portfolio recipe in this paper; what it gives is a **decision rule for choosing among the
aggregators in the companion note**, plus one diagnostic.

1. **Estimate the judge regime, not the judges.** The relevant quantity is `p`, the probability that
   one lead orders a random *pair* of names correctly by subsequent return. For a score with
   cross-sectional information coefficient, `p` is a monotone transform of it and the transform
   depends on which IC is reported. If the lead's IC is **Kendall's tau** then exactly
   `p = 1/2 + tau/2`, since `tau = P(concordant) − P(discordant) = 2p − 1`. If it is a **Spearman or
   Pearson correlation** `ρ`, then under joint normality `p = 1/2 + arcsin(ρ)/π ≈ 1/2 + ρ/π` for
   small `ρ`. Either transform lands in the same place for the single-digit-percent ICs this lab
   measures: `p` is within a few hundredths of a half. **That is the weak-judge limit, and Result 2
   says the positional composite is the maximum-likelihood rule there.**
2. **Pick the aggregator by the question being asked.** Membership of a top-K set is a *choice*
   problem on K items, not a ranking problem, so Result 2 applies and the mean-of-ranks composite is
   the defensible default. Use a Kemeny/Copeland-type rule only if the construction actually needs the
   full ordering (e.g. a rank-weighted book, which `#513` and `#517` argue against anyway).
3. **Test local stability directly, because the lab's item set genuinely shrinks and grows.** At each
   rebalance date `t`: take the composite ranking over the names eligible at `t`; recompute it over
   only the names eligible at *both* `t` and `t+1`; and measure how many names change relative order,
   and how many enter or leave the top K, **with no score of any retained name having changed**. Any
   such churn is pure positional-rule instability and it is charged at 15–40 bps per side plus
   statutory taxes.
4. **If the churn in (3) is material, the fix is the cheap one, not Kemeny.** Local Kemenization of
   the composite (Dwork note, step 6) buys the ECC and prefix-consistency at `O(k n log n)`; full
   Kemeny optimisation is NP-hard and Result 2 says it is answering the wrong question anyway.

## Robustness evidence (qualitative only)

- The content is a derivation and a theorem; there is no sample, no subperiod, and nothing to decay.
  Both results have been rediscovered repeatedly — Young notes the maximum-likelihood ranking rule
  "has been rediscovered by other writers", names Kemeny's independent derivation, and his note 15
  lists a separate statistics literature on the same object under the name *median procedure*.
- The model's assumptions are the fragile part, and Young is explicit about it: "the specific
  probabilistic model by which Condorcet reached his conclusions is almost certainly not correct in
  its details. The plausibility of his solution must therefore be subjected to other tests, as I have
  attempted to do." That is why he supplies the axiomatic route (Result 4/5) as an independent
  justification — the two arguments for the pairwise rule do not share assumptions.
- The identical-competence assumption is restrictive in a way that matters here: with unequal `p`
  across judges the MLE weights judges by `log(p_ℓ/(1−p_ℓ))`, which is no longer a plain
  majority count. This paper does not derive that case, so a lab wanting to weight leads by measured
  quality has no warrant from this source.
- Young's own summary of when to use what, with no numbers attached: where the object is accuracy of
  a decision ("jury trials, expert opinion pooling"), the pairwise rule "gives the ranking of the
  outcomes that is most likely to be correct"; and it is "relatively stable against manipulation by
  the introduction of unrealistic or inferior alternatives" in a way Borda is not. He concedes
  Borda's three advantages in the same passage: it is much cheaper to compute, it is the better
  estimate of the best candidate when `p` is near a half, and even when `p` is not near a half the
  Borda winner is very likely the best candidate anyway.

## Implementability here

**The headline is a refusal, and it is the useful kind.** The aim went looking for a better
aggregator than the arithmetic mean of normalised ranks. The answer from inside the aggregation
literature's own theory is that **for this lab's regime — a membership choice, from several
individually near-worthless rankings — the mean of ranks already IS the maximum-likelihood rule**,
and the elaborate alternatives (Kemeny, Copeland, the Markov chains) are optimal for a question the
lab is not asking (recovering a full true ordering) or for a judge quality the lab does not have.
That closes the aggregation axis as a *source of edge* at the cost of zero trials, and it means a
future proposal to swap the composite for a pairwise rule must first argue that one of the three
regime conditions has changed.

**The two things that are nevertheless worth taking.**

1. **Local instability is a turnover cost with no information in it, and it is measurable for free.**
   Under protocol v2/v3 the `eligible` panel's columns change — index entries and exits — so between
   consecutive rebalance dates the item set genuinely shrinks and grows. Result 4 says a positional
   composite's *relative* ordering of the names that stayed can move purely because other names
   arrived or left; the six-alternative example turns a `c a b` into a `b a c`. Every position so
   changed is a trade the lab pays for and receives nothing for. The measurement in step 3 of the
   recipe isolates exactly that component of turnover from the component caused by scores actually
   moving, which is what `#515` measures. The two together decompose a composite book's turnover into
   score churn + field churn.
2. **The regime test gives the lab a reason to state, rather than assume, that its leads are weak.**
   `p ≈ 1/2 + IC/2` is one line off stored scores and the honest finding may be that the lab's leads
   are *so* weak that no aggregation rule can be told apart from any other — in which case the
   `#514` name-overlap screen will show it as near-total agreement between the arms, and the whole
   question is closed by two cheap measurements rather than by a trial.

**Pitfalls.**
- The independence assumption is the same binding one as in the companion note, and it is worse here
  because Result 2's derivation needs independence *across pairs within a judge* as well as across
  judges. A lead's score is a smooth function of a characteristic, so its pairwise judgments are
  massively dependent: a single mis-estimated characteristic flips a whole block of pairs at once.
  Read Result 2 as "the positional rule is right in the weak-judge regime", not as a likelihood the
  lab can evaluate.
- Result 2 is about the single **best** alternative. For a top-K set with K in the dozens the strict
  MLE is neither Borda nor Kemeny but the maximiser over K-subsets, which nobody computes; Borda
  remains the defensible approximation but the theorem does not literally cover it.
- Do not read "Borda is optimal as `p` → 1/2" as "weak signals are fine". It says only which
  *aggregator* is right given weak signals; the aggregate of k useless rankings is a useless ranking.
- The `p` → 1 regime (maximin: rank by the worst pairwise showing) is the one regime that would
  recommend a genuinely different construction — select names no lead ranks badly, rather than names
  the leads rank well on average. That is the intersection-type book, which `learnings.md` has
  already measured as a lower bound by construction. Noted as a coincidence of form, not as a
  warrant to re-run it.

## Related

- `notes/2026-11-24-rank-aggregation-positional-versus-pairwise.md` — Dwork et al. (2001): the
  algorithms, the complexity map, and the impossibility theorem that no positional rule can be
  Condorcet. This note says when that impossibility does and does not cost anything.
- `notes/2026-11-24-top-k-distance-measures-and-the-equivalence-class.md` — the measurement side:
  how to quantify the top-K disagreement that step 3's local-stability test produces.
- `#513`, `#517` (`notes/2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md`,
  `notes/2026-11-23-exposure-matched-blend-comparison-and-the-active-risk-crossover.md`) — the
  construction that uses a composite to decide membership, and the open mix-versus-integrate tension.
  Result 2 is a theoretical argument *for* the composite-as-membership arm being built with the plain
  mean, which is what those sources do empirically.
- `#515` — between-rebalance rank autocorrelation of each lead's score; the companion half of the
  turnover decomposition proposed above.
- `#1` (`notes/2026-08-17-naive-vs-optimized-weighting.md`) — the estimate-nothing triage screen.
  Every rule in this note and the companion estimates nothing, so the screen is silent on them and
  the choice has to be made on the grounds in this note instead.
