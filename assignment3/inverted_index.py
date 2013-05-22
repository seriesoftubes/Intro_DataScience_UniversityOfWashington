import MapReduce
import sys


mr = MapReduce.MapReduce()


def mapper(record):
    book_name, text = record
    for word in text.split():
        mr.emit_intermediate(word, book_name)

def reducer(word, book_names):
    distinct_book_names = set(book_names)
    mr.emit((word, list(distinct_book_names)))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)