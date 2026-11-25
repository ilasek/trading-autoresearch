---
title: "Optimal weights for judges of UNEQUAL competence, and what dependence does to them — the log-odds weight that ignores every other judge, the test that says whether ANY weighted rule is optimal at all, and the bloc partition that is the actual answer for correlated judges"
authors: Shapley, Grofman
year: 1984
venue: "Public Choice 43(3), 329–343. Peer-reviewed; the flagship journal of public-choice economics and a standard venue for the Condorcet-jury literature (tier 1 within its field, tier 2 by this folder's finance-centric table — graded on content and replication, per the rubric's note that a heavily-cited non-finance source is not Tier C for not being a finance journal)."
url: https://doi.org/10.1007/BF00118940
citations: "176 (Crossref `is-referenced-by-count`, checked 2026-11-25); 273 (Semantic Scholar by DOI, same date). The companion review that states the same theorem as its Theorem XIII, Grofman–Owen–Feld (1983), `10.1007/BF00125672`: 303 (Crossref) / 473 (Semantic Scholar), same date."
sample_period: "n/a — theorems plus arithmetic worked examples with invented competence vectors. No data of any kind."
markets: "None. Judges are voters, items are a pair of alternatives; transfer to this lab is by construction."
tier: "A. Peer-reviewed, heavily cited across political science, statistics and decision analysis, and the content is theorems, so there is no sample to be fragile. Honest limits recorded below: Theorem II holds only under independence, the dependence section is worked EXAMPLES rather than a general theory, and the bloc-partition recipe the lab would actually use is stated in the Discussion as an approximation with no error bound."
validation_overlap: false
published_post_2018: false
read: "Full text, 15 pp. (329–343), 830 KB PDF from the second author's UC Irvine faculty page, HTTP 200 first request; `pdftotext -layout` → 44 KB of text, 266 instances of ` the `, parenthesis balance 253/252, no ASCII shift, title and journal line verified. The OCR mangles subscripts and some displayed fractions (`w_i ∝ log p_i/(1-p_i)` prints as `wi oc log P ( ~ )` in one of the two places it appears), so every algebraic claim below was cross-checked against the paper's own running prose, which restates each one in words, and against the same theorem as stated in the companion review (Grofman–Owen–Feld 1983, read the same night)."
access_note: "`sites.socsci.uci.edu/~bgrofman/<NN>%20<Authors>-<Title>.pdf` served this article, the 1983 companion review and a third related paper, all at HTTP 200 on the first request. The channel is the 2026-09-18 faculty-page lesson in its strongest form: a scholar's own numbered reprint archive, where the number is a bibliography index and the filename contains the full title. Found by a plain title search, not by guessing the hostname."
---

## Why this source is here

The [2026-11-24] aim: *aggregating several rankings or forecasts of the same items when the judges
are **correlated** and/or of **unequal quality***, admitted only with (i) explicitly correlated or
unequally competent judges, (ii) the weight or effective-count **in closed form**, (iii) the
**degenerate limit** as judge correlation goes to one, and (iv) nothing estimated beyond a
correlation the lab already measures. That aim exists because `#518` and `#522`(c) left the folder
with an aggregation rule whose derivation assumes independent judges while `learnings.md` records an
inter-signal ensemble killed at rank correlation **0.89** and a promoted blend whose two legs
correlate **0.66**.

This paper is the primary for the unequal-competence half, and it is the source of the log-odds
weight that the whole later literature cites. It is admitted on (i), (ii) and (iv) without strain.
On (iii) it satisfies the weak arm: it does not give a correlation-indexed weight, it gives a
**test** for whether weighting is the right operator at all, plus a partition recipe. The
correlation-indexed weight itself is in the companion note (`2026-11-25-the-opinion-leader-model-...`),
and the identification problem underneath both is in the third (`...-what-a-pairwise-correlation-does-not-pin-down`).

## Mechanism

**The setting.** `N` judges face a dichotomous choice; exactly one of the two options is "better"
under some linear ordering. Judge `i` picks the better one with probability `p_i` (their
*competence*). The two options are a priori equally likely. The group's decision rule maps the
`N` votes to one choice, and `P_N` is the probability the group's choice is the better one.

**Theorem I (the heterogeneous Condorcet result, stated as background).** With independent judges,
simple majority rule makes `P_N` rise toward 1 in `N` when the average competence exceeds a half.
The paper's own interest is in what beats simple majority.

**Theorem II — the Bayesian optimal decision rule.** *In a heterogeneous group with mutually
independent choices and even priors, the rule that maximises `P_N` is a weighted majority rule with*

```
w_i  ∝  log( p_i / (1 - p_i) )
```

The proof is attributed to Shapley (1979, unpublished) and independently to Nitzan & Paroush (1982);
the paper's own gloss is that the theorem is a restatement of Bayes' theorem, which is why the
posterior is invariant to the order in which the evidence arrives.

