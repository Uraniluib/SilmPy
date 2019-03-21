# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 05:24:07 2019

@author: xingg
"""

import sqlite3
from sqlite3 import Error
from os import listdir
from os.path import isfile, join
from collections import defaultdict
 
def main(conn,attribute):
        
    #if "a" == "a":
        cur = conn.cursor()
        
        # read all attribute files
        mypath = '../CleanData/attribute'
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        rows = [] # [(i['col1'], i['col2']) for i in dr]
        
        # open article data --node
        file = open('../CleanData/article.csv','r', encoding = 'utf-8')
        articles = {}
        for c in file.readlines():
            c = (c.replace('\n','').replace('_',' ')).split('\t')
            articles[c[0]] = c[1]
        file.close()

        
        #print('41')
        for f in files:
            onerow = []
            anum = f.split('_')[0]
            onerow.append(int(anum)) # add id
            onerow.append(articles[anum].lower())
            
            file = open(join(mypath, f), 'r', encoding = 'utf-8')    
            lines = file.readlines()
            file.close()
            
            # get all value
            defdesc = []
            '''
            # Larger example
            rows = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                    ('2006-04-05', 'BUY', 'MSOFT', 1000, 72.00),
                    ('2006-04-06', 'SELL', 'IBM', 500, 53.00)]
            c.executemany('insert into stocks values (?,?,?,?,?)', rows)
            connection.commit()
            '''
            
            for l in lines:
                tempkv = (l.replace('\n','')).split('\t') 
                if tempkv[0] == 'to':
                    tempkv[0] = 'to_'
                if tempkv[0] == 'group':
                    tempkv[0] = 'group1'
                attr = ''.join([i for i in tempkv[0].lower() if not i.isdigit()]).replace('-','_').replace("references","ref")
                if attribute.lower() in attr.lower() and tempkv[1] in articles.keys():
                    defdesc.append(articles[tempkv[1]])
            for d in defdesc:
                #onerow.append(d) # create a row
            
                # add one row to rows
                rows.append(tuple(onerow+[d]))
                
        print(attribute)
        #print(rows)
        # add rows to db
        cur.executemany(('insert into '+attribute+' values (?,?,?)').replace('"','""'), list(set(rows)))
        


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
            
    except Error as e:
        print(e)
    
    return None
 
if __name__ == '__main__':
    database = "../CleanData/article_attribute_9.db"
    
    file = open('../CleanData/attribute.csv','r', encoding = 'utf-8')
    temp = set()
    for c in file.readlines():
        c = c.replace('\n','').split('\t')
        if c[0] == 'to':
           c[0] = 'to_'
        word = ''.join([i for i in c[0] if not i.isdigit()]).replace('-','_').replace("references","ref").replace('group','group1')
        if not word.isupper(): #not all upper case
            temp.add(word) #remove number
    file.close()
        
    allAttribute = list(temp)
    allAttribute.sort()
    
    conn = create_connection(database)
    #conn.execute("PRAGMA busy_timeout = 300000")
    
    for a in allAttribute:
        a = a.lower()
        sql_create_projects_table = ' CREATE TABLE IF NOT EXISTS ' +a+ ' (id int NOT NULL, name varchar(50) NOT NULL, ' + a + ' varchar(50) NOT NULL, PRIMARY KEY (id,name,'+a.lower()+'));'
        
        
        if conn is not None:
            # create projects table
            #print(sql_create_projects_table)
            create_table(conn, sql_create_projects_table)
            main(conn,a)

    conn.commit()    