-- Runestack records. Paste this whole file into Supabase > SQL Editor and press Run. Safe to run more than once.

alter table public.scores
  add column if not exists best_stack int not null default 0 check (best_stack between 0 and 200),
  add column if not exists best_chain int not null default 0 check (best_chain between 0 and 300),
  add column if not exists best_burst int not null default 0 check (best_burst between 0 and 200),
  add column if not exists best_move  int not null default 0 check (best_move  between 0 and 10000000);

-- Each player's best results, now with their records.
create or replace view public.best with (security_invoker = on) as
  select device, player,
         (array_agg(name order by created_at desc))[1] as name,
         max(delve_depth) as delve_depth,
         max(delve_score) as delve_score,
         max(story)       as story,
         max(best_stack)  as best_stack,
         max(best_chain)  as best_chain,
         max(best_burst)  as best_burst,
         max(best_move)   as best_move
  from public.scores
  group by device, player;

grant select on public.best to anon;
