program task_25_25037848_01; //поиск натуральных чисел (<=10^10), соответствующих маске 32?056*6, делящихся на 2023 без остатка
const dv = 2023;

begin
  var nums := new List<(BigInteger,BigInteger)>;
  for var n:=1_000_000 to 10_000_000_000 do begin if Regex.IsMatch(n.ToString,'^32\d056(?:\d)*6$') and (n mod dv = 0) then nums.Add((n,n div dv)); end;
 
  foreach var t in nums.OrderBy(t->t[0]) do println(t);
end.