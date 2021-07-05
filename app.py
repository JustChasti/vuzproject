from flask import Flask, request, jsonify
import json
import requests
import config
import db


app = Flask(__name__)


@app.route("/links/parse/", methods=["GET"])
def send_urls():
    """Send links to parser"""
    return jsonify(db.get_links())


@app.route("/links/update/", methods=["PUT"])
def get_parse_urls():
    """Get links from parser and update in base"""
    j_request = request.json
    try:
        db.update_link(j_request[0]['url'], j_request[0]['Name'], j_request[0]['Price'], j_request[0]['Art'], j_request[0]['Col_otz'], j_request[1])
    except Exception as e:
        print('неизвестный баг')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/links/add/", methods=["POST"])
def get_link():
    """Add a new link to base"""
    j_request = request.json
    db.append_link(j_request['link'])
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True)
