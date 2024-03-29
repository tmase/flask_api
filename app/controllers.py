from app import app
import os
import psycopg2
from flask import request, jsonify

field_dict = {"cik":"cik","start_date":"periodofreport","end_date":"periodofreport"}

@app.route('/')
@app.route('/index')
def index():
	return "Welcome to the Summary Data API"

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
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	cur.execute(sql)
	results = cur.fetchall()
	return jsonify(results)