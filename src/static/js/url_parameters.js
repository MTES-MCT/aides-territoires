function set_param_value(param, value) {
    /* update or remove a GET parameter from the current URL */
    if ('URLSearchParams' in window) {
        let searchParams = new URLSearchParams(window.location.search);
        if (value) {
            searchParams.set(param, value);
        } else {
            searchParams.delete(param);
        }
        window.location.search = searchParams.toString();
    }
}