from rest_framework import serializers
from authentication.models import User
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Jwt token process 
from rest_framework_simplejwt.tokens import RefreshToken
def generate_token(user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    return token



def activateEmail(request,email):
    user = User.objects.get(email = email)
    username = User.objects.get(email=email).username
    id = user.id
    domain =  get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_token(user)
    protocol = 'https' if request.is_secure() else 'http'
    print(f"The email is {email}")
    print(f"The email is {domain}")
    print(f"The email is {token}")
    print(f"The email is {protocol}")
    
    
    subject = f"Hello {username}"
    print(token)
    message = "Activate Your account"
    message = render_to_string("drf-email-activate.html", {
        'user': user.first_name,
        'domain': domain,
        'uid': uid,
        'token': token,
        "protocol": protocol,
    })
    email_from = settings.EMAIL_HOST_USER 
    send_mail(
        subject=subject,
        message=message,
        from_email=email_from,
        recipient_list=[email],
        fail_silently=False,
    )
    # subject = 'Hello'
    # body = 'This is the body of the email.'
    # from_email = settings.EMAIL_HOST_USER,
    # to = ['sunilnepali844@gmail.com']

    # email = EmailMessage(subject, message, from_email, to)
    # email.send()


    

class SignUpSerializer(serializers.Serializer):
    
    ADDRESS  = (
     ('Kathmandu', 'Kathmandu'),
    ('Pokhara', 'Pokhara'),
    ('Butwal', 'Butwal'),
    ('Dharan', 'Dharan'),
    ('Bhaktpur', 'Bhaktpur'),
    ('LalitPur', 'Lalitpur'),
)
    
    email = serializers.EmailField()
    phone = serializers.CharField(max_length = 10)
    address = serializers.ChoiceField(ADDRESS, default='kathmandu')
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists try with new.")
        
        elif value[0].isdigit() == True:
            raise serializers.ValidationError("Email Must start with String.")
        
        end_strings = [".gmail.com", ".yahoo.com", ".hotmail.com", "yopmail.com", "tempmail.com"]
        val = any(value.endswith(end_str) for end_str in end_strings)
        if not val:
            raise serializers.ValidationError("This is invalid format")
        return value
        
    
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists try with new.")
        
        
        if value.startswith("98") == False or len(value) > 10 or len(value) < 10 or value.isalpha() == True:
            raise serializers.ValidationError("Phone is invalid.")
        return value
   
    def validate(request, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            return serializers.ValidationError("Password is not match Try again")
        return attrs

            
    
    def create(self,validated_data):
        request = self.context.get('request')
        email = validated_data.get("email")
        
        phone = validated_data.get("phone")
        address = validated_data.get("address")
        password = validated_data.get("password")
        password2 = validated_data.get("password2")
        print(email)
        print(phone)
        print(address)
        print(password)
        print(password2)
        
        if password != password2:
            raise serializers.ValidationError("Password is not match.")
        
        username = email.split('@')[0]
        print(username)
        # username = ""
        
        usr  = User(
            email = email,
            username = username,
            phone = phone,
            address = address,
            password = password
        ).save()
        # myuser = usr.save()
        activateEmail(request,email)

        return Response({"message":"Created"})

        
        
#-------------- code for signin-------------------------------------------------------------- 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
