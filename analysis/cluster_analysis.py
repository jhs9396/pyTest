# -*- coding: utf-8 -*-
from repo import store
from util import file
from util.tool import to_list, to_time
from analysis.algorithm import community_detection as cd

class ClusterAnalysis():
    """
    initialize
    """
    def __init__(self, datum, cluster=None):
        # cluster based on search data 
        self.datum = datum
        self.cluster = cluster
        self.graph = store.Graph()
        self.clusterMapper = store.ClusterMapper(self.cluster)
        
        # networkx
        self.nx = store.NetworkX()
        self.community = cd.CommunityDetection(self.nx.getGraph())

        if self.cluster is not None:
            self.handleCluster()

    """
    cluster data가 존재하는 경우 vertex에 클러스터 ID를 setting
    """
    def handleCluster(self):
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
            valueArr = to_list(value)
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
        
    """
    step 1. In clusters, dtime distinct and counting : complete
    step 2. check clusters alive time : complete
    """
    def getDtimeStatistics(self,cluster,db=None):
        dtimeDict = dict()
        dtimeRangeDict = dict()

        for cluster_id,members in cluster:
            dtimeDict[cluster_id] = set()
            for vertex in list(filter(lambda x:x['cluster_id'] == cluster_id, [self.graph.getVertex(member).get() for member in to_list(members)])):
                dtimeDict[cluster_id].add(to_time(vertex['dtime']))
                
            dtimeRangeDict[cluster_id] = dict()
            dtimeRangeDict[cluster_id]['alive'] = (max(dtimeDict[cluster_id]) - min(dtimeDict[cluster_id])).days + 1
                
        for cluster_id,members in cluster:
            dtimeCntDict = dict()
            for vertex in list(filter(lambda x:x['cluster_id'] == cluster_id, [self.graph.getVertex(member).get() for member in to_list(members)])):
                for time in dtimeDict[cluster_id]:
                    if to_time(vertex['dtime']) == time:
                        if not dtimeCntDict.has_key(time):
                            dtimeCntDict[time] = 0
                        dtimeCntDict[time] += 1
                
            dtimeDict[cluster_id] = dtimeCntDict
        
        print('dtimeDict >> ', dtimeDict)
        print('dtimeRangeDict >> ', dtimeRangeDict)

    """
    step 3. get each cluster detection reason distinct : complete
    """
    def getDetectionReasonCluster(self,cluster):
        reasonDict = dict()
        
        for cluster_id, members in cluster:
            reasonDict[cluster_id] = set()
            for vertex in list(filter(lambda x:x['cluster_id'] == cluster_id, [self.graph.getVertex(member).get() for member in to_list(members)])):
                reasonDict[cluster_id].add(vertex['detection_reason'])
            
#         print(reasonDict)
        
    def getMaxMemberCluster(self,cluster):
        return reduce(lambda x,y: y if len(x) < len(y) else x, [(cluster_id, to_list(members)) for cluster_id, members in cluster])
        
    def exportCSV4ClusterNumber(self):
        header = list()
        results = list()
        idx = 0
        for cluster_id, members in self.cluster:
            for vertex in self.getClusterMember(cluster_id):
                result = list()
                for key in vertex.get():
                    if idx == 0: 
                        header.append(key)
                    result.append(vertex.get()[key])
                
                results.append(result)
                idx += 1
                
        file.writeCSV('result.csv', header, results)
                
    def runLouvainMethod(self, datum):
        self.nx.add_edges_from(datum)
        self.clusterMapper.setLouvainMethodCluster(self.community.louvain_method())
        self.nx.clear()
        
        return self.clusterMapper.louvainMethodCluster
        
    def runGirvanNewman(self, datum):
        self.nx.add_edges_from(datum)
        self.clusterMapper.setGirvanNewmanCluster(self.community.girvan_newman())
        self.nx.clear()
        
        return self.clusterMapper.girvanNewmanCluster
    
    