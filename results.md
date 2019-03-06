# For Data Warehouse Performance: One Big Table or Star Schema?

Many have wondered, and some have even claimed to know, which data-organization style provides the best performance in a data warehouse. The two schools of thought are, roughly:

* Denormalize the data into one-big-table (OBT) so that the warehouse never has to do any joins on-the-fly
* Maintain a star schema that can take advantage of sort keys on the dimension tables

Before writing this blog post, I was very much on team "star schema" -- I had been taught that organizing data in a star schema was _critical_ to performance in analytic data warehouses. It turns out, I was wrong.

The first sign that I was wrong was when I wrote this slack message in the [dbt](https://www.getdbt.com) slack channel:

![A screenshot of me being an idiot.](/static/slack_screenshot.png)

If I had learned anything from my history of making statements that claim 100% certainty, I'd know that this is a _strong_ predictor of me being wrong and having to come back and eat crow. So here we are.

## The Goal: Understand Warehouse Performance for BI workloads

The objective of this analysis is to understand the performance implications of these different warehouse distribution patterns under normal BI-style workloads _within a given warehouse_. That is, we aren't trying to [benchmark warehouses against each other](https://fivetran.com/blog/warehouse-benchmark) or understand their relative performance and cost tradeoffs. We want to understand how different data architecture patterns perform once you've chosen which warehouse to use.

In particular, this analysis is focused on architecture patterns to support business-intelligence style workloads, not necessarily the query performance of miscellaneous, arbitrarily complex ad-hoc queries. The way many people build their warehouses today (using an ELT paradigm with a tool like [dbt](https://www.getdbt.com)), the star schema is constructe at the end of an ELT run and is explicitly designed to support BI-type queries in tools like Looker or Periscope. With that in mind, the queries that we use to test these different distribution styles are not especially complex as they're intentionally designed to reflect the common sorts of queries that are run by a BI tool -- aggregating measures over a variety of different dimensions, occasionally with a CTE or window function thrown in.

You can review the queries we used for the test [here](https://github.com/mikekaminsky/compare-warehouse-distributions/tree/master/test_queries).

## The Results: Denormalized Tables Result in Faster Query-Response

For all three of the warehouses we tested, Redshift, Snowflake, and Bigquery, using a single denormalized table instead of a star schema leads to a substantial improvement in query times. The difference is most pronounced in Redshift and Bigquery, where the speed improvement of using a single denormalized table represents an improvemnt of 25%-30%. This amounts to a difference of about 10 seconds on a single-node cluster in Redshift. In the Snowflake warehouse, the difference was still a meaningful 8%, but the difference is much less pronounced than in Redshift or Bigquery. 

### Redshift

For the redshift results, we present data from runs using both a large multi-node cluster as well as a small single-node cluster. We also split the results between the first time a query was executed (which will include the time Redshift needs to compile the query) as well as subsequent runs that only include compute time

#### Single-Node
First run
![dc2.large, single-node, first run](/Analysis/images/dc2.large_single-node_first.png)

Subsequent runs
![dc2.large, single-node, subsequent runs](/Analysis/images/dc2.large_single-node_subsequent.png)

#### Multi-Node
First run
![dc2.8xlarge, multi-node, first run](/Analysis/images/dc2.8xlarge_multi-node_first.png)

Subsequent runs
![dc2.8xlarge, multi-node, subsequent runs](/Analysis/images/dc2.8xlarge_multi-node_subsequent.png)

Here we can see that the OBT (denormalized) model out-performs the star-schema model in all but one of the 10 queries we tested[^1].

With the exception of the query-4 enigma, the denormalized table out performs the star schema from 10% to 45% depending on the query.

### Snowflake

For Snowflake, the results are more mixed. While the OBT (denormalized) model is definitely faster than the star schema in the slowest of queries (queries 8, 9, and 10), the star schema actually does appear to out-perform the OBT model in some of the simpler queries (namely 3, 4, and 7).

![Snowflake query results](/Analysis/images/snowflake.png)

I do not have a good enough intuition for the inner-workings of snowflake to cast any light on _why_ this might be happening, but if any of our readers are snowflake experts we'd love to hear your hypotheses!

### Bigquery

For bigquery, the results are just as dramatic as what we saw in Redshift -- the average improvement in query response time is 32%, with the denormalized table out-performing the star schema in almost every category (query 4 is basically a tie). 

![Bigquery query results](/Analysis/images/bigquery.png)

One thing that's interesting to note is how dramatically different the _variances_ in the query response times are between the two different distribution styles -- the star schema has a much higher variance in query response time which I assumes has to do with how bigquery is planning the execution under the hood (but I'm definitely not a BQ expert, so would love someone with more knowledge to weigh-in on what's going on here).

## Analysis details

This comparison was made using a subset of the data from the TPC-DS benchmark, kindly [made available](https://github.com/fivetran/benchmark/) by the folks at Fivetran. For all analyses, we used the TPC-DS "100" data.

* Redshift: 
  * dc2.large with 1 node
  * dc2.8xlarge cluster with three nodes
* Snowflake:
  * X-Large warehouse (16 servers) 
* Bigquery:
  * I used whatever the default configuration comes with a fresh warehouse

We make use of the following tables: `store_sales`, `date_dim`, `store`, `household_demographics`, `customer_address`

For the star schema, I just kept these tables as-is (distributing the fact table by `ss_item_key` and distributing the dimension tables across all nodes. 
In redshift, I distribute this by `ss_item_key` as well. For the timing test, we disable redshift's query caching mechanism according to [these docs](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_result_cache_for_session.html). 

For the denormalized tables, I just do a simple join to bring everything together:

```
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
```

All of the code to reproduce the analysis can be found in [this repo](https://github.com/mikekaminsky/compare-warehouse-distributions).


## Other considerations

There are a few reasons why you might still want to consider using the star schema (or something like it):

* The star schema promotes better ELT / ETL code conceptualization and organization.
* The star schema is easier for end-users (analysts and other query-writers) to navigate.
* The star schema takes up less disk space.

While the first two concerns are important, I think they can be handled pretty easily by staging your ELT process such that the data all get transformed into something like a star schema before everything gets re-joined back together for end-user querying.

The third point deserves more consideration, especially in a datawarehouse like Redshift -- materializing the denormalized takes up a significant amount of disk space on the cluster. Simply materializing the table bumped the disk-space usage up from a bit over 30 gigabytes to over 90. 

```
       tablename        |  megabytes
------------------------+-------
 household_demographics |     8
 date_dim               |    31
 store                  |    32
 customer_address       |    56
 store_sales            | 29778
 one_big_table          | 60250
```

And this is only a subset of the data we could have joined to `store_sales`! In fact, when I initially started on this analysis task I wanted to join all of the possible dimensions onto `store_sales` but couldn't because redshift ran out of disk-space (on a dc2.large cluster with 1 node)

Depending on the scale of your data, the storage cost of duplicating all of the dimensions on disk could just be too high[^2].

## Get in touch

If you have questions or thoughts on this analysis, I'd love to hear them. You can reach me via email at [kaminsky.michael@gmail.com](mailto:kaminsky.michael@gmail.com) or you can find me at my other blog locallyoptimistic.com.


[^1]: Determining why the star-schema out performs the denormalized table on query 4 is left as an exercise for the reader. Mostly because I have no idea.

[^2]: Because dbt doesn't have the ability to specify column compression or encoding style in Redshift, this is probably the worst-possible-case in terms of disk storage size. I suspect that with proper column encoding you could alleviate a fair amount of this issue.


