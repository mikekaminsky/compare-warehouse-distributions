WITH

cte_1 AS (
SELECT
    d_year
  , d_moy
  , SUM(ss_net_profit) AS ss_net_profit
FROM public.store_sales
LEFT JOIN public.date_dim
  ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
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
