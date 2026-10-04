/* Layout sizing and optional sidebar scrolling. Original template license: MIT. */
(function ($, Niche) {
    'use strict';

    class Layout {
        constructor(element, options) {
            this.options = options;
            this.activate();
            $(window).on('resize.nicheLayout', () => this.refresh());
            $('.sidebar-menu').on('expanded.tree collapsed.tree', () => this.refresh());
            $('.main-header .logo, .sidebar').on('transitionend.nicheLayout', () => this.refresh());
        }

        activate() {
            this.refresh();
            $('body').removeClass('hold-transition');
            if (this.options.resetHeight) $('body, html, .wrapper').css({ height: 'auto', 'min-height': '100%' });
        }

        refresh() {
            this.fix();
            this.fixSidebar();
        }

        fix() {
            $('.layout-boxed > .wrapper').css('overflow', 'hidden');
            const footerHeight = $('.main-footer').outerHeight() || 0;
            const headerHeight = $('.main-header').outerHeight() || 0;
            const viewportHeight = $(window).height();
            const sidebarHeight = $('.sidebar').height() || 0;
            let minimumHeight = $('body').hasClass('fixed')
                ? viewportHeight - footerHeight
                : Math.max(viewportHeight - headerHeight - footerHeight, sidebarHeight);
            minimumHeight = Math.max(minimumHeight, $('.control-sidebar').height() || 0, 0);
            $('.content-wrapper').css('min-height', minimumHeight);
        }

        fixSidebar() {
            if (typeof $.fn.slimScroll !== 'function') return;
            const sidebar = $('.sidebar');
            if (!$('body').hasClass('fixed')) sidebar.slimScroll({ destroy: true }).height('auto');
            else if (this.options.slimscroll) {
                sidebar.slimScroll({ destroy: true }).height('auto').slimScroll({
                    height: $(window).height() - ($('.main-header').height() || 0) + 'px',
                    color: 'rgba(0,0,0,0.2)', size: '3px'
                });
            }
        }
    }

    Niche.definePlugin('layout', Layout, 'lte.layout', { slimscroll: true, resetHeight: true });
    Niche.onLoad(() => $('body').layout());
})(jQuery, window.Niche);
