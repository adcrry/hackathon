import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import src.utils.ask_question_to_pdf as ask_question_to_pdf

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = {"pdf"}

json_database = open("data.json")
data = json.loads(json_database.read())

json_theme = open("theme.json")
theme = json.loads(json_theme.read())

app = Flask("app")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super secret key"


@app.route("/")
def hello_world():
    return render_template("index.html", name="index", data=data)


@app.route("/theme", methods=["GET"])
def getTheme():
    return theme["theme"]


@app.route("/theme", methods=["PUT"])
def putTheme():
    "modify the json file to change the theme"
    nowTheme = theme["theme"]
    if nowTheme == "light":
        theme["theme"] = "dark"
    else:
        theme["theme"] = "light"
    with open("theme.json", "w") as json_file:
        json.dump(theme, json_file)


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
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], "filename.pdf"))
            return redirect("/")
@app.route("/qcm", methods=["GET"])
def qcm_page():
    return render_template("qcm.html", name="qcm")


@app.route("/qcm/question", methods=["POST"])
def qcmQuestion():
    n = request.form["nbrQuestions"]
    qcmQuestion = ask_question_to_pdf.generate_QCM(n)
    print(qcmQuestion)
    return {"qcmQuestion": qcmQuestion}


@app.route("/qcm/answer", methods=["GET"])
def qcmAnswer():
    # eeuuh faut gérer de récup les réponses de l'élève
    # qcmAnswer = ask_question_to_pdf.generate_answer_QCM(n, answers)
    return {"qcmAnswer": qcmAnswer}
