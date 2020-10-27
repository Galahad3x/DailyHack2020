c 1 = 1
c n = if even n then 1 + c (n `div` 2) else 1 + c (3*n + 1)
p n m = if c n == m then n else p (n+1) m
main = print $ p 1 $ maximum $ map c $ [1,2..100000]
