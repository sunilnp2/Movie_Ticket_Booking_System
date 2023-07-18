from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from api.serializers import SignUpSerializer
from rest_framework.views import APIView

# Create your views here.


class SingupSerializerView(APIView):
    def get(self, request):
        message = {"message":"Signup Here"}
        
        return Response(message, status= status.HTTP_200_OK)
    
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone = serializer.validated_data.get('phone')
            add = serializer.validated_data.get('address')
            password1 = serializer.validated_data.get('password1')
            password2 = serializer.validated_data.get('password2')
            
            print(email)
            print(phone)
            print(add)
            print(password1)
            print(password2)
            return Response("Done")
        return Response(serializer.errors)
        