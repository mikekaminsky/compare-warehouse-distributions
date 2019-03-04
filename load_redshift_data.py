import os
import db

ROLE_ARN = "arn:aws:iam::768805597102:role/RedshiftReadS3"

TABLE_LIST = [
    "date_dim",
    "store",
    "household_demographics",
    "customer_address",
    "store_sales"
]

conn = db.get_connection('redshift')

# Create table commands
with open("load_commands.sql", "r") as f:
    cmds = f.readlines()

for cmd in cmds:
    print(cmd)
    conn.cursor().execute(cmd)
    conn.commit()

copy_template = """
    copy public.{table_name} from 's3://fivetran-benchmark/tpcds_100_dat/{table_name}/' region 'us-east-1' format delimiter '|' acceptinvchars compupdate on iam_role '{role_arn}';
"""

for table in TABLE_LIST:
    cmd = copy_template.format(table_name=table, role_arn=ROLE_ARN)
    print(cmd)
    conn.cursor().execute(cmd)
    conn.commit()
