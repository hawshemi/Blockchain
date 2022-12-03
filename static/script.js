function table2Excel(){
    var table2excel = new Table2Excel();
    table2excel.export(document.querySelectorAll("table.table"));
}
