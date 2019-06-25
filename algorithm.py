from repo import store
import community

class CommunityDetection():
    def __init__(self):
        self.G = store.NetworkX().getGraph()
    