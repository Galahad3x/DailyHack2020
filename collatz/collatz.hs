c 1 = 1
c n = if odd n then 1 + c (3*n + 1) else 1 + c (div n 2)
p n m = if c n == m then n else p (n+1) m
main = print $ p 1 $ maximum $ map c [1..100000]
