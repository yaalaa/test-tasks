# подобрать к каждой тройке чисел четвёртое число так, чтобы полученные четыре числа могли быть длинами сторон прямоугольника, иначе приписать 0.
# определить сумму всех полученных четвёртых чисел
from pandas import read_excel

df = read_excel('9-10.ods', engine = 'odf')

filter_squares = df[df.nunique(axis = 1) == 1]

filter_rectangles = df[df.nunique(axis = 1) == 2]

last_numbers_for_squares = filter_squares.apply(lambda row: row[:1],axis = 1)

last_numbers_for_rectangles = filter_rectangles.apply(lambda row: row.value_counts().index[-1],axis = 1)

print(last_numbers_for_squares.apply(sum)) # + last_numbers_for_rectangles.apply(sum))

print(last_numbers_for_rectangles.apply(sum))
