import fileinput

keywords= ["programming","code","program","implementation","iterative",
           "method","answer","solution","technique","way","shown","below",
           "create","following","implements","algorithm","function",
           "implementations","example","demonstrate","class",":","source"
           ,"using","language","follows"]
print(keywords)

keys_query=[]
weight_count=[]
count=0
counter=0

query="bubble sort in java find"

for word in query.split(' '):
    print(word)
    keys_query.append(word)
    keywords.append(word)

print(keys_query)    

file = open('try.txt', 'r')
#count the number of lines in the file
for line in file.read().split('\n'):
    counter = counter + 1
    file.close()
no_of_lines=counter
print("no of lines total count")
print(no_of_lines)

file = open('try.txt', 'r')
#store all the text data in content    
content=file.readlines()
#turn everything in lower case
lower_content=[line.lower() for line in content]
#initialize the weight vector to zero
for i in range(no_of_lines):
    weight_count.insert(i,0)
    
#print(weight_count)
#print(lower_content)
#for word in keywords:
   # print(word)
print('before weight vector')    
for index,key in enumerate(lower_content):
    for word in keywords:
        if word in key:
            print(index)
            print(word)
            weight_count[index]+=1

    #print(index)
    #print(key)
max=0            
for i in weight_count:
    if weight_count[i] >max:
        max=weight_count[i]
        max_index=i
        
print(weight_count)
print(max_index)

