$(document).ready(function() {

    // We want to highlight the key words even whatever the form is (plural or singular)

    // create a basic singular form of KEY_WORDS string
    SINGULAR_KEY_WORDS = KEY_WORDS.split(" ")
    for (var i = 0; i < SINGULAR_KEY_WORDS.length; i++) {
        SINGULAR_KEY_WORDS[i] = SINGULAR_KEY_WORDS[i].replace(/(s\b)/,"");
    }
    SINGULAR_KEY_WORDS = SINGULAR_KEY_WORDS.join(' ')
    SINGULAR_KEY_WORDS = SINGULAR_KEY_WORDS.replace(/(\s+)/,"(<[^>]+>)*$1(<[^>]+>)*");

    // create a basic plural form of KEY_WORDS string
    PLURAL_KEY_WORDS = KEY_WORDS.split(" ")
    for (var i = 0; i < PLURAL_KEY_WORDS.length; i++) {
        PLURAL_KEY_WORDS[i] = PLURAL_KEY_WORDS[i].replace(/(\b\w+\b)/,"$&s");
    }
    PLURAL_KEY_WORDS = PLURAL_KEY_WORDS.join(' ')
    PLURAL_KEY_WORDS = PLURAL_KEY_WORDS.replace(/(\s+)/,"(<[^>]+>)*$1(<[^>]+>)*");

    KEY_WORDS = KEY_WORDS.replace(/(\s+)/,"(<[^>]+>)*$1(<[^>]+>)*");    
    textarea = $('#aid');    
    newTextArea = '';

    if (KEY_WORDS) {    

        newTextArea = textarea.html().replace(/(<mark>|<\/mark>)/igm, "");    
        textarea.html(newTextArea);     
            
        query = new RegExp("("+KEY_WORDS+")", "gim");
        query_plural_form = new RegExp("("+PLURAL_KEY_WORDS+")", "gim");
        query_singular_form = new RegExp("("+SINGULAR_KEY_WORDS+")", "gim");
        
        newtext= textarea.html().replace(query, "<mark>$1</mark>");
        newtext= newtext.replace(/(<mark>[^<>]*)((<[^>]+>)+)([^<>]*<\/mark>)/,"</mark><mark>");    
        textarea.html(newtext);

        newtext= textarea.html().replace(query_plural_form, "<mark>$1</mark>");
        newtext= newtext.replace(/(<mark>[^<>]*)((<[^>]+>)+)([^<>]*<\/mark>)/,"</mark><mark>");    
        textarea.html(newtext);

        if (KEY_WORDS !== SINGULAR_KEY_WORDS) {
            newtext= textarea.html().replace(query_singular_form, "<mark>$1</mark>");
            newtext= newtext.replace(/(<mark>[^<>]*)((<[^>]+>)+)([^<>]*<\/mark>)/,"</mark><mark>");    
            textarea.html(newtext);   
        }
    }  
});
