# Layers A to D, the sweep, and the P2 forward check

NBA build thread, 2026-10-15, **corrected after independent review** (`REVIEW_LAYERS_A_D.md`, PASS WITH FIXES; what changed is listed under "Review fixes" below). Specs: `SPEC_LAYERS_A_D.md` (v1 frozen before any A-C count; v1.1 adds the layer E review fixes and fixes the sweep rules before the sweep ran; v1.2 applies this review) and `../../p2_forward/SPEC_P2.md` (frozen before the read window was counted). Same population and outcome as layer E: 560 players, 51,859 player-games, upside = his own top quarter of DK points.

## Verdict

1. **Absences are the biggest pregame lever by far, and they hold forward.** When a teammate played 0 minutes, upside nights jump: same-position starter out 20.3% to 36.1% (2024-25) and 20.8% to 38.4% (2025-26), top-assist teammate out +12.7 / +14.2, top-usage teammate out +12.5 / +11.9, two or more rotation players out +12.6 / +11.0. Built on games before 2026-01-15, every absence condition lifted more after that date (same-position starter +15.8 then +22.4). The lift is mostly minutes: with a same-position starter out, he played above his own median minutes in 63-66% of games against 41-42% otherwise.
2. **Who absorbs it: everyone a little, bench and middle-usage players most.** Inside usage tiers, two-plus rotation players out lifts bottom- and middle-tier players +13 to +15 and top-tier players +6.7 to +8.4. A same-position starter out lifts centers and point guards most (C +24.3 / +21.1, PG +18.6 / +21.8). Per player, nearly everyone gains: of player x absence rows with a +10 build-window lift, 75% were positive again later, and 63% of build-window negatives were too. Absences lift the whole roster; the data does not single out a specific absorber beyond role and position, and B7 (his own on/off usage history) does not either.
3. **Role sorts upside less than in the NFL, because upside here is measured against his own level.** Starting (confirmed lineup, lock-time) is +14.6 / +12.7, started 3 of the prior 5 +6.8 / +5.8, prior-10 minutes bottom third -7.7 / -7.7. Usage tiers barely move it (top third +2.4 / +0.1). Recent minutes trend matters; the usage level is already priced into his own top quarter.
4. **Lines and pace do almost nothing to own-top-quarter nights.** Opening implied team total: all thirds within 1.3 points both seasons. Spread: within 1.8. Both teams top-10 pace: -1.4 then +9.3 (reversed). A big total and a fast pace raise everyone's DK points, which moves the slate, not a player's chance of beating his own norm. Back-to-back is slightly positive (+1.9 / +2.3).
5. **The opponent alone registers, modestly.** DRtg bottom 5 +4.7 / +5.4; DvP (opponent-adjusted) bottom 10 +2.9 / +4.8; few turnovers forced bottom 5 +3.5 / +3.7. Blocks and FTA allowed are mixed: FTA bottom 5 is -0.8 in 2024-25 but +3.9 in 2025-26, blocks bottom 5 +0.8 / +2.5. DRtg holds forward too (bottom 5 +4.1 then +6.7).
6. **The sweep found no reliable multiplier.** Of 106,918 readable crosses (condition pair x usage tier x position, 30+ games each season), 14,448 beat both of their legs in both seasons, mostly one real leg plus a near-zero second leg in a small cell. Counted properly as a 2x2 (both / one only / other only / neither), crosses where both legs lift scatter around additive: 5,109 below additive in both seasons, 6,996 above, 11,726 mixed, median +0.8 / +0.6 points. Two good conditions roughly add; no pair reliably multiplies.
7. **P2: pooled conditions hold forward, per-player reads mostly do not.** Of the 21 pregame conditions with a build-window difference of 3 points or more, 19 kept their direction after 2026-01-15; across all 130 pregame conditions, 95 (73%) did. Per player, build-window leads were positive later 54.9% of the time against 48.5% for build-window negatives (layer E alone: 52.2% vs 48.3%; correlation 0.03). A player's personal split adds little beyond the league-wide lift of the same condition.

**What this means for picking (in order):** (1) who sits tonight on his team, with same-position starter and top playmaker first; (2) whether he starts and his recent minutes trend; (3) the opponent's overall defense and DvP; (4) shot-type funnels only as a tiebreak. Implied totals and pace set the slate's scoring level but not whose night it is.

