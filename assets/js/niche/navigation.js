/* Horizontal menu, sidebar navigation and tree menus. Original template license: MIT. */
(function ($, Niche) {
    'use strict';

    class PushMenu {
        constructor(element, options) {
            this.options = options;
            if (options.expandOnHover || $('body').is('.sidebar-mini.fixed')) {
                $('.main-sidebar').on('mouseenter.nichePushMenu', () => {
                    if ($('body').is('.sidebar-mini.sidebar-collapse') && !this.isMobile()) this.expand();
                }).on('mouseleave.nichePushMenu', () => {
                    if ($('body').hasClass('sidebar-expanded-on-hover')) this.collapse();
                });
                $('body').addClass('sidebar-mini-expand-feature');
            }
            $('.content-wrapper').on('click.nichePushMenu', () => {
                if (this.isMobile() && $('body').hasClass('sidebar-open')) this.close();
            });
            $('.sidebar-form .form-control').on('click.nichePushMenu', event => event.stopPropagation());
        }

        isMobile() { return $(window).width() <= this.options.collapseScreenSize; }

        toggle() {
            const open = this.isMobile() ? $('body').hasClass('sidebar-open') : !$('body').hasClass('sidebar-collapse');
            if (open) this.close();
            else this.open();
        }

        open() {
            if (this.isMobile()) $('body').addClass('sidebar-open');
            else $('body').removeClass('sidebar-collapse');
            $('body').trigger('expanded.pushMenu');
        }

        close() {
            if (this.isMobile()) $('body').removeClass('sidebar-open sidebar-collapse');
            else $('body').addClass('sidebar-collapse');
            $('body').trigger('collapsed.pushMenu');
        }

        expand() {
            window.clearTimeout(this.hoverTimer);
            this.hoverTimer = window.setTimeout(() => {
                $('body').removeClass('sidebar-collapse').addClass('sidebar-expanded-on-hover');
            }, this.options.expandTransitionDelay);
        }

        collapse() {
            window.clearTimeout(this.hoverTimer);
            this.hoverTimer = window.setTimeout(() => {
                $('body').removeClass('sidebar-expanded-on-hover').addClass('sidebar-collapse');
            }, this.options.expandTransitionDelay);
        }
    }

    class Tree {
        constructor(element, options) {
            this.element = element;
            this.options = options;
            element.addClass('tree').find('.treeview.active').addClass('menu-open');
            element.on('click.nicheTree', options.trigger, event => this.toggle($(event.currentTarget), event));
        }

        toggle(link, event) {
            const menu = link.next('.treeview-menu');
            const parent = link.parent();
            if (!parent.hasClass('treeview') || !menu.length) return;
            if (!this.options.followLink || link.attr('href') === '#') event.preventDefault();
            if (parent.hasClass('menu-open')) this.collapse(menu, parent);
            else this.expand(menu, parent);
        }

        expand(menu, parent) {
            if (this.options.accordion) {
                const siblings = parent.siblings('.menu-open, .active');
                this.collapse(siblings.children('.treeview-menu'), siblings);
            }
            parent.addClass('menu-open');
            menu.stop(true, true).slideDown(this.options.animationSpeed, () => this.element.trigger('expanded.tree'));
        }

        collapse(menu, parent) {
            menu.find('.menu-open, .active').removeClass('menu-open');
            parent.removeClass('menu-open');
            menu.stop(true, true).slideUp(this.options.animationSpeed, () => {
                menu.find('.treeview-menu').hide();
                this.element.trigger('collapsed.tree');
            });
        }
    }

    class ControlSidebar {
        constructor(element, options) {
            this.element = element;
            this.options = options;
            if (!element.is('[data-toggle="control-sidebar"]')) {
                element.on('click.nicheControlSidebar', event => {
                    event.preventDefault();
                    this.toggle();
                });
            }
            this.fix();
            $(window).on('resize.nicheControlSidebar', () => this.fix());
        }

        toggle() {
            this.fix();
            if ($('.control-sidebar, body').hasClass('control-sidebar-open')) this.collapse();
            else this.expand();
        }

        expand() {
            $(this.options.slide ? '.control-sidebar' : 'body').addClass('control-sidebar-open');
            this.element.trigger('expanded.controlsidebar');
        }

        collapse() {
            $('body, .control-sidebar').removeClass('control-sidebar-open');
            this.element.trigger('collapsed.controlsidebar');
        }

        fix() {
            if ($('body').hasClass('layout-boxed')) {
                $('.control-sidebar-bg').css({ position: 'absolute', height: $('.wrapper').height() });
            }
        }
    }

    Niche.definePlugin('pushMenu', PushMenu, 'lte.pushmenu', {
        collapseScreenSize: 767, expandOnHover: false, expandTransitionDelay: 200
    });
    Niche.definePlugin('tree', Tree, 'lte.tree', {
        animationSpeed: 500, accordion: true, followLink: false, trigger: '.treeview a'
    });
    Niche.definePlugin('controlSidebar', ControlSidebar, 'lte.controlsidebar', { slide: true });

    $(document).on('click.nicheNavigation', '[data-toggle="push-menu"]', function (event) {
        event.preventDefault();
        $(this).pushMenu('toggle');
    }).on('click.nicheNavigation', '[data-toggle="control-sidebar"]', function (event) {
        event.preventDefault();
        $(this).controlSidebar('toggle');
    });
    Niche.onLoad(() => {
        $('[data-toggle="push-menu"]').pushMenu();
        $('[data-widget="tree"]').tree();
    });

    $(function () {
        if (typeof $.fn.aceResponsiveMenu !== 'function') return;
        $('#respMenu').each(function () {
            if (this.dataset.nicheMenuInitialized) return;
            $(this).aceResponsiveMenu({ resizeWidth: '768', animationSpeed: 'fast', accoridonExpAll: false });
            this.dataset.nicheMenuInitialized = 'true';
        });
    });
})(jQuery, window.Niche);
