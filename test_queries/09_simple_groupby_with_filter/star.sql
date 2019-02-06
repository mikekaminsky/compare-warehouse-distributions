SELECT
    ca_state
  , COUNT(*)
FROM public.store_sales
LEFT JOIN public.customer_address
  ON store_sales.ss_addr_sk = customer_address.ca_address_sk
WHERE ca_state IN ('TX','NY','CA')
GROUP BY
  ca_state
