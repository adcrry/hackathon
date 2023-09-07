const generateButton = document.getElementById("generate-button");
const promptForm = document.getElementById("qcm-form")
const qcmForm = document.getElementById("qcm-questions-form")
var questions = null
var nbQuestion = 0
const createQCM = async (messagePromise) => {
  qcmForm.innerHTML = ""
  const qcmData = await messagePromise();
  const jsonData = JSON.parse(qcmData)
  questions = jsonData
  for (var question in jsonData.questions) {
    const div = document.createElement("div");
    const questionElement = document.createElement("p");
    const input1 = document.createElement("input");
    const input2 = document.createElement("input");
    const input3 = document.createElement("input");
    const label1 = document.createElement("label");
    const label2 = document.createElement("label");
    const label3 = document.createElement("label");

    input1.id = "q-" + question + "-0"
    input2.id = "q-" + question + "-1"
    input3.id = "q-" + question + "-2"

    input1.name = "q-" + question
    input2.name = "q-" + question
    input3.name = "q-" + question

    input1.type = "radio"
    input2.type = "radio"
    input3.type = "radio"

    label1.for = "q-" + question + "-0"
    label2.for = "q-" + question + "-1"
    label3.for = "q-" + question + "-2"

    label1.id = "label-" + question + "-0"
    label2.id = "label-" + question + "-1"
    label3.id = "label-" + question + "-2"

    questionElement.innerHTML = jsonData.questions[question].question

    label1.innerHTML = jsonData.questions[question].answers[0]
    label2.innerHTML = jsonData.questions[question].answers[1]
    label3.innerHTML = jsonData.questions[question].answers[2]
    div.appendChild(questionElement)
    div.appendChild(input1)
    div.appendChild(label1)
    div.appendChild(input2)
    div.appendChild(label2)
    div.appendChild(input3)
    div.appendChild(label3)

    qcmForm.appendChild(div)

  }

};

const handleNbrQuestions = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();
  nbQuestion = data.get("nbrQuestions")
  let url = "/qcm/question"
  await createQCM(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.qcmQuestion;
  });
}
promptForm.addEventListener("submit", handleNbrQuestions);

const correctQCM = () => {
  for (var i = 0; i < nbQuestion; i++) {
    const labels = [
      document.getElementById("label-" + i + "-0"),
      document.getElementById("label-" + i + "-1"),
      document.getElementById("label-" + i + "-2")
    ]
    const inputs = [
      document.getElementById("q-" + i + "-0"),
      document.getElementById("q-" + i + "-1"),
      document.getElementById("q-" + i + "-2")
    ]
    console.log(inputs[questions.questions[i].correct_answer])
    if (inputs[questions.questions[i].correct_answer].checked) {
      labels[questions.questions[i].correct_answer].style.color = "green"
    } else {
      for (var j = 0; j < 3; j++) {
        if (inputs[j].checked) {
          labels[j].style.color = "red"
        }
      }
    }


  }
}

