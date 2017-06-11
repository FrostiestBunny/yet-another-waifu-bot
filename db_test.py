import psycopg2
import urllib.parse as urlparse


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://xxaytwrfomnnml:9c4c70dd8f25b43cb187d34d01f6fa6f0885a0cb705d9d64ad88dcc21df1d630@" +
                        "ec2-54-247-189-141.eu-west-1.compute.amazonaws.com:5432/d3cnnian2qaq96")

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
