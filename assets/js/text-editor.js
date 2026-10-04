/* Summernote demos and delegated edit/save actions, initialized after Bootstrap. */
jQuery(function ($) {
    'use strict';
    if (typeof $.fn.summernote !== 'function') return;

    $('#summernote').summernote({
        height: 300, placeholder: 'Hello default Summernote',
        minHeight: null, maxHeight: null, focus: false
    });
    $('#compose-textarea').summernote({
        height: 300, minHeight: null, maxHeight: null, focus: true,
        toolbar: [
            ['style', ['style']], ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']], ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']], ['table', ['table']],
            ['insert', ['link', 'picture', 'video']], ['view', ['fullscreen', 'help']]
        ]
    });
    document.addEventListener('click', function (event) {
        const button = event.target.closest('[data-editor-action]');
        if (!button) return;
        const editor = $('.click2edit');
        if (button.dataset.editorAction === 'edit' && !editor.data('summernote')) {
            editor.summernote({ focus: true });
        } else if (button.dataset.editorAction === 'save' && editor.data('summernote')) {
            editor.summernote('destroy');
        }
    });
});
