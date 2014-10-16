#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui
import re, math
from collections import Counter
from nltk.corpus import stopwords
import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import nltk
import re
import time
import nltk.tag, nltk.data
import sqlite3
import sys
from nltk.corpus import stopwords
import nltk
from nltk.corpus import brown
from nltk.corpus import wordnet as wn

'''class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(self)
        self.button = QtGui.QPushButton('Get Code')
        self.edit = QtGui.QTextEdit()
        self.ans= QtGui.QTextEdit()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layout.addWidget(self.ans)
        self.button.clicked.connect(self.handleTest)

    def handleTest(self):
        self.ans.append('spam: spam spam spam spam')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
'''



conn=sqlite3.connect('example.db')
c=conn.cursor()

#c.execute("select * from employees where name='merge'")
#c.execute(
#print (c.fetchall())
#row=c.execute("SELECT *  FROM code_tag1 where language='python' and tag='bubblesort'").fetchone()
#print (str(row[1]))
stop = stopwords.words('english')

conn.commit()
#conn.close()

#exampleArray ='I want to sort numbers using bubblesort in php and java and python'
from1="from"
where="where"
equal="="
verbs=[]
pronoun=[]
where=[]
string=""
#result=[]
WORD = re.compile(r'\w+')


#to handle cosine similarity

def get_cosine(vec1, vec2):
     #print (vec1)
     #print (vec2)
     intersection = set(vec1.keys()) & set(vec2.keys())
     #print (intersection)
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     #print (words)
     return Counter(words)
    

def processingLanguage(exampleArray):
    result=[]
    dicti={}
    useful=[]
    final_exampleArray=""
    exampleArray_list=[]

    #print (exampleArray)

    for i in exampleArray.split(" "):
         print (i)
         for synset in wn.synsets(i):
              for lemma in synset.lemmas:
                   #print lemma.name,
                   exampleArray_list.append(lemma.name)
         for synset in wn.synsets(i):
              for hypernym in synset.hypernyms():
                   for ss in hypernym.lemmas:
                        #print ss.name,
                        exampleArray_list.append(ss.name)

    final_exampleArray=" ".join(exampleArray_list)

    

    try:
        #print ("inside processingLanguage")
        larr= [i for i in final_exampleArray.lower().split() if i not in stop]
        #print (larr)
        x=nltk.pos_tag(larr) #tagged sentences with pos_tag
        #print (x)
        
        
        '''default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
        model={'select':'VB','show':'VB','get':'VB','fetch':'VB','bring':'VB', 'print' : 'VB', 'display':'VB'}
        tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)
        x=tagger.tag(tokenized)
        '''
        '''for item in x:
            print (item)
            for m in item:
                print (m)'''
        dicti=dict((word,tag) for (word,tag) in x)
        #print (dicti)
        for key in dicti:
            #print ("key-->"+key)
            if dicti[key].startswith("VB"):
                useful.append(key)
            if dicti[key].startswith("NN") or key.startswith("PDT") or key.startswith("DT") :
                #print ("val--->"+dicti[key])
                useful.append(key)
            if dicti[key].startswith("RB"):
                where.append(dicti[key])
            
        #noun = [word.replace("all",'\\*') for word in noun]
        #ind=noun.index('all')
        #noun[ind]='*'
        #print (ind)

        
        print (useful)
        for i in useful:
            for j in useful:
                #print ("i-->"+i+" and j-->"+j)
                try:
                    if i==j:
                         pass
                    else:
                         #print ("j :",j)
                         row=c.execute("SELECT *  FROM code_tag1 where language=? and tag like ?",(i,'%'+j+'%')).fetchone()
                         #print ('SELECT '+i+' FROM '+j)
                         #print (str(row[1]))
                         #print ("----------------------------------------------------------------------------------")
                         result.append(str(row[1]))
                except:
                    pass
            
        #except:
        #    pass
        #except sqlite3.Error as e:
            #print ("error occured: ",e.args[0])
        #print (dicti)
        #print (verbs)
        #print (noun)
        #print (where)
    except:
        #print ("in error :", e)
        #sys.exc_clear()
        pass
    dicti.clear()

    return result


def handleTest1():
        a1Edit.clear()
        #print ("inside handle")
        #print (edit.toPlainText())
        res=processingLanguage(str(q1Edit.toPlainText()))
        string="".join(res)
        a1Edit.append(string)
        res=[]

def handleTest2():
        a2Edit.clear()
        #print ("inside handle")
        #print (edit.toPlainText())
        res=processingLanguage(str(q2Edit.toPlainText()))
        string="".join(res)
        a2Edit.append(string)
        res=[]

def handleTest3():

    text1=q1Edit.toPlainText()
    text2=q2Edit.toPlainText()
    #print (text1)
    
    vector1=text_to_vector(text1)
    vector2=text_to_vector(text2)
    cosine=get_cosine(vector1,vector2)
    string=""
    if cosine >=0.8 :
        string="Both the queries are very similar"
    elif cosine >=0.5 and cosine<0.8:
        string="Both the queries are quite similar"
    elif cosine<0.5:
        string="Both the queries are different" 
    print (cosine)
    QtGui.QMessageBox.about(w,"Paraphrase Info",string)
        

app = QtGui.QApplication(sys.argv)
w=QtGui.QWidget()
w.resize(800,600)
w.move(300,300)
w.setWindowTitle('Code Extractor')
queryLabel1 = QtGui.QLabel('Enter Query')
queryLabel2 = QtGui.QLabel('Enter Query')

codeLabel1 = QtGui.QLabel('Code')
codeLabel2 = QtGui.QLabel('Code')

button1 = QtGui.QPushButton('Get Code')
button2 = QtGui.QPushButton('Get Code')
button3 = QtGui.QPushButton('is similar to?')
button3.setGeometry(0,0,30,30)

q1Edit = QtGui.QTextEdit()
q2Edit = QtGui.QTextEdit()

a1Edit = QtGui.QTextEdit()
a2Edit = QtGui.QTextEdit()


grid = QtGui.QGridLayout()
grid.setSpacing(10)

grid.addWidget(queryLabel1, 1, 0)
grid.addWidget(queryLabel2, 1, 2)

grid.addWidget(q1Edit, 2, 0)
grid.addWidget(q2Edit, 2, 2)
grid.addWidget(button3,2,1)

grid.addWidget(button1, 3, 0)
grid.addWidget(button2, 3, 2)



grid.addWidget(codeLabel1, 4, 0)
grid.addWidget(codeLabel2, 4, 2)

grid.addWidget(a1Edit, 5, 0)
grid.addWidget(a2Edit, 5, 2)
        
w.setLayout(grid)
button1.clicked.connect(handleTest1)
button2.clicked.connect(handleTest2)
button3.clicked.connect(handleTest3)
        
#w.setGeometry(300, 300, 350, 300)
#w.setWindowTitle('Review')    
w.show()
sys.exit(app.exec_())
