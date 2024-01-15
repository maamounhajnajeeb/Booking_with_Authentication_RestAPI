from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import status

from django.contrib.auth import login, logout, get_user_model
from django.conf import settings

import jwt

from .serializers import (
    SignUpSerializer, LogInSerializer, ForgetPasswordSerializer, ResetPassSerializer, UserSerializer,
    BookingSerializer
    )

from .models import ResetPassword, Booking
from .token_generator import Token
from .send_mail import EmailContent, send_email
from .request_class import Request


User = get_user_model()

# authentication classes
class LogOutView(generics.GenericAPIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"Error": "Already Signed Out"}, status=status.HTTP_403_FORBIDDEN)

        logout(request)
        return Response({"Success": "Signed Out Successfully"}, status=status.HTTP_200_OK)
    

class LogInView(views.APIView):
    permission_classes = (AllowAny, )
    serializer_class = LogInSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=self.request.data, context={"request": self.request}
            )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(
            {"message": "Logged in successfully"}, status=status.HTTP_202_ACCEPTED
        )
    

class SignUpView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SignUpSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        user.unactivate_user()
        
        token = Token(user).generate_token()
        
        email_content = EmailContent(request, user, token).setup_content()
        
        send_email(email_content)
        
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    
    def get(self, request):
        token = request.GET.get("token")
        
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256", ])
            
            user = User.objects.get(pk=payload["user_id"])
            user.activate_user()
            
            return Response({"Done": "Successfully Activated, log in please"}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError:
            return Response({"Error": "Expired activation link"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"Error": "Activation link has been tampered"}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPass(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ForgetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data["user"]
        
        token = Token(user).generate_token()
        
        ResetPassword.objects.create(user=user, reset_token=token)
        
        email_content = EmailContent(request, user, token).reset_password_content()
        
        send_email(email_content)
        
        return Response(
            {"Done": "We've send an activation link to your inbox, check it out."},
                status=status.HTTP_200_OK
                )


class ResetPass(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResetPassSerializer
    token_id: int | None = None
    
    def get(self, request):
        token = request.GET.get("token")
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256", ])
            ResetPass.token_id = payload.get("user_id")
            return Response(
                {"Done": "Write your new password please"}, status=status.HTTP_202_ACCEPTED
                )
        
        except jwt.ExpiredSignatureError:
            return Response({"Error": "Expired activation link"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"Error": "Activation link has been tampered"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.get(pk=self.token_id)
        user.change_password(new_password=serializer.data["password1"])
        
        ResetPassword.objects.get(user=user).delete()
        
        return Response({"Done": "Successfully reset your password, now log in"}, status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        return self.queryset.get(pk=self.request.user.id)


# booking classes
class BookingView(generics.ListCreateAPIView):
    "Create book or view all books"
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    
    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        new_request = Request(request)
        new_request.add_user(user_id)
        return super().create(new_request, *args, **kwargs)

class SpecificBookingView(generics.RetrieveUpdateDestroyAPIView):
    "Read, Update and Delete specific book"
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
