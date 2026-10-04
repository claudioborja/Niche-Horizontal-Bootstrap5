/* Bootstrap-styled native controls; checkboxes do not support HTML readonly. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    var demo = document.querySelector('.switch-demo');
    if (!demo) return;

    function update(input) {
        var label = demo.querySelector("label[for='" + input.id + "'] .switch-value");
        if (label) label.textContent = input.checked ? input.dataset.onText : input.dataset.offText;
    }
    demo.querySelectorAll('input').forEach(update);
    demo.addEventListener('change', function (event) {
        if (event.target.matches('input')) update(event.target);
    });
    demo.addEventListener('click', function (event) {
        if (event.target.matches("input[aria-readonly='true']")) {
            event.preventDefault();
            return;
        }
        var clear = event.target.closest('[data-clear-radio]');
        if (clear) demo.querySelectorAll("input[name='" + clear.dataset.clearRadio + "']").forEach(function (input) {
            input.checked = false;
            input.dispatchEvent(new Event('change', { bubbles: true }));
        });
    });
});
