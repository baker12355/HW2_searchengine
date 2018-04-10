
## Create table

![Alt text](https://github.com/baker12355/Searchengine/blob/master/Create_table.png)

# pseudo code

## start:

    1.create index[1000000]                                 #this index recoeds a mapping between words and numbers
        read source.csv line by line 
        fetch each line and cut by jieba, then get a str series: cut_list=str1,str2.. ,strn
        for each strk in cut_list
        define f_ord=ord(strk[0])                          #this meaning the index is decided by ascii code of the first character
        check whether the strk is in index[f_ord]          #example: str1:Apple . It should be index in index[65] cause 'A'=65 in ascii
        if strk is not in index[f_ord]:
           then add 'strk',(L)  into index[f_ord]          #L = the L-th line right now.
        else:
            append the line L into index[f_ord]= 'strk',(line1,line2..,L)

    2.query: p1 and p2 and p3
        query each p individually, and return the set of lines                      #exaple: p1->(1,3,7,15,...0) p2->(5,7,15,...)  
        do the set operating associate with p={p1,p2...}, and return the outpput    #exaple: (3,5,7) and (3,6,7)  = (3,7)

## end      

# Flowchart

![Alt text](https://github.com/baker12355/Searchengine/blob/master/temp.png "Optional title")


