import csv
import numpy as np
import pandas as pd 
import jieba
import math





def loaddata(file):
    df=[]
    with open(file, mode='r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            df.append(row)
    return df

def get_position(index,n,j):
    if index[n]==[]:
        return False, None
    for i in range(len(index[n])):
        if index[n][i][0]== j :
            return True,i
        else:
            continue
    return False, None


def cut(strr):
    cut_=list()
    for i in range(len(strr)-1):
        cut_.append(strr[i]+strr[i+1])
    for i in range(len(strr)-2):
        cut_.append(strr[i]+strr[i+1]+strr[i+2])
    return cut_

def createengine(data):
    index=[list() for i in range (50000)]
    for i in range(len(data)):
        seg=jieba.cut_for_search(data[i][1])
        for j in seg:
            n=int(ord(j[0]))
            if n>=65 and n<=122 and len(j)>=2:
                aisin,pos=get_position(index,n,j)
                if (aisin):
                    st=index[n][pos][0]
                    ori=index[n][pos][1]
                    index[n][pos]= ( st , ori+','+str(i+1))
                else:
                    tp=(j,str(i+1))
                    index[n].append(tp)
                    
            elif (len(j)>=2) &(len(j)<=3)  :
                aisin,pos=get_position(index,n,j)
                if (aisin):
                    st=index[n][pos][0]
                    ori=index[n][pos][1]
                    index[n][pos]= ( st , ori+','+str(i+1))
                else:
                    tp=(j,str(i+1))
                    index[n].append(tp)
    return index


def query_for_one(index,q):
    asc=int(ord(q[0]))
    _,pos=get_position(index,asc,q)
    if pos!=None:
        return index[asc][pos][1]
    else:
        return None


def query_combine(index,q):
    query_=q.split(' ')
    qa=qo=0
    qa= query_[1]=='and'
    qo= query_[1]=='or'
    qn= query_[1]=='not'
    qry_s=['0' for i in range(math.ceil(len(query_)/2)) ]
    for i in range(math.ceil(len(query_)/2)):
        qry_s[i]=query_[i*2]
    qry_a=['0' for i in range(math.ceil(len(query_)/2))]
    for i in range(len(qry_a)):
        qry_a[i]=query_for_one(index,qry_s[i])
        if qry_a[i] != None: 
            qry_a[i]= set(int(i) for i in qry_a[i].split(','))
        else : qry_a[i]=set()

    ans=set()
    if qa:
        ans=qry_a[0]
        for i in range(len(qry_a)):
            ans=ans&qry_a[i]
    elif qo:
        for i in range(len(qry_a)):
            ans=ans|qry_a[i]
    elif qn:
        for i in range(len(qry_a)):
            ans=ans-qry_a[i]
    ans=sorted(ans)
    return ans



file='source.csv'
df=loaddata(file)
table=createengine(df)
a=query_for_one(table,'MLB')

qr=loaddata('query.txt')
ans=query_combine(table,qr[2][0])


















