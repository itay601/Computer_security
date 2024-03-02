import pymysql
import argon2


SECRET_KEY = "@@##sfasfd321"  # Replace with a strong and unique secret key
TOKEN_EXPIRATION_SECONDS = 3600  # Set the expiration time for the token (e.g., 1 hour)


def connect_to_db():
    host = "127.0.0.1"
    user = "root"
    password = "my-secret-pw"
    dbname = "USERS"

    # Connect to the database
    db_connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=dbname,
        port=3456,
        cursorclass=pymysql.cursors.DictCursor,
    )

    return db_connection
