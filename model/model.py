import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._genre = None
        self._artists = None

    def getAllGenre(self):
        self._genre = DAO.getAllGenre()
        return self._genre


    def buildGraph(self, genre):
        self._artists = DAO.getArtistByGenre(genre)
        self._graph.add_nodes_from(self._artists)
        self._graph.add_edges_from(DAO.getAllEdges(genre))



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)