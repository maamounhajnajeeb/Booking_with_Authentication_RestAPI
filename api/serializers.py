from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate

from .models import Booking

User = get_user_model()

class SignUpSerializer(serializers.Serializer):
    # fields
    username = serializers.CharField(max_length=64, min_length=6)
    email = serializers.CharField(max_length=64, min_length=12)
    password = serializers.CharField(max_length=64, min_length=6)
    
    # errors (as class attributes)
    username_err_msg = {
        "username" : "Username should contain alphnumeric characters only (letters and numbers)"
        }
    repeated_username_err = {"username" : "Username already exists"}
    repeated_email_err = {"email" : "Email already exists"}
    
    def validate(self, attrs):
        email, username = attrs.get("email"), attrs.get("username")
        
        if not username.isalnum():
            raise serializers.ValidationError(
                self.username_err_msg
            )
        
        repeated_username, repeated_email = self.repeated_query(email, username)
        terms = (repeated_username, repeated_email)
        errors = (self.repeated_username_err, self.repeated_email_err)
        
        for i in range(len(terms)):
            self.repeating_test(terms[i], errors[i])
        
        return attrs
    
    def repeated_query(self, email, username):
        return User.objects.filter(username=username), User.objects.filter(email=email)
    
    def repeating_test(self, repeated_term, error):
        if repeated_term.exists():
            raise serializers.ValidationError(
                error
            )
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64, min_length=6, label="Username", write_only=True)
    password = serializers.CharField(max_length=64, min_length=6, label="Password", write_only=True)
    
    def validate(self, attrs):
        username, password = attrs.get("username"), attrs.get("password")
        
        if not(username or password):
            raise serializers.ValidationError(
                '"Both" Username and Password are required', code="authorization"
            )
        
        user = authenticate(
            request=self.context.get("request"), username=username, password=password
            )
        
        if not user:
            raise serializers.ValidationError(
                "Access denied, wrong username of password", code="authorization"
            )
        
        attrs["user"] = user
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=256, min_length=8)
    
    def validate(self, attrs):
        
        user = User.objects.get(email=attrs.get("email"))
        
        if not user:
            raise serializers.ValidationError(
                "There is no account with this email", code="authorization"
            )
        
        attrs["user"] = user
        return attrs
    
class ResetPassSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=64, min_length=6)
    password2 = serializers.CharField(max_length=64, min_length=6)

    def validate(self, attrs):
        password1, password2 = attrs.get("password1"), attrs.get("password2")
        
        if not password1 == password2:
            raise serializers.ValidationError(
                "The two passwords are not the same value", code="authorization"
            )
        
        return attrs

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email",
        )

class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = "__all__"


# class ChargeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentTable
#         fields = "__all__"
        