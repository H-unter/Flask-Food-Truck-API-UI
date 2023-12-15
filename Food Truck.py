import requests
import json
import sqlite3
import os
import urllib3
import random
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import session

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #removal of warnings make testing clearner

#check if file truck.db exists
path = 'truck.db'
if os.path.isfile(path) == False:
  try:
    test=0
    poop="lol"
    db = sqlite3.connect('truck.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE fruck ( `truck_id` INTEGER, `name` TEXT, `category` TEXT, `bio` TEXT, `avatar_src` TEXT, `avatar_alt` TEXT, `avatar_title` TEXT, `cover_photo_src` TEXT, `cover_photo_alt` TEXT, `cover_photo_title` TEXT, `website` TEXT, `facebook_url` TEXT, `instagram_handle` TEXT, `twitter_handle` TEXT )")
    cursor.execute("CREATE TABLE reviews ( `review_id` INTEGER, `truck_id` INTEGER, `user_id` INTEGER, `review_rating1` INTEGER, `review_rating2` INTEGER, `review_rating3` INTEGER, `review_comment` TEXT )")
    insertreview = """INSERT INTO reviews (review_id, truck_id, user_id, review_rating1, review_rating2, review_rating3, review_comment)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(insertreview,(test, test, test, test, test, test, poop))
    db.commit()
  except Exception as error:
    db.rollback()
    print("!!!!!!!!!!!!!!! Something went wrong in the creation of the database: " + str(error))
  finally:
    db.close()
else: #This file does indeed exist, however the contents of the table must be removed to assure that it is as up to date as possible
  os.remove(path)
  try:
    db = sqlite3.connect('truck.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE fruck ( `truck_id` INTEGER, `name` TEXT, `category` TEXT, `bio` TEXT, `avatar_src` TEXT, `avatar_alt` TEXT, `avatar_title` TEXT, `cover_photo_src` TEXT, `cover_photo_alt` TEXT, `cover_photo_title` TEXT, `website` TEXT, `facebook_url` TEXT, `instagram_handle` TEXT, `twitter_handle` TEXT )")
    cursor.execute("CREATE TABLE reviews ( `review_id` INTEGER, `truck_id` INTEGER, `user_id` INTEGER, `review_rating1` INTEGER, `review_rating2` INTEGER, `review_rating3` INTEGER, `review_comment` TEXT )")
    cursor.execute("CREATE TABLE login ( `user_id` INTEGER, `truck_id` INTEGER, `username` TEXT, `password` TEXT )")
    #some initial test data must be inserted to allow for future code to work
    insertreview = '''INSERT INTO reviews (review_id, truck_id, user_id, review_rating1, review_rating2, review_rating3, review_comment)
                          VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(insertreview,(0,"null", "null", "null", "null", "null", "null"))
    insertlogin = '''INSERT INTO login (user_id, truck_id, username, password)
                          VALUES (?, ?, ?, ?)'''
    cursor.execute(insertlogin,(0,0, "test", "123"))
    db.commit()
  except Exception as error:
    db.rollback()
    print("!!!!!!!!!!!!!!! Something went wrong in the creation of the database: " + str(error))
  finally:
    db.close()

answer = requests.get("https://www.bnefoodtrucks.com.au/api/1/trucks", verify=False)
#convert to Python dictionary:
trucks = json.loads(answer.text)

#this assumes that a table is there witht he neccessary colums, as such, a new table will be created before this and it will be EMPTY woo

insertionSQLstring = '''INSERT INTO fruck (truck_id, name, category, bio, avatar_src, avatar_alt, avatar_title, cover_photo_src, cover_photo_alt, cover_photo_title, website, facebook_url, instagram_handle, twitter_handle)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

try:
  n=0
  for x in trucks:
    for y in x:
      #looping through truck_id, avatar, social media and all that stuff KEYS VALUES AND ALL
      db = sqlite3.connect('truck.db')
      cursor = db.cursor()
      #set up parameters for INSERT:
      if str(y) == "truck_id":##################
        truck_id = x[y]
        review_num = random.randint(3, 10)
        review_num = 1 #####DELETE THIS BEFORE THE THING
        z = 0
        while z < review_num:
          try:
            
            insertreview = '''INSERT INTO reviews (review_id, truck_id, user_id, review_rating1, review_rating2, review_rating3, review_comment)
                          VALUES (?, ?, ?, ?, ?, ?, ?)'''
            db2 = sqlite3.connect('truck.db')
            review_cursor = db2.cursor()
            review_id = review_cursor.execute("SELECT review_id FROM reviews ORDER BY review_id DESC").fetchone()
            review_id = int(review_id[0]) + 1
            
            truck_id = x[y]
            user_id = "bot"

            review_rating1 = random.randint(-1,1)
            review_rating2 = random.randint(-1,1)
            review_rating3 = random.randint(-1,1)
            
            sum_review = review_rating1+review_rating2+review_rating3
            if (sum_review/3) >= 0:
              review_comment = "my experience was positive overall"
            else:
              review_comment = "I believe there are better options out there to be honest"

            review_cursor.execute(insertreview,(review_id, truck_id, user_id, review_rating1, review_rating2, review_rating3, review_comment))
            db2.commit()
            
            z = z+1
          except Exception as error:
            db2.rollback()
            print(str(error))
            break
          finally:
            db2.close()
            
            

        
        
        
          
      elif str(y) == "name":
        name = x[y]
      elif str(y) == "category":
        category = x[y]
      elif str(y) == "bio":
        bio = x[y]
      elif str(y) == "avatar":
        for z in x[y]:
          if str(z) == "src":
            avatar_src = x[y][z]
          elif str(z) == "alt":
            avatar_alt = x[y][z]
          elif str(z) == "title":
            avatar_title = x[y][z]
      elif str(y) == "cover_photo": 
        for z in x[y]:
          if str(z) == "src":
            cover_photo_src = x[y][z]
          elif str(z) == "alt":
            cover_photo_alt = x[y][z]
          elif str(z) == "title":
            cover_photo_title = x[y][z] 
      elif str(y) == "website":
        if x[y] is None:
          website == "null"
        else:
          website = x[y]
        
      elif str(y) == "facebook_url":
        facebook_url= x[y]
      elif str(y) == "instagram_handle":
        instagram_handle = x[y]
      elif str(y) == "twitter_handle":
        twitter_handle= x[y] 
        cursor.execute(insertionSQLstring,(truck_id, name, category, bio, avatar_src, avatar_alt, avatar_title, cover_photo_src, cover_photo_alt, cover_photo_title, website, facebook_url, instagram_handle, twitter_handle))      
      db.commit()
except Exception as error:
  db.rollback()
  print( str(error))

finally:
  db.close()

print("SQL processes successful")




















logged = "false"
app = Flask(__name__)
app.secret_key = "session" #session variable for the website

@app.route("/")
def main():
  try:
      db = sqlite3.connect('truck.db')
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      database = cursor.execute("SELECT * FROM fruck").fetchall()
      categories = cursor.execute("SELECT DISTINCT category FROM fruck").fetchall()
      db.commit()
      print(logged)
  except Exception as error:
    db.rollback()
    print( str(error))
  finally:
    db.close()
  return render_template("index.html", database = database, categories = categories, login_status = logged)



@app.route("/awards")
def award():
  try:
      db = sqlite3.connect('truck.db')
      db.row_factory = sqlite3.Row
      cursor = db.cursor()

      eligible = cursor.execute("SELECT category from fruck GROUP BY category ORDER BY count(category) DESC LIMIT 5").fetchall()
      n=0
      for x in eligible:
        n=n+1
        print("Woo Hoo Number "+ str(n))
        if n == 1:
          cate1 = x[0]
          print(cate1)
        elif n == 2:
          cate2 = x[0]
          print(cate2)
        elif n == 3:
          cate3 = x[0]
          print(cate3)
        elif n == 4:
          cate4 = x[0]
          print(cate4)
        elif n == 5:
          cate5 = x[0]
          print(cate5)

      cat_1 = cursor.execute("SELECT * FROM fruck WHERE category ==?", (cate1,)).fetchall()
      cat_2 = cursor.execute("SELECT * FROM fruck WHERE category ==?", (cate2,)).fetchall()
      cat_3 = cursor.execute("SELECT * FROM fruck WHERE category ==?", (cate3,)).fetchall()
      cat_4 = cursor.execute("SELECT * FROM fruck WHERE category ==?", (cate4,)).fetchall()
      cat_5 = cursor.execute("SELECT * FROM fruck WHERE category ==?", (cate5,)).fetchall()
      


      db.commit()
      print(logged)
      print("Hello world")
      
    

  except Exception as error:
    db.rollback()
    print( str(error))
  finally:
    db.close()
    return render_template("awards.html", login_status = logged, cat1=cat_1, cat2=cat_2, cat3=cat_3, cat4=cat_4, cat5=cat_5)







@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/login-verify", methods=['GET', 'POST'])
def verify():
  try:

    u_input = request.form["username"]
    p_input = request.form["password"]

    db = sqlite3.connect('truck.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    login_SQL = cursor.execute("SELECT * FROM login").fetchall()
    db.commit()
    global logged
    for entry in login_SQL:
      if u_input == entry[2] and p_input == entry[3]:
        print("valid details entered")
        logged = "true"
        print(logged)
        return redirect("/") #joe
      else:
        return render_template("login.html")
    #####MAKE SURE THAT YOU CANT HAVE THE SAME USERNAME AS SOMEONE ESLE
    db.commit()
  except Exception as error:
    db.rollback()
    print( str(error))
  finally:
    db.close()


@app.route("/register")
def reg():
  return render_template("register.html")

@app.route("/register-verify", methods=['GET', 'POST'])
def regv():

  try:

    u_input = request.form["username"]
    p_input = request.form["password"]
    e_input = request.form["email"]
    print(e_input)
    if e_input.find('@')!=-1 and e_input.find('.')!=-1:
      print("valid email!")
      db = sqlite3.connect('truck.db')
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      
      insertlogin = '''INSERT INTO login (user_id, truck_id, username, password)
                        VALUES (?, ?, ?, ?)'''
      user_id = cursor.execute("SELECT user_id FROM login ORDER BY user_id DESC").fetchone()
      user_id = int(user_id[0]) + 1 
      cursor.execute(insertlogin,(user_id, "null", u_input, p_input))
      db.commit()
      global logged
      logged = "true"
      return redirect("/")

      
    else:
      print("invalid bitch")
      return render_template("register.html")
  except Exception as error:
    db.rollback()
    print( str(error))
  finally:
    db.close()
  return render_template("register.html")


@app.route("/filter/<category>")
def filter(category):
  try:
      db = sqlite3.connect('truck.db')
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      filtered = cursor.execute("SELECT * FROM fruck WHERE category == ?", (category,)).fetchall()
      categories = cursor.execute("SELECT DISTINCT category FROM fruck").fetchall()

  except Exception as error:
    db.rollback()
    print( str(error))
  finally:
    db.close()
  return render_template("index.html", database = filtered, categories = categories)


@app.route("/trucks/<truckID>")
def truckInfo(truckID):
  try:
    tid = truckID
    db = sqlite3.connect('truck.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    database = cursor.execute("SELECT * FROM fruck WHERE truck_id == ? ", (truckID,)).fetchall()
    review = cursor.execute("SELECT * FROM reviews WHERE truck_id == ? ", (truckID,)).fetchall()
    
  except Exception as error:
    db.rollback()
    print("!!!!!!!!!!!!!!! Something went wrong in def main thing sql game" + str(error))
  finally:
    db.close()
  return render_template("trucks.html", database = database, review = review, tid=tid, login_status = logged)


@app.route("/trucks/<truckID>/review_submit", methods=['GET', 'POST'])
def truckreview(truckID):
    truck_id = truckID
    user_id = "test"
    review_rating1 = request.form["radio1"]
    review_rating2 = request.form["radio2"]
    review_rating3 = request.form["radio3"]
    review_comment = request.form["comment"]
    try:

      db = sqlite3.connect('truck.db')
      db.row_factory = sqlite3.Row
      cursor = db.cursor()

      insertreview = '''INSERT INTO reviews (review_id, truck_id, user_id, review_rating1, review_rating2, review_rating3, review_comment)
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''
      review_id = cursor.execute("SELECT review_id FROM reviews ORDER BY review_id DESC").fetchone()
      review_id = int(review_id[0]) + 1 
      cursor.execute(insertreview,(review_id, truck_id, user_id, review_rating1, review_rating2, review_rating3, review_comment))

      db.commit()
    except Exception as error:
      db.rollback()
      print( str(error))
    finally:
      db.close()
    url = "/trucks/" + str(truckID)
    return redirect(url)

@app.route("/info")
def info():
  return render_template("info.html")





app.run(debug=True)