import fileinput
import re
import pickle
import os

language_name=["c"]

file=open('datac++.txt','r')

textfile=file.read()
weight_vector={}
keywords=[]
count=0
total_wt=0
new_count=0

ignore=[' ','','\n','{','}','[',']',';','"',':','?','++','--','=','==','<=','!=','>=','(',')','//']
wt_vector_read={}


def search(word):
    global count
    count+=1
    if word in weight_vector:
        return 1
    else:
        return 0

def ignore_word(w):
    flag=1
    for word in ignore:
            if word==w:
                flag=0
    if(flag):
        return 1
    else:
        return 0

for word in re.split(r'(\(|\)|\#|\"|\{|\}|\*|\n|\ |\.|\,|\=|\-;|\:)',textfile):
    #print (word)
    #count+=1
    if(ignore_word(word)):
        keywords.append(word)
        if(search(word)):
            weight_vector[word]+=1
        else:
            weight_vector[word]=1

for k,v in weight_vector.items():
    weight_vector[k]=weight_vector[k]/count
    total_wt+=weight_vector[k]
    

pickle.dump(weight_vector, open("c++.p","wb"))
print(count)
print(total_wt)
