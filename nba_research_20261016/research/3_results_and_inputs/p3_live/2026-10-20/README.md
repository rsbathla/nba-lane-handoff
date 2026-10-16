# Opening night 2026-10-20: board (draft, built 2026-10-15)

The DK classic slate has 3 games and 125 players: BOS @ DET 3:00, PHI @ NYK 7:00, OKC @ SAS 9:30 ET. This board uses the engine approved on the 2026-03-18 template, with three opening-night changes.

1. **Absences come from the injury report.** A teammate counts as out only when the report lists him as Out, because the 0-minute rule needs a game that has not happened yet. The report used here was captured 2026-10-15. It lists preseason rest days (shown as "day-to-day", not counted) and three players as Out: Oweh (out for the season), Quaintance (not yet cleared) and Hukporti. None of them holds a team role, so no absence line fires yet. **Rebuild on game day with the report at lock.**
2. **Everything is last season.**
   - Player usage tier, shot-type leans, and games/minutes/starts are from 2025-26.
   - Opponent DRtg, DvP and shot-type ranks are 2025-26 final (through April 11), and they describe last year's rosters.
   - The upside line is his own top quarter over 2024-25 and 2025-26.
   - 25 slate players changed teams (flagged "NEW TEAM"); 38 have under 20 NBA games (no upside line).
3. **Starting comes from preseason, not lineups.** "Started X% of preseason games" is a pointer only: it requires 2+ games and 50%+ starts, and is rebuilt by `27_preseason.py` from your pipeline's latest NBA.com preseason game log plus every preseason boxscore (starters = boxscore position filled in). Current file: all 53 preseason games through 2026-10-14 (`build/data/preseason_2026_through_1014.csv`; raw captures in `inputs/preseason_raw/`). The +12.6 lift belongs to confirmed starters at lock. Prior-10 minutes is not shown, because last April's minutes trend says little about October.

**Team roles for absences** are built on the current DK rosters from earlier seasons:
- Top usage: minutes-weighted 2025-26 usage, 15+ mpg.
- Top playmaker: minutes-weighted share of his team's assists in 2025-26.
- Starter at each position: most starts over 2024-25 and 2025-26 at his last-season position, with preseason starts breaking ties.
- Once this season's games exist, the in-season rules take over.

The rest is unchanged from the template:
- Lines are listed, never added.
- Shot type uses raw volume allowed only and is marked as a tiebreak: "shot-mix shift" for rim, paint and FT rate, "more shots overall" for the others.
- NEG marks a line whose league lift is negative.
- The Matchup Lab composite is left out tonight, because half of it is the opponent's last 7 games from last April.

## Files

- `board.csv`: every slate player.
- `GAMES.md`: per game, last season's team ranks, who is new, who is out, and each player's lines.
- `inputs/`: the DK slate, injury report and schedule used.
- `REVIEW_OPENING_BOARD.md`: the independent review (pass with fixes); all fixes are applied.
- Scripts: `../../p1_historical/layer_e/build/25_opening_board.py` and `26_opening_games.py`. Build inputs are in `../../p1_historical/layer_e/build/data/`.

## Rerun at lock

```
python3 27_preseason.py <latest leaguegamelog_P json> <out csv> <boxscore dirs...>
python3 25_opening_board.py 2026-10-20 <latest dk_slate parquet> <latest injuries parquet> <latest schedule parquet> <preseason csv from 27>
python3 26_opening_games.py 2026-10-20
```

The newest slate and injury captures are written by Ramneik's daily pipeline on the Mac, under `dfs/nba/analytics/data/daily/pregame/`.
