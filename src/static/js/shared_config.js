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

function show_number_of_selected() {
    // Used for select2 fields.
    // Replaces the multi-line list of selected values by a line formated as such:
    // (<number of selected values>) <List, of, values, labels…>
    let uldiv = $(this).siblings('span.select2').find('ul')
    let values = $(this).select2('data')
    let count = values.length

    let labels = values.map(x => x.text).join(', ')
    if (labels.length > 20) {
        labels = labels.substring(0, 19) + "…";
    }

    if (count == 0) {
        uldiv.removeAttr('value')
    } else {
        uldiv.html("<li> (" + count + ") " + labels + "</li>")
    }
}