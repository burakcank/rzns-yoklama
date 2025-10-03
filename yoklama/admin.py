from django.contrib import admin

from .models import Student, Yoklama


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("name",)
    verbose_name = "Koro Üyesi"
    verbose_name_plural = "Koro Üyeleri"


@admin.register(Yoklama)
class YoklamaAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "datetime", "present")
    list_filter = ("date", "present", "datetime")
    search_fields = ("student__name",)
    date_hierarchy = "date"
    ordering = ("-datetime",)
    verbose_name = "Prova Katılımı"
    verbose_name_plural = "Prova Katılımları"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("student")