## Table 1. Every A-D condition, pooled (upside when present vs absent)

| Layer | Condition | 2024-25 upside when present vs absent | 2025-26 |
|---|---|---|---|
| A pregame | usage rate, season-to-date = top | 2218/7953 = 27.9% vs 25.5% (**+2.4**) | 2293/8774 = 26.1% vs 26.0% (**+0.1**) |
| A pregame | usage rate, season-to-date = middle | 2075/8055 = 25.8% vs 26.6% (**-0.9**) | 2378/8766 = 27.1% vs 25.5% (**+1.6**) |
| A pregame | usage rate, season-to-date = bottom | 1828/7243 = 25.2% vs 26.8% (**-1.6**) | 2022/8156 = 24.8% vs 26.6% (**-1.8**) |
| A pregame | usage rate, prior 10 = top | 2263/8052 = 28.1% vs 25.4% (**+2.7**) | 2171/8027 = 27.0% vs 26.3% (**+0.7**) |
| A pregame | usage rate, prior 10 = middle | 2020/7965 = 25.4% vs 26.8% (**-1.5**) | 2180/7935 = 27.5% vs 26.1% (**+1.4**) |
| A pregame | usage rate, prior 10 = bottom | 1838/7234 = 25.4% vs 26.7% (**-1.3**) | 1904/7586 = 25.1% vs 27.3% (**-2.2**) |
| A pregame | minutes, season-to-date = top | 2550/8911 = 28.6% vs 24.9% (**+3.7**) | 2660/9773 = 27.2% vs 25.3% (**+1.9**) |
| A pregame | minutes, season-to-date = middle | 2293/8401 = 27.3% vs 25.8% (**+1.5**) | 2501/9359 = 26.7% vs 25.7% (**+1.1**) |
| A pregame | minutes, season-to-date = bottom | 1278/5939 = 21.5% vs 28.0% (**-6.5**) | 1532/6564 = 23.3% vs 27.0% (**-3.6**) |
| A pregame | minutes, prior 10 = top | 2663/8988 = 29.6% vs 24.2% (**+5.4**) | 2632/8782 = 30.0% vs 24.5% (**+5.4**) |
| A pregame | minutes, prior 10 = middle | 2266/8452 = 26.8% vs 26.0% (**+0.8**) | 2360/8707 = 27.1% vs 26.2% (**+0.9**) |
| A pregame | minutes, prior 10 = bottom | 1192/5811 = 20.5% vs 28.3% (**-7.7**) | 1263/6059 = 20.8% vs 28.5% (**-7.7**) |
| A pregame | FGA share of team = top | 2544/8811 = 28.9% vs 24.8% (**+4.1**) | 2622/9696 = 27.0% vs 25.4% (**+1.6**) |
| A pregame | FGA share of team = middle | 2312/8559 = 27.0% vs 25.9% (**+1.1**) | 2481/9267 = 26.8% vs 25.6% (**+1.1**) |
| A pregame | FGA share of team = bottom | 1265/5881 = 21.5% vs 28.0% (**-6.4**) | 1590/6733 = 23.6% vs 26.9% (**-3.3**) |
| A pregame | assist share of team = top | 2482/8776 = 28.3% vs 25.1% (**+3.1**) | 2560/9535 = 26.8% vs 25.6% (**+1.3**) |
| A pregame | assist share of team = middle | 2252/8340 = 27.0% vs 25.9% (**+1.1**) | 2493/9098 = 27.4% vs 25.3% (**+2.1**) |
| A pregame | assist share of team = bottom | 1387/6135 = 22.6% vs 27.7% (**-5.1**) | 1640/7063 = 23.2% vs 27.1% (**-3.9**) |
| A pregame | potential assists = top | 2456/8706 = 28.2% vs 25.2% (**+3.0**) | 2581/9497 = 27.2% vs 25.4% (**+1.8**) |
| A pregame | potential assists = middle | 2272/8457 = 26.9% vs 26.0% (**+0.8**) | 2419/8971 = 27.0% vs 25.6% (**+1.4**) |
| A pregame | potential assists = bottom | 1393/6088 = 22.9% vs 27.5% (**-4.7**) | 1693/7228 = 23.4% vs 27.1% (**-3.7**) |
| A pregame | rebound chances = top | 2487/8836 = 28.1% vs 25.2% (**+2.9**) | 2606/9524 = 27.4% vs 25.3% (**+2.1**) |
| A pregame | rebound chances = middle | 2314/8508 = 27.2% vs 25.8% (**+1.4**) | 2401/8994 = 26.7% vs 25.7% (**+1.0**) |
| A pregame | rebound chances = bottom | 1320/5907 = 22.3% vs 27.7% (**-5.3**) | 1686/7178 = 23.5% vs 27.0% (**-3.6**) |
| A pregame | DK salary on the slate = top | 2643/8912 = 29.7% vs 23.4% (**+6.2**) | 2592/8938 = 29.0% vs 24.3% (**+4.7**) |
| A pregame | DK salary on the slate = middle | 2294/8431 = 27.2% vs 24.8% (**+2.4**) | 2343/8311 = 28.2% vs 24.9% (**+3.3**) |
| A pregame | DK salary on the slate = bottom | 1463/7616 = 19.2% vs 28.5% (**-9.3**) | 1587/7873 = 20.2% vs 28.6% (**-8.5**) |
| A lock-time | started (confirmed lineup) | 4083/12269 = 33.3% vs 18.7% (**+14.6**) | 3994/12238 = 32.6% vs 19.9% (**+12.7**) |
| A pregame | started 3+ of prior 5 | 3235/10799 = 30.0% vs 23.2% (**+6.8**) | 3203/10780 = 29.7% vs 23.9% (**+5.8**) |
| A pregame | 5th-9th man by minutes | 2632/9958 = 26.4% vs 28.1% (**-1.7**) | 2890/10628 = 27.2% vs 26.9% (**+0.3**) |
| B pregame (0-minute rule) | top-usage teammate out | 1981/5657 = 35.0% vs 22.5% (**+12.5**) | 2403/6951 = 34.6% vs 22.6% (**+11.9**) |
| B pregame (0-minute rule) | top-assist teammate out | 1645/4600 = 35.8% vs 23.1% (**+12.7**) | 1917/5177 = 37.0% vs 22.8% (**+14.2**) |
| B pregame (0-minute rule) | starting center out | 1684/4905 = 34.3% vs 23.1% (**+11.2**) | 1814/5383 = 33.7% vs 23.6% (**+10.1**) |
| B pregame (0-minute rule) | same-position starter out | 1410/3908 = 36.1% vs 20.3% (**+15.8**) | 1498/3896 = 38.4% vs 20.8% (**+17.6**) |
| B pregame (0-minute rule) | 2+ rotation teammates out | 3556/10780 = 33.0% vs 20.4% (**+12.6**) | 3864/12170 = 31.8% vs 20.8% (**+11.0**) |
| B pregame (0-minute rule) | a 25%+ usage teammate out | 3037/9655 = 31.5% vs 22.3% (**+9.2**) | 3331/10267 = 32.4% vs 21.7% (**+10.8**) |
| C pregame | opening implied team total = top | 2205/8807 = 25.0% vs 25.0% (**-0.0**) | 2302/8520 = 27.0% vs 25.7% (**+1.3**) |
| C pregame | opening implied team total = middle | 1516/6213 = 24.4% vs 25.3% (**-0.9**) | 1798/6993 = 25.7% vs 26.3% (**-0.6**) |
| C pregame | opening implied team total = bottom | 1640/6387 = 25.7% vs 24.8% (**+0.9**) | 2418/9424 = 25.7% vs 26.4% (**-0.8**) |
| C pregame | opening game total = top | 2345/9217 = 25.4% vs 24.7% (**+0.7**) | 2337/8258 = 28.3% vs 25.1% (**+3.2**) |
| C pregame | opening game total = middle | 1585/6508 = 24.4% vs 25.3% (**-1.0**) | 1846/7271 = 25.4% vs 26.4% (**-1.1**) |
| C pregame | opening game total = bottom | 1431/5682 = 25.2% vs 25.0% (**+0.2**) | 2335/9408 = 24.8% vs 26.9% (**-2.1**) |
| C lock-time | closing implied team total = top | 2087/8556 = 24.4% vs 25.5% (**-1.1**) | 2239/8454 = 26.5% vs 26.0% (**+0.5**) |
| C lock-time | closing implied team total = middle | 1600/6507 = 24.6% vs 25.2% (**-0.7**) | 1824/7282 = 25.0% vs 26.6% (**-1.5**) |
| C lock-time | closing implied team total = bottom | 1674/6344 = 26.4% vs 24.5% (**+1.9**) | 2455/9201 = 26.7% vs 25.8% (**+0.9**) |
| C pregame | opening spread fav8+ | 839/3538 = 23.7% vs 24.9% (**-1.2**) | 1208/4783 = 25.3% vs 26.0% (**-0.7**) |
| C pregame | opening spread close | 2338/9727 = 24.0% vs 25.3% (**-1.2**) | 2685/10489 = 25.6% vs 26.0% (**-0.4**) |
| C pregame | opening spread dog8+ | 879/3354 = 26.2% vs 24.5% (**+1.7**) | 1206/4402 = 27.4% vs 25.6% (**+1.8**) |
| C pregame | both teams top-10 pace | 595/2376 = 25.0% vs 26.5% (**-1.4**) | 752/2146 = 35.0% vs 25.8% (**+9.3**) |
| C pregame | back-to-back | 1279/4685 = 27.3% vs 25.4% (**+1.9**) | 1295/4655 = 27.8% vs 25.5% (**+2.3**) |
| C pregame | home | 3352/12916 = 26.0% vs 25.3% (**+0.6**) | 3412/13056 = 26.1% vs 25.6% (**+0.5**) |
| C lock-time | spread moved 1.5+ toward his team | 1146/5132 = 22.3% vs 25.5% (**-3.1**) | 1316/5392 = 24.4% vs 26.2% (**-1.8**) |
| C lock-time | total moved up 3+ | 1228/4921 = 25.0% vs 24.7% (**+0.3**) | 1555/5881 = 26.4% vs 25.7% (**+0.7**) |
| in-game | final margin 15+ | 2153/9678 = 22.2% vs 27.7% (**-5.5**) | 2505/10473 = 23.9% vs 27.2% (**-3.2**) |
| in-game | overtime | 409/1139 = 35.9% vs 25.2% (**+10.7**) | 385/1077 = 35.7% vs 25.4% (**+10.3**) |
| in-game | 5+ fouls | 383/1142 = 33.5% vs 25.3% (**+8.3**) | 422/1304 = 32.4% vs 25.5% (**+6.8**) |
| in-game | minutes above his median | 5772/12979 = 44.5% vs 6.5% (**+38.0**) | 5828/12800 = 45.5% vs 7.0% (**+38.6**) |
| in-game | usage above his median | 4598/12542 = 36.7% vs 15.2% (**+21.5**) | 4738/13251 = 35.8% vs 15.7% (**+20.1**) |
| in-game | FGA above his median | 5645/11234 = 50.2% vs 6.6% (**+43.6**) | 5753/11558 = 49.8% vs 6.9% (**+42.9**) |
| in-game | DK per minute above his median | 6150/12550 = 49.0% vs 3.4% (**+45.6**) | 6298/13243 = 47.6% vs 3.5% (**+44.0**) |
| D pregame | defensive rating, bottom 5 | 1141/3784 = 30.2% vs 25.5% (**+4.7**) | 1196/3842 = 31.1% vs 25.7% (**+5.4**) |
| D pregame | defensive rating, bottom 10 | 2178/7597 = 28.7% vs 25.0% (**+3.6**) | 2277/7708 = 29.5% vs 25.1% (**+4.4**) |
| D pregame | DK points allowed to his position, bottom 5 | 1076/3700 = 29.1% vs 25.7% (**+3.4**) | 1202/3747 = 32.1% vs 25.6% (**+6.5**) |
| D pregame | DK points allowed to his position, bottom 10 | 2073/7438 = 27.9% vs 25.5% (**+2.4**) | 2194/7496 = 29.3% vs 25.4% (**+3.9**) |
| D pregame | DvP opponent-adjusted, bottom 5 | 1102/3751 = 29.4% vs 25.7% (**+3.7**) | 1180/3768 = 31.3% vs 25.7% (**+5.6**) |
| D pregame | DvP opponent-adjusted, bottom 10 | 2119/7519 = 28.2% vs 25.3% (**+2.9**) | 2263/7580 = 29.9% vs 25.0% (**+4.8**) |
| D pregame | offensive rebounds allowed, bottom 5 | 1125/3795 = 29.6% vs 25.6% (**+4.1**) | 1121/3879 = 28.9% vs 26.1% (**+2.8**) |
| D pregame | offensive rebounds allowed, bottom 10 | 2139/7575 = 28.2% vs 25.3% (**+3.0**) | 2162/7612 = 28.4% vs 25.7% (**+2.7**) |
| D pregame | turnovers forced (fewest), bottom 5 | 1102/3777 = 29.2% vs 25.7% (**+3.5**) | 1126/3788 = 29.7% vs 26.0% (**+3.7**) |
| D pregame | turnovers forced (fewest), bottom 10 | 2086/7538 = 27.7% vs 25.6% (**+2.1**) | 2171/7586 = 28.6% vs 25.6% (**+3.0**) |
| D pregame | rim eFG allowed, bottom 5 | 1081/3781 = 28.6% vs 25.8% (**+2.8**) | 1112/3791 = 29.3% vs 26.1% (**+3.3**) |
| D pregame | rim eFG allowed, bottom 10 | 2079/7562 = 27.5% vs 25.7% (**+1.8**) | 2162/7592 = 28.5% vs 25.7% (**+2.8**) |
| D pregame | blocks (fewest), bottom 5 | 1003/3718 = 27.0% vs 26.1% (**+0.8**) | 1082/3774 = 28.7% vs 26.2% (**+2.5**) |
| D pregame | blocks (fewest), bottom 10 | 2009/7516 = 26.7% vs 26.0% (**+0.7**) | 2038/7560 = 27.0% vs 26.4% (**+0.5**) |
| D pregame | FTA allowed per 100, bottom 5 | 960/3748 = 25.6% vs 26.4% (**-0.8**) | 1144/3837 = 29.8% vs 26.0% (**+3.9**) |
| D pregame | FTA allowed per 100, bottom 10 | 1982/7549 = 26.3% vs 26.3% (**-0.0**) | 2123/7628 = 27.8% vs 26.0% (**+1.8**) |

