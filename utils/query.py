from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

try:
    connection = psycopg2.connect(user='postgres',
                        password='mm8yFDnK@_QPw*C',
                        host='db.fbjooeqzxmiqemnhaels.supabase.co',
                        port="5432",
                        database="postgres")

    # Create a cursor to perform database operations
    connection.autocommit = True
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]


def query(query_str: str):
    hasil = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SET SEARCH_PATH TO sepak_bola")
        try:
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                connection.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e

    return hasil