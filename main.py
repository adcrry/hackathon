import json

from flask import Flask, render_template, request

import src.utils.ask_question_to_pdf as ask_question_to_pdf

json_database = open("data.json")
data = json.loads(json_database.read())
app = Flask("app")


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


@app.route("/qcm", methods=["GET"])
def qcm_page():
    return render_template("qcm.html", name="qcm")


@app.route("/qcm/question", methods=["GET"])
def qcmQuestion():
    n = request.form["nbrQuestions"]
    qcmQuestion = ask_question_to_pdf.generate_QCM(n)
    return {"qcmQuestion": qcmQuestion}


@app.route("/qcm/answer", methods=["GET"])
def qcmAnswer():
    # eeuuh faut gérer de récup les réponses de l'élève
    qcmAnswer = ask_question_to_pdf.generate_answer_QCM(n, answers)
    return {"qcmAnswer": qcmAnswer}
