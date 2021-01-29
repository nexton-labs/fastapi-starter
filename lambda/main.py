import psycopg2
import os
import sys

DB_HOST = os.environ["dbHost"]
DB_USER = os.environ["dbUser"]
DB_PASSWORD = os.environ["dbPassword"]
DB_NAME = os.environ["dbName"]
DB_PORT = os.environ["dbPort"]

try:
    conn = psycopg2.connect(
        "dbname={} user={} host={} password={}".format(
            DB_NAME, DB_USER, DB_HOST, DB_PASSWORD
        )
    )
    str(conn)
except Exception as ex:
    print("Cannot connect: " + str(ex))
    sys.exit()


def lambda_handler(event, context):
    print(event)

    if event["request"]["userAttributes"]["cognito:user_status"] == "EXTERNAL_PROVIDER":
        query_cmd = "INSERT INTO users (id, username, email) VALUES ('{id}', '{username}', '{email}')"
        sub = (
            event["request"]["userAttributes"]["sub"]
            if "sub" in event["request"]["userAttributes"]
            else None
        )
        email = (
            event["request"]["userAttributes"]["email"]
            if "email" in event["request"]["userAttributes"]
            else None
        )
        phone = (
            event["request"]["userAttributes"]["phone"]
            if "phone" in event["request"]["userAttributes"]
            else None
        )

        if sub:
            if email:
                query_cmd = query_cmd.format(id=sub, email=email, username=email)
            elif phone:
                query_cmd = query_cmd.format(id=sub, email=phone, username=phone)

            print(query_cmd)

            with conn.cursor() as cur:
                cur.execute(query_cmd)
                conn.commit()

            conn.commit()

    return event
