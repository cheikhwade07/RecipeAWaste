const saved = localStorage.getItem('ingredients');
const resultDiv = document.getElementById('result');


const ingredients = saved ? JSON.parse(saved) : [];

generateRecipe(ingredients);

async function generateRecipe(ingredients) {
  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredients })
  });

  // ai starts here
  const aiText = await res.text();
  resultDiv.innerHTML = `<pre>${aiText}</pre>`;
  // ai ends here
}