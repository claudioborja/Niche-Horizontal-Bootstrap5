/* Shared DataTables examples; register before mailbox and export callbacks. */
jQuery(function () {
    'use strict';
    if (!window.DataTable) return;
    const first = document.getElementById('example1');
    const second = document.getElementById('example2');
    if (first && !DataTable.isDataTable(first)) new DataTable(first, { deferRender: false });
    if (second && !DataTable.isDataTable(second)) {
        new DataTable(second, {
            deferRender: false, paging: true, lengthChange: false,
            searching: false, ordering: true, info: true, autoWidth: false
        });
    }
});