## Table 2. Inside usage tiers (season-to-date usage, top / middle / bottom third at his position)

| Condition | Usage tier | 2024-25 diff (present games) | 2025-26 diff (present games) |
|---|---|---|---|
| started (confirmed lineup) | top | +11.6 (5,486) | +9.4 (6,027) |
| started (confirmed lineup) | middle | +13.6 (3,561) | +13.5 (3,889) |
| started (confirmed lineup) | bottom | +19.2 (2,342) | +19.1 (2,257) |
| top-usage teammate out | top | +11.7 (1,659) | +9.9 (2,040) |
| top-usage teammate out | middle | +13.7 (1,947) | +12.7 (2,599) |
| top-usage teammate out | bottom | +12.3 (1,811) | +12.6 (2,260) |
| top-assist teammate out | top | +8.9 (1,288) | +13.8 (1,578) |
| top-assist teammate out | middle | +14.1 (1,615) | +13.6 (1,839) |
| top-assist teammate out | bottom | +15.3 (1,527) | +15.1 (1,722) |
| same-position starter out | top | +16.0 (787) | +12.7 (769) |
| same-position starter out | middle | +14.5 (1,411) | +18.2 (1,630) |
| same-position starter out | bottom | +16.0 (1,485) | +19.0 (1,438) |
| 2+ rotation teammates out | top | +8.4 (3,373) | +6.7 (3,930) |
| 2+ rotation teammates out | middle | +15.1 (3,692) | +13.1 (4,274) |
| 2+ rotation teammates out | bottom | +14.6 (3,407) | +13.1 (3,877) |
| defensive rating, bottom 5 | top | +4.2 (1,219) | +3.3 (1,276) |
| defensive rating, bottom 5 | middle | +4.7 (1,305) | +6.9 (1,315) |
| defensive rating, bottom 5 | bottom | +5.1 (1,168) | +6.2 (1,238) |
| DvP opponent-adjusted, bottom 5 | top | +3.7 (1,221) | +5.3 (1,283) |
| DvP opponent-adjusted, bottom 5 | middle | +3.1 (1,303) | +5.7 (1,285) |
| DvP opponent-adjusted, bottom 5 | bottom | +4.4 (1,136) | +5.6 (1,184) |
| opening implied team total = top | top | +1.1 (2,788) | +0.3 (2,980) |
| opening implied team total = top | middle | +0.1 (2,969) | +1.6 (2,682) |
| opening implied team total = top | bottom | -0.6 (2,567) | +2.3 (2,780) |
| both teams top-10 pace | top | -3.2 (798) | +9.7 (832) |
| both teams top-10 pace | middle | +0.6 (848) | +9.4 (645) |
| both teams top-10 pace | bottom | -2.0 (670) | +8.8 (652) |

