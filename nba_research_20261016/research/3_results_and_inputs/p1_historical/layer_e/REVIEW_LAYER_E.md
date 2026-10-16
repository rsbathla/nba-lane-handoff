# Layer E independent review (spec v1.1)

**Verdict: PASS WITH FIXES.** Every headline number I recomputed matches the build exactly. Nothing leaks a same-day or later game into an as-of value. I found four small defects in rules and labels (D1-D4). None of them changes the sign of a headline. One reading caveat (C1) bears on how the headlines are read.

Reviewer code lives in /tmp/review (c1*.py, tg.py, c1d*.py, sens.py, c3.py to c6.py). It is written from scratch from the raw inputs: NBA.com intake JSON, the Codex tracking CSVs plus the 2026-10-13 backfill and the quarantine files, BigDataBall (BDB) play-by-play CSVs, and the BDB DFS feed. It does not import any build script.

## 1. Recomputations

### 1a. Upside threshold and upside flag
- Qualifying players: 560 (build 560). Qualifying player-games: 51,859 (build 51,859). All have a `002` game ID and MIN > 0.
- 10 random players: the 75th-percentile threshold and the upside count match exactly for all 10.

| Player | Games | My p75 | Build p75 | Upside games (mine / build) |
|---|---|---|---|---|
| Christie | 155 | 26.25 | 26.25 | 39 / 39 |
| Mogbo | 103 | 19.625 | 19.625 | 26 / 26 |
| Holmes II | 25 | 11.75 | 11.75 | 7 / 7 |
| C. Williams | 117 | 20.5 | 20.5 | 30 / 30 |
| Umude | 24 | 4.1875 | 4.1875 | 6 / 6 |
| Simons | 125 | 37.25 | 37.25 | 32 / 32 |
| Knueppel | 81 | 39.75 | 39.75 | 21 / 21 |
| C. Joseph | 50 | 13.6875 | 13.6875 | 13 / 13 |
| Z. Collins | 74 | 23.25 | 23.25 | 20 / 20 |
| Houstan | 76 | 11.6875 | 11.6875 | 19 / 19 |

- Checked over all rows: the largest p75 difference is 0.0, and 0 of 51,859 upside flags differ.

### 1b. DK points
- 200 random rows from the frame, scored with DK Classic rules including the double-double (+1.5) and triple-double (+3) bonuses. The sample held 15 double-doubles and 2 triple-doubles.
- My DK points differ from the build's in 0 of 200 rows.
- They differ from BDB's DK points in 2 of 200 rows (Moody 0022500037, Jokić 0022500054). Both look like stat corrections and both are in dk_mismatches.csv.
- Across the full frame there are 256 mismatches with BDB out of 51,858 matched rows (0.49%).
- Among the 284 triple-doubles, 274 match BDB with both bonuses added (+4.5 total). None match a "triple-double replaces double-double" rule, so the scoring rule is right.

### 1c. Opponent volume allowed per 100 possessions, and rank
How I built it:
- **Team-game totals.** Box FTA. cs3 from tracking, with the quarantine rule and the v1.1 scaling: scale up when clean players cover at least 70% of team FGA, otherwise leave the team-game out; 258 team-games fall below 70%. Rim counted directly from play-by-play at team level (not via player matching): 2PA at 3 ft or less, with 2025-26 distances rounded half-up as the build does.
- **As-of values.** Each defense, using only its games strictly before the date, divided by opponent POSS. A rank exists only when the team has at least 10 games.

| Season | Date | Types | Teams with a rank | Largest value difference | Rank mismatches | Same bottom 5 |
|---|---|---|---|---|---|---|
| 2024-25 | 2024-11-03 | cs3, rim, ftr | 0 | 0 | 0 | yes |
| 2024-25 | 2024-12-04 | cs3, rim, ftr | 30 | 0 | 0 | yes |
| 2024-25 | 2025-03-13 | cs3, rim, ftr | 30 | 0 | 0 | yes |
| 2025-26 | 2025-11-02 | cs3, rim, ftr | 0 | 0 | 0 | yes |
| 2025-26 | 2026-01-20 | cs3, rim, ftr | 30 | 0 | 0 | yes |
| 2025-26 | 2026-04-12 | cs3, rim, ftr | 30 | 0 | 0 | yes |

- I then ran all 327 dates × 3 types (981 date-type pairs) against opp_ranks.parquet: 0 rank mismatches.
- My rim count comes straight from team-level play-by-play and still matches exactly, so the build's player-name matching drops no rim shots.

