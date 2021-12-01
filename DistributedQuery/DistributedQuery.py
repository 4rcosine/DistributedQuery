
import queryplan

#Init esempio
soggetti = dict()

soggetti["H"] = { 'p' : {'S', 'B', 'D', 'T', 'C'}, 'e' : {'P'}, 'own' : {'hosp'}, "pri" : 4}
soggetti["I"] = { 'p' : {'B', 'C', 'P'}, 'e' : {'S', 'D', 'T'}, 'own' : {'ins'}, "pri" : 5}
soggetti["U"] = { 'p' : {'S', 'D', 'T', 'C', 'P'}, 'e' : {}, 'own' : {}, "pri" : 6}
soggetti["X"] = { 'p' : {'D', 'T'}, 'e' : {'S', 'C', 'P'}, 'own' : {}, "pri" : 1}
soggetti["Y"] = { 'p' : {'B', 'D', 'T', 'P'}, 'e' : {'S', 'C'}, 'own' : {}, "pri" : 2}
soggetti["Z"] = { 'p' : {'S', 'T', 'C'}, 'e' : {'D', 'P'}, 'own' : {}, "pri" : 3}
soggetti["any"] = { 'p' : {'D', 'T'}, 'e' : {'P'}, 'own' : {}, "pri" : 7}

qp = queryplan.query_plan()
i = 0

dict_qplan = {
        1 : { "tipo_op" : "sel_val", "set_attr" : {'P'}, "set_oper" : {}, "set_attrplain" : {'P'}, "id_padre" : 0, "ordine" : 0},
        2 : { "tipo_op" : "gby", "set_attr" : {'T'}, "set_oper" : {'P'}, "set_attrplain" : {}, "id_padre" : 1, "ordine" : 0},
        3 : { "tipo_op" : "join", "set_attr" : {'S', 'C'}, "set_oper" : {}, "set_attrplain" : {}, "id_padre" : 2, "ordine" : 0},
        4 : { "tipo_op" : "sel_val", "set_attr" : {'D'}, "set_oper" : {}, "set_attrplain" : {}, "id_padre" : 3, "ordine" : 0},
        5 : { "tipo_op" : "proj", "set_attr" : {'S', 'D', 'T'}, "set_oper" : {}, "set_attrplain" : {}, "id_padre" : 4, "ordine" : 0},
        6 : { "tipo_op" : "base", "set_attr" : {'S', 'B', 'D', 'T'}, "set_oper" : {"hosp"}, "set_attrplain" : {}, "id_padre" : 5, "ordine" : 0},
        7 : { "tipo_op" : "base", "set_attr" : {'C', 'P'}, "set_oper" : {"ins"}, "set_attrplain" : {}, "id_padre" : 3, "ordine" : 1},
    }

qp.add_nodo(1, 'sel_val', {'P'}, {}, {'P'}, 0, 0)
qp.add_nodo(2, 'gby', {'T'}, {'P'}, {}, 1, 0)
qp.add_nodo(3, 'join', {'S', 'C'}, {}, {}, 2, 0)
qp.add_nodo(4, 'sel_val', {'D'}, {}, {}, 3, 0)
qp.add_nodo(5, 'proj', {'S', 'D', 'T'}, {}, {}, 4, 0)
qp.add_nodo(6, 'base', {'S', 'B', 'D', 'T'}, {"hosp"}, {}, 5, 0)
qp.add_nodo(7, 'base', {'C', 'P'}, {"ins"}, {}, 3, 1)

qp.set_subj(soggetti)
qp.esegui_step_rec(1, True)
qp.pulisci_profili()
qp.esegui_step_rec(1, False)

for i in range(1, 8):
    nodo = qp.get_nodo(i)
    vp, ve, ip, ie, eq, cand, assegn = nodo.get_profilo()
    print("Nodo: " + str(i) + "\n-> Candidati: " + str(cand) + "\n-> Assegnatario: " + assegn + "\n\n\tvp: " + str(list(vp)) + "\n\tve: " + str(list(ve)) + "\n\tip: " + str(list(ip)) + "\n\tie: " + str(list(ie)) + "\n\teq: " + str(list(eq)) + "\n=====================\n")

lista_ocd = qp.get_ocd()
print("=== OPERAZIONI CIFRATURA ===")
for ocd in lista_ocd: 
    print(("Cifratura " if ocd["tipo_op"] == "C" else "Decifratura ") + "attributi " + str(ocd["adc"]) + " tra i nodi " + str(ocd["figlio"]) + " e " + str(ocd["padre"]) + " da parte del soggetto " + ocd["exec"])

lista_asc = qp.get_asc()
for asc in lista_asc:
    print("Gli attributi " + str(asc) + " devono essere cifrati con la stessa chiave")

print("\nFine computazione\n\n")