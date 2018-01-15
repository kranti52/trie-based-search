import csv
import os
from trie import Trie
from flask import Flask, jsonify, request, render_template
from flask_script import Manager, Server
app = Flask(__name__)

FILE = os.environ.get("FILE", "data.csv")

trie = Trie()
def start():
	with open(FILE) as f:
	    for i,row in enumerate(f):
	    	if 0 == i:
	    		continue
	    	name = ''
	    	data = row.split(',')
	    	if data[0].strip():
	    		name += data[0].strip()
	    	if data[1].strip():
	    		if name:
	    			name += ' ' + data[1].strip()
	    		else:
	    			name += data[1].strip()
	    	if data[2].strip():
	    		if name:
	    			name += ' ' + data[2].strip()
	    		else:
	    			name += data[2].strip()

	    	if data[0].strip():
	    		print(data[0].lower())
	    		trie.insert(data[0].strip().lower(), name)
	    	if data[1].strip():
	    		print(data[1].lower())
	    		trie.insert(data[1].strip().lower(), name)
	    	if data[2].strip():
	    		print(data[2].lower())
	    		trie.insert(data[2].strip().lower(), name)

start()

@app.route('/auto')
def autocomplete():
    query = request.args.get("q", '')
    if not query or len(query) < 3:
    	return jsonify(results = [])
    results = trie.autocomplete(query.lower().strip().replace(" ", "%20"))
    resp = jsonify(results=results[:10])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/")
def index():
    return render_template('index.html')
