from psycopg2 import pool
import os
from contextlib import contextmanager

db_pool_harmonic_user = pool.SimpleConnectionPool(minconn=1, maxconn=10, dbname=os.getenv("REPORTINGDBNAME"), user=os.getenv("PGUSERREPORTING"), password=os.getenv("PGPASSWORDREPORTING"), host=os.getenv("PGHOST"), port=os.getenv("PGPORT"))


@contextmanager
def get_db_conn(pool):
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

