#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
"""
JSON API:
incoming : 
{
    "src_lang" : "en",
    "tgt_lang" : "de" or "fr",
    "text" : "text to translate"
}

outgoing :
{
    "text" : "translated text",
    "err_no" : error number,
    "err" : "error descr"
}
"""

def translate_req_checker(req):
    if ("src_lang" in req and "tgt_lang" in req and "text" in req):
        if ((req["tgt_lang"] == "fr" or req["tgt_lang"] == "de") and (req["src_lang"] == "en")):
            return True

def return_translated_json(text, err_no = 200, err = "OK"):
    ret_dict = {
        "text" : text,
        "err_no" : err_no,
        "err" : err
    }
    return jsonify(ret_dict)


@app.route("/", methods=["GET", "POST"])
@app.route("/translate", methods = ["GET", "POST"])
def translate_handler():
    if not request.json or not translate_req_checker(request.json):
        return return_translated_json("", 400, "Bad Request")
    print(request.json)
    translated_text = str(datetime.now()) + " Devashish Says Hi ! :)"
    return return_translated_json(translated_text)
    


if __name__ == "__main__":
    app.run(debug=True, port=5001)