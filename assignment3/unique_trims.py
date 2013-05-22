import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(id_and_sequence):
    trimmed_sequence = id_and_sequence[1][:-10]
    mr.emit_intermediate(trimmed_sequence, False)

def reducer(trimmed_sequence, temp):
    mr.emit(trimmed_sequence)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)