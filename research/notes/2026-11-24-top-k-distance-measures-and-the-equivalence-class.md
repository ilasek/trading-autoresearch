---
title: "Measuring agreement between two TOP-K lists — the four-case Kendall distance with a penalty parameter, the footrule with a location parameter that IS a metric, the prefix-weighted intersection metric that is provably NOT equivalent to either, and why 'which measure' matters far less than 'which equivalence class'"
authors: Fagin, Kumar, Sivakumar
year: 2003
venue: "SIAM Journal on Discrete Mathematics 17(1), 134–160 (preliminary version in ACM-SIAM SODA 2003, 28–36). Peer-reviewed; SIAM journal, tier 1 for the field."
url: https://doi.org/10.1137/S0895480102412856
citations: "555 (Crossref `is-referenced-by-count`, checked 2026-11-24); 1116 (Semantic Scholar by DOI, same date). The companion generalisation to rankings WITH TIES — Fagin, Kumar, Mahdian, Sivakumar & Vee, 'Comparing Partial Rankings', SIAM J. Discrete Math. (2006), `10.1137/05063088X` — carries 104 (Crossref, same date) and was NOT obtained; it is named here as a pointer only."
sample_period: "n/a — theorems about distance measures. The illustration uses top-50 result lists from seven web search engines over 750 user queries, collected ~2002. No market data anywhere."
markets: "None. The items ranked are web pages."
tier: "A. Peer-reviewed SIAM journal, heavily cited, every claim is a stated proposition or theorem with a proof in the text, and the central results are negative/structural (what is NOT a metric, what is NOT in the equivalence class) rather than empirical, so there is no sample to decay. Single-domain illustration; the transfer to this lab is by construction."
validation_overlap: false
published_post_2018: false
read: "Full text, the typeset SIAM article (27 pp. of journal pagination; `file` reported '8 page(s)', which is the usual unreliable page count), 353 KB PDF from `www.biz.uiowa.edu/faculty/nstreet/Fagin03.pdf`, HTTP 200 on the first request, `pdftotext -layout` → 105 KB of text, 480 instances of `\" the \"`, no ASCII shift. Definitions, Theorem 5.1/5.3, Propositions 3.7/3.8/7.2/7.3 and section 9 read closely; the longer counting proofs were skimmed. The extraction renders the superscript/subscript parameters as `F (#)` and `K (p)`, so the parameter names in this note are written out in words where there is any risk of ambiguity."
access_note: "A **course/faculty page at a business school** (`biz.uiowa.edu/faculty/<name>/<Author><Year>.pdf`) served the complete typeset SIAM article on the first request. This extends the 2026-09-18 faculty-page lesson in a specific direction worth copying: a *teaching* page's reading list hosts other people's canonical papers under an `<Author><Year>.pdf` filename, so for a famous methods paper, a search restricted to `.edu` faculty directories is a first-try channel. IBM Research's own publication pages (`research.ibm.com/publications/<slug>`) hold records with muddled metadata (one lists this paper as SODA 1998) and no file."
---

## Why this source is here

The [2026-11-23] entry's carry-forward was explicit: *"the relevant property of an aggregator is how
stable its top-K set is, not how well it orders the tail. A source that only compares full-ranking
distances is weaker here than one that reports top-K agreement."* This paper is that source. It is
about nothing except how to measure the distance between two top-K lists, by the same IBM Almaden
group whose rank-aggregation paper is the companion note, and it was written because the aggregation
work needed it.

It also answers a question the lab has been settling by convention rather than by argument. The lab's
decorrelation screen compares two candidate scores by **rank correlation over the whole
cross-section** (`learnings.md`: an inter-signal ensemble killed for free at rank correlation 0.89),
and groups family leads into mechanisms by the **correlation of their active returns** (≥ 0.5 = one
mechanism). Neither of those is a measure of top-K agreement, and this paper proves that the
difference is not cosmetic: the prefix-weighted top-K measure is **not** in the same equivalence
class as the Kendall/footrule family, so it is a genuinely different measurement and cannot be
inferred from a full-ranking correlation.

## Mechanism

**The object.** A *top k list* is a ranking of a k-element subset of a universe, with everything
unranked implicitly below everything ranked. Two top-K lists usually disagree about **membership**
as well as about order, which is what breaks the textbook measures: Kendall's tau and Spearman's
footrule "deal only with comparing one permutation against another over the same elements". The naive
fix — set intersection, or symmetric difference — is rejected with a one-line counterexample: "two
top 10 lists that are reverses of each other would be declared to be very close."

