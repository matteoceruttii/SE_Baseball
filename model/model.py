import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._anni = DAO.selezionaAnno()
        self._squadre = []
        self._map = {}


# funzione che gestisce le squadre relative all'anno scelto
    def squadreAnno(self, anno):
        # lista di tuple
        self._squadre = DAO.getSquadreAnno(anno)
        return self._squadre


# funzione che crea il grafo NON ORDINATO MA PESATO
    def build_graph(self, anno):
        # nodi
        self.G.add_nodes_from(self._squadre)

        # archi
        self.G.edges(data=True)
        # pesi
        salari = DAO.getSalario(anno)
        for i, s1 in enumerate(self._squadre):
            for s2 in self._squadre[i+1:]:
                if not self.G.has_edge(s1, s2):
                    self.G.add_edge(s1, s2, weight = salari[i].somma_salario)
                else:
                    self.G[s1]['weight'] += salari[i].somma_salario
        print(self.G)
        for arco in self.G.edges(data = True):
            print(arco)


# funzione che restituisce la lista di nodi connessi a quello inserito in input tramite libreria networkx
    def connessi(self, utente):
        for nodo in self.G.nodes():
            if utente == nodo.team_code:
                nodo_partenza = nodo

        # ricavo i nodi connessi al nodo dato
        connessi = nx.descendants(self.G, source = nodo_partenza)
        return connessi