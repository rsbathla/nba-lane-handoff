# Layer E: shot type vs funnel, every player (P1, built first)

NBA build thread, 2026-10-15. Spec `SPEC_LAYER_E.md`: v1.1 was frozen (hash in `SPEC_FREEZE.json`) before any upside was counted; v1.2 adds the independent reviewer's four rule fixes after the first count, disclosed in its changelog. Regular seasons 2024-25 and 2025-26, 560 players with 20+ games, 51,859 player-games. Upside = a player's own top quarter of DK points. Counts only; no tests, scores or weights.

## Verdict

1. **A defense that is bottom 5 in a shot type does lift upside nights, but only by about 2 to 4 points on a 26% base, and most of that is the defense being bad overall.** A bottom-5 defense by points allowed per 100 (DRtg) lifts upside more than any single shot-type funnel: 30.2% vs 25.5% in 2024-25 and 31.1% vs 25.7% in 2025-26 (+4.7 and +5.4). For the funnels that show a lift, half to four fifths of the "bottom 5 in type X" nights are also nights against a bottom-10 DRtg defense (Table 3, last column).
2. **The match to the player's own shot type adds almost nothing.** Players who lean on the type and players who do not get about the same lift on the interior funnels (rim, under 10 ft, short paint, mid-range eFG). The three-point volume funnels (catch-and-shoot, wide open, above the break) give leaners about 1 to 4 points more than non-leaners, but once games against bottom-10 DRtg defenses are set aside, that edge holds in one season and not the other. The one funnel that keeps about +2 points outside the weak defenses is rim volume allowed (bottom 5: +2.0 / +2.3; Matchup Lab <10ft bottom 10: +2.5 / +3.5), and it lifts every player, not just rim-heavy ones, so it reads as a soft interior defense rather than a shot-type match. Same pattern as the NFL study: the cross mostly restates one leg.
3. **Per-player funnel reads do not carry from one season to the next.** Player-condition rows that were +10 points or better in 2024-25 were positive again in 2025-26 51.7% of the time; rows that were -10 or worse were positive again 52.2% of the time, and the correlation between the two seasons' differences is 0.006 (Table 4). A strong personal read in one season says nothing about the next. A per-player lead list exists (3,130 rows positive in both seasons with 10+ games each), but across the 32,480 headline rows, 4,455 were positive both seasons and 3,732 negative both seasons: close to what chance alone produces around a small league-wide lift.
4. **One clear negative, both seasons:** opponents that allow a lot of pull-up 3s go with *fewer* upside nights (bottom 5: -1.5 and -2.7; bottom 10: -2.2 and -2.7), for leaners and non-leaners alike. Mid-range and pull-up 2 volume allowed are also slightly negative. A generous pull-up-3 defense is not a target.
5. **Ramneik's Matchup Lab composite, rebuilt as of each date, behaves like the plain funnels:** ML <10ft rank 26-30 +3.7 / +4.0, ML 3PT +3.9 / +2.8, ML PITP 21-30 +2.7 / +4.1, ML C&S +1.9 / +4.8, ML Pull Up and ML Mid flat. Its interior composites (<10ft, PITP) share two thirds to four fifths of their nights with a bottom-10 DRtg defense, so the ML score is mostly reading general defensive weakness. The dashboard's 20% share rule marks 78-94% of player-games as "leans on" for C&S, <10ft, PITP and 3PT, so the player side of the ML score barely separates anyone.

**What this means for picking:** the baseline read is the opponent's overall defense, then the player's role (layers A to C, next). Treat a shot-type funnel as a small tiebreak on top of an already weak defense, not as a separate edge, and drop "bottom-5 pull-up 3 defense" as a positive. This matches Codex's earlier finding (funnels real but small and additive) and the NFL ordering (usage, then script, then matchup).

## What was counted

