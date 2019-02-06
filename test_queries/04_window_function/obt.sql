SELECT
    SUM(ss_net_profit)
  , s_state
  , s_county
  , RANK() OVER (
     PARTITION BY s_state, s_county
     ORDER BY SUM(ss_net_profit) DESC
    )  AS rank_within_parent
FROM dbt.one_big_table
GROUP  BY s_state, s_county
ORDER  BY s_state, rank_within_parent
