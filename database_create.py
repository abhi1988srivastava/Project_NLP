import sqlite3

conn=sqlite3.connect('example.db')
c=conn.cursor()

c.execute("create table code_tag1 (language text, code BLOB, tag text)")
#c.execute("select * from sqlite_master")
with open("max_frequent_java.txt","rb") as f:
    ablob=f.read()
    
c.execute("insert into code_tag1 values('java',?,'max frequent java')",[buffer(ablob)])
#print (c.fetchall())
conn.commit()
#row=c.execute("select * from code_tag1 where language='java' and tag like '%swap%'").fetchone()
#print (str(row[1]))
conn.close()
