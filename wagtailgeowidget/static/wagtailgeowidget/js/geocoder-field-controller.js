// wagtailgeowidget/static/wagtailgeowidget/js/geocoder-field-controller.js

class GeocoderFieldController extends window.StimulusModule.Controller {
    static values = { geocoder: String, options: Object };

    connect() {
        let id = this.element.id;
        let geocoder = this.geocoderValue;
        let options = this.optionsValue;

        const fieldByGeocoder = {
            "nominatim": NominatimGeocoderField,
            "google_maps": GoogleMapsGeocoderField,
            "google_maps_places": GoogleMapsGeocoderPlacesField,
            "google_maps_places_new": GoogleMapsGeocoderPlacesNewField,
            "mapbox": MapboxGeocoderField,
        };

        options = Object.assign({}, options, {
            "id": id,
        });

        new fieldByGeocoder[geocoder](options);
    }
}

window.wagtail.app.register('geocoder-field', GeocoderFieldController);
