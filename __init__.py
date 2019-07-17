from analysis import cluster_analysis as c_analyis
from analysis.algorithm import centrality
from repo import query_repo, db
from nmi import nmi
from service import logic
from request import missinglink

if __name__ == '__main__':
    qt = db.QueryTemplate()
    qr = query_repo.QueryRepo()
    
    qt.createConnectionPool(5, 20, "host=192.168.0.68 port=5555 dbname=agens user=agens password=agens")
    qt.setGraphPath("movie_graph")
    print('####### initialize')
#     qt.doQuery(qr.getQueryString('creation.vertex.hackthekisa'))
    
    print('####### developer area')
    datum = qt.doQuery('MATCH (a)-[r]->(b) RETURN a,r,b')
    cent = centrality.Centrality(datum)
    
    print('####### start')
#     datum = qt.doQuery('SELECT * FROM pg_stat_activity LIMIT 5')
#     datum = qt.doQuery('MATCH path=(a)-[r]->(b) RETURN path LIMIT 2')        

#     cluster = qt.doQuery(qr.getQueryString('algorithm.louvain_method_result'))
#     cluster = qt.doQuery(qr.getQueryString('reading.rightanwser3'))
#     cluster = qt.doQuery(qr.getQueryString('reading.rightanwser4'))

    
    print('####### clustering function execute')
#     datum = qt.doQuery(qr.getQueryString('reading.node2node'))
#     ca = c_analyis.ClusterAnalysis(datum)

#     print(ca.runLouvainMethod(datum))
#     print(ca.runGirvanNewman(datum))
    
    print('####### analysis')
#     ca = c_analyis.ClusterAnalysis(datum,cluster)

#     print(ca.getSimilarClusterList())
#     ca.exportCSV4ClusterNumber()
    
    print('####### get cluster info')
#     ca.getDtimeStatistics(cluster)
#     ca.getDetectionReasonCluster(cluster)
#     
#     print(ca.getMaxMemberCluster(cluster))
    
    print('####### create edges based on ip')    
    q = db.Query(qt)
#     q.createEdgeByIp('creation.edge.ref_to', qt.doQuery(qr.getQueryString('reading.iplist')))
#     q.createEdgeByIp('creation.edge.similar_to', qt.doQuery(qr.getQueryString('reading.iplist')))

    print('####### clustering nmi ')
    """
    cluster members : Number of nodes: 17270, Number of edges: 17341
    # louvain method ('NMI', 0.9912852877125228)
    # louvain method include similar ('NMI', 0.9715911871342564)
    # clustering timing : 8s
    
    # girvan_newman ('NMI', 0.9897133027297328)
    # girvan_newman include similar ('NMI', 0.9703506027348707)
    # clustering timing : 600s
    
    # infomap ('NMI', 0.9949571112604476)
    # infomap include similar ('NMI', 0.9754626710222238)
    # clustering timing : 10s
    """
    
    # ref_to result
#     rightAnswer = qt.doQuery(qr.getQueryString('reading.rightanwser'))
    
    # similar to result 
#     rightAnswer = qt.doQuery(qr.getQueryString('reading.rightanwser2'))
    
    # Not exists edge, vertex to vertex and include rightanswer1~2
#     rightAnswer = qt.doQuery(qr.getQueryString('reading.rightanwser3'))
#     print('NMI(louvain method) ', nmi.run(rightAnswer, cluster))
#  
#     cluster = qt.doQuery(qr.getQueryString('algorithm.girvan_newman_result'))
#     print('NMI(girvan_newman) ', nmi.run(rightAnswer, cluster))
#      
#     cluster = qt.doQuery(qr.getQueryString('algorithm.infomap_result'))
#     print('NMI(infomap) ', nmi.run(rightAnswer, cluster))

    print('####### missinglink')
#     iplist = qt.doQuery(qr.getQueryString('reading.ip4oneNode'))
#     requestList = logic.getSameClassIpList(iplist)
#     for ip in requestList:
#         missinglink.missinglink_sample(requestList[ip])
    
    print('####### TF-IDF')
#     ca.insertClusterTfIdf(qt=qt, qr=qr)
    
    
    print('####### end')
    qt.close()