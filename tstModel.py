from model.model import Model

myModel = Model()
myModel.buildGraph('USA', 3)
nodes, edges = myModel.getGraphDetails()
print(len(nodes))
print(len(edges))

heaviest = myModel.getHeaviestEdges()
for u, v, data in heaviest:
    print(f"{u} --> {v}: {data['weight']}")

nodo = myModel.getMAxCompatibility()
print(f"{nodo[0]}: {nodo[1]}")

num, max = myModel.getCompConn()
print(f"Componenti connesse: {num}")
for c in max:
    print(c)

bestPath, bestValue = myModel.handlePath(16, 3)
print(f"\nCammino ottimo  di peso {bestValue}")
for i in range(len(bestPath)-1):
    n1 = bestPath[i]
    n2 = bestPath[i+1]
    print(f"{n1} --> {n2}: {myModel._graph[n1][n2]['weight']}")