from rest_framework import serializers
from .models import Customer, Courrier, Supplier,User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode




class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    #set write_only to true so that to avoid exposing it to the front end
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate(self,attrs):
        email = attrs.get('email', '')# the empty string is a fallback value so that it does not crush
        username = attrs.get('username', '')

        #check is username is alphanumric
        if not username.isalnum():
            raise serializers.ValidationError('The username should only cointain alphanumric characters')
        return attrs
    #function to create the user takes the user data as argument
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']
 
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'password']


class CourrrierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Courrier
        fields = ['name', 'phone', 'address']


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, read_only=True)
    tokens = serializers.CharField(max_length=68, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user=auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('email is not verified')
        

        return {
            'email': user.email,
            'username': user.username,
            'tokens':user.tokens()
        }

        return super().validate(attrs)


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password','token','uidb64']



    def validate(self,attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uibd64')

            id= force_str(urlsafe_base64_decode(uidb64))
            user =User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
        except Exception as e:
                raise AuthenticationFailed('The reset link is invalid', 401)
            
        return super().validate(attrs)





   