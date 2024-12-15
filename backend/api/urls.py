from django.urls import path
from . import views

urlpatterns = [
    # Notes routes
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),

    # Profile routes
    path("profile/", views.ProfileDetail.as_view(), name="profile-detail"),

    # Appointment routes
    path("appointments/", views.AppointmentListCreate.as_view(), name="appointment-list-create"),
    path("appointments/<int:pk>/", views.AppointmentDetail.as_view(), name="appointment-detail"),

    # Administrator Action routes
    path("admin-actions/", views.AdministratorActionList.as_view(), name="admin-action-list"),
    path("admin-actions/create/", views.AdministratorActionCreate.as_view(), name="admin-action-create"),
]


