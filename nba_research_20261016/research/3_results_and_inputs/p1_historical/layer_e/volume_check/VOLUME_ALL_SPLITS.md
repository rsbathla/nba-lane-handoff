# Every shot type x every defense split: does it raise HIS volume?

Asked by Ramneik on 2026-10-15 ("do every split/shot type"), following `VOLUME_CHECK.md`.

- **Scripts:** `../build/24_volume_all.py` and `../build/24b_volume_control.py`.
- **Data:** `volume_all_wide.csv` (every type x split x cut x player group, both seasons), `volume_all_long.csv.gz`, `volume_all_per_player_repeat.csv`, `volume_control_total_fga.csv`.

## Verdict

1. **"Volume allowed" works and the other splits don't.**
   - When the opponent is bottom 10 in raw attempts allowed of a type (season or last 10), players take more of that type than their own average in **255 of 264** type x group x season rows, with none fewer, across every position and usage tier.
   - The Matchup Lab composite does the same: 118 of 132.
   - Efficiency allowed (eFG% allowed) does **not** move volume: rows split between more, fewer and mixed. A defense that lets shots go in does not make players take more of them.
   - Opponent-adjusted volume also does not move volume (mostly mixed). The raw "allowed" number is the one that carries the signal.
2. **The rise is about +0.1 to +0.45 attempts a game.**
   - The largest rises are short paint, rim, catch-and-shoot 3, wide open, free throws, and under 10 ft in 2025-26.
   - Pull-up 3 barely moves (+0.03 / +0.08).
3. **For some types it is a real shift in shot mix; for others it is just more shots.** I compared each type's rise with the rise in his total FGA under the same split:
   - **Real shift in shot mix:** rim (+0.36 / +0.44 rim attempts with total FGA -0.20 / +0.06), short paint (+0.45 / +0.43 with total FGA +0.08 / -0.02), free throws (+0.26 / +0.35 FTA with total FGA down).
   - **Mostly more shots overall:** catch-and-shoot 3 (+0.34 / +0.35 C&S with total FGA +0.30 / +0.33), wide open, mid-range, corner 3, transition. Against these defenses he simply shoots more, and C&S rises about in step.
4. **Upside follows volume only weakly.** Strong-in-type players against a bottom-10 raw-volume defense:
   - C&S +4.5 / +3.7, wide open +3.6 / +3.7, transition +3.0 / +5.5, rim +2.0 / +2.7, Matchup Lab under 10 ft +3.2 / +4.7, Matchup Lab paint +2.3 / +4.2.
   - Pull-up 3 is negative (-3.6 / -2.2).
   - These are the same +2 to +5 funnel lifts as layer E, which overlap heavily with simply facing a bad defense (DRtg bottom 5 alone +4.7 / +5.4).
5. **Per player, the direction repeats but the size does not.**
   - On raw-volume splits, about half of strong players (for example 46 of 86 for C&S, 48 of 91 for rim) took more of the type in both seasons; only 3 to 16 took fewer in both.
   - How big his bump was in 2024-25 barely predicts 2025-26 (correlations -0.1 to +0.26; rim and short paint are the best at about +0.2).

**For the board:** use raw volume allowed (season or last 10) or the Matchup Lab composite, not efficiency allowed and not opponent-adjusted. Read rim, paint and FTA funnels as real shot-diet shifts. Read C&S, wide-open and mid funnels as "more shots overall." Treat all of them as a small nudge (about a third of an attempt), still behind absences, starting and minutes.

## Table 1. Attempts of the type vs his own average: bottom-10 defense minus other games (strong-in-type players; 2024-25 / 2025-26)