**Measure family 1: Kendall distance with a penalty parameter `p`.** Enumerate all unordered pairs
{i,j} drawn from the *union* of the two lists' domains, and charge each pair by case:

1. **Both items in both lists** — 0 if the two lists agree on the order, 1 if they disagree.
2. **Both in one list, exactly one in the other** — the one that appears in the second list is known
   to be ahead there, so charge 0 or 1 accordingly.
3. **i in one list only, j in the other list only** — charge 1 (each list puts "its" item ahead).
4. **Both in one list, neither in the other** — a **special pair**: the second list expresses no
   opinion. Charge `p`. This is "the only case where there is really an option as to what the penalty
   should be."

`K^(p)` is the sum. `p = 0` is the *optimistic* convention and equals `K_min`, the minimum Kendall
distance over all ways of extending both lists to permutations of the union. `p = 1/2` is the
*neutral* convention and equals `K_avg`, the expectation over all such extensions (also equal to the
Hausdorff version). **`K^(p)` is not a metric for any choice of `p`** — a three-list counterexample
with k = 2 breaks the triangle inequality.

**Measure family 2: footrule with a location parameter.** Place every missing element of each list at
a notional position `ℓ > k`, then take the ordinary footrule (L1) distance. `ℓ = k + 1` is "a natural
choice" and is written `F*`. Two facts make this the practical member of the family:

- **`F^(ℓ)` IS a metric, for every `ℓ`** — because it is literally the L1 distance between two
  n-vectors (actual rank where present, `ℓ` where absent), so the triangle inequality is inherited
  from the L1 norm. This is the one measure in the paper you can treat as a true distance without
  qualification.
- The min/avg/Hausdorff versions of the footrule all coincide (`F_min = F_avg = F_Haus`), and that
  common value is `F^(ℓ)` with the *dynamic* choice `ℓ = (3k − z + 1)/2`, where `z` is the number of
  items common to both lists — i.e. "placing the missing elements at an average location". None of
  these is a metric.

**Main result: the big equivalence class.** Two measures are *equivalent* if each bounds the other
within positive constant multiples (independent of k). Theorem 5.1: `K_min`, `K_avg`, `K_Haus`,
`K^(p)` for every `p`, `F_min`, `F_avg`, `F_Haus` and `F^(ℓ)` for every `ℓ` are **all in one
equivalence class**, with explicit constants in Theorem 5.3 — e.g. `K_min ≤ F_min ≤ 2·K_min` (via
Diaconis–Graham), `F* ≤ F_min ≤ 2·F*`, and `K^(p) ≤ K^(p′) ≤ ((1+p′)/(1+p))·K^(p)` for `p ≤ p′`. Two
consequences, both practical:

- Since one member (`F^(ℓ)`) is a metric, every other member is a **near metric** — it satisfies a
  relaxed polygonal inequality `d(x,z) ≤ c·(d(x,x₁) + … + d(x_{n−1},z))` for a fixed `c`. The paper
  proves the surprising equivalence of the two notions of "near metric" (metric boundedness ⟺
  relaxed polygonal inequality).
- **The only choice that matters is which equivalence class, not which measure.** "Up to constant
  factors (that do not depend on k), all distance measures in an equivalence class are essentially
  the same." The authors' own default is this class.

**The measure that is NOT in that class, and it is the one the carry-forward asked for.** Define, for
each prefix length `i = 1…k`, `δ_i = |D_{τ₁(i)} Δ D_{τ₂(i)}| / (2i)` — the normalised symmetric
difference between the two lists' **top-i sets** — and let the **intersection metric** `δ^(w)` be the
average of `δ_i` over `i = 1…k`. Then:

- `δ^(w)` **is a metric** (Proposition 7.2), lies in [0,1], and equals 1 exactly when the two lists
  are disjoint. Any convex combination of the `δ_i` with strictly positive coefficients is also a
  metric, so the prefix weighting can be chosen deliberately.
- `δ^(w)` is **not** in the big equivalence class, even after normalising everything (Proposition
  7.3): on a top-k list versus its own cyclic shift, the normalised footrule is Θ(1/k) while `δ^(w)`
  is Θ(ln k / k), so no constant multiples can bound one by the other.

