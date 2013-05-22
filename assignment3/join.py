import collections
import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(order_id, records):
    data_by_table_name = collections.defaultdict(list)
    for record in records:
        data_by_table_name[record[0]].append(record) 
    order_data = data_by_table_name['order'][0]
    for line_item_data in data_by_table_name['line_item']:
        mr.emit(order_data + line_item_data)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)