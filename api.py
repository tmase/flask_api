import flask
from flask import request, jsonify
import psycopg2


field_dict = {"cik":"cik","start_date":"periodofreport","end_date":"periodofreport"}
app = flask.Flask(__name__)

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
	DATABASE_URL = 'postgres://xguecwohsbjfdz:dcbaf4d0b37bf4f3a508cd044a7a56c7c6ef8c9d32b3668b4ac408b43bf6f086@ec2-23-21-91-183.compute-1.amazonaws.com:5432/d4lfl5vii49uqk'
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	cur.execute(sql)
	results = cur.fetchall()
	
	return jsonify(results)
	
app.run()