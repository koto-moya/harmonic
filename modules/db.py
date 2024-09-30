from psycopg2.extras import RealDictCursor 

from config import get_db_conn, db_pool_harmonic_user

def get_brands():
    with get_db_conn(db_pool_harmonic_user) as db_conn:
        with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
            pass
def get_podcasts():
    with get_db_conn(db_pool_harmonic_user) as db_conn:
        with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
            pass
def get_codes():
    with get_db_conn(db_pool_harmonic_user) as db_conn:
        with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
            pass