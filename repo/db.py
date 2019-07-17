import agensgraph as ag
# import psycopg2 as pg
from psycopg2 import pool
import query_repo as qr
from util.format import graph_format

"""
postgresql connection driver template
create connection pool
set graph path
execute method
"""
class QueryTemplate():

    def createConnectionPool(self, minConnection, maxConnection, info):
        self.pool = pool.SimpleConnectionPool(minConnection, maxConnection, info)
        self.conn = self.pool.getconn()
        self.cursor = self.conn.cursor()
        
    def createConnection(self, info):
        self.conn = ag.connect(info)
        self.cursor = self.conn.cursor()
        
    def setGraphPath(self, path):
        self.cursor.execute("SET GRAPH_PATH TO "+path)
    
    def doQuery(self, qry, params=None):
        try: 
            if params is not None:
                self.cursor.execute(qry, params)
            else:
                self.cursor.execute(qry)

            records = self.cursor.fetchall()
            
#             graph_format.convertGraphObject(records)
        
            return records
        except Exception, e:
            e

        finally:
            self.conn.commit()
    
    def close(self):
        self.conn.close()
        self.cursor.close()
        if self.pool is not None:
            self.pool.closeall()
        
#     def poolPutConn(self):
#         try:
#             self.pool(self.conn)
#         except Exception, e:
#             print('error >> '+str(e))

class Query():
    def __init__(self, qt):
        self.qt = qt
        self.qr = qr.QueryRepo()
    
    def createEdgeByIp(self, queryPath, ipList):
        query = self.qr.getQueryString(queryPath)
                   
        for ip in tuple(ipList):
            self.qt.doQuery(query, {'source_ip':ip})

    def getVertex(self, gid):
        return self.qt.doQuery(self.qr.getQueryString('reading.vertex'), {'id':gid})
        
        
        