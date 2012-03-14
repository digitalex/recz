Recz
====
Recz is a lightweight, fast recommendation system for item-to-item recommendations.

Setup
-----
Recz expects a sqlite database named 'recz.sqlite' with a table named 'example'. In the sqlite3 console, create it like this:

    CREATE TABLE examples (item_id TEXT, session_id TEXT);
    CREATE INDEX main.itemidx ON examples(item_id);
    CREATE INDEX main.sessionidx ON examples(session_id);

Import some data however you'd like (I use grep, sed and awk to create a sql script). Then start the server simply like this:

    ./server.py

Test it:

    curl "http://localhost:8888/recommend?itemId=NO0000000995516055&k=3"
    # example output: {"itemIds": ["NO0000000930668656", "NO0000000993905321", "NO0000000895476722"]}
