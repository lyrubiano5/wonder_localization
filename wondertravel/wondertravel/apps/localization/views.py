from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import AntennaSerializer, OutputSerializer
from .services import (
    CalculateMassiveLocalization,
    CalculateLocalizationPart,
    MessageReceivedByPart,
    MassiveMessageReceived
)
# Create your views here.


class LocalizationView(APIView):

    def post(self, request):
        antennas_data = request.data['antenas']
        serializer = AntennaSerializer(data=antennas_data, many=True)
        serializer.is_valid(raise_exception=True)
        localization = CalculateMassiveLocalization()
        message_obj = MassiveMessageReceived()
        localization = localization.get_location(serializer.data)
        message = message_obj.get_message(serializer.data)
        response = {
            "position": {
                "x": str(localization[0]),
                "y": str(localization[1])
            },
            "message": message
        }
        output_serializer = OutputSerializer(data=response)
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data, HTTP_200_OK)


class LocalizationPart(APIView):

    def post(self, request, antenna):
        data_ = dict(
            name=antenna
        )
        data_.update(request.data)
        serializer = AntennaSerializer(data=data_)
        serializer.is_valid(raise_exception=True)
        message_obj = MessageReceivedByPart()
        message_obj.create_message(serializer.data)
        return Response("Message created", HTTP_200_OK)

    def get(self, request, antenna):
        data_ = dict(
            name=antenna
        )
        localization = CalculateLocalizationPart()
        localization = localization.get_location([data_])
        message_obj = MessageReceivedByPart()
        response = {
            "position": {
                "x": str(localization[0]),
                "y": str(localization[1])
            },
            "message": message_obj.get_message([data_])
        }
        output_serializer = OutputSerializer(data=response)
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data, HTTP_200_OK)
