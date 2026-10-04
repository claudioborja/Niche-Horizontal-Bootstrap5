/* Local examples: prevent placeholder navigation and accidental form requests. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    let status;
    let origin;
    function announce(message, source) {
        origin = source;
        if (!status) {
            status = document.createElement('div');
            status.className = 'demo-status';
            status.setAttribute('role', 'status');
            status.setAttribute('aria-live', 'polite');
            const text = document.createElement('span');
            text.className = 'demo-status-text';
            const close = document.createElement('button');
            close.type = 'button';
            close.className = 'btn btn-light border';
            close.textContent = 'Close';
            close.setAttribute('aria-label', 'Close demo notice');
            close.addEventListener('click', function () {
                status.hidden = true;
                if (origin?.isConnected) origin.focus();
            });
            status.append(text, close);
            document.body.append(status);
        }
        status.hidden = false;
        status.querySelector('.demo-status-text').textContent = message;
    }
    function mark(control) {
        control.dataset.demoAction = 'true';
        if (control.tagName === 'A') control.setAttribute('role', 'button');
        const name = control.getAttribute('aria-label') || control.textContent.trim().replace(/\s+/g, ' ') || 'Action';
        control.setAttribute('aria-label', name + ' (demo)');
        control.title = 'Demo action. No external service or destination is configured.';
    }
    const functional = '[data-bs-toggle], [data-bs-dismiss], [data-toggle], [data-widget], [data-editor-action], [data-gallery-filter], [role="tab"], .mailbox-star a';
    document.querySelectorAll('a[href="#"]').forEach(function (link) {
        if (link.matches(functional) || link.closest('#respMenu, .treeview-menu, .jodit-container, .filepond--root')) return;
        mark(link);
    });
    document.querySelectorAll('button').forEach(function (button) {
        if (button.id || button.matches(functional + ', .checkbox-toggle, [type="reset"]') ||
            [...button.attributes].some(attr => attr.name.startsWith('data-')) ||
            button.closest('form, .jodit-container, .filepond--root, .chart-data, .tabulator, .dt-container, #calendar, #calendar1, [role="group"][aria-label^="Export table"]')) return;
        mark(button);
    });
    document.querySelectorAll('[data-demo-action]:not([title])').forEach(mark);
    document.querySelectorAll('form[data-demo-form]').forEach(function (form) {
        const note = document.createElement('p');
        note.className = 'demo-form-note';
        note.textContent = 'Demo form. No account is created and no information is sent or saved.';
        form.prepend(note);
    });
    document.addEventListener('click', function (event) {
        const control = event.target.closest('[data-demo-action]');
        if (!control || event.defaultPrevented) return;
        event.preventDefault();
        announce(control.dataset.demoMessage || 'Demo action. No external service or destination is configured.', control);
    });
    document.addEventListener('keydown', function (event) {
        const link = event.target.closest('a[data-demo-action]');
        if (link && event.key === ' ') {
            event.preventDefault();
            link.click();
        }
    });
    document.addEventListener('submit', function (event) {
        if (event.defaultPrevented) return;
        event.preventDefault();
        announce(event.target.matches('.search-form') ? 'Demo search. No search service is connected.' : 'Demo completed. No information was sent or saved.', event.submitter);
    });
});
