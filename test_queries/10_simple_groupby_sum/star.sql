SELECT
    ca_state
  , sum(ss_net_profit)
FROM public.store_sales
LEFT JOIN public.customer_address
  ON store_sales.ss_addr_sk = customer_address.ca_address_sk
GROUP BY
  ca_state
