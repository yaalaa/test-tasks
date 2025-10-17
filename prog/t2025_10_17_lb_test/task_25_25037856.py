# поиск 5 наибольших чисел, не превышающих 1 200 000, у которых значение S суммы трёх наибольших нетривиальных делителей, не превышающих
# половину самого числа, делится на 2022, отлично от 0 и не равно самому числу
import math
dv = 2022

def S(n):
    (sm,d_count) = (0,0)
    for i in range(n//2,2-1,-1):
        if n%i == 0:
            sm += i
            d_count += 1
            if d_count == 3: break
    if d_count == 3 and sm != n and sm%dv == 0: return sm
    else: return 0

def numbers_generator():
    (n,count) = (1_200_001,0)
    
    while count < 5:
        n -= 1
        S_ = S(n)
        if S_ != 0:
            count += 1
            yield (n,S_)

for t in sorted(numbers_generator(),key = lambda t: t[0]): print(t)
