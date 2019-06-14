import agensgraph as ag
from psycopg2 import pool

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
    
    def doQuery(self, qry):
        try:
            self.cursor.execute(qry)
            return self.cursor.fetchall()
        
        except Exception, e:
            print('error >> '+str(e))

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
