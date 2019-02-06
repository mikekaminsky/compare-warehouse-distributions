# For Data Warehouse Performance: One Big Table or Star Schema?

Many have wondered, and some have even claimed to know, which data-organization style provides the best performance in a data warehouse. The two schools of thought are, roughly:

* Denormalize the data into one-big-table (OBT) so that the warehouse never has to do any joins on-the-fly
* Maintain a star schema that can take advantage of sort keys on the dimension tables

Before writing this blog post, I was very much on team "star schema" -- I had been taught that organizing data in a star schema was _critical_ to performance in analytic data warehouses. It turns out, I was wrong.

The first sign that I was wrong was when I wrote this slack message in the [dbt](https://www.getdbt.com) slack channel:

![A screenshot of me being an idiot.](/static/slack_screenshot.png)

If I had learned anything from my history of making statements that claim 100% certainty, I'd know that this is a _strong_ predictor of me being wrong and having to come back and eat crow. So here we are.

## The Results: Denormalized Tables Result in Faster Query-Response

Across the 10 different queries I tested, **using a denormalized table resulted in a 26% improvement in query-response time** over using a star schema. We ran each of the queries eight times (four against each type of data warehouse design).

Here's a visualization of the results between the one-big-table (OBT) approach, and the star-schema approach:

![Chart showing denormalized outperforms star](/static/side_by_side_performance.png)

Here we can see that the OBT model out-performs the star-schema model in all but one of the 10 queries we tested[^1].

If we visualize the data in terms of relative performance, we can see that (with the exception of the query-4 enigma) the denormalized table out performs the star schema from 10% to 45% depending on the query.

![Chart showing relative performance in percentages](/static/relative_performance.png)

## Analysis details

This comparison was made using a subset of the data from the TPC-DS benchmark, kindly [made available](https://github.com/fivetran/benchmark/) by the folks at Fivetran. We used the TPC-DS "100" data on a redshift dc2.large with 1 node and a dc2.8xlarge cluster with three nodes. All of the graphics presented in this post are from the run with three-nodes, but the one-node results all follow the same pattern (though with slower query times).

We make use of the following tables: `store_sales`, `date_dim`, `store`, `household_demographics`, `customer_address`

For the star schema, I just kept these tables as-is (distributing the fact table by `ss_item_key` and distributing the dimension tables across all nodes.

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

I distribute this by `ss_item_key` as well. For the timing test, we disable redshift's query caching mechanism according to [these docs](https://docs.aws.amazon.com/redshift/latest/dg/r_enable_result_cache_for_session.html).


All of the code to reproduce the analysis can be found in [this repo](https://github.com/mikekaminsky/compare-warehouse-distributions).


## Other considerations

There are a few reasons why you might still want to consider using the star schema (or something like it):

* The star schema promotes better ELT / ETL code conceptualization and organization.
* The star schema is easier for end-users (analysts and other query-writers) to navigate.
* The star schema takes up less disk space.

While the first two concerns are important, I think they can be handled pretty easily by staging your ELT process such that the data all get transformed into something like a star schema before everything gets re-joined back together for end-user querying.

The third point deserves more consideration -- materializing the denormalized takes up a significant amount of disk space on the cluster. Simply materializing the table bumped the disk-space usage up from a bit over 30 gigabytes to over 90. 

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


[^1]: Determining why the star-schema out performs the denormalized table on query 4 is left as an exercise for the reader. Mostly because I have no idea.
[^2]: Because dbt doesn't have the ability to specify column compression or encoding style in Redshift, this is probably the worst-possible-case in terms of disk storage size. I suspect that with proper column encoding you could alleviate a fair amount of this issue.


