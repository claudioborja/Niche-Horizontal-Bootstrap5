/* Native collapsible boxes, todo lists and chat panes. Original template license: MIT. */
(function (Niche) {
    'use strict';
    class BoxWidget {
        constructor(element, options) {
            this.element = element; this.options = options;
            this.expanded = !element.classList.contains('collapsed-box');
            this.updateAccessibility(this.expanded);
            element.addEventListener('click', event => {
                const button = event.target.closest(options.collapseTrigger + ', ' + options.removeTrigger);
                if (!button || button.closest('.box') !== element) return;
                event.preventDefault();
                if (button.matches(options.collapseTrigger)) this.toggle();
                else this.remove();
            });
        }
        toggle() { if (this.expanded) this.collapse(); else this.expand(); }
        updateAccessibility(expanded) {
            this.element.querySelectorAll(this.options.collapseTrigger).forEach(button => {
                button.setAttribute('aria-expanded', String(expanded));
                button.setAttribute('aria-label', expanded ? 'Collapse panel' : 'Expand panel');
            });
        }
        setExpanded(expanded) {
            this.expanded = expanded;
            this.updateAccessibility(expanded);
            if (expanded) this.element.classList.remove('collapsed-box');
            const oldIcon = expanded ? this.options.expandIcon : this.options.collapseIcon;
            const newIcon = expanded ? this.options.collapseIcon : this.options.expandIcon;
            this.element.querySelectorAll('.box-tools .' + oldIcon).forEach(icon => {
                icon.classList.remove(oldIcon); icon.classList.add(newIcon);
            });
            const panels = Array.from(this.element.children).filter(node => node.matches('.box-body, .box-footer'));
            let pending = panels.length;
            const finish = () => {
                if (this.expanded !== expanded) return;
                this.element.classList.toggle('collapsed-box', !expanded);
                Niche.emit(this.element, expanded ? 'expanded.boxwidget' : 'collapsed.boxwidget');
            };
            if (!pending) finish();
            panels.forEach(panel => Niche.slide(panel, expanded, this.options.animationSpeed, () => {
                if (!--pending) finish();
            }));
        }
        expand() { this.setExpanded(true); }
        collapse() { this.setExpanded(false); }
        remove() {
            Niche.slide(this.element, false, this.options.animationSpeed, () => {
                Niche.emit(this.element, 'removed.boxwidget'); this.element.remove();
            });
        }
    }
    class TodoList {
        constructor(element, options) {
            this.options = options;
            element.addEventListener('change', event => { if (event.target.matches('input[type=checkbox]')) this.toggle(event.target); });
            element.addEventListener('ifChanged', event => { if (event.target.matches('input[type=checkbox]')) this.toggle(event.target); });
        }
        toggle(checkbox) {
            checkbox.closest('li')?.classList.toggle('done', checkbox.checked);
            if (checkbox.checked) this.check(checkbox); else this.unCheck(checkbox);
        }
        check(checkbox) { this.options.onCheck.call(checkbox); }
        unCheck(checkbox) { this.options.onUnCheck.call(checkbox); }
    }
    class DirectChat {
        constructor(element) { this.element = element; }
        toggle() { this.element.closest('.direct-chat')?.classList.toggle('direct-chat-contacts-open'); }
    }
    Niche.defineComponent('boxWidget', BoxWidget, 'lte.boxwidget', {
        animationSpeed: 500, collapseTrigger: '[data-widget="collapse"]', removeTrigger: '[data-widget="remove"]',
        collapseIcon: 'fa-minus', expandIcon: 'fa-plus', removeIcon: 'fa-times'
    });
    Niche.defineComponent('todoList', TodoList, 'lte.todolist', { onCheck() {}, onUnCheck() {} });
    Niche.defineComponent('directChat', DirectChat, 'lte.directchat', {});
    Niche.onLoad(() => {
        document.querySelectorAll('.box').forEach(element => Niche.component(element, 'boxWidget'));
        document.querySelectorAll('[data-widget="todo-list"]').forEach(element => Niche.component(element, 'todoList'));
    });
    document.addEventListener('click', event => {
        const button = event.target.closest('[data-widget="chat-pane-toggle"]');
        if (button) { event.preventDefault(); Niche.component(button, 'directChat', 'toggle'); }
    });
})(window.Niche);
