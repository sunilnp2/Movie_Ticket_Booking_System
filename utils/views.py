# from django.shortcuts import render

# # Create your views here.
# from time import sleep
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from celery import shared_task

# @shared_task()
# def my_mail():
#         """Sends an email when the feedback form has been submitted."""
#         sleep(20)  # Simulate expensive operation(s) that freeze Django
#         send_mail(
#             "Your Feedback",
#             "Thank you!",
#             "nepalisun22@gmail.com",
#             "suniltest@yopmail.com",
#             fail_silently=False,
#         )
#         return HttpResponse("Send")
        
    


# def testmail():
#     my_mail()
#     return HttpResponse("SEnd")