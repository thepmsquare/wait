from django.urls import path

from tracker.views import SignUpView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("all_entries/", views.all_entries, name="all_entries"),
    path("delete_entry/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path("export/csv/", views.export_entries_csv, name="export_entries_csv"),
]
