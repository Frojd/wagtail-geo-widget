# Changelog

## [Unreleased]
### Added
### Changed
### Fixed
- Add Wagtail 4.2 compability (@marteinn)
### Removed

## [7.0.0] - 2022.12.03
### Added
- Add Wagtail 4 compability (@katdom13)
- Add contribution documentation (@marteinn)

### Changed
- Update StreamFieldPanel to just FieldPanel in tests (@katdom13)
- Update StreamFields to have additional argument use_json_field in test (@katdom13)
- Rename wagtailgeowidget.edit_handlers to wagtailgeowidget.panels (@katdom13)
- Update imports in docs (@katdom13)

### Fixed
- Ensure setup() is only called after user focus if showEmptyLocation is true (@kleingeist)
- Add support for permissions on field panels (@unicode-it)

### Breaking changes
- `wagtailgeowidget.edit_handlers` has been renamed to `wagtailgeowidget.panels`


## [6.2.0] - 2022.07.03
### Added
- Add Wagtail 3 compability (@marteinn)
- Add French translations (@ThbtSprt)

### Changed
- Make GEO_WIDGET_EMPTY_LOCATION False by default (@marteinn)

### Removed
- Drop support for Wagtail 2.14 (@marteinn)

### Fixed
- Add support for running outside of docker with custom .env file in development (@marteinn)


## [6.1.0] - 2022.02.20
### Added
- Add geocoding support for Mapbox (Martin Sandström)
- Add Wagtail 2.16 support

### Fixed
- Fix: Replace ugettext with gettext (@mariusboe)
- Fix: Add documentation on leaflet settings (Martin Sandström)
- Fix: Replace test runniner with pytest
- Fix: Drop duplicated tests from wagtailgeowidget/tests


## [6.0.0] - 2022.02.06

### Added
- Add support for Leaflet with LeafletPanel/LeafletBlock (Martin Sandström)
- Add standalone block and panel for GoogleMaps (Martin Sandström)
- Add panel for address field (Martin Sandström)
- Add geocoding support for Nominatim (Martin Sandström)
- Add telepath to widgets (Martin Sandström)

### Changed
- Deprecate GeoPanel, GeoBlock and GeoWidget in favour of GoogleMapsPanel, GoogleMapsBlock and GoogleMapsWidget (Martin Sandström)
- Add Swedish translations (Martin Sandströms)

### Fixed
- Fix: Disable form submit on latlang field enter (Martin Sandström)
- Fix: Apply prettier formatting to all js (Martin Sandström)

### Removed
- Drop support for Wagtail < 2.14 (Martin Sandström)

### Note: Upgrading from 5 to 6

- Replace `GeoPanel` with `GoogleMapsPanel`
- Replace `GeoBlock` with `GoogleMapsBlock`
- Replace `FieldPanel('address')` with `GeoAddressPanel("address", geocoder=geocoders.GOOGLE_MAPS)`


## [5.3.0] - 2022.01.05

### Added
- Add persistant and user editable zoom for map widget (Martin Sandström)
- Enable loading Google Maps API key dynamically (Martin Sandström)
- Make it possible to hide latlng field for GeoBlock (@vladox)

### Fixed
- Fix: Solve issue with address not working streamfield in Wagtail 1.13+ (@vladox)
- Fix: Drop six dependency (Martin Sandström)


## [5.2.0] - 2022.01.04

### Removed
- Drop support for Python 3.6
- Drop support for EOL Wagtail


## [5.1.0] - 2020.11.21

### Added
- Implement setting for leaving location field empty (Andreas Bernacca)

### Fixed
- Update docs for services that needs to be activated (Timothy Allen)
- Fix: Move CI from Travis to Github Actions (Martin Sandström)

