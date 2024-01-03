import sqlite3
import json
import os

def create_table(name, vars):
    '''在資料庫裡面建一個表'''
    # open the data base
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    # create a table
    cursor.execute("CREATE TABLE IF NOT EXISTS %s(%s)" % (name, vars))

    # save
    conn.commit()
    conn.close()

def insert_file(file, table):
    '''把 json 轉成 SQL'''
    # read JSON
    with open(file) as f:
        data = json.load(f)
    
    # open the data base
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    for objects in data:
        Code = objects['Code']
        Category = objects['Category']
        Name = objects['Name']
        Credit = objects['Credit']
        Campus = objects['Campus']
        Instructor = objects['Instructor']
        val = (Code, Category, Name, Credit, Campus, Instructor)

        # insert data
        cursor.execute("INSERT INTO %s VALUES %s" % (table, val))

    # save
    conn.commit()
    conn.close()

def fetch_data(cols, table):
    '''找資料，回傳序列'''
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT %s FROM %s" % (cols, table))
    rows = cursor.fetchall()

    conn.close()
    return rows

def fetch_data(cols, table, cond):
    '''找資料，回傳序列'''
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT %s FROM %s %s" % (cols, table, cond))
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def drop_database():
    os.remove('CCSdatabase.db')

def drop_table(table):
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sqlite_sequence WHERE name = '%s'" % (table))
    cursor.execute("VACUUM")
    
    conn.commit()
    conn.close()
