# NBA research data (20261016)

Everything the NBA upside research has produced, in one place. Raw source files are in the separate nba_raw_inputs_20261016.zip.

## 1_board
The team board and Claude Design canvas data: teams, players, per-game preseason lines, all 332 X posts (has its own README).

## 2_history (2024-25 and 2025-26 regular seasons)
- **frame_abcd**: 52,952 player-game rows x 429 columns. Box score, DK points, the upside flag (top quarter of the player's own DK games), who was out, start and minutes role, lines, pace and matchup fields. Given as parquet and as gzipped CSV. frame_abcd_columns.csv lists every column with its type and how often it is filled.
- **teamgames**: 4,920 team-game rows x 55 columns of team advanced stats.
- **opp_ranks**: 9,810 rows x 102 columns. Each defense's rank on each date by shot type (volume and efficiency allowed, raw and opponent-adjusted, season and last 10). Only data available before that date is used.
- intermediate/: working tables the scripts build on the way (Layer E frame, defense state by date, per-player counts, on/off).
- preseason_2026_through_1014.csv (this preseason by player), preseason_projections_all_rostered_2026.csv, p2_pooled.csv.

## 3_results_and_inputs
Reports, specs, reviewer notes and result tables from each stage, in their project folders: p1_historical (layers A-E, shot-type volume checks), p2_forward, p3_live (opening-night board draft, its inputs, the tweets digest and X post files).

## 4_scripts
The Python build scripts (numbered in run order) that produced all of the above.

## Method
Descriptive counts only, no models or scores. Upside = the player's own top quarter of DK points. Both seasons are shown side by side, and nothing uses information from after the game.
