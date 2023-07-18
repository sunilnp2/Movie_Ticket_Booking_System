from rest_framework import serializers
from authentication.models import User

def validate_email(self, value):
    user = User.objects.all()
    if user.filter(email = value).exists():
        raise serializers.ValidationError("This email is already Taken Enter new")
    
    return value

def validate_phone(self, value):
    user = User.objects.all()
    if user.filter(phone = value).exists():
        raise serializers.ValidationError("This phone is already Taken Enter new")
    
    return value

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
    
    def validate(self, email):
        email = email.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        return email
    
    def validate_phone(self, phone):
        phone = phone.get('phone')
        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("This phone is already in use.")
        return phone
    
    def create(self, validated_data):
        return super().create(**validated_data)