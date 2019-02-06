WITH

cte AS (
SELECT
    ca_state
  , COUNT(*) total_in_state
FROM public.store_sales
LEFT JOIN public.customer_address
  ON store_sales.ss_addr_sk = customer_address.ca_address_sk
GROUP BY
    ca_state
)

SELECT
    ca.ca_state
  , ca_zip
  , COUNT(*) / total_in_state
FROM public.store_sales
LEFT JOIN public.customer_address ca
  ON store_sales.ss_addr_sk = ca.ca_address_sk
LEFT JOIN cte
  ON ca.ca_state = cte.ca_state
GROUP BY
    ca.ca_state
  , total_in_state
  , ca_zip
