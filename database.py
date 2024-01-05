import sqlite3
import json
import os
from class_spyder import *

def create_table(table_name, vars):
    '''在資料庫裡面建一個表'''
    # open the data base
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    # create a table
    cursor.execute("CREATE TABLE IF NOT EXISTS %s(%s)" % (table_name, vars))

    # save
    conn.commit()
    conn.close()

def insert_file(file, table_name, jsonFile = False):
    '''把檔案放到資料庫裡'''
    if jsonFile:
        # read JSON
        with open(file) as f:
            data = json.load(f)
    else:
        data = file
    
    # open the data base
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    for objects in data:
        Code = objects['Code']              # 課號
        Category = objects['Category']      # 類別
        Name = objects['Name']              # 課名
        Credit = objects['Credit']          # 學分
        Campus = objects['Campus']          # 校區
        Instructor = objects['Instructor']  # 老師/時間/教室
        Time = objects['Time']              # 時間
        val = (Code, Category, Name, Credit, Campus, Instructor, Time)

        # insert data
        cursor.execute("INSERT INTO %s VALUES %s" % (table_name, val))

    # save
    conn.commit()
    conn.close()
    print("file inserted.")

def fetch_data(table_name, cols, cond):
    '''找資料，回傳序列'''
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT %s FROM %s %s" % (cols, table_name, cond))
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def drop_database():
    os.remove('CCSdatabase.db')

def drop_table(table_name):
    conn = sqlite3.connect('CCSdatabase.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS %s" % (table_name))
    cursor.execute("VACUUM")
    
    conn.commit()
    conn.close()

def install_data(data, table_name: str, reinstall = False):
    if reinstall:
        drop_table('math')
        create_table(table_name, 
                    "\
                        Code        INT   PRIMARY KEY NOT NULL,\
                        Category    TEXT              NOT NULL,\
                        Name        TEXT              NOT NULL,\
                        Credit      REAL              NOT NULL,\
                        Campus      TEXT              NOT NULL,\
                        Instructor  TEXT              NOT NULL,\
                        Time        INT               NOT NULL")
        insert_file(eval(data), table_name)