# NBA preseason team board data

Built 2026-10-15. Preseason box scores run through 2026-10-14; X posts through 2026-10-15. This is the same data as the team board and the Claude Design canvas.

## Files
- **teams.csv**: 30 rows, opening-night teams first. Includes the opening-night game, the read (notes joined by " | "), the preview and availability.
- **players.csv**: 606 rows, one per player per team. Players are included if they played in preseason, averaged 12+ minutes in 2025-26, or are named in a post. Fields: preseason games, MPG, starts out of games with a box score, usage %, and the same for 2025-26 (start % instead of starts).
- **player_games.csv**: 1544 rows, one per player per preseason game: minutes, started (1/0), usage %.
- **posts.csv**: 332 rows. kind = analyst / beat (lineups and beat) / coach (coach quotes). source = Read in your Chrome, Your bookmark, Web search, Quote relay, or Codex summary. Multi-team analyst notes are cut to each team's section.
- **nba_teams.json**: the nested file the canvas loads (display-ready strings).

## Notes
- Usage is the box formula 100·(FGA+0.44·FTA+TOV)·(team MIN/5)/(MIN·team possessions), minutes-weighted across games.
- Post dates are UTC, so an evening ET post shows the next day.
- Posts are opinions and reports, not confirmed roles. Thunder Dan, Adam Stock and Besbris are only partly covered because X stops loading author searches after about 9 posts.
- Descriptive counts only; nothing here is a projection.
