#!/usr/bin/env python3

import os
from flask import Flask, jsonify, abort, request, flash
from werkzeug.utils import secure_filename
from flask_cors import CORS
from driver import *

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])


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

def return_json_error(err_no = 400, err = "Bad Request"):
    return return_translated_json("", err_no, err)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_textfile(filename):
    return filename.rsplit('.', 1)[1].lower() in ["txt"]

def is_pdffile(filename):
    return filename.rsplit('.', 1)[1].lower() in ["pdf"]

def is_imagefile(filename):
    return filename.rsplit('.', 1)[1].lower() in ["png", "jpg", "jpeg"]


@app.route("/", methods=["GET", "POST"])
def index_handler():
    return "Please access localhost:5000/translate for rest API"

@app.route("/translate", methods = ["GET", "POST"])
def translate_handler():
    if not request.json or not translate_req_checker(request.json):
        return return_json_error()
    translated_text = driver(src_lang=request.json["src_lang"],
                            tgt_lang=request.json["tgt_lang"],
                            input_str=request.json["text"])
    return return_translated_json(translated_text)
    


@app.route("/translate/text", methods =["POST"])
def textfile_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return return_json_error()
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return return_json_error()
        if file and allowed_file(file.filename) and is_textfile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extracted = file.read()
            print(extracted)
            print(request.is_json())
            return return_translated_json("file received")
    return return_json_error()


if __name__ == "__main__":
    app.run(debug=True)