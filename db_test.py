import psycopg2
import urllib.parse as urlparse

import os

DB_TOKEN = os.getenv("WAIFU_DB_TOKEN")


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(DB_TOKEN)

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()


def roll():
    conn.rollback()


def commit():
    conn.commit()


def execute(command):
    cur.execute(command+";")


def fetch():
    for r in cur.fetchall():
        print(r)


def close():
    cur.close()
    conn.close()


inp = input("DB: ")
while inp != "close":
    if inp.startswith("$"):
        execute(inp[1:])
    elif inp.startswith(">"):
        fetch()
    elif inp == "commit":
        commit()
    elif inp == "rollback":
        roll()
    else:
        print("I duno")
    inp = input("DB: ")

close()
