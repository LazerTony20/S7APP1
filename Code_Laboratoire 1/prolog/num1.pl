% Numero 1 laboratoire Prologue
horsdoeuvre(salade, 1).
horsdoeuvre(pate, 6).
plat(sole, 2).
plat(thon, 4).
plat(porc, 7).
plat(boeuf, 3).
dessert(glace, 5).
dessert(fruit, 1).

repas(H, P, D) :- horsdoeuvre(H, X), plat(P, Y), dessert(D, Z), W is X+Y+Z, W >= 10.
repasLeger(H, P, D) :- horsdoeuvre(H, X), plat(P, Y), dessert(D, Z), W is X+Y+Z, W < 10.