- Shot types (12): catch-and-shoot 3, pull-up 3, pull-up 2, under 10 ft, wide open (NBA.com tracking, full seasons); rim 0-3 ft, short paint 3-10 ft, mid-range, corner 3, above-the-break 3, transition proxy (play-by-play; 2024-25 through 2025-03-24 only); free-throw rate (box). Plus Matchup Lab's six rebuildable composites (C&S, Pull Up, <10ft, PITP, Mid, 3PT).
- Opponent leg as of each date (earlier games only, rank of 30, 30 = most allowed, ranked once a team has 10 games): volume allowed per 100 possessions and eFG allowed, season-to-date (headline), plus last-10 and opponent-adjusted versions in the CSV. Bottom 5 = 26-30, bottom 10 = 21-30.
- Player leg: his share of FGA in the type from earlier games, top third at his DK position on that date.
- Family size: 109,760 opponent-leg rows, 109,760 cross rows and 10,080 player-leg rows across player x type x condition (each with both seasons). Headline opponent rows: 32,480.


## Tables

### Table 1. Opponent leg alone, bottom 5 (all qualifying players pooled)

| Shot type | Condition | 2024-25: upside when present (rate) vs absent | 2025-26: same |
|---|---|---|---|
| Catch-and-shoot 3 | Volume allowed, bottom 5 | 1036/3791 = 27.3% vs 26.1% (**+1.3**) | 1028/3777 = 27.2% vs 26.5% (**+0.7**) |
| Catch-and-shoot 3 | eFG allowed, bottom 5 | 987/3764 = 26.2% vs 26.3% (**-0.1**) | 1072/3754 = 28.6% vs 26.2% (**+2.3**) |
| Pull-up 3 | Volume allowed, bottom 5 | 940/3752 = 25.1% vs 26.5% (**-1.5**) | 922/3787 = 24.3% vs 27.1% (**-2.7**) |
| Pull-up 3 | eFG allowed, bottom 5 | 1061/3737 = 28.4% vs 25.8% (**+2.5**) | 1018/3788 = 26.9% vs 26.6% (**+0.3**) |
| Pull-up 2 | Volume allowed, bottom 5 | 977/3752 = 26.0% vs 26.3% (**-0.3**) | 958/3773 = 25.4% vs 26.8% (**-1.5**) |
| Pull-up 2 | eFG allowed, bottom 5 | 1052/3710 = 28.4% vs 25.9% (**+2.5**) | 1119/3784 = 29.6% vs 26.0% (**+3.6**) |
| Under 10 ft | Volume allowed, bottom 5 | 983/3731 = 26.3% vs 26.3% (**+0.1**) | 1178/3815 = 30.9% vs 25.7% (**+5.1**) |
| Under 10 ft | eFG allowed, bottom 5 | 1073/3714 = 28.9% vs 25.8% (**+3.1**) | 1091/3787 = 28.8% vs 26.2% (**+2.6**) |
| Wide open | Volume allowed, bottom 5 | 1106/3797 = 29.1% vs 25.7% (**+3.4**) | 1109/3781 = 29.3% vs 26.1% (**+3.3**) |
| Wide open | eFG allowed, bottom 5 | 998/3793 = 26.3% vs 26.3% (**+0.0**) | 1012/3835 = 26.4% vs 26.6% (**-0.3**) |
| Rim 0-3 ft | Volume allowed, bottom 5 | 893/3210 = 27.8% vs 24.8% (**+3.0**) | 1139/3867 = 29.5% vs 26.0% (**+3.4**) |
| Rim 0-3 ft | eFG allowed, bottom 5 | 899/3243 = 27.7% vs 24.8% (**+2.9**) | 1112/3791 = 29.3% vs 26.1% (**+3.3**) |
| Short paint 3-10 ft | Volume allowed, bottom 5 | 807/3135 = 25.7% vs 25.2% (**+0.5**) | 1031/3869 = 26.6% vs 26.6% (**+0.1**) |
| Short paint 3-10 ft | eFG allowed, bottom 5 | 856/3178 = 26.9% vs 25.0% (**+1.9**) | 1128/3801 = 29.7% vs 26.0% (**+3.7**) |
| Mid-range | Volume allowed, bottom 5 | 806/3267 = 24.7% vs 25.4% (**-0.8**) | 974/3879 = 25.1% vs 26.9% (**-1.8**) |
| Mid-range | eFG allowed, bottom 5 | 851/3119 = 27.3% vs 24.9% (**+2.4**) | 1144/3810 = 30.0% vs 25.9% (**+4.1**) |
| Corner 3 | Volume allowed, bottom 5 | 803/3235 = 24.8% vs 25.4% (**-0.6**) | 1035/3734 = 27.7% vs 26.4% (**+1.3**) |
| Corner 3 | eFG allowed, bottom 5 | 733/3239 = 22.6% vs 25.9% (**-3.2**) | 1044/3837 = 27.2% vs 26.5% (**+0.7**) |
| Above-break 3 | Volume allowed, bottom 5 | 874/3247 = 26.9% vs 25.0% (**+1.9**) | 1057/3776 = 28.0% vs 26.3% (**+1.7**) |
| Above-break 3 | eFG allowed, bottom 5 | 864/3161 = 27.3% vs 24.9% (**+2.4**) | 1005/3807 = 26.4% vs 26.6% (**-0.2**) |
| Transition (proxy) | Volume allowed, bottom 5 | 880/3268 = 26.9% vs 25.0% (**+1.9**) | 1164/3755 = 31.0% vs 25.7% (**+5.3**) |
| Transition (proxy) | eFG allowed, bottom 5 | 869/3259 = 26.7% vs 25.0% (**+1.6**) | 1020/3789 = 26.9% vs 26.5% (**+0.4**) |
| Free-throw rate | Volume allowed, bottom 5 | 960/3748 = 25.6% vs 26.4% (**-0.8**) | 1144/3837 = 29.8% vs 26.0% (**+3.9**) |
| ML C&S | ML rank 26-30 | 1102/3955 = 27.9% vs 25.9% (**+1.9**) | 1178/3855 = 30.6% vs 25.8% (**+4.8**) |
| ML Pull Up | ML rank 26-30 | 1024/3788 = 27.0% vs 26.1% (**+0.9**) | 1052/3938 = 26.7% vs 26.6% (**+0.1**) |
| ML <10ft | ML rank 26-30 | 1147/3906 = 29.4% vs 25.6% (**+3.7**) | 1195/4000 = 29.9% vs 25.9% (**+4.0**) |
| ML PITP | ML rank 26-30 | 979/3564 = 27.5% vs 24.8% (**+2.6**) | 1228/4171 = 29.4% vs 26.0% (**+3.5**) |
| ML Mid | ML rank 26-30 | 850/3397 = 25.0% vs 25.4% (**-0.4**) | 1156/4186 = 27.6% vs 26.4% (**+1.2**) |
| ML 3PT | ML rank 26-30 | 966/3383 = 28.6% vs 24.6% (**+3.9**) | 1174/4057 = 28.9% vs 26.1% (**+2.8**) |

