#!/usr/bin/python

import fileinput
from recz import Recz

class Dumper:
    @staticmethod
    def main():
        n = 0
        recz = Recz()
        for line in fileinput.input():
          vals = line.split()
          if len(vals) == 2:
            item_id, session_id = vals
            recz.add_example(item_id, session_id)
            n += 1
        recz.compact()
        recz.dump()

if __name__ == "__main__":
    Dumper.main()
