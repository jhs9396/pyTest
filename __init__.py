import db
import func

if __name__ == '__main__':
    q = db.QueryTemplate()
#     q.createConnection("host=localhost port=5432 dbname=agens user=agens password=agens")
    q.createConnectionPool(5,20,"host=localhost port=5432 dbname=agens user=agens password=agens")
    q.setGraphPath("tmp")
    print('####### start')
    
    datum = q.doQuery('MATCH (a) RETURN a')
    cluster = q.doQuery('SELECT cluster_id, nodes FROM public.louvain_method_result')
    
    print('####### analysis')
    ac = func.AnalysisClass(datum,cluster)
    print(ac.getSimilarClusterList())
    
    print('####### end')
    q.close()