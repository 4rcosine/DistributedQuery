
import queryplan
import json

#Step 0: Inizializzazione
qp_json = open('queryplan.json')
subj_json = open('soggetti.json')

subj_dict = json.load(subj_json)
qp_dict = json.load(qp_json)

qp = queryplan.query_plan()

for chiave, valore in qp_dict.items():
    qp.add_nodo(int(chiave), valore["tipo_op"], set(valore["set_attr"]), set(valore["set_oper"]), set(valore["set_attrplain"]), valore["id_padre"], valore["ordine"])

qp.set_subj(subj_dict)

#Step 1: Calcolo della funzione di assegnamento dei candidati
qp.esegui_step_rec(1, True)

#Step 2: Assegnazione del soggetto e estensione del query plan
qp.esegui_step_rec(1, False)

#Step 3: Output
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