import math

def execute_origin(filePath,rs):
    f = open(filePath,'r')
    lines = f.readlines()
    #print(lines)
    i=0
    component=list()
    community=list()
    for line in lines:
        if i==0:
            i+=1
            continue
        Temp_community=line[3:len(line)-2]
        #print("Temp_community ",str(Temp_community))
        Temp_component=list()
        quotation_position1=[line.find("'", 0),line.find("'", line.find("'", 0)+1)]
        #print("quotation1 position ",str(quotation_position1))
        quotation_position2=[line.find("'", quotation_position1[1]+1),line.find("'", line.find("'", quotation_position1[1]+1)+1)]
        #print("quotation2 position ",str(quotation_position2))
        quotation_position=[quotation_position1,quotation_position2]
        #print("quotation position ", str(quotation_position))
        for j in range(2,int(Temp_community.count("'")/2)):
            quotation_position2=[line.find("'", quotation_position[j-1][1]+1),line.find("'",line.find("'", quotation_position[j-1][1]+1)+1)]
            quotation_position.append(quotation_position2)
        for j in range(0,len(quotation_position)):
            component.append(line[quotation_position[j][0]+1:quotation_position[j][1]])
            Temp_component.append(line[quotation_position[j][0]+1:quotation_position[j][1]])
        community.append([i,Temp_component])
        #print('community',community)
        i+=1

    f.close()
    i=0
    component2=list()
    community2=list()
    for cluster_id,nodes in tuple(rs):
        if i==0:
            i+=1
            continue
        for node in nodes:
            component2.append(node)
        
        community2.append([i,nodes])
        i+=1
    
    for i in range(len(component2)-1,-1,-1):
        for j in range(len(component)-1,-1,-1):
            if component2[i]==component[j]:
                break
            elif j==0:
                try:
                    community2.remove(component2[i])
                    del component2[i]
                except Exception, e:
                    #print('i', i, 'j', j, 'component2[i]',component2[i])
                    continue

    N = [[0 for cols in range(len(community2))]for rows in range(len(community))]
    for i in range(0,len(community)):
        for j in range(0,len(community2)):
            Tempcount=0
            for ii in range(0,len(community[i][1])):
                for jj in range(0,len(community2[j][1])):
                    if community[i][1][ii]==community2[j][1][jj]:
                        Tempcount+=1
                        break
            N[i][j]=Tempcount

    Ni=[0 for cols in range(len(community))]
    for i in range(0,len(Ni)):
        Ni[i]=sum(N[i][:])

    print('Ni', Ni)
    Nj=[0 for cols in range(len(community2))]
    
    for j in range(0,len(Nj)):
        for i in range(0,len(Ni)):
            try:
                Nj[j]+=N[i][j]
            except Exception, e:
                print('range over j',j)
        
    print('Nj ', Nj)
    numerator=0
    for i in range(0,len(Ni)):
        for j in range(0,len(Nj)):
            try:
                if N[i][j]==0:
                    continue
                numerator=numerator+(N[i][j])*math.log(float(N[i][j]*len(component))/(Ni[i]*Nj[j]))
            except ZeroDivisionError, e:
                print('Zero DivisionError : ', 'i',i,'j',j)

    denominator1=0
    for i in range(0,len(Ni)):
        if Ni[i]==0:
            continue
        denominator1=denominator1+Ni[i]*math.log(float(Ni[i])/len(component))

    denominator2=0
    for j in range(0,len(Nj)):
        if Nj[j]==0:
            continue
        denominator2=denominator2+Nj[j]*math.log(float(Nj[j])/len(component))

    NMI=(-2)*numerator/(denominator1+denominator2)
    print('NMI', NMI)


def run(rightAnswer, algorithmRslt):
    print('##### nmi run start ')
    ii = 0
    component=list()
    community=list()
    
    for cluster_id, nodes in tuple(rightAnswer):
        if ii==0:
            ii += 1
            continue
        
        for node in nodes:
            component.append(node)
            
        community.append([ii,nodes])
        ii += 1
    
    ii = 0    
    component2=list()
    community2=list()
    
    for cluster_id,nodes in tuple(algorithmRslt):
        if ii==0:
            ii+=1
            continue
        for node in nodes:
            component2.append(node)
         
        community2.append([ii,nodes])
        ii+=1
     
    for i in range(len(component2)-1,-1,-1):
        for j in range(len(component)-1,-1,-1):
            if component2[i]==component[j]:
                break
            elif j==0:
                try:
                    community2.remove(component2[i])
                    del component2[i]
                except Exception, e:
                    #print('i', i, 'j', j, 'component2[i]',component2[i])
                    continue

    N = [[0 for cols in range(len(community2))]for rows in range(len(community))]
    for i in range(0,len(community)):
        for j in range(0,len(community2)):
            cnt=0
            
#             print('community[i][1] >> ',community[i][1])
#             print('community2[j][1] >> ',community2[j][1])
            
            for value in community[i][1].replace('{','').replace('}','').split(','):
                for value2 in community2[j][1].replace('{','').replace('}','').split(','):
                    if value == value2:
                        cnt += 1
                        break
            
            N[i][j] = cnt
  
    Ni=[0 for cols in range(len(community))]
    for i in range(0,len(Ni)):
        Ni[i]=sum(N[i][:])
  
#     print('Ni', Ni)
    Nj=[0 for cols in range(len(community2))]
      
    for j in range(0,len(Nj)):
        for i in range(0,len(Ni)):
            try:
                Nj[j]+=N[i][j]
            except Exception, e:
                print('range over j',j)
          
#     print('Nj ', Nj)
    numerator=0
    for i in range(0,len(Ni)):
        for j in range(0,len(Nj)):
            try:
                if N[i][j]==0:
                    continue
                numerator=numerator+(N[i][j])*math.log(float(N[i][j]*len(component))/(Ni[i]*Nj[j]))
            except ZeroDivisionError, e:
                print('Zero DivisionError : ', 'i',i,'j',j)
  
    denominator1=0
    for i in range(0,len(Ni)):
        if Ni[i]==0:
            continue
        denominator1=denominator1+Ni[i]*math.log(float(Ni[i])/len(component))
  
    denominator2=0
    for j in range(0,len(Nj)):
        if Nj[j]==0:
            continue
        denominator2=denominator2+Nj[j]*math.log(float(Nj[j])/len(component))
  
    NMI=(-2)*numerator/(denominator1+denominator2)
#     print('NMI', NMI)
    
    return NMI
