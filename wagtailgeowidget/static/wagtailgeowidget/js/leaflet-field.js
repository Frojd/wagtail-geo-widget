// This file must follow ES5
function LeafletField(options) {
    var id = options.id;
    var self = this;

    this.defaultLocation = {
        lat: parseFloat(options.defaultLocation.lat),
        lng: parseFloat(options.defaultLocation.lng),
    };

    this.translations = options.translations;
    this.mal = null;
    this.mapEl = $("#" + id + "_map");
    this.zoom = options.zoom;
    this.srid = options.srid;
    this.sourceField = $("#" + id);
    this.addressField = $(options.addressSelector);
    this.zoomField = $(options.zoomSelector);
    this.latLngField = $("#" + id + "_latlng");
    this.tileLayer = options.tileLayer;
    this.tileLayerOptions = options.tileLayerOptions;

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

LeafletField.prototype.setup = function () {
    if (this.hasSetup) {
        return;
    }

    var self = this;

    this.initMap(this.mapEl, this.defaultLocation);
    this.initEvents();
    this.setMapPosition(this.defaultLocation);
    this.updateLatLng(this.defaultLocation);

    this.checkVisibility(function () {
        var coords = self.latLngField.val();
        var latLng = self.parseStrToLatLng(coords);

        self.map.invalidateSize();
        self.updateMapFromCoords(latLng);
    });

    this.hasSetup = true;
};

LeafletField.prototype.initMap = function (mapEl, defaultLocation) {
    var map = L.map(mapEl[0]).setView(defaultLocation, this.zoom);

    L.tileLayer(
        this.tileLayer,
        Object.assign(
            {},
            {
                maxZoom: 19,
            },
            this.tileLayerOptions
        )
    ).addTo(map);

    let marker = L.marker(defaultLocation, { draggable: true }).addTo(map);

    this.map = map;
    this.marker = marker;
};

LeafletField.prototype.initEvents = function () {
    var self = this;

    self.marker.on("dragend", function (event) {
        var latLng = event.target.getLatLng();

        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });

    self.map.on("zoomend", function (_e) {
        var zoomLevel = self.map.getZoom();
        self.updateZoomLevel(zoomLevel);
    });

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

    this.addressField.on("searchGeocoded", function (_e, latLng) {
        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });
};

LeafletField.prototype.displayWarning = function (msg, options) {
    var warningMsg;
    var field = options.field;
    var className = this.genMessageId(field);

    this.clearFieldMessage({ field: field });

    warningMsg = document.createElement("p");
    warningMsg.className = "help-block help-warning " + className;
    warningMsg.innerHTML = msg;

    $(warningMsg).insertAfter(field);
};

LeafletField.prototype.clearFieldMessage = function (options) {
    var field = options.field;

    if (!field) {
        return;
    }

    var className = this.genMessageId(field);
    $("." + className).remove();
};

LeafletField.prototype.genMessageId = function (field) {
    return "wagtailgeowdidget__" + field.attr("id") + "--warning";
};

LeafletField.prototype.updateLatLng = function (latLng) {
    this.latLngField.val(latLng.lat + "," + latLng.lng);
};

LeafletField.prototype.updateZoomLevel = function (zoomLevel) {
    this.zoomField.val(zoomLevel);
};

LeafletField.prototype.parseStrToLatLng = function (value) {
    value = value.split(",").map(function (value) {
        return parseFloat(value);
    });

    var latLng;
    try {
        latLng = L.latLng(value[0], value[1]);
    } catch {
        return null;
    }

    if (isNaN(latLng.lat) || isNaN(latLng.lng)) {
        return null;
    }
    return latLng;
};

LeafletField.prototype.updateMapFromCoords = function (latLng) {
    this.setMapPosition(latLng);
};

LeafletField.prototype.setMapPosition = function (latLng) {
    this.marker.setLatLng(latLng);
    this.map.panTo(latLng);
};

LeafletField.prototype.writeLocation = function (latLng) {
    var lat = latLng.lat;
    var lng = latLng.lng;
    var value = LeafletField.buildLocationString(this.srid, lng, lat);

    this.setState(value);
};

LeafletField.buildLocationString = function (srid, lng, lat) {
    return "SRID=" + srid + ";POINT(" + lng + " " + lat + ")";
};

// Duplicate of GeoField.locationStringToStruct
LeafletField.locationStringToStruct = function (locationString) {
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

LeafletField.prototype.checkVisibility = function (callback) {
    var self = this;
    var intervalId = setInterval(function () {
        var visible = self.mapEl.is(":visible");
        if (!visible) {
            return;
        }

        clearInterval(intervalId);
        callback();
    }, 1000);
};

LeafletField.prototype.setState = function (newState) {
    this.sourceField.val(newState);
};

LeafletField.prototype.getState = function () {
    return this.sourceField.val();
};

LeafletField.prototype.getValue = function () {
    return this.sourceField.val();
};

LeafletField.prototype.focus = function () {
    // TODO: Implement this
};
