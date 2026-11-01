---
title: "Do t-Statistic Hurdles Need to be Raised?"
authors: Chen
year: 2025
venue: Management Science 71(7), 5830–5848 (Tier 1 by this folder's rubric). The version read is the author's arXiv v4 (April 2024, arXiv:2204.10275); first posted to SSRN September 2018.
url: https://doi.org/10.1287/mnsc.2023.03083 · full text read from https://arxiv.org/pdf/2204.10275
citations: 5 (Crossref `is-referenced-by-count` on the Management Science DOI, checked 2026-11-01); 4 (Semantic Scholar, checked 2026-11-01). **Low on recency, not on impact** — the journal version is very recent, the working paper circulated from 2018, and the rubric's instruction not to downgrade tier on a count alone applies: the venue is Tier 1 and this author's directly adjacent paper is a *Journal of Finance* article already in this folder.
sample_period: "No market estimation window of its own. The empirical object is the distribution of **published t-statistics** for cross-sectional stock-return predictors, taken from the open-source reproduction dataset; those predictors' own in-sample windows end mostly in the 1980s–2000s. Theoretical results impose no sample at all."
markets: not a market study — the unit of observation is a published factor, drawn from the US cross-sectional predictability literature
tier: A− — Tier-1 venue, the propositions are proved and distribution-free, the empirical claims are bootstrapped and shown to hold across 10 alternative specifications, and the author's code is public. Held at A− because the citation record is too young to be evidence and because the empirical half inherits the reference dataset's own limits.
validation_overlap: false
published_post_2018: true
---

## Access

Read in full from **`arxiv.org/pdf/2204.10275`** (905 KB; `pdftotext -layout` → 130 KB of clean
text, 600 instances of `" the "`, zero `( )` dropout, no ASCII shift). Note the integrity-check
trap: `file -b` reports **"1 page(s)"** for this document while extraction yields a complete
40-page article — the 2026-10-07 lesson that `file`'s page count is not a completeness check,
now in its most extreme form yet.

**Post-2023 source, handled explicitly.** The journal version carries a 2025 publication year and
the copy read is dated April 2024. Per `research/README.md`'s absolute ban, **nothing in this note
describes the world after 2023-12-31**: the content recorded below is (a) proved propositions with
no sample, and (b) estimates computed on the distribution of t-statistics of predictors whose own
samples end well before this lab's validation window. No market event, no performance, no regime
commentary from the source's own vintage is recorded or should be inferred.

## Mechanism

**The question.** A long line of work calls for raising the conventional `|t| > 1.96` discovery
threshold to guard against false discoveries in a literature that has tested very many factors.
This paper asks whether that call can be **empirically justified**, and finds that the data cannot
answer it — while the *same* data answer a neighbouring question sharply. Both halves matter here,
because this lab's promotion gate is a raised hurdle whose height grows with the trial count.

**Result 1 — the hurdle should be raised if and only if one specific inequality holds, and it is
not automatic.** Write `π_F` for the share of false candidates in the tested population and
`Pr(|t| > 1.96)` for the share of candidates that clear the classical threshold. Then (the paper's
Proposition 1, under a mild monotonicity condition on `Pr(false | |t| > h)`):

```
FDR-controlling hurdle at 5%   >  1.96   iff   π_F  >  Pr(|t| > 1.96)
                               =  1.96   iff   π_F  =  Pr(|t| > 1.96)
                               <  1.96   iff   π_F  <  Pr(|t| > 1.96)
```

So a multiple-testing correction **can lower the threshold**, and whether it raises it is an
empirical question about two quantities, not a consequence of having run many tests. The intuition
is a mass comparison: if nearly everything tested is false, 5% of them clear 1.96 by luck and the
false-discovery rate among discoveries is enormous, so the hurdle must rise; but if a substantial
fraction of candidates are real and the realised discovery rate is well above 5%, the discoveries
are mostly real and the classical threshold is already conservative. The author is blunt that the
pessimistic case has no logical priority — assuming it "amounts to placing additional restrictions
on the model and it is unclear how to motivate these restrictions".

**Result 2 — the popular corrections assume the answer.** Two standard algorithms are shown to be
*equivalent* to fixing `π_F` rather than estimating it:

- **Benjamini–Hochberg (1995)** is isomorphic to setting `π_F = 1.0` — i.e. assuming *everything*
  tested is false. It therefore raises the hurdle in every case except the degenerate one where
  every candidate clears 1.96.
- **Benjamini–Yekutieli Theorem 1.3** — the arbitrary-dependence variant, the one the finance
  multiple-testing literature leans on and the one the hierarchical-Bayes replication study used
  for its frequentist comparison — is isomorphic to setting `π_F = Σ_{i=1..N} 1/i`. For `N ≈ 300`
  that is **`π_F ≈ 6.3`**, i.e. six times the largest value a share can take. A corollary follows
  immediately: this algorithm **always** concludes that hurdles must be raised. The original
  authors themselves describe it as "very often unneeded, and yields too conservative of a
  procedure", and the statistics literature prefers the 1995 algorithm over it.

The transferable point is not that these algorithms are wrong — they are valid conservative FDR
controls — but that **they are not evidence about how severe a correction is needed**, because the
severity is an input rather than an output. A gate built on one of them cannot be cited as showing
that its own height is justified.

**Result 3 — `π_F` is weakly identified *when the data are censored*, which is why the hurdle
question cannot be settled.** Published data exhibit publication bias: results failing the
existing threshold are often never observed. The share of false candidates lives almost entirely
in the unobserved region, so it must be extrapolated, and the likelihood is nearly flat in it. The
paper proves the identification failure and then demonstrates it: bootstrapped hurdle estimates on
the published-predictor dataset have **90% confidence intervals spanning roughly 0 to 2.9** in most
of the 10 alternative specifications — i.e. the data are consistent with lowering the threshold to
nothing and with raising it substantially.

**Result 4 — the right tail IS well observed, so shrinkage and the local FDR *are* strongly
identified.** Statistics that only need the published (right-tail) region are plentifully
supplied. Across all 10 specifications the bootstrap puts **shrinkage at most 29%** and the
**local false-discovery rate among published predictors at most 25%**, both with 95% confidence;
the modal shrinkage estimate is near 12%. The author also notes that the pessimistic study's *own*
numerical estimates (`π_F = 0.444`, 353 of 1,378 t-statistics above 1.96) imply, by Bayes' rule,
a false-discovery rate among published findings of only about **8.6%** — in tension with that
study's verbal summary that most claimed findings are likely false. **The arithmetic and the
rhetoric of the pessimistic position point in different directions.**

So the practical recommendation inverts the usual move: **do not raise the threshold on the
strength of a trial count — shrink the estimate instead**, because the shrinkage factor is
estimable from data you actually have and the hurdle correction is not.

## Construction recipe

Not a portfolio recipe. A **decision-procedure** recipe, for a lab choosing how to penalise a
search:

1. **Before adopting any multiple-testing correction, ask what value of `π_F` it implies.** Invert
   the algorithm (the paper does this for both standard ones) and read off the share of false
   candidates it is assuming. If that number is above 1, the procedure is conservative by
   construction and carries no information about the right severity.
2. **Estimate the discovery rate you actually observe**, `Pr(|t| > 1.96)` — the fraction of your
   own candidates clearing the classical threshold — and compare it with any estimate of `π_F`.
   Proposition 1 then says which direction the correction goes. **Both quantities must be measured
   on the same population.**
3. **Prefer statistics defined on the region you can see.** Empirical-Bayes shrinkage of the
   estimate and the local FDR among the candidates you *did* discover need only the right tail;
   hurdle estimation needs the censored left region. Choose the former.
4. **Bootstrap, and report the interval, not the point.** The paper's entire contribution is the
   width of the interval; a point estimate of a hurdle from censored data is not a result.
5. **Check robustness by re-specifying the latent distribution, not by re-running the same
   model.** The paper's 10 alternatives vary the publication-probability function, the
   distributional family, the treatment of small observed t-statistics, and a floor on `π_F`; the
   strongly-identified quantities move little and the weakly-identified one stays uninformative.

## Robustness evidence (qualitative only)

The two load-bearing propositions are proved and impose almost no functional form, which is why
the empirical robustness across 10 specifications is unsurprising rather than lucky. The author
reports that earlier drafts reached the same conclusions under further variations (separating
standard errors from t-statistics, modelling the full correlation distribution) and the code is
public. The shrinkage estimate independently reproduces the point estimate from a different paper
by the same author, obtained under a *unimodal* latent distribution, while this paper assumes a
**bimodal** one — which answers a published critique that claimed the estimate was an artefact of
unimodality. That is a real out-of-model check and the strongest single robustness item here.

Weaknesses, two of them honest and one structural. The empirical half inherits the reference
dataset's composition — US cross-sectional predictors, classified by hand — so a different corpus
could give different right-tail estimates. The author's framing concedes that readers may disagree
about whether a worst-case false-discovery rate of 25% is acceptable; the paper establishes the
bound, not the verdict. And the citation record is too young to count as independent validation;
tier rests on venue, proof, and the author's prior Tier-1 work in the same vein.

Lookahead status: no market sample of its own, so `validation_overlap: false`;
`published_post_2018: true`, and the source postdates 2023 — see Access for how that is handled.

## Implementability here

**Free, and it bears directly on the gate rather than on any book.** Four items.

1. **The lab's trial record is NOT censored, which puts it in the favourable case of this paper's
   own taxonomy.** The identification failure here is caused entirely by publication bias: results
   below the threshold are unobserved, so `π_F` must be extrapolated. `experiments/trials.jsonl`
   records **every** trial of every protocol version — `REJECT`, `GATE_FAIL`, `SCOUT`,
   `HOLDOUT_VETO` and `PROMOTE` alike — and the lab's own rules forbid deleting or rewriting that
   history. **There is no censoring, so there is no weak identification, and `π_F` and
   `Pr(skill > 0 at the classical threshold)` are both directly countable from the record.** This
   is the single most useful thing in the paper for this repo: the objection that makes the hurdle
   question unanswerable in the literature **does not apply here**, and the comparison in
   Proposition 1 is therefore computable rather than extrapolated. That is a free diagnostic.
2. **Run Proposition 1's comparison before defending the height of the deflated bar.** Count, over
   the whole recorded trial history, the fraction of trials whose validation skill cleared the
   classical threshold — that is `Pr(|t| > 1.96)` for this lab — and compare it with any estimate
   of the share of candidates that were genuinely skill-free. The proposition then says whether an
   FDR-controlling threshold for this lab sits **above or below** 1.96. Two cautions that are this
   folder's, not the paper's: the lab's trials are strongly dependent (many share a mechanism and
   a return stream, which is why `distinct_mechanisms` exists), and a trial is not an independent
   draw when it is a knob-sweep of its predecessor — so the honest count is at the **mechanism**
   level, matching this folder's 2026-11-01 denominator lesson.
