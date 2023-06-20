from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from movie.models import *

# # Create your views here.

class BaseView(View):
    views = {}
    views['showing'] = Movie.objects.filter(status = "showing")
    views['coming'] = Movie.objects.filter(status = "comingsoon")


class HomeView(BaseView):
    def get(self,request):
        user = get_user_model()
        name = user.first_name

        return render(request,'index.html', self.views)
    
