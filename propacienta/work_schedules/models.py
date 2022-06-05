from datetime import date, datetime, time, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import json_to_times


class WorkDay(models.Model):
    """Модель рабочего дня врача."""
    TIMESLOT = 15
    APPOINTMENT_DURATION_CHOICES = [
        (15, _("15 минут")),
        (30, _("30 минут")),
        (45, _("45 минут")),
        (60, _("60 минут")),
    ]
    date = models.DateField(_("Дата"))
    doctor = models.ForeignKey(
        "doctors.doctor",
        related_name="workdays",
        verbose_name=_("Врач"),
        on_delete=models.CASCADE,
        # editable=False,
    )
    since = models.TimeField(_("Начало периода работы"))
    to = models.TimeField(_("Окончание периода работы"))
    hospital = models.ForeignKey(
        "hospitals.hospital",
        related_name="workdays",
        verbose_name=_("Клиника"),
        on_delete=models.CASCADE,
        # editable=False,
    )
    appointment_duration = models.IntegerField(
        _("Продолжительность приема в минутах"),
        choices=APPOINTMENT_DURATION_CHOICES,
        default=15,
        # editable=False,
    )
    timeslotmask = models.CharField(
        _("Маска занятости рабочего времени"),
        max_length=60 * 24,
        help_text="""Последовательность 0 и 1 для фильтрации уже занятых временных слотов,
        где 0 - свободный {timeslot}-ти минутный интервал, 1 - занятый. Максимальная длина
        соответсвует максимальному количеству {timeslot}-ти минутных интервалов в сутках.""".format(
            timeslot=TIMESLOT
        ),
        blank=True
    )
    breaks = models.JSONField(
        _("Перерывы"),
        help_text="""Перерывы рабочего времени,
        например {"breaks": [{"end": "1215", "start": "1200"}, {"end": "1545", "start": "1515"}]}""",
        default=dict
    )
    have_a_rest_timeslotmask = models.CharField(
        _("Маска перерывов рабочего времени"),
        max_length=60 * 24,
        blank=True,
        default=""
    )

    class Meta:
        verbose_name = "Рабочий день"
        verbose_name_plural = "Рабочие дни"
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Рабочий период {} с {} по {} для {} в {}".format(
            self.date, self.since, self.to, self.doctor, self.hospital
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            breaks = json_to_times(self.breaks)
            self.timeslotmask = self.empty_timeslotsmask
            if "breaks" in breaks:
                for (time_start, time_end) in breaks["breaks"]:
                    self.add_break(time_start, time_end)
            self.have_a_rest_timeslotmask = self.timeslotmask
        super().save(*args, **kwargs)

    @property
    def appointment_duration_in_timeslots(self):
        return int(self.appointment_duration / self.TIMESLOT)

    @property
    def return_free_timeslots(self):
        free_timeslots_idx = [
            i for i in range(
                0, len(self.timeslotmask), self.appointment_duration_in_timeslots
            ) if self.timeslotmask[i] == "0"
        ]
        _date = date.today()
        return [
            (
                datetime.combine(_date, self.since) + timedelta(minutes=i*self.TIMESLOT)
            ).time() for i in free_timeslots_idx
        ]

    def return_free_timeslots_objects(self):
        class TimeSlot:
            def __init__(self, timeslot) -> None:
                self.timeslot = timeslot
        return [TimeSlot(i) for i in self.return_free_timeslots]

    @property
    def empty_timeslotsmask(self):
        to = timedelta(
            hours=self.to.hour,
            minutes=self.to.minute,
            seconds=self.to.second
        )
        since = timedelta(
            hours=self.since.hour,
            minutes=self.since.minute,
            seconds=self.since.second
        )
        duration = to - since
        timeslots_count = duration.seconds / (self.TIMESLOT * 60)
        return "0" * int(timeslots_count)

    def check_free_timeslot(self, timeslot: time) -> bool:
        return timeslot in self.return_free_timeslots

    def change_timeslot(self, timeslot, mask="1") -> bool:
        since = timedelta(
            hours=self.since.hour,
            minutes=self.since.minute,
            seconds=self.since.second
        )
        slot = timedelta(
            hours=timeslot.hour,
            minutes=timeslot.minute,
        )
        duration = slot - since
        timeslots_count = int(duration.seconds / (self.TIMESLOT * 60))
        try:
            self.timeslotmask = "{}{}{}".format(
                self.timeslotmask[:timeslots_count],
                mask * self.appointment_duration_in_timeslots,
                self.timeslotmask[timeslots_count + self.appointment_duration_in_timeslots:]
            )
            return True
        except:
            return False

    def reserve_timeslot(self, timeslot) -> bool:
        if not self.check_free_timeslot(timeslot):
            return False
        res = self.change_timeslot(timeslot)
        self.save()
        return res

    def cancel_reserve_timeslot(self, timeslot) -> bool:
        if self.check_free_timeslot(timeslot):
            return False
        res = self.change_timeslot(timeslot, "0")
        self.save()
        return res

    def add_break(self, start, end):
        since = timedelta(
            hours=self.since.hour,
            minutes=self.since.minute,
            seconds=self.since.second
        )
        start = timedelta(
            hours=start.hour,
            minutes=start.minute,
        )
        end = timedelta(
            hours=end.hour,
            minutes=end.minute,
        )
        duration = start - since
        timeslots_count = int(duration.seconds / (self.TIMESLOT * 60))
        break_duration = end - start
        break_duration_in_timeslots = int(break_duration.seconds / (self.TIMESLOT * 60))
        try:
            self.timeslotmask = "{}{}{}".format(
                self.timeslotmask[:timeslots_count],
                "1" * break_duration_in_timeslots,
                self.timeslotmask[timeslots_count + break_duration_in_timeslots:]
            )
        except:
            return False


class NotWorkingPeriod(models.Model):
    REASON_CHOICES = [
        ("weekend", _("Выходной")),
        ("vacation", _("Отпуск")),
        ("disease", _("Болезнь")),
        ("pregnancy", _("Беременность")),
        ("business_trip", _("Коммандировка"))
    ]
    reason = models.CharField(
        _("Причина"),
        choices=REASON_CHOICES,
        default="weekend",
        max_length=20
    )
    doctor = models.ForeignKey(
        "doctors.doctor",
        related_name="not_working_periods",
        verbose_name=_("Врач"),
        on_delete=models.CASCADE,
        # editable=False,
    )
    hospital = models.ManyToManyField(
        "hospitals.hospital",
        related_name="not_working_periods",
        verbose_name=_("Клиники"),
    )
    since = models.DateField(_("Дата начала"), null=True, blank=True)
    to = models.DateField(_("Дата окончания"), null=True, blank=True)
    is_open = models.BooleanField(
        _("Статус неоконченности периода"),
        default=True,
        help_text="Для фильтрации"
    )

    class Meta:
        verbose_name = "Нерабочий период"
        verbose_name_plural = "Нерабочие периоды"
        ordering = ["-id"]
