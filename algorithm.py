import community
from networkx.algorithms.community.centrality import girvan_newman

class CommunityDetection():
    def __init__(self,G):
        self.G = G
        
    def louvain_method(self):
        return community.best_partition(self.G)
        
    def girvan_newman(self):
        return girvan_newman(self.G)
        
    