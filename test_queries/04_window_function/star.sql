SELECT
    SUM(ss_net_profit)
  , s_state
  , s_county
  , RANK() OVER (
     PARTITION BY s_state, s_county
     ORDER BY SUM(ss_net_profit) DESC
    )  AS rank_within_parent
FROM public.store_sales
LEFT JOIN public.store
  ON store_sales.ss_store_sk = store.s_store_sk
GROUP  BY s_state, s_county
ORDER  BY s_state, rank_within_parent
