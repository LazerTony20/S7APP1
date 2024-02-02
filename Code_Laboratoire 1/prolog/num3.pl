%%
%% Auteur: Charles-Antoine Brunet
%% Date: 2015-07-27
%% Modifié par : Audrey Corbeil Therrien
%% Date: 2024-01-18
%% Solution au probleme "Trouver les actions possibles"
%%
%% Test du guide:
%%
%% actionsPossibles([on(b,table),on(a,table),on(c,a),clear(b),
%%                   clear(c),block(a),block(b),block(c)],R).
%%

action(Env, move(B, X, Y))  :-
    member(on(B,X), Env),
    member(clear(B), Env),
    member(clear(Y), Env),
    member(block(B), Env),
    member(block(Y), Env),
    B \= X, B \= Y, X \= Y.
 
 action(Env, moveToTable(B,X)) :-
    member(on(B, X), Env),
    member(clear(B), Env),
    member(block(B), Env),
    B \= X, X \= table.
 
 actionsPossibles(Env, Res) :-
    findall(Action, action(Env, Action), Res).
 