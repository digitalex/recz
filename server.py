#!/usr/bin/python
import fileinput
import tornado.web
import tornado.ioloop
from time import clock
from collections import defaultdict

PORT = 8888

class Recz:
    """Lightweight, fast recommendation system for item-to-item recommendations."""

    def __init__(self):
        self.sessions = {}
        self.items = {}

    def add_example(self, item_id, session_id):
        self.sessions.setdefault(item_id, set()).add(session_id)
        self.items.setdefault(session_id, set()).add(item_id)

    def compact(self):
        """Removes data that cannot help recommendations."""
        for key in filter(lambda k: len(self.sessions[k])<2, self.sessions.iterkeys()):
          del self.sessions[key]
        for key in filter(lambda k: len(self.items[k])<2, self.items.iterkeys()):
          del self.items[key]

    def recommend(self, item_id, k=5):
        """Build a list of k recommended items, based on the given item_id."""
        sessions = dict(self.sessions)
        sessionset = sessions.pop(item_id, set())
        itemcounts = defaultdict(int)

        # Count the occurrences of other items viewed by the same sessions
        for session_id in sessionset:
            itemset = self.items.get(session_id, set())
            itemset.discard(item_id)
            for other_item_id in itemset:
                itemcounts[other_item_id] += 1

        # Sort by count, descending, then take the k first items.
        return sorted(
                itemcounts.iterkeys(),
                key=lambda k: itemcounts[k],
                reverse=True)[:k]


class Server(tornado.web.RequestHandler):
    def initialize(self, recz):
        self.recz = recz

    def get(self):
        item_id = self.get_argument('itemId')
        k = int(self.get_argument('k', 5))
        start_recommend = clock()
        self.write({'itemIds': self.recz.recommend(item_id, k)})
        print "Recommended %d items for %s in %f seconds." % 
              (k, item_id, clock() - start_recommend)


if __name__ == "__main__":
    recz = Recz()

    i = 0
    start_read = clock()
    for line in fileinput.input():
      vals = line.split()
      if len(vals) == 2:
        item_id, session_id = vals
        recz.add_example(item_id, session_id)
        i += 1

    recz.compact()
    print "Processed %d examples in %f seconds." % (i, clock() - start_read)

    app = tornado.web.Application([(r'/recommend', Server, dict(recz=recz)),])
    app.listen(PORT)
    print "Server ready and listening at port %d!" % PORT
    tornado.ioloop.IOLoop.instance().start()
