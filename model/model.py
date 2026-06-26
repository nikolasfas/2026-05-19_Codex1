import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapA = {}

    def handlePath(self, start_id):

        start = self._idMapA[int(start_id)]

        self._bestPath = []
        parziale = [start]

        self._ricorsione(parziale, 0)

        return self._bestPath

    def _ricorsione(self, parziale, currentValue):
        print(parziale ,  currentValue)

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                newValue = self._graph[parziale[-1]][n]['weight']

                if newValue > currentValue:

                    parziale.append(n)
                    self._ricorsione(parziale, newValue)
                    parziale.pop()


    def getMostInfluent(self):

        mostInfluenti = []

        for node in self._graph.nodes:
            pesoE = 0
            pesoU = 0

            for u, v, data in self._graph.in_edges(node, data=True):
                pesoE += data['weight']
            for u, v, data in self._graph.out_edges(node, data=True):
                pesoU += data['weight']

            influenza = pesoU-pesoE
            mostInfluenti.append((node, influenza))
        mostInfluenti.sort(key=lambda x: x[1], reverse=True)
        mostInfluent = mostInfluenti[0]

        return mostInfluent

    def bestEdges(self):

        edges = list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'], reverse=True)
        bestFive = edges[:5]
        return bestFive



    def getAllGenres(self):
        genres = DAO.getAllGenre()
        return genres

    def buildGraph(self, genreId):
        self._graph.clear()

        artists = DAO.getArtists(genreId)
        for artist in artists:
            self._idMapA[artist.ArtistId] = artist
        self._graph.add_nodes_from(artists)

        connections =  DAO.getConnections(genreId)
        for connection in connections:
            a1 = self._idMapA[connection[0]]
            pop1 = int(connection[1])
            a2 = self._idMapA[connection[2]]
            pop2 = int(connection[3])

            if a1 in self._graph.nodes and a2 in self._graph.nodes:
                if pop1 > pop2:
                    self._graph.add_edge(a1, a2, weight= pop1+pop2)
                elif pop2 > pop1:
                    self._graph.add_edge(a2, a1, weight= pop2+pop1)
                else:
                    self._graph.add_edge(a1, a2, weight= pop1+pop2)
                    self._graph.add_edge(a2, a1, weight=pop2 + pop1)

    def getGraphDetails(self):
        nodes = self._graph.nodes()
        edges = self._graph.edges()
        return nodes, edges

