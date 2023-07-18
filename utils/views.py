from django.shortcuts import render
from utils.tasks import my_mail
from django.http import HttpResponse, JsonResponse
# Create your views here.
def testmail(self):
    my_mail.delay()
    return HttpResponse ("Done")
    