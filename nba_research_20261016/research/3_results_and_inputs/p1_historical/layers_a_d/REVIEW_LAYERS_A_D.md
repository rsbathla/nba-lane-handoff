# Independent review: Layers A to D, sweep, P2

**Verdict: PASS WITH FIXES.** The data and scripts reproduce. The B1/B4 flags, the matrix counts, the sweep counts, the P2 thresholds and the P2 per-player summaries all match my own code exactly. No same-day or future data reaches the A-tier cutoffs, B roles, C tertiles or D ranks. The headline findings hold: absences are the largest pregame lever, they also hold in the forward window, and lines and pace are near flat. Four things must be fixed before the report is circulated:

1. Tables 1 and 2 are stale. They come from the run before the v1.1 fixes and do not match `pooled_ad.csv` or the frame.
2. Verdict item 6 ("no multiplier, conditions saturate") uses a comparison that is biased by construction. A proper 2x2 count does not support it.
3. A11 (rotation spot) leaks tonight's absences.
4. B-layer role holders include players who have already left the team, and players who average only garbage-time minutes.

Reviewer: independent agent, 2026-10-15. Work dir `/tmp/review2`. Inputs: `frame_abcd.parquet`, `teamgames.parquet`, raw BigDataBall team feeds and the NBA.com player logs (read-only). The report was re-read after it changed on disk during the review. Its Verdict and Tables 1 to 5 were unchanged in the version checked.

---

## Check 1. Independent recompute of B1/B4 and of pooled Table 1 rows

**B flags, all rows (own code, `b.py`).** I rebuilt "out" from the appearance list and the team schedule. A player counts as out when he appeared for the team earlier this season, did not appear in this game, and his next appearance is for the same team or there is none. I rebuilt the roles from strictly earlier games: top usage means the highest mean usage among players with 5+ games for the team; same-position starter means the most starts at the player's DK position group.
- B1: 0 value mismatches and 0 NaN-pattern mismatches across all 52,952 rows. This holds when "out" also requires that his most recent appearance before the date was for this team, which is the build's span logic. Read literally, the spec text gives 733 different B1 values and 127 different B4 values. These are traded-away players who never appear again; the build's reading is the sensible one, but the spec should say it.
- B4: 0 mismatches.
- The raw NBA.com logs hold 52,957 regular-season rows; the frame holds 52,952. The 5 missing rows are 0-minute appearances, so they count as "out", which is consistent with the decision.

**30-game sample (`samp.py`).** 8 B4=1, 7 B4=0, 8 B1=1, 7 B1=0. In all 30, the role holder was the correct one from earlier games only (for example, Curry with 39 PG starts against 19 for the next PG), his presence or absence was correct, and his next appearance was for the same team or there was none. My flag matched the build in 30/30. Two cases inside the sample point to a defect (D4): Damion Lee was PHX's "top usage" player (39.5 mean usage over 16 games), and Shaedon Sharpe was the PG/SG "starter" on a 12-12 tie.

**Pooled rows (own counts from the frame) against `pooled_ad.csv` and the report.**

| Row | Mine 2024-25 | Mine 2025-26 | Report Table 1 | Match? |
|---|---|---|---|---|
| B4 same-pos starter out | 1378/3834 = 35.9% vs 20.6% (+15.3) | 1481/3858 = 38.4% vs 21.0% (+17.4) | 1379/3821 36.1% (+15.5); 1476/3840 (+17.5) | **No (stale)** |
| B2 top-assist out | 1527/4243 36.0 vs 23.3 (+12.6) | 1926/5238 36.8 vs 22.9 (+13.9) | same | yes |
| B1 top-usage out | 2096/6396 32.8 vs 23.0 (+9.7) | 2373/6985 34.0 vs 22.9 (+11.1) | same | yes |
| A9 started | 4083/12269 (+14.6) | 3994/12238 (+12.7) | same | yes |
| D1 DRtg bottom 5 | 1141/3784 30.2 vs 25.5 (+4.7) | 1196/3842 31.1 vs 25.7 (+5.4) | 1130/3738 (+4.7); 1187/3809 31.2% (+5.5) | **No (stale)** |
| D1 DRtg bottom 10 | 2178/7597 (+3.6) | 2277/7708 (+4.4) | 2164/7543; 2258/7654 | **No (stale n)** |
| C1 implied total top / mid / bottom | +0.1 / -1.0 / +0.9 | +1.4 / -0.6 / -0.8 | same n and rates | yes |

