isList([]).
isList([_|_]).

flatten([], []).
flatten([H|T], [H|Rest]) :- not(isList(H)), flatten(T, Rest).
flatten([H|T], Rest) :- isList(H), flatten(T, R1), append(H, R1, Rest).
