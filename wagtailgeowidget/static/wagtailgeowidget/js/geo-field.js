"use strict";

function GeoField(options) {
    var self = this;
    var defaultLocation = options.defaultLocation;

    defaultLocation = new google.maps.LatLng(
        parseFloat(defaultLocation.lat),
        parseFloat(defaultLocation.lng)
    );

    this.zoom = options.zoom;
    this.srid = options.srid;
    this.sourceField = $(options.sourceSelector);
    this.addressField = $(options.addressSelector);
    this.latLngField = $(options.latLngDisplaySelector);
    this.geocoder = new google.maps.Geocoder();

    this.initMap(options.mapEl, defaultLocation);
    this.initEvents();

    this.setMapPosition(defaultLocation);
    this.updateLatLng(defaultLocation);

    if (this.addressField.length) {
        this.initAutocomplete(this.addressField[0]);
    }

    this.checkVisibility(function() {
        var coords = $(self.latLngField).val();
        google.maps.event.trigger(self.map, 'resize');
        var latLng = self.parseStrToLatLng(coords);
        self.updateMapFromCoords(latLng);
    });
}

GeoField.prototype.initMap = function(mapEl, defaultLocation) {
    var map = new google.maps.Map(mapEl, {
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
}

GeoField.prototype.initEvents = function() {
    var self = this;

    google.maps.event.addListener(this.marker, "dragend", function(event) {
        self.setMapPosition(event.latLng);
        self.updateLatLng(event.latLng);
        self.writeLocation(event.latLng);
    });

    this.latLngField.on("input", function(e) {
        var coords = $(this).val();
        var latLng = self.parseStrToLatLng(coords);
        if (latLng === null) {
            self.displayWarning(
                'Invalid location coordinate, use Latitude and Longitude '+
                '(example: 59.3293234999,18.06858080003)', {
                field: self.latLngField,
            });
            return;
        }

        self.clearFieldMessage({field: self.latLngField});
        self.updateMapFromCoords(latLng);
        self.writeLocation(latLng);
    });

    this.addressField.on("keydown", function(e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            e.stopPropagation();
        }
    });

    this.addressField.on("input", function(e) {
        clearTimeout(self._timeoutId);

        var query = $(this).val();

        if (query === "") {
            self.clearFieldMessage({field: self.addressField});
            return;
        }

        self._timeoutId = setTimeout(function() {
            self.geocodeSearch(query);
        }, 400);
    });
}

GeoField.prototype.initAutocomplete = function(field) {
    var self = this;
    var autocomplete = new google.maps.places.Autocomplete(field);

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();

        if (!place.geometry) {
            self.geocodeSearch(place.name);
            return;
        }

        self.clearAllFieldMessages();
        self.displaySuccess('Address has been successfully geo-coded', {
            field: self.addressField,
        });

        var latLng = place.geometry.location;

        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });
};

GeoField.prototype.genMessageId = function(field) {
    return 'wagtailgeowdidget__'+field.attr('id')+'--warning';
}

GeoField.prototype.displayWarning = function(msg, options) {
    var warningMsg;
    var field = options.field;
    var className = this.genMessageId(field);

    this.clearFieldMessage({field: field});

    warningMsg = document.createElement('p');
    warningMsg.className = 'help-block help-warning ' + className;
    warningMsg.innerHTML = msg;

    $(warningMsg).insertAfter(field);
}

GeoField.prototype.displaySuccess = function(msg, options) {
    var self = this;
    var successMessage;
    var field = options.field;
    var className = this.genMessageId(field);

    clearTimeout(this._successTimeout);

    this.clearFieldMessage({field: field});

    successMessage = document.createElement('p');
    successMessage.className = 'help-block help-info ' + className;
    successMessage.innerHTML = msg;

    $(successMessage).insertAfter(field);

    this._successTimeout = setTimeout(function() {
        self.clearFieldMessage({field: field});
    }, 3000);
}

GeoField.prototype.clearFieldMessage = function(options) {
    var field = options.field;

    if (!field) {
        return;
    }

    var className = this.genMessageId(field);
    $('.' + className).remove();
}

GeoField.prototype.clearAllFieldMessages = function() {
    var self = this;
    var fields = [this.addressField, this.latLngField];
    fields.map(function(field) {
        self.clearFieldMessage({field: field});
    });
}

GeoField.prototype.checkVisibility = function(callback) {
    var self = this;
    var intervalId = setInterval(function() {
        var visible = $(self.map.getDiv()).is(':visible')
        if (!visible) {
            return;
        }

        clearInterval(intervalId);
        callback();
    }, 1000);
}

GeoField.prototype.geocodeSearch = function(query) {
    var self = this;

    this.geocoder.geocode({'address': query}, function(results, status) {
        if (status === google.maps.GeocoderStatus.ZERO_RESULTS || !results.length) {
            self.displayWarning(
                'Could not geocode address "' + query + '". '+
                'The map may not be in sync with the address entered.', {
                    field: self.addressField
                }
            );
            return;
        }

        if (status !== google.maps.GeocoderStatus.OK) {
            self.displayWarning('Google Maps Error: '+status, {
                field: self.addressField,
            });
            return;
        }

        self.clearAllFieldMessages();
        self.displaySuccess('Address has been successfully geo-coded', {
            field: self.addressField,
        });
        var latLng = results[0].geometry.location;

        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });
}

GeoField.prototype.updateLatLng = function(latLng) {
    this.latLngField.val(latLng.lat()+","+latLng.lng());
}

GeoField.prototype.parseStrToLatLng = function(value) {
    value = value.split(",").map(function(value) {
        return parseFloat(value);
    });

    var latLng = new google.maps.LatLng(value[0], value[1]);
    if (isNaN(latLng.lat()) || isNaN(latLng.lng())) {
        return null;
    }
    return latLng
}

GeoField.prototype.updateMapFromCoords = function(latLng) {
    this.setMapPosition(latLng);
}

GeoField.prototype.setMapPosition = function(latLng) {
    this.marker.setPosition(latLng);
    this.map.setCenter(latLng);
}

GeoField.prototype.writeLocation = function(latLng) {
    var lat = latLng.lat();
    var lng = latLng.lng();
    var value = 'SRID=' + this.srid + ';POINT(' + lng + ' ' +lat+')';

    this.sourceField.val(value);
}

function initializeGeoFields() {
    $(".geo-field").each(function(index, el) {
        var $el = $(el);

        if ($el.data('geoInit')) {
            return;
        }

        var data = window[$el.data('data-id')];
        var options = {
            mapEl: el,
            sourceSelector: $(data.sourceSelector),
            latLngDisplaySelector: $(data.latLngDisplaySelector),
            zoom: data.zoom,
            srid: data.srid,
        }

        $el.data('geoInit', true);

        options.addressSelector = data.addressSelector;
        options.defaultLocation = data.defaultLocation;

        new GeoField(options);
    });
}
