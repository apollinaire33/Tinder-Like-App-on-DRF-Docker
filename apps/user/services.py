import geocoder
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

User = get_user_model()

# serivice class for converting geolocation
class GeoConverting:
    # func for translating adress to PointField
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

    # func for translating PointField to distance between users
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
            content = {'error': 'Provide your coordinates, please!'}
            raise ValidationError(content, code=status.HTTP_409_CONFLICT)


class UserValidation:
    def email_exists( email):
        if User.objects.filter(email=email).exists():
            content = {'error': 'Email already exists'}
            raise ValidationError(content, code=status.HTTP_409_CONFLICT)

    def password_length(password):
        if len(password) < 6:
            content = {'error': 'Password must be at least 6 characters'}
            raise ValidationError(content, code=status.HTTP_409_CONFLICT)