## Minutes or per-minute?

Of upside games, 80% came with both above-median minutes and above-median DK per minute, 7% with minutes only, 13% with per-minute only (both seasons within 1.5 points). Absence lifts run mostly through minutes; DRtg bottom-5 lifts run through per-minute production (DK per minute above median 56% / 58% vs 48% / 50%), not minutes.

## Table 3. The sweep's largest cross leads with 100+ present games in each season

Full list: `sweep_cross_leads.csv` (14,448 rows); every readable cell: `sweep_all_readable_cells.csv.gz`. Family: 130 pregame conditions, 8,385 pairs, 15 usage-tier x position groups (106,918 readable cells).

| Usage tier | Pos | Condition 1 | Condition 2 | 2024-25 cross (n) / leg 1 / leg 2 | 2025-26 cross (n) / leg 1 / leg 2 |
|---|---|---|---|---|---|
| middle | SF | A6_astsh_szn_t=middle | D1_drtg_rk_b5 | +16.4 (108) / +4.1 / +6.1 | +13.6 (101) / +3.5 / +4.5 |
| bottom | PG | D2_dvp_rk_b10 | E_rim_eff_b5 | +14.3 (104) / +6.0 / +3.6 | +13.0 (129) / +1.7 / +3.8 |
| middle | PG | A3_min_szn_t=middle | A4_min_l10_t=top | +16.3 (146) / +8.9 / +4.3 | +17.6 (106) / -3.9 / +9.0 |
| bottom | PG | A12_sal_t=middle | B1_top_usg_out | +18.8 (207) / +7.4 / +11.0 | +23.9 (291) / +8.3 / +16.6 |
| top | PG | E_mid_eff_b10 | E_ml_3pt_b5 | +11.4 (111) / +3.5 / +4.5 | +9.8 (140) / +1.5 / +2.1 |
| middle | SG | B3_start_c_out | D6a_rim_eff_rk_b10 | +16.7 (110) / +9.9 / +5.0 | +12.1 (111) / +5.3 / +3.8 |
| top | PG | E_mid_eff_b10 | E_ml_cs_b5 | +10.1 (123) / +3.5 / +1.4 | +10.3 (118) / +1.5 / +2.6 |
| middle | PF | B1_top_usg_out | D2_dvp_rk_b10 | +23.9 (101) / +17.3 / +4.3 | +23.3 (138) / +15.0 / +8.5 |
| top | PF | A3_min_szn_t=middle | A7_potast_szn_t=top | +13.2 (159) / +2.9 / +4.5 | +10.4 (103) / +3.3 / +3.9 |
| top | PG | D2_dvp_rk_b5 | E_pu2_eff_b10 | +10.3 (131) / +3.0 / +2.6 | +9.9 (151) / +3.6 / +3.5 |
| top | PG | D1_drtg_rk_b5 | E_mid_eff_b10 | +10.7 (105) / +3.3 / +3.5 | +10.3 (135) / +4.1 / +1.5 |
| middle | PG | D2_dvp_rk_b5 | E_rim_eff_b5 | +11.4 (127) / +0.4 / +5.2 | +19.2 (106) / +8.4 / +6.1 |
| middle | SG | A3_min_szn_t=middle | E_leg_lt10 | +9.7 (117) / +1.4 / +3.6 | +15.6 (122) / -1.3 / +8.8 |
| middle | PG | D3_dvpadj_rk_b5 | E_paint_eff_b10 | +12.4 (109) / +4.9 / -0.6 | +11.4 (134) / +5.3 / +1.8 |
| middle | PF | D6a_rim_eff_rk_b5 | E_pu3_eff_b10 | +9.9 (101) / +2.0 / +2.0 | +9.9 (105) / +0.8 / +3.9 |

