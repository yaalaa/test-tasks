# поиск натуральных чисел (<=10^10), соответствующих маске 32?056*6, делящихся на 2023 без остатка
import re
dv = 2023

nums = []
for n in range(1_000_000, 10_000_000_000+1):
    if re.fullmatch(r'32\d056(?:\d)*6$',str(n)) and n%dv == 0: nums.append((n,n//dv))
            
for t in sorted(nums,key = lambda t: t[0]): print(t)