A full automated comparison of Table 1 against `pooled_ad.csv` found **91 of 152 season cells differ**. Every A tier row differs (A1 to A8 and A12), as do B3, B4, C4 and every D row. All B rows except B3/B4, plus A9, A10, A11, C1, C2, C3, C5 to C11 and the in-game rows, match. The mismatched rows are exactly those that the v1.1 fixes touched (past-only tertile cutoffs; ranks across 30 teams), so Table 1 was not regenerated after v1.1. **Table 2 is stale too.** Every row I checked differs from `pooled_ad.csv` (by=season+A1 tier). For example, "same-position starter out, top tier" is +16.1 (821) / +14.1 (841) in the report against +14.8 (774) / +12.8 (772) in the data, and "started, top tier" is +11.7 (5,551) against +11.6 (5,486). Tables 3, 4 and 5 match the data exactly (Table 4: 36/36 rows).

## Check 2. Look-ahead

| Item | Finding |
|---|---|
| A tertiles (`12_conds_ad.py:25-35`) | Clean. Cutoffs come from each player's entering state for his last game before D (`fs.date<D`), and the value classified is the player's entering value. I recomputed A1 values myself (season-to-date mean of earlier games; previous-season fallback at 10+ games). Max abs diff 0.65, from 1 row with missing usage. Tertile labels on 6 random dates x 5 positions: 0 mismatches. |
| A10 (`:57`) | Clean: shift(1) rolling 5. 0 mismatches against my recompute. |
| **A11 (`:59-67`)** | **Leak.** The rank is taken only among players who are in *this game* and also appeared in the team's previous game; the comment at `:65` admits the approximation. Teammates sitting tonight drop out of the denominator, so a player's rank rises on absence nights. The spec ranks among everyone who appeared in the previous game. My spec version disagrees on 3,809 of 42,286 rows (9%). **All 3,809 are on nights with a teammate out.** The pooled result moves from **-4.2 / -1.4 (build) to -1.7 / +0.3 (spec)**, so A11's sign reverses in 2025-26. Players who missed the team's previous game get NaN. |
| A12 (`:72-73`) | Minor. Salary is pregame, but the tertile pool is the players who *appeared* that date, which conditions the cutoffs on who played. Better: use every DK-listed player on the slate. |
| A2/A4 (`:23-24`, `:38-39`) | Minor spec deviation: there is no previous-season fallback, although the spec says tier facts fall back at 5 or fewer earlier games. |
| B roles (`13_conds_bcd.py:37-51`) | No future data: `y=x[x.date<D]`. **However, see defects D3/D4.** |
| C implied-total tertiles (`szn_t`, `:89-99`) | Clean. Cutoffs come from team-games strictly before D, with 100+ needed. 10 random dates (1,729 rows): 0 mismatches. This differs from spec C1 ("third on the date"), and the v1.1 changelog does not record the change. |
| C4 pace (`:107-115`) | Clean. searchsorted side='left' (strictly earlier), ranked across all 30 teams, hidden under 10 games. |
| D ranks (`14_conds_d.py`) | Clean. D2 on 8 dates x 5 positions (1,480 rows): 0 mismatches. D4/D5 on 8 dates (1,202 rows): 0 mismatches. All use searchsorted 'left' over every season date for every team, so ranks cover all 30 teams and **not only tonight's participants**. D1 (from layer E) matches a possession-weighted DRtg built strictly before D on 7 of 8 dates; one date had 12 rows differ by one rank step, a rounding issue and not a leak. |

## Check 3. Lines

