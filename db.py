import psycopg2
import os

identifier = os.getenv("REDSHIFT_CLUSTER_IDENTIFIER")
host_root = os.getenv("REDSHIFT_HOST_ROOT")
dbname = os.getenv("REDSHIFT_DBNAME")
username = os.getenv("REDSHIFT_USER")
password = os.getenv("REDSHIFT_PASSWORD")
port = os.getenv("REDSHIFT_PORT", 5439)

host = ".".join([identifier, host_root])


def get_connection():
    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname, user=username, password=password
    )
    return conn

def run_command(conn, cmd):
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()

def get_query_results(conn, qry):
    cur = conn.cursor()
    cur.execute(qry)
    results = cur.fetchall()
    return results
