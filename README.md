Recz
====
Recz is a lightweight, fast recommendation system for item-to-item recommendations.

Setup
-----
Recz expects a sqlite database named 'recz.sqlite' with two tables named 'items' and 'sessions'. If you use the importer, they are created automatically. Import a list of item_id, session_id like this:

    python importer.py < items.txt

Then start the server simply like this:

    python server.py

Test it:

    curl "http://localhost:8888/recommend?itemId=NO0000000995516055&k=3"
    # example output: {"itemIds": ["NO0000000930668656", "NO0000000993905321", "NO0000000895476722"]}