Columns `tfeed` (`13:69-73`): indices 45/46/51/52 = OPENING SPREAD, OPENING TOTAL, CLOSING SPREAD, CLOSING TOTAL, confirmed against the header row in both feeds. **Negative = favourite is confirmed.** Closing spread sign agrees with the moneyline sign in 97.6% of 4,606 team-games, and all 109 disagreements are pick'em lines (|spread| 1.0 to 1.5, ML -102 to -112). Opening spreads sum to 0 within every game.

Implied team total = total/2 - spread/2, worked examples (frame matches raw):

| Game | Team | Open spread | Total | Implied (mine) | Frame |
|---|---|---|---|---|---|
| 0022500001 | OKC | -6.5 | 225.5 | 116.0 | 116.0 |
| 0022500001 | HOU | +6.5 | 225.5 | 109.5 | 109.5 |
| 0022500002 | LAL | -3.5 | 224.5 | 114.0 | 114.0 |
| 0022500003 | NYK / CLE | -4.5 / +4.5 | 227.5 | 116.0 / 111.5 | 116.0 / 111.5 |

**Defect D5 (neutral sites).** `13:75-80`: `drop_duplicates(['GAME_ID','venue'])` keeps only one of the two `venue=='N'` rows, and in teamgames both teams' MATCHUP reads "@". Both teams therefore get the *same* (first-listed) team's spread and implied total. For example, MIA and WAS both show -8.5 / 117.5, and OKC and SAS both show +10.5 "dog8+". This affects 10 games (20 team-games: Paris, Mexico City and NBA Cup knockout games). Impact on the pooled rows is negligible, but one team per game has the wrong sign.

## Check 4. Sweep

- **3 random cells plus 1 Table 3 cell, counted directly from the frame** (`sw.py`). n_p, u_p, n_a and u_a match exactly in both seasons:
  - bottom PG A6=top x D6b_b5: (65,19,1859,478) / (63,16,1946,503)
  - top PF E_wo_vol_b10 x E_ml_lt10_b5: (103,34,1156,326) / (87,31,1365,341)
  - bottom PG A4=top x E_leg_cs3: (102,35,1928,486) / (211,76,1886,463)
  - middle PG B3 x B4: +24.93 / +31.27, as in Table 3
- **108,834 readable:** confirmed (all cells have n_p and n_a of 30+ in both seasons). **14,363 cross leads:** confirmed by recomputing the status from the leg columns. **133 conditions** confirmed; 8,778 pairs.
- **12,842 below vs 2,165 above:** reproduced, but only within the 23,994 cells where both legs are positive in both seasons, and with "below/above in both seasons". The other 8,987 cells are mixed. The report states neither the denominator nor the mixed count.
- **Defect D6 (conclusion-changing).** The "sum of legs" benchmark is biased downward by construction. The cross diff is (both present) against (everything else), and "everything else" contains the games where only one leg is present, which have high upside. So the cross diff is mechanically shrunk against the leg diffs. I recounted the same 23,994 cells as a 2x2 (both / i only / j only / neither, `sw3.py`) and compared r11-r00 with (r10-r00)+(r01-r00). With all four groups at 30+ in both seasons (23,403 cells): **5,023 below additive in both seasons, 6,810 above, 11,570 mixed; median interaction +0.75 / +0.60 points.** The data does not show saturation. It shows noise around additive, if anything slightly super-additive. "Conditions overlap and saturate; they do not stack" is not supported. "The sweep found no reliable multiplier" is.
- **D7 (minor).** 1,934 of the 108,834 readable cells cross an A1 tier condition inside its own A1 tier, where it is always present. They are single-leg restatements (margin NaN), counted as "restates a leg / flat / reversed". Exclude A1_usg_szn_t from the family (130 conditions).
- The cross-lead description holds up: 81% of cross leads have a weaker leg of +2 or less in at least one season, and the median smaller-season n_p is 88. "Often an absence" is weak: only 10.4% of cross leads involve a B condition.

## Check 5. P2

