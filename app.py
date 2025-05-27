
import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask import jsonify
import sqlite3
from routes import setup_routes


app = Flask(__name__)


app.config["Session_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
setup_routes(app)




if __name__ == "__main__":
    app.run(debug=True)
