from flask import Flask, request, jsonify
from wsgimod import HttpRequest
from pretty import PrettyDict

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    req = HttpRequest(request.environ);
    print(req.query())
    print(req.body())
    print(req.file())
    return jsonify(req.request())