

class query_plan(object):
    """Classe che rappresenta l'albero della query"""

    def __init__(self):
        self.lista_nodi = []

    def add_node(self, nodo):
        self.lista_nodi.append(nodo)

    def add_node(self, id, tipo_op, set_attributi):
        nodo = nodo_plan(id, tipo_op, set_attributi)
        self.lista_nodi.append(nodo)


    #I profili sono calcolati secondo una visita post-order
    def calcola_profili(self, nodo):
        #Determino i figlio del nodo corrente
        figli = []
        
        for nodo_tmp in self.lista_nodi:
            if nodo_tmp.id_padre == nodo.id:
                figli.append()

        #Lancio il calcola_profili ricorsivamente su tutti i figli
        for figlio in figli:
            calcola_profili(figlio)
            
            #Per tutti i figli, faccio l'union degli insiemi (escluso che per le join e prodotti cartesiani, il figlio sarà uno solo sempre)
            for i in range(0, 5):
                nodo.profilo[i].union(figlio.profilo[i])

        #Determino il profilo del nodo corrente
        if nodo.tipo_op == "proj":
            nodo.profilo["vp"] = nodo.profilo["vp"].intersection(nodo.set_attr)
            nodo.profilo["ve"] = nodo.profilo["ve"].intersection(nodo.set_attr)

        elif nodo.tipo_op == "sel_val":
            self.profilo["ip"] = nodo.profilo["ip"].union(nodo.profilo["vp"]).intersection(nodo.set_attr)
            self.profilo["ie"] = nodo.profilo["ie"].union(nodo.profilo["ve"]).intersection(nodo.set_attr)

        elif nodo.tipo_op == "sel_attr":
            self.profilo["eq"] = nodo.profilo["eq"].union(nodo.set_attr)       #Qua viene aggiunto un set dentro al set → rappresentare il set di attributi come frozenset o come tupla

        elif nodo.tipo_op == "cart":
            #Non faccio nulla perché prendo l'union fatte precedenti

        elif nodo.tipo_op == "join":
            self.profilo["eq"] = nodo.profilo["eq"].union(nodo.set_attr)       #Discorso analogo per sel_attr

        elif nodo.tipo_op == "gby":
            nodo.profilo["vp"] = nodo.profilo["vp"].intersection(nodo.set_attr.union(nodo.set_oper))
            nodo.profilo["ve"] = nodo.profilo["ve"].intersection(nodo.set_attr.union(nodo.set_oper))
            self.profilo["ip"] = nodo.profilo["ip"].union(nodo.profilo["vp"].intersection(nodo.set_attr))
            self.profilo["ie"] = nodo.profilo["ie"].union(nodo.profilo["ve"].intersection(nodo.set_attr))

        elif 







class nodo_plan:
    """Classe che rappresenta il nodo dell'albero della query"""
    #id = identificativo del nodo, serve per identificare il padre
    #tipo_op = operazione eseguita
    #set_attributi = attributi coinvolti dall'operazione
    #id_padre = identificativo del nodo padre

    def __init__(self, id, tipo_op, set_attributi, set_operandi, id_padre):
        self.id = id
        self.tipo_op = tipo_op
        self.set_attr = set_attributi
        self.set_oper = set_operandi
        self.id_padre = id_padre
        self.profilo["vp"] = set()
        self.profilo["ve"] = set()
        self.profilo["ip"] = set()
        self.profilo["ie"] = set()
        self.profilo["eq"] = set()