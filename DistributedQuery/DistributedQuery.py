
import queryplan
import json
import utils

#Step 0: Inizializzazione
qp_json = open('queryplan.json')
hosp_json = open('hosp.json')
ins_json = open('ins.json')
pri_json = open('priority.json')

qp_dict = json.load(qp_json)

#Carico i json con le autorizzazioni delle tabelle
lista_tab_json = []
lista_tab_json.append(json.load(hosp_json))
lista_tab_json.append(json.load(ins_json))

subj_dict = utils.build_initial_json(lista_tab_json)

#Assegno le priorità
pri_dict = json.load(pri_json)
utils.give_priority(subj_dict, pri_dict)

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
	print("Node: " + str(i) + "\n-> Candidates: " + str(cand) + "\n-> Assignee: " + assegn + "\n\n\tvp: " + str(list(vp)) + "\n\tve: " + str(list(ve)) + "\n\tip: " + str(list(ip)) + "\n\tie: " + str(list(ie)) + "\n\teq: " + str(list(eq)) + "\n=====================\n")

lista_ocd = qp.get_ocd()
print("=== ENCRYPTION OPERATIONS ===")
for ocd in lista_ocd: 
	print(("Encryption of " if ocd["tipo_op"] == "C" else "Decifratura ") + "attributes " + str(ocd["adc"]) + " between nodes " + str(ocd["figlio"]) + " and " + str(ocd["padre"]) + " by subject " + ocd["exec"])

lista_asc = qp.get_asc()
print("\r\n=== KEY ENCRYPTION SETS ===")
for asc in lista_asc:
	print(" - " + str(asc))

print("\nEnd of computation...\n\n")