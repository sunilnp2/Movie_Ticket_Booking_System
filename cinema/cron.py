from django.shortcuts import redirect
from authentication.models import User
def DeleteUnverifiedAccount():
    unver = User.objects.filter(email_verified = False)
    unver.delete()
    return redirect('cinema:home')