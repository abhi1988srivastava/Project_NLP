import fileinput
import re
import pickle

wt_vector_read={}
ignore=[' ','','\n','{','}','[',']',';','"',':','?','++','--','=','==','<=','!=','>=','(',')','//']
test_arrays=["c.p","c++.p"]
all_wts={}

file=open('c++.txt','r')
textfile=file.read()
total_weight=0
max=0
lang='t'

def ignore_word(w):
    flag=1
    for word in ignore:
            if word==w:
                flag=0
    if(flag):
        return 1
    else:
        return 0

#Finds the language with the highest value
def max_no(val,cur_lang):
    global max
    global lang
    if(val>max):
        lang=cur_lang
        max=val
        
        
#searches the word in a weight vector
def search(word):
    if word in wt_vector_read:
        return wt_vector_read[word]
    else:
        return 0
    
#calculates the total weight of the words from the program
def calc_wt():
    global total_weight
    total_weight=0
    for word in re.split(r'(\(|\)|\#|\"|\{|\}|\*|\n|\ |\.|\,|\=|\-;|\:)',textfile):
        if(ignore_word(word)):
            temp=search(word)
            total_weight+=temp
            #print(total_weight)
    return total_weight


#print(wt_vector_read['printk'])
#print(wt_vector_read['%d']


for i in range(len(test_arrays)):
    wt_vector_read=pickle.load(open(test_arrays[i],"rb"))
    all_wts[test_arrays[i]]=calc_wt()
    
    
for k,v in all_wts.items():
    max_no(v,k)
    #print(v)
    #print(k)

#print(max)
print('********************************************')
print(lang)
#wt_vector_read=pickle.load(open("c.p","rb"))            
#c=calc_wt()
#wt_vector_read=pickle.load(open("c++.p","rb"))
#cplus=calc_wt()

#print(all_wts[1])
#print(cplus)
