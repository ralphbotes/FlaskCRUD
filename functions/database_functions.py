from functions.global_functions import clean
from flask import render_template, request, flash
import sqlite3
from datetime import datetime

def create_db():
    msg = []
    try:
        sqliteConnection = sqlite3.connect('SQLite_Drivers.db')
        msg.append("Database created and Successfully Connected to SQLite")
        cursor = sqliteConnection.cursor()

        #Check if table exists
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='database' ''')
        #if the count is 1, then table exists
        if cursor.fetchone()[0]==1 :
            msg.append("Drivers Table already exists")
        else: 
            cursor.execute("CREATE TABLE database (                                \
            id INTEGER PRIMARY KEY NOT NULL, name TEXT, surname TEXT,              \
            email TEXT UNIQUE, ethnicity TEXT, gender TEXT, addate timestamp);")

            msg.append("Table sqlite_drivers_db Created")

            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            msg.append(clean("SQLite Database Version is: " + str(record)))
            cursor.close()

    finally:
        sqliteConnection.close()

    return msg

def add_new():
    msg = []
    if request.method == 'POST':
      try:
         id = int(request.form['id'])
         name = str(request.form['name'])
         surname = str(request.form['surname'])
         email = str(request.form['email'])
         ethnicity = str(request.form['ethnicity'])
         gender = str(request.form['gender'])
         addate = datetime.strptime(str(request.form['date_added']), '%Y-%m-%d')

         sqliteConnection = sqlite3.connect('SQLite_Drivers.db')
         msg.append("Successfully Connected to SQLite")
         
         cursor = sqliteConnection.cursor()
         
         try:
            cursor.execute("INSERT INTO database (id,name,surname,email,ethnicity,gender,addate) VALUES (?,?,?,?,?,?,?)",(id,name,surname,email,ethnicity,gender,addate) )
            sqliteConnection.commit()
            msg.append("Values successfully added to Database")
         except:
             msg.append("ID or Email already exists!")
      
      except sqlite3.Error as error:
            msg.append("ERROR WHILE CONNECTING TO SQLITE")
    
    return msg

def list_db():
    sqliteConnection = sqlite3.connect('SQLite_Drivers.db')

    sqliteConnection.row_factory = sqlite3.Row
   
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM database ORDER BY addate DESC;")
   
    rows = cursor.fetchall(); 
    return rows

def user_selected(id):
    sqliteConnection = sqlite3.connect('SQLite_Drivers.db')

    sqliteConnection.row_factory = sqlite3.Row
   
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM database WHERE id=%s"%(id) )
   
    user = cursor.fetchall(); 
    return user

def delete_driver(id):
    sqliteConnection = sqlite3.connect('SQLite_Drivers.db')
    sqliteConnection.row_factory = sqlite3.Row
   
    cursor = sqliteConnection.cursor()
    cursor.execute("DELETE from database where id=%s"%(id))

    sqliteConnection.commit()
    sqliteConnection.close()

def update_driver():
    if request.method == 'POST':
      id = str(request.form['id'])
      name = str(request.form['name'])
      surname = str(request.form['surname'])
      email = str(request.form['email'])
      ethnicity = str(request.form['ethnicity'])
      gender = str(request.form['gender'])
         
      sqliteConnection = sqlite3.connect('SQLite_Drivers.db')
      sqliteConnection.row_factory = sqlite3.Row
      cursor = sqliteConnection.cursor()

      # Check if ethnicity changed
      cursor.execute("SELECT * FROM database WHERE id=%s"%(id) )
      eth_check = cursor.fetchall()

      for row in eth_check:
          id = row['id']
          # Check and set name
          if name != str(row['name']):
              sqliteConnection.execute("UPDATE database SET name = ? WHERE id=?",(name,id))
          
          # Check and set surname
          if surname != str(row['surname']):
              sqliteConnection.execute("UPDATE database SET surname = ? WHERE id=?",(surname,id))
          
          # Check and set email
          if email != str(row['email']):
              sqliteConnection.execute("UPDATE database SET email = ? WHERE id=?",(email,id))
          
          # Check and set ethnicity
          if ethnicity != str(row['ethnicity']):
              sqliteConnection.execute("UPDATE database SET ethnicity = ? WHERE id=?",(ethnicity,id))
          
          # Check and set 
          if gender != str(row['gender']):
              sqliteConnection.execute("UPDATE database SET gender = ? WHERE id=?",(gender,id))

            
      sqliteConnection.commit()
      sqliteConnection.close()