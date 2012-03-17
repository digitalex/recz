#!/usr/bin/python

import sys
import fileinput
import sqlite3 as lite
from time import clock

i = 0
items = {}
sessions = {}
start_read = clock()

for line in fileinput.input():
    parts = line.split()
    if len(parts) == 2:
        item_id, session_id = parts
        items.setdefault(item_id, set()).add(session_id)
        sessions.setdefault(session_id, set()).add(item_id)
        i += 1

print "Read %d examples in %f seconds" % (i, clock()-start_read)
conn = lite.connect('recz.sqlite')
with conn:
    conn.execute("CREATE TABLE IF NOT EXISTS items (item_id TEXT PRIMARY KEY, sessions TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY, items TEXT)")
    conn.execute("BEGIN TRANSACTION")

    print "Inserting items..."
    for item_id, sessionset in items.iteritems():
        conn.execute("INSERT INTO items(item_id,sessions) VALUES(?,?)", [item_id, ','.join(sessionset)])

    print "Inserting sessions..."
    for session_id, itemset in sessions.iteritems():
        conn.execute("INSERT INTO sessions(session_id,items) VALUES(?,?)", [session_id, ','.join(itemset)])
