// This file must follow ES5
(function () {
    function GoogleMapsFieldAdapter(html, _id, options) {
        this.html = html;
        this.options = options || {};
    }

    GoogleMapsFieldAdapter.prototype.render = function (
        placeholder,
        name,
        id,
        initialState
    ) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        if (!initialState) {
            initialState = GoogleMapsField.buildLocationString(
                this.options.srid,
                this.options.defaultLocation.lng,
                this.options.defaultLocation.lat
            );
        }

        var sourceFieldData =
            GoogleMapsField.locationStringToStruct(initialState);
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
        var field = new GoogleMapsField(args);
        field.setState(initialState);
        return field;
    };

    window.telepath.register(
        "wagtailgewidget.widgets.GoogleMapsFieldAdapter",
        GoogleMapsFieldAdapter
    );
})();
