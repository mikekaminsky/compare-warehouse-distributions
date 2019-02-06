SELECT
    ca_state
  , sum(ss_net_profit)
FROM dbt.one_big_table
GROUP BY
  ca_state
