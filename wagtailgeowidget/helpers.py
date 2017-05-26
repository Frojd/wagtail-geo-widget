import re

geos_ptrn = re.compile(
    "^SRID=([0-9]{1,});POINT\((-?[0-9\.]{1,})\s(-?[0-9\.]{1,})\)$"
)


def geosgeometry_str_to_struct(value):
    '''
    Parses a geosgeometry string into struct.

    Example:
        SRID=5432;POINT(12.0 13.0)
    Returns:
        >> [5432, 12.0, 13.0]
    '''

    result = geos_ptrn.match(value)

    if not result:
        return None

    return {
        'srid': result.group(1),
        'x': result.group(2),
        'y': result.group(3),
    }
