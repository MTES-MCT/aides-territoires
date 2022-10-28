/**
 * This is an override of django's default `jquery.init.js` file.
 *
 * By default, the django admin loads jquery in a custom `django.jQuery`
 * namespace so the `$` and `jQuery` variables are not populated.
 *
 * This does not suit us since we are using plugins (Trumbowyg, notably) that
 * rely on the `jQuery` variable being populated.
 *
 * Therefore, we have two choices:
 *  1) loading a duplicate version of jquery to populate the `jQuery`
 *     variable or…
 *  2) preventing Django to override it in the first place.
 *
 * See jQuery's api for more info:
 * https://api.jquery.com/jQuery.noConflict/
 */

var django = django || {};
django.jQuery = jQuery.noConflict(false);
