import time
import os
import datetime

import pandas as pd

import db
import sys


db_type = sys.argv[1]
print(db_type)

today_str = datetime.datetime.today().strftime('%Y-%m-%d')

disable_cache = """SET enable_result_cache_for_session TO OFF;"""

conn = db.get_connection(db_type)

# Disable cache
if db_type == 'redshift':
    db.run_command(db_type, conn, disable_cache)
if db_type == 'snowflake':
    db.run_command(db_type, conn, 'USE DATABASE DEMO_DB')

def time_it(test_dir, style, nth):
    fn = os.path.join("test_queries", test_dir, style + ".sql")
    print("Evaluating {}".format(fn))
    with open(fn, "r") as f:
        query = f.read()
    start_time = time.time()
    if db_type == 'redshift':
        query = disable_cache + query
    query_res = db.get_query_results(db_type, conn, query)
    end_time = time.time()
    elapsed = end_time - start_time
    print("Completed in: {}".format(elapsed))
    res = {'test':test_dir, 'style':style, 'time':elapsed, 'nth':nth}
    pd_res = pd.DataFrame.from_records([res])
    return pd_res


row_list = []
for i in range(1,6):
    for test_q in os.listdir("test_queries"):
        row_list.append(time_it(test_q, "star", i))
        row_list.append(time_it(test_q, "obt", i))

results = pd.concat(row_list)
results['date'] = today_str
if db_type == 'redshift':
    results['cluster_type'] = db.config['redshift']['cluster_type']
    results['node_type'] = db.config['redshift']['node_type']
results['db_type'] = db_type

results.to_csv('data/{}_results.csv'.format(db_type), mode='a')
