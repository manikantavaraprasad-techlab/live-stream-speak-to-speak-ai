#!/usr/bin/env python3
import sqlite3, gzip, os, re

DB = "knowledge.db"

IMDB_NAMES = "entity_db/entity_db/name.basics.tsv.gz"
IMDB_TITLES = "entity_db/entity_db/title.basics.tsv.gz"
GEONAMES = "entity_db/entity_db/allCountries.txt"

_ws = re.compile(r"\s+")
_bad = re.compile(r"[^a-z0-9\s]+")


def norm(s):
    s = (s or "").lower()
    s = _bad.sub(" ", s)
    s = _ws.sub(" ", s).strip()
    return s


def connect():
    return sqlite3.connect(DB)


def create_table(con):
    con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS entities USING fts5(name, etype)")


def insert_rows(con, rows):
    cur = con.cursor()
    cur.executemany("INSERT INTO entities(name, etype) VALUES (?,?)", rows)
    con.commit()


def load_imdb_people(con):
    print("Loading people...")
    rows = []
    with gzip.open(IMDB_NAMES, "rt", encoding="utf-8", errors="ignore") as f:
        header = f.readline().split("\t")
        idx = header.index("primaryName")

        for line in f:
            name = norm(line.split("\t")[idx])
            if len(name) > 2:
                rows.append((name, "person"))

            if len(rows) > 5000:
                insert_rows(con, rows)
                rows = []

    insert_rows(con, rows)


def load_geonames(con):
    print("Loading places...")
    rows = []
    with open(GEONAMES, encoding="utf-8", errors="ignore") as f:
        for line in f:
            name = norm(line.split("\t")[1])
            if len(name) > 2:
                rows.append((name, "place"))

            if len(rows) > 5000:
                insert_rows(con, rows)
                rows = []

    insert_rows(con, rows)


def main():
    con = connect()
    create_table(con)

    load_imdb_people(con)
    load_geonames(con)

    print("Optimizing...")
    con.execute("INSERT INTO entities(entities) VALUES('optimize')")
    con.commit()
    con.close()

    print("✅ knowledge.db ready")


if __name__ == "__main__":
    main()
