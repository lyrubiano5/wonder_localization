from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import AntennaSerializer
# Create your views here.


class LocalizationView(APIView):

    def post(self, request):
        antennas_data = request.data['antenas']
        serializer = AntennaSerializer(data=antennas_data, many=True)
        serializer.is_valid(raise_exception=True)
        message = "ok"
        return Response(data=message, status=HTTP_200_OK)
