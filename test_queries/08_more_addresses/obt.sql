WITH

cte AS (
SELECT
    ca_state
  , COUNT(*) total_in_state
FROM dbt.one_big_table
GROUP BY
    ca_state
)

SELECT
    obt.ca_state
  , ca_zip
  , COUNT(*) / total_in_state
FROM dbt.one_big_table obt
LEFT JOIN cte
  ON obt.ca_state = cte.ca_state
GROUP BY
    obt.ca_state
  , total_in_state
  , ca_zip
