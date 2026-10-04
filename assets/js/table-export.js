/* Export the filtered table, including rows on other pages, with SheetJS. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    document.querySelectorAll('.content table').forEach(function (table) {
        var controls = document.createElement('div');
        controls.className = 'd-flex flex-wrap gap-2 my-3';
        controls.setAttribute('role', 'group');
        controls.setAttribute('aria-label', 'Export table ' + table.id);

        ['xlsx', 'xls', 'csv', 'txt'].forEach(function (format) {
            var button = document.createElement('button');
            button.type = 'button';
            button.className = 'btn btn-outline-primary btn-sm';
            button.textContent = 'Export ' + format.toUpperCase();
            button.addEventListener('click', function () {
                var header = table.tHead ? Array.from(table.tHead.rows) : [];
                var rows = window.DataTable && DataTable.isDataTable(table)
                    ? new DataTable(table).rows({ search: 'applied', order: 'applied' }).nodes().toArray()
                    : Array.from(table.tBodies).reduce(function (all, body) {
                        return all.concat(Array.from(body.rows));
                    }, []);
                var data = header.concat(rows).map(function (row) {
                    return Array.from(row.cells).map(function (cell) {
                        return cell.textContent.trim();
                    });
                });
                var sheet = XLSX.utils.aoa_to_sheet(data);
                var workbook = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(workbook, sheet, 'Data');
                XLSX.writeFile(workbook, (table.id || 'table') + '.' + format, {
                    bookType: format === 'xls' ? 'biff8' : format
                });
            });
            controls.appendChild(button);
        });

        var container = table.closest('.dt-container') || table;
        container.parentNode.insertBefore(controls, container);
    });
});
