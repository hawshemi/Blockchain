function table2Excel() {

    let table2excel = new Table2Excel();
    table2excel.export(document.querySelectorAll("table.table"));
}

function resetBlockchain() {
    
    let text = "Are you sure?\nOk=Delete all data.";
    if (confirm(text) == true) {
        document.getElementById("deleteForm").submit();
    } else {
        alert("Cancelled!");
    }
}
