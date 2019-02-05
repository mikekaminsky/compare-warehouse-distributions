import psycopg2
import os

identifier = os.getenv('REDSHIFT_CLUSTER_IDENTIFIER')
host_root = os.getenv('REDSHIFT_HOST_ROOT')
dbname = os.getenv('REDSHIFT_DBNAME')
username = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PASSWORD')
port = os.getenv('REDSHIFT_PORT', 5439)


host = '.'.join([identifier, host_root])

conn = psycopg2.connect(
    host=host, port=port, dbname=dbname, user=username, password=password
)

with open('load_commands.sql','r') as f:
    cmds = f.read()

conn.cursor().execute(cmds)

# TODO:
# * On create-whitelist, on name-conflict, vlad should warn and ask for user input to over-write
