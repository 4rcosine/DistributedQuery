
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
	qp.add_nodo(int(chiave), valore["op_type"], set(valore["set_attr"]), set(valore["set_oper"]), set(valore["set_attrplain"]), valore["parent_id"], valore["order"])

qp.set_subj(subj_dict)

#Step 1: Calcolo della funzione di assegnamento dei candidati
qp.esegui_step_rec(1, True)

#Step 2: Assegnazione del soggetto e estensione del query plan
qp.esegui_step_rec(1, False)

#Step 3: Output
lista_ocd = qp.get_ocd()
lista_asc = qp.get_asc()

for i in range(1, 8):
	nodo = qp.get_nodo(i)
	vp, ve, ip, ie, eq, cand, assegn, operazione, attributi, operandi = nodo.get_profilo()
	print("Node: " + str(i))
	print("-> Operation: " + utils.ope_name[operazione], end='')
	
	#Parti di output generate in base al tipo di operazione
	if operazione == "gby":
		print(" - operation on attribute(s) " + str(operandi).replace("'", "") + ", grouping", end='')

	if operazione != "base":
		print(" on attribute(s) " + str(attributi).replace("'", ""), end='')


	print("")
	print("-> Candidates: " + str(cand).replace("'", ""))
	print("-> Assignee: " + assegn + "\n\n\tvp: " + str(list(vp)).replace("'", ""))
	print("\tve: " + str(list(ve)).replace("'", "") + "\n\tip: " + str(list(ip)).replace("'", "") + "\n\tie: " + str(list(ie)).replace("'", "") + "\n\teq: " + str(list(eq)).replace("'", ""))

	#Parti di output generate in base all'eventuale cifratura
	for ocd in lista_ocd:
		if i == ocd["figlio"] and ocd["tipo_op"] == "C":
			print("\n-> Encryption of attribute(s) " + str(ocd["adc"]).replace("'", "") + " by subject " + ocd["exec"])

		if i == ocd["padre"] and ocd["tipo_op"] == "D":
			print("\n-> Decryption of attribute(s) " + str(ocd["adc"]).replace("'", "") + " by subject " + ocd["exec"])

	print("\n=====================\n")



#print("=== ENCRYPTION OPERATIONS ===")
#for ocd in lista_ocd: 
#	print("\n-> " + ("Encryption of " if ocd["tipo_op"] == "C" else "Decryption ") + "attributes " + str(ocd["adc"]).replace("'", "") + " between nodes " + str(ocd["figlio"]).replace("'", "") + " and " + str(ocd["padre"]).replace("'", "") + " by subject " + ocd["exec"])


print("\r\n=== KEY ENCRYPTION SETS ===")
for asc in lista_asc:
	print(" • " + str(asc).replace("'", ""))

print("\nEnd of computation\n\n")