import psycopg2
import os
import yaml
import snowflake.connector

with open('dbconf.yml', 'r') as f:
    config = yaml.load(f)


def get_connection(db_type):
    if db_type == 'redshift':
        host_root = os.getenv("REDSHIFT_HOST_ROOT")
        host = ".".join([identifier, host_root])
        identifier = config['redshift']['cluster_identifier']
        dbname = config['redshift']['db_name']
        username = config['redshift']['user']
        password = config['redshift']['password']
        port = config['redshift']['port']
        conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=username, password=password
        )
        return conn
    if db_type == 'snowflake':
        password = config['snowflake']['password']
        user = config['snowflake']['user']
        account = config['snowflake']['account']

        conn = snowflake.connector.connect(
          user=user,
          password=password,
          account=account,
        )
        return conn

def run_command(conn, cmd):
    print(cmd)
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()

def get_query_results(conn, qry):
    cur = conn.cursor()
    cur.execute(qry)
    results = cur.fetchall()
    return results