### Table 2. Opponent leg alone, bottom 10

| Shot type | Condition | 2024-25: upside when present (rate) vs absent | 2025-26: same |
|---|---|---|---|
| Catch-and-shoot 3 | Volume allowed, bottom 10 | 2127/7599 = 28.0% vs 25.4% (**+2.6**) | 2108/7475 = 28.2% vs 25.8% (**+2.4**) |
| Catch-and-shoot 3 | eFG allowed, bottom 10 | 1975/7574 = 26.1% vs 26.4% (**-0.3**) | 2167/7776 = 27.9% vs 26.0% (**+1.9**) |
| Pull-up 3 | Volume allowed, bottom 10 | 1856/7490 = 24.8% vs 27.0% (**-2.2**) | 1873/7560 = 24.8% vs 27.5% (**-2.7**) |
| Pull-up 3 | eFG allowed, bottom 10 | 2019/7524 = 26.8% vs 26.0% (**+0.8**) | 2061/7564 = 27.2% vs 26.3% (**+1.0**) |
| Pull-up 2 | Volume allowed, bottom 10 | 1843/7394 = 24.9% vs 26.9% (**-2.0**) | 1960/7632 = 25.7% vs 27.1% (**-1.4**) |
| Pull-up 2 | eFG allowed, bottom 10 | 2022/7574 = 26.7% vs 26.1% (**+0.6**) | 2170/7549 = 28.7% vs 25.5% (**+3.2**) |
| Under 10 ft | Volume allowed, bottom 10 | 1987/7543 = 26.3% vs 26.2% (**+0.1**) | 2142/7655 = 28.0% vs 25.9% (**+2.1**) |
| Under 10 ft | eFG allowed, bottom 10 | 2120/7573 = 28.0% vs 25.4% (**+2.6**) | 2108/7594 = 27.8% vs 26.0% (**+1.7**) |
| Wide open | Volume allowed, bottom 10 | 2117/7605 = 27.8% vs 25.5% (**+2.4**) | 2144/7477 = 28.7% vs 25.6% (**+3.1**) |
| Wide open | eFG allowed, bottom 10 | 1947/7514 = 25.9% vs 26.5% (**-0.5**) | 1961/7651 = 25.6% vs 27.1% (**-1.5**) |
| Rim 0-3 ft | Volume allowed, bottom 10 | 1723/6458 = 26.7% vs 24.6% (**+2.1**) | 2142/7592 = 28.2% vs 25.8% (**+2.4**) |
| Rim 0-3 ft | eFG allowed, bottom 10 | 1734/6499 = 26.7% vs 24.6% (**+2.1**) | 2162/7592 = 28.5% vs 25.7% (**+2.8**) |
| Short paint 3-10 ft | Volume allowed, bottom 10 | 1608/6365 = 25.3% vs 25.3% (**-0.1**) | 2022/7605 = 26.6% vs 26.6% (**-0.0**) |
| Short paint 3-10 ft | eFG allowed, bottom 10 | 1704/6475 = 26.3% vs 24.8% (**+1.5**) | 2079/7632 = 27.2% vs 26.3% (**+1.0**) |
| Mid-range | Volume allowed, bottom 10 | 1586/6446 = 24.6% vs 25.7% (**-1.1**) | 1967/7635 = 25.8% vs 27.0% (**-1.3**) |
| Mid-range | eFG allowed, bottom 10 | 1683/6385 = 26.4% vs 24.8% (**+1.6**) | 2140/7612 = 28.1% vs 25.8% (**+2.3**) |
| Corner 3 | Volume allowed, bottom 10 | 1739/6534 = 26.6% vs 24.6% (**+2.0**) | 2019/7487 = 27.0% vs 26.4% (**+0.5**) |
| Corner 3 | eFG allowed, bottom 10 | 1537/6396 = 24.0% vs 25.9% (**-1.9**) | 2094/7597 = 27.6% vs 26.1% (**+1.4**) |
| Above-break 3 | Volume allowed, bottom 10 | 1688/6408 = 26.3% vs 24.8% (**+1.5**) | 2016/7560 = 26.7% vs 26.6% (**+0.1**) |
| Above-break 3 | eFG allowed, bottom 10 | 1726/6449 = 26.8% vs 24.6% (**+2.2**) | 2029/7706 = 26.3% vs 26.7% (**-0.4**) |
| Transition (proxy) | Volume allowed, bottom 10 | 1764/6463 = 27.3% vs 24.3% (**+3.0**) | 2212/7561 = 29.3% vs 25.3% (**+4.0**) |
| Transition (proxy) | eFG allowed, bottom 10 | 1680/6463 = 26.0% vs 25.0% (**+1.0**) | 2089/7650 = 27.3% vs 26.3% (**+1.1**) |
| Free-throw rate | Volume allowed, bottom 10 | 1982/7549 = 26.3% vs 26.3% (**-0.0**) | 2123/7628 = 27.8% vs 26.0% (**+1.8**) |
| ML C&S | ML rank 21-30 | 2157/7793 = 27.7% vs 25.5% (**+2.2**) | 2188/7674 = 28.5% vs 25.6% (**+2.9**) |
| ML Pull Up | ML rank 21-30 | 1990/7675 = 25.9% vs 26.4% (**-0.5**) | 2080/7885 = 26.4% vs 26.7% (**-0.3**) |
| ML <10ft | ML rank 21-30 | 2190/7702 = 28.4% vs 25.1% (**+3.3**) | 2318/7835 = 29.6% vs 25.0% (**+4.5**) |
| ML PITP | ML rank 21-30 | 1829/6752 = 27.1% vs 24.4% (**+2.7**) | 2410/8256 = 29.2% vs 25.1% (**+4.1**) |
| ML Mid | ML rank 21-30 | 1706/6716 = 25.4% vs 25.3% (**+0.1**) | 2110/7732 = 27.3% vs 26.3% (**+1.0**) |
| ML 3PT | ML rank 21-30 | 1868/6694 = 27.9% vs 23.9% (**+4.0**) | 2165/7750 = 27.9% vs 25.9% (**+2.0**) |

