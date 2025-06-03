from flask import session, redirect, url_for, render_template,jsonify,request
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import returnError
from queries import execute_query,selectID,loginQuery
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



import datetime

def login_required(route_function):
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return redirect(url_for("login"))  
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__  
    return wrapper


def isLoggedIn():
    if session.get("user_id"):
        return True
    else:
        return False
    
def hasSession():
    if session.get("temp_id"):
        return True
    else:
        return False

import datetime
import random

def generate_id():
    now = datetime.datetime.now()

    a = now.day
    b = now.month
    c = now.year

    x = 3
    y = 2
    d = 0

    if a % 2 == 0:
        for ch in str(a):
            d += int(ch) * x
    else:
        for ch in str(b):
            d += int(ch) * y

    random_part = random.randint(100, 999) 
    return f"{c}{b:02d}{a:02d}-{d}-{random_part}"

    
def assignTemp():
  if isLoggedIn():
    return
  elif hasSession():
      return
  else:
    session["temp_id"] = generate_id()


def validEmail(text):
   if "@" not in text:
      return False
   if "." not in text:
      return False
   if text.index(".") < text.index("@"):
      return False
   if not text[text.index(".")+1].isalpha():
      return False
   
   return True

GLOBAL_PASSWORD_LEN = 8
GLOBAL_PASSWORD_CHARS = "!£$%^&*()-+"

def validPassword(password):
  specialChars = GLOBAL_PASSWORD_CHARS
  if len(password) < GLOBAL_PASSWORD_LEN:
    return False
  count = 0
  for char in specialChars:
    if char in password:
      count +=1
  if count<2:
     return False
  
  return True


def sendCode(email,first_name, last_name,password):
  code = random.randint(1000,9999)
  load_dotenv()
  loginEmail = os.getenv("APPLE_EMAIL")
  senderEmail = loginEmail
  smtp_password = os.getenv("APPLE_PASSWORD")
  recipientEmail = email
  print(loginEmail)
  print(password)

  msg = MIMEMultipart()
  msg["From"] = senderEmail
  msg["To"] = recipientEmail
  msg["Subject"] = "Verify your email - Translator"
  message = f"""Hi, {first_name}
  
  Enter the following code to authenticate your account:
  
   {code} """
  
  msg.attach(MIMEText(message))

  mailserver = smtplib.SMTP('smtp.mail.me.com',587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login(loginEmail,smtp_password)
  mailserver.sendmail(senderEmail,recipientEmail,msg.as_string())

  mailserver.quit()

  session["auth_code"] = code
  session["first_name"] = first_name
  session["last_name"] = last_name
  session["email"] = email
  session["password"] = password


       
   
   
   

def register(request):
  if isLoggedIn():
    session["user_id"] = False
  
  if request.method == "GET":
    return render_template("register.html")
  else:
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not first_name:
       return returnError("Missing first name")
    
    if not last_name:
       return returnError("Missing last name")
    
    if not email:
       return returnError("Missing email")
    if not validEmail(email):
       return returnError("Invalid email")
    
    if not password:
       return returnError("Missing password")
    
    if not validPassword(password):
      return returnError(f"Password must be {GLOBAL_PASSWORD_LEN} character long and include two special characters: {GLOBAL_PASSWORD_CHARS} ")
    
    return jsonify({"auth":"true","email":email,"first_name":first_name,"password":password,"last_name":last_name})
    
    
    
def authenticateCode(request):
  print(request.method)
  

  if request.method == "POST":
      
    if request.is_json:
      email = request.get_json().get("email")
      first_name = request.get_json().get("first_name")
      last_name = request.get_json().get("first_name")
      password = request.get_json().get("password")
      sendCode(email,first_name, last_name,password)
      print(jsonify({"status":"sent"}),200)
      return jsonify({"status":"sent"}),200
    else:
      print("HERE")
      code = request.form.get("code")

      if code == str(session["auth_code"]):

        hash_pw = generate_password_hash(session["password"])
        print(hash_pw)
        
        query = """
        INSERT INTO user (first_name, last_name, email, password_hash) VALUES (?,?,?,?)"""
        res = execute_query(query, (session["first_name"],session["last_name"],session["email"],hash_pw))
        if res:
          return res
        
       
        
        
        
        
        session["auth_code"] = False
        session["first_name"] = False
        session["last_name"] = False
        session["email"] = False
        session["password"] = False
        if str(res).isnumeric():
          session["user_id"] = res

        else:
          return returnError("Server error"),500
        session["auth_code"] = False
        return redirect("/")
  
  elif request.method == "GET":
     print("true")
     return "GET"

     
  

def login(request):
  if request.method == "GET":
      return render_template("login.html")
  else:
     email = request.form.get("email")
     print(email)
     password = request.form.get("password")
     result = loginQuery(email,password)
     print(result)
     if result:
        print("TRUE")
        return jsonify({"status":"success"}),200
     else:
        return returnError("Incorrect credentials")



    

   
   

   

    



    
    
