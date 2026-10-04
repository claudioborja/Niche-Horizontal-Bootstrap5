/* File selection demos; connect FilePond.server to an API for persistent uploads. */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    if (!window.FilePond) return;
    FilePond.registerPlugin(FilePondPluginImagePreview, FilePondPluginFileValidateSize);
    document.querySelectorAll('input.filepond').forEach(function (input) {
        var removable = input.dataset.showRemove !== 'false';
        var options = {
            allowMultiple: input.multiple,
            disabled: input.disabled,
            allowRemove: removable,
            allowReplace: removable,
            instantUpload: false,
            allowProcess: false,
            allowRevert: false,
            credits: false,
            labelIdle: 'Drag & Drop your files or <span class="filepond--label-action">Browse</span>'
        };
        if (input.dataset.maxFileSize) options.maxFileSize = input.dataset.maxFileSize;
        if (input.dataset.defaultFile) options.files = [input.dataset.defaultFile];
        var pond = FilePond.create(input, options);
        if (input.dataset.height) pond.element.style.height = Number(input.dataset.height) + 'px';
    });
});
