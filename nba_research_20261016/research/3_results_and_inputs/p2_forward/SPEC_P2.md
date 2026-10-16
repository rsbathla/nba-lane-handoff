# P2 forward check spec (frozen before the read window is counted)

Written 2026-10-15. Plan v2 section 6.

- **Build window:** 2024-25 regular season plus 2025-26 games before 2026-01-15. **Read window:** 2025-26 games on or after 2026-01-15.
- **Upside threshold:** each player's 75th percentile of DK points over his build-window games only (20+ build games required). The same frozen threshold is applied in the read window. No read-window game ever sets a threshold.
- **Conditions:** unchanged from layer E v1.2 and layers A-D v1.1 (all pregame, as of date). Lock-time and in-game conditions are reported separately and are not leads.
- **What is frozen from the build window:**
  1. Pooled: every single pregame condition's difference (upside rate present minus absent, points).
  2. Per player: every player x condition row with 10+ present and 10+ absent build games; a **build lead** is a difference of +10 points or more, a **build negative** -10 or less.
- **Read:** (1) pooled differences in the read window next to the build window, same sign or not; (2) per player, the share of build leads that are positive in the read window (5+ present and 5+ absent read games) against the same share for build negatives. Reported as counts; no tests.
