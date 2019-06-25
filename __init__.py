import func
from repo import query_repo, db
from nmi import nmi

if __name__ == '__main__':
    qt = db.QueryTemplate()
    qr = query_repo.QueryRepo()
    
    qt.createConnectionPool(5, 20, "host=localhost port=15432 dbname=agens user=agens password=agens")
    qt.setGraphPath("tmp")

    print('####### start')
    
    datum = qt.doQuery('MATCH (a) RETURN a LIMIT 100')
    cluster = qt.doQuery(qr.getQueryString('algorithm.louvain_method_result'))
    
    print('####### analysis')
    
    ac = func.AnalysisClass(datum,cluster)
    print(ac.getSimilarClusterList())
    
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
    rightAnswer = qt.doQuery(qr.getQueryString('reading.rightanwser3'))
    print('NMI(louvain method) ', nmi.run(rightAnswer, cluster))
 
    cluster = qt.doQuery(qr.getQueryString('algorithm.girvan_newman_result'))
    print('NMI(girvan_newman) ', nmi.run(rightAnswer, cluster))
     
    cluster = qt.doQuery(qr.getQueryString('algorithm.infomap_result'))
    print('NMI(infomap) ', nmi.run(rightAnswer, cluster))
    
    print('####### end')
    qt.close()