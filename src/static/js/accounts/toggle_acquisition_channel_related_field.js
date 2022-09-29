(function (exports) {

    /**
     * Enable the acquisition_channel_comment field toggling.
     */
    exports.toggleAcquisitionChannelCommentField = function (form, div) {

        var select = form.find('select#id_acquisition_channel option[value="other"]');
        var selected = select.prop('selected');
        var hasErrors = div.find('p.error').length > 0;

        if (selected || hasErrors) {
            div.addClass('fr-collapse--expanded');
        } else {
            div.removeClass('fr-collapse--expanded');
        }
    };

})(this);

$(document).ready(function () {
    // If a "source" URL parameter is set, set the 
    let searchParams = new URLSearchParams(window.location.search);
    if (searchParams.has('source')) {
        let source = searchParams.get('source');
        $("#id_acquisition_channel_comment").val(source);
    }

    // Only display acquisition_channel related field when the `other`
    // option is selected.
    var registerForm = $('form#register-form');
    var AcquisitionChannelCommentFieldDiv = $('div#acquisition-channel-comment-collapse');

    toggleAcquisitionChannelCommentField(registerForm, AcquisitionChannelCommentFieldDiv);

    registerForm.on('change', function () {
        toggleAcquisitionChannelCommentField(registerForm, AcquisitionChannelCommentFieldDiv);
    });


});
