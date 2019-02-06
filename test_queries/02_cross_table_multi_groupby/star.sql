SELECT
    ca_state
  , s_country
  , COUNT(*)
FROM public.store_sales
LEFT JOIN public.customer_address
  ON store_sales.ss_addr_sk = customer_address.ca_address_sk
LEFT JOIN public.store
  ON store_sales.ss_store_sk = store.s_store_sk
GROUP BY
    ca_state
  , s_country

