/* Native Niche component registry and shared browser helpers. Original template license: MIT. */
(function (window) {
    'use strict';
    const definitions = new Map();
    const animations = new WeakMap();
    function dataOptions(element) {
        return Object.fromEntries(Object.entries(element.dataset).map(([key, value]) => {
            try { return [key, JSON.parse(value)]; } catch (_) { return [key, value]; }
        }));
    }
    function defineComponent(name, Constructor, dataKey, defaults = {}) {
        definitions.set(name, { Constructor, dataKey, defaults, instances: new WeakMap() });
    }
    function getComponent(element, name) {
        if (typeof element === 'string') element = document.querySelector(element);
        return element ? definitions.get(name)?.instances.get(element) : undefined;
    }
    function component(element, name, option) {
        if (typeof element === 'string') element = document.querySelector(element);
        if (!element) return undefined;
        const definition = definitions.get(name);
        if (!definition) throw new Error('Unknown component: ' + name);
        let instance = definition.instances.get(element);
        if (!instance) {
            const options = Object.assign({}, definition.defaults, dataOptions(element),
                typeof option === 'object' && option !== null ? option : {});
            instance = new definition.Constructor(element, options);
            definition.instances.set(element, instance);
            window.Niche.bridgeInstance?.(element, definition, instance);
        }
        if (typeof option === 'string') {
            if (typeof instance[option] !== 'function') throw new Error('No method named ' + option);
            instance[option]();
        }
        return instance;
    }
    function onReady(callback) {
        if (document.readyState !== 'loading') callback();
        else document.addEventListener('DOMContentLoaded', callback, { once: true });
    }
    function onLoad(callback) {
        if (document.readyState === 'complete') callback();
        else window.addEventListener('load', callback, { once: true });
    }
    function emit(element, name) {
        element.dispatchEvent(new CustomEvent(name, { bubbles: true }));
        window.Niche.bridgeEvent?.(element, name);
    }
    function slide(element, visible, duration = 200, complete = () => {}) {
        if (typeof duration !== 'number') duration = { fast: 200, slow: 600 }[duration] ?? Number(duration);
        if (!Number.isFinite(duration) || duration < 0) duration = 200;
        const previous = animations.get(element);
        const startHeight = element.getBoundingClientRect().height;
        if (previous) {
            previous.animation.cancel();
            element.style.overflow = previous.overflow;
            animations.delete(element);
        }
        if (visible) {
            element.style.display = '';
            if (getComputedStyle(element).display === 'none') element.style.display = 'block';
        }
        const finish = () => {
            if (!visible) element.style.display = 'none';
            complete();
        };
        if (!duration || window.matchMedia('(prefers-reduced-motion: reduce)').matches || !element.animate) {
            finish();
            return;
        }
        const overflow = element.style.overflow;
        element.style.overflow = 'hidden';
        const animation = element.animate([
            { height: startHeight + 'px', opacity: visible && !startHeight ? 0 : 1 },
            { height: (visible ? element.scrollHeight : 0) + 'px', opacity: visible ? 1 : 0 }
        ], { duration, easing: 'ease-out' });
        animations.set(element, { animation, overflow });
        animation.finished.then(() => {
            if (animations.get(element)?.animation !== animation) return;
            animations.delete(element);
            element.style.overflow = overflow;
            finish();
        }).catch(() => {}); // A new toggle can cancel the preceding animation.
    }
    window.Niche = { defineComponent, component, getComponent, definitions, onReady, onLoad, emit, slide };
})(window);
