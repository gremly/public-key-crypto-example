from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cipher.serializers import PublicKeySerializer, ValidationSerializer

# Create your views here.

class PublicKeyRegister(APIView):

    def post(self, request, format=None):
        """docstring for re"""

        serializer = PublicKeySerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            # Removing key from JSON object to return only the object id.
            del serializer.data['key']

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicKeyValidation(APIView):

    def post(self, request, format=None):
        """docstring for re"""

        serializer = ValidationSerializer(data=request.DATA)

        # Codes to be returned according to validation.
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
