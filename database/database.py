import psycopg

from psycopg.rows import dict_row



def create_connection():
    conn = psycopg.connect(
        dbname="Dev_CMMI",
        user="postgres",
        password="12345",
        host="localhost",
        row_factory=dict_row
    )
    return conn

def run_sql(conn, sql: str):
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows
