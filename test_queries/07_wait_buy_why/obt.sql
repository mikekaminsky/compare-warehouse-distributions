SELECT
    SUM(ss_net_profit)
  , d_moy
  , d_year
  , RANK() OVER (
     PARTITION BY d_moy, d_year
     ORDER BY SUM(ss_net_profit) DESC
    )  AS rank_within_parent
FROM dbt.one_big_table
GROUP  BY d_moy, d_year
ORDER  BY d_moy, rank_within_parent
