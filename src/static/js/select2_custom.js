function format_number_of_selected(data) {
    // Used for select2 fields.
    // Replaces the multi-line list of selected values by a line formated as such:
    // (<number of selected values>) <List, of, values, labels…>

    let labels = data.selected.map(x => x.text).join(', ')
    let count = data.selected.length
    if (labels.length > 20) {
        labels = labels.substring(0, 19) + "…";
    }
    return "(" + count + ") " + labels;

}

$(document).ready(function () {
    $.fn.select2.amd.define("NumberOfSelectedSelectionAdapter", [
        "select2/utils",
        "select2/selection/multiple",
        "select2/selection/placeholder",
        "select2/selection/eventRelay",
        "select2/selection/single",
    ],
        function (Utils, MultipleSelection, Placeholder, EventRelay, SingleSelection) {
            // custom selection adapter needed to use the format_number_of_selected function

            let adapter = Utils.Decorate(MultipleSelection, Placeholder);
            adapter = Utils.Decorate(adapter, EventRelay);

            adapter.prototype.render = function () {
                return SingleSelection.prototype.render.call(this);
            };

            adapter.prototype.update = function (data) {
                this.clear();

                let $rendered = this.$selection.find('.select2-selection__rendered');
                let noItemsSelected = data.length === 0;
                let formatted = "";

                if (noItemsSelected) {
                    formatted = this.options.get("placeholder") || "";
                } else {
                    let itemsData = {
                        selected: data || [],
                        all: this.$element.find("option") || []
                    };
                    // Pass selected and all items to display method
                    // which calls templateSelection
                    formatted = this.display(itemsData, $rendered);
                }

                $rendered.empty().append(formatted);
                $rendered.prop('title', formatted);
            };

            return adapter;
        });

    $.fn.select2.amd.define("DropdownWithSearchAdapter", [
        "select2/utils",
        "select2/dropdown",
        "select2/dropdown/attachBody",
        "select2/dropdown/search",
        "select2/dropdown/minimumResultsForSearch",
        "select2/dropdown/closeOnSelect",
    ],
        function (Utils, Dropdown, AttachBody, AttachContainer, Search, MinimumResultsForSearch, CloseOnSelect) {

            // Decorate Dropdown with Search functionalities
            let dropdownWithSearch = Utils.Decorate(Dropdown, Search);

            // Decorate the dropdown+search with necessary containers
            let adapter = Utils.Decorate(dropdownWithSearch, AttachContainer);
            adapter = Utils.Decorate(adapter, AttachBody);

            return adapter;
        });
});