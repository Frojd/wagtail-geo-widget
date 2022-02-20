// This file must follow ES5
"use strict";

function GoogleMapsField(options) {
    var id = options.id;
    var self = this;
    var defaultLocation = options.defaultLocation;

    this.defaultLocation = new google.maps.LatLng(
        parseFloat(defaultLocation.lat),
        parseFloat(defaultLocation.lng)
    );

    this.translations = options.translations;
    this.mapEl = $("#" + id + "_map");
    this.zoom = options.zoom;
    this.srid = options.srid;
    this.sourceField = $("#" + id);
    this.addressField = $(options.addressSelector);
    this.zoomField = $(options.zoomSelector);
    this.latLngField = $("#" + id + "_latlng");
    this.geocoder = new google.maps.Geocoder();
    this.showEmptyLocation = options.showEmptyLocation;

    if (this.zoomField && this.zoomField.val()) {
        this.zoom = parseInt(this.zoomField.val());
    }

    if (this.zoomField && !this.zoomField.val()) {
        this.updateZoomLevel(this.zoom);
    }

    if (options.showEmptyLocation) {
        this.addressField.attr("placeholder", this.translations.enter_location);
        this.latLngField.attr("placeholder", this.translations.initialize_map);

        this.mapEl.css("display", "none");

        this.latLngField.on("focus", function () {
            self.mapEl.css("display", "block");
            self.setup();
        });
        this.addressField.on("focus", function () {
            self.mapEl.css("display", "block");
            self.setup();
        });
    } else {
        this.setup();
    }
}

GoogleMapsField.prototype.setup = function () {
    if (this.hasSetup) {
        return;
    }
    var self = this;

    this.initMap(this.mapEl, this.defaultLocation);
    this.initEvents();
    this.setMapPosition(this.defaultLocation);
    this.updateLatLng(this.defaultLocation);

    this.checkVisibility(function () {
        var coords = $(self.latLngField).val();
        google.maps.event.trigger(self.map, "resize");
        var latLng = self.parseStrToLatLng(coords);
        self.updateMapFromCoords(latLng);
    });

    if (this.addressField.length && !this.hasAddressFieldOwnGeocoder()) {
        this.initAutocomplete(this.addressField[0]);
    }

    this.hasSetup = true;
};

GoogleMapsField.prototype.initMap = function (mapEl, defaultLocation) {
    var map = new google.maps.Map(mapEl[0], {
        zoom: this.zoom,
        center: defaultLocation,
    });

    var marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: true,
    });

    this.map = map;
    this.marker = marker;
};

GoogleMapsField.prototype.hasAddressFieldOwnGeocoder = function () {
    return !!this.addressField.data("geocoder");
};

GoogleMapsField.prototype.initEvents = function () {
    var self = this;

    google.maps.event.addListener(this.marker, "dragend", function (event) {
        self.setMapPosition(event.latLng);
        self.updateLatLng(event.latLng);
        self.writeLocation(event.latLng);
    });

    google.maps.event.addListener(this.map, "zoom_changed", function () {
        var zoomLevel = this.getZoom();
        self.updateZoomLevel(zoomLevel);
    });

    if (this.hasAddressFieldOwnGeocoder()) {
        this.addressField.on("searchGeocoded", function (_e, latLng) {
            var gMLatLng = new google.maps.LatLng(
                parseFloat(latLng.lat),
                parseFloat(latLng.lng)
            );

            self.setMapPosition(gMLatLng);
            self.updateLatLng(gMLatLng);
            self.writeLocation(gMLatLng);
        });
    } else {
        this.addressField.on("keydown", function (e) {
            if (e.keyCode === 13) {
                e.preventDefault();
                e.stopPropagation();
            }
        });

        this.addressField.on("input", function (_e) {
            clearTimeout(self._timeoutId);

            var query = $(this).val();

            if (query === "") {
                self.clearFieldMessage({ field: self.addressField });
                return;
            }

            self._timeoutId = setTimeout(function () {
                self.geocodeSearch(query);
            }, 400);
        });
    }

    this.latLngField.on("keydown", function (e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            e.stopPropagation();
        }
    });

    this.latLngField.on("input", function (_e) {
        var coords = $(this).val();
        var latLng = self.parseStrToLatLng(coords);
        if (latLng === null) {
            self.displayWarning(
                self.translations.error_message_invalid_location,
                {
                    field: self.latLngField,
                }
            );
            return;
        }

        self.clearFieldMessage({ field: self.latLngField });
        self.updateMapFromCoords(latLng);
        self.writeLocation(latLng);
    });

    this.zoomField.on("keydown", function (e) {
        if (e.keyCode !== 13) {
            // enter (13)
            return;
        }

        e.preventDefault();
        e.stopPropagation();

        var zoom = $(this).val();
        zoom = parseInt(zoom);
        if (isNaN(zoom)) {
            zoom = self.defaultZoom;
        }

        self.map.setZoom(zoom);
        self.updateZoomLevel(zoom);
    });
};

