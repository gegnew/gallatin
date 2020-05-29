import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_tables(cur, conn):
    """
    Make new tables!
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    """
    Insert data from staging tables into our new db schema.
    
    Args:
        cur: psycopg2 (or boto3) cursor object
        conn: psycopg2 (or boto3) connection object
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()