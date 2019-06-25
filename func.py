# -*- coding: utf-8 -*-
from repo import store

class AnalysisClass():
    """
    initialize
    """
    def __init__(self, datum, cluster):
        self.datum = datum
        self.cluster = cluster
        self.graph = store.Graph()
        self.clusterMapper = store.ClusterMapper(self.cluster)
        
        for data in tuple(self.datum):
            vertex = store.Vertex(data)
            (vid, label, properties) = vertex.getData()
            
            vertex.setClusterId(self.getClusterIdByVid(vid))
            self.graph.setVertex(vid,vertex)
    
    """
        클러스터에 속한 vertex들을 반환한다.
    """
    def getClusterMember(self,clusterId):
        return list(filter(lambda x : x.getClusterId() == clusterId, self.graph.getVertices().values()))
    
    """
    vertex의 클러스터 번호를 반환한다.
    """
    def getClusterIdByVid(self, vid):
        clusterId = ''
        for key, value in self.cluster:
            valueArr = value.replace('{','').replace('}','').split(',')
            if vid in valueArr:
                clusterId = key
        
        return clusterId

    """
    rule 기반 클러스터와 location 기반 클러스터를 비교검산하여 새로은 클러스터 리스트를 반환한다.
    """
    def getSimilarClusterList(self):
        vertices = self.graph.getVertices()
        self.clusterMapper.setClusterListByRule(vertices)
        self.clusterMapper.setClusterListByLoc(vertices)
        
        print('ruleMapper >> '+str(self.clusterMapper.ruleMapper))
        print('locationMapper >> '+str(self.clusterMapper.locMapper))
        
        # new cluster list dictionary
        clusterList = dict()
        # new cluster number
        idx = 1
        
        # new cluster 생성 시작 
        for cids in self.clusterMapper.ruleMapper.values():
            locDict = dict()
            locCntDict = dict()
            
            # rule이 같은 cluster 번호마다 location을 조회하여 딕셔너리 생성
            for cid in cids:
                locDict[cid] = self.clusterMapper.getLocMapperItem(cid) 

            # 만들어진 location 딕셔너리를 비교하여 같은 location이면 값 증가
            for key,value in locDict.items():
                for v in value:
                    if not locCntDict.has_key(v):
                        locCntDict[v] = 1
                    else:
                        locCntDict[v] += 1
                
            # location 딕셔너리에서 위에서 체크된 location count 수를 비교하여 2 이상인 지역정보를 조회하고, 같은 지역인 클러스터 번호를 분류
            for key, value in locDict.items():
                for v in value:
                    for key1,value1 in list(filter(lambda item: item[:][1] > 1, locCntDict.items())):
                        if not clusterList.has_key(idx):
                            clusterList[idx] = set()

                        if v == key1:
                            clusterList[idx].add(key)
            
            if clusterList.has_key(idx):
                idx += 1
        
        # new cluster 생성 끝
        self.clusterMapper.createNewCluster(clusterList)
        
        return clusterList
        
    