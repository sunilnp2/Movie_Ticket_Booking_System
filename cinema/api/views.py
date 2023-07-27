from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HomeAPiView(APIView):
    def get(self, request):
        response_data = {'success':"This is Homepage"}
        return Response( response_data, status = status.HTTP_202_ACCEPTED)



