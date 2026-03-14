import psycopg
from psycopg_pool import ConnectionPool

DATABASE_URL="postgresql://postgres:root@localhost:5432/postgres"

pool=ConnectionPool(conninfo=DATABASE_URL)


def get_conn():
    with pool.connection() as conn:
        yield conn