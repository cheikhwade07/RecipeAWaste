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