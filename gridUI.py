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

import re, math
from collections import Counter
from nltk.corpus import stopwords
from sys import float_info as fi
from collections import defaultdict
from math import sqrt, log
from decimal import *
import nltk
import re
import time
import nltk.tag, nltk.data
import sqlite3
import sys
from nltk.corpus import stopwords
from collections import Counter
from nltk.corpus import stopwords
from sys import float_info as fi
from collections import defaultdict
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
def getAllWords(text):
     exampleArray_list=[]
     for i in text.split(" "):
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
     return final_exampleArray

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

        '''for i in noun:
            if i in "all":
                print ("yes")
                string="select * from"
        '''


        '''
        #print (noun)
        for i in noun:
            #print ("i :",i)
            for j in noun:
                try:
                    #print ("j :",j)
                    c.execute('SELECT *  FROM employees where name = '+j)
                    #print ('SELECT '+i+' FROM '+j)
                    print (c.fetchall())
                except:
                    pass
                    
        '''
        
        for i in useful:
            for j in useful:
                
                try:
                    if i==j:
                         pass
                    else:
                         #print ("j :",j)
                         row=c.execute("SELECT *  FROM code_tag1 where language=? and tag like ?",(i,'%'+j+'%')).fetchone()
                         #print ('SELECT '+i+' FROM '+j)
                         
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

        
def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator



#http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Dice's_coefficient
""" duplicate bigrams in a word should be counted distinctly
(per discussion), otherwise 'AA' and 'AAAA' would have a 
dice coefficient of 1...
"""
def dice_coefficient(a,b):
    if not len(a) or not len(b): return 0.0
    """ quick case for true duplicates """
    if a == b: return 1.0
    """ if a != b, and a or b are single chars, then they can't possibly match """
    if len(a) == 1 or len(b) == 1: return 0.0
 
    """ use python list comprehension, preferred over list.append() """
    a_bigram_list = [a[i:i+2] for i in range(len(a)-1)]
    b_bigram_list = [b[i:i+2] for i in range(len(b)-1)]
 
    a_bigram_list.sort()
    b_bigram_list.sort()
 
    # assignments to save function calls
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)
    # initialize match counters
    matches = i = j = 0
    while (i < lena and j < lenb):
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1
 
    score = float(matches)/float(lena + lenb)
    return score


def jenshannon(x,y):
    
    # get the words that occur in either x or y
    s = set(x.keys()) | set(y.keys())
    x = defaultdict(float,x)
    y = defaultdict(float,y)
    def H(xcount, ycount):
        h = 0.
        if xcount:
            h += xcount*log(2.*xcount/(xcount+ycount))
        if ycount:
            h+= ycount*log(2.*ycount/(xcount+ycount))
        return h
    return Decimal(1./(fi.epsilon + float(sum([H(float(x[word]),float(y[word])) for word in s]))))


def handleTest3():
    text1=q1Edit.toPlainText()
    text2=q2Edit.toPlainText()
    #print (text1)
    text1=str(text1)
    text2=str(text2)
    new_text1=getAllWords(text1)
    new_text2=getAllWords(text2)
    
    vector1=text_to_vector(new_text1)
    vector2=text_to_vector(new_text2)
    cosine=get_cosine(vector1,vector2)
    string=""
    if cosine >= 0.5 : 
        string="Yuhoooo..Texts are quite similar..."
    else:
        string="Whooopss..texts are quite different" 
    print (cosine)
    QtGui.QMessageBox.about(w,"Paraphrase Info",string)
    

def handleTest4():
    text1=q1Edit.toPlainText()
    text2=q2Edit.toPlainText()
    #print (text1)
    
    text1=str(text1)
    text2=str(text2)
    new_text1=getAllWords(text1)
    new_text2=getAllWords(text2)
    
    dice=dice_coefficient(new_text1,new_text2)
    string=""
    if dice >= 0.5 :
        string="Yuhoooo..Texts are quite similar"
    else:
        string="Whooopss..texts are quite different" 
    print (dice)
    QtGui.QMessageBox.about(w,"Paraphrase Info",string)


def handleTest5():
    text1=q1Edit.toPlainText()
    text2=q2Edit.toPlainText()
    #print (text1)
    text1=str(text1)
    text2=str(text2)
    
    new_text1=getAllWords(text1)
    new_text2=getAllWords(text2)
    vector1=text_to_vector(new_text1)
    vector2=text_to_vector(new_text2)
    
    jens=jenshannon(vector1,vector2)
    string=""
    if jens >= 0.5 :
        string="Yuhoooo..Texts are quite similar..."
    else:
        string="Whooopss..texts are quite different" 
    print (jens)
    QtGui.QMessageBox.about(w,"Paraphrase Info",string)



app = QtGui.QApplication(sys.argv)
w=QtGui.QWidget()
w.resize(800,600)
w.move(300,300)
w.setWindowTitle('Code Extractor')
queryLabel1 = QtGui.QLabel('Enter Query')
queryLabel2 = QtGui.QLabel('Enter Query')
matchQuery= QtGui.QLabel('Click Below For Similarity')
font=QtGui.QFont()
font.setUnderline(False)
font.setBold(True)
font.setPointSize(10)
matchQuery.setFont(font)
queryLabel1.setFont(font)
queryLabel2.setFont(font)

codeLabel1 = QtGui.QLabel('Code')
codeLabel2 = QtGui.QLabel('Code')
codeLabel1.setFont(font)
codeLabel2.setFont(font)

button1 = QtGui.QPushButton('Get Code')
button2 = QtGui.QPushButton('Get Code')
button3 = QtGui.QPushButton('Cosine Similarity')
button4 = QtGui.QPushButton('Dice ')
button5 = QtGui.QPushButton('Jensen Shannon')

button1.setFont(font)
button2.setFont(font)
button3.setFont(font)
button4.setFont(font)
button5.setFont(font)

#button3.setGeometry(0,0,30,30)

q1Edit = QtGui.QTextEdit()
q2Edit = QtGui.QTextEdit()

a1Edit = QtGui.QTextEdit()
a2Edit = QtGui.QTextEdit()


grid = QtGui.QGridLayout()
vbox = QtGui.QVBoxLayout()
grid.setSpacing(10)

grid.addWidget(queryLabel1, 1, 0)
grid.addWidget(matchQuery, 1, 1)
grid.addWidget(queryLabel2, 1, 2)

grid.addWidget(q1Edit, 2, 0)
grid.addWidget(q2Edit, 2, 2)

vbox.addWidget(button3)

vbox.addWidget(button4)
vbox.addWidget(button5)
grid.addLayout(vbox,2,1)

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
button4.clicked.connect(handleTest4)
button5.clicked.connect(handleTest5)

#w.setGeometry(300, 300, 350, 300)
#w.setWindowTitle('Review')    
w.show()
sys.exit(app.exec_())
