---
title: "Instrumental Variables as Bias Amplifiers with General Outcome and Confounding"
authors: Ding, VanderWeele, Robins
year: 2017
venue: Biometrika (venue tier 1 — peer-reviewed)
url: https://doi.org/10.1093/biomet/asx009
citations: 70 (Crossref `is-referenced-by-count`, checked 2026-11-15)
sample_period: n/a — analytic theorems plus Monte Carlo over a parameter space; two non-financial applied illustrations
markets: none (methodology; illustrations are an education effect and a class-size effect)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the **adversarial source of the vein**, in the sense `research/README.md` requires: it
is the paper that says the dominant practice — *adjust for everything measured before the
treatment, because a more conditional assumption is a weaker one* — is **not merely wasteful
but can be strictly worse than doing nothing**, and it proves it rather than simulating it.

The object is a covariate `Z` that is a cause of the treatment `A`, is independent of the
unmeasured confounder `U`, and affects the outcome `Y` only through `A` — an **instrument**.
With `U` unmeasured, *both* the adjusted and the unadjusted analyses are biased. The paper
asks when the **adjusted** one is worse, and calls such a `Z` a **bias amplifier** ("Z-bias").

**Why it happens, in one mechanism.** The treatment's variation has three sources: the
instrument, the unmeasured confounder, and independent noise. **Conditioning on the instrument
removes one of the innocent sources**, so within strata of `Z` the treatment's remaining
variation is driven *proportionally more* by `U` — and the confounding bias from `U` gets a
larger share of a smaller variance. The paper's own phrasing of the paradox is the useful one:
*without* adjusting for the instrument, the study is **more like a randomised experiment**, and
the bias is smaller. This is a statement about the *composition* of the treatment's variance,
not about any association being estimated badly, which is why it survives generalisation.

**What the paper adds to what was already known.** Z-bias had been shown numerically
(including by the applied simulation study this folder could not obtain — see *Channels*
below) and proved **only for linear structural equation models**. This paper proves it for a
wide non-parametric class under **monotonicity** conditions, so it cannot be dismissed as a
linear-algebra artifact:

- **Theorem 1 (scalar `Z`, scalar `U`)**: if `pr(A=1 | Z=z)` is non-decreasing in `z`,
  `pr(A=1 | U=u)` is non-decreasing in `u`, and `E(Y | A=a, U=u)` is non-decreasing in `u` for
  both `a`; **and** `E(Y | A=a, Z=z)` is non-increasing in `z` for both `a` — then the
  adjusted estimators' biases are **component-wise no smaller** than the unadjusted one's, for
  the treated, control and whole populations.
- The second condition is not an extra assumption so much as a consequence: **conditioning on
  `A` is conditioning on a collider**, and if `Z` and `U` push `A` in the same direction, that
  collider bias makes `Z` and `U` negatively associated given `A`, which with `U` positively
  related to `Y` delivers the non-increasing condition.
- **Theorems 2 and 3** replace the awkward second condition with an interpretable one: if `A`
  given `(Z, U)` has **no additive interaction** (`pr(A=1|z,u) = β(z) + γ(u)`) or **no
  multiplicative interaction** (`β(z)γ(u)`) between instrument and confounder, plus
  monotonicity, Z-bias follows. With binary `Z` and `U` these become conditions on
  `p_zu = pr(A=1|Z=z,U=u)` that can be read off a two-by-two: no additive interaction is
  `p₁₁ − p₁₀ − p₀₁ + p₀₀ = 0`, no multiplicative interaction is `p₁₁p₀₀ = p₁₀p₀₁`.
- **The weaker sufficient condition** is the practically important one, because it is an
  inequality rather than an equality: `p₁₁p₀₀/(p₁₀p₀₁) ≤ 1` **and**
  `(1−p₁₁)(1−p₀₀)/((1−p₁₀)(1−p₀₁)) ≤ 1` — non-positive multiplicative interaction on both the
  presence and the absence of `A`. **Half the parameter space satisfies it**, so Z-bias arises
  over more than half the space even with interactions present.
- **Theorem 4** is the fully general one and assumes **no causal diagram at all**: taking
  `U = {Y(1), Y(0)}` (the pair of potential outcomes, which is not an assumption — it is
  forced, because `Y = AY(1) + (1−A)Y(0)` makes that pair a sufficient confounder), Z-bias
  follows if `pr{A=1 | Y(a)}` is non-decreasing in `Y(a)` and `cov{Π, ν_a(Π)} ≤ 0`, where
  `Π = Π(Z) = pr(A=1|Z)` is the instrument's own propensity score and
  `ν_a(π) = E(Y | A=a, Π=π)`. The first condition **is** the self-selection of an
  observational study (under randomisation it would be flat); the second is the collider-bias
  measure in general form.
- A general vector instrument and vector confounder reduce to the scalar case through `Π(Z)`,
  so the result is not about dimension.

