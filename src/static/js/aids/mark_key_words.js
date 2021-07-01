$(document).ready(function() {

    KEY_WORDS = KEY_WORDS.replace(/(\s+)/,"(<[^>]+>)*$1(<[^>]+>)*");    
    textarea = $('#aid');    
    newTextArea = '';
    
    if (KEY_WORDS) {    

        newTextArea = textarea.html().replace(/(<mark>|<\/mark>)/igm, "");    
        textarea.html(newTextArea);     
            
        query = new RegExp("("+KEY_WORDS+")", "gim");    
        newtext= textarea.html().replace(query, "<mark>$1</mark>");    
        newtext= newtext.replace(/(<mark>[^<>]*)((<[^>]+>)+)([^<>]*<\/mark>)/,"</mark><mark>");    

        textarea.html(newtext);     
    }  
});
