import os
from flask import Flask
from flask import Response, request, g
import mysql.connector as sql
import sys
import json

app = Flask(__name__)


@app.before_request
def before_request():
    g.cnx = sql.connect(
            host       =os.environ['MYSQL_IP'],
            port       =os.environ['MYSQL_PORT'],
            user       =os.environ['MYSQL_USER'],
            password   =os.environ['MYSQL_PASSWORD'],
            database   ="myapi-stories"
            )

@app.teardown_request
def teardown_request(exception):
    g.cnx.close()
  

@app.route("/health")
def health():
    resp = Response('{ "message" : "Service running. Python version: ' + sys.version + '"}')
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route("/story", methods=['GET', 'POST', 'DELETE'])
def story():
    if request.method == 'GET':
        cursor = g.cnx.cursor()
        cursor.execute(f"SELECT ID, story, Project FROM stories where Project={request.args['project']} AND Evaluated=0 LIMIT 1")
        results= []
        for (story_id, story_info, story_project) in cursor:
            results.append({"id":story_id, "info":story_info, "project": story_project})
        response = app.response_class(
            response=json.dumps(results),
            status=200,
            mimetype='application/json'
            )
        return response
    if request.method == 'POST':
        cursor = g.cnx.cursor()
        cursor.execute(f"INSERT INTO stories (info, project) VALUES ('{request.args['info']}','{request.args['project']}')")
        g.cnx.commit()
        response = app.response_class(
            response=json.dumps({"msg":f"Saved {request.args['info']}"}),
            status=200,
            mimetype='application/json'
            )
        return response
    if request.method == 'DELETE':
        cursor = g.cnx.cursor()
        cursor.execute(f"DELETE FROM stories WHERE id = \"{request.args['id']}\"")
        g.cnx.commit()
        response = app.response_class(
            response=json.dumps({"msg":"Deleted", "count": f"{cursor.rowcount}"}),
            status=200,
            mimetype='application/json'
            )
        return response