# -*- coding: utf-8 -*-


import sys

file1 = open(sys.argv[1], "r")
file2 = open(sys.argv[2], "w+")
file3 = open(sys.argv[3], "r")


#Saving the corpus documents in list:
data={}
lines = [line.strip() for line in file1]
data = [line.split('\t') for line in lines]

#Inverted-Index Dictionary:
inverted_index = {}
count={}
for DocID, Sentence in data:
    for word in Sentence.split(" "):
        count[word]=count.get(word,0)+1
        if inverted_index.get(word,False):
            if DocID not in inverted_index[word]:
                inverted_index[word].append(DocID)
        else:
                inverted_index[word] = [DocID]


#DocID-Sentence Dictionary for TF-IDF Calculation:
document={}
for DocID,Sentence in data:      
    document[DocID]=Sentence



for line in file3.readlines():                                 
    query=line.strip()
    postingList=[]
    keysList = []
    query_length=0
    #Postings List
    for word in (query.split(" ")):
        query_length=query_length+1
        if(word in inverted_index):
          file2.write("GetPostings\n")
          file2.write(word+"\n")
          file2.write("Postings list: ")
          for doc_id in inverted_index.get(word):
              file2.write(str(doc_id)+" ")
          postingList.append(inverted_index.get(word))
          keysList.append(word)
        file2.write("\n") 

    #DAAT-And                    
    comparisions_AND=0
    minPosting=0;  
    list_and1=[]
    minimum=len(postingList[0]); 
    
    for min in range(1,len(postingList)):
        if(minimum>len(postingList[min])):
            minimum=len(postingList[min])
            minPosting=min
            
    list_and1.append(postingList[minPosting])

    postingList_Dup=postingList.copy()
    postingList_Dup.pop(minPosting)
    
    final_AndList=[]
    temp=0;
    for k in range(len(list_and1[0])):
        count_and=1;
        for l in range(len(postingList_Dup)):
            flag=0;
            for m in range(temp,len(postingList_Dup[l])):
                comparisions_AND=comparisions_AND+1
                if(list_and1[0][k]==postingList_Dup[l][m]):
                    count_and=count_and+1
                    break;
                elif(list_and1[0][k]<postingList_Dup[l][m]):
                    temp=m
                    flag=1
                    break;
            if(flag==1):
                break;
        if(count_and==query_length):
            final_AndList.append(list_and1[0][k])   
    
    file2.write("DaatAnd\n")
    file2.write(query+"\n")
    file2.write("Results: ")           
    if(len(final_AndList)==0):
            file2.write("empty")
    else:
        for r in final_AndList:
            file2.write(r+" ")
    file2.write("\n")
    file2.write("Number of documents in results: "+str(len(final_AndList))+"\n")
    file2.write("Number of comparisions: "+str(comparisions_AND)+"\n") 
    
    #TF-IDF-AND
    tfidf_and={}
    for id in final_AndList:
        tfidf_all=0
        for key in keysList:
            terms_doc=[]
            count_and=0
            terms_doc.append(document.get(id).split(" "))
            if(any(key in sublist for sublist in terms_doc)):
                count_and=count_and+1
            tf= (count_and)/len(terms_doc[0])
            idf=len(data)/len(inverted_index[key])
            tf_idf=tf*idf
            tfidf_all=tfidf_all+tf_idf
        tfidf_and[id]=tfidf_all
    sorted_dict = sorted(tfidf_and.items(), key=lambda item: item[1], reverse=True)
    
    file2.write("TF-IDF\n")
    file2.write("Results: ")
    if(len(sorted_dict)==0):
        file2.write("empty")
    else:
        for t in range(len(sorted_dict)):
            file2.write(str(sorted_dict[t][0])+" ")
    file2.write("\n")
    
    
    #DAAT-Or
    comparisions_OR=0
    list_or1=[]
        
    for k in range(len(postingList)):
            for l in postingList[k]:
                    list_or1.append(l)
    list_or1=sorted(list_or1)        
    
    
    final_Orlist=[]
    for term in list_or1:
        comparisions_OR=comparisions_OR+1
        if term not in final_Orlist:
            final_Orlist.append(term)  
     
    file2.write("DaatOr\n")
    file2.write(query+"\n")
    file2.write("Results: ")           
    if(len(final_Orlist)==0):
            file2.write("empty")
    else:
        for r in final_Orlist:
            file2.write(r+" ")
    file2.write("\n")
    file2.write("Number of documents in results: "+str(len(final_Orlist))+"\n")
    file2.write("Number of comparisions: "+str(comparisions_OR)+"\n")
    
    #TF-IDF-OR
    tfidf_or={}
    for id in final_Orlist:
        tfidf_all=0
        for key in keysList:
            terms_doc=[]
            count_and=0
            terms_doc.append(document.get(id).split(" "))
            if(any(key in sublist for sublist in terms_doc)):
                count_and=count_and+1
            tf= (count_and)/len(terms_doc[0])
            idf=len(data)/len(inverted_index[key])
            tf_idf=tf*idf
            tfidf_all=tfidf_all+tf_idf
        tfidf_or[id]=tfidf_all
    sorted_dict = sorted(tfidf_or.items(), key=lambda item: item[1], reverse=True)
    
    file2.write("TF-IDF\n")
    file2.write("Results: ")
    if(len(sorted_dict)==0):
        file2.write("empty")
    else:
        for t in range(len(sorted_dict)):
            file2.write(str(sorted_dict[t][0])+" ")
    file2.write("\n")
    file2.write("\n")
    

file1.close() 
file2.close() 
file3.close()