TRUMBOWYG_UPLOAD_ADMIN_JS = [
    "/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js",
    "/static/jquery-resizable-dom/dist/jquery-resizable.js",
    # We are using a local version of trumbowyg.resizimg because there is
    # a bug on the upstream version. Once that bug is resolved and released,
    # we should get back to using upstream.
    # See PR : https://github.com/Alex-D/Trumbowyg/pull/1116
    # See issue : https://github.com/Alex-D/Trumbowyg/issues/1158
    "/static/js/trumbowyg-resizimg/trumbowyg.resizimg-with-canvas-fix.js",
]
