import psycopg2
import os
import yaml
import snowflake.connector
from google.cloud import bigquery

with open("dbconf.yml", "r") as f:
    config = yaml.load(f)


def get_connection(db_type):
    if db_type == "redshift":
        host_root = os.getenv("REDSHIFT_HOST_ROOT")
        identifier = config["redshift"]["cluster_identifier"]
        host = ".".join([identifier, host_root])
        dbname = config["redshift"]["db_name"]
        dbname = os.getenv("REDSHIFT_DBNAME")
        username = os.getenv("REDSHIFT_USER")
        password = os.getenv("REDSHIFT_PASSWORD")
        port = config["redshift"]["port"]
        conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=username, password=password
        )
        return conn

    if db_type == "snowflake":
        password = os.getenv("SNOWFLAKE_PASSWORD")
        user = os.getenv("SNOWFLAKE_USER")
        account = os.getenv("SNOWFLAKE_ACCOUNT")
        conn = snowflake.connector.connect(
            user=user, password=password, account=account
        )
        return conn

    if db_type == "bigquery":
        client = bigquery.Client()
        return client


def run_command(db_type, conn, cmd):
    print(cmd)
    if db_type == "bigquery":

        job_config = bigquery.QueryJobConfig()
        job_config.use_query_cache = False
        query_job = conn.query(cmd, job_config=job_config)
        results = query_job.result()
    else:
        cur = conn.cursor()
        cur.execute(cmd)
        conn.commit()


def get_query_results(db_type, conn, qry):
    if db_type == "bigquery":
        query_job = conn.query(qry)
        job_config = bigquery.QueryJobConfig()
        job_config.use_query_cache = False
        query_job = conn.query(qry, job_config=job_config)
        results = query_job.result()
    else:
        cur = conn.cursor()
        cur.execute(qry)
        results = cur.fetchall()
    return results
