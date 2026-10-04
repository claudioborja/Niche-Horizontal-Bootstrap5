/* Validate each step before advancing; going back clears its validation errors. */
jQuery(function ($) {
    'use strict';
    if (typeof $.fn.steps !== 'function' || typeof $.fn.validate !== 'function') return;
    const forms = ['frmRes', 'frmInfo', 'frmLogin', 'frmMobile'].map(id => $('#' + id));
    const validators = forms.map(form => form.validate({
        errorElement: 'span',
        errorClass: 'invalid-feedback',
        messages: Object.fromEntries(form.find('[required]').get().map(field => {
            const label = document.querySelector('label[for="' + field.id + '"]');
            const name = (label ? label.textContent : field.getAttribute('aria-label') || field.name).trim().replace(/\s*:\s*$/, '');
            return [field.name, { required: 'Complete the ' + name.toLowerCase() + ' field.', email: 'Enter a valid email address, such as name@example.com.' }];
        })),
        highlight: function (element) { element.classList.add('is-invalid'); },
        unhighlight: function (element) { element.classList.remove('is-invalid'); },
        errorPlacement: function (error, element) { error.insertAfter(element); }
    }));
    const finish = () => window.alert('Wizard Completed');
    $('#demo1').steps({
        onChange: function (currentIndex, newIndex, direction) {
            const form = forms[currentIndex];
            if (!form || !form.length) return true;
            if (direction === 'forward') {
                const valid = form.valid();
                if (!valid && validators[currentIndex].errorList.length) {
                    validators[currentIndex].errorList[0].element.focus();
                }
                return valid;
            }
            if (direction === 'backward') {
                validators[currentIndex].resetForm();
                form.find('.is-invalid').removeClass('is-invalid');
            }
            return true;
        },
        onFinish: finish
    });
    $('#demo').steps({ onFinish: finish });
});