**Do crosses stack?** Counted as a 2x2 inside each cell (both present / only condition 1 / only condition 2 / neither, each group 30+ games both seasons), interaction = (both - neither) - (only 1 - neither) - (only 2 - neither). Where both legs lift on their own in both seasons (23,831 cells): below additive in both seasons 5,109, above additive in both 6,996, mixed 11,726; median interaction +0.8 / +0.6 points. All readable cells (105,212): below 24,855, above 27,966, mixed 52,391; median +0.2 / +0.3.

## Table 4. P2 pooled: build window (2024-25 + 2025-26 before Jan 15) vs read window (after Jan 15), conditions with |build diff| >= 2.5

The upside threshold is frozen from build games only, so the read window's base rate is 30.9% (late-season scoring is higher).

| Condition | Build window diff (present games) | Read window diff (present games) | Same direction |
|---|---|---|---|
| B4_samepos_starter_out | +15.8 (5,274) | +22.4 (2,074) | yes |
| B2_top_ast_out | +12.4 (6,597) | +19.5 (2,756) | yes |
| B5_two_rotation_out | +11.4 (15,585) | +16.3 (6,538) | yes |
| B1_top_usg_out | +11.0 (8,186) | +16.7 (3,866) | yes |
| B3_start_c_out | +9.5 (7,195) | +15.8 (2,718) | yes |
| B6_25usg_out | +8.6 (13,400) | +14.8 (5,812) | yes |
| A10_started3of5 | +4.7 (15,706) | +3.1 (5,776) | yes |
| A12_sal_t=top | +4.4 (13,326) | +1.8 (4,491) | yes |
| D1_drtg_rk_b5 | +4.1 (5,386) | +6.7 (2,026) | yes |
| D5_tov_rk_b5 | +4.0 (5,323) | +2.7 (2,040) | yes |
| D2_dvp_rk_b5 | +3.9 (5,242) | +6.4 (1,997) | yes |
| A4_min_l10_t=top | +3.9 (12,837) | +2.8 (4,886) | yes |
| E_wo_vol_b5 | +3.9 (5,299) | +2.1 (2,084) | yes |
| D3_dvpadj_rk_b5 | +3.8 (5,299) | +6.8 (2,011) | yes |
| E_ml_lt10_b5 | +3.6 (5,542) | +5.1 (2,140) | yes |
| D3_dvpadj_rk_b10 | +3.1 (10,644) | +6.0 (4,047) | yes |
| E_trans_vol_b10 | +3.0 (9,558) | +3.5 (4,065) | yes |
| E_ml_3pt_b5 | +3.0 (5,069) | +2.3 (2,172) | yes |
| E_ml_lt10_b10 | +2.9 (10,938) | +5.8 (4,173) | yes |
| E_trans_vol_b5 | +2.8 (4,765) | +4.1 (2,058) | yes |
| E_lt10_eff_b5 | +2.8 (5,292) | +4.0 (2,015) | yes |
| E_ml_3pt_b10 | +2.8 (9,850) | +1.5 (4,188) | yes |
| D1_drtg_rk_b10 | +2.7 (10,784) | +6.9 (4,103) | yes |
| D4_orb_rk_b5 | +2.7 (5,448) | +5.4 (2,004) | yes |
| E_mid_eff_b5 | +2.6 (4,703) | +3.1 (2,016) | yes |
| E_pu2_eff_b5 | +2.6 (5,258) | +3.2 (2,045) | yes |
| E_rim_eff_b5 | +2.5 (4,792) | +5.5 (2,059) | yes |
| D6a_rim_eff_rk_b5 | +2.5 (5,322) | +5.5 (2,059) | yes |
| D5_tov_rk_b10 | +2.5 (10,615) | +1.7 (4,102) | yes |
| A8_rebch_szn_t=bottom | -2.9 (9,418) | +2.3 (2,956) | **no** |
| A7_potast_szn_t=bottom | -3.0 (9,630) | +0.6 (3,069) | **no** |
| A6_astsh_szn_t=bottom | -3.1 (9,579) | -0.8 (2,944) | yes |
| A5_fgash_szn_t=bottom | -3.4 (9,151) | +1.6 (2,649) | **no** |
| A3_min_szn_t=bottom | -3.5 (9,184) | +2.7 (2,603) | **no** |
| A4_min_l10_t=bottom | -5.3 (8,563) | -8.1 (2,661) | yes |
| A12_sal_t=bottom | -6.6 (11,237) | -8.5 (3,389) | yes |

