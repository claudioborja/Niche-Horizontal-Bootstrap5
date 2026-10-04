/* Native checkbox selection and delegated starring, including paginated rows. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    function checkboxes() {
        var table = document.querySelector('.mailbox-messages table');
        if (table && window.DataTable && DataTable.isDataTable(table)) {
            return new DataTable(table).rows({ search: 'applied' }).nodes().toArray().reduce(function (all, row) {
                return all.concat(Array.from(row.querySelectorAll("input[type='checkbox']:not(:disabled)")));
            }, []);
        }
        return Array.from(document.querySelectorAll(".mailbox-messages input[type='checkbox']:not(:disabled)"));
    }

    function synchronize() {
        var inputs = checkboxes();
        var allChecked = inputs.length > 0 && inputs.every(function (input) { return input.checked; });
        document.querySelectorAll('.checkbox-toggle').forEach(function (button) {
            button.setAttribute('aria-label', allChecked ? 'Deselect all messages' : 'Select all messages');
            button.setAttribute('aria-pressed', String(allChecked));
            var icon = button.querySelector('.fa');
            if (icon) {
                icon.classList.toggle('fa-check-square-o', allChecked);
                icon.classList.toggle('fa-square-o', !allChecked);
            }
        });
    }

    document.addEventListener('click', function (event) {
        var toggle = event.target.closest('.checkbox-toggle');
        if (toggle) {
            event.preventDefault();
            var inputs = checkboxes();
            var checked = !inputs.every(function (input) { return input.checked; });
            inputs.forEach(function (input) {
                input.checked = checked;
                input.dispatchEvent(new Event('change', { bubbles: true }));
            });
            synchronize();
        }
        var star = event.target.closest('.mailbox-star a');
        if (star) {
            event.preventDefault();
            var icon = star.querySelector('i');
            if (!icon) return;
            if (icon.classList.contains('fa')) {
                icon.classList.toggle('fa-star');
                icon.classList.toggle('fa-star-o');
            } else if (icon.classList.contains('glyphicon')) {
                icon.classList.toggle('glyphicon-star');
                icon.classList.toggle('glyphicon-star-empty');
            }
        }
    });
    document.addEventListener('change', function (event) {
        if (event.target.matches(".mailbox-messages input[type='checkbox']")) synchronize();
    });
    synchronize();
    // jQuery-ready runs after existing DataTables initializers registered by the page.
    if (window.jQuery) jQuery(function () {
        var table = document.querySelector('.mailbox-messages table');
        if (table && window.DataTable && DataTable.isDataTable(table)) {
            new DataTable(table).on('draw', synchronize);
        }
        synchronize();
    });
});
