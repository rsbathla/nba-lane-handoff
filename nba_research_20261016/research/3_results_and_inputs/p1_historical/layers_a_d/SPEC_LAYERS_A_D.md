# Layers A to D condition spec (frozen before any upside count in these layers)

Written 2026-10-15 by the NBA build thread under plan v2 sections 1, 5 and 8. Same population, outcome and counting rules as `../layer_e/SPEC_LAYER_E.md` sections 1, 2, 7 and 8 (regular season, 2024-25 and 2025-26, players with 20+ games, own top-quarter DK upside, counts both ways, both seasons side by side, leads ranked by the smaller season difference, flat within +/-5, small under 10 present games). Every condition is labelled **pregame**, **lock-time** or **in-game**. "Earlier games" always means games strictly before the game date in the same season unless a previous-season fallback is stated.

## Layer A: usage and role (the NFL's role tier)

Tier facts, each a top / middle / bottom third within DK position group on the date (cutoffs from every player's state entering his next game, as in layer E). A player needs 5 earlier games this season; with fewer, his previous-season value is used if he had 10+ games then.

| Key | Condition | Label | Source |
|---|---|---|---|
| A1 | Season-to-date usage rate (mean of BigDataBall per-game usage) | pregame | BDB DFS feed |
| A2 | Prior-10 usage rate | pregame | same |
| A3 | Season-to-date minutes per game | pregame | NBA.com box |
| A4 | Prior-10 minutes per game | pregame | same |
| A5 | FGA share of team FGA in his games, season-to-date | pregame | box |
| A6 | Assist share of team assists in his games, season-to-date | pregame | box |
| A7 | Potential assists per game, season-to-date | pregame | NBA.com daily player passing (2026-10-13 capture) |
| A8 | Rebound chances per game, season-to-date | pregame | NBA.com daily player rebounding |
| A9 | Started this game | **lock-time** (confirmed starters) | BDB DFS feed starter flag |
| A10 | Started at least 3 of his prior 5 games | pregame | same |
| A11 | Rotation spot: 5th to 9th on his team by season-to-date minutes among players who appeared in the team's previous game | pregame | box |
| A12 | DK salary top / middle / bottom third within position on the slate date | pregame | BDB DFS feed |

The NFL-style tier table: share of games reaching upside in each third, per position group and overall, both seasons.

**In-game shape (labelled in-game, never used as a lead):** minutes above his own median; usage above his own median; FGA above his own median. Each upside game is also split into "more minutes" (minutes above his own median) vs "more per minute" (DK per minute above his own median), per plan section 8.

## Layer B: absences (teammate played 0 minutes)

A teammate is **out** for a game if he appeared for this team earlier this season, did not appear in this game, and his next appearance (if any) is for the same team (so traded or waived players are not counted as out). Per decision 5 this is treated as known before the game; reports label it "played 0 minutes".

| Key | Condition (pregame by decision 5) |
|---|---|
| B1 | The team's top season-to-date usage player (5+ games) is out, and it is not this player |
| B2 | The team's top season-to-date assist-share player is out |
| B3 | The team's most frequent starting center (by starts this season) is out |
| B4 | A teammate who starts at this player's DK position group (most frequent starter there) is out |
| B5 | Two or more rotation teammates out (rotation = 20+ season-to-date minutes per game, 5+ games) |
| B6 | Any teammate with 25%+ season-to-date usage is out |

Question asked: who absorbs the usage (counts by teammate role and by this player's usage tier), and does this player's upside rate move when present vs absent, per player.

**Player-specific on/off prior (B7, pregame):** this player's usage share (FGA + 0.44 FTA + TOV per 100 of his on-court team plays) with teammate X off the floor vs on, from play-by-play lineups in earlier games, for X = the B1 player. Condition: his off-court share is at least 3 points higher than his on-court share, with 100+ minutes in each state. Counted only on nights B1 is present. 2025-26 full; 2024-25 through 2025-03-24.

## Layer C: pace, line and script

| Key | Condition | Label | Source |
|---|---|---|---|
| C1 | Opening implied team total top / middle / bottom third on the date (total/2 minus spread/2 for his team) | pregame | BDB team feed |
| C2 | Opening spread: his team favoured by 8+; within 4.5 either way; underdog by 8+ | pregame | same |
| C3 | Opening game total top / bottom third of the season so far | pregame | same |
| C4 | Both teams' season-to-date pace (possessions per 48) top third of the league | pregame | NBA.com team logs |
| C5 | Back-to-back (0 days rest) for his team | pregame | box dates |
| C6 | Home | pregame | box |
| C7 | Closing spread / total, same cuts as C1 to C3 | **lock-time** | BDB team feed |
| C8 | Line moved 1.5+ points toward his team (spread) or 3+ up (total) | **lock-time** | same |
| C9 | Final margin 15+ either way | **in-game** | box |
| C10 | Overtime | **in-game** | box |
| C11 | He had 5+ fouls | **in-game** | box |

BigDataBall's team feed covers 2025-26 fully but 2024-25 only through 2025-03-24; line conditions are counted only where the feed has the game. C1 to C3 are also read inside each layer A usage tier (A1), which is the NFL's key cut.

## Layer D: general defensive weakness (opponent alone)

Disclosure: D1 bottom 5 and bottom 10 (season-to-date) was already counted once, as a control in the layer E report (upside 30.2% vs 25.5% in 2024-25, 31.2% vs 25.7% in 2025-26). D1 is therefore not a fresh condition; its definition here is unchanged from that control.

All as of date from the opponent's earlier games; rank of 30, 30 = most generous; ranked once the opponent has 10 games; bottom 5 = 26-30, bottom 10 = 21-30.

| Key | Condition |
|---|---|
| D1 | Opponent defensive rating (points allowed per 100 possessions) |
| D2 | Opponent DK points allowed per game to this player's DK position group (DvP) |
| D3 | D2 opponent-adjusted: each earlier game's DK points by that position minus those players' own season-to-date averages, averaged |
| D4 | Opponent defensive rebound rate allowed (opponent offensive rebound % against them) |
| D5 | Opponent turnovers forced per 100 (bottom = forces fewest) |
| D6 | Opponent rim protection: rim eFG allowed (from layer E play-by-play) and blocks per 100 |
| D7 | Opponent fouls: opponents' FTA per 100 possessions allowed |

## Sweep (after A to D)

Every pair of pregame conditions from A to E, read inside each usage tier (A1) and position group, counted both seasons; reported as ranked leads with the family size stated, crosses shown with both legs alone, a cross that only restates a leg named as such. Lock-time conditions enter the sweep in their own family. In-game conditions never enter it.

## Labels

Pregame, lock-time and in-game columns are kept separate in every table. No combined scores, no counts of how many conditions are on.

## Changelog

- **v1.1 (2026-10-15, after the first A-D count, before the sweep):** (a) Same fixes as layer E v1.2: tertile cutoffs on a date use only players' states from games before that date (here, each player's entering state for his last game before the date); ranks are taken across all 30 teams, ties to the more generous rank, then hidden under 10 games. (b) B7 (on/off usage prior) is deferred until after the P3 template slate because of the opening-night deadline; it is reported as not yet counted. (c) Sweep rules fixed before the sweep runs: conditions = every pregame binary condition in A (each tier level), B, C, D and layer E's headline opponent conditions and player legs; cells = condition pair x usage tier (A1) x position group, pooled across players; a cell is read only with 30+ present games in each season; a **cross lead** = difference positive both seasons AND larger than each leg's own difference in the same cell group in both seasons, ranked by the smaller of the two seasons' margins over the better leg; everything else is reported by count (restates a leg / flat / reversed).
- **v1.2 (2026-10-15, after the independent review of the A-D count, sweep and P2; disclosed):** (a) A11 ranks every player who appeared in the team's previous game by his season-to-date minutes after that game (v1.1 ranked only those also playing tonight, which used tonight's absences). (b) Layer B roles drop players whose latest appearance before the date was for another team; top usage and top assist share are minutes-weighted means and need 15+ minutes per game (also for the B6 25%+ usage list); start-count ties go to the player with more minutes. (c) "Out" also requires that his latest appearance before the date was for this team (what the build always did); a player who never appears again is out for the rest of the season. (d) Lines join to teams by team name, so neutral-site games get each team's own spread. (e) The A1 usage tier is the sweep's cell and is removed from the sweep's condition family (130 conditions). (f) Crosses are also counted as a 2x2 (both / one only / other only / neither) and reported as the interaction against additive. (g) Recorded deviations: A12 salary tertiles use the players who played that day (BigDataBall's DFS feed lists no one else); A2/A4 have no previous-season fallback; C1/C3/C7 thirds are cut from season-to-date team-games before the date, not the slate.
