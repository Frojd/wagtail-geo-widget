## FAQ

### Is it possible to hide the lat/lng field?

Yes, by passing `hide_latlng=True` to the GeoPanel.

```python
GeoPanel('location', address_field='address', hide_latlng=True)
```

For streamfields use the following:

```python
GeoBlock(address_field='address', hide_latlng=True)
```

