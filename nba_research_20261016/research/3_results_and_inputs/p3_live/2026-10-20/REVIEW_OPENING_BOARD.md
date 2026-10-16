# Review: opening-night board 2026-10-20

**Verdict: PASS WITH FIXES.** Lift numbers, upside lines, new-team flags and opponent ranks are correct. Fix D1 before the game-day rebuild: as written, Shai Gilgeous-Alexander, Karl-Anthony Towns, Kentavious Caldwell-Pope, De'Aaron Fox, David Jones-Garcia and Ja'Kobi Gillespie can never be marked Out or day-to-day. D2 to D5 change what the board shows tonight.

I reran `25_opening_board.py` into `/tmp/review_open/out/`, and its board.csv matches the published one byte for byte. My check scripts are in `/tmp/review_open/c*.py`.

## Defects

**D1 (high). Injury names are normalized differently on the two sides, so hyphenated or apostrophe names never match.** `25_opening_board.py:48`
- Evidence: the injury side normalizes `name_key` ("karl anthony towns"), but the slate side normalizes `dk_player`. `norm` deletes the hyphen without a space, which gives "karlanthony towns".
- Six slate players are affected: Gilgeous-Alexander, Towns, Caldwell-Pope, Fox, Jones-Garcia and Gillespie. Towns and Caldwell-Pope are Day-To-Day on the 10-15 report, and the board shows them blank.
- If Gilgeous-Alexander is Out at lock, none of OKC's absence lines (top usage, same-position starter, 2+ rotation) will fire.
- Fix: `s['key']=s.name_key.map(norm)`. The slate already carries a `name_key` in the same form as the injury report. Better still, match on (team, key).

**D2 (medium). The NEG pull-up-3 line is limited to players who lean on pull-up 3s. The approved template shows it for every player.** `25_opening_board.py:87`
- Evidence: in `18_template.py:67`, the line fires whenever `pu3_vol_szn_rk>=26`, with no leg check. LAYER_E_REPORT finding 4 says the negative holds "for leaners and non-leaners alike."
- Tonight BOS ranks 28/30 on pull-up 3s allowed, so every DET player should carry `NEG opp allowed pull-up 3s 28/30 (-1.1)`. Only Duncan Robinson and Taurean Prince do.
- Fix: drop `r.leg_pu3 and` from the condition.

**D3 (medium). Every tip time is 15:00.** `25_opening_board.py:76,89`, `26_opening_games.py:8,12`
- Evidence: the slate's `start_est` is 2026-10-20T15:00 for all 125 rows. Every board row and all three GAMES.md headings say 15:00.
- The schedule capture (`schedule_20261013T003345`) has the real tips: 3:00, 7:00 and 9:30 pm ET, which README states correctly. Game order on the board is also alphabetical rather than by tip.
- Fix: join `tip_et` from the newest schedule capture on (home, away), and sort and label by it.

**D4 (medium). The starter roles (same-position starter, starting C) can name the wrong player, because they combine last season's start counts with this season's DK primary position.** `25_opening_board.py:57-58,68`
- NYK starting C = Andre Drummond (25 starts, all for PHI). DK now lists Towns as PF/C, so his primary slot is PF and he drops out of the C pool, although he was C in the frame with 75 starts. If Drummond is Out, every Knick gets "starting center out (+9.5)".
- BOS PF = Jordan Walsh (25 starts) over Jayson Tatum (16 starts, because he played only 16 games).
- PHI SG = Kentavious Caldwell-Pope (14 starts, for MEM). Edgecombe moved to PG.
- 25 slate players have a DK primary position this season that differs from their 2025-26 frame position.
- Fix: rank by starts among players eligible at the slot (any position in `position_dk`), or by start rate, or by preseason `starter_rate`. Print the role holders per team in GAMES.md so they get a human check at lock.

**D5 (low-medium). The top-playmaker (B2) proxy is not the spec metric, and it changes the holder on 2 of 6 teams.** `25_opening_board.py:55-56`
- Evidence: the spec (v1.2 b) and `13_conds_bcd.py:35,38` use the minutes-weighted per-game share of team assists. The board uses assists per minute instead.
- The per-game share is a ratio within each old team's games, so it stays comparable across old teams. The comment's reason for the proxy does not hold.
- With the proxy: BOS = Tatum (spec: Derrick White) and OKC = Nikola Topic, who played 10 games last season (spec: Gilgeous-Alexander).
- Fix: compute `AST / team AST` per game and minutes-weight it, as in 13_conds_bcd.

