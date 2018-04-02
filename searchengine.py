import csv
import jieba
import math

def loaddata(file):                     #load data
    df=[]
    with open(file, mode='r',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            df.append(row)
    return df


def get_position(index,n,j,line):      #確認字串是否已在table中有索引
    if index[n]==[]:
        return False, None
    for i in range(len(index[n])):     #若存在則回傳位置
        if (index[n][i][0]== j)& (str(line) not in index[n][i][1].split(',')) :
            return True,i
        else:
            continue
    return False, None


#def cut(strr):                       #暴力破解法切割字串
#    cut_=list()
#    for i in range(len(strr)-1):
#        cut_.append(strr[i]+strr[i+1])
#    for i in range(len(strr)-2):
#        cut_.append(strr[i]+strr[i+1]+strr[i+2])
#    return cut_

#def exist(index,n,j,i):              #確認索引中是否已存在
#    for i in range(len(index[n])):
#        if (index[n][i][0]==j):
#            if str(i) in index[n][i][1].split(','):
#                return False
#        return True


def createengine(data):                                     #建立索引表
    index=[list() for i in range (50000)]
    for i in range(len(data)):
        seg=jieba.cut_for_search(data[i][1])                #以jeiba搜尋引擎法斷詞
        for j in seg:
            n=int(ord(j[0]))                                #以ascii為索引入口
            if n>=65 and n<=122 and len(j)>=2:              #若開頭為英文字,則考慮加入索引
                aisin,pos=get_position(index,n,j,i+1)
                if (aisin):                                 #若已存在索引則加入新的列數即可
                    st=index[n][pos][0]                     #如 ('MLB',(3,5,9,13...))
                    ori=index[n][pos][1]
                    index[n][pos]= ( st , ori+','+str(i+1))
                else:                                       
                    tp=(j,str(i+1))                         #若不存在索引則加入新索引
                    index[n].append(tp)                     #如 ascii==50處 ->  append--('MLB',(5))   

            elif (len(j)>=2) &(len(j)<=3)  :                #若開頭為中文字,則考慮加入索引
                aisin,pos=get_position(index,n,j,i+1)       #加入法如上
                if (aisin):
                    st=index[n][pos][0]
                    ori=index[n][pos][1]
                    index[n][pos]= ( st , ori+','+str(i+1))
                else:
                    tp=(j,str(i+1))
                    index[n].append(tp)
    print ('table have been created')
    return index


def query_for_one(index,q):             #一次只查詢一筆資料
    asc=int(ord(q[0]))                  #輸入為"查表格" & 'MLB' 
    _,pos=get_position(index,asc,q,0)   #回傳值為(1,3,5,7...)
    if pos!=None:
        return index[asc][pos][1]
    else:
        return None


def query_combine(index,q):             #一次查詢n筆集合互動
    query_=q.split(' ')
    qa=qo=0
    qa= query_[1]=='and'                #紀錄 and or not
    qo= query_[1]=='or'
    qn= query_[1]=='not'
    qry_s=['0' for i in range(math.ceil(len(query_)/2)) ]   #qry_s為查詢字串集合
    for i in range(math.ceil(len(query_)/2)):
        qry_s[i]=query_[i*2]
    qry_a=['0' for i in range(math.ceil(len(query_)/2))]
    for i in range(len(qry_a)):
        qry_a[i]=query_for_one(index,qry_s[i])
        if qry_a[i] != None: 
            qry_a[i]= set(int(i) for i in qry_a[i].split(','))
        else : qry_a[i]=set()
    ans=set()                           #將各個查詢結果已集合的方式運算
    if qa:                              # set
        ans=qry_a[0]
        for i in range(len(qry_a)):
            ans=ans&qry_a[i]
    elif qo:
        for i in range(len(qry_a)):
            ans=ans|qry_a[i]
    elif qn:
        for i in range(len(qry_a)):
            ans=ans-qry_a[i]
    ans=sorted(ans)                     #sorting
    return ans


def storeoutput(index):                 #儲存結果
    qr=loaddata('query.txt')
    with open('output.txt', 'a') as f:
        for i in qr:
            for j in i:
                ans=query_combine(table,j)
                ans=[str(i) for i in ans]
                if ans== []:
                    f.write('0\n')
                else:
                    f.write(','.join(ans)+'\n')





jieba.set_dictionary('dict.txt.big')   #繁體中文字典
file='source.csv'
df=loaddata(file)                      #load titles
table=createengine(df)                 #ceate search engine
storeoutput(table)                     #store results


















