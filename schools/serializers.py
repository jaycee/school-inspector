from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

import schools.models as schools_models

class SchoolListSerializer(geo_serializers.GeoModelSerializer):
    eligibility = serializers.SerializerMethodField('get_eligibility')
    preference = serializers.SerializerMethodField('get_preference')

    class Meta:
        model = schools_models.School
        fields = ('id', 'name', 'level', 'address', 'type', 'eligibility', 'location', 'preference')

    def get_eligibility(self, obj):
        pt = self.context['point']
        if obj.district is not None and obj.district.contains(pt):
            return 'assigned'
        if obj.walk_zone is not None and obj.walk_zone.contains(pt):
            #TODO set highlight color
            return 'assigned'
        if obj.type == 'magnet':
            return 'option'
        if obj.type == 'charter':
            return 'option'
        return 'all'

    def get_preference(self, obj):
        pt = self.context['point']
        if obj.priority_zone is not None and obj.priority_zone.contains(pt):
            return 'priority'
        if obj.choice_zone is not None and obj.choice_zone.contains(pt):
            return 'choice'

class SchoolDetailSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = schools_models.School
