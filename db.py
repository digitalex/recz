import sqlite3 as lite

class Db:
    """Simple database wrapper. Inserts are handled outside"""

    def __init__(self, db_name='recz.sqlite'):
        self.db_name = db_name

    def add_example(self, item_id, session_id):
        itemset = self.get_itemset(session_id)
        sessionset = self.get_sessionset(item_id)
        itemset.add(item_id)
        sessionset.add(session_id)
        conn = lite.connect(self.db_name)
        with conn:
            conn.execute("UPDATE items SET sessions=? WHERE item_id=?", [','.join(sessionset), item_id])
            conn.execute("UPDATE sessions SET items=? WHERE session_id=?", [','.join(itemset), session_id])

    def get_itemset(self, session_ids):
        conn = lite.connect(self.db_name)
        with conn:
            items = set()
            query = "SELECT items FROM sessions WHERE session_id IN ('%s')" % ("','".join(session_ids))
            curs = conn.execute(query)
            for row in curs.fetchall():
                for item_id in row[0].split(','):
                    items.add(item_id)
        return items

    def get_sessionset(self, item_id):
        conn = lite.connect(self.db_name)
        with conn:
            curs = conn.execute("SELECT sessions FROM items WHERE item_id=? LIMIT 1",[item_id])
            return set(curs.fetchone()[0].split(','))

