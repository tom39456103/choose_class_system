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
        name = objects['name']
        price = objects['price']

        # insert data
        cursor.execute("INSERT INTO %s (name, price) VALUES (%s, %s)" % (table, name, price))

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

    cursor.execute("SELECT %s FROM %s WHERE %s" % (cols, table, cond))
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def drop_database():
    os.remove('CCSdatabase.db')
