

class query_plan(object):
    """Classe che rappresenta l'albero della query"""

    def __init__(self):
        self.lista_nodi = {}

    def add_node(self, id, nodo):
        self.lista_nodi[id] = nodo

    def add_node(self, id, tipo_op, set_attributi):
        nodo = nodo_plan(tipo_op=tipo_op, set_attr=set_attributi)
        self.lista_nodi[id] = nodo


    #I profili sono calcolati secondo una visita post-order
    def calcola_profilo(self, id):

        #Determino i figli del nodo corrente
        figli = []
        
        for nodo_tmp in self.lista_nodi:
            if nodo_tmp.id_padre == id:
                figli.append(nodo_tmp.id)

        if nodo.tipo_op not in ["cart", "join", "set"]:
            #Solo un figlio → Mi recupero il suo profilo
            calcola_profilo(figli[0])
            self.lista_nodi[id].profilo = self.lista_nodi[figli[0]].profilo

        elif nodo.tipo_op in ["cart", "join"]:
            #Cartesian / Join → Determino i figlio del nodo corrente

            #Lancio il calcola_profilo iterativamente su tutti i figli
            for figlio in figli:
                calcola_profilo(figlio)
            
                #Per tutti i figli, faccio l'union degli insiemi (escluso che per le join e prodotti cartesiani, il figlio sarà uno solo sempre)
                for i in range(0, 4):
                    self.lista_nodi[id].profilo[i].union(self.lista_nodi[figlio].profilo[i])

                self.lista_nodi[id].profilo["eq"].append(self.lista_nodi[figlio].profilo["eq"])

        #Determino il profilo del nodo corrente
        if self.lista_nodi[id].tipo_op == "proj":
            self.lista_nodi[id].profilo["vp"] = self.lista_nodi[id].profilo["vp"].intersection(self.lista_nodi[id].set_attr)
            self.lista_nodi[id].profilo["ve"] = self.lista_nodi[id].profilo["ve"].intersection(self.lista_nodi[id].set_attr)

        elif self.lista_nodi[id].tipo_op == "sel_val":
            self.lista_nodi[id].profilo["ip"] = self.lista_nodi[id].profilo["ip"].union(self.lista_nodi[id].profilo["vp"]).intersection(self.lista_nodi[id].set_attr)
            self.lista_nodi[id].profilo["ie"] = self.lista_nodi[id].profilo["ie"].union(self.lista_nodi[id].profilo["ve"]).intersection(self.lista_nodi[id].set_attr)

        elif self.lista_nodi[id].tipo_op == "sel_attr":
           self.lista_nodi[id].profilo["eq"].append(self.lista_nodi[id].set_attr)       #Qua viene aggiunto un set dentro al set → rappresentare il set di attributi come frozenset o come tupla

        elif self.lista_nodi[id].tipo_op == "join":
            self.lista_nodi[id].profilo["eq"].append(self.lista_nodi[id].set_attr)       #Discorso analogo per sel_attr

        elif self.lista_nodi[id].tipo_op == "gby":
            self.lista_nodi[id].profilo["vp"] = self.lista_nodi[id].profilo["vp"].intersection(self.lista_nodi[id].set_attr.union(self.lista_nodi[id].set_oper))
            self.lista_nodi[id].profilo["ve"] = self.lista_nodi[id].profilo["ve"].intersection(self.lista_nodi[id].set_attr.union(self.lista_nodi[id].set_oper))
            self.lista_nodi[id].profilo["ip"] = self.lista_nodi[id].profilo["ip"].union(self.lista_nodi[id].profilo["vp"].intersection(self.lista_nodi[id].set_attr))
            self.lista_nodi[id].profilo["ie"] = self.lista_nodi[id].profilo["ie"].union(self.lista_nodi[id].profilo["ve"].intersection(self.lista_nodi[id].set_attr))

        elif self.lista_nodi[id].tipo_op == "set":
            for figlio in figli:
                #Calcolo i profili dei figli
                calcola_profilo(figlio)

                #Figlio più a sinistra → lo uso per gli attributi visibili in plain e cifrati
                if self.lista_nodi[figlio].ordine == 0:
                    self.lista_nodi[id].profilo["vp"] = self.lista_nodi[figlio].profilo["vp"]
                    self.lista_nodi[id].profilo["ve"] = self.lista_nodi[figlio].profilo["ve"]

                #Ottengo gli attributi impliciti in plain e cifrati come unione diq uelli di tutti i figli
                self.lista_nodi[id].profilo["ip"].union(self.lista_nodi[figlio].profilo["ip"])
                self.lista_nodi[id].profilo["ie"].union(self.lista_nodi[figlio].profilo["ie"])

                #Le relazioni di equivalenza sono ottenute come unione tra gli insiemi delle tabelle, e tutto l'arrcocchio degli attributi visibili
                self.lista_nodi[id].profilo["eq"].append(self.lista_nodi[figlio].profilo["eq"])

                #Determino tutte gli insiemi di attributi delle varie relazioni in modo posizione (primo di R1 con primo di R2 e primo di R3...)

    def sistema_eq(self, id):
        self.lista_nodi[id]

                
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
        self.profilo["vp"] = set()
        self.profilo["ve"] = set()
        self.profilo["ip"] = set()
        self.profilo["ie"] = set()
        self.profilo["eq"] = []