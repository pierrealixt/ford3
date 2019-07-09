import re


def location_as_dict(location):
    res = re.search(
        r'SRID=([0-9]{4});POINT \(([0-9.-]*) ([0-9.-]*)\)',
        location)
    if res:
        return {
            'srid': int(res.group(1)),
            'lat': float(res.group(2)),
            'lng': float(res.group(3))
        }
    else:
        return None
