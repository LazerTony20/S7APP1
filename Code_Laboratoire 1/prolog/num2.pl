un_sur_deux([],[]).
un_sur_deux([_,Y|QList],[Y|Z]) :- un_sur_deux(QList,Z).
un_sur_deux([_],[ ]).