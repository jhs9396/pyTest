# -*- coding: utf-8 -*-
import networkx

"""
Graph element (Vertices, Edges)를 관리하는 클래스
"""
class Graph():
    def __init__(self):
        self.vertices = dict()
        self.edges = dict()
        self.verticesKeys = set()
    
    def setVertex(self,vid,vertex):
        self.vertices[vid] = vertex
        for key in vertex.get().keys():
            self.verticesKeys.add(key)
        
    def setEdge(self,eid,edge):
        self.edges[eid] = edge
        
    def getVertex(self,vid):
        return self.vertices.get(vid)
    
    def getEdge(self,eid):
        return self.edges.get(eid)
    
    def getVertices(self):
        return self.vertices
    
    def vKeys(self):
        return self.verticesKeys
    
    def getEdges(self):
        return self.edges

"""
메모리 저장용 vertex 클래스 
"""
class Vertex():
    def __init__(self,v):
        self.id = None
        self.label = None
        self.properties = dict()
        self.setData(v[0])

    def setData(self,v):
        for key in v:
            self.id = v[key] if key is 'vid' else self.id
            self.label = v[key] if key is 'label' else self.label
            if key is not 'vid' and key is not 'label':
                self.properties[key] = v[key]
        
    def getData(self):
        return (self.id, self.label, self.properties)
    
    def getGid(self):
        return self.id
    
    def get(self):
        properties = self.properties
        if 'detection_reason' in properties: del properties['detection_reason']
#         if 'data_stream' in properties: del properties['data_stream']
#         if 'url' in properties: del properties['url']
        if 'type' in properties: del properties['type']
        if hasattr(self, 'cluster_id'):
            properties['cluster_id'] = self.cluster_id
        
        return properties
    
    def setClusterId(self,cluster_id):
        self.cluster_id = cluster_id
    
    def getClusterId(self):
        return self.cluster_id
    
    def compareData(self,datum):
        (vid, rule, location) = datum
        return True if self.id is vid and self.properties['rule'] is rule and self.properties['location'] is location else False
        

"""
클러스터 정보와 mapper정보를 담고있는 클래스
"""
class ClusterMapper():
    def __init__(self,cluster):
        self.cluster = cluster
        self.ruleMapper = dict()
        self.locMapper = dict()
        self.louvainMethodCluster = dict()
        self.girvanNewmanCluster = dict()
        self.infomapCluster = dict()
        
    def setClusterListByRule(self,vertices):
        for vertex in vertices.values():
            self.ruleMapper[vertex.properties['rule']] = set()
            
        for vertex in vertices.values():
            self.ruleMapper[vertex.properties['rule']].add(vertex.getClusterId())
        
    def setClusterListByLoc(self,vertices):
        for vertex in vertices.values():
            self.locMapper[vertex.properties['location']] = set()
            
        for vertex in vertices.values():
            self.locMapper[vertex.properties['location']].add(vertex.getClusterId())
        
    def getLocMapperItem(self,clusterId):
        loc = set()
        for key,cids in self.locMapper.iteritems():
            if clusterId in cids:
                loc.add(key)
        
        return loc
    
    def createNewCluster(self,clusterList):
        self.newCluster = clusterList
        
    def setLouvainMethodCluster(self,partition):
        cluster = 1
        for com in set(partition.values()):
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            self.louvainMethodCluster[cluster] = list_nodes 
            cluster += 1
    
    def setGirvanNewmanCluster(self,partition):
        cluster = 1
        for node_list in tuple(sorted(c) for c in next(partition)):
            self.girvanNewmanCluster[cluster] = node_list
            cluster += 1
    
class NetworkX():
    def __init__(self):
        self.G = networkx.Graph()
        
    def add_edges_from(self,datum):
        self.G.add_edges_from([tuple(d) for d in datum])
    
    def getGraph(self):
        return self.G
    
    def clear(self):
        self.__init__()
        
    