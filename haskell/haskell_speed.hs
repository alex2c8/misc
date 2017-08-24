tr ([]:_) = []
tr m = (map head m):(tr (map tail m))

r i j = sum $ zipWith (*) i j
mult m1 m2 = map (\i -> (map (\j -> (r i j)) (tr m2))) m1

n = 4000
v1 = 1.201
v2 = 0.021

mat1 = replicate n (replicate n v1)
mat2 = replicate n (replicate n v2)

res v1 v2 n = let z = mult (replicate n (replicate n v1)) (replicate n (replicate n v2))
              in seq z $ (z !! (n `div` 2)) !! (n `div` 3 - 1)
