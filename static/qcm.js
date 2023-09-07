const generateButton = document.getElementById("generate-button");

const handleNbrQuestions = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  console.log(data);
  generateButton.reset();

  let url = "/qcm/question";

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
}

generateButton.addEventListener("submit", handleNbrQuestions);

