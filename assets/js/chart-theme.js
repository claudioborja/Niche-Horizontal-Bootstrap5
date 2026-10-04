/* Apply the template typography before the page initializes its charts. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    if (!window.Chart) return;
    const theme = getComputedStyle(document.documentElement);
    Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
    Chart.defaults.font.size = parseFloat(theme.getPropertyValue('--niche-font-size-xs')) || 12;
    Chart.defaults.color = theme.getPropertyValue('--niche-color-muted').trim() || '#505b62';
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        Chart.defaults.animation = false;
    }
    // Re-measure labels after the local font has finished loading.
    document.fonts.ready.then(function () {
        Object.values(Chart.instances).forEach(function (chart) { chart.update('none'); });
    });
});
