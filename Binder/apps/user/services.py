import geocoder
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


# service func for translating adress to PointField
def adress_to_point(self, serializer):
    adress = serializer.initial_data['adress']
    if adress:
        g = geocoder.osm(adress)
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        pnt = 'POINT(' + str(longitude) + ' ' + str(latitude) + ')'
        serializer.save(location=pnt)
    else:
        serializer.save()


# service func for translating PointField to distance between users
def point_to_distance(self, qs):
    latitude = self.request.query_params.get('lat', None)
    longitude = self.request.query_params.get('lng', None)
    if latitude and longitude:        
        pnt = GEOSGeometry('POINT(' + str(longitude) + ' ' + str(latitude) + ')', srid=4326)
        if self.request.user.id is None or self.request.user.subscription == 'BASE':
            qs = qs.annotate(distance=Distance('location', pnt)).order_by('distance').filter(distance__lte=D(km=10.01).m)[:25]
        elif self.request.user.subscription == 'VIP':
            qs = qs.annotate(distance=Distance('location', pnt)).order_by('distance').filter(distance__lte=D(km=25.01).m)[:100]
        elif self.request.user.subscription == 'PREMIUM':
            qs = qs.annotate(distance=Distance('location', pnt)).order_by('distance')
        return qs
    else:
        raise Exception('Provide your coordinates, please!')
