SELECT
    d_year
  , d_moy
  , Sum(ss_net_profit)*100/Sum(Sum(ss_net_profit)) OVER (partition BY d_moy, d_year)
FROM public.store_sales
LEFT JOIN public.date_dim
  ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
GROUP  BY
    d_year
  , d_moy
ORDER BY
    d_year
  , d_moy
