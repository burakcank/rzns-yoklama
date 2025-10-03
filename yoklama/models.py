from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    name = models.CharField(_("İsim"), max_length=100)
    created_at = models.DateTimeField(_("Kayıt Tarihi"), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Koro Üyesi")
        verbose_name_plural = _("Koro Üyeleri")


class Yoklama(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name=_("Koro Üyesi")
    )
    date = models.DateField(_("Tarih"), default=timezone.now)
    datetime = models.DateTimeField(_("Tarih ve Saat"), auto_now_add=True)
    present = models.BooleanField(_("Katıldı"), default=True)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {_('Katıldı') if self.present else _('Katılmadı')}"

    class Meta:
        ordering = ["-datetime"]
        unique_together = [
            "student",
            "date",
        ]  # Aynı gün için tekrar yoklama alma engellemesi
        verbose_name = _("Prova Katılımı")
        verbose_name_plural = _("Prova Katılımları")
