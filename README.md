# Runestack

A cave-delving gem-stacking puzzle. Play it at https://unevent0ast.github.io/runestack/

- `index.html` is the game.
- `dev/` holds the source for the Claude version, the build script, and the scoreboard database setup (`setup.sql` for a new board, `records.sql` to add the record columns to an existing one).
- To rebuild the site after changing the Claude version: copy its source into `dev/runestack-artifact.html`, then run `python3 dev/build_site.py <supabase_url> <publishable_key>`. It writes `index.html`.
