SELECT
    ca_state
  , COUNT(*)
FROM dbt.one_big_table
WHERE ca_state IN ('TX','NY','CA')
GROUP BY
  ca_state
