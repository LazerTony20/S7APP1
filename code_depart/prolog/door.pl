ouvrirPorte(Array,Position) :- compteurCouleur(Array,Result,Count),((Count =:=3,regle3Cristaux(Result,Position),!);((Count =:=4, getMetal(Array,Metal),regle4Cristaux(Result,Metal,Position),!));((Count =:=5, getMetal(Array,Metal),regle5Cristaux(Result,Metal,Position),!));((Count =:=6, getMetal(Array,Metal),regle6Cristaux(Result,Metal,Position),!))).

regle3Cristaux(Array,Position) :- getColor(Array,'red',Count,_), Count=:= 0, Position = 'second'.
regle3Cristaux([_,_,Z|_],Position) :- Z == 'white', Position = 'third'.
regle3Cristaux(Array,Position) :- getColor(Array,'blue',Count,Last), Count > 1, getPosition(Last,Position).
regle3Cristaux(_,Position) :- Position = 'first'.

regle4Cristaux(Array,Metal,Position) :- Metal == 'silver', getColor(Array,'red',Count,Last), Count > 1, getPosition(Last,Position).
regle4Cristaux(Array,_,Position) :- getColor(Array,'yellow',_,Last), getColor(Array,'red',Count,_), Count=:= 0,Last =:= 4, Position = 'first'.
regle4Cristaux(Array,_,Position) :- getColor(Array,'blue',Count,_), Count =:= 1, Position = 'first'.
regle4Cristaux(Array,_,Position) :- getColor(Array,'yellow',Count,_), Count > 1,Position = 'fourth'.
regle4Cristaux(_,_,Position) :- Position = 'second'.

regle5Cristaux(Array,Metal,Position) :- Metal == 'gold', getColor(Array,'black',_,Last), Last =:= 5, Position = 'fourth'.
regle5Cristaux(Array,_,Position) :- getColor(Array,'red',CountRed,_), CountRed =:= 1, getColor(Array, 'yellow', CountYellow, _), CountYellow > 1, Position = 'first'.
regle5Cristaux(Array,_,Position) :- getColor(Array,'black',Count,_), Count =:= 0, Position = 'second'.
regle5Cristaux(_,_,Position) :- Position = 'first'.

regle6Cristaux(Array,Metal,Position) :- Metal == 'bronze', getColor(Array,'yellow',Count,_),Count =:= 0, Position = 'third'.
regle6Cristaux(Array,_,Position) :- getColor(Array,'yellow',CountYellow,_), CountYellow =:= 1, getColor(Array, 'white', CountWhite, _), CountWhite > 1, Position = 'fourth'.
regle6Cristaux(Array,_,Position) :- getColor(Array,'red',Count,_), Count =:= 0, Position = 'sixth'.
regle6Cristaux(_,_,Position) :- Position = 'forth'.

getColor(Array,TargetColor, Count,Last) :- getColorSub(Array, TargetColor, 1, 0, 0, Count, Last).
getColorSub([], _, _, Count, Last, Count, Last).
getColorSub([Color|Qliste], TargetColor, CurrentIndex, CurrentCount, CurrentLast, Count, Last) :- 
    ((
        Color == TargetColor,
        NextCount is CurrentCount + 1,
        NextLast is CurrentIndex)
    ;(
        Color \= TargetColor,
        NextCount is CurrentCount,
        NextLast is CurrentLast
    )),
    NextIndex is CurrentIndex + 1,
    getColorSub(Qliste, TargetColor, NextIndex, NextCount, NextLast, Count, Last).
compteurCouleur(Array,Result,Count):- retirerMetal(Array,ArraySansMetal),retirerNull(ArraySansMetal,Result),longueur(Result,Count).
longueur([], 0).
longueur([_|Qliste], NombreItems):- longueur(Qliste, NombreItemsQueue), NombreItems is NombreItemsQueue+1.
retirerMetal([_|ArraySansMetal], ArraySansMetal).
retirerMetal([],[]).
retirerNull([], []).
retirerNull([''|Array], NonNull) :- retirerNull(Array, NonNull).
retirerNull([X|Array], [X|NonNull]) :- X \= '', retirerNull(Array, NonNull).
getMetal([Metal|_], Metal).
getPosition(X,Position) :- (X =:= 1,Position = 'first');(X =:= 2,Position = 'second');(X =:= 3,Position = 'third');(X =:= 4,Position = 'fourth');(X =:= 5,Position = 'fifth');(X =:= 6,Position = 'sixth').