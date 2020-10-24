from django.shortcuts import render
from rest_framework import generics, status, views
from .serializer import RegisterSerializer, EmailVerificationSerializer, LoginSerializer,RequestPasswordResetEmailSerializer, SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from decouple import config
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # gettting the data
    def post(self,request): 
        user = request.data
        #sending the data to serializer
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        #constract absolute url 
        absurl = 'http://' + current_site + relativeLink+"?token="+str(token)
        email_body = 'Hi '+ user.username + ' Use link below to verify your email \n' + absurl
        data = {'email_body':email_body,'to_email':user.email, 'email_subject':'Verify your email'}
        

        
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, config('SECRET_KEY'))
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email':'Successfully activated'}, status=status.HTTP_200_OK)  
        
        
        except  jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def Post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        email = request.data['email']


        if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)

                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
 
                #constract absolute url 
                absurl = 'http://' + current_site + relativeLink
                email_body = 'Hello, \n Use link below to reset your password \n' + absurl
                data = {'email_body':email_body,'to_email':user.email, 'email_subject':'Reset yor password'}
                

                
                Util.send_email(data)


     

        return Response({'sucess': 'We have sent you a link to reset your password'}, status = status.HTTP_200_OK)




class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'sucess':True,'message':'Credentials valid', 'uidb64': uidb64,'token': token}, status=status.HTTP_200_OK)


            
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token is not valid, please request a new one'})



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self,request):
        serializer = self.serializer_class(data= request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'sucesss':True, 'message':'Password reset success'}, status=status.HTTP_200_OK)