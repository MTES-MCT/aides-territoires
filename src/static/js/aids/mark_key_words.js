$(document).ready(function() {

    divWords = $("#aid").html().split(' ');    
    aidPage = ''
    for (i = 0; i < divWords.length; i++) 
    {   
       if (divWords[i] == KEY_WORDS) {
          aidPage += ' ' + '<mark>' + divWords[i] + '</mark>';
       } else {
           aidPage += ' ' + divWords[i];           
       }
     }    
     $("#aid").html(aidPage);

});
