async function add() {
    const ingredient = document.getElementById('ingredient').value;
    const quantity = document.getElementById('quantity').value;
    const calorie = document.getElementById('calorie').value;  // You need to add this input field to HTML
    const protein = document.getElementById('protein').value;  // You need to add this input field to HTML

    if(!ingredient || !quantity) {
        alert("Please enter ingredient and quantity.");
        return;
    }
    const host= 8001
    try {
        const res = await fetch("http://localhost:"+host+"/add_Food_Item", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: ingredient,
                calorie: parseInt(calorie) || 0,
                protein: parseInt(protein) || 0,
                expiry_date: null
            })
        });

        if (!res.ok) {
            alert("Failed to add item to fridge");
            return;
        }

        document.getElementById("ingredient-table-body").innerHTML += `
        <tr>
          <td>${ingredient}</td>
          <td>${quantity}</td>
          <td>${calorie || 0}</td>
          <td>${protein || 0}</td>
        </tr>
        `;

        document.getElementById('ingredient').value = '';
        document.getElementById('quantity').value = '';
        document.getElementById('calorie').value = '';
        document.getElementById('protein').value = '';

    } catch (error) {
        alert("Error connecting to server");
        console.error(error);
    }
}

function generateRecipe(){
    window.location.href = "recipes.html";
}