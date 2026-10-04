/* Validate each step before advancing; going back clears its validation errors. */
jQuery(function ($) {
    'use strict';
    if (typeof $.fn.steps !== 'function' || typeof $.fn.validate !== 'function') return;
    const forms = ['frmRes', 'frmInfo', 'frmLogin', 'frmMobile'].map(id => $('#' + id));
    const validators = forms.map(form => form.validate());
    const finish = () => window.alert('Wizard Completed');
    $('#demo1').steps({
        onChange: function (currentIndex, newIndex, direction) {
            const form = forms[currentIndex];
            if (!form || !form.length) return true;
            if (direction === 'forward') return form.valid();
            if (direction === 'backward') validators[currentIndex].resetForm();
            return true;
        },
        onFinish: finish
    });
    $('#demo').steps({ onFinish: finish });
});
