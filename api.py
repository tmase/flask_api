from flask import Flask
from flask import request, jsonify
import os
import psycopg2


field_dict = {"cik":"cik","start_date":"periodofreport","end_date":"periodofreport"}
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return "<h1>Summary data API</h1>"
	
app.run()