
const resultDiv = document.getElementById('recipe-result');


const host=8001;

 generateRecipe();
async function generateRecipe() {
  try {
        const res = await fetch("http://localhost:"+host+"/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const aiText = await res.text();
        const formattedText = aiText.replace(/\\n/g, '');
        resultDiv.innerHTML = formattedText;


    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        console.error(error);

    }

}