Table 3 note: "All players" here is limited to games where the player leg and DRtg rank both exist, so it differs slightly from Tables 1 and 2.

### Table 3. Does the match to his shot type add anything? (difference in points, 2024-25 / 2025-26)

| Shot type | Condition | All players | Players who lean on the type | Players who do not | Only games vs defenses outside DRtg bottom 10 | Share of these games also vs a DRtg bottom-10 defense |
|---|---|---|---|---|---|---|
| Catch-and-shoot 3 | vol b5 | +1.2 / +0.8 | +2.8 / +3.2 | +0.4 / -0.5 | -0.9 / -3.9 | 48% |
| Catch-and-shoot 3 | vol b10 | +2.6 / +2.4 | +4.4 / +3.7 | +1.7 / +1.7 | +0.1 / -1.0 | 48% |
| Catch-and-shoot 3 | eff b5 | +0.1 / +2.3 | +0.7 / +1.6 | -0.2 / +2.7 | +0.1 / +0.8 | 52% |
| Catch-and-shoot 3 | eff b10 | -0.1 / +1.9 | +0.1 / +1.6 | -0.2 / +2.0 | +0.0 / -1.2 | 46% |
| Pull-up 3 | vol b5 | -1.4 / -2.6 | -2.4 / -2.3 | -0.8 / -2.8 | -0.5 / -2.2 | 32% |
| Pull-up 3 | vol b10 | -2.2 / -2.7 | -3.6 / -1.9 | -1.3 / -3.2 | -1.2 / -2.7 | 25% |
| Pull-up 3 | eff b5 | +2.5 / +0.4 | +3.6 / -1.6 | +1.9 / +1.4 | +2.0 / -0.7 | 44% |
| Pull-up 3 | eff b10 | +0.9 / +0.9 | +0.2 / -1.1 | +1.2 / +2.0 | +1.0 / +1.5 | 37% |
| Pull-up 2 | vol b5 | -0.3 / -1.4 | +0.3 / -0.1 | -0.5 / -2.1 | +0.8 / +0.2 | 22% |
| Pull-up 2 | vol b10 | -2.1 / -1.3 | -1.6 / -0.4 | -2.4 / -1.8 | -1.1 / +1.3 | 20% |
| Pull-up 2 | eff b5 | +2.5 / +3.7 | +2.7 / +3.3 | +2.4 / +3.9 | +1.3 / +2.5 | 42% |
| Pull-up 2 | eff b10 | +0.7 / +3.3 | -0.0 / +3.4 | +1.1 / +3.2 | +0.6 / +2.3 | 40% |
| Under 10 ft | vol b5 | -0.1 / +5.0 | +0.2 / +7.1 | -0.2 / +4.0 | -0.1 / +6.3 | 61% |
| Under 10 ft | vol b10 | -0.0 / +2.0 | +1.0 / +2.7 | -0.5 / +1.7 | -0.8 / +1.1 | 51% |
| Under 10 ft | eff b5 | +3.4 / +2.7 | +3.8 / +2.9 | +3.2 / +2.6 | +0.3 / -0.4 | 80% |
| Under 10 ft | eff b10 | +2.7 / +1.8 | +0.7 / +1.9 | +3.7 / +1.7 | +0.7 / -1.0 | 63% |
| Wide open | vol b5 | +3.4 / +3.3 | +4.6 / +3.3 | +2.8 / +3.4 | +1.3 / -0.4 | 58% |
| Wide open | vol b10 | +2.2 / +3.2 | +3.7 / +4.3 | +1.5 / +2.6 | -0.2 / +1.1 | 47% |
| Wide open | eff b5 | -0.1 / -0.3 | +1.2 / +1.2 | -0.8 / -1.1 | -1.3 / -0.8 | 44% |
| Wide open | eff b10 | -0.6 / -1.5 | +0.1 / -1.0 | -0.9 / -1.7 | -0.6 / -2.6 | 40% |
| Rim 0-3 ft | vol b5 | +3.0 / +3.4 | +3.5 / +4.5 | +2.8 / +2.8 | +2.0 / +2.3 | 63% |
| Rim 0-3 ft | vol b10 | +2.0 / +2.4 | +2.0 / +2.6 | +2.0 / +2.2 | +1.2 / +1.5 | 50% |
| Rim 0-3 ft | eff b5 | +2.9 / +3.3 | +2.9 / +3.7 | +2.9 / +3.1 | -0.8 / +2.4 | 72% |
| Rim 0-3 ft | eff b10 | +2.0 / +2.8 | +1.9 / +2.9 | +2.1 / +2.8 | -0.3 / +1.1 | 63% |
| Short paint 3-10 ft | vol b5 | +0.4 / +0.1 | +1.3 / -0.1 | -0.1 / +0.2 | +0.2 / -1.0 | 35% |
| Short paint 3-10 ft | vol b10 | -0.1 / +0.0 | -0.2 / +0.7 | -0.1 / -0.3 | +0.8 / -0.0 | 32% |
| Short paint 3-10 ft | eff b5 | +2.2 / +3.8 | +0.2 / +4.9 | +3.3 / +3.3 | +1.5 / +0.7 | 59% |
| Short paint 3-10 ft | eff b10 | +1.7 / +1.1 | +0.4 / +2.0 | +2.4 / +0.6 | +1.6 / -0.5 | 47% |
| Mid-range | vol b5 | -0.7 / -1.7 | -0.4 / -0.5 | -0.8 / -2.3 | -0.6 / -0.2 | 18% |
| Mid-range | vol b10 | -1.0 / -1.2 | -1.5 / -0.4 | -0.8 / -1.6 | -0.4 / +1.1 | 21% |
| Mid-range | eff b5 | +2.2 / +4.2 | +2.5 / +4.0 | +2.0 / +4.3 | +0.0 / +3.5 | 49% |
| Mid-range | eff b10 | +1.7 / +2.3 | +1.3 / +2.2 | +1.8 / +2.3 | +0.6 / +2.4 | 42% |
| Corner 3 | vol b5 | -0.7 / +1.3 | +0.5 / +1.8 | -1.2 / +1.1 | -1.3 / +0.4 | 49% |
| Corner 3 | vol b10 | +1.9 / +0.6 | +3.3 / +0.9 | +1.2 / +0.4 | +0.2 / +0.9 | 44% |
| Corner 3 | eff b5 | -3.1 / +0.7 | -4.4 / +0.8 | -2.4 / +0.7 | -2.6 / -0.7 | 46% |
| Corner 3 | eff b10 | -1.8 / +1.4 | -2.5 / +1.7 | -1.5 / +1.2 | -1.3 / +0.6 | 39% |
| Above-break 3 | vol b5 | +2.0 / +1.7 | +4.7 / +2.4 | +0.7 / +1.3 | +1.2 / -2.3 | 54% |
| Above-break 3 | vol b10 | +1.6 / +0.1 | +2.4 / +0.9 | +1.3 / -0.3 | +1.1 / -2.4 | 40% |
| Above-break 3 | eff b5 | +2.3 / -0.3 | +3.3 / +0.0 | +1.8 / -0.4 | +3.0 / -4.5 | 59% |
| Above-break 3 | eff b10 | +2.1 / -0.5 | +2.8 / -1.2 | +1.7 / -0.1 | +1.4 / -2.5 | 52% |
| Transition (proxy) | vol b5 | +1.9 / +5.2 | +1.9 / +7.6 | +1.9 / +4.0 | +0.1 / +3.3 | 61% |
| Transition (proxy) | vol b10 | +2.9 / +4.0 | +3.0 / +5.4 | +2.9 / +3.2 | +1.6 / +3.0 | 55% |
| Transition (proxy) | eff b5 | +1.6 / +0.5 | -0.8 / +1.2 | +2.8 / +0.1 | +2.0 / -1.5 | 59% |
| Transition (proxy) | eff b10 | +1.1 / +1.1 | -0.3 / +2.8 | +1.9 / +0.2 | +1.4 / -1.5 | 53% |
| Free-throw rate | vol b5 | -0.6 / +3.9 | -2.0 / +3.9 | -0.0 / +3.8 | -0.1 / +0.1 | 51% |
| Free-throw rate | vol b10 | +0.1 / +1.9 | -0.1 / +2.0 | +0.1 / +1.8 | -0.3 / -0.3 | 45% |
| ML C&S | ml b5 | +1.6 / +4.7 | +1.7 / +5.6 | +1.3 / +1.6 | -2.3 / +2.2 | 56% |
| ML C&S | ml b10 | +2.1 / +2.8 | +2.3 / +3.8 | +1.5 / -0.6 | -0.1 / +0.6 | 50% |
| ML Pull Up | ml b5 | +0.9 / +0.2 | +2.2 / +0.3 | -0.2 / +0.2 | +2.4 / +2.1 | 24% |
| ML Pull Up | ml b10 | -0.5 / -0.3 | +0.5 / -1.1 | -1.4 / +0.3 | +0.5 / +2.2 | 26% |
| ML <10ft | ml b5 | +3.7 / +4.0 | +3.3 / +4.4 | +7.3 / +1.0 | +1.0 / +3.4 | 78% |
| ML <10ft | ml b10 | +3.3 / +4.6 | +3.2 / +4.6 | +4.6 / +4.0 | +2.5 / +3.5 | 66% |
| ML PITP | ml b5 | +2.4 / +3.6 | +2.2 / +3.8 | +6.2 / -0.4 | -0.2 / +4.1 | 79% |
| ML PITP | ml b10 | +2.7 / +4.1 | +2.3 / +4.2 | +7.8 / +1.9 | +2.1 / +2.3 | 66% |
| ML Mid | ml b5 | -0.4 / +1.3 | +1.2 / +1.5 | -0.5 / +1.2 | -0.2 / +3.0 | 27% |
| ML Mid | ml b10 | +0.0 / +1.1 | +1.6 / +1.6 | -0.1 / +1.0 | -0.7 / +2.2 | 29% |
| ML 3PT | ml b5 | +3.9 / +2.8 | +4.1 / +3.1 | +2.4 / +1.3 | +2.9 / -0.4 | 59% |
| ML 3PT | ml b10 | +3.9 / +2.0 | +4.1 / +2.6 | +2.9 / -1.6 | +2.2 / -2.1 | 52% |