**How much of the space it covers — the one number worth carrying.** Over `10⁶` draws of all
ten probabilities of the binary `(Z, U, A, Y)` model from independent uniforms, the adjusted
estimator is more biased than the unadjusted one in **0.6805 of the parameter space (standard
error 0.0005)** — call it **about 68%**. And the complement is real: the paper exhibits a
worked case with monotonicity and interactions where **Z-bias does not arise**. The conditions
are **sufficient, not necessary**, in both directions.

**The boundary — and it is the clause that matters most for any real application.** If `Z` has
*any* direct arrow to `Y` (a "near-instrument"), **Theorems 2, 3, 5 and 6 all fail.**
Theorem 1 generalises (Theorem 7) and Theorem 4 still holds, but the paper's own assessment is
that Theorem 7 is *"of little use in practice without strong substantive knowledge about the
size of the direct effect of `Z` on `Y`"*. The same collapse happens if there is an unmeasured
common cause of `Z` and `Y`, even with no direct effect. So the clean result applies to a
**clean** instrument, and a variable that is *mostly* unrelated to the outcome does not inherit
it.

## Construction recipe

There is no estimator to build. The construction is a **decision procedure plus a free
diagnostic**, and the diagnostic is the paper's own recommendation for the case that actually
occurs in practice — where you cannot tell whether a covariate is a confounder (control it) or
an instrument (controlling it only amplifies existing bias):

1. **Classify, if you can.** Is the candidate a cause of the treatment with no path to the
   outcome except through the treatment? If yes, and you are confident, **do not adjust for
   it** (this is step 3 of the modified disjunctive cause criterion).