**The property that makes it usable, and that the authors themselves call counterintuitive.** Once
a logarithmic base is fixed, *a judge's weight is a function purely of that judge's own competence
and is independent of the competence of the other judges and of the group size.* A judge carries
the same weight into any panel. What varies with the panel is the judge's **power** — the share of
vote configurations their weight actually decides — which can range from dictatorial to a dummy
with the weight unchanged.

**Optimal weights are almost never unique.** The worked five-judge example `(0.9, 0.9, 0.6, 0.6,
0.6)` gives log-odds weights `(0.954, 0.954, 0.176, 0.176, 0.176)`, normalised `(0.392, 0.392,
0.072, 0.072, 0.072)`; the paper then writes out the seven linear inequalities that *any* weight
vector must satisfy to induce the same winning coalitions, and notes `(1/3, 1/3, 1/9, 1/9, 1/9)`
satisfies them too. **The object that matters is the set of winning coalitions, not the weight
vector.** Two weight vectors that differ numerically but induce the same coalitions are the same
rule. (The companion review's worked numbers for this example: best-member-decides `0.9`, simple
majority `0.87`, optimal weighted rule `0.93`.)

**Section 3 — interdependent competences, and the finding is a refusal, not a formula.** Dropping
independence, the authors do not produce a dependence-adjusted weight. They produce two examples and
one theorem.

*Example 1, negative dependence.* Three judges, exactly one of whom is certainly wrong, each equally
likely to be the wrong one, the other two independently right with probability `r`. Unconditional
competence is `p̄ = 2r/3`; the conditional probability that judge 1 is right given judge 2 is right
is only `r/2 < p̄`, so competences are **negatively** dependent. The distribution of "exactly `k`
judges right" is `p(0) = (1-r)²`, `p(1) = 2r(1-r)`, `p(2) = r²`, `p(3) = 0`. **If the group is
unanimous it must be wrong.** Majority rule is correct with probability `r²`; the *non-monotonic*
rule "follow a 2–1 majority, oppose a 3–0 unanimity" is correct with probability `r² + (1-r)²`,
which is strictly better. Under independence with every `p_i > 1/2` nothing like this can happen.

**Theorem III — the admissibility test for weighting itself.** For any distribution that is fully
symmetric in the judges (dependent or not), let `p(k)` be the probability that exactly `k` judges
are right. Then **weighted voting is optimal if and only if**

```
p(k) > p(N - k)   for all k > N/2
```

and the posterior that a choice backed by `k` votes is correct is `p(k) / (p(k) + p(N-k))`. The
proof is monotonicity of any weighted rule (Shapley 1962): a weighted rule is forced to be more
confident in a larger plurality, so if the data say otherwise, *no* weighted rule — not simple
majority, not the log-odds rule, not any reweighting — can be optimal.

*Example 2, blocs.* Nine judges in three "districts" of three, each district internally dependent as
in Example 1, districts independent of each other. Simple majority over all nine is correct with
probability `r⁵(6 - 5r)`; a compound rule — majority inside each district, then majority of the
three district verdicts — is correct with probability `r⁴(3 - 2r²)`, which is **larger for every
`r < 1`**, and the best monotonic rule here is not representable as weighted voting at all. A third,
non-monotonic compound rule does better still. The paper's own aside on an intermediate case: the
weight vector `(1,1,1,0,0,0,0,0,0)` — *ignore six of nine judges* — beats simple majority over a
narrow range of `r`. "Three heads are better than nine!"

**The Discussion's recipe, which is the transferable instrument.** *Partition the judges into blocs
such that choices may be correlated **within** a bloc and are independent **across** blocs. Find the
optimal rule inside each bloc and compute that bloc's competence, treating the bloc as a single
entity voting by its own internal rule. Then apply Theorem II to the blocs, i.e. weight each bloc
by the log odds of its bloc competence.* The authors add that "even if interbloc correlations exist,
as long as they are small, partitioning the voters into discrete cluster-blocs and then proceeding
as outlined will yield a very good approximation to optimality" — stated as an approximation, with
**no error bound**, which is the honest limit of the recipe.

Also recorded, because a future session will want it: the restriction to a dichotomous choice is
less binding than it looks, since multi-alternative procedures (sequential pairwise amendment,
and the Borda rule itself) decompose into pairwise choices — though the authors expect the
decomposition chosen to affect the probability of a correct choice.

## Construction recipe

Judge-level, for a panel of `k` scoring rules over the same item set:

1. **Reduce each judge to a dichotomous verdict per item pair, or per item against a reference.**
   The theorem is about a binary choice; a continuous score has to be binarised (e.g. "does this
   lead place item `i` above the cut?") before any of this applies.
2. **Estimate each judge's competence `p_i`.** Either against realised outcomes, or — see the
   companion note — from the judge's agreement rate with the panel majority, with no answer key.
3. **Weight `w_i ∝ log(p_i/(1-p_i))`**, then decide by weighted majority. The base of the log is
   free. Check which *coalitions* the weights make winning; two weight vectors with the same
   winning coalitions are the same rule and the numeric difference is meaningless.
4. **Before any of that, run the Theorem III test.** Tabulate `p(k)` = the frequency with which
   exactly `k` of the `k` judges are right, over whatever history exists. If `p(k) ≤ p(N-k)` for
   some `k > N/2` — i.e. if unanimity is *less* reliable than a bare majority — stop: no weighted
   rule is optimal, and the right operator is non-monotonic (discount unanimous agreement).
5. **If judges are correlated, partition first.** Cluster judges into blocs by their measured
   agreement; find each bloc's internal rule and bloc competence; apply step 3 **to the blocs**.

## Robustness evidence (qualitative only)

The log-odds theorem is a theorem, not an empirical claim, and it was derived independently at least
three times in different literatures — Shapley (1979, unpublished), Nitzan & Paroush (1982), and, in
pattern-recognition form, the sources the companion review cites (Pierce 1961; Minsky & Papert 1971;
Duda & Hart 1973). That independent rediscovery is the strongest robustness statement available for
an analytic result. The companion review (Grofman–Owen–Feld 1983, Theorem XIII) restates it
identically, which is how the subscript-mangled OCR in this PDF was checked.

The dependence results are **worked examples, not a general theory**: three judges, nine judges in
three blocs, one symmetric distribution class. Theorem III itself is general within the class of
distributions symmetric in the judges, which is a real restriction — it assumes exchangeable judges,
and a panel of deliberately different signals is the case where exchangeability is least plausible.

The paper's closing caveat, which cuts against its own headline: "especially for large `N`, simple
majority rule may turn out to be 'near' optimal". The companion review repeats it as unpublished
work in progress. So the measured gain from optimal weighting over equal weighting is expected to be
*small* when the panel is large, and the theorem's value is mostly as a *bound* on what reweighting
can buy.

## Implementability here

**What transfers, and it is the thing the [2026-11-24] aim asked for.** The lab combines `k` lead
scores into one composite that decides membership (`#513`, `#518`). This source says the correct
object is not a per-lead weight but a **bloc structure**: correlated leads are one judge, and the
log-odds weight applies at the bloc level. That is a direct, buildable amendment to `#513`'s
composite, and it needs only the lead-score correlations the lab already computes for its
decorrelation screen, plus a per-lead hit rate.

**What is free here and should be measured before any trial.** The Theorem III test costs nothing:
for the stored lead scores, count over dates how often exactly `k` of the `k` leads put a name above
the cut *and* that name subsequently outperformed the eligible pool, and compare `p(k)` to
`p(N-k)`. If unanimous agreement among the leads is not more reliable than a bare majority, every
weighting scheme the lab might try is dominated, and `#521`'s local Kemenization — a monotone,
majority-based post-process — is pointed the wrong way.

**What does NOT transfer, stated plainly.**
- `p_i` here is a competence on a *single binary decision with a true answer*. A lead's information
  coefficient is a cross-sectional rank correlation; converting it to a `p` is the `#518` regime
  test (`p = 1/2 + τ/2`, or `≈ 1/2 + ρ/π` under joint normality), and at the lab's single-digit ICs
  every `p_i` sits within a few hundredths of a half. The log-odds weights of two leads with `p` of
  `0.52` and `0.54` differ by about a factor of two, which is **inside** the noise of estimating
  either — so the weights are not estimable at the lab's effect sizes even though the formula is
  exact. This is the same objection `#375`/`#518` raise against magnitude weighting, arriving from
  a different direction.
- The bloc recipe assumes blocs are independent *of each other*. The lab's leads are all long-only
  books on one equity panel and share a market factor by construction, so inter-bloc correlation is
  **not** small and the approximation's unbounded error is live. The honest reading is that the
  recipe gives the right *shape* (cluster, then weight clusters) and not a calibrated weight.
- Nothing here licenses a return expectation, and none is recorded.

**Pitfall.** The uniqueness failure is the practical trap: a session that tunes a weight vector
without checking the induced coalitions will spend trials distinguishing rules that are literally
identical. With `k = 2` leads there are no non-trivial coalitions at all, so "weighting" degenerates
to picking one lead or the other; the whole apparatus needs `k ≥ 3` blocs to say anything.

## Related

- `notes/2026-11-25-the-opinion-leader-model-and-the-bloc-weight-discount.md` — the companion
  review, which supplies the closed-form **discount** for a correlated bloc that this paper's
  Discussion only gestures at, plus the answer-key-free competence estimator.
- `notes/2026-11-25-what-a-pairwise-correlation-does-not-pin-down.md` — the identification result
  that limits both: pairwise correlations do not determine the panel's competence.
- `notes/2026-11-24-when-a-positional-rule-is-the-right-aggregator.md` (`#518`) — Young's
  independent-judge model, whose independence assumption this note is the correction to.
- `notes/2026-11-24-rank-aggregation-positional-versus-pairwise.md` (`#521`, `#522`(c)) — the
  anti-candidate this note gives a constructive answer to.
- `notes/2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` (`#513`) — the
  construction the bloc amendment attaches to.
- `experiments/learnings.md` — the 0.89 inter-signal rank correlation that killed an ensemble, and
  the 0.66/0.69 correlation of the two legs of a blend that was promoted: the lab's own evidence
  that its judges are blocs, not independents.