### Table 4. Do per-player reads carry from 2024-25 into 2025-26?

| Rows | Group by 2024-25 difference | Rows | Positive again in 2025-26 | Mean 2025-26 difference |
|---|---|---|---|---|
| Opponent leg alone | +10 or more | 4,798 | 51.7% | +1.8 |
| Opponent leg alone | -10 to +10 | 9,388 | 51.9% | +1.6 |
| Opponent leg alone | -10 or less | 4,043 | 52.2% | +1.6 |
| Cross (leans on it AND opponent bottom) | +10 or more | 1,671 | 54.3% | +3.0 |
| Cross (leans on it AND opponent bottom) | -10 to +10 | 3,002 | 53.4% | +2.4 |
| Cross (leans on it AND opponent bottom) | -10 or less | 1,300 | 56.1% | +2.8 |

Per-player headline opponent rows with enough games both seasons: 18,229. Lead both seasons: 4,455. Negative both seasons: 3,732. Flat: 1,395. Reversed: 8,155. Too few games: 0.

### Table 5. Strongest per-player opponent-leg leads (positive both seasons, 10+ present games each season)

Read with Table 4: these held for two seasons, but the same screen run on negatives finds as many rows, and per-player reads did not carry forward as a group. Full list: `layer_e_leads.csv`; every player, type and condition: `layer_e_per_player.csv`.