2. **If you cannot classify it — which is the normal case — run the analysis both ways.**
   Report the estimate **with** and **without** the covariate.
   - **If the two agree**, Z-bias is not a concern for this covariate and the choice does not
     matter. (The paper's own applied illustration lands in this cell.)
   - **If they disagree**, you have learned that the covariate is doing something, and
     **no amount of further staring at the same data resolves it** — the paper says
     explicitly that additional information and analysis are required before deciding.
3. **Check the monotonicity conditions you can check.** The signs of the dependences
   (treatment increasing in the covariate, outcome increasing in the confounder) are often
   substantively known; a binary two-by-two makes the no-interaction conditions arithmetic.
4. **Do not treat the absence of a direct effect as a free assumption.** A near-instrument
   puts you outside every interpretable theorem.

## Robustness evidence (qualitative only)

Analytic, so there is no sample and nothing to decay: the content is theorems plus a
Monte Carlo over a parameter space (not over a time period), plus two non-financial applied
illustrations. The robustness that matters for a result of this kind is **generality**, and the
paper is explicit about its own limits in both directions — it supplies a counterexample where
Z-bias does not arise, states that its conditions are sufficient and not necessary, and
identifies precisely which theorems break when the instrument is not clean.

Replication status is unusually clear for a methodological claim: the phenomenon was
established numerically by several independent applied groups before it was proved, proved
first for linear models, and this paper is the general proof — the opposite of the usual
sequence in which a single result fails to replicate. The applied simulation study whose
generative models the paper re-reads (additive and multiplicative in `(U, Z)`) is shown to
satisfy the corollaries, so **the simulated finding and the theorem are the same finding**.
The authors note their theory says nothing about the **magnitude** of the bias, only its
direction — magnitudes stay with the simulation literature.

## Implementability here

**What this is, for this lab: the formal ceiling on "add another control".** The lab's
instinct when a reading looks contaminated has been to add a control — log `P` on
2026-11-08/09, then jointly `vol126` on 2026-11-10/11. This paper is the reason that instinct
needs a stopping rule rather than a counter: **when the confounder you actually care about is
unmeasured, a control that is strongly related to the score and weakly related to forward
returns can leave the reading *more* biased, not less.** The lab's residual confounders are
not hypothetical — the engine issues filed 2026-10-18 and 2026-10-22 are precisely unmeasured
contamination in the stored price level, and `#432` records two opposite-signed biases in the
equal-weight pool. That is the `U` of Figure 1(b), and it is the configuration in which
Z-bias lives.

**The free diagnostic, and the lab is already running it by accident.** Step 2 above — report
with and without — is what the 2026-11-12/13 and 2026-11-13/14 nightlies did when they read
each score raw and controlled. Under this paper that practice is **correct and is the
recommended procedure**, which is worth recording because the lab has been treating the
controlled number as *the* number and the raw one as superseded. The three cells:

- **Raw ≈ controlled** → the control is not doing anything; Z-bias is not a concern; the
  reading stands on its own. (Nothing in the lab's record is in this cell, which is itself
  informative.)
- **Controlled much smaller** → consistent with the control removing a real confound, which is
  the reading the lab has taken (`amihud126` `+1036 → −99`; log `P` itself `−1021 → +0.1`).
  The calibration of 2026-11-13/14 — where information-free noise carrying the object's
  loadings went to ≈0 and log `P` itself went to ≈0 — is strong evidence for this reading in
  those specific cases, and this paper does not weaken it.
- **Controlled larger** → `rank_stability` (`+212 → +483`) and 12−1 momentum on the full
  window. **This is the cell this paper and `#444` and the companion note all speak to, and
  none of the three says it is corroboration.** Under Z-bias logic a control can move a
  reading in either direction while making it worse; under the companion note's `X₃` case it
  adds variance; under `#444`'s precision transform it can genuinely raise standardised
  signal. **Three live explanations, one of which is "worse", and the lab's current practice
  of reading it as a strengthened result is the one reading all three rule out.**

**The rule to adopt, stated so it can be pre-registered.** Before admitting a variable to the
mandatory joint control:

> State whether the variable is believed to be a cause of the **forward return** by some path
> other than through the score. If the answer is no, it is an instrument for the lab's purpose
> and **adjusting for it amplifies whatever unmeasured contamination remains** — report the
> reading **both ways** and treat a disagreement as unresolved rather than as the controlled
> number being right.

**Why this does not amount to "stop controlling".** The lab's log-`P` control was not admitted
on a hunch; it was admitted because Amihud is proportional to `1/price` and the stored level
carries a known engine artifact — i.e. log `P` is a **proxy for an unmeasured common cause** of
both the score and the measured return, which is step 4 of the modified disjunctive cause
criterion and an *inclusion*, not an exclusion. The honest summary is: **the log-`P` control
is well-motivated under the criterion and the calibration supports it; `vol126`'s outcome-side
justification has never been written down; and the direction of the control's effect is not
evidence about either.**

**One structural caution specific to this panel, and it bites hard.** Every interpretable
theorem here requires a **clean** instrument — no direct arrow to the outcome, no unmeasured
common cause with the outcome. On a point-in-time panel of nine large-cap national indices,
essentially no observable is clean in that sense: `vol126`, log `P`, liquidity tier and region
are all plausibly related to forward returns by paths that do not go through any particular
score, and index admission is a selection that touches all of them
(`notes/2026-11-06-index-membership-is-not-an-information-free-selection.md`). So the lab is in
the **near-instrument** regime, where the paper's own verdict is that the clean theorems are of
little practical use without knowing the size of the direct effect. **The usable content for
this lab is therefore the mechanism, the 68% figure as a statement about how common the bad
case is in an unstructured parameter space, and the with-and-without procedure — not the
monotonicity conditions as a test to run.**

**Cost profile: free.** It is a reporting discipline and a classification question, not a
computation.

**Anti-candidate it rules out.** Any proposal of the form *"add more controls to make the
no-unmeasured-confounding assumption more plausible"*. The paper's opening target is exactly
that belief, and the lab should not reach for a wider control set as a response to a suspect
reading. `#444` says the same thing about balance tests from the power side; this says it
about point estimates from the bias side. **Widening the conditioning set is not a free
robustness move in either object.**

## Related

- `notes/2026-11-15-the-modified-disjunctive-cause-criterion.md` (same session) — step 3 of
  that criterion is this paper's result; the criterion is where the decision rule lives.
- `notes/2026-11-15-covariate-selection-for-the-propensity-score.md` (same session) — the same
  covariate type priced in variance rather than bias, and the simulation whose generative
  models this paper shows satisfy its corollaries.
- `notes/2026-11-14-sparse-alternatives-and-the-precision-transformed-test.md` — `#444`'s
  "widening the covariate list weakens the test", the test-side twin of this note's
  estimate-side ceiling, and the precision-transform mechanism that is the competing
  explanation for a control raising a reading.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` — why no
  observable on this panel is a clean instrument.
- `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — carries the
  selection-space / return-space two-by-two (`#446`); the with-and-without procedure is a
  third reading of the same object.

## Channels

Recorded because it cost a channel hunt and because it is a reusable substitution. The
**applied** source for this mechanism — Myers et al., *Effects of Adjusting for Instrumental
Variables on Bias and Precision of Effect Estimates*, **Am J Epidemiol** 174(11), 1213–1222
(2011), `10.1093/aje/kwr364`, **261** Crossref citations checked 2026-11-15 — was **not
obtained**. Europe PMC lists it as `inEPMC: Y` but `isOpenAccess: N`, so `fullTextXML`
returns **HTTP 500**; NCBI's `efetch` returns metadata with the explicit note *"The publisher
of this article does not allow downloading of the full text in XML form"*; and
`pmc.ncbi.nlm.nih.gov` answers an automated client with **HTTP 200 and a 21 KB
Material-design challenge shell** — identical in byte size for two different articles, which
is the cheap tell. A web search surfaced no mirror. Per `research/README.md`'s 2026-10-15
lesson, the budget went to a **different source for the same mechanism** rather than a third
channel, and the substitution was an upgrade: this paper is the general theorem behind that
simulation, re-reads its exact generative models, and shows they satisfy its corollaries — so
the applied finding is carried here **through the theorem that contains it**, not at second
hand. Its abstract was read from the NCBI `efetch` deposit; nothing in this note rests on it.
The one thing the substitution loses is **magnitude** — Myers et al. report how large the
amplification is in finite samples, and this paper is explicit that it makes no magnitude
claims. If a later session needs the size rather than the direction, that paper is the named
pointer and its channels are the ones listed above.
