# Layer E condition spec: shot type vs funnel (frozen before any outcome is counted)

Written 2026-10-15 by the NBA build thread, under plan v2 section 1 (method) and section 5 (layer E). This file is hashed into `SPEC_FREEZE.json` before the first upside count is run. Any later change gets a new version and a changelog line; results built on an earlier version are labelled with it.

## 1. Population

- Regular-season games only (NBA.com game id prefix `002`), 2024-25 and 2025-26. NBA Cup group games count (they are regular season). The Cup final (`006…`), play-in (`005…`) and playoffs (`004…`) are excluded.
- A player-game is any appearance with minutes > 0 in NBA.com `playergamelogs` (full box for both seasons).
- Player qualifies for the per-player tables with at least 20 regular-season games across the two seasons.

## 2. Outcome

- **DK points** computed from the NBA.com box with DraftKings NBA Classic scoring (PTS 1, 3PM 0.5, REB 1.25, AST 1.5, STL 2, BLK 2, TOV -0.5, double-double 1.5, triple-double 3). Checked against BigDataBall's DFS feed DK points; mismatches listed.
- **Upside game** = DK points at or above the player's own 75th percentile across all his qualifying games in both seasons (pandas `quantile(0.75)`, linear interpolation). Fixed once for the historical study. No league-wide or value outcomes.

## 3. Shot types

| Key | Type | Source | Seasons covered |
|---|---|---|---|
| cs3 | Catch-and-shoot 3PA | NBA.com tracking per player per date (Codex repaired file + 2026-10-13 backfill; quarantined rows dropped) | Both, full |
| pu3 | Pull-up 3PA | tracking `pu` FG3A | Both, full |
| pu2 | Pull-up 2PA | tracking `pu` FGA - FG3A | Both, full |
| lt10 | FGA under 10 ft | tracking `lt10` | Both, full |
| wo | Wide-open FGA (closest defender 6+ ft) | tracking `wo` | Both, full |
| rim | 2PA at 0-3 ft | BigDataBall play-by-play shot distance | 2025-26 full; 2024-25 through 2025-03-24 |
| paint | 2PA at more than 3 and up to 10 ft | play-by-play | same |
| mid | 2PA beyond 10 ft | play-by-play | same |
| c3 | Corner 3PA (3PA taken within 9 ft of the baseline-basket line, i.e. NBA LOC_Y <= 90) | play-by-play coordinates | same |
| atb3 | Above-the-break 3PA (all other 3PA) | play-by-play | same |
| trans | Transition FGA, **proxy**: FGA taken within 6 seconds of the shooting team gaining the ball on a defensive rebound or an opponent turnover. Same rule both seasons (2024-25 files have no fast-break qualifier); cross-checked against BDB's `fastbreak` qualifier in 2025-26 | play-by-play | same |
| ftr | Free-throw rate (FTA per FGA) | NBA.com box | Both, full |

Heaves (BDB event type `heave`) are excluded. For play-by-play types, 2024-25 games after 2025-03-24 are **excluded** from that type's counts (no play-by-play on the Mac; NBA.com is not reachable from the sandboxes). Tracking and box types use the full season.

## 4. Player leg (pregame)

- **Share** of a type = his attempts of that type / his FGA (for ftr: FTA / FGA), over his earlier games this season (season-to-date before the game date). If he has fewer than 5 earlier games this season, his full previous-season share is used when he had 10+ games then; otherwise the leg is unavailable for that game.
- **Strong in the type** = share in the top third among players at his DK position group on that date (players with an available share). Position group = the first DK position listed in BigDataBall's DFS feed (PG, SG, SF, PF, C), most common across his games.
- Prior-10 share is stored as a column but not used for the headline.

## 5. Opponent leg (pregame, as of date)

For each team and type, from that team's earlier games this season only (strictly before the game date):

- **Volume allowed** = opponents' attempts of the type per 100 opponent possessions (NBA.com team `POSS`). For ftr: opponents' FTA per 100 possessions.
- **Efficiency allowed** = opponents' eFG% on the type ((FGM + 0.5 x 3PM) / FGA). Not defined for ftr.
- **Windows**: season-to-date (headline) and last 10 games (secondary).
- **Opponent-adjusted** (secondary): for each earlier game, the opposing offense's rate in that game minus that offense's own season-to-date rate before the game date in its other games; averaged over the team's earlier games.
- **Rank of 30**, 1 = stingiest (fewest attempts allowed, or lowest eFG allowed); 30 = most generous. Ranked across all 30 teams on each date. A rank exists only once the team has played 10 games this season; before that the condition is unavailable and the game is left out of that condition's counts (neither present nor absent).
- **Bottom 5** = rank 26-30. **Bottom 10** = rank 21-30.

