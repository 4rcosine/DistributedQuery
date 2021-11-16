

class query_plan(object):
	"""Classe che rappresenta l'albero della query"""

	def __init__(self):
		self.lista_nodi = {}

	def add_nodo(self, id, nodo):
		self.lista_nodi[id] = nodo

	def add_nodo(self, id, tipo_op, set_attributi, set_operandi, id_padre, ordine):
		nodo = nodo_plan(tipo_op=tipo_op, set_attributi=set_attributi, set_operandi=set_operandi, id_padre=id_padre, ordine=ordine)
		self.lista_nodi[id] = nodo

	def get_nodo(self, id):
		return self.lista_nodi[id]

	#I profili sono calcolati secondo una visita post-order
	def calcola_profilo(self, id):

		#Uso una variabile temporanea per migliorare la leggibilità
		curr_n = self.lista_nodi[id]

		#Determino i figli del nodo corrente
		figli = []
		
		for indice, nodo_tmp in self.lista_nodi.items():
			if nodo_tmp.id_padre == id:
				figli.append(indice)

		if len(figli) > 0:
			#Lancio il calcola_profilo iterativamente su tutti i figli
			for figlio in figli:
				self.calcola_profilo(figlio)
			
				#Per tutti i figli, faccio l'union degli insiemi (escluso che per le join e prodotti cartesiani, il figlio sarà uno solo sempre)
				for i in {'vp', 've', 'ip', 'ie'}:
					self.lista_nodi[id].profilo[i].update(self.lista_nodi[figlio].profilo[i])

				if(len(self.lista_nodi[figlio].profilo["eq"]) > 0):
					for subset in self.lista_nodi[figlio].profilo["eq"]:
						self.lista_nodi[id].profilo["eq"].append(subset)

				self.lista_nodi[id].profilo["rn"].update(self.lista_nodi[figlio].profilo["rn"])

		#Determino il profilo del nodo corrente
		if curr_n.tipo_op == "base":
			self.lista_nodi[id].profilo["vp"] = curr_n.set_attr

		elif curr_n.tipo_op == "proj":
			self.lista_nodi[id].profilo["vp"] = curr_n.profilo["vp"].intersection(curr_n.set_attr)
			self.lista_nodi[id].profilo["ve"] = curr_n.profilo["ve"].intersection(curr_n.set_attr)

		elif curr_n.tipo_op == "sel_val":
			self.lista_nodi[id].profilo["ip"] = curr_n.profilo["ip"].union(curr_n.profilo["vp"].intersection(curr_n.set_attr))
			self.lista_nodi[id].profilo["ie"] = curr_n.profilo["ie"].union(curr_n.profilo["ve"].intersection(curr_n.set_attr))

		elif curr_n.tipo_op == "sel_attr":
		   self.lista_nodi[id].profilo["eq"].append(curr_n.set_attr)       #Qua viene aggiunto un set dentro al set → rappresentare il set di attributi come frozenset o come tupla

		elif curr_n.tipo_op == "join":
			self.lista_nodi[id].profilo["eq"].append(curr_n.set_attr)       #Discorso analogo per sel_attr

		elif curr_n.tipo_op == "gby":
			self.lista_nodi[id].profilo["vp"] = curr_n.profilo["vp"].intersection(curr_n.set_attr.union(curr_n.set_oper))
			self.lista_nodi[id].profilo["ve"] = curr_n.profilo["ve"].intersection(curr_n.set_attr.union(curr_n.set_oper))
			self.lista_nodi[id].profilo["ip"] = curr_n.profilo["ip"].union(curr_n.profilo["vp"].intersection(curr_n.set_attr))
			self.lista_nodi[id].profilo["ie"] = curr_n.profilo["ie"].union(curr_n.profilo["ve"].intersection(curr_n.set_attr))
		
		elif curr_n.tipo_op == "rename_p":
			self.lista_nodi[id].profilo["rn"][list(curr_n.set_oper)[0]] = list(curr_n.set_attr)[0]
			self.lista_nodi[id].profilo["vp"] = curr_n.profilo["vp"].difference(curr_n.set_attr).union(curr_n.set_oper)

		elif curr_n.tipo_op == "rename_e":
			self.lista_nodi[id].profilo["rn"][list(curr_n.set_oper)[0]] = list(curr_n.set_attr)[0]
			self.lista_nodi[id].profilo["ve"] = curr_n.profilo["ve"].difference(curr_n.set_attr).union(curr_n.set_oper)


		#elif self.lista_nodi[id].tipo_op == "set":
		#    for figlio in figli:
		#        #Calcolo i profili dei figli
		#        calcola_profilo(figlio)

		#        #Figlio più a sinistra → lo uso per gli attributi visibili in plain e cifrati
		#        if self.lista_nodi[figlio].ordine == 0:
		#            self.lista_nodi[id].profilo["vp"] = self.lista_nodi[figlio].profilo["vp"]
		#            self.lista_nodi[id].profilo["ve"] = self.lista_nodi[figlio].profilo["ve"]

		#        #Ottengo gli attributi impliciti in plain e cifrati come unione diq uelli di tutti i figli
		#        self.lista_nodi[id].profilo["ip"].union(self.lista_nodi[figlio].profilo["ip"])
		#        self.lista_nodi[id].profilo["ie"].union(self.lista_nodi[figlio].profilo["ie"])

		#        #Le relazioni di equivalenza sono ottenute come unione tra gli insiemi delle tabelle, e tutto l'arrcocchio degli attributi visibili
		#        self.lista_nodi[id].profilo["eq"].append(self.lista_nodi[figlio].profilo["eq"])

		#        #Determino tutte gli insiemi di attributi delle varie relazioni in modo posizione (primo di R1 con primo di R2 e primo di R3...)
		
		elif curr_n.tipo_op == "udf":
			self.lista_nodi[id].profilo["vp"] = curr_n.profilo["vp"].difference((curr_n.set_attr.difference(curr_n.set_oper)))
			self.lista_nodi[id].profilo["ve"] = curr_n.profilo["ve"].difference((curr_n.set_attr.difference(curr_n.set_oper)))
			self.lista_nodi[id].profilo["eq"].append(curr_n.set_attr)

		elif curr_n.tipo_op == "encr":
			self.lista_nodi[id].profilo["vp"] = curr_n.profilo["vp"].difference(curr_n.set_attr)
			self.lista_nodi[id].profilo["ve"] = curr_n.profilo["ve"].union(curr_n.set_attr)

		elif curr_n.tipo_op == "decr":
			self.lista_nodi[id].profilo["ve"] = curr_n.profilo["ve"].difference(curr_n.set_attr)
			self.lista_nodi[id].profilo["vp"] = curr_n.profilo["vp"].union(curr_n.set_attr)

		#Se siamo all'altezza del nodo padre significa che non abbiamo più profili da calcolare: sistemiamo le rinomine e gli insiemi eq
		if curr_n.id_padre == 0:
			self.sistema_set(fix_eq=True)



	def sistema_set(self, fix_eq):

		for id, nodo in self.lista_nodi.items():
			#Sistemo le rinomine in vp, ve, ip, ie
			for pseudo, real in nodo.profilo["rn"].items():
				for i in {'vp', 've', 'ip', 'ie'}:
					if pseudo in curr_n.profilo[i]:
						self.lista_nodi[id].profilo[i] = curr_n.profilo[i].difference(pseudo).union(real)

				#Sistemo le rinomine in eq
				for i in range(0, len(nodo.profilo["eq"])):
					if pseudo in nodo.profilo["eq"][i]:
						self.lista_nodi[id].profilo["eq"][i] = nodo.profilo["eq"][i].difference(pseudo).union(real)

			#Sistemo gli insiemi eq (opzionale, solo a scopo visuale)
			if fix_eq == True:
				#Mi ottengo la lista degli attributi in eq
				set_attr = set()
				for elem in self.lista_nodi[id].profilo["eq"]:
					set_attr.update(elem)

				#Creo un dizionario dove per ogni attributo in eq viene specificato il set collassato di appartenenza
				newEq = {}
				oldEq = {'dummy'}

				while oldEq != newEq:
					oldEq = newEq.copy()
					for attr in set_attr:
						newEq[attr] = set()
						for subset in self.lista_nodi[id].profilo["eq"]:
							if attr in subset:
								newEq[attr].update(subset)

				#Terminato il form che crea il dizionario ho un dizionario dove per ogni attributo in eq ho il relativo set collassato: creo una lista ignorando i doppioni
				self.lista_nodi[id].profilo["eq"] = []
				for key, sel in newEq.items():
					if sel not in self.lista_nodi[id].profilo["eq"]:
						self.lista_nodi[id].profilo["eq"].append(sel)

class nodo_plan:
	"""Classe che rappresenta il nodo dell'albero della query"""
	#id = identificativo del nodo, serve per identificare il padre
	#tipo_op = operazione eseguita
	#set_attr = attributi coinvolti dall'operazione
	#set_oper = operandi coinvolti nell'operazione (per group by)
	#id_padre = identificativo del nodo padre
	#ordine = posizione del nodo (per quando ci sono più nodi su un solo livello, come nelle set operation)

	def __init__(self, tipo_op, set_attributi, set_operandi, id_padre, ordine):
		self.tipo_op = tipo_op
		self.set_attr = set_attributi
		self.set_oper = set_operandi
		self.id_padre = id_padre
		self.ordine = ordine
		self.profilo = {}
		self.profilo["vp"] = set()
		self.profilo["ve"] = set()
		self.profilo["ip"] = set()
		self.profilo["ie"] = set()
		self.profilo["eq"] = []
		self.profilo["rn"] = {}

	def get_profilo(self):
		return (self.profilo["vp"], self.profilo["ve"], self.profilo["ip"], self.profilo["ie"], self.profilo["eq"])