The intuition for why this matters is in the construction: averaging over prefixes puts weight
`1/(2i)` on the disagreement at depth `i`, so `δ^(w)` is dominated by the **very top** of the list,
whereas the Kendall/footrule family weights a transposition the same wherever it occurs. Moving an
item from rank 1 to rank 2 is nearly free in the big equivalence class and expensive in `δ^(w)`.

**One further measure worth knowing because it handles TIES.** Goodman & Kruskal's gamma: let `C` be
the set of pairs on which *both* lists express an opinion (explicitly or implicitly) — exactly cases
1–3 above, excluding the special pairs — and let gamma be the **fraction of `C` on which the two
lists disagree**. It discards the special pairs rather than pricing them, which is why it is not in
the big equivalence class either, and it was originally defined for **bucket orders** (total orders
with ties), which is the structure a quantised score produces. The full treatment of ties is the
companion 2006 paper, named in the frontmatter and not obtained.

## Construction recipe

All of this is arithmetic on two rank vectors; nothing is estimated.

1. **Represent each lead's selection at date `t` as a top-K list** — the names it ranks, in order,
   with the rest implicitly below.
2. **To ask "do these two leads agree overall?"** use any member of the big equivalence class and do
   not agonise: `F*` (place each missing name at position K+1 and take the L1 distance between the
   two rank vectors) is three lines, is a genuine metric, and normalising by its maximum puts it in
   [0,1]. If pairwise reasoning is wanted, use `K^(1/2)` (the neutral convention: charge 1/2 for a
   pair that only one list ranks).
3. **To ask "do these two leads agree about the NAMES AT THE TOP?"** — the question `#514` and the
   [2026-11-23] carry-forward actually pose — compute `δ^(w)`: for `i = 1…K`, the size of the
   symmetric difference of the two top-`i` sets divided by `2i`, averaged over `i`. One `numpy`
   cumulative-membership computation per pair of leads per date. **Report this separately from step
   2; Proposition 7.3 says it cannot be deduced from it.**
4. **To ask "how much does one lead's own top-K move between rebalances?"** apply step 3 to the same
   lead at `t` and `t+1`. That is a top-weighted turnover forecast and it is the right companion to
   `#515`'s rank autocorrelation, which is a full-ranking measure and therefore in the wrong
   equivalence class for a membership question.
5. **To group leads into mechanisms** build the full `δ^(w)` (or `F*`) matrix across leads and read
   it as a distance matrix. Metric status (step 2's `F*`, step 3's `δ^(w)`) or near-metric status
   (everything else) is what licenses transitive inference — see Robustness.
6. **Choose the prefix weights on purpose if the book's breadth is known.** Since any strictly
   positive convex combination of the `δ_i` is a metric, a book that holds K names can weight
   `i ≤ K` and ignore deeper prefixes, instead of inheriting the `1/i` weighting by default.

## Robustness evidence (qualitative only)

- The content is theorems; there is no sample. The equivalence-class constants in Theorem 5.3 are
  explicitly "not tight", which matters only if one wants to convert between measures numerically,
  and the paper says so rather than leaving it to be discovered.
- The measures were **independently adopted and used by other groups** for the purpose this note
  proposes — the paper records two: a search-index pruning study verified its hypothesis "that their
  pruning technique would have only small effects on the top k list for moderate values of k" using
  one of these measures, and a PageRank-approximation study used one to evaluate an approximate
  ranking against the exact one. Both are the same shape of question as "did this change to the
  construction change the book?", which is a question the lab asks constantly and currently answers
  by eyeballing holdings overlap.
- **The illustration is the most transferable part, and it is a diagnosis of SHARED INPUTS between
  rankers that look independent.** Over 750 real queries, the pairwise normalised `K_min` distances
  between seven search engines' top-50 lists separated into a clear structure: two pairs were far
  closer to each other than to anything else, two engines were far from everything, and the paper
  then matched that structure to the publicly documented data-supply alliances — two of the close
  engines drew crawl data from the same supplier, as did a third that came out only *moderately*
  close, which the authors read as "while they all use crawl data from Inktomi, HotBot probably uses
  a ranking function quite different". The two distant engines were the two running their own
  crawling, indexing and ranking.
