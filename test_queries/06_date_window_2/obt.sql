SELECT
    d_year
  , d_moy
  , Sum(ss_net_profit)*100/Sum(Sum(ss_net_profit)) OVER (partition BY d_moy, d_year)
FROM dbt.one_big_table
GROUP BY d_year, d_moy
ORDER  BY d_year, d_moy