| Player | Shot type | Condition | 2024-25 present / absent | 2025-26 present / absent |
|---|---|---|---|---|
| Isaiah Collier (PG) | Matchup Lab <10ft | Matchup Lab rank 26-30 | 6/10 vs 7/59 | 7/11 vs 13/47 |
| Steven Adams (C) | Matchup Lab PITP | Matchup Lab rank 21-30 | 6/14 vs 3/32 | 7/10 vs 3/14 |
| P.J. Washington (PF) | Catch-and-shoot 3 | Volume allowed, bottom 10 | 14/22 vs 5/28 | 5/11 vs 5/35 |
| Kel'el Ware (C) | Catch-and-shoot 3 | eFG allowed, bottom 5 | 6/12 vs 9/47 | 7/13 vs 13/54 |
| Tidjane Salaün (PF) | Catch-and-shoot 3 | Volume allowed, bottom 10 | 7/12 vs 9/40 | 5/11 vs 3/19 |
| Kristaps Porziņģis (C) | Rim (0-3 ft) | Volume allowed, bottom 10 | 8/15 vs 5/21 | 4/10 vs 0/14 |
| Jaden McDaniels (SF) | Wide open | Volume allowed, bottom 5 | 7/11 vs 11/61 | 7/14 vs 10/48 |
| Jae'Sean Tate (SF) | Matchup Lab PITP | Matchup Lab rank 21-30 | 9/17 vs 6/26 | 6/18 vs 1/23 |
| Josh Giddey (PG) | Transition (proxy) | Volume allowed, bottom 10 | 6/15 vs 4/39 | 7/13 vs 8/32 |
| Xavier Tillman (PF) | Under 10 ft | Volume allowed, bottom 10 | 4/11 vs 1/13 | 4/13 vs 0/10 |
| Isaiah Collier (PG) | Matchup Lab PITP | Matchup Lab rank 26-30 | 4/10 vs 6/52 | 9/12 vs 11/46 |
| Alex Sarr (C) | Wide open | Volume allowed, bottom 10 | 6/13 vs 5/47 | 6/11 vs 7/26 |
| Bronny James (PG) | Matchup Lab C&S | Matchup Lab rank 21-30 | 4/11 vs 1/11 | 5/10 vs 4/25 |
| Devin Booker (PG) | Matchup Lab PITP | Matchup Lab rank 26-30 | 6/11 vs 12/44 | 5/12 vs 5/41 |
| Ziaire Williams (SG) | Matchup Lab PITP | Matchup Lab rank 21-30 | 8/14 vs 10/33 | 6/14 vs 3/34 |

