from django.urls import path

from . import views

app_name = "yoklama"

urlpatterns = [
    path("", views.yoklama_page, name="prova_katilim"),
    path("api/katilim-kaydet/", views.check_in, name="katilim_kaydet"),
    path(
        "api/katilim-durumu/<int:student_id>/",
        views.get_attendance_status,
        name="katilim_durumu",
    ),
]
