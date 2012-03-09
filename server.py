#!/usr/bin/python
import fileinput
import tornado.web
import tornado.ioloop

PORT = 8888

class Recz:
    def __init__(self):
        self.sessions = {}

    def add_example(self, item_id, session_id):
        self.sessions.setdefault(item_id, set()).add(session_id)

    def compact(self):
        for key in filter(lambda k: len(self.sessions[k])<2, self.sessions.iterkeys()):
          del self.sessions[key]

    def recommend(self, item_id, k=5):
        data = dict(self.sessions)
        try:
            itemset = data.pop(item_id)
            return sorted(data.keys(), key=lambda k: len(data[k] & itemset),reverse=True)[:k]
        except KeyError:
            return []

class Server(tornado.web.RequestHandler):
    def initialize(self, recz):
        self.recz = recz

    def get(self):
        k = int(self.get_argument('k', 5))
        item_id = self.get_argument('itemId')
        self.write(str(self.recz.recommend(item_id, k)))

if __name__ == "__main__":
    recz = Recz()

    for line in fileinput.input():
      vals = line.split()
      if len(vals) == 2:
        item_id, session_id = vals
        recz.add_example(item_id, session_id)

    recz.compact()
    app = tornado.web.Application([(r'/recommend', Server, dict(recz=recz)),])
    app.listen(PORT)
    print "Server ready and listening at port %d!" % PORT
    tornado.ioloop.IOLoop.instance().start()
