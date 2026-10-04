/* Optional compatibility for integrations using the original jQuery plugin APIs. */
(function (Niche, $) {
    'use strict';
    if (!$) return;
    Niche.bridgeInstance = (element, definition, instance) => $(element).data(definition.dataKey, instance);
    Niche.bridgeEvent = (element, name) => $(element).trigger(name);
    Niche.definitions.forEach((definition, name) => {
        const previous = $.fn[name];
        function plugin(option) {
            return this.each(function () {
                let options;
                if (!Niche.getComponent(this, name)) {
                    options = Object.assign({}, $(this).data(), option && typeof option === 'object' ? option : {});
                    ['onCheck', 'onUncheck', 'onUnCheck'].forEach(key => {
                        const callback = options[key];
                        if (typeof callback === 'function') options[key] = function () { return callback.call($(this)); };
                    });
                }
                const instance = Niche.component(this, name, options);
                if (typeof option === 'string') Niche.component(this, name, option);
                Niche.bridgeInstance(this, definition, instance);
                if (name === 'tree' && !$(this).data('niche.treeBridge')) {
                    $(this).data('niche.treeBridge', true).on('click.nicheCompat', instance.options.trigger, event => {
                        if (!event.originalEvent) {
                            event.preventDefault();
                            const click = new MouseEvent('click', { bubbles: true, cancelable: true });
                            click.preventDefault(); // A synthetic jQuery click on a link does not navigate.
                            event.currentTarget.dispatchEvent(click);
                        }
                    });
                }
                if (name === 'todoList' && !$(this).data('niche.todoBridge')) {
                    $(this).data('niche.todoBridge', true).on('change.nicheCompat ifChanged.nicheCompat', 'input:checkbox', event => {
                        if (!event.originalEvent) instance.toggle(event.target);
                    });
                }
            });
        }
        plugin.Constructor = definition.Constructor;
        plugin.noConflict = () => { $.fn[name] = previous; return plugin; };
        $.fn[name] = plugin;
    });
})(window.Niche, window.jQuery);
