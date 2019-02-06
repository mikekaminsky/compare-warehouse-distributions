SELECT
    ca_state
  , COUNT(*)
FROM dbt.one_big_table
GROUP BY
  ca_state
