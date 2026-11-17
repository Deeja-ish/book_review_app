from .models import User, EmailVerification
from .serializers import RegistrationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, LoginSerializer, ViewUserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework. response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

# create a class for user registration
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    code = EmailVerification.objects.create(user=user)

                    send_mail(
                        subject = "Your verification code",
                        message = f"Your One-Time OTP PIN is {code.otp}",
                        from_email = settings.EMAIL_BACKEND,
                        recipient_list = [user.email],
                        fail_silently = False,  
                    )

                    return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status" : "error", "message" : str(e)})
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# allow only admins and authenticated users to view all users
class AllUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer =ViewUserSerializer(data=users, many=True)
        if serializer.is_valid():
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# show the data of the single user
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(user=self.request.user)
        serializer = ViewUserSerializer(data=user)
        if serializer.is_valid():
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)
        return Response({"status" : "error", "message" : serializer.errors})

# create a class to verify the user otp 
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data 
        email = data.get('email')
        otp = data.get("otp")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status" : "error", "message" : "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            email_otp = EmailVerification.objects.get(user=user)
        except EmailVerification.DoesNotExist:
            return Response({"status" : "error", "message" : "Verification details not Found"}, status=status.HTTP_400_BAD_REQUEST)

        # check if otp match
        if(str(otp) != str(email_otp.otp)):
            return Response({"status" : "error", "message" : "Wrong OTP Try again"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        return Response({"status" : "success", "message" : "User verification is successful"}, status=status.HTTP_200_OK)    

#create the login view 
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            if response.status_code == 200:
                access_token = response.data.get("access")
                refresh_token = response.data.get("refresh")
                response = Response({
                    "message" : "Login Successful"
                }, status=status.HTTP_200_OK)

                response.set_cookie(
                    key="access",
                    value=access_token,
                    httponly=True,
                    secure=False,
                    samesite='Lax'
                )
                
                response.set_cookie(
                    key="refresh",
                    value=refresh_token,
                    httponly=True,
                    secure=False,
                    samesite='Lax'
                )

            return response
        return Response({"message" : "Login Failed"}, status=status.HTTP_400_BAD_REQUEST)


# crete the refresh token view 
class RefreshToken(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"message" : "Refresh Token not found"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh' : refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"message" : "Invalid Refresh Token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data['access']
        response = Response({"message" : "Access token has been refreshed Successfully"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access',
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        return response

# create a class for password change
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : "Password Reset is successfull"}, status=status.HTTP_200_OK)
        return Response({"status" : "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# create a class to get the otp for password
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data, context={"request" : request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : "Email Sent successfully"}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message" : serializer.errors}, HTTP_400_BAD_REQUEST) 

# create a class to reset the password
class ResetPasswordView(APIView):
    permission_classes[AllowAny]
    def post(self, request):
        serializer= ResetPasswordSerializer(data=request.data, context={"request" : request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message" : "password reset successfull"},status=status.HTTP_200_OK)
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
