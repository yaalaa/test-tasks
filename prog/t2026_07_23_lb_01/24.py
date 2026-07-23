# поиск наибольшей длины подстроки, которая является корректным арифметическим выражением (без стоящих рядом операций, состоящей из не более чем 50 натуральных чисел,
# без унарных плюсов) (1-9 * +)
from re import finditer

f = open('24.txt')
s = f.readline().strip()
f.close()

number = r'[1-9]+'
search_data = finditer(fr'{number}(?:[+*]{number}){{0,49}}',s)  # {0,49}
print(fr'{number}(?:[+*]{number}){{0,49}}')

def max_key(t): return t.end() - t.start()
print(max_key(max(search_data,key = max_key)))
