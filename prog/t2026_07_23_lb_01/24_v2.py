# поиск наибольшей длины подстроки, которая является корректным арифметическим выражением (без стоящих рядом операций, состоящей из не более чем 50 натуральных чисел,
# без унарных плюсов) (1-9 * +)
from re import search,split

separator = '[+*]'
max_sep = 50-1
len_sep = 1

with open('24.txt') as f: lines = split(fr'(?:{separator}{{2,}})',f.readline().strip())

lengths = []
for line in lines:
    if line.count('+') + line.count('*') <= max_sep:
        lengths += [len(line)]
        continue

    word_lengths = list(map(len,split(separator,line)))
    for i in range(len(word_lengths)-max_sep): lengths += [sum(word_lengths[i:i+max_sep+1]) + max_sep*len_sep]

print(max(lengths) if lengths else 'решение не найдено')
