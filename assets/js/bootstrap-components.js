/* Shared initialization for Bootstrap 5 components that require opt-in. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    if (!window.bootstrap) return;

    document.querySelectorAll('[data-bs-toggle="dropdown"]').forEach(function (element) {
        bootstrap.Dropdown.getOrCreateInstance(element);
    });

    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (element) {
        bootstrap.Tooltip.getOrCreateInstance(element);
    });

    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (element) {
        var templateId = element.dataset.popoverTemplate;
        var template = templateId ? document.getElementById(templateId) : null;
        var options = {};
        if (template && template.tagName === 'TEMPLATE') {
            options = {
                html: true,
                title: template.dataset.title || '',
                // Only local, authored templates provide DOM content; text remains sanitized by Bootstrap.
                content: function () { return template.content.firstElementChild.cloneNode(true); },
                container: 'body',
                customClass: 'niche-popover-' + (template.dataset.theme || 'default')
            };
        }
        var alignment = element.dataset.popoverAlign;
        if (alignment === 'start' || alignment === 'end') {
            options.popperConfig = function (config) {
                return Object.assign({}, config, { placement: config.placement + '-' + alignment });
            };
        }
        bootstrap.Popover.getOrCreateInstance(element, options);
    });

    function hidePopovers() {
        document.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (element) {
            var instance = bootstrap.Popover.getInstance(element);
            if (instance) instance.hide();
        });
    }
    document.addEventListener('click', function (event) {
        var close = event.target.closest('[data-popover-close]');
        if (close) {
            event.preventDefault();
            var popover = close.closest('.popover');
            if (!popover) return;
            document.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (element) {
                if (element.getAttribute('aria-describedby') === popover.id) {
                    var instance = bootstrap.Popover.getInstance(element);
                    if (instance) instance.hide();
                    element.focus();
                }
            });
        } else if (!event.target.closest('.popover, [data-bs-toggle="popover"]')) {
            hidePopovers();
        }
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') hidePopovers();
    });
});
