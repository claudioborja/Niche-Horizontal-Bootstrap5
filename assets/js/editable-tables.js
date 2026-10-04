/* Local table demos. Edits last until the page is reloaded. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    if (!window.Tabulator || !window.NicheGridData) return;
    var countries = NicheGridData.countries;
    function countryName(value) {
        var country = countries.find(function (item) { return item.Id === Number(value); });
        return country ? country.Name : '';
    }
    function columns(editable) {
        return [
            { title: 'Name', field: 'Name', formatter: 'plaintext', minWidth: 150, editor: editable ? 'input' : false, headerFilter: editable ? 'input' : false },
            { title: 'Age', field: 'Age', width: 90, sorter: 'number', editor: editable ? 'number' : false, editorParams: { min: 0, max: 120 }, validator: ['numeric', 'min:0', 'max:120'], headerFilter: editable ? 'number' : false, headerFilterFunc: '=' },
            { title: 'Address', field: 'Address', formatter: 'plaintext', minWidth: 200, editor: editable ? 'input' : false, headerFilter: editable ? 'input' : false },
            { title: 'Country', field: 'Country', minWidth: 150,
                formatter: function (cell) { var text = document.createElement('span'); text.textContent = countryName(cell.getValue()); return text; },
                sorter: function (a, b) { return countryName(a).localeCompare(countryName(b)); },
                editor: editable ? 'list' : false,
                editorParams: { values: countries.map(function (item) { return { value: item.Id, label: item.Name || '(None)' }; }) },
                mutatorEdit: function (value) { return Number(value); },
                headerFilter: editable ? 'list' : false,
                headerFilterParams: { values: countries.map(function (item) { return { value: item.Id || '', label: item.Name || 'All' }; }), clearable: true },
                headerFilterFunc: function (value, rowValue) { return Number(value) === Number(rowValue); }
            },
            { title: 'Is Married', field: 'Married', width: 120, formatter: 'tickCross', sorter: 'boolean', editor: editable ? 'tickCross' : false,
                headerFilter: editable ? 'list' : false,
                headerFilterParams: { values: [{ value: '', label: 'All' }, { value: 'yes', label: 'Yes' }, { value: 'no', label: 'No' }], clearable: true },
                headerFilterFunc: function (value, rowValue) { return rowValue === (value === 'yes'); }
            }
        ];
    }
    function create(selector, editable) {
        if (!document.querySelector(selector)) return null;
        var fields = columns(editable);
        if (editable) fields.push({ title: 'Actions', headerSort: false, width: 100, formatter: function () {
            var button = document.createElement('button');
            button.type = 'button'; button.className = 'btn btn-sm btn-outline-danger'; button.textContent = 'Delete';
            return button;
        }, cellClick: function (event, cell) {
            if (event.target.closest('button') && window.confirm('Do you really want to delete the client?')) cell.getRow().delete();
        } });
        return new Tabulator(selector, {
            data: NicheGridData.clients.map(function (client, index) { return Object.assign({ id: index + 1 }, client); }),
            height: 500, layout: 'fitColumns', responsiveLayout: 'collapse',
            pagination: true, paginationMode: 'local', paginationSize: 15,
            paginationSizeSelector: [15, 30, 50], placeholder: 'No matching records',
            columns: fields
        });
    }
    create('#basicscenario', true);
    create('#staticdata', false);
    var sorting = create('#soarting', false);
    var field = document.getElementById('sortingField');
    if (sorting && field) {
        sorting.on('tableBuilt', function () { sorting.setSort(field.value, 'asc'); });
        field.addEventListener('change', function () { sorting.setSort(field.value, 'asc'); });
    }
});
