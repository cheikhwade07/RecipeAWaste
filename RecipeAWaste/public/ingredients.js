function add() {
    const ingredient = document.getElementById('ingredient').value;
    const quantity = document.getElementById('quantity').value;

    // case of empty input
    if(!ingredient || !quantity) {
        alert("Please enter both ingredient and quantity.");
        return;
    }

    document.getElementById("ingredient-table-body").innerHTML += `
    <tr>
      <td>${ingredient}</td>
      <td>${quantity}</td>
    </tr>
    `;

    // delete input values after adding
    document.getElementById('ingredient').value = '';
    document.getElementById('quantity').value = '';
}

function getIngredients(){
    const table = document.getElementById("ingredient-table-body");
    const ingredients = [];
    for (let row of table.rows) {
        const ingredient = row.cells[0].innerText;
        const quantity = row.cells[1].innerText;
        ingredients.push({ ingredient, quantity });
    }
    return ingredients;
}

function generateRecipe(){
    const ingredients = getIngredients();
    
   
    localStorage.setItem("ingredients", JSON.stringify(ingredients));
    window.location.href = "recipes.html";
}