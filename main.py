from flask import (
    Flask,
    render_template,
    request
)

import src.utils.ask_question_to_pdf as ask_question_to_pdf


app = Flask("app")

@app.route("/")
def hello_world():
    return render_template("index.html", name="index")

@app.route("/prompt", methods=['POST'])
def prompt():
    question = request.form['prompt']
    answer = ask_question_to_pdf.ask_question_to_pdf(question)
    return {"answer": answer}

@app.route("/question", methods=['GET'])
def question():
    answer = ask_question_to_pdf.question()
    return {"answer": answer}

@app.route("/answer", methods=['POST'])
def answer():
    print(request.form)
    user_answer = request.form['prompt']
    question = request.form['question']
    answer = ask_question_to_pdf.correct_answer(user_answer, question)
    return {"answer": answer}
