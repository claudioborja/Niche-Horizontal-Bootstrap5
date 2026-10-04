/* Native horizontal navigation, sidebar toggles and trees. Original template license: MIT. */
(function (Niche) {
    'use strict';
    class PushMenu {
        constructor(element, options) {
            this.options = options;
            if (options.expandOnHover || document.body.matches('.sidebar-mini.fixed')) {
                document.querySelectorAll('.main-sidebar').forEach(sidebar => {
                    sidebar.addEventListener('mouseenter', () => {
                        if (document.body.matches('.sidebar-mini.sidebar-collapse') && !this.isMobile()) this.expand();
                    });
                    sidebar.addEventListener('mouseleave', () => {
                        if (document.body.classList.contains('sidebar-expanded-on-hover')) this.collapse();
                    });
                });
                document.body.classList.add('sidebar-mini-expand-feature');
            }
            document.querySelectorAll('.content-wrapper').forEach(content => content.addEventListener('click', () => {
                if (this.isMobile() && document.body.classList.contains('sidebar-open')) this.close();
            }));
            document.querySelectorAll('.sidebar-form .form-control').forEach(input => input.addEventListener('click', event => event.stopPropagation()));
        }
        isMobile() { return window.innerWidth <= this.options.collapseScreenSize; }
        toggle() {
            const opened = this.isMobile() ? document.body.classList.contains('sidebar-open') : !document.body.classList.contains('sidebar-collapse');
            if (opened) this.close(); else this.open();
        }
        open() {
            if (this.isMobile()) document.body.classList.add('sidebar-open');
            else document.body.classList.remove('sidebar-collapse');
            Niche.emit(document.body, 'expanded.pushMenu');
        }
        close() {
            if (this.isMobile()) document.body.classList.remove('sidebar-open', 'sidebar-collapse');
            else document.body.classList.add('sidebar-collapse');
            Niche.emit(document.body, 'collapsed.pushMenu');
        }
        expand() {
            window.clearTimeout(this.hoverTimer);
            this.hoverTimer = window.setTimeout(() => {
                document.body.classList.remove('sidebar-collapse');
                document.body.classList.add('sidebar-expanded-on-hover');
            }, this.options.expandTransitionDelay);
        }
        collapse() {
            window.clearTimeout(this.hoverTimer);
            this.hoverTimer = window.setTimeout(() => {
                document.body.classList.remove('sidebar-expanded-on-hover');
                document.body.classList.add('sidebar-collapse');
            }, this.options.expandTransitionDelay);
        }
    }
    class Tree {
        constructor(element, options) {
            this.element = element; this.options = options;
            element.classList.add('tree');
            element.querySelectorAll('.treeview.active').forEach(item => item.classList.add('menu-open'));
            element.addEventListener('click', event => {
                const link = event.target.closest(options.trigger);
                if (link && element.contains(link)) this.toggle(link, event);
            });
        }
        toggle(link, event) {
            const menu = link.nextElementSibling;
            const parent = link.parentElement;
            if (!parent.classList.contains('treeview') || !menu?.matches('.treeview-menu')) return;
            if (!this.options.followLink || link.getAttribute('href') === '#') event.preventDefault();
            if (parent.classList.contains('menu-open')) this.collapse(menu, parent);
            else this.expand(menu, parent);
        }
        expand(menu, parent) {
            if (this.options.accordion) Array.from(parent.parentElement.children).forEach(sibling => {
                if (sibling !== parent && sibling.matches('.menu-open, .active')) {
                    const child = sibling.querySelector(':scope > .treeview-menu');
                    if (child) this.collapse(child, sibling);
                }
            });
            parent.classList.add('menu-open');
            parent.querySelector(':scope > a')?.setAttribute('aria-expanded', 'true');
            Niche.slide(menu, true, this.options.animationSpeed, () => Niche.emit(this.element, 'expanded.tree'));
        }
        collapse(menu, parent) {
            parent.classList.remove('menu-open');
            parent.querySelector(':scope > a')?.setAttribute('aria-expanded', 'false');
            menu.querySelectorAll('.menu-open, .active').forEach(item => item.classList.remove('menu-open', 'active'));
            menu.querySelectorAll('.treeview-menu').forEach(child => { child.style.display = 'none'; });
            Niche.slide(menu, false, this.options.animationSpeed, () => Niche.emit(this.element, 'collapsed.tree'));
        }
    }
    class ControlSidebar {
        constructor(element, options) {
            this.element = element; this.options = options;
            if (!element.matches('[data-toggle="control-sidebar"]')) element.addEventListener('click', event => {
                event.preventDefault(); this.toggle();
            });
            this.fix();
            window.addEventListener('resize', () => this.fix());
        }
        toggle() {
            this.fix();
            if (document.querySelector('.control-sidebar-open')) this.collapse(); else this.expand();
        }
        expand() {
            document.querySelectorAll(this.options.slide ? '.control-sidebar' : 'body').forEach(node => node.classList.add('control-sidebar-open'));
            this.element.setAttribute('aria-expanded', 'true');
            Niche.emit(this.element, 'expanded.controlsidebar');
        }
        collapse() {
            document.querySelectorAll('body, .control-sidebar').forEach(node => node.classList.remove('control-sidebar-open'));
            this.element.setAttribute('aria-expanded', 'false');
            Niche.emit(this.element, 'collapsed.controlsidebar');
        }
        fix() {
            if (document.body.classList.contains('layout-boxed')) document.querySelectorAll('.control-sidebar-bg').forEach(node => {
                node.style.position = 'absolute';
                node.style.height = (document.querySelector('.wrapper')?.getBoundingClientRect().height || 0) + 'px';
            });
        }
    }
    class HorizontalMenu {
        constructor(menu, options) {
            this.element = menu; this.options = options;
            this.toggleButton = document.getElementById('menu-btn');
            this.originalStyle = menu.dataset.menuStyle || 'horizontal';
            this.branches = Array.from(menu.querySelectorAll('li > a')).filter(link => link.nextElementSibling?.tagName === 'UL');
            this.branches.forEach((link, index) => {
                const submenu = link.nextElementSibling;
                submenu.classList.add('sub-menu');
                submenu.id = submenu.id || 'niche-submenu-' + index;
                link.setAttribute('aria-controls', submenu.id);
                link.setAttribute('aria-expanded', 'false');
                if (link.getAttribute('href') === '#') link.setAttribute('role', 'button');
                if (!link.querySelector('.arrow')) {
                    const arrow = document.createElement('span');
                    arrow.className = 'arrow'; arrow.setAttribute('aria-hidden', 'true'); link.append(arrow);
                }
                link.parentElement.addEventListener('pointerenter', event => {
                    if (!this.collapsed && event.pointerType !== 'touch') this.open(link);
                });
                link.parentElement.addEventListener('pointerleave', () => {
                    if (!this.collapsed && !link.parentElement.contains(document.activeElement)) this.close(link);
                });
            });
            menu.addEventListener('click', event => {
                const link = event.target.closest('a');
                if (!link || !menu.contains(link)) return;
                if (this.branches.includes(link)) {
                    if (link.getAttribute('href') === '#') event.preventDefault();
                    if (link.getAttribute('aria-expanded') === 'true') this.close(link); else this.open(link);
                }
            });
            menu.addEventListener('focusin', event => {
                const link = event.target.closest('a');
                if (!this.collapsed && this.branches.includes(link)) this.open(link);
            });
            menu.addEventListener('focusout', () => window.setTimeout(() => {
                if (this.collapsed) return;
                this.branches.forEach(link => {
                    if (!link.parentElement.contains(document.activeElement) && !link.parentElement.matches(':hover')) this.close(link);
                });
            }, 0));
            menu.addEventListener('keydown', event => this.keydown(event));
            this.toggleButton?.addEventListener('click', () => this.toggle());
            this.breakpoint = window.matchMedia('(max-width: ' + options.resizeWidth + 'px)');
            this.breakpoint.addEventListener('change', () => this.resize());
            this.resize();
            menu.dataset.nicheMenuInitialized = 'true';
        }
        open(link) {
            if (!this.options.accoridonExpAll) Array.from(link.parentElement.parentElement.children).forEach(sibling => {
                const trigger = sibling.querySelector(':scope > a');
                if (trigger !== link && this.branches.includes(trigger)) this.close(trigger);
            });
            link.parentElement.classList.add('menu-active');
            link.nextElementSibling.classList.add('slide');
            link.setAttribute('aria-expanded', 'true');
            Niche.slide(link.nextElementSibling, true, this.options.animationSpeed);
        }
        close(link, duration = this.options.animationSpeed) {
            const submenu = link.nextElementSibling;
            link.parentElement.classList.remove('menu-active');
            link.setAttribute('aria-expanded', 'false');
            submenu.classList.remove('slide');
            this.branches.filter(child => submenu.contains(child)).forEach(child => {
                child.parentElement.classList.remove('menu-active'); child.setAttribute('aria-expanded', 'false');
                child.nextElementSibling.classList.remove('slide'); Niche.slide(child.nextElementSibling, false, 0);
            });
            Niche.slide(submenu, false, duration);
        }
        toggle() {
            const visible = this.element.classList.contains('hide-menu');
            this.element.classList.toggle('hide-menu', !visible);
            Niche.slide(this.element, visible, this.options.animationSpeed);
            this.toggleButton?.setAttribute('aria-expanded', String(visible));
        }
        resize() {
            this.collapsed = this.breakpoint.matches || this.originalStyle === 'accordion';
            this.branches.forEach(link => this.close(link, 0));
            this.element.classList.toggle('collapse', this.collapsed);
            this.element.classList.toggle('hide-menu', this.breakpoint.matches);
            Niche.slide(this.element, !this.breakpoint.matches, 0);
            if (!this.collapsed) this.element.style.display = '';
            this.element.dataset.menuStyle = this.breakpoint.matches ? '' : this.originalStyle;
            const toggleContainer = this.toggleButton?.closest('.menu-toggle');
            if (toggleContainer) toggleContainer.style.display = this.breakpoint.matches ? 'block' : 'none';
            this.toggleButton?.setAttribute('aria-expanded', String(!this.breakpoint.matches));
        }
        keydown(event) {
            const link = event.target.closest('a');
            if (!link) return;
            if (event.key === ' ' && this.branches.includes(link)) { event.preventDefault(); link.click(); }
            else if (event.key === 'ArrowDown' && this.branches.includes(link)) {
                event.preventDefault(); this.open(link); link.nextElementSibling.querySelector('a')?.focus();
            } else if (event.key === 'Escape') {
                const parent = link.closest('ul.sub-menu');
                const trigger = parent ? parent.previousElementSibling : link;
                if (this.branches.includes(trigger)) { event.preventDefault(); trigger.focus(); this.close(trigger); }
            }
        }
    }
    Niche.defineComponent('pushMenu', PushMenu, 'lte.pushmenu', { collapseScreenSize: 767, expandOnHover: false, expandTransitionDelay: 200 });
    Niche.defineComponent('tree', Tree, 'lte.tree', { animationSpeed: 500, accordion: true, followLink: false, trigger: '.treeview a' });
    Niche.defineComponent('controlSidebar', ControlSidebar, 'lte.controlsidebar', { slide: true });
    Niche.defineComponent('horizontalMenu', HorizontalMenu, 'niche.horizontalMenu', { resizeWidth: 768, animationSpeed: 200, accoridonExpAll: false });
    document.addEventListener('click', event => {
        const button = event.target.closest('[data-toggle="push-menu"], [data-toggle="control-sidebar"]');
        if (!button) return;
        event.preventDefault();
        Niche.component(button, button.matches('[data-toggle="push-menu"]') ? 'pushMenu' : 'controlSidebar', 'toggle');
    });
    Niche.onLoad(() => {
        document.querySelectorAll('[data-toggle="push-menu"]').forEach(element => Niche.component(element, 'pushMenu'));
        document.querySelectorAll('[data-widget="tree"]').forEach(element => Niche.component(element, 'tree'));
    });
    Niche.onReady(() => document.querySelectorAll('#respMenu').forEach(element => Niche.component(element, 'horizontalMenu')));
})(window.Niche);
