/* Native layout sizing and browser sidebar scrolling. Original template license: MIT. */
(function (Niche) {
    'use strict';
    const height = selector => document.querySelector(selector)?.getBoundingClientRect().height || 0;
    class Layout {
        constructor(element, options) {
            this.options = options;
            this.activate();
            window.addEventListener('resize', () => this.refresh());
            document.addEventListener('expanded.tree', () => this.refresh());
            document.addEventListener('collapsed.tree', () => this.refresh());
            document.querySelectorAll('.main-header .logo, .sidebar').forEach(node => node.addEventListener('transitionend', () => this.refresh()));
        }
        activate() {
            this.refresh();
            document.body.classList.remove('hold-transition');
            if (this.options.resetHeight) document.querySelectorAll('body, html, .wrapper').forEach(node => {
                node.style.height = 'auto'; node.style.minHeight = '100%';
            });
        }
        refresh() { this.fix(); this.fixSidebar(); }
        fix() {
            document.querySelectorAll('.layout-boxed > .wrapper').forEach(node => { node.style.overflow = 'hidden'; });
            const minimum = document.body.classList.contains('fixed')
                ? window.innerHeight - height('.main-footer')
                : Math.max(window.innerHeight - height('.main-header') - height('.main-footer'), height('.sidebar'));
            document.querySelectorAll('.content-wrapper').forEach(node => {
                node.style.minHeight = Math.max(minimum, height('.control-sidebar'), 0) + 'px';
            });
        }
        fixSidebar() {
            document.querySelectorAll('.sidebar').forEach(sidebar => {
                const fixed = document.body.classList.contains('fixed') && this.options.slimscroll;
                sidebar.style.height = fixed ? Math.max(0, window.innerHeight - height('.main-header')) + 'px' : 'auto';
                sidebar.style.overflowY = fixed ? 'auto' : '';
                sidebar.style.scrollbarWidth = fixed ? 'thin' : '';
            });
        }
    }
    Niche.defineComponent('layout', Layout, 'lte.layout', { slimscroll: true, resetHeight: true });
    Niche.onLoad(() => Niche.component(document.body, 'layout'));
})(window.Niche);
