import flask
from flask import request, jsonify
import pandas as pd
import psycopg2
from config import config

field_dict = {"cik":"cik","start_date":"periodofreport","end_date":"periodofreport"}

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
	return "<h1>Summary data API</h1>"
	
@app.route('/api/v1/resources/summary', methods=['GET'])
def api_filter():
	sql = "SELECT * FROM summary WHERE"
	query_parameters = request.args
	for param in query_parameters:
		val = query_parameters.get(param)
		field_name = field_dict[param]
		if param == 'start_date':
			sql += " " + field_name + ">=" + val + "AND "
		elif param == 'end_date':
			sql += " " + field_name + "<=" + val + "AND "
		else:
			sql += " " + field_name + "=" + val + "AND "
	sql = sql[:-4] + ';'
	
	#submit sql query to database
	conn = None
	params = config()
	conn = psycopg2.connect(**params)
	cur = conn.cursor()
	cur.execute(sql)
	results = cur.fetchall()
	
	return jsonify(results)
	
app.run()