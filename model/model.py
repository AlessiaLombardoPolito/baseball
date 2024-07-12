import copy
import itertools

import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allteams = []
        self._idMapTeams = {}
        self._bestPath = []
        self._bestObjVal = 0


    def build_graph(self, year):
        self._grafo.clear()
        if len(self._allteams) == 0:
            return

        self._grafo.add_nodes_from(self._allteams)

    #per collegare tutti i nodi con degli archi ci sono due modi
    # Modo Brutto:
        """for t in self._grafo.nodes:
            for t2 in self._grafo.nodes:
                if t!=t2 :
                    self._grafo.add_edge(t,t2)"""


    # Modo Bello: c'è una libreria chiamata itertools, nella quale c'è un metodo "combination"
        myedges = list(itertools.combinations(self._allteams, 2))  #lo metto in una lista perché combination mi
        # produce un iterable. così viene creata una lista di tuple, con nodo di partenza e nodo di arrivo che è
        # già utilizzabile con il metodo add_edges_from

        self._grafo.add_edges_from(myedges)


        #recupero i salari
        salariesOfTeams = DAO.getSalaryOfTeams(year, self._idMapTeams)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]


    def getSortedNeighbors(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))


        viciniTuple.sort(key=lambda x: x[1],reverse=True)
        return viciniTuple


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getALlYears(self):
        return DAO.getAllYears()

    def getPercorso(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]
        listaVicini = []
        for v in self._grafo.neighbors(v0):
            edgeV = self._grafo[v0][v]["weight"]
            listaVicini.append((v, edgeV))
        listaVicini.sort(key=lambda x: x[1], reverse=True)

        parziale.append(listaVicini[0][0])
        self._ricorsioneV2(parziale)
        parziale.pop()

        return self.getWeightsOfPath(self._bestPath)

    def _ricorsione(self, parziale):
        # verifico se sol attuale è migliore del best
        if self._getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._getScore(parziale)

        # verifico se posso aggiungere un altro elemeneto
        for v in self._grafo.neighbors(parziale[-1]):
            edgeW = self._grafo[parziale[-1]][v]["weight"]
            if (v not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] > edgeW):
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()
        #aggiungo e faccio ricorsione

    def _ricorsioneV2(self, parziale):
        # verifico se sol attuale è migliore del best
        if self._getScore(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._getScore(parziale)

        # verifico se posso aggiungere un altro elemeneto
        listaVicini = []
        for v in self._grafo.neighbors(parziale[-1]):

            edgeV = self._grafo[parziale[-1]][v]["weight"]
            listaVicini.append( (v, edgeV) )

        listaVicini.sort(key=lambda x: x[1], reverse=True)

        for v1 in listaVicini:
            if (v1[0] not in parziale and
                    self._grafo[parziale[-2]][parziale[-1]]["weight"] >
                    v1[1]):
                parziale.append(v1[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return
        #aggiungo e faccio ricorsione

    def _getScore(self, listOfNodes):

        if len(listOfNodes) == 1:
            return 0

        score = 0
        for i in range(0, len(listOfNodes)-1):
            score += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return score

    def getTeamsOfYear(self, anno):
        self._allteams = DAO.getTeamsOfYear(anno)
        self._idMapTeams ={t.ID : t for t in self._allteams}
        # questa è la forma compatta di :
        # for t in self._allTeams:
        #   self._idMapTeams[t.ID] = t
        return self._allteams


    def getWeightsOfPath(self, path):
        listTuples = [(path[0], 0)]
        for i in range(0, len(path)-1):
            listTuples.append((path[i+1], self._grafo[path[i]][path[i+1]]["weight"]))

        return listTuples


