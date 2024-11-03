let column_values;
let row_values;

const upper_number_of_values = 20;
const lower_nubmer_of_values = 5;

let values_to_multiply;
const upper_boundary = 99;
const lower_boudnary = 1;

function multiply(num1, num2) {
    if (num1 == 0 || num2 == 0){
        return 0;
    } else {
        return num1 * num2
    } 
} 

function getRandomValues(number, upper_boundary, lower_boudnary){
    const values = new Set();
    while (values.size < number) {
        values.add(Math.floor(Math.random() * (upper_boundary - lower_boudnary + 1)) + lower_boudnary);
    }
    return Array.from(values);
}

document.getElementById("generate-table").addEventListener("click", function() {
    const n = parseInt(document.getElementById("n-value").value);
    if (isNaN(n) || n < 5 || n > 20) {
        document.getElementById("message").innerText = "Wrong value chosen, setting n=5.";
        generateMultiplicationTable(5);
    } else {
        document.getElementById("message").innerText = "";
        generateMultiplicationTable(n);
    }
});

function generateMultiplicationTable(multipliersNumber){
    const tableContainer = document.getElementById("table-container");
    tableContainer.innerHTML = "";
    
    column_values = getRandomValues(multipliersNumber, upper_boundary, lower_boudnary);
    row_values = column_values;
    // row_values = getRandomValues(multipliersNumber, upper_boundary, lower_boudnary);

    generateTableWithHeaderRow();
    generateRows();
}

function generateTableWithHeaderRow(){
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody")
    const headerRow = document.createElement("tr");
    const emptyHeader = document.createElement("th");
    emptyHeader.className = "header-row";
    headerRow.appendChild(emptyHeader);
    column_values.forEach(element => {
        const th = document.createElement("th");
        th.textContent = element;
        th.className = "header-row";
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);
    table.appendChild(tbody);
    document.getElementById("table-container").appendChild(table);
}

function generateRows() {
    const tbody = document.querySelector("#table-container table tbody");
    row_values.forEach(rowValue => {
        const row = document.createElement("tr");
        const rowHeader = document.createElement("th");
        rowHeader.textContent = rowValue;
        rowHeader.className = "header-row"
        row.appendChild(rowHeader);

        column_values.forEach(colValue => {
            const cell = document.createElement("td");
            const result = multiply(rowValue, colValue);
            cell.textContent = result;
            cell.className = result % 2 === 0 ? "even" : "odd";
            row.appendChild(cell);
        });

        tbody.appendChild(row);
    });
}