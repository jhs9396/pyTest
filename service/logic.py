def getSameClassIpList(iplist):
    requestArr = dict()
    idx = 1
    for ip in iplist:
        if idx == 1:
            idx += 1
        else: 
            try:
                requestArr[ip[0]] = []
                separate = ip[0].split('.')
                if len(separate) > 3:
                    cClass = separate[0]+'.'+separate[1]+'.'+separate[2]
                    for nm in range(1,256):
                        newIp = cClass+'.'+str(nm)
                        requestArr[ip[0]].append(newIp)
                        
            except Exception, e:
                print(e)
        
    return requestArr 

        
        
    
    
    
    