All 130 pregame conditions: 95 kept their sign (73%). With a build difference of 3+ points: 19 of 21.

## Table 5. P2 per player: do personal reads carry forward?

A row is one player x condition with 10+ present and 10+ absent build games and 5+ / 5+ read games. A build lead is a build difference of +10 or more; a build negative is -10 or less.

| Layer | Rows | Build leads | Positive again in read | Build negatives | Positive in read | Correlation build vs read |
|---|---|---|---|---|---|---|
| A | 1,210 | 380 | 49.5% | 324 | 43.2% | 0.117 |
| B | 907 | 518 | 75.1% | 60 | 63.3% | 0.129 |
| C | 2,687 | 562 | 50.9% | 560 | 41.4% | 0.072 |
| D | 3,752 | 1,005 | 57.2% | 614 | 56.8% | 0.026 |
| E | 13,760 | 3,172 | 52.2% | 2,590 | 48.3% | 0.034 |
| lock-time | 1,103 | 278 | 54.7% | 234 | 44.9% | 0.232 |
| all pregame | 22,316 | 5,637 | 54.9% | 4,148 | 48.5% | 0.076 |

## B7: his on/off usage prior does not pick who benefits (counted after the template)

On nights the team's top-usage teammate played 0 minutes, players whose earlier play-by-play showed a usage share at least 3 points higher with that teammate off the floor (100+ minutes each way) were compared with everyone else on those nights. On/off minutes rebuilt from play-by-play lineups match the box (minutes correlation 0.9998).

