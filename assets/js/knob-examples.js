/* Gauge configurations and infinite-dial example. */
jQuery(function ($) {
    'use strict';
    if (typeof $.fn.knob !== 'function') return;
    const gaugeDescriptions = new WeakMap();
    function describeGauge(input, value) {
        const description = gaugeDescriptions.get(input);
        if (!description) return;
        description.textContent = 'Value: ' + value + '. Range: ' + (input.dataset.min || 0) + ' to ' + (input.dataset.max || 100) + '.';
    }
    $('.knob').each(function (index) {
        const description = document.createElement('p');
        description.id = 'niche-gauge-value-' + index;
        description.className = 'form-text';
        gaugeDescriptions.set(this, description);
        this.setAttribute('aria-describedby', [this.getAttribute('aria-describedby'), description.id].filter(Boolean).join(' '));
        describeGauge(this, this.value);
    });

    $('.knob').knob({
        change: function (value) { describeGauge(this.$[0], value); },
        release: function (value) { describeGauge(this.$[0], value); },
        draw: function () {
            if (this.$.data('skin') !== 'tron') return;
            this.cursorExt = 0.3;
            const currentArc = this.arc(this.cv);
            const context = this.g;
            const radius = this.radius - this.lineWidth;
            context.lineWidth = this.lineWidth;

            if (this.o.displayPrevious) {
                const previousArc = this.arc(this.v);
                context.beginPath();
                context.strokeStyle = this.pColor;
                context.arc(this.xy, this.xy, radius, previousArc.s, previousArc.e, previousArc.d);
                context.stroke();
            }
            context.beginPath();
            context.strokeStyle = this.o.fgColor;
            context.arc(this.xy, this.xy, radius, currentArc.s, currentArc.e, currentArc.d);
            context.stroke();
            context.lineWidth = 2;
            context.beginPath();
            context.strokeStyle = this.o.fgColor;
            context.arc(this.xy, this.xy, radius + 1 + this.lineWidth * 2 / 3, 0, 2 * Math.PI, false);
            context.stroke();
            return false;
        }
    });
    $('.knob').each(function () {
        this.parentElement.after(gaugeDescriptions.get(this));
        this.parentElement.querySelectorAll('canvas').forEach(canvas => canvas.setAttribute('aria-hidden', 'true'));
        $(this).on('change', () => describeGauge(this, this.value));
    });

    let previousValue;
    let increasing = false;
    let decreasing = false;
    let count = 0;
    function updateCount(change) {
        count += change;
        $('div.idir').show().text(change > 0 ? '+' : '-').fadeOut();
        $('div.ival').text(count);
    }
    $('input.infinite').knob({
        min: 0, max: 20, stopper: false,
        change: function () {
            if (previousValue > this.cv) {
                if (increasing) {
                    updateCount(-1);
                    increasing = false;
                } else {
                    increasing = true;
                    decreasing = false;
                }
            } else if (previousValue < this.cv) {
                if (decreasing) {
                    updateCount(1);
                    decreasing = false;
                } else {
                    decreasing = true;
                    increasing = false;
                }
            }
            previousValue = this.cv;
        }
    });
});