3. **The standing tension with the deflated-Sharpe bar, now sharpened.** This folder has carried a
   stated tension between the deflated-Sharpe machinery and the hierarchical-shrinkage view since
   2026-09-15. This paper resolves part of it with an argument rather than a preference: a
   trial-count-indexed threshold is in the family that *assumes* its own severity, whereas a
   shrinkage factor is estimable. Combined with the open question's own observation that the
   deflation benchmark now exceeds the board-best skill — making the gate's numerator negative for
   every book the lab has built — the implication is specific: **the gate's conservatism is
   currently an input, not a measurement, and the measurable alternative is to shrink the reported
   skill and keep the classical threshold.** That is a change to a protocol threshold, so it is a
   matter for the human owner and **not** something a session may act on; it is filed as such.
4. **One correction this folder owes a previous note.** The hierarchical-Bayes replication study
   reports a frequentist comparison using **Benjamini–Yekutieli Theorem 1.3** and finds its
   replication rate drops sharply under it. This paper shows that algorithm is isomorphic to
   `π_F ≈ 6.3` at that study's `N` — an impossible value — and therefore **always** raises the
   hurdle. So the gap between that study's Bayesian and frequentist replication rates is in large
   part a property of the chosen frequentist algorithm, not a measurement of how much multiple
   testing costs. Any future citation of "the frequentist correction cuts the rate by this much"
   should carry that caveat.

