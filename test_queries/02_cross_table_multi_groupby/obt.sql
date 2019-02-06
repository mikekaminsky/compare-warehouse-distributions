SELECT
    ca_state
  , s_country
  , COUNT(*)
FROM dbt.one_big_table
GROUP BY
    ca_state
  , s_country
