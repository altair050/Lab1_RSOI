from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.Serializer):
    name = serializers.CharField()
    director = serializers.CharField()
    release_date = serializers.IntegerField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.director = validated_data.get('director', instance.director)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.save()

        return instance

    def validate_name(self, value):

        return value

    def validate_release_date(self, value):
        if value < 1895:
            raise serializers.ValidationError("Release data is impossibly old")

        return value