**Not implementable as a signal, and it proposes no book.** It is a screen on the lab's own
decision rule, and one of its two conclusions (item 3) is explicitly out of this agent's hands.

## Related

- `notes/2026-08-24-multiple-testing-haircut.md` — the Harvey–Liu–Zhu haircut and the `t > 3`
  recommendation this paper is a direct rebuttal to; this note supplies the identification argument
  that the recommendation lacks, plus the Bayes-rule arithmetic showing that study's own parameters
  imply a modest false-discovery rate among published findings.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — the family the lab's own bar belongs to; item 3
  above is the sharpened form of the tension this folder has carried since 2026-09-15.
- `notes/2026-10-01-limits-of-p-hacking-publication-bias.md` — the **same author** on the companion
  questions (p-hacking cannot generate the observed t-distribution; how much to shrink a published
  t-statistic). The 12% shrinkage point estimate this paper reproduces under a bimodal latent
  distribution is that note's number, and the reproduction answers the published critique of it.
- `notes/2026-11-01-reproduction-versus-replication-open-source.md` — the dataset this paper's
  empirical half is estimated on, and the source of the denominator lesson item 2 depends on.
- `notes/2026-08-25-hierarchical-bayesian-factor-replication.md` — the empirical hierarchical-Bayes
  alternative this paper recommends in principle; item 4 is a correction to how that note's
  frequentist comparison should be read.
- `notes/2026-08-25-prior-weighted-multiple-testing.md` and
  `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — the rest of this folder's
  multiple-testing shelf. Every one of them asks whether the best of `N` is *significant*; this one
  asks whether the question is *identified*, which is a prior step none of them takes.
