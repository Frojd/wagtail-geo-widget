// This file must follow ES5
(function () {
    function GeocoderFieldWrap(html, geocoder, translations, params) {
        this.html = html;

        // In Wagtail < 7.1 argument 2 was id
        // TODO: Remove when Wagtail 6 is EOL
        if (arguments[1] === "__ID__") {
            geocoder= arguments[2]
            translations = arguments[3]
            params = arguments[4]
        }

        this.geocoder = geocoder;
        this.translations = translations;
        this.params = params;
    }

    GeocoderFieldWrap.prototype.render = function (
        placeholder,
        name,
        id,
        initialState
    ) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        var fieldByGeocoder = {
            nominatim: NominatimGeocoderField,
            google_maps: GoogleMapsGeocoderField,
            google_maps_places: GoogleMapsGeocoderPlacesField,
            google_maps_places_new: GoogleMapsGeocoderPlacesNewField,
            mapbox: MapboxGeocoderField,
        };

        var Field = fieldByGeocoder[this.geocoder];

        var geocoderField = new Field({
            id: id,
            translations: this.translations,
            params: this.params,
        });
        geocoderField.setState(initialState);
        return geocoderField;
    };

    window.telepath.register(
        "wagtailgewidget.widgets.GeocoderFieldWrap",
        GeocoderFieldWrap
    );
})();
