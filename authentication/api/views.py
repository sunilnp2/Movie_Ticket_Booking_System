from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.api.serializers import SignUpSerializer, LoginSerializer
from django.conf import settings
from authentication.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import jwt
from jwt.exceptions import InvalidTokenError
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


# function for get token and refresh token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def verify_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token
        
    except InvalidTokenError:
        return Response({"error":"Invalid"})
    except Exception as e:
        return Response({"error":e})

class VerifyTOkenView(APIView):
    def get(self,request, uidb64, token):
        user = request.user
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        decoded_token = verify_jwt_token(token)
        
        if decoded_token is not None:
            user.email_verified = True
            user.save()
            return Response({"success":"Thank you for Email Confirmation"}, status = status.HTTP_200_OK)
        else:
            return Response({"message":"Invalid Token"}, status.HTTP_400_BAD_REQUEST)


class SignUpSerializerView(APIView):
    
    def get(self, request):
        return Response({"message":"This is get field"})
    
    def post(self,request):
        print(request.data)
        serializer = SignUpSerializer(data = request.data,context={'request': request})
        # ,context={'request': request}
        if serializer.is_valid():
            validated_data=serializer.validated_data
            serializer.create(validated_data) 
            # serializer.save()
            return Response({"message":"created"})
        return Response(serializer.errors)
    
    
class LoginSerializerView(APIView):
    def get(self, request):
        return Response({"message":"This is get method in Login"})
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(request,email = email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                login(request, user)
                return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response({'errors':{'non_field_errors':["Username Or Password is not valid"]}},
                            status = status.HTTP_404_NOT_FOUND)
