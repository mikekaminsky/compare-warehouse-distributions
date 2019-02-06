SELECT
    SUM(ss_net_profit)
  , d_moy
  , d_year
  , RANK() OVER (
     PARTITION BY d_moy, d_year
     ORDER BY SUM(ss_net_profit) DESC
    )  AS rank_within_parent
FROM public.store_sales
LEFT JOIN public.date_dim
  ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
GROUP BY d_moy, d_year
ORDER BY d_moy, rank_within_parent