## 6. Ramneik's Matchup Lab composite (rebuilt as of date)

Rebuilt from `nba-dashboard/app.js` and `data.json` meta ("Composite rank: FG% + FGA Volume (L7 + Season). Rank 30 = worst defense"):

- Tracking types C&S (`cs` all FGA), Pull Up (`pu` all FGA), <10ft (`lt10`): composite = mean of four ranks (L7 FG% allowed, L7 FGA allowed per game, season FG% allowed, season FGA allowed per game; each 30 = most allowed), re-ranked 1-30.
- Zones PITP, Mid, 3PT (play-by-play; PITP = 2PA inside the painted area, Mid = other 2PA, 3PT = all 3PA): composite = mean of season FGA-allowed rank and season FG%-allowed rank, re-ranked (as the dashboard's `*_def_rank`).
- Player leg as the dashboard uses it: his share of FGA in that zone or play type >= 20% (earlier games this season, same fallback as section 4).
- Conditions: ML rank 26-30 (the dashboard's lightning tier) and ML rank 21-30. Synergy-only play types (transition, spot-up, PnR, iso, post, handoff) cannot be rebuilt as of date (season totals only) and are not counted.

## 7. Conditions counted

Per player x type x season (2024-25 and 2025-26 side by side):

1. **Opponent leg alone**: vol_b5, vol_b10, eff_b5, eff_b10 (season-to-date, headline); the same on L10 and adjusted (secondary); ml_b5, ml_b10 for the six ML types.
2. **Player leg alone**: strong in the type (ML: share >= 20%).
3. **Cross**: player leg present AND opponent condition present, against all other games.

Each row reports: games present, upside games when present, games absent, upside when absent, the forward rate both ways, and the difference (rate present minus rate absent, percentage points). Both counting directions are given: "present in a of A upside games vs b of B other games".

Beside each player: usage tier (season-to-date BigDataBall usage rate before the game, top / middle / bottom third within position group on that date) shown as the share of his games in each tier.

Pooled rows: the same counts pooled across all qualifying players, by position group and overall.

## 8. How leads are ranked (fixed now)

- A per-player **lead** = an opponent-leg or cross condition whose difference is positive in **both** seasons with at least 5 present games in each season. Ranked by the smaller of the two seasons' differences. Present games under 10 in either season are labelled **small**.
- A cross that does not beat the same player's leg-alone difference in both seasons is labelled **"player leg restated"**.
- **Flat** = difference within +/-5 points in both seasons. **Reversed** = opposite signs. These are reported as such, never as positive.
- Family size is stated with every lead list (how many player x type x condition rows were looked at), so a lead is read against how many chances there were.
- No p-values, no shuffles, no gates, no scores, no weights.

## 9. Labels

All conditions in this spec are pregame. No in-game facts are used in layer E. Every table states the season, the condition, the window, and the counts.

## Changelog

- **v1.1 (2026-10-15, before any upside count):** team-level handling of quarantined tracking rows, which v1 left unstated. A team-game's tracking totals are scaled up by (team FGA / FGA of players with clean tracking) when clean players cover at least 70% of the team's FGA; below 70% the team-game is left out of that team's tracking allowance. Without this, 36% of team-games would drop out because one player row was quarantined. Matchup Lab PITP here is the whole painted area (about 43 FGA a game); the dashboard's own PITP averages about 34, so its zone source counts a narrower area. Ranks agree closely anyway (team FGA allowed correlation 0.88; C&S 0.99, pull-up 0.97, under 10 ft 0.99).
- **v1.2 (2026-10-15, after the first count; disclosed):** fixes from the independent review, none changing a headline's sign. (a) "Strong in the type" and usage-tier cutoffs on a date now use every player's state after his last game before that date (v1 used players who played again on or after the date, which depended on future appearances). (b) Ranks are taken across all 30 teams and then hidden for teams with under 10 games (v1 ranked only eligible teams); tied values take the more generous rank. (c) Rows with an exact zero difference in a season are "other", not "reversed". (d) Position group ties are broken by the position in his most recent game. (e) Report label added: a cross where the player leg is present in nearly every game is noted as "player leg present nearly every game (cross = opponent leg for him)".
