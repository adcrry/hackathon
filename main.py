import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import src.utils.ask_question_to_pdf as ask_question_to_pdf

UPLOAD_FOLDER = "/"
ALLOWED_EXTENSIONS = {"pdf"}

json_database = open("data.json")
data = json.loads(json_database.read())
app = Flask("app")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super secret key"


@app.route("/")
def hello_world():
    return render_template("index.html", name="index", data=data)


@app.route("/prompt", methods=["POST"])
def prompt():
    question = request.form["prompt"]
    answer = ask_question_to_pdf.ask_question_to_pdf(question)
    return {"answer": answer}


@app.route("/question", methods=["GET"])
def question():
    answer = ask_question_to_pdf.question()
    return {"answer": answer}


@app.route("/answer", methods=["POST"])
def answer():
    user_answer = request.form["prompt"]
    question = request.form["question"]
    answer = ask_question_to_pdf.correct_answer(user_answer, question)
    # Write json file
    data.append({"question": question, "answer": answer})
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)
    return {"answer": answer}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("index", name=filename))