### 1d. Pooled headline counts (both seasons)
Each cell is present games (upside games) / absent games (upside games), then the difference in points.

| Row | 2024-25 mine | 2025-26 mine | Build |
|---|---|---|---|
| rim vol_szn_b5 opp | 3146 (874) / 16170 (4015), +2.951 | 3825 (1126) / 18964 (4937), +3.404 | identical |
| wo vol_szn_b5 opp | 3739 (1094) / 18753 (4815), +3.583 | 3771 (1107) / 19018 (4956), +3.296 | identical |
| cs3 vol_szn_b10 cross | 2338 (667) / 19569 (5124), +2.344 | 2436 (701) / 20231 (5342), +2.372 | identical |
| ml_lt10 ml_b5 opp | 3636 (1063) / 18856 (4846), +3.535 | 3761 (1122) / 19028 (4941), +3.865 | identical |

- The cs3 cross row needed my own pregame share and tertile leg. It matches leg_cs3 on 100% of rows, and the share's largest difference is 0.0. The cs3 shares include the previous-season fallback.
- The ml_lt10 composite is recomputed from tracking: L7 and season FG% and FGA per game, mean of the four ranks, re-ranked.
- Per player, the counts for rim and wo vol_szn_b5 and ml_lt10 ml_b5 match players_wide on all 560 players.

### 1e. Opponent DRtg bottom-5 control
DRtg is recomputed from points allowed per 100 possessions, season to date, with at least 10 games.

| Condition | 2024-25 (upside % present vs absent) | 2025-26 (upside % present vs absent) |
|---|---|---|
| DRtg bottom 5 | 30.2 vs 25.5 (n = 3738) | 31.2 vs 25.7 (n = 3809) |
| DRtg bottom 10 | 28.7 vs 25.1 | 29.5 vs 25.1 |

- The bottom-5 rows match the build (30.2 vs 25.5; 31.2 vs 25.7).
- Using box opponent points instead of DEF_RATING × POSS moves each number by 0.1 at most.

## 2. Look-ahead checks
- **Opponent state (05_opp.py:58).** `searchsorted(side='left')` gives games strictly before the date. My independent strictly-before computation matches exactly on every date, so no same-day game gets in. The L10 and L7 windows use `okpos < i`, also strictly before. The adjusted-rate prior (05_opp.py:29-34) is a cumulative sum minus the current game.
- **Player shares (06_legs.py:18).** Cumulative sum minus the current game, within player and season. My shares, computed strictly before the game, match with a largest difference of 0.0.
- **Previous-season fallback (06_legs.py:20-24).** It uses only 2024-25 totals for 2025-26 games, and only when the player has fewer than 5 earlier games and at least 10 games the previous season. There is no fallback in 2024-25, so those legs are unavailable, as the spec says. Correct.
- **Tertile cutoffs (06_legs.py:35).** Each player's share value is pregame: his first game on or after D has no games of his between D and that game. But who is in the population depends on the future: a player is included only if he plays again on or after D. Players who never play again are left out. See D1.
- **Upside threshold.** It uses both seasons, so 2024-25 labels depend on 2025-26 games. The spec fixes the outcome this way, and it is not a leak in any condition. It is noted here so nobody reads it as one.

## 3. Per-player carry-over
Population: players_wide rows with kind = opp, cond in vol/eff_szn_b5/b10 or ml_b5/b10, and at least 5 present and 5 absent games in each season. That is 17,959 rows out of 32,480.

| 2024-25 difference | Rows | Positive in 2025-26 | At least 0 in 2025-26 | Mean 2025-26 difference |
|---|---|---|---|---|
| +10 or more | 4,744 | 51.3% | 53.2% | +1.71 |
| -10 or less | 3,992 | 52.0% | 53.5% | +1.49 |
| between | 9,223 | 52.4% | 54.0% | +1.75 |

- Base rate (positive in 2025-26, all rows): 52.0%. Correlation between the two seasons' differences: 0.007.
- The claim (about 51% vs about 52%) is confirmed.
- Across all of players_wide, "lead" (13,540 opp rows) is about as common as "negative both seasons" (13,378), which also fits noise.

