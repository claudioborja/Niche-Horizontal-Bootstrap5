/* Local Jodit demos and edit/save actions; no jQuery bridge or remote services. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    const editors = new WeakMap();
    function create(element, focus) {
        if (editors.has(element)) return editors.get(element);
        const editor = Jodit.make(element, {
            height: 300, language: 'en', autofocus: focus,
            placeholder: 'Write your text here...',
            sourceEditor: 'area', beautifyHTML: false,
            uploader: { insertImageAsBase64URI: true },
            imageProcessor: { replaceDataURIToBlobIdInView: false },
            buttons: ['source', '|', 'bold', 'italic', 'underline', 'eraser', '|',
                'font', 'fontsize', 'brush', 'paragraph', '|', 'ul', 'ol', 'align', '|',
                'link', 'image', 'video', 'table', '|', 'undo', 'redo', 'fullsize'],
            buttonsMD: ['source', 'bold', 'italic', 'underline', 'brush', 'paragraph',
                'ul', 'ol', 'link', 'image', 'table', 'undo', 'redo', 'fullsize'],
            buttonsSM: ['bold', 'italic', 'ul', 'link', 'image', 'dots'],
            buttonsXS: ['bold', 'italic', 'image', 'dots']
        });
        editor.editor.setAttribute('aria-label', element.id === 'compose-textarea' ? 'Message body' : 'Rich text editor');
        editors.set(element, editor);
        return editor;
    }
    document.querySelectorAll('#rich-text-editor, #compose-textarea').forEach(function (element) {
        create(element, false);
    });
    document.addEventListener('click', function (event) {
        const button = event.target.closest('[data-editor-action]');
        if (!button) return;
        document.querySelectorAll('.click2edit').forEach(function (element) {
            if (button.dataset.editorAction === 'edit') {
                create(element, true);
            } else if (button.dataset.editorAction === 'save' && editors.has(element)) {
                const editor = editors.get(element);
                const html = editor.value;
                editor.destruct();
                element.innerHTML = html;
                editors.delete(element);
            }
        });
    });
});
