import collections
import sys

import MapReduce


mr = MapReduce.MapReduce()
#5 X 5 matrices, must hard code those dimensions for this solution to work
#within the parameters of this assignment
number_of_columns_in_matrix_b = 5
number_of_rows_in_matrix_a = 5


def mapper(matrix_element):
    matrix_name, row, column, value = matrix_element
    if matrix_name.lower() == 'a':
        index_and_value = (column, value)
        for product_matrix_column_number in xrange(number_of_columns_in_matrix_b):
            product_matrix_coordinates = (row, product_matrix_column_number)
            mr.emit_intermediate(product_matrix_coordinates, index_and_value)
    else:
        index_and_value = (row, value)
        for product_matrix_row_number in xrange(number_of_rows_in_matrix_a):
            product_matrix_coordinates = (product_matrix_row_number, column)
            mr.emit_intermediate(product_matrix_coordinates, index_and_value)

def reducer(row_and_column, indices_and_values):
    values_by_index = collections.defaultdict(list)
    for index, value in indices_and_values:
        values_by_index[index].append(value)
    dot_product = 0
    for index, values in values_by_index.iteritems():
        #sparse matrix so sometimes an accompanying value can be missing 
        if len(values) == 2:
            dot_product += values[0] * values[1]
    row, column = row_and_column
    mr.emit((row, column, dot_product))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)