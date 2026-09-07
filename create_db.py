import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Try connecting as postgres user
    conn = psycopg2.connect(user="postgres", password="password", host="127.0.0.1", port="5432")
except Exception as e:
    try:
        # Try connecting with no password
        conn = psycopg2.connect(user="postgres", host="127.0.0.1", port="5432")
    except Exception as e:
        try:
            # Try connecting as current user
            conn = psycopg2.connect(host="127.0.0.1", port="5432")
        except Exception as e:
            print("Could not connect to postgres:", e)
            exit(1)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

try:
    cur.execute("CREATE USER stevesai WITH PASSWORD 'stevesai';")
except Exception as e:
    print("User might exist:", e)

try:
    cur.execute("CREATE DATABASE stevesai_cms OWNER stevesai;")
except Exception as e:
    print("DB might exist:", e)

cur.close()
conn.close()
print("Database and user created.")