| type                     | Vol season    | Vol L10       | Vol adj season   | Vol adj L10   | Eff season    | Eff L10       | Eff adj season   | Eff adj L10   | Matchup Lab   |
|:-------------------------|:--------------|:--------------|:-----------------|:--------------|:--------------|:--------------|:-----------------|:--------------|:--------------|
| catch-and-shoot 3        | +0.34 / +0.35 | +0.30 / +0.33 | -0.06 / +0.06    | -0.07 / +0.04 | -0.11 / +0.08 | -0.05 / +0.04 | +0.01 / +0.13    | +0.05 / +0.02 |               |
| pull-up 3                | +0.03 / +0.08 | +0.09 / +0.07 | +0.12 / +0.03    | +0.03 / -0.01 | -0.06 / +0.01 | -0.01 / -0.00 | -0.01 / +0.01    | +0.03 / -0.07 |               |
| pull-up 2                | +0.15 / +0.31 | +0.18 / +0.27 | +0.01 / -0.05    | -0.01 / -0.06 | +0.05 / -0.02 | +0.02 / +0.01 | -0.13 / +0.10    | -0.15 / +0.05 |               |
| under 10 ft              | +0.09 / +0.31 | +0.25 / +0.28 | +0.16 / -0.09    | +0.01 / -0.15 | +0.04 / +0.09 | -0.02 / +0.07 | -0.17 / +0.12    | -0.05 / -0.06 |               |
| wide open                | +0.30 / +0.29 | +0.32 / +0.28 | -0.09 / +0.07    | -0.10 / +0.12 | -0.11 / -0.12 | -0.10 / -0.04 | -0.01 / -0.04    | +0.02 / +0.01 |               |
| rim (0-3 ft)             | +0.36 / +0.44 | +0.44 / +0.37 | +0.07 / -0.02    | +0.01 / -0.05 | -0.04 / -0.02 | -0.06 / -0.07 | -0.03 / -0.08    | -0.04 / -0.04 |               |
| short paint (3-10 ft)    | +0.45 / +0.43 | +0.40 / +0.34 | -0.18 / +0.09    | -0.03 / +0.14 | +0.14 / +0.18 | +0.04 / +0.11 | -0.10 / -0.13    | -0.01 / -0.08 |               |
| mid-range 2              | +0.19 / +0.19 | +0.16 / +0.25 | +0.07 / -0.06    | -0.00 / -0.06 | +0.08 / +0.01 | +0.02 / +0.03 | -0.17 / +0.07    | -0.06 / +0.05 |               |
| corner 3                 | +0.12 / +0.18 | +0.05 / +0.20 | -0.04 / +0.01    | +0.02 / +0.02 | -0.10 / +0.04 | -0.03 / -0.05 | -0.00 / +0.06    | +0.01 / -0.00 |               |
| above-break 3            | +0.27 / +0.14 | +0.16 / +0.09 | +0.08 / +0.00    | -0.09 / -0.06 | +0.03 / -0.03 | -0.14 / -0.01 | -0.02 / -0.05    | -0.01 / +0.07 |               |
| transition               | +0.20 / +0.15 | +0.16 / +0.14 | +0.05 / +0.05    | +0.04 / -0.03 | +0.10 / +0.10 | +0.06 / +0.09 | -0.01 / +0.09    | +0.03 / +0.03 |               |
| free throws (FTA)        | +0.26 / +0.35 | +0.18 / +0.21 | -0.03 / -0.04    | -0.02 / -0.08 |               |               |                  |               |               |
| ML catch-and-shoot (all) |               |               |                  |               |               |               |                  |               | +0.16 / +0.29 |
| ML pull-up (all)         |               |               |                  |               |               |               |                  |               | +0.12 / +0.17 |
| ML under 10 ft           |               |               |                  |               |               |               |                  |               | +0.19 / +0.32 |
| ML paint                 |               |               |                  |               |               |               |                  |               | +0.10 / +0.34 |
| ML mid                   |               |               |                  |               |               |               |                  |               | +0.40 / +0.36 |
| ML 3PT                   |               |               |                  |               |               |               |                  |               | +0.23 / +0.25 |

## Table 2. Upside lift, percentage points (same games)

