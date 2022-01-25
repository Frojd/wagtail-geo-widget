// This file must follow ES5
(function() {
    function GeocoderFieldWrap(html, _id, geocoder) {
        this.html = html;
        this.geocoder = geocoder;
    }

    GeocoderFieldWrap.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        var fieldByGeocoder = {
            "nominatim": NominatimGeocoderField,
            "google_maps": GoogleMapsGeocoderField,
        };

        var Field = fieldByGeocoder[this.geocoder];

        var geocoderField = new Field({"id": id})
        geocoderField.setState(initialState);
        return geocoderField;
    }

    window.telepath.register('wagtailgewidget.widgets.GeocoderFieldWrap', GeocoderFieldWrap);
})();
