# Comparing Data Warehouse Distribution Styles

This repo contains the code for testing how different data warehouse data-organization schemes impact query performance.

You can use this repo to either review the queries that were used in the test (in the [test_queries](/test_queries) folder) or to run the analysis yourself.

This guide assumes you have a Redshift cluster up and running with the following conditions:

* You have query access to it from your IP address
* The cluster has permission to read from S3

You'll need to set the following environment variables:

```
  export REDSHIFT_DBNAME=test_db
  export REDSHIFT_USER=test_user
  export REDSHIFT_PASSWORD=test_Pa55w0rd
  export DBT_PROFILES_DIR=path/to/profiles/dir
  export REDSHIFT_HOST=something-something.aws.amazon.com
```

You can then run the script to load the data we need into the cluster:

```
python load_data.py
```

Once you've done that, you can use DBT to create the table we'll use

```
cd dbt-proj
dbt run
```

Finally, we can run the script to execute our test queries and persist the results

```
cd .. # go back to the root project directory
python test_queries.py
```

You can then analyze the results using the jupyter notebook in the `Analysis/` directory.
