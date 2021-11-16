
import queryplan

#Init esempio
authz = dict()

authz["H"] = { 'p' : {'S', 'B', 'D', 'T', 'C'}, 'e' : {'P'}}
authz["I"] = { 'p' : {'B', 'C', 'P'}, 'e' : {'S', 'D', 'T'}}
authz["U"] = { 'p' : {'S', 'D', 'T', 'C', 'P'}, 'e' : {}}
authz["X"] = { 'p' : {'D', 'T'}, 'e' : {'S', 'C', 'P'}}
authz["Y"] = { 'p' : {'B', 'D', 'T', 'P'}, 'e' : {'S', 'C'}}
authz["Z"] = { 'p' : {'S', 'T', 'C'}, 'e' : {'D', 'P'}}
authz["any"] = { 'p' : {'D', 'T'}, 'e' : {'P'}}

qp = queryplan.query_plan()
i = 0
qp.add_nodo(1, 'sel_val', {'P'}, {}, 0, 0)
qp.add_nodo(2, 'decr', {'P'}, {}, 1, 0)
qp.add_nodo(3, 'gby', {'T'}, {'P'}, 2, 0)
qp.add_nodo(4, 'join', {'S', 'C'}, {}, 3, 0)

qp.add_nodo(5, 'sel_val', {'D'}, {}, 4, 0)
qp.add_nodo(6, 'encr', {'S', 'D', 'T'}, {}, 5, 0)
qp.add_nodo(7, 'proj', {'S', 'D', 'T'}, {}, 6, 0)
qp.add_nodo(8, 'base', {'S', 'B', 'D', 'T'}, {}, 7, 0)

qp.add_nodo(9, 'encr', {'C', 'P'}, {}, 4, 1)
qp.add_nodo(10, 'base', {'C', 'P'}, {}, 9, 1)

''' Senza cifratura
qp.add_nodo(1, 'sel_val', {'P'}, {}, 0, 0)
qp.add_nodo(2, 'gby', {'T'}, {'P'}, 1, 0)
qp.add_nodo(3, 'join', {'S', 'C'}, {}, 2, 0)
qp.add_nodo(4, 'sel_val', {'D'}, {}, 3, 0)
qp.add_nodo(5, 'proj', {'S', 'D', 'T'}, {}, 4, 0)
qp.add_nodo(6, 'base', {'S', 'B', 'D', 'T'}, {}, 5, 0)
qp.add_nodo(7, 'base', {'C', 'P'}, {}, 3, 1)
'''

qp.calcola_profilo(1)
qp.calcola_candidati(authz)

for i in range(1, 8):
    nodo = qp.get_nodo(i)
    vp, ve, ip, ie, eq, cand = nodo.get_profilo()
    print(str(i) + " -> Candiati: " + str(cand) + "\n\tvp: " + str(list(vp)) + "\n\tve: " + str(list(ve)) + "\n\tip: " + str(list(ip)) + "\n\tie: " + str(list(ie)) + "\n\teq: " + str(list(eq)) + "\n=====================")