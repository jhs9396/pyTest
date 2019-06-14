import agensgraph as ag

class QueryTemplate():

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
