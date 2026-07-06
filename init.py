import os
import sys
import boto3
import pymysql

client = boto3.client("ssm", region_name="us-east-1")


def get_param(name):
    response = client.get_parameter(
        Name=f"/application/testing/{name}",
        WithDecryption=True
    )
    return response["Parameter"]["Value"]


try:
    # Get parameters
    DB_HOST = get_param("DB_HOST")
    DB_USER = get_param("DB_USER")
    DB_PASSWORD = get_param("DB_PASSWORD")
    DB_PORT = int(get_param("DB_PORT"))

    # Connect WITHOUT specifying a database
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        connect_timeout=10,
        autocommit=True
    )

    cursor = conn.cursor()

    # Read init.sql
    sql_file = "/tmp/init.sql"

    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    # Execute every SQL statement
    for statement in sql.split(";"):
        statement = statement.strip()

        if statement:
            cursor.execute(statement)

    cursor.close()
    conn.close()

    print("✅ Database initialized successfully.")

except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)