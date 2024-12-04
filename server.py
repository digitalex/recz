#!/usr/bin/python

import fileinput
import tornado.web
import tornado.ioloop
import os
import sys
import time
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

    def post(self):
        item_id = self.get_argument('itemId')
        session_id = self.get_argument('sessionId')
        self.recz.add_example(item_id, session_id)
        self.write({})

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
        app = tornado.web.Application([(r'/recommend', Server, dict(recz=recz)), (r'/post', Server, dict(recz=recz))])
        app.listen(PORT)

        if "--test" in sys.argv:
            time.sleep(1)
            os.system('curl -X POST -d "itemId=123&sessionId=456" http://localhost:8888/post')
            time.sleep(1)
            test_output = os.popen('curl http://localhost:8888/recommend?itemId=123&k=1').read()
            if '"itemIds": [' not in test_output or ']' not in test_output:
                print("Test failed! Unexpected output format.")
                print(test_output)

                sys.exit(1)

            start_index = test_output.find('"itemIds": [') + len('"itemIds": [')
            end_index = test_output.find(']', start_index)
            recommended_items = test_output[start_index:end_index].strip()

            if recommended_items:
                print("Test passed!")
            else:
                print("Test failed! No items recommended.")
                sys.exit(1)

        else:
            print "Server ready and listening at port %d!" % PORT
            tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    Server.main()
