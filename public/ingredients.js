async function add() {
    const ingredient = document.getElementById('ingredient').value;
    const weight= document.getElementById('weight').value;


    if(!ingredient || !weight) {
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
                weight: parseFloat(weight) || 0,
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
          <td>${weight || 0}kg</td>
        </tr>
        `;

        document.getElementById('ingredient').value = '';
        document.getElementById('weight').value = '';

    } catch (error) {
        alert("Error connecting to server");
        console.error(error);
    }
}

function generateRecipe(){
    window.location.href = "recipes.html";
}