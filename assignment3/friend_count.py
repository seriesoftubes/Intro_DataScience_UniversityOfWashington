import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    friendship_recipient, friendship_giver = record
    mr.emit_intermediate(friendship_recipient, friendship_giver)

def reducer(friendship_recipient, friendship_givers):
    distinct_givers = set(friendship_givers)
    mr.emit((friendship_recipient, len(distinct_givers)))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)