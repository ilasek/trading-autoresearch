## Assessment against the pre-registered criteria

The five criteria were fixed in the plan before any trial was re-scored. Numbers are from the tables below.

1. **Hindsight neutralised — FAILED.** The hard-coded list of today's 15 biggest 2010–23 winners passes every v2 gate (validation Sharpe 1.12, 100th null percentile). Point-in-time membership cannot help when the hindsight names were index members throughout the scored window, and a random-selection null cannot flag a selection that really was the best. Survivorship is fixed *in the universe*; hindsight *in the candidate's code* needs its own guard before v2 is switched on (e.g. refuse instrument literals in candidate source, as the static check already refuses membership reads). Random selection lands at the 8th–26th null percentile: no false positive, though one realisation is noisy.
2. **The bias is measurable and material — PASSED.** The current champion (#98) goes from validation Sharpe 1.27 / CAGR 24% (v1) to 0.19 / 2% when it ranks only point-in-time members (ported). That is the 0th percentile of its own random-selection null and below the equal-weight pool (IR −0.30). Every champion since #35 lands at 0.36–0.48 ported, at the 29th–43rd null percentile. For scale, the same correction cost trading-agent 19.5 pp of TWR.
3. **Signal survives where theory expects it — PARTLY.** Plain 12-1 momentum keeps a positive excess over the pool on a point-in-time universe (IR +0.28, 82nd null percentile) but does not clear the 90% gate. The gate is not prohibitive: 27 of 104 historical trials clear it under V2m, mostly portfolio-learning, seasonality and lead-lag work. None of the ones that clear it are the momentum lineage the lab optimised.
4. **Consistency improves — MOSTLY.**
   - The train−validation gap turns from the implausible −0.08 (validation *better* than train, a symptom of the flattering universe) to +0.11.
   - Across the 8 champions, validation→holdout rank agreement rises from −0.33 (v1) to +0.54 (ported). With n = 8 that is weak evidence.
   - v2 reorders the search: rank agreement of validation Sharpe v1 vs V2m is only +0.43, and 39 trials pass the 90% null only under v1.
5. **Residual bias quantified — PASSED, with a limit.** Yahoo prices 89–97% of point-in-time members over validation (2018–23), but only 40–66% over 1996–2008. Validation-based decisions therefore rest on well-covered years, while train numbers remain optimistic. The planned sensitivity re-run restricted to ≥ 80%-coverage years was not needed for validation (every validation year qualifies) and was not run for train.

**Verdict.** v2 is a step in the right direction. It removes a large, measured bias that v1 cannot see, the null gate is calibrated (random selection fails it, genuine cross-sectional structure passes), and splits that disagreed under v1 agree better. It is **not ready to switch on as is**, because of criterion 1. Recommended order:

1. Add a static guard against hard-coded instrument lists.
2. Cut over with a fresh deflated-Sharpe history. v1 trial Sharpes are not on the v2 scale: pooling them would inflate the variance term and the bar.
3. Re-seat the champion by running the best V2m/V2p candidates through `run_experiment.py` under v2.

**Caveats.**
- V2m is an adaptation for code written before v2: a new index joiner becomes rankable only once its lookback fills with in-index prices. On the momentum lineage the exact port (V2p) scores *lower* than V2m in 7 of 8 cases, so V2m is not the pessimistic bound.
- One trial (#26) is rebuilt from a commit whose file already held the next trial's fix (it re-scores at #27's recorded 1.052). The other 103 reproduce to ±0.001.
- Holdout numbers under U (today's members eligible throughout) are inflated by 2024–26 index joiners; they are shown only to expose that effect.
