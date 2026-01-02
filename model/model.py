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
        for i, squadra in enumerate(self._squadre):
            self._map[squadra.team_id] = squadra
        return self._squadre


# funzione che crea il grafo NON ORDINATO MA PESATO
    def build_graph(self, anno):
        # nodi
        self.G.add_nodes_from(self._squadre)

        # archi
        self.G.edges(data=True)
        # aggiungo i pesi
        for i, s1 in enumerate(self._squadre):
            for s2 in self._squadre[i+1:]:
                if not self.G.has_edge(s1, s2) or not self.G.has_edge(s2, s1):
                    self.G.add_edge(s1, s2, weight = s1.somma_salario + s2.somma_salario)
                else:
                    self.G[s1][s2]['weight'] += s1.somma_salario + s2.somma_salario

        lista_squadre_contrario = sorted(self._squadre, reverse=True)
        for i, s1 in enumerate(lista_squadre_contrario):
            for s2 in self._squadre[:i-1]:
                if not self.G.has_edge(s2, s1) or not self.G.has_edge(s1, s2):
                    self.G.add_edge(s2, s1, weight = s1.somma_salario + s2.somma_salario)
                else:
                    self.G[s2][s1]['weight'] += s1.somma_salario + s2.somma_salario

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
        connessi = list(connessi)
        return connessi


# funzione che fa partire la ricorsione
    def compute_best_set(self, start_node, max_salario):
        """Ricerca ricorsiva del set massimo di album nella componente connessa"""
        component = self.connessi(start_node)
        self.soluzione_best = []
        self._ricorsione(component, [start_node], start_node.somma_salario, max_salario)
        return self.soluzione_best

    def _ricorsione(self, albums, current_set, current_salario, max_salario):
        # condizione per chiudere la ricorsione
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set[:]

        # condizione di ricorsione
        for squadra in self._squadre:
            if squadra in current_set:
                continue
            new_salario = current_salario + squadra.duration
            if new_salario <= max_salario:
                current_set.append(squadra)
                self._ricorsione(albums, current_set, new_salario, max_salario)
                current_set.pop()