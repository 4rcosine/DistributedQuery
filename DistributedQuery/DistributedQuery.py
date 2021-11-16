
import queryplan

#Init esempio
qp = queryplan.query_plan()
i = 0
qp.add_nodo(1, 'sel_val', {'P'}, {}, 0, 0)
qp.add_nodo(2, 'gby', {'T'}, {'P'}, 1, 0)
qp.add_nodo(3, 'join', {'S', 'C'}, {}, 2, 0)
qp.add_nodo(4, 'sel_val', {'D'}, {}, 3, 0)
qp.add_nodo(5, 'proj', {'S', 'D', 'T'}, {}, 4, 0)
qp.add_nodo(6, 'base', {'S', 'B', 'D', 'T'}, {}, 5, 0)
qp.add_nodo(7, 'base', {'C', 'P'}, {}, 3, 1)

qp.calcola_profilo(1)

for i in range(1, 8):
    nodo = qp.get_nodo(i)
    vp, ve, ip, ie, eq = nodo.get_profilo()
    print(str(i) + ": \n\tvp: " + str(list(vp)) + "\n\tve: " + str(list(ve)) + "\n\tip: " + str(list(ip)) + "\n\tie: " + str(list(ie)) + "\n\teq: " + str(list(eq)) + "\n=====================")