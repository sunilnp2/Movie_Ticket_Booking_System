from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.api.serializers import SignUpSerializer, LoginSerializer

class SignUpSerializerView(APIView):
    
    def get(self, request):
        return Response({"message":"This is get field"})
    
    def post(self,request):
        print(request.data)
        serializer = SignUpSerializer(data = request.data,context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"created"})
        return Response(serializer.errors)
    
    
class LoginSerializerView(APIView):
    def get(self, request):
        return Response({"message":"This is get method in Login"})
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success":"Login Successfully"})