GoogleMapsField.prototype.initAutocomplete = function (field) {
    var self = this;
    var autocomplete = new google.maps.places.Autocomplete(field);

    autocomplete.addListener("place_changed", function () {
        var place = autocomplete.getPlace();

        if (!place.geometry) {
            self.geocodeSearch(place.name);
            return;
        }

        self.clearAllFieldMessages();
        self.displaySuccess(self.translations.success_address_geocoded, {
            field: self.addressField,
        });

        var latLng = place.geometry.location;

        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });
};

GoogleMapsField.prototype.genMessageId = function (field) {
    return "wagtailgeowdidget__" + field.attr("id") + "--warning";
};

GoogleMapsField.prototype.displayWarning = function (msg, options) {
    var warningMsg;
    var field = options.field;
    var className = this.genMessageId(field);

    this.clearFieldMessage({ field: field });

    warningMsg = document.createElement("p");
    warningMsg.className = "help-block help-warning " + className;
    warningMsg.innerHTML = msg;

    $(warningMsg).insertAfter(field);
};

GoogleMapsField.prototype.displaySuccess = function (msg, options) {
    var self = this;
    var successMessage;
    var field = options.field;
    var className = this.genMessageId(field);

    clearTimeout(this._successTimeout);

    this.clearFieldMessage({ field: field });

    successMessage = document.createElement("p");
    successMessage.className = "help-block help-info " + className;
    successMessage.innerHTML = msg;

    $(successMessage).insertAfter(field);

    this._successTimeout = setTimeout(function () {
        self.clearFieldMessage({ field: field });
    }, 3000);
};

GoogleMapsField.prototype.clearFieldMessage = function (options) {
    var field = options.field;

    if (!field) {
        return;
    }

    var className = this.genMessageId(field);
    $("." + className).remove();
};

GoogleMapsField.prototype.clearAllFieldMessages = function () {
    var self = this;
    var fields = [this.addressField, this.latLngField];
    fields.map(function (field) {
        self.clearFieldMessage({ field: field });
    });
};

GoogleMapsField.prototype.checkVisibility = function (callback) {
    var self = this;
    var intervalId = setInterval(function () {
        var visible = $(self.map.getDiv()).is(":visible");
        if (!visible) {
            return;
        }

        clearInterval(intervalId);
        callback();
    }, 1000);
};

GoogleMapsField.prototype.geocodeSearch = function (query) {
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
                    field: self.addressField,
                }
            );
            return;
        }

        if (status !== google.maps.GeocoderStatus.OK) {
            self.displayWarning("Google Maps Error: " + status, {
                field: self.addressField,
            });
            return;
        }

        self.clearAllFieldMessages();
        self.displaySuccess(self.translations.success_address_geocoded, {
            field: self.addressField,
        });

        var latLng = results[0].geometry.location;
        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });
};

GoogleMapsField.prototype.updateLatLng = function (latLng) {
    this.latLngField.val(latLng.lat() + "," + latLng.lng());
};

GoogleMapsField.prototype.updateZoomLevel = function (zoomLevel) {
    this.zoomField.val(zoomLevel);
};

GoogleMapsField.prototype.parseStrToLatLng = function (value) {
    value = value.split(",").map(function (value) {
        return parseFloat(value);
    });

    var latLng = new google.maps.LatLng(value[0], value[1]);
    if (isNaN(latLng.lat()) || isNaN(latLng.lng())) {
        return null;
    }
    return latLng;
};

GoogleMapsField.prototype.updateMapFromCoords = function (latLng) {
    this.setMapPosition(latLng);
};

GoogleMapsField.prototype.setMapPosition = function (latLng) {
    this.marker.setPosition(latLng);
    this.map.setCenter(latLng);
};

GoogleMapsField.prototype.writeLocation = function (latLng) {
    var lat = latLng.lat();
    var lng = latLng.lng();
    var value = GoogleMapsField.buildLocationString(this.srid, lng, lat);

    this.sourceField.val(value);
};

GoogleMapsField.buildLocationString = function (srid, lng, lat) {
    return "SRID=" + srid + ";POINT(" + lng + " " + lat + ")";
};

GoogleMapsField.locationStringToStruct = function (locationString) {
    if (!locationString) {
        return {};
    }

    var matches = locationString.match(
        /^SRID=([0-9]{1,});POINT\s?\((-?[0-9\.]{1,})\s(-?[0-9\.]{1,})\)$/
    );

    return {
        srid: matches[1],
        defaultLocation: {
            lng: matches[2],
            lat: matches[3],
        },
    };
};

GoogleMapsField.prototype.setState = function (newState) {
    this.sourceField.val(newState);
};

GoogleMapsField.prototype.getState = function () {
    return this.sourceField.val();
};

GoogleMapsField.prototype.getValue = function () {
    return this.sourceField.val();
};

GoogleMapsField.prototype.focus = function () {
    // TODO: Implement this
};
