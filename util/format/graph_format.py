import re

def convertGraphObject(resultSet):
    _pattern = re.compile(r'(.+?)\[(.+?)\](.*)', re.S)
    for data in resultSet:
        print(data)
        try:
            m = _pattern.match(data[0])
            print(m.group(1),m.group(2),m.group(3)) 
        except Exception, e:
            print(data)