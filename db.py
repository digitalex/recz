import sqlite3 as lite

class Db:
    """Simple database wrapper. Inserts are handled outside"""

    def __init__(self, db_name='recz.sqlite'):
        self.db_name = db_name

    def get_itemset(self, session_id):
        conn = lite.connect(self.db_name)
        curs = conn.execute("select item_id from examples where session_id=?",[session_id])
        rows = curs.fetchall()
        conn.close()
        return set(map(lambda r: r[0], rows))

    def get_sessionset(self, item_id):
        conn = lite.connect(self.db_name)
        curs = conn.execute("select session_id from examples where item_id=?",[item_id])
        rows = curs.fetchall()
        conn.close()
        return set(map(lambda r: r[0], rows))