| Season | Prior says he gains: upside | Other players those nights: upside | Difference |
|---|---|---|---|
| 2024-25 (through 2025-03-24) | 270 of 668 (40.4%) | 278 of 900 (30.9%) | +9.5 |
| 2025-26 | 548 of 1,521 (36.0%) | 544 of 1,508 (36.1%) | -0.0 |

Verdict: flat in 2025-26, so not a lead. The absence itself lifts upside (B1 above); the on/off prior does not say which teammate gets it. Scripts `20_onoff.py`, `21_b7.py`.

## Not yet counted

- Lines exist for 2024-25 only through 2025-03-24 (BigDataBall team feed); C conditions skip later 2024-25 games.

## Review fixes (spec v1.2)

The review reproduced the counts and found no future data in the cutoffs, roles or ranks. Fixes applied, then everything from layer A conditions onward was rerun:

- **Tables 1 and 2 were stale** (from the run before v1.1). All tables are now generated by `22_ad_report_tables.py` from the build outputs.
- **Verdict item 6 was wrong.** "Crosses fall below the sum of their legs, conditions saturate" came from comparing the cross against all other games, which include the one-leg games. The 2x2 count above replaces it: no saturation, no reliable multiplier.
- **A11 (5th to 9th man) used tonight's absences.** It now ranks everyone who appeared in the team's previous game by season minutes as of that game. Result moved from -4.2 / -1.4 to -1.7 / +0.3 (flat).
- **Absence roles kept players who had left the team** (Doncic stayed Dallas's top-usage player after the trade) **and let garbage-time players win top usage** (unweighted mean of per-game usage, no minutes floor). Roles now drop players whose latest appearance was for another team, weight usage and assist share by minutes, need 15+ minutes a game for the usage and assist roles and the 25%+ usage list, and break start ties by minutes. Top-usage out moved from +9.7 / +11.1 to +12.5 / +11.9; same-position starter out from +15.3 / +17.4 to +15.8 / +17.6.
- **Neutral-site games** (20 team-games) gave both teams the same spread; lines now join by team.
- **The usage tier is the sweep's cell,** so it was removed as a sweep condition (130 conditions, was 133).
- **Recorded, not changed:** the DK salary tertile pool is the players who appeared that day, because BigDataBall's DFS feed lists only players who played; prior-10 tiers have no previous-season fallback; implied-total thirds use season-to-date team-games before the date rather than the slate. A player who never appears again is "out" for the rest of the season (season-ending injuries and waived players alike).

No headline changed direction; absences got slightly larger.

## Files

`layers_a_d_per_player.csv` (every player x A-D condition, both seasons), `pooled_ad.csv` (pooled by season, position and usage tier), `sweep_cross_leads.csv`, `sweep_all_readable_cells.csv.gz` (with the 2x2 interaction), `../../p2_forward/p2_pooled.csv`, `p2_perplayer_summary.csv`, `p2_perplayer_rows.csv.gz`. Scripts: `../layer_e/build/12_*.py` to `17_p2.py`, `20_onoff.py`, `21_b7.py`, `22_ad_report_tables.py`.
