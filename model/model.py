import copy
import math

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._customers = []
        self._graph = nx.Graph()
        self._customersArtists = {}
        self._customersGenres = {}
        self._idMapC = {}

    def handlePath(self, start_id, L):

        start = self._idMapC[start_id]
        parziale = [start]
        self._bestPath = []
        self._bestValue = 0

        self._ricorsione(parziale, L, math.inf, 0)

        return self._bestPath, self._bestValue

    def _ricorsione(self, parziale, L, currentValue, totValue):

        if len(parziale) == L+1:
            if totValue > self._bestValue:
                self._bestValue = totValue
                self._bestPath = copy.deepcopy(parziale)

        if len(parziale) < L+1:

            for n in self._graph.neighbors(parziale[-1]):
                if n not in parziale:
                    newValue = self._graph[parziale[-1]][n]['weight']

                    if newValue < currentValue:

                        parziale.append(n)
                        self._ricorsione(parziale, L, newValue, totValue+newValue)
                        parziale.pop()

    def getCompConn(self):

        compConn = list(nx.connected_components(self._graph))
        numComp = len(compConn)
        maxComp = max(compConn, key=len)

        return numComp, maxComp

    def getMAxCompatibility(self):

        nodoConCompa = []

        nodes = list(self._graph.nodes)
        for n in nodes:

            compa = 0
            for u, v, data in list(self._graph.edges(n, data=True)):
                compa += data['weight']

            nodoConCompa.append((n, compa))

        return max(nodoConCompa, key=lambda x:x[1])


    def getHeaviestEdges(self):

        edges = list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'], reverse=True)
        bestFive = edges[:5]

        return bestFive


    def getCountries(self):
        countries = DAO.getAllCountries()
        return countries

    def _calculateCommonArtists(self, n1, n2):
        commonArtists = set()
        for artist1 in n1.artists:
            if artist1 in n2.artists:
                commonArtists.add(artist1)

        for artist2 in n2.artists:
            if artist2 in n1.artists:
                commonArtists.add(artist2)
        return len(commonArtists)

    def _calculateCommonGenres(self, n1, n2):
        commonGenres = set()
        for genre1 in n1.genres:
            if genre1 in n2.genres:
                commonGenres.add(genre1)

        for genre2 in n2.genres:
            if genre2 in n1.genres:
                commonGenres.add(genre2)

        return len(commonGenres)

    def buildGraph(self, county, S):
        self._graph.clear()
        self._customers.clear()
        self._customersArtists.clear()
        self._customersGenres.clear()
        self._idMapC.clear()

        self._customers = DAO.getAllCustomers(county, S)
        for customer in self._customers:
            self._idMapC[customer.CustomerId] = customer
        self._graph.add_nodes_from(self._customers)

        self.getAllStats(county)

        nodes = list(self._graph.nodes)

        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):

                n1 = nodes[i]
                n2 = nodes[j]

                numCA = self._calculateCommonArtists(n1, n2)
                numCG = self._calculateCommonGenres(n2, n1)

                if numCA >= 1:
                    self._graph.add_edge(n1, n2, weight=numCA+numCG)

    def getAllStats(self, country):

        self._customersArtists, self._customersGenres = DAO.getAllStats(country, self._customersArtists, self._customersGenres)
        for stat in self._customersArtists.keys():
            if stat in self._idMapC:
                customer1 = self._idMapC[stat]
                artists = self._customersArtists[stat]
                if customer1 in self._graph.nodes:
                    customer1.artists.extend(artists)

        for stat in self._customersGenres.keys():
            if stat in self._idMapC:
                customer1 = self._idMapC[stat]
                genres = self._customersGenres[stat]
                if customer1 in self._graph.nodes:
                    customer1.genres.extend(genres)

    def getGraphDetails(self):
        nodes = self._graph.nodes
        edges = self._graph.edges
        return nodes, edges