- **And the near-metric property did real work there**, which is the paper's observation (4): because
  the measure obeys a relaxed triangle inequality, "exploiting the transitivity of closeness for a
  near metric" let them infer relative distances between the *underlying data services* that were
  never directly measured. That is the formal license for the kind of transitive reasoning the lab
  does informally when it decides two leads are "the same bet".
- No dated performance of any kind appears in this paper, so nothing had to be withheld under the
  anti-lookahead policy.

## Implementability here

**Free, and it upgrades a screen the lab already runs.** No returns, no costs, no trial, no holdout.
The inputs are stored lead scores. The deliverable is two numbers per pair of leads per date
(`F*` or `K^(1/2)` for overall agreement; `δ^(w)` for top-K agreement), and the finding is whatever
gap appears between them.

**The sharpest use, stated as a claim the lab can falsify cheaply.** The lab's screens are
full-cross-section measures: rank correlation between scores, and return correlation between
finished books. Proposition 7.3 says a top-weighted membership measure lives in a different
equivalence class, so **two leads can rank-correlate at 0.89 and still select substantially different
top-K sets, and two leads can rank-correlate modestly and select nearly the same top-K set.** Which
of those is happening is exactly what decides whether a combination is worth building (`#514`), and
it is one `numpy` pass away. If the `δ^(w)` matrix reproduces the rank-correlation ordering of the
leads, the lab's existing screen is sufficient and this is closed for free; if it does not, the lab
has been grouping mechanisms on the wrong statistic.

**Runtime.** `δ^(w)` over the full eligible panel is a cumulative set-membership computation —
`O(n)` per prefix with a running count, so `O(n)` total per pair of lists with the obvious
implementation, or `O(K)` if restricted to the book's own depth. Nothing here is a constraint even at
daily frequency; this is diagnostic code, not a strategy.

**The one adaptation to make, and the reason.** Set K to the book's actual selection breadth rather
than to a conventional 10 or 50. The prefix weighting makes `δ^(w)` a statement about the depth
range it covers, and a measure averaged to depth 500 when the book holds 40 names is answering a
question nobody asked.

**Pitfalls.**
- **Do not mix measures across equivalence classes in one comparison.** A table that puts a
  Kendall-family number beside a `δ^(w)` number and treats them as commensurable is making exactly
  the error Proposition 7.3 rules out.
- `K^(p)` and `F_min` are **not metrics**; do not feed them to anything that needs the triangle
  inequality (clustering, embedding, a "distance to the nearest existing mechanism" threshold)
  without noting that only the relaxed inequality holds. `F^(ℓ)` and `δ^(w)` are metrics and are the
  safe choices for that.
- Ties are not handled by this paper. A lead's score is "informative at the top and quantised at the
  bottom" (`#375`), which is a **bucket order**, so pairs inside a tied block need a convention:
  Goodman–Kruskal gamma's (drop pairs on which either list is silent) is the one available here, and
  the proper treatment is the 2006 companion paper, which this folder does not hold.
- Normalisation matters for comparability across dates: the raw measures grow with k and with the
  union size, and the eligible panel's width changes. Use the normalised ([0,1]) versions
  throughout, as the paper does for its own table.

## Related

- `notes/2026-11-24-rank-aggregation-positional-versus-pairwise.md` — Dwork et al. (2001), by two of
  the same authors: the aggregation rules whose outputs this paper measures. The scaled-footrule
  aggregation there and the footrule-with-location-parameter here are the same idea applied to the
  two different problems (building a consensus list; scoring two lists).
- `notes/2026-11-24-when-a-positional-rule-is-the-right-aggregator.md` — Young (1988): the
  local-stability test proposed there produces exactly a pair of top-K lists over overlapping item
  sets, which is the object this paper measures.
- `#514` (`notes/2026-11-23-exposure-matched-blend-comparison-and-the-active-risk-crossover.md`) —
  the free pre-trial screen whose two quantities are name overlap between the mix and the composite
  book, and the composite rank of the mix-only names. This paper is the measurement theory for the
  first of those, and says to use a prefix-weighted metric rather than a raw overlap count.
- `#515` — between-rebalance rank autocorrelation; the full-ranking analogue of the top-weighted
  churn measure in step 4, and in a different equivalence class from it.
- `experiments/learnings.md` — the 0.89 rank-correlation screen and the `leaderboard.json`
  mechanism-grouping rule (active-return correlation ≥ 0.5), both of which are full-cross-section
  measures that this paper says cannot answer a top-K membership question.
