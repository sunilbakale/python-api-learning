import sqlite3
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
import textwrap
import os
import sys

app = Flask(__name__)
api = Api(app)

# Code Snippet Example
code_snippet = """ 
def factorial(num): 
    fact=1 
    for i in range(1,num+1): 
        fact = fact*i 
    return fact 
code = factorial(5)
print(code)
"""


# To Save the Record in DB
class SaveSnippetCode(Resource):
    def post(self):
        data = request.get_json()

        conn = sqlite3.connect('python_code_snippet_db.db')

        query = '''CREATE TABLE IF NOT EXISTS CODE_SNIPPET
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        NAME           TEXT    NOT NULL, 	
                        CODE         VARCHAR NOT NULL)'''

        conn.execute(query)

        query = "INSERT INTO CODE_SNIPPET (NAME,CODE) VALUES (?, ?)"
        argument = (data['code_title'], data['code_snippet'])

        conn.execute(query, argument)
        conn.commit()

        cursor = conn.execute("SELECT id from CODE_SNIPPET")
        conn.commit()

        id_ = len(cursor.fetchall())

        unique_id = {'snippet_id': id_}

        return unique_id


# To Get all the Records from DB
class GetAllCodes(Resource):
    def get(self):
        conn = sqlite3.connect('python_code_snippet_db.db')

        cursor = conn.execute("SELECT id, name, code from CODE_SNIPPET")
        conn.commit()

        return {"data": cursor.fetchall()}


# To Get a Single Record from DB
class GetCodeById(Resource):
    def get(self, code_id):
        conn = sqlite3.connect('python_code_snippet_db.db')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        query = "SELECT * FROM CODE_SNIPPET WHERE id == %d " % int(code_id)

        cursor.execute(query)

        return_data = {"SNIPPET": str(cursor.fetchone()[2])}

        return return_data


# To Execute the Code in DB and returns the Result
class ExecuteCodeById(Resource):
    def post(self, code_id):
        conn = sqlite3.connect('python_code_snippet_db.db')

        cursor = conn.cursor()

        query = "SELECT * FROM CODE_SNIPPET WHERE id == %d " % int(code_id)

        cursor.execute(query)

        data = {}

        exec(str(cursor.fetchone()[2]), globals(), data)

        return_data = {"output": data['code']}

        return return_data


class DeleteCodeById(Resource):
    def post(self, code_id):
        conn = sqlite3.connect('python_code_snippet_db.db')

        cursor = conn.cursor()

        query = "DELETE FROM CODE_SNIPPET WHERE id == %d " % int(code_id)

        cursor.execute(query)

        conn.commit()

        return {
            'message': ' Code Deleted Successfully '
        }


api.add_resource(SaveSnippetCode, '/Savecode')

api.add_resource(GetAllCodes, '/GetAllCodes')

api.add_resource(GetCodeById, '/GetCode/<code_id>')

api.add_resource(ExecuteCodeById, '/execute/<code_id>')

api.add_resource(DeleteCodeById, '/delete/<code_id>')


app.run(host='0.0.0.0', port=5001, debug=True)