| type                     | Vol season   | Vol L10     | Vol adj season   | Vol adj L10   | Eff season   | Eff L10     | Eff adj season   | Eff adj L10   | Matchup Lab   |
|:-------------------------|:-------------|:------------|:-----------------|:--------------|:-------------|:------------|:-----------------|:--------------|:--------------|
| catch-and-shoot 3        | +4.5 / +3.7  | +4.2 / +2.4 | +0.1 / +1.2      | +0.6 / +0.8   | +0.2 / +1.8  | -0.0 / +1.8 | -2.4 / +1.3      | +1.4 / -1.1   |               |
| pull-up 3                | -3.6 / -2.2  | -2.0 / -2.2 | +2.5 / +1.2      | -0.1 / +0.6   | +0.5 / -1.2  | -1.3 / -1.6 | +0.7 / +1.0      | +1.7 / -0.4   |               |
| pull-up 2                | -1.3 / +0.3  | -2.2 / -0.9 | -0.0 / +1.2      | +0.7 / +0.9   | -0.2 / +3.3  | +2.4 / +2.9 | -0.4 / -0.2      | -1.3 / -1.1   |               |
| under 10 ft              | +1.0 / +3.1  | +0.9 / +3.3 | +1.7 / -1.3      | +0.1 / -2.9   | +0.6 / +2.0  | +2.1 / +2.6 | -1.1 / +2.1      | -0.5 / -0.5   |               |
| wide open                | +3.6 / +3.7  | +3.8 / +2.8 | +0.7 / -0.5      | -0.5 / +1.4   | +0.4 / -0.4  | -0.1 / -0.2 | -2.0 / -0.6      | +0.6 / +1.2   |               |
| rim (0-3 ft)             | +2.0 / +2.7  | +3.5 / +2.9 | +0.1 / -0.2      | +1.3 / -0.3   | +1.9 / +2.8  | +0.2 / +1.3 | -1.7 / +1.4      | -1.9 / -0.6   |               |
| short paint (3-10 ft)    | -0.2 / +0.6  | -0.7 / +0.2 | +1.0 / -1.0      | +0.8 / -1.7   | +0.4 / +1.9  | -0.4 / +1.4 | +0.1 / +2.5      | -0.9 / -0.5   |               |
| mid-range 2              | -1.5 / -0.2  | -0.4 / +0.3 | -0.7 / -1.4      | +0.1 / -0.8   | +1.3 / +2.2  | +1.0 / +4.3 | -2.1 / +1.1      | -0.7 / -0.2   |               |
| corner 3                 | +3.3 / +0.7  | +0.5 / +2.0 | -2.2 / +2.4      | +0.6 / -0.7   | -2.5 / +1.6  | -0.0 / -0.0 | +1.0 / +2.6      | -0.3 / +0.4   |               |
| above-break 3            | +2.4 / +0.9  | +2.3 / +0.6 | +1.8 / +0.5      | +0.0 / -1.3   | +2.8 / -1.2  | -1.8 / -0.4 | +0.1 / -1.4      | +1.2 / -1.4   |               |
| transition               | +3.0 / +5.5  | +1.5 / +4.8 | -0.1 / +2.1      | +0.2 / -1.9   | -0.3 / +2.9  | +0.5 / +2.1 | +0.1 / +2.0      | -0.1 / +0.1   |               |
| free throws (FTA)        | -0.1 / +2.1  | +1.2 / +2.0 | +1.5 / +0.9      | +0.6 / -1.2   |              |             |                  |               |               |
| ML catch-and-shoot (all) |              |             |                  |               |              |             |                  |               | +2.5 / +3.9   |
| ML pull-up (all)         |              |             |                  |               |              |             |                  |               | +0.5 / -0.9   |
| ML under 10 ft           |              |             |                  |               |              |             |                  |               | +3.2 / +4.7   |
| ML paint                 |              |             |                  |               |              |             |                  |               | +2.3 / +4.2   |
| ML mid                   |              |             |                  |               |              |             |                  |               | +1.6 / +1.6   |
| ML 3PT                   |              |             |                  |               |              |             |                  |               | +4.1 / +2.6   |

## Table 3. How often each split raises volume (all 12 types and 11 player groups, bottom 5 and bottom 10)

"More" means more attempts than other games in both seasons.

| sp             |   more attempts both seasons |   fewer attempts both seasons |   mixed |   rows |
|:---------------|-----------------------------:|------------------------------:|--------:|-------:|
| Vol season     |                          255 |                             0 |       9 |    264 |
| Vol L10        |                          254 |                             0 |      10 |    264 |
| Vol adj season |                           49 |                            43 |     172 |    264 |
| Vol adj L10    |                           40 |                            68 |     156 |    264 |
| Eff season     |                           76 |                            65 |     101 |    242 |
| Eff L10        |                           64 |                            99 |      79 |    242 |
| Eff adj season |                           41 |                            57 |     144 |    242 |
| Eff adj L10    |                           65 |                            41 |     136 |    242 |
| Matchup Lab    |                          118 |                             1 |      13 |    132 |

## Method

- **Population:** qualifying players (20+ games).
- **Baseline:** his mean attempts of the type over earlier games this season (5+ earlier games).
- **Opponent ranks:** as of the date, ranked against all 30 teams, shown once a team has 10 games.
- **Player groups:** all players; strong in the type (top third of share at his position; Matchup Lab types use the dashboard's 20% share rule); not strong; each position; each usage tier.
- **Upside:** his own top quarter of DK points.
- **Play-by-play coverage:** 2024-25 play-by-play types run only through 2025-03-24.
- **Free throws:** "volume allowed" is FTA allowed per 100 possessions; there is no efficiency split.
- Descriptive counts only.
