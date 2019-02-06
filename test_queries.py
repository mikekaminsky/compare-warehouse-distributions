import time
import os

import pandas as pd

import db

disable_cache = """SET enable_result_cache_for_session TO OFF;"""

conn = db.get_connection()

# Disable cache
db.run_command(conn, disable_cache)


def time_it(test_dir, style, nth):
    fn = os.path.join("test_queries", test_dir, style + ".sql")
    print("Evaluating {}".format(fn))
    with open(fn, "r") as f:
        query = f.read()
    start_time = time.time()
    query_res = db.get_query_results(conn, disable_cache + query)
    end_time = time.time()
    elapsed = end_time - start_time
    print("Completed in: {}".format(elapsed))
    res = {'test':test_dir, 'style':style, 'time':elapsed, 'nth':nth}
    pd_res = pd.DataFrame.from_records([res])
    return pd_res


row_list = []
for i in range(2,6):
    for test_q in os.listdir("test_queries"):
        row_list.append(time_it(test_q, "star", i))
        row_list.append(time_it(test_q, "obt", i))

results = pd.concat(row_list)

results.to_csv('data/redshift_results.csv')
