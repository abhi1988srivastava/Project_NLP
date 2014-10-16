import nltk
import re
import time
from nltk import pos_tag, word_tokenize
import urllib2
import urllib
import json
import nltk   
from urllib import urlopen
import os
import os
import subprocess


index=0
j=0
count=0
startIndex=[]
endIndex=[]
urlList={}
keywords= ["programming","code","program","implementation","iterative",
           "method","answer","solution","technique","way","shown","below",
           "create","following","implements","algorithm","function",
           "implementations","example","demonstrate","class",":","source"
           ,"using","language","follows","this","version","versions","(",")","main","public","main"]

keys_query=[]
weight_count=[]
#count=0
counter=0
max_index=0
lower_content=[]
max=0
url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"
f1=open("Output_R.txt","w")
output=[]

exampleArray="i want to sort array in java using bubble sort"
#exampleArray="fibonacci series code recursion"



def break_query():
    query=exampleArray
    global keywords
    for word in query.split(' '):
        keys_query.append(word)
        keywords.append(word)
    '''rand=open("rand.txt","w+")
    for key in keywords:
        rand.write(key+'\n')'''


#count the number of lines in the file
def count_lines():
    file = open('output_R.txt', 'r')
    global no_of_lines
    global counter
    for line in file.read().split('\n'):
        counter = counter + 1
        file.close()
    no_of_lines=counter
    print("counter:",counter)
    file.close()
    

def init_data():
    file = open('output_R.txt', 'r')
    global lower_content
    global no_of_lines
    #store all the text data in content    
    content=file.readlines()
    #turn everything in lower case
    lower_content=[line.lower() for line in content]
    #initialize the weight vector to zero
    for i in range(no_of_lines):
        weight_count.insert(i,0)
    

def program_detector():
    global weight_count
    global lower_content
    global keywords
    for index,key in enumerate(lower_content):
        for word in keywords:
            if word in key:
                #print(index)
                #print(word)
                weight_count[index]+=1

    #print(weight_count)       
    

def get_max():
    max=0
    global weight_count
    global max_index
    for i in range(len(weight_count)):
        if weight_count[i] >=max:
            max=weight_count[i]
            #print(max)
            #print(i)
            max_index=i
    print(max_index)
    
def extract_just_code(f2,temp):
    global index
    global max_index
    output=""
    break_query()
    count_lines()
    init_data()
    program_detector()
    get_max()
    
    index=max_index
    print(max_index)
    lnum=0
    count=0
    #copy=False
    f2=open("Output_R.txt","r")
    content=f2.readlines()
    lines=[line.lower() for line in content]
    
    for line in lines:
        #print ("------"+line)
        lnum+=1
        if lnum>=index:
            '''if '{' in line.strip():
            #print (index1)
            copy=True
            elif '}' in line.strip():
            copy=False
            elif ccopy:
            print (line)
            '''
            if '{' in line:
                count+=1
                startIndex.append(lnum)
            elif '}' in line:
                count-=1
                endIndex.append(lnum)

    #print ("STARTING")
    #print (startIndex)
    start=startIndex[0]
    end=endIndex[len(endIndex)-1]-1
    lnumm=0
    for line in lines:
        lnumm+=1
        if lnumm>=start and lnumm<=end+1:
            #print (line)
            output+=line
        

        
        
    #print (index,"--",item)
    
    #print  (output)
    output_file=open(str(temp),"w")
    output_file.write(output)
    output_file.close()
    

tokenized = nltk.word_tokenize(exampleArray)
tokenized=[x.lower() for x in tokenized]
x=pos_tag(tokenized)
#print (x)

dicti=dict((word,tag) for (word,tag) in x)

for key in dicti:
    if dicti[key].startswith("NN") or dicti[key].startswith("JJ"):
        output.append(key)
        
#print (dicti)
#print (output)

y=" ".join(output)

query = urllib.urlencode( {'q' : y } )

response = urllib2.urlopen (url + query ).read()

data = json.loads ( response )
results = data [ 'responseData' ] [ 'results' ]

for result in results:
    url=result['url']
    title=result['title']
    #print ("-->"+url)
    if "stack" in url or "Stack" in url or "ranch" in url:
        continue
    else:
        #print ("yes")
        urlList[title]=url


#print (urlList)
temp=1
for key in urlList:
    j=0
    
    f1=open("Output_R.txt","w")
    f=open("Output.txt","w")
    
    url=urlList[key]
    html=urlopen(url).read()
    raw=nltk.clean_html(html)
    #print ("=======RAW=======")
    #print (raw)
    f.write(raw)
    f.close()
    f=open("Output.txt","r")
    content=f.readlines()

    new_contents=[]
    for line in content:
        if not line.strip():
            continue
        else:
            new_contents.append(line)

    z="".join(new_contents)
    #print (z)
    f1.write(z)
    f1.close()
    print(temp)
    extract_just_code(f1,temp);
    temp=temp+1
    #print(weight_count)
      
    
