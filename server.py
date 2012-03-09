#!/usr/bin/python
import fileinput
import tornado.ioloop
import tornado.web

PORT = 8888

class Recz:
    def __init__(self):
        self.sessions = {}

    def add_example(self, company_id, session_id):
        self.sessions.setdefault(company_id, set()).add(session_id)

    def compact(self):
        for key in filter(lambda k: len(self.sessions[k])<2, self.sessions.iterkeys()):
          del self.sessions[key]

    def recommend(self, company_id, k=5):
        data = dict(self.sessions)
        try:
            itemset = data.pop(company_id)
            return sorted(data.keys(), key=lambda k: len(data[k] & itemset),reverse=True)[:k]
        except KeyError:
            return []


class Server(tornado.web.RequestHandler):
    def initialize(self, recz):
        self.recz = recz

    def get(self):
        k = int(self.get_argument('k', 5))
        company_id = self.get_argument('companyId')
        self.write(str(self.recz.recommend(company_id, k)))

if __name__ == "__main__":
    recz = Recz()

    for line in fileinput.input():
      vals = line.split()
      if len(vals) == 2:
        company_id, session_id = vals
        recz.add_example(company_id, session_id)

    recz.compact()
    app = tornado.web.Application([(r'/recommend', Server, dict(recz=recz)),])
    app.listen(PORT)
    print "Server ready and listening at port %d!" % PORT
    tornado.ioloop.IOLoop.instance().start()
