
from django.urls import path
<<<<<<< Updated upstream
from .views import SignUpSerializerView, LoginSerializerView
from utils.api.jwt_tokens import VerifyTOkenView, RefreshToken

=======
from .views import SignUpSerializerView, LoginSerializerView, CustomTokenObtainPairView
from utils.api.jwt_tokens import VerifyTOkenView
from rest_framework_simplejwt.views import TokenRefreshView
>>>>>>> Stashed changes

urlpatterns = [
    path('api_signup/', SignUpSerializerView.as_view(), name='api_signup'),
    path('api_login/', LoginSerializerView.as_view(), name = 'api_login'),
    path('drf_activate/<uidb64>/<token>/',VerifyTOkenView.as_view(), name='drf_activate'),

    # urls for custom jwt token 
     path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    #  path('protect/', MyProtectedView.as_view(), name='protect'),



]