## Data and checks

- **Frame:** NBA.com player game logs (regular season, minutes > 0): 52,952 player-games (26,303 in 2024-25, 26,649 in 2025-26). DK points from the box match BigDataBall's DFS feed exactly on 52,695 of 52,951 rows; the 256 differences are paired stat corrections (`build/dk_mismatches.csv`). All 47,039 rows of Codex's `research_games.parquet` are reproduced (DK points identical on 99.5%, FGA 99.9%, usage 99.99%); my frame has 373 extra rows, all appearances under 1.3 minutes that Codex dropped.
- **Tracking:** Codex's repaired 2024-25 and 2025-26 files plus the 2026-10-13 backfill for 2025-03-11 to 04-13. Quarantined rows (2,309, 7% of FGA) are left out of player shares; team totals are scaled up when clean players cover 70%+ of a team's FGA (spec v1.1).
- **Play-by-play:** 410,560 shots parsed; per player-game FGA match the box on 99.9% and 3PA on 99.95%. Corner share of 3PA 25.7% / 26.1%; transition proxy agrees with BigDataBall's fast-break tag on 95% of 2025-26 shots. 2024-25 games after 2025-03-24 are left out of play-by-play types (BigDataBall stops there; NBA.com refused connections from both the cloud and the Mac's sandbox).
- **Matchup Lab rebuild:** against the dashboard's own 2026-03-26 data, team C&S, pull-up and under-10 FGA allowed correlate 0.99 / 0.97 / 0.99 and final ranks 0.88 / 0.81 / 0.95. The dashboard's PITP counts about 34 FGA a game against 43 here, so its paint area is narrower; ranks still correlate 0.88.
- **Independent review:** an independent reviewer recomputed the upside flags (0 of 51,859 differ), 200 DK scores, every opponent rank for three types on all 327 dates (0 mismatches), four pooled rows, the DRtg control and the carry-over claim, and found no look-ahead. Verdict PASS WITH FIXES: four rule fixes (cutoffs used only past states, ranks across all 30 teams with ties to the more generous rank, exact-zero rows no longer called reversed, a fixed position tie-break), all applied and the numbers above rerun. No headline changed sign. `REVIEW_LAYER_E.md`.

## Files

- `layer_e_per_player.csv`: every qualifying player x shot type x headline condition, opponent leg alone, player leg alone and cross, with upside counts present and absent and the difference, both seasons, usage-tier mix, status (lead / flat / negative / reversed / too few games).
- `layer_e_leads.csv`: rows positive in both seasons with 10+ present games each season.
- `build/pooled_overall.csv`, `build/pooled_by_position.csv`, `build/controls.csv`: pooled counts for every condition including last-10 and adjusted windows.
- `build/*.py`: the scripts, in run order.
