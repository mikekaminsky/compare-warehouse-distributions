WITH

cte_1 AS (
SELECT
    d_year
  , d_moy
  , SUM(ss_net_profit) AS ss_net_profit
FROM dbt.one_big_table
GROUP  BY
    d_year
  , d_moy
)

SELECT
    d_year
  , d_moy
  , ss_net_profit /
    SUM(ss_net_profit) OVER (
        PARTITION BY
        d_year
      )
FROM cte_1
