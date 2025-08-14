// This file must follow ES5
(function () {
    function LeafletFieldAdapter(html, options) {
        this.html = html;

        // In Wagtail < 7.1 argument 2 was id
        // TODO: Remove when Wagtail 6 is EOL
        if (arguments[1] === "__ID__") {
            options = arguments[2]
        }

        this.options = options || {};
    }

    LeafletFieldAdapter.prototype.render = function (
        placeholder,
        name,
        id,
        initialState
    ) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        if (!initialState) {
            initialState = LeafletField.buildLocationString(
                this.options.srid,
                this.options.defaultLocation.lng,
                this.options.defaultLocation.lat
            );
        }

        var sourceFieldData = LeafletField.locationStringToStruct(initialState);
        var namespace = id.split("-").slice(0, -1).join("-");
        namespace = namespace + "-";

        var addressSelector = this.options.addressField;
        if (addressSelector) {
            addressSelector = "#" + namespace + addressSelector;
        }

        var zoomSelector = this.options.zoomField;
        if (zoomSelector) {
            zoomSelector = "#" + namespace + zoomSelector;
        }

        var args = Object.assign({}, this.options, {
            id: id,
            addressSelector: addressSelector,
            zoomSelector: zoomSelector,
        });
        args = Object.assign({}, args, sourceFieldData);
        var field = new LeafletField(args);
        field.setState(initialState);
        return field;
    };

    window.telepath.register(
        "wagtailgewidget.widgets.LeafletFieldAdapter",
        LeafletFieldAdapter
    );
})();
