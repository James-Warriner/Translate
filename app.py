

from flask import Flask
from flask_session import Session

from datetime import datetime, timedelta
from flask import jsonify
import sqlite3
from routes import setup_routes



app = Flask(__name__)


app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


setup_routes(app)





if __name__ == "__main__":
    app.run(debug=True)
