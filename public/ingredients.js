const host = 8001;

async function add() {
    const ingredient = document.getElementById('ingredient').value;
    const weight = document.getElementById('weight').value;

    if(!ingredient || !weight) {
        alert("Please enter ingredient and weight.");
        return;
    }

    try {
        const res = await fetch("http://localhost:" + host + "/add_Food_Item", {
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

        // Reload the table to show updated data
        await loadFridgeItems();

        // Clear inputs
        document.getElementById('ingredient').value = '';
        document.getElementById('weight').value = '';

    } catch (error) {
        alert("Error connecting to server");
        console.error(error);
    }
}

async function loadFridgeItems() {
    try {
        const res = await fetch("http://localhost:" + host + "/fridge_items");
        const data = await res.json();

        const tableBody = document.getElementById("ingredient-table-body");
        tableBody.innerHTML = ''; // Clear table

        data.items.forEach(item => {
            tableBody.innerHTML += `
            <tr>
              <td>${item.name}</td>
              <td>${item.weight}kg</td>
              <td><button onclick="deleteItem('${item.name}')">Delete</button></td>
            </tr>
            `;
        });

    } catch (error) {
        console.error("Error loading fridge items:", error);
    }
}

async function deleteItem(itemName) {
    try {
        const res = await fetch("http://localhost:" + host + "/remove_Food_Item", {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: itemName })
        });

        if (!res.ok) {
            alert("Failed to delete item");
            return;
        }

        // Reload table after deletion
        await loadFridgeItems();

    } catch (error) {
        alert("Error deleting item");
        console.error(error);
    }
}

async function clearAll() {
    if (!confirm("Are you sure you want to clear all ingredients?")) {
        return;
    }

    try {
        const res = await fetch("http://localhost:" + host + "/clear_Fridge", {
            method: "DELETE"
        });

        if (!res.ok) {
            alert("Failed to clear fridge");
            return;
        }
        await loadFridgeItems();

    } catch (error) {
        alert("Error clearing fridge");
        console.error(error);
    }
}

function generateRecipe() {
    window.location.href = "recipes.html";
}


loadFridgeItems();