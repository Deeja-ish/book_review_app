from rest_framework import serializers
from .models import User, EmailVerification, PasswordForget
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        read_only_fields = ['is_verified']

        
    # validate the password
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password" : "Passwords Must Match"})
        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({"password" : list(e.messages)})

        return attrs

    # validate the email field
    def validate_email(self, value):
        user_email = value.lower()

        if User.objects.filter(email__iexact=user_email).exists():
            raise serializers.ValidationError({"email" : "Email already exists"})
        return user_email

    # save the user
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

# create the login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'message' : "User does not exist"})
        
        if not user.check_password(password):
            raise serializers.ValidationError({"Password" : "Wrong Email or Password"})

        attrs['user'] = user
        return attrs

# create the view serializer
class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ["username", "first_name", "last_name", "email", "is_verified", "created_at"]

    
# create a change password serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        request = self.context.get("request")

        if request is None and not hasattr(request, "user"):
            raise serializers.ValidationError({"Request body is empty"})
        user = request.user

        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")

        if not user.check_password(old_password):
            raise serializers.ValidationError({"password" : "Wrong Password"})
        if old_password == new_password:
            raise serializers.ValidationError({"password" : "New Password cannot be the same as old password"})

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"status" : "error", "message" : list(e.messages)})
        return attrs 
    
    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save() 
        return user


# create a forgot password serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs['email']

        user = User.objects.filter(email=email.lower()).first()
        if not user:
            raise serializers.ValidationError({"User" : "user not found"})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        code = PasswordForget.objects.create(user=user)

        send_mail(
            subject="Password Reset OTP",
            message = f"Your Password Rest OTP is: {code.otp}",
            from_email= "noreply@example.com",
            recipient_list= [user.email],
            fail_silently=False
        )

        return user

# create a serializer to retrieve forgotten password
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    otp = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        password = attrs['password']

        user = User.objects.filter(email=email.lower()).first()
        if not user:
            raise serializers.ValidationError({"Email" : "Email Does not exist"})
        
        code = PasswordForget.objects.get(user=user, otp=otp)
        if not code or str(otp) != str(code.otp):
            raise serializers.ValidationError({"OTP" : "Wrong OTP "})

        try:
            validate_password(password, user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"message" : list(e.message)})
        
        attrs['password'] = password
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.validated_data['user']

        user.set_password(password)
        user.save()
        return user

