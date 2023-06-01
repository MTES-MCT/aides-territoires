// JS shared configurations are kept here.

var trumbowygConfig = {
    lang: 'fr',
    btnsDef: {
        image: {
            dropdown: ['insertImage', 'upload'],
            ico: 'insertImage'
        }
    },
    btns: [
        ['viewHTML'],
        ['undo', 'redo'],
        ['formatting'],
        ['strong', 'em'],
        ['link'],
        ['unorderedList', 'orderedList'],
        ['removeformat'],
        ['fullscreen']
    ],
    minimalLinks: true,
    removeformatPasted: true,
    svgPath: '/static/trumbowyg/dist/ui/icons.svg',
    plugins: {
        upload: {
            serverPath: '/upload/',
            fileFieldName: 'image'
        }
    },
    defaultLinkTarget: '_blank',
}

