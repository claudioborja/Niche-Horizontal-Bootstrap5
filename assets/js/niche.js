/* Niche component registry. Load before niche/layout.js, navigation.js and widgets.js.
 * Adapted from the original template's MIT-licensed layout plugins.
 * @license MIT <https://opensource.org/licenses/MIT>
 */
(function (window, $) {
    'use strict';

    function definePlugin(name, Constructor, dataKey, defaults) {
        const previousPlugin = $.fn[name];
        function plugin(option) {
            return this.each(function () {
                const element = $(this);
                let instance = element.data(dataKey);
                if (!instance) {
                    const options = $.extend({}, defaults, element.data(),
                        typeof option === 'object' && option !== null ? option : {});
                    instance = new Constructor(element, options);
                    element.data(dataKey, instance);
                }
                if (typeof option === 'string') {
                    if (typeof instance[option] !== 'function') throw new Error('No method named ' + option);
                    instance[option]();
                }
            });
        }
        plugin.Constructor = Constructor;
        plugin.noConflict = function () {
            $.fn[name] = previousPlugin;
            return plugin;
        };
        $.fn[name] = plugin;
    }

    function onLoad(callback) {
        if (document.readyState === 'complete') callback();
        else window.addEventListener('load', callback, { once: true });
    }

    window.Niche = { definePlugin, onLoad };
})(window, jQuery);
