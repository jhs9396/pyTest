import community
from networkx.algorithms.community.centrality import girvan_newman

"""
clustering algorithm execute class
"""
class CommunityDetection():
    def __init__(self,G):
        self.G = G
    
    """
    execute louvain
    dependency by store.py by networkx
    """
    def louvain_method(self):
        return community.best_partition(self.G)
        
    """
    execute girvan newman
    dependency by store.py networkx
    """
    def girvan_newman(self):
        return girvan_newman(self.G)
        
    