**D6 (low). The usage tier is minutes-weighted, but spec A1 is the plain mean of per-game usage.** `25_opening_board.py:22,44`
- Weighting is correct for the B1/B6 roles (v1.2 b). The displayed tier, though, is labelled as A1, the usage tier the study's lifts were sliced by.
- 14 of the matched slate players change tier under the A1 definition, for example John Collins (middle → top), Kevin Huerter (top → middle) and Neemias Queta (middle → bottom).
- Fix: use `L.groupby('PLAYER_ID').usage.mean()` for the tier and keep the weighted value for roles.

**D7 (low). The board shows fewer absence lines than the template.** `25_opening_board.py:68,52`
- The B3 line is suppressed for C-position players (`r.posg!='C'`). The template (`18_template.py:47-48`) shows B3 and B4 together for a backup C.
- The starter pool needs 5+ games (`y=x[gp25>=5]`), but 13_conds_bcd ranks starters among all players.
- Fix: remove the `posg!='C'` guard, and build the starter roles from `x` rather than `y`.

**D8 (low). README misstatements.** `README.md`
- Item 1 calls Quaintance's injury "season-long". The report says only "not yet cleared for basketball activities"; Oweh and Hukporti are the season-ending ones.
- Item 3 does not date the preseason source. `projections_all_rostered.csv` was built 2026-10-13 and holds 1-3 games per player. The path is hard-coded (`25:16`), so a lock-time rerun will still use the 10-13 preseason start rates. Say so, or point the script at a newer pull.
- "No lift line fires yet" should read "no absence line fires yet". Starter-pointer, DvP and shot-type lines do fire.

**D9 (cosmetic).**
- `25:17-18` loads a roster file it never uses. The path sort picks `2026-10-20/roster_20261013…`, the oldest capture, and the script crashes if no roster file exists. Remove it.
- Three slate players have no `person_id`: Christopher Cenac Jr., EJ Harkless and RJ Davis. They have no NBA history, so nothing changes, but the 10-15 roster has Person IDs for Cenac and Harkless if you want to fill them in.

## Checked and correct

1. **Joins.** 122 of 125 slate players have IDs, and the one name that differs (Jones-Garcia vs "Jones Garcia") is the same player. The 33 players not in the frame have no 2025-26 games. The 25 NEW TEAM flags match each player's date-sorted last 2025-26 team exactly.
2. **Upside line.** Recomputed as the 75th percentile of DK points over 2024-25 and 2025-26 regular-season games (no 0-minute rows, no duplicates). It matches on all rows. 38 players with fewer than 20 games show "n<20".
3. **Shot-type leans.**
   - Shares use only games where the tracking source has data (the columns are NaN otherwise), as in 06_legs.
   - The top-third cutoff is taken over 2025-26 players with 5+ games at the same position. The player needs 10+ games, which is stricter than the in-season rule.
   - `tier()` has no bug. Its reference group uses last season's frame position, and the player's own position is this season's DK primary, which is defensible.
4. **Roles: who is considered.**
   - The DK slate covers all 122 players on the 10-15 rosters for these six teams (plus three more), and it includes the long-term Out players. So "only slate players can hold roles" changes nothing tonight.
   - Players who played for these teams last season but are no longer on the roster are correctly left out.
   - The top-usage holders, rotation lists and B5 logic (excluding the player himself, 2+ out) agree with my independent computation.
   - Risk at lock: if DK drops an Out player from the slate, he disappears from both the roles and the outs without any warning. Consider building roles from the roster file and warning when a roster player is missing from the slate.
5. **Opponent ranks.**
   - The opponent-rank file's last 2025-26 row is 2026-04-12, the state entering game 82 (81 games). README's "through April 11" is accurate.
   - Direction is right: DRtg rank 30 = worst defense, with a 0.998 correlation to full-season DEF_RATING rank. Shot-type 26-30 = most allowed.
   - DvP is looked up by (opponent, the player's DK primary position). GAMES.md team ranks use all 82 games, so they can differ by about one place from the board's.
6. **Lifts.** Every attached number equals `p2_pooled.diff_build` for the right condition: paint +1.3, FT rate -0.1, mid-range -0.9, C&S 3 +1.5, above-break 3 +1.8, wide-open +3.9, pull-up 2 -0.7, corner 3 +0.2, rim +2.0, pull-up 3 -1.1, DvP +3.1, started +12.6. NEG appears exactly where the lift is negative.
7. **Scripts.** The published copies in `p1_historical/layer_e/build/` are identical to the build-directory copies.
