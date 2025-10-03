import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Student, Yoklama


def yoklama_page(request):
    students = Student.objects.all().order_by("name")
    return render(request, "yoklama/index.html", {"students": students})


@csrf_exempt
@require_http_methods(["POST"])
def check_in(request):
    try:
        data = json.loads(request.body)
        student_id = data.get("student_id")
        confirmed = data.get("confirmed", False)

        if not student_id:
            return JsonResponse(
                {"success": False, "error": _("Koro üyesi ID gereklidir")}, status=400
            )

        if not confirmed:
            return JsonResponse(
                {
                    "success": False,
                    "error": _(
                        "Lütfen yalnızca kendiniz için katılım kaydettiğinizi onaylayın"
                    ),
                },
                status=400,
            )

        student = get_object_or_404(Student, id=student_id)

        today = timezone.now().date()
        existing_record = Yoklama.objects.filter(student=student, date=today).first()

        if existing_record:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Bugün zaten provaya katılım kaydettiniz"),
                },
                status=400,
            )

        Yoklama.objects.create(student=student, date=today, present=True)

        return JsonResponse(
            {
                "success": True,
                "message": _("{} provaya katılım kaydetti").format(student.name),
                "check_in_time": timezone.now().isoformat(),
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": _("Geçersiz JSON verisi")}, status=400
        )
    except Exception:
        return JsonResponse(
            {"success": False, "error": _("Beklenmeyen bir hata oluştu")}, status=500
        )


def get_attendance_status(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        today = timezone.now().date()

        has_checked_in = Yoklama.objects.filter(
            student=student, date=today, present=True
        ).exists()

        return JsonResponse(
            {
                "success": True,
                "student_name": student.name,
                "has_checked_in": has_checked_in,
                "date": today.isoformat(),
            }
        )

    except Exception:
        return JsonResponse(
            {"success": False, "error": _("Koro üyesi bulunamadı")}, status=404
        )
