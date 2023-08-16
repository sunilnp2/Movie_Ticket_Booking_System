from rest_framework import serializers
from authentication.models import User, Customer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from utils.api.jwt_tokens import get_tokens_for_user
from rest_framework import status
from utils.api.activate_email import activateEmail

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
        return Response({"success":"Created"})
        

        
        
#-------------- code for signin-------------------------------------------------------------- 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
    def create(self,validated_data):
        email = validated_data.get('email')
        pw = validated_data.get('password')
    
        user = authenticate(email = email, password = pw)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
        return Response({'errors':{'non_field_errors':["Username Or Password is not valid"]}},
                        status = status.HTTP_404_NOT_FOUND)


# customer

class CustomerSerializer(serializers.Serializer):
    profile = serializers.ImageField(allow_null=True, required=False)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=200, allow_blank=True, allow_null=True, required=False)
    last_name = serializers.CharField(max_length=200, allow_blank=True, allow_null=True, required=False)
    phone = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=50)
    balance = serializers.IntegerField(default=0)
    
    def create(self, validated_data):
        return Customer.objects.create(**validated_data)