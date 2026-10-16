# Shot-type volume check: does a generous defense raise HIS attempts of that type?

Asked by Ramneik on 2026-10-15 after the layer E and A-D reports. Layer E measured upside (his own top quarter of DK points), not volume. This file counts volume directly. Script: `../build/23_volume_check.py`. Data: `volume_by_type.csv`, `volume_per_player_repeat.csv`.

## Verdict

**Ramneik is right that volume moves. It moves only a little, and that small move is why upside barely changes.**

1. **Volume does rise.** Strong catch-and-shoot players against a bottom-10 defense in C&S attempts allowed:
   - They took about 0.3 more C&S attempts than their own season-to-date average: +0.34 in 2024-25 and +0.28 in 2025-26.
   - Against other defenses they were at their average (0.00 / -0.07), and against the 5 stingiest they were below it (-0.16 / -0.14).
   - They beat their own C&S average on 51% / 50% of nights against those defenses, vs 44% / 43% otherwise.
2. **The same holds for most types.** Wide-open, rim, short paint, mid-range, above-break 3 and pull-up 2 all show the same small rise, in both seasons.
   - Pull-up 3 does not rise.
   - The share of his FGA shifts too (C&S share +1.3 vs -0.4 points for all players), so part of the rise is specific to the shot type, not just more shots overall.
3. **Why the upside lift stays small.**
   - A night above his own C&S average is a big upside night: 41% upside vs 12-13% when he is not above it. But that is in-game, and it is mostly him playing and shooting more.
   - The matchup only moves his chance of such a night by about 7 points (44% to 51%).
   - Multiplied out (7 points x about 28 points of upside difference), that is about +2 points of upside, which matches the +2 to +4 the funnels showed in layer E.
   - Once his volume is up, the matchup adds nothing more: 44.7% / 42.6% upside when he is above his average against a generous defense, vs 40.9% / 41.2% for all his above-average nights.
4. **Per player, the direction repeats but the size does not.**
   - Of 86 strong C&S players with 5+ games each way in both seasons, 46 took more C&S attempts against bottom-10 defenses in both seasons, 5 took fewer in both, and 35 were mixed.
   - Most players get a bit more volume, but how much more in 2024-25 does not predict 2025-26 (correlation -0.09).

**For picking:** a generous C&S defense is a real but small nudge toward more C&S volume, about one extra attempt every three games. Treat it as a tiebreak inside the funnel line, not a reason on its own. Absences, starting and minutes still move volume and upside far more.

## Method

- Qualifying players only (20+ games).
- Baseline: his mean attempts of the type over earlier games this season, with 5+ earlier games required.
- Opponent: season-to-date volume allowed per 100 possessions, ranked against all 30 teams.
- "Strong in the type": top third of FGA share at his position on the date, as in layer E.
- Play-by-play types for 2024-25 run only through 2025-03-24.
- Descriptive counts only.
