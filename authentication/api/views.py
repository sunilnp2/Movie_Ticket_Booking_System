from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.api.serializers import SignUpSerializer, LoginSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status
from authentication.api.serializers import SignUpSerializer, LoginSerializer, MyCustomTokenObtainPairSerializer

class SignUpSerializerView(APIView):
    
    def get(self, request):
        return Response({"message":"This is get field"})
    
    def post(self,request):
        print(request.data)
        serializer = SignUpSerializer(data = request.data,context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)  # This will raise a ValidationError if data is invalid
            serializer.save()
            return Response("Successfully created", status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginSerializerView(APIView):
    def get(self, request):
        return Response({"message":"This is get method in Login"})
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success":"Login Successfully"})
        



# View code for custom jwt-----------------------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyCustomTokenObtainPairSerializer

# Your other views and endpoints can inherit from APIView
# class MyProtectedView(APIView):
#     def get(self, request, format=None):
#         custom_token_view = CustomTokenObtainPairView.as_view()

#         # Simulate a POST request with user credentials
#         request = RequestFactory().post('/auth/token/', data={'email': 'admin@gmail.com', 'password': 'admin123'})
#         token_response = custom_token_view(request)

#         # Get the token from the response
#         access = token_response.data.get('access', None)
#         refresh = token_response.data.get('refresh', None)

#         return Response({"Access":access, "Refresh":refresh})
