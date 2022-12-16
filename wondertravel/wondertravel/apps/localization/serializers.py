from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField(allow_blank=True)


class AntennaSerializer(serializers.Serializer):
    name = serializers.CharField()
    distance = serializers.FloatField()
    message = StringListField()


class OutputSerializer(serializers.Serializer):
    position = serializers.DictField()
    message = serializers.CharField()

