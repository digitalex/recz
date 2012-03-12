#!/usr/bin/python

import fileinput
import tornado.web
import tornado.ioloop
from time import clock
from recz import Recz

PORT = 8888

class Server(tornado.web.RequestHandler):
    def initialize(self, recz):
        self.recz = recz

    def get(self):
        item_id = self.get_argument('itemId')
        k = int(self.get_argument('k', 5))
        start_recommend = clock()
        self.write({'itemIds': self.recz.recommend(item_id, k)})
        print "Recommended %d items for %s in %f seconds." % (k, item_id, clock() - start_recommend)

    @staticmethod
    def main():
        n = 0
        recz = Recz()
        start_read = clock()
        for line in fileinput.input():
          vals = line.split()
          if len(vals) == 2:
            item_id, session_id = vals
            recz.add_example(item_id, session_id)
            n += 1
        recz.compact()

        print "Processed %d examples in %f seconds." % (n, clock() - start_read)
        app = tornado.web.Application([(r'/recommend', Server, dict(recz=recz)),])
        app.listen(PORT)

        print "Server ready and listening at port %d!" % PORT
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    Server.main()
