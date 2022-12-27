from flask import Flask
from os import listdir, path
from quix.quix import QuixSql


app = Flask(__name__)

@app.route("/en")
def en_txt():
  return QuixSql().generate_fragment()
  