- Thresholds come from the build window only (`17_p2.py:62-65`: quantile over `win=='build'`, 20+ build games). My own recompute: 524 players, 38,292 build games, 12,286 read games, read-window upside rate 30.92% (report 30.9%).
- Per-player summary (own counting with the build's condition definitions, 10+/10+ build and 5+/5+ read): **B layer 927 rows, 504 leads at 74.0% positive, 77 negatives at 66.2%, correlation 0.118. E layer 13,760 rows, 3,172 leads at 52.2%, 2,590 negatives at 48.3%, correlation 0.034.** Exact match with `p2_perplayer_summary.csv` and Table 5.
- Pooled claim: **21 pregame conditions with |build diff| of 3+, 19 same sign.** Confirmed: the reversals are A3 bottom and A5 bottom. Across all 133 pregame conditions, only **96/133 (72%)** kept their sign. The report should state that alongside the cut at 3+.

## Check 6. Verdict section numbers against the data

| Item | Claim | Data | OK? |
|---|---|---|---|
| 1 | B4 20.6 to 35.9 / 21.0 to 38.4; B2 +12.6/+13.9; B5 +12.6/+11.0; B1 +9.7/+11.1 | same | yes (but contradicts the stale Table 1 B4 row, 36.1%) |
| 1 | P2 B4 +15.6 then +21.6; every absence condition lifts more after | +15.63 / +21.57; all six B rise | yes |
| 1 | above-median minutes 63-66% vs 42% | 62.8% / 65.7% vs 42.0% / 42.2% | yes |
| 2 | B5 by tier: bottom/middle +13 to +15, top +7 to +8 | bottom 14.6/13.1, middle 15.1/13.1, top 8.4/6.7 | roughly (top is 6.7 to 8.4) |
| 2 | B4 C +23.9/+20.3, PG +18.7/+21.8 | same | yes |
| 2 | 74% / 66% | 74.0% / 66.2% | yes |
| 3 | started +14.6/+12.7; started 3 of 5 +6.8/+5.8; usage top +2.4/+0.1 | same | yes |
| 3 | prior-10 minutes bottom -7.8 / -7.7 | **-7.7 / -7.7** | minor error |
| 4 | implied-total thirds within 1.4; spread within 1.8; pace -1.4/+9.3; B2B +1.9/+2.3 | same | yes |
| 5 | DRtg b5 +4.7/+5.4; DvP-adj b10 +2.9/+4.8; TO b5 +3.5/+3.7; DRtg forward +4.1 to +6.7 | same | yes |
| 5 | "blocks and FTA allowed near flat" | FTA b5 -0.8 / **+3.9**, blocks b5 +0.8 / +2.5 | overstated: FTA b5 2025-26 is as large as TO b5 |
| 6 | 108,834 / 14,363 / 12,842 vs 2,165 | reproduced | numbers yes; **conclusion not supported (D6)** |
| 7 | 19 of 21; 54.8% vs 48.5%; E 52.2% vs 48.3%, correlation 0.03 | same | yes (add 96/133) |
| Minutes or per-minute | 80/7/13; DRtg b5 DK per minute above median 56/58 vs 48/50 | 80.6/6.9/12.6 and 79.5/6.8/13.7; 55.7/58.2 vs 47.9/49.5 | yes |

---

## Defects and fixes

| # | Severity | Where | Problem | Fix |
|---|---|---|---|---|
| D1 | High (report integrity) | `LAYERS_A_D_REPORT.md` Table 1 and Table 2 | Stale from the run before v1.1: 91/152 Table 1 cells and every Table 2 row checked differ from `pooled_ad.csv`. The Verdict uses the new numbers, so the report contradicts itself (B4 35.9% vs 36.1%; DRtg +5.4 vs +5.5). | Regenerate both tables from `pooled_ad.csv` (by=season and by=season+A1_usg_szn_t) with a script, as layer E did with `11_report_tables.py`, and commit that script. |
| D2 | High (claim) | Report Verdict item 6; `16_sweep.py:29-30, 44-47` | "Below the sum of legs" compares the cross's present-vs-rest diff with single-leg diffs. The rest group includes one-leg games, so the result is biased toward "saturation". A 2x2 count gives 5,023 below vs 6,810 above (median +0.7). | In `16_sweep.py`, also compute `x.T@m` and `(x*u).T@m` to get the i-only, j-only and neither counts. Report the interaction (r11-r00)-(r10-r00)-(r01-r00) with the denominator and the mixed count. Rewrite item 6 as "no reliable multiplier; interactions scatter around additive". |
| D3 | Medium | `13_conds_bcd.py:40-50` (roles loop) | The role pool includes players who have left the team. Luka Doncic stays DAL's top-usage player after 2025-02-12, Fox stays SAC's, AD stays LAL's same-position starter. Those games are coded "not out" by construction: 3,031 qualifying B1 rows (1,899 departed plus 1,132 traded before the next game) and 861 B4 rows. Corrected: B1 **+10.1 / +11.2**, B4 **+15.8 / +17.7** (from +9.7/+11.1 and +15.3/+17.4). | Before `.agg`, drop players whose latest appearance before D (any team) was for another team. |
| D4 | Medium | `13_conds_bcd.py:42-45, 50` | Top usage (B1), top assist share (B2) and the 25%+ usage list (B6) use an *unweighted mean of per-game usage* with no minutes floor. Garbage-time players win the role: Tristen Newton at 1.6 MPG was IND's top-usage player on 59 dates, and 9.5% of team-dates have a top-usage holder under 15 MPG. 14.8% of B6=1 rows are triggered only by sub-15-MPG players. Corrected B1 (minutes-weighted usage, 15+ MPG, departed players dropped): **+12.5 / +11.9**. | Weight usage and assist share by minutes (sum usage x MIN / sum MIN) and require 15+ MPG for role eligibility. Apply the same floor to `high_usg`. Break B4 start ties by minutes. |
| D5 | Medium (leak) | `12_conds_ad.py:65-66` | A11 ranks only among players who are in tonight's game, so it uses tonight's absences (the lock-time participants). It disagrees with the spec version on 9% of rows, all on absence nights. The pooled result goes from -4.2/-1.4 to -1.7/+0.3. | Rank all players who appeared in the team's previous game by their as-of season minutes (state after their last game before D), then attach the rank to this game's rows. |
| D6 | Low | `13_conds_bcd.py:75-80` | Neutral-site games (venue 'N', 10 games): both teams get the first-listed team's spread and implied total, so one sign is wrong. | Map team names to TEAM_ID (name to abbreviation table) and merge on (GAME_ID, TEAM_ID), not on the home flag. |
| D7 | Low | `16_sweep.py:4` (and C1 to C8 lists) | 1,934 degenerate cells (A1 tier condition crossed inside its own tier) are counted as "readable". | Drop A1_usg_szn_t from the sweep family (130 conditions, 8,385 pairs) or drop cells where a leg's n_a is 0. |
| D8 | Low | `12_conds_ad.py:72-73` | A12 salary tertile pool is the players who appeared that day. | Use every DK-listed player on the slate from the BigDataBall DFS feed. |
| D9 | Low | `12_conds_ad.py:24,38-39`; spec C1 | A2/A4 have no previous-season fallback (spec deviation). C1 uses season-to-date cutoffs, not "on the date"; the changelog does not record this. | Add both to the spec changelog, or implement the fallback. |
| D10 | Low (wording) | Report Verdict 3, 5, 7 | -7.8 should be -7.7. "Blocks and FTA near flat" is wrong for FTA b5 2025-26 (+3.9). Item 7 omits that only 96/133 pregame conditions kept their sign. | Edit the text. |
| D11 | Note | `13_conds_bcd.py:15-20`; spec layer B | The build's "out" also requires that his latest appearance before the date was for this team. That is correct, but the spec text does not say so (literal spec reading: 733 B1 / 127 B4 values differ). Players who never appear again are "out" for the rest of the season: 2,641 B1=1 qualifying rows, a mix of season-ending injuries and waived players. | Write both rules into the spec. |

None of D3 to D6 changes the direction of any headline: absences stay the largest pregame lever, and B1/B4 get *larger* after the fixes. D2 changes the wording of verdict item 6. D5 changes the A11 row, which the verdict does not use.
