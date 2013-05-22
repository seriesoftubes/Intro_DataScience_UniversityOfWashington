import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(one_way_friendship):
    people_involved = frozenset(one_way_friendship)
    mr.emit_intermediate(people_involved, 1)

def reducer(people_involved, one_way_friendships):
    asymmetric = sum(one_way_friendships) == 1
    if asymmetric:
        people = list(people_involved) 
        mr.emit((people[0], people[1]))
        mr.emit((people[1], people[0]))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)  