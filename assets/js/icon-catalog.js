/* A searchable catalog generated from the locally installed icon font. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    var catalog = document.getElementById('icon-catalog');
    var search = document.getElementById('icon-search');
    var count = document.getElementById('icon-count');
    if (!catalog || !search || !window.NicheIconNames) return;
    var brands = ['facebook', 'twitter', 'twitter-x', 'github', 'gitlab', 'google', 'instagram', 'linkedin', 'dropbox', 'microsoft', 'apple', 'android', 'youtube', 'twitch', 'reddit', 'whatsapp', 'telegram', 'discord', 'spotify', 'pinterest', 'tiktok', 'threads', 'meta'];
    var category = catalog.dataset.category;
    var names = NicheIconNames.filter(function (name) {
        if (category === 'brands') return brands.includes(name);
        if (category === 'arrows') return /arrow|chevron|caret/.test(name);
        if (category === 'interface') return !brands.includes(name) && !/arrow|chevron|caret/.test(name);
        return true;
    });
    function render() {
        var query = search.value.trim().toLowerCase();
        var matches = names.filter(function (name) { return name.includes(query); });
        var fragment = document.createDocumentFragment();
        matches.forEach(function (name) {
            var item = document.createElement('div');
            item.className = 'col-6 col-md-4 col-lg-3';
            var icon = document.createElement('i');
            icon.className = 'bi bi-' + name + ' me-2';
            icon.setAttribute('aria-hidden', 'true');
            item.appendChild(icon);
            item.appendChild(document.createTextNode(name));
            fragment.appendChild(item);
        });
        catalog.replaceChildren(fragment);
        count.textContent = matches.length + ' icons';
    }
    search.addEventListener('input', render);
    render();
});
