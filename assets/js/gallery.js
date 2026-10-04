/* Filtered responsive gallery with the browser's modal dialog and keyboard navigation. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    const grid = document.getElementById('gallery-grid');
    if (!grid) return;
    const items = Array.from(grid.querySelectorAll('.gallery-item'));
    const filters = Array.from(document.querySelectorAll('.gallery-filter'));
    const dialog = document.getElementById('gallery-lightbox');
    const image = dialog.querySelector('img');
    const caption = document.getElementById('gallery-caption');
    const counter = document.getElementById('gallery-position');
    let current = 0;
    let links = [];
    filters.forEach(function (button) {
        const selector = button.dataset.filter;
        const count = items.filter(function (item) { return selector === '*' || item.matches(selector); }).length;
        button.querySelector('.gallery-counter').textContent = '(' + count + ')';
        button.addEventListener('click', function () {
            items.forEach(function (item) { item.hidden = selector !== '*' && !item.matches(selector); });
            filters.forEach(function (filter) { filter.setAttribute('aria-pressed', String(filter === button)); });
        });
    });
    function show(index) {
        current = (index + links.length) % links.length;
        const link = links[current];
        image.src = link.href;
        image.alt = link.querySelector('.gallery-title').textContent;
        caption.textContent = link.querySelector('.gallery-caption').textContent.trim().replace(/\s+/g, ' ');
        counter.textContent = (current + 1) + ' of ' + links.length;
    }
    grid.addEventListener('click', function (event) {
        const link = event.target.closest('.gallery-link');
        if (!link) return;
        event.preventDefault();
        links = items.filter(function (item) { return !item.hidden; }).map(function (item) { return item.querySelector('.gallery-link'); });
        show(links.indexOf(link));
        dialog.showModal();
    });
    dialog.querySelector('[data-gallery-close]').addEventListener('click', function () { dialog.close(); });
    dialog.querySelector('[data-gallery-prev]').addEventListener('click', function () { show(current - 1); });
    dialog.querySelector('[data-gallery-next]').addEventListener('click', function () { show(current + 1); });
    dialog.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
            event.preventDefault();
            show(current + (event.key === 'ArrowRight' ? 1 : -1));
        }
    });
    dialog.addEventListener('click', function (event) {
        const rect = dialog.getBoundingClientRect();
        if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
    });
});
