SELECT
    ca_zip
  , COUNT(*)
FROM dbt.one_big_table
GROUP BY
    ca_zip
ORDER BY 2 DESC
limit 20
