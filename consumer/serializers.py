from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from consumer.models import Consumer

class ConsumerSerializer(GeoFeatureModelSerializer):
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = Consumer
        id_field = False
        geo_field = 'location'
        fields = ('id', 'amount_due', 'previous_jobs_count', 'status', 'street')

