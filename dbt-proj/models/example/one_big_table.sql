{{ config(materialized='table', dist='ss_item_sk') }}

SELECT *
FROM public.store_sales
LEFT JOIN public.date_dim
  ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
LEFT JOIN public.store
  ON store_sales.ss_store_sk = store.s_store_sk
LEFT JOIN public.household_demographics
  ON store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
LEFT JOIN public.customer_address
  ON store_sales.ss_addr_sk = customer_address.ca_address_sk
