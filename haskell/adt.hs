data T t = A | B Integer | C String t deriving Show

instance Show (a -> b) where
    show f = "Functie"



data Set a = Set (a -> Bool)

is (Set f) e = f e 

data Tree a = Null | Leaf a | Node a (Tree a) (Tree a) | Node a (Tree a) (Tree a) (Tree a)
