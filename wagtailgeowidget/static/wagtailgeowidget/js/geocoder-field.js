// This file must follow ES5
"use strict";

function GeocoderField(options) {
    var self = this;
    var id = options.id;
    var $el = $("#" + id);

    this.translations = options.translations;
    this.field = $el;
    this.delayTime = 1000;

    $el.on("input", function (_e) {
        clearTimeout(self._timeoutId);

        var query = $(this).val();

        if (query === "") {
            return;
        }

        self._timeoutId = setTimeout(function () {
            self.geocodeSearch(query);
        }, self.delayTime);
    });

    $el.on("keydown", function (e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            e.stopPropagation();
        }
    });
}

GeocoderField.prototype.focus = function () {
    this.field.focus();
};

GeocoderField.prototype.setState = function (newState) {
    this.field.val(newState);
};

GeocoderField.prototype.geocodeSearch = function (_query) {
    throw Exception("geocodeSearch not implemented");
};

GeocoderField.prototype.genMessageId = function (field) {
    return "wagtailgeowidget__" + field.attr("id") + "--warning";
};

GeocoderField.prototype.clearFieldMessage = function (options) {
    var field = options.field;

    if (!field) {
        return;
    }

    var className = this.genMessageId(field);
    $("." + className).remove();
};

GeocoderField.prototype.displaySuccess = function (msg, options) {
    var self = this;
    var successMessage;
    var field = options.field;
    var className = this.genMessageId(field);

    clearTimeout(this._successTimeout);

    this.clearFieldMessage({ field: this.field });

    successMessage = document.createElement("p");
    successMessage.className = "help-block help-info " + className;
    successMessage.innerHTML = msg;

    $(successMessage).insertAfter(field);

    this._successTimeout = setTimeout(function () {
        self.clearFieldMessage({ field: field });
    }, 3000);
};

GeocoderField.prototype.displayWarning = function (msg, options) {
    var warningMsg;
    var field = options.field;
    var className = this.genMessageId(field);

    this.clearFieldMessage({ field: field });

    warningMsg = document.createElement("p");
    warningMsg.className = "help-block help-warning " + className;
    warningMsg.innerHTML = msg;

    $(warningMsg).insertAfter(field);
};

// Nominatim
function NominatimGeocoderField(options) {
    GeocoderField.call(this, options);
}

NominatimGeocoderField.prototype = Object.create(GeocoderField.prototype);
NominatimGeocoderField.prototype.constructor = GeocoderField;

NominatimGeocoderField.prototype.geocodeSearch = function (query) {
    var self = this;

    var url =
        "https://nominatim.openstreetmap.org/search?" +
        new URLSearchParams({
            q: query,
            format: "json",
        });

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            if (!data.length) {
                self.displayWarning(
                    self.translations.error_could_not_geocode_address.replace(
                        "%s",
                        query
                    ),
                    {
                        field: self.field,
                    }
                );
                return;
            }

            self.displaySuccess(self.translations.success_address_geocoded, {
                field: self.field,
            });

            var location = data[0];
            self.field.trigger("searchGeocoded", [
                { lat: location.lat, lng: location.lon },
            ]);
        })
        .catch((error) => {
            self.displayWarning("Nominatim Error: " + error, {
                field: self.field,
            });
            throw error;
        });
};

// Google Maps
function GoogleMapsGeocoderField(options) {
    GeocoderField.call(this, options);

    this.delayTime = 400;
    this.geocoder = new google.maps.Geocoder();

    var self = this;
    var autocomplete = new google.maps.places.Autocomplete(this.field[0]);

    autocomplete.addListener("place_changed", function () {
        var place = autocomplete.getPlace();

        if (!place.geometry) {
            self.geocodeSearch(place.name);
            return;
        }

        self.displaySuccess(self.translations.success_address_geocoded, {
            field: self.field,
        });

        var latLng = place.geometry.location;
        self.field.trigger("searchGeocoded", [
            { lat: latLng.lat(), lng: latLng.lng() },
        ]);
    });
}

GoogleMapsGeocoderField.prototype = Object.create(GeocoderField.prototype);
GoogleMapsGeocoderField.prototype.constructor = GeocoderField;

GoogleMapsGeocoderField.prototype.geocodeSearch = function (query) {
    var self = this;

    this.geocoder.geocode({ address: query }, function (results, status) {
        if (
            status === google.maps.GeocoderStatus.ZERO_RESULTS ||
            !results.length
        ) {
            self.displayWarning(
                self.translations.error_could_not_geocode_address.replace(
                    "%s",
                    query
                ),
                {
                    field: self.field,
                }
            );
            return;
        }

        if (status !== google.maps.GeocoderStatus.OK) {
            self.displayWarning("Google Maps Error: " + status, {
                field: self.field,
            });
            return;
        }

        var latLng = results[0].geometry.location;
        self.field.trigger("searchGeocoded", [
            { lat: latLng.lat(), lng: latLng.lng() },
        ]);
    });
};

// Mapbox
function MapboxGeocoderField(options) {
    GeocoderField.call(this, options);

    var params = options.params || {};

    this.accessToken = params.accessToken;
    this.language = params.language;
}

MapboxGeocoderField.prototype = Object.create(GeocoderField.prototype);
MapboxGeocoderField.prototype.constructor = GeocoderField;

MapboxGeocoderField.prototype.geocodeSearch = function (query) {
    var self = this;

    var url =
        "https://api.mapbox.com/search/geocode/v6/forward?" +
        new URLSearchParams({
            q: query,
            proximity: "ip",
            limit: 1,
            access_token: this.accessToken,
            language: this.language,
        });

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            // https://docs.mapbox.com/api/search/geocoding/#geocoding-api-errors
            if (data.message) {
                self.displayWarning("Map box Error: " + data.message, {
                    field: self.field,
                });
                return;
            }

            if (!data.features.length) {
                self.displayWarning(
                    self.translations.error_could_not_geocode_address.replace(
                        "%s",
                        query
                    ),
                    {
                        field: self.field,
                    }
                );
                return;
            }

            self.displaySuccess(self.translations.success_address_geocoded, {
                field: self.field,
            });

            var feature = data.features[0];
            var coordinates = feature.geometry.coordinates;
            self.field.trigger("searchGeocoded", [
                { lat: coordinates[1], lng: coordinates[0] },
            ]);
        })
        .catch((error) => {
            self.displayWarning("Map box Error: " + error, {
                field: self.field,
            });
            throw error;
        });
};
