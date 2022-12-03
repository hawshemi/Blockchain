function table2Excel(){
    let table2excel = new Table2Excel();
    table2excel.export(document.querySelectorAll("table.table"));
}
