from argparse import ArgumentParser
import sys
import re
import requests

parser = ArgumentParser(description="Run a SQL command to create a table")
parser.add_argument('sql_file', type=str, help='Path to the .sql file')
parser.add_argument('--database-name', type=str, default="", help='name of the database')

args = parser.parse_args()

db_name = args.database_name

if db_name:
    result = requests.post(
        "http://localhost:8123",
        params={"query": f"CREATE DATABASE IF NOT EXISTS {db_name}"},
    )
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise Exception(result.text) from exc

with open(args.sql_file) as fp:
    query = fp.read()

m = re.search(r"table (\S*)", query)
table_name = m.group(1)

if db_name:
    query = query.replace(f"create table {table_name}", f"create table {db_name}.{table_name}")

    from_db = f"FROM {db_name}"
else:
    from_db = ""

tables = requests.post("http://localhost:8123", params={"query": f"SHOW TABLES {from_db}"}).text.split("\n")
if table_name in tables:
    print(f"Table `{table_name}` already exists, not continuing")
    sys.exit()

result = requests.post(
    "http://localhost:8123",
    params={"query": query},
)
try:
    result.raise_for_status()
except requests.exceptions.HTTPError as exc:
    raise Exception(result.text) from exc
