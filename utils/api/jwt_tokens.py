from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import jwt
from jwt.exceptions import InvalidTokenError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings


# Jwt token process 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def generate_token(user):
    refresh = RefreshToken.for_user(user)

    
    # token = str(refresh.access_token)
    # return token
    return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }



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

        if user.email_verified == True:
             return Response({"Error":"Your Email is Verified already"}, status = status.HTTP_200_OK)
        else:
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