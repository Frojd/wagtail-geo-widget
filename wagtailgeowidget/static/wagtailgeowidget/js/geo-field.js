"use strict";

function GeoField(options) {
    defaultLocation = options.defaultLocation;
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
    this.geoErrorClassName = 'wagtailgeowidget__geo-error';

    this.initMap(options.mapEl, defaultLocation);
    this.initEvents();

    this.setMapPosition(defaultLocation);
    this.updateLatLng(defaultLocation);
}

GeoField.prototype.initMap = function(mapEl, defaultLocation) {
    var map = new google.maps.Map(mapEl, {
        zoom: this.zoom,
        center: defaultLocation
    });

    var marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: true
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
        coords = coords.split(",").map(function(value) {
            return parseFloat(value);
        });

        var latLng = new google.maps.LatLng(
            coords[0],
            coords[1]
        );

        self.setMapPosition(latLng);
    });

    this.addressField.on("input", function(e) {
        clearTimeout(self._timeoutId);

        var query = $(this).val();

        if (query === "") {
          self.clearError();
          return;
        }

        self._timeoutId = setTimeout(function() {
            self.geocodeSearch(query);
        }, 400);
    });
}

GeoField.prototype.displayError = function (msg) {
    var self = this;

    $('.' + self.geoErrorClassName).remove();
    var errMessage = document.createElement('p');
    var errSpan = document.createElement('span');

    errMessage.className = 'error-message ' + self.geoErrorClassName;
    errSpan.innerHTML = msg;
    errMessage.appendChild(errSpan)

    $(errMessage).insertAfter(self.addressField);
    self.addressField.closest('.field').addClass('error');
}

GeoField.prototype.clearError = function () {
    var self = this;

    $('.' + self.geoErrorClassName).remove();
    self.addressField.closest('.field').removeClass('error');
}

GeoField.prototype.geocodeSearch = function(query) {
    var self = this;

    this.geocoder.geocode({'address': query}, function(results, status) {
        if (status === google.maps.GeocoderStatus.ZERO_RESULTS || !results.length) {
          self.displayError('No results found');
        }
        if (status !== google.maps.GeocoderStatus.OK) {
            self.displayError('Google Maps Error: '+status);
            return;
        }

        self.clearError();
        var latLng = results[0].geometry.location;

        self.setMapPosition(latLng);
        self.updateLatLng(latLng);
        self.writeLocation(latLng);
    });
}

GeoField.prototype.updateLatLng = function(latLng) {
    this.latLngField.val(latLng.lat()+","+latLng.lng());
}

GeoField.prototype.setMapPosition = function(latLng) {
    this.marker.setPosition(latLng);
    this.map.setCenter(latLng);
}

GeoField.prototype.writeLocation = function(latLng) {
    var lat = latLng.lat();
    var lng = latLng.lng();
    var value = 'SRID='+this.srid+';POINT('+lng+' '+lat+')';

    this.sourceField.val(value);
}

var initializeGeoFields = function() {
    $(".geo-field").each(function(index, el) {
        var $el = $(el);

        var data = window[$el.data('data-id')];
        var options = {
            mapEl: el,
            sourceSelector: $(data.sourceSelector),
            latLngDisplaySelector: $(data.latLngDisplaySelector),
            zoom: data.zoom,
            srid: data.srid,
        }

        options.addressSelector = data.addressSelector;
        options.defaultLocation = data.defaultLocation;

        new GeoField(options);
    });
}

$(document).ready(function() {
    google.maps.event.addDomListener(window, 'load', initializeGeoFields);
});