## 4. Spec rules
- **2024-25 play-by-play types excluded after 2025-03-24.** The last play-by-play date is 2025-03-24. The 157 games with no file are all after that date, and no frame row after it has pbp_ok. rim 2024-25 counts 19,316 games, exactly the ranked games through 2025-03-24; the 3,176 later games are left out. 2025-26 has play-by-play for all 1,230 games. Correct.
- **Rank only once a team has 10 games.** The n_games used for eligibility matches my count of the team's earlier games on every date checked. Teams below 10 get NaN, and those games are left out of the counts. Correct, apart from D2.
- **Bottom 5 = rank 26-30, with 30 = most allowed.** Ranks are ascending, so 30 = most attempts or highest eFG allowed. Thresholds are `>= 26` and `>= 21` (07_count.py:11). Correct.
- **Heaves.** BDB `heave` is its own event_type, so the `shot` filter leaves it out. Correct.

## 5. Defects and fixes

**D1. Tertile and usage-tier population uses future appearances** (06_legs.py:35 and 06_legs.py:48)
- The cutoff on date D is taken over players who have any game on or after D. Who is counted therefore depends on whether a player appears again later. The spec says "players at his position group on that date".
- Fix: take the population from players who play on D, e.g. `st = fs[fs.date == D]`. Or use every player's as-of state at D, whatever his future games.
- Effect on the cs3 leg:
  - Slate population: 94.8% of leg flags agree with the build. The cs3 vol_szn_b10 cross moves from +2.34/+2.37 to +1.98/+2.58, and cs3 leg-alone moves from -1.28/-0.69 to -1.68/-0.48.
  - As-of roster population: 98.1% agree, and the cross moves to +2.56/+2.19.
- Signs do not change, but the "strong in type" leg and the "player leg restated" labels are sensitive to this choice, so pin it down in the spec.

**D2. Ranks are taken among eligible teams only, not across all 30** (05_opp.py:106-107 and 05_opp.py:111-113; 10_controls.py:11-12 the same)
- On the 10 transition dates (2024-11-09 to 11-13 and 2025-11-08 to 11-12), fewer than 30 teams have 10 games. The top rank is then fewer than 30, so `>= 26` flags none or only a few teams (0 teams with 25 eligible).
- This affects 1,058 of 45,281 ranked qualifying player-games.
- Fix: rank every team that has a value, then mask: `st[c].groupby([st.season, st.date]).rank().where(st.elig)`.
- Effect: rim b5 moves from +2.95/+3.40 to +3.01/+3.43, wo from +3.58/+3.30 to +3.44/+3.27, cs3 vol b5 from +1.49/+0.73 to +1.27/+0.73. Small.

**D3. A zero difference is labelled "reversed"** (09_players.py:14)
- `np.sign(d1) != np.sign(d2)` is true when one difference is exactly 0. This happens on 1,945 rows; the spec defines reversed as opposite signs.
- Fix: use `(d1 * d2) < 0` for reversed, and send zero differences to "other" (or to "flat" when within ±5).

**D4. Position tie-break is arbitrary** (01_frame.py:32)
- `value_counts().index[0]` with tied counts gives an unspecified order. Three qualifying players are exact ties: 1630171 SG/SF 58-58, 1631111 PG/SG 14-14, 1642852 PF/C 39-39.
- Fix: a deterministic tie-break, such as the position in his most recent game, written into the spec.

**Minor**
- 6 rank values are tied and come out as x.5 (`method='average'`), so a tie at 25.5 is not bottom 5. This is negligible. Use `method='min'` or `'max'` if that is wanted, and state which.
- 09_players.py gives the "lead" status to kind = leg rows (144). Spec §8 defines leads only for opponent or cross rows, so filter `kind != 'leg'` in any lead list.
- 09_players.py:27 adds a label the spec does not have: "player leg present nearly every game". It is used when leg-alone is undefined, and covers 3,448 of 3,817 cross leads. This is reasonable, but add it to the spec changelog.

## 6. Caveat on reading the headlines (not a code defect)

**C1. General weak defense explains most of the type-specific bottom-5 headlines.**
- The opponent DRtg bottom-5 difference, +4.7 / +5.5, is as large as or larger than nearly every type-specific bottom-5 row: rim +2.95/+3.40, wo +3.58/+3.30, ml_lt10 +3.54/+3.87. Only lt10 2025-26 (+5.13) and trans 2025-26 (+5.02) are close or above.
- Between 58% and 83% of the bottom-5 games for those types are also against a DRtg bottom-10 opponent.
- In controls.csv, restricted to opponents outside the DRtg bottom 10, most differences fall to about 0 to 2 points, or flip sign. For example, wo is +1.5 / -0.4, cs3 is -0.6 / -3.9, and ml_lt10 is +0.6 / +3.3.
- Any headline that names a type-specific funnel should sit next to the DRtg control.
