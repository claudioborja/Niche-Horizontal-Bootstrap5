/* Collapsible boxes, todo lists and chat panes. Original template license: MIT. */
(function ($, Niche) {
    'use strict';

    class BoxWidget {
        constructor(element, options) {
            this.element = element;
            this.options = options;
            this.updateAccessibility(!element.hasClass('collapsed-box'));
            element.on('click.nicheBox', options.collapseTrigger, event => {
                event.preventDefault();
                this.toggle();
            }).on('click.nicheBox', options.removeTrigger, event => {
                event.preventDefault();
                this.remove();
            });
        }

        toggle() {
            if (this.element.hasClass('collapsed-box')) this.expand();
            else this.collapse();
        }

        updateAccessibility(expanded) {
            this.element.find(this.options.collapseTrigger).attr({
                'aria-expanded': String(expanded),
                'aria-label': expanded ? 'Collapse panel' : 'Expand panel'
            });
        }

        expand() {
            this.updateAccessibility(true);
            this.element.removeClass('collapsed-box');
            this.element.find('.box-tools .' + this.options.expandIcon)
                .removeClass(this.options.expandIcon).addClass(this.options.collapseIcon);
            this.element.find('.box-body, .box-footer').stop(true, true).slideDown(this.options.animationSpeed,
                () => this.element.trigger('expanded.boxwidget'));
        }

        collapse() {
            this.updateAccessibility(false);
            this.element.find('.box-tools .' + this.options.collapseIcon)
                .removeClass(this.options.collapseIcon).addClass(this.options.expandIcon);
            this.element.find('.box-body, .box-footer').stop(true, true).slideUp(this.options.animationSpeed, () => {
                this.element.addClass('collapsed-box').trigger('collapsed.boxwidget');
            });
        }

        remove() {
            this.element.stop(true, true).slideUp(this.options.animationSpeed, () => {
                this.element.trigger('removed.boxwidget').remove();
            });
        }
    }

    class TodoList {
        constructor(element, options) {
            this.options = options;
            element.on('change.nicheTodo ifChanged.nicheTodo', 'input:checkbox', event => this.toggle($(event.target)));
        }

        toggle(checkbox) {
            checkbox.closest('li').toggleClass('done', checkbox.prop('checked'));
            if (checkbox.prop('checked')) this.check(checkbox);
            else this.unCheck(checkbox);
        }

        check(checkbox) { this.options.onCheck.call(checkbox); }
        unCheck(checkbox) { this.options.onUnCheck.call(checkbox); }
    }

    class DirectChat {
        constructor(element) { this.element = element; }
        toggle() { this.element.closest('.direct-chat').toggleClass('direct-chat-contacts-open'); }
    }

    Niche.definePlugin('boxWidget', BoxWidget, 'lte.boxwidget', {
        animationSpeed: 500, collapseTrigger: '[data-widget="collapse"]', removeTrigger: '[data-widget="remove"]',
        collapseIcon: 'fa-minus', expandIcon: 'fa-plus', removeIcon: 'fa-times'
    });
    Niche.definePlugin('todoList', TodoList, 'lte.todolist', { onCheck: function () {}, onUnCheck: function () {} });
    Niche.definePlugin('directChat', DirectChat, 'lte.directchat', {});

    Niche.onLoad(() => {
        $('.box').boxWidget();
        $('[data-widget="todo-list"]').todoList();
    });
    $(document).on('click.nicheChat', '[data-widget="chat-pane-toggle"]', function (event) {
        event.preventDefault();
        $(this).directChat('toggle');
    });
})(jQuery, window.Niche);
