from repo import store

class Centrality():
    def __init__(self,rows):
        self.graph = store.Graph()
    
        for datum in tuple(rows):
            for data in datum:
                if data['type'] == 'vertex':
                    if self.graph.getVertex(data['vid']) is None:
                        vertex = store.Vertex(data)
                        self.graph.setVertex(vertex.getGid(),vertex)
                else:
                    if self.graph.getEdge(data['eid']) is None:
                        edge = store.Edge(data)
                        self.graph.setEdge(edge.getGid(), edge)
            
        print('vertex >> ', self.graph.getVertices())
        print('edge >> ', self.graph.getEdges())
    
    def closeness_centrality(self,graph):
        # step 1. Vertex to Vertex Two-dimensional array
        for vertex in graph.getVertices():
            print(vertex.get())