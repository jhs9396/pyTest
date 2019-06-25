from functools import reduce
import yaml

class QueryRepo():
    def __init__(self):
        with open('repo/query.yaml', 'r') as stream:
            try:
                self.queryRepo = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)
         
    def getQueryString(self,queryId):
        return reduce(lambda memo, key: memo[key], queryId.split('.'), self.queryRepo)
