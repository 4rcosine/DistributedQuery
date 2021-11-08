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

        #Determino il profilo del nodo corrente


        


class nodo_plan:
    """Classe che rappresenta il nodo dell'albero della query"""
    #id = identificativo del nodo, serve per identificare il padre
    #tipo_op = operazione eseguita
    #set_attributi = attributi coinvolti dall'operazione
    #id_padre = identificativo del nodo padre

    def __init__(self, id, tipo_op, set_attributi, id_padre):
        self.id = id
        self.tipo_op = tipo_op
        self.set_attr = set_attributi
        self.id_padre = id_padre