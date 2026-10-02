-- Runestack scoreboard. Paste this whole file into Supabase > SQL Editor and press Run.

create table if not exists public.scores (
  id          bigint generated always as identity primary key,
  device      text not null check (char_length(device) between 4 and 40),
  player      text not null check (char_length(player) between 1 and 40),
  name        text not null check (char_length(name) between 1 and 16),
  delve_depth int  not null default 0 check (delve_depth between 0 and 500),
  delve_score int  not null default 0 check (delve_score between 0 and 10000000),
  story       int  not null default 0 check (story between 0 and 10000000),
  daily       int  not null default 0 check (daily between 0 and 1000000),
  day         date,
  created_at  timestamptz not null default now()
);

-- Anyone can read scores and add new ones. Nobody can edit or delete them from the game.
alter table public.scores enable row level security;
drop policy if exists "anyone can read" on public.scores;
drop policy if exists "anyone can add"  on public.scores;
create policy "anyone can read" on public.scores for select to anon using (true);
create policy "anyone can add"  on public.scores for insert to anon with check (true);
grant select, insert on public.scores to anon;

-- Each player's best results.
create or replace view public.best with (security_invoker = on) as
  select device, player,
         (array_agg(name order by created_at desc))[1] as name,
         max(delve_depth) as delve_depth,
         max(delve_score) as delve_score,
         max(story)       as story
  from public.scores
  group by device, player;

-- Each player's best Daily Delve score per day.
create or replace view public.daily_best with (security_invoker = on) as
  select device, player,
         (array_agg(name order by created_at desc))[1] as name,
         day,
         max(daily) as daily
  from public.scores
  where daily > 0 and day is not null
  group by device, player, day;

grant select on public.best, public.daily_best to anon;
