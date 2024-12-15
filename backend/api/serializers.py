from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Note, Profile, Appointment, AdministratorAction

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Include role in JWT token payload
        data["role"] = self.user.profile.role
        return data

class UserSerializer(serializers.ModelSerializer):
    # Lazy import of ProfileSerializer
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False)

    class Meta:
        model = User
        fields = ["id", "username", "password", "profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)

        if profile_data:
            # Create profile only if one doesn't exist
            Profile.objects.get_or_create(user=user, defaults=profile_data)
        else:
            # Ensure a default profile is created only if none exists
            Profile.objects.get_or_create(user=user, role='relief_recipient')

        return user


class ProfileSerializer(serializers.ModelSerializer):
    # Lazy import of UserSerializer
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'full_name', 'contact_number', 'address']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class AppointmentSerializer(serializers.ModelSerializer):
    relief_recipient = UserSerializer(read_only=True)
    consultant = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'relief_recipient', 'consultant', 'date_time', 'status']


class AdministratorActionSerializer(serializers.ModelSerializer):
    administrator = UserSerializer(read_only=True)
    user_affected = UserSerializer(read_only=True)

    class Meta:
        model = AdministratorAction
        fields = ['id', 'administrator', 'user_affected', 'action_taken', 'action_date']
