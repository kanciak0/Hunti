from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, ProfileSerializer, AppointmentSerializer, \
    AdministratorActionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, Profile, Appointment, AdministratorAction

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the profile related to the current user
        return self.request.user.profile

class AppointmentListCreate(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter appointments for the current user (either as recipient or consultant)
        user = self.request.user
        return Appointment.objects.filter(
            models.Q(relief_recipient=user) | models.Q(consultant=user)
        )

    def perform_create(self, serializer):
        # Ensure the correct user is assigned as either relief_recipient or consultant
        user = self.request.user
        role = user.profile.role
        if role == 'relief_recipient':
            serializer.save(relief_recipient=user)
        elif role == 'consultant':
            serializer.save(consultant=user)
        else:
            print("Invalid role for appointment creation.")

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter appointments for the current user (either as recipient or consultant)
        user = self.request.user
        return Appointment.objects.filter(
            models.Q(relief_recipient=user) | models.Q(consultant=user)
        )

class AdministratorActionList(generics.ListAPIView):
    queryset = AdministratorAction.objects.all()
    serializer_class = AdministratorActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow administrators to view actions
        if self.request.user.profile.role == 'administrator':
            return AdministratorAction.objects.all()
        else:
            return AdministratorAction.objects.none()

class AdministratorActionCreate(generics.CreateAPIView):
    queryset = AdministratorAction.objects.all()
    serializer_class = AdministratorActionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.profile.role == 'administrator':
            serializer.save(administrator=self.request.user)
        else:
            print("User is not authorized to create administrator actions.")
