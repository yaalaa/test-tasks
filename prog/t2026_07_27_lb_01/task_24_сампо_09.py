# определение длины самой длинной подстроки, состоящей из подряд идущих троек одинаковых символов (ABCDEF) (тройки не перекрываются)
from re import finditer

# захват символа, идущего подряд >= 3 раз, далее захват троек одинаковых символов
with open('24_25036900.txt') as f: search_data = [len(t.group()) for t in finditer(r'(?:(.)\1\1*\1)(?:(.)\2{2})*',f.readline().strip())]

maxlen = 0 if not search_data else max(search_data)
print(maxlen - maxlen%3) # не учитываем начальные вхождения первого символа, если он повторяется некратное 3 кол-во раз

# aaaabbbbbb -> 9
