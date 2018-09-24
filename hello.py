from flask import Flask, request, jsonify
from wsgimod import HttpRequest
from pretty import PrettyDict
import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    req = HttpRequest(request.environ)
    if req.has_query():
        print(req.query())
    
    if req.has_body():
        print(req.body())
    
    if req.has_files():
        print(req.file())

    # print(req.to_dict())
    
    return jsonify(req.to_dict())