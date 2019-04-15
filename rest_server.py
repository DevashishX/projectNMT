#!/usr/bin/env python3

import os
from flask import Flask, jsonify, abort, request, flash, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from json import dumps
from driver import *

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io

from datetime import datetime



# try:
#     from PIL import Image
# except ImportError:
#     import Image
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
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

def filename_to_dottxt(filename):
    return filename.rsplit('.', 1)[0] + ".txt"

def text_to_text(filename):
    fd = open(filename, "r")
    extracted = fd.readlines()
    fd.close()
    extracted = "".join(extracted)    
    return extracted

def image_to_text(filename):
    im = Image.open(filename)
    im = im.convert('L')
    new_width = im.size[0] * 3
    new_height = im.size[1] * 3
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    im = im.filter(ImageFilter.SHARPEN)
    im = im.filter(ImageFilter.EDGE_ENHANCE)
    im.save(filename, dpi=(300,300))
    text = pytesseract.image_to_string(Image.open(filename))
    print(text)
    return text

def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    return data

def pdf_to_text(filename):
    return pdfparser(filename)
    pass




@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index_handler():
    return send_file("index.html")

@app.route("/upload.html", methods=["GET", "POST"])
def uploadhtml_handler():
    return send_file("upload.html")

@app.route("/feedback.html", methods=["GET", "POST"])
def feedbackhtml_handler():
    return send_file("feedback.html")

@app.route("/thankyou.html", methods=["GET", "POST"])
def thankyouhtml_handler():
    return send_file("thankyou.html")

@app.route("/moreinfo.html", methods=["GET", "POST"])
def moreinfohtml_handler():
    return send_file("moreinfo.html")

@app.route("/favicon.ico", methods=["GET", "POST"])
def faviconico_handler():
    return send_file("favicon.ico")


@app.route("/translate", methods = ["GET", "POST"])
def translate_handler():
    print(request.json)
    if not request.json or not translate_req_checker(request.json):
        print("In error")
        return return_json_error()
    print("no error")
    translated_text = driver(src_lang=request.json["src_lang"],
                            tgt_lang=request.json["tgt_lang"],
                            input_str=request.json["text"])
    return return_translated_json(translated_text)
    


@app.route("/translate/text/de", methods =["POST"])
def de_textfile_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return return_json_error()
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return return_json_error()
        if file and allowed_file(file.filename) and is_textfile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fd = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "r")
            extracted = fd.readlines()
            fd.close()
            extracted = "".join(extracted)
            translated_text = driver(src_lang="en",
                            tgt_lang="de",
                            input_str=extracted)
            attachment_name = filename = "de_"+filename
            filename = os.path.join(DOWNLOAD_FOLDER, filename)
            fd = open(filename, "w")
            fd.write(translated_text)
            fd.close()
            return send_file(filename, attachment_filename = attachment_name, as_attachment=True)
            
    return return_json_error()


@app.route("/translate/text/fr", methods =["POST"])
def fr_textfile_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return return_json_error()
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return return_json_error()
        if file and allowed_file(file.filename) and is_textfile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fd = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "r")
            extracted = fd.readlines()
            fd.close()
            extracted = "".join(extracted)
            translated_text = driver(src_lang="en",
                            tgt_lang="fr",
                            input_str=extracted)
            attachment_name = filename = "fr_"+filename
            filename = os.path.join(DOWNLOAD_FOLDER, filename)
            fd = open(filename, "w")
            fd.write(translated_text)
            fd.close()
            return send_file(filename, attachment_filename = attachment_name, as_attachment=True)
    return return_json_error()

@app.route("/translate/file/de", methods =["POST"])
def de_file_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return return_json_error()
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return return_json_error()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename_with_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename_with_path)
            extracted = ""

            if is_textfile(filename):
                extracted = text_to_text(filename_with_path)
            elif is_imagefile(filename):
                extracted = image_to_text(filename_with_path)
            elif is_pdffile(filename):
                extracted = pdf_to_text(filename_with_path)
            
            translated_text = extracted
            translated_text = driver(src_lang="en",
                            tgt_lang="de",
                            input_str=extracted)

            filename = "de_" + filename
            attachment_name = filename_to_dottxt(filename)
            filename = os.path.join(DOWNLOAD_FOLDER, filename)
            fd = open(filename, "w")
            fd.write(translated_text)
            fd.close()
            return send_file(filename, attachment_filename = attachment_name, as_attachment=True)
    return return_json_error()


@app.route("/translate/file/fr", methods =["POST"])
def fr_file_handler():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return return_json_error()
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return return_json_error()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename_with_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename_with_path)
            extracted = ""

            if is_textfile(filename):
                extracted = text_to_text(filename_with_path)
            elif is_imagefile(filename):
                extracted = image_to_text(filename_with_path)
            elif is_pdffile(filename):
                extracted = pdf_to_text(filename_with_path)
            
            translated_text = extracted
            translated_text = driver(src_lang="en",
                            tgt_lang="fr",
                            input_str=extracted)

            filename = "fr_" + filename
            attachment_name = filename_to_dottxt(filename)
            filename = os.path.join(DOWNLOAD_FOLDER, filename)
            fd = open(filename, "w")
            fd.write(translated_text)
            fd.close()
            return send_file(filename, attachment_filename = attachment_name, as_attachment=True)
    return return_json_error()

@app.route("/feedback", methods =["POST"])
def feedback_handler():
    print(request.form)
    name = request.form["name"]
    email = request.form["email"]
    feedback = request.form["feedback"]
    feedback_dict = {"name" : name, "email" : email, "feedback" : feedback}
    filename = os.path.join("./feedback/", str(datetime.now()).replace(" ", "-") + ".txt")
    fd = open(filename , "w")
    fd.write(str(dumps(feedback_dict)))
    fd.close()
    return send_file("thankyou.html")


    pass

if __name__ == "__main__":
    app.run(debug=True)