create table public.date_dim as select * from `singular-vector-135519`.tpcds_100.date_dim;
create table public.store as select * from `singular-vector-135519`.tpcds_100.store;
create table public.household_demographics as select * from `singular-vector-135519`.tpcds_100.household_demographics;
create table public.customer_address as select * from `singular-vector-135519`.tpcds_100.customer_address;
create table public.store_sales as select * from `singular-vector-135519`.tpcds_100.store_sales;
