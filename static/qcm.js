const generateButton = document.getElementById("generate-button");
const promptForm = document.getElementById("qcm-form")

const handleNbrQuestions = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  generateButton.reset();

  let url = "/qcm/question";

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.qcmQuestion;
  });
}

promptForm.addEventListener("submit", handleNbrQuestions);

