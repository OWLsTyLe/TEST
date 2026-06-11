from rest_framework import serializers
from .models import Project, ProjectPlace


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['id', 'external_id', 'title', 'notes', 'is_visited', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'created_at', 'places']
        read_only_fields = ['id', 'created_at', 'is_completed']

class CreateProjectSerializer(serializers.ModelSerializer):
    place_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        max_length=10
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'place_ids']

    def validate_place_ids(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 places per project.")
        return value

class AddPlaceSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()


class UpdatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['notes', 'is_visited']

