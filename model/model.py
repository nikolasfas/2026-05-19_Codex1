import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._genre = None
        self._artists = None
        self._sales = None
        self._idMap = {}

    def getAllGenre(self):
        self._genre = DAO.getAllGenre()
        return self._genre

    def getAllArtists(self, genre):
        return DAO.getArtistByGenre(genre)


    def buildGraph(self, genre):
        self._artists = DAO.getArtistByGenre(genre)

        for a in self._artists:
            self._idMap[a.ArtistId] = a

        self._graph.add_nodes_from(self._artists)
        self._sales = DAO.getAllEdges(genre, self._idMap)

        for a1, a2, peso in self._sales:
            self._graph.add_edge(a1, a2, weight=peso)

        influenza = None
        top_infl = None

        for n in self._graph.nodes:
            peso_uscenti = 0
            peso_entranti = 0

            for u, v, data in self._graph.out_edges(n, data=True):
                peso_uscenti += data["weight"]

            for u, v, data in self._graph.in_edges(n, data=True):
                peso_entranti += data["weight"]

            infl_n = peso_uscenti - peso_entranti

            if influenza is None or infl_n > influenza:
                influenza = infl_n
                top_infl = n

        top_influenza = (top_infl.Name, influenza)

        archi = list(self._graph.edges(data=True))
        archi.sort(key = lambda x: x[2]["weight"], reverse = True)
        top_5 = archi[:5]

        return top_influenza, top_5

    def getPercorso(self, artist):
        self._bestPath = []
        self._ricorsione([artist], 0)
        return self._bestPath

    def _ricorsione(self, parziale, peso_precedente):
        current = parziale[-1]

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for vicino in self._graph.successors(current):
            if vicino not in parziale:
                peso = self._graph[current][vicino]["weight"]

                if peso > peso_precedente:
                    parziale.append(vicino)
                    self._ricorsione(parziale, peso)
                    parziale.pop()




    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)