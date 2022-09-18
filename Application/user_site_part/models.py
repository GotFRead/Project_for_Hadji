from django.db import models

# Create your models here.

import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.utils import timezone
from django.dispatch import receiver
# Create your models here.


class Visit(models.Model):
    date = models.DateField(verbose_name='Дата визита',
                            help_text='Выберите дату приема',)

    time_start_visit = models.TimeField(verbose_name='Время начала визита',
                                        help_text='Выберите время начала приема',)

    time_end_visit = models.TimeField(verbose_name='Время окончания визита',
                                      help_text='Выберите время окончания приема',)

    who_visit = models.ForeignKey('Client',
                                  verbose_name='ФИО клиент',
                                  help_text='Введите ФИО клиента',
                                  on_delete=models.DO_NOTHING,
                                  null=True)

    who_accept = models.ForeignKey('Staff',
                                   verbose_name='Обслуживал:',
                                   help_text='Выберите кто обслуживал',
                                   on_delete=models.CASCADE,
                                   null=True)

    summ_visit = models.IntegerField(verbose_name='Сумма посещения',
                                     help_text='Введите сумму посещения')

    service = models.ForeignKey('Service',
                                verbose_name='Услуга',
                                help_text='Выберите услуги',
                                on_delete=models.PROTECT)

    status = models.CharField(max_length=20,
                              verbose_name='Статус приема',
                              help_text='Введиет статус приема',
                              null=True)

    class Meta:
        verbose_name_plural = 'Посещения'

    def check_overlap(self, fixed_time_start, fixed_time_end, start_time, end_time):
        results = False
        if start_time != fixed_time_start and end_time != fixed_time_end:
            results = True
        elif start_time == fixed_time_end and start_time != fixed_time_start:
            results = True
        elif fixed_time_start < start_time < fixed_time_end:
            results = False

        return results

    def clean(self):
        if self.time_end_visit <= self.time_start_visit:
            raise ValidationError('Окончания приема должна быть позднее, начала приема')

        visits = Visit.objects.filter(date=self.date)

        if visits.exists():
            for visit in visits:
                if self.check_overlap(visit.time_start_visit, visit.time_end_visit, self.time_start_visit, self.time_end_visit):
                    raise ValidationError(f'Выбранная дата {str(self.date)}и время приема {str(self.time_start_visit)} ,и время окончания {str(self.time_end_visit)} занято другим клиентом ')

    def __str__(self):
        return str(self.date)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=40,
                                  verbose_name='Имя',
                                  help_text='Введите имя')

    last_name = models.CharField(max_length=40,
                                 verbose_name='Фамилия',
                                 help_text='Введите фамилию')

    last_last_name = models.CharField(max_length=40,
                                      verbose_name='Отчество',
                                      help_text='Введите отчество')

    number = models.CharField(max_length=100,
                              help_text='Укажите номер телефона',
                              verbose_name='Номер телефона')

    address = models.CharField(max_length=100,
                               help_text='Укажите адрес',
                               verbose_name='Адрес')

    advert_status = models.CharField(max_length=100,
                                     help_text='Укажите статус рекламы',
                                     verbose_name='Статус рекламы')

    class Meta:
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return str(self.last_name)


@receiver(post_save, sender=User)
def create_user_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_client(sender, instance,**kwargs):
    instance.client.save()


class Service(models.Model):
    type_service = models.CharField(max_length=30,
                                    verbose_name='Тип услуги',
                                    help_text='Выберите статус договора')

    service_description = models.TextField(max_length=1500,
                                           verbose_name='Описание услуги',
                                           help_text='Введите описание услуги')

    short_service_description = models.TextField(max_length=150,
                                                 verbose_name='Короткое описание услуги',
                                                 help_text='Введите короткое описание услуги',
                                                 null=True)

    staff_list = models.ManyToManyField('Staff',
                                        help_text='Выберите специалиста',
                                        verbose_name='Cпециалисты')

    class Meta:
        verbose_name_plural = 'Услуги'

    def get_absolute_url(self):
        return reverse('service-details', args=[str(self.id)])

    def __str__(self):
        return str(self.type_service)


class Contract(models.Model):
    type_contract = models.CharField(max_length=20,
                                     verbose_name='Тип договора',
                                     help_text='Введите тип контракта')

    client_side = models.ForeignKey('Client',
                                    on_delete=models.CASCADE,
                                    help_text='Выберите клиента',
                                    null=True)

    who_accept = models.ForeignKey('Staff',
                                   on_delete=models.CASCADE,
                                   null=True)

    description_contract = models.TextField(max_length=100,
                                            verbose_name='Описание контракта',
                                            help_text='Введите описание контракта')

    class Meta:
        verbose_name_plural = 'Контракты'

    def __str__(self):
        return str(id)


class Staff(models.Model):
    first_name = models.CharField(max_length=40,
                                  verbose_name='Имя',
                                  help_text='Введите имя')

    last_name = models.CharField(max_length=40,
                                 verbose_name='Фамилия',
                                 help_text='Введите фамилию')

    last_last_name = models.CharField(max_length=40,
                                      verbose_name='Отчество',
                                      help_text='Введите отчество')

    address = models.CharField(max_length=100,
                               help_text='Укажите адрес',
                               verbose_name='Адрес')

    number = models.CharField(max_length=100,
                              help_text='Укажите номер телефона',
                              verbose_name='Номер телефона')

    specialization = models.CharField(max_length=100,
                                      verbose_name='Специальность',
                                      help_text='Введите специальность')

    type_staff = models.CharField(max_length=20,
                                  verbose_name='Тип персонала',
                                  help_text='Введите тип персонала',
                                  null=True)

    class Meta:
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return str(self.last_name)


class BioStaff(models.Model):
    staff = models.OneToOneField(Staff,
                                 verbose_name='Персонал',
                                 on_delete=models.CASCADE,
                                 primary_key=True)

    bio = models.TextField(max_length=200,
                           verbose_name='Описание персонала',
                           help_text='Введите описание персонала')

    root_to_image = models.CharField(max_length=150,
                                     verbose_name='Адрес до фото персонала',
                                     help_text='Введите адрес к фото персонала',
                                     null=True)

    class Meta:
        verbose_name_plural = 'Биография персонала'

    def __str__(self):
        return str(self.staff)


class PayrollPreparation(models.Model):
    staff = models.ForeignKey('Staff',
                              on_delete=models.CASCADE)

    summ_payroll = models.IntegerField(verbose_name='Заработная плата',
                                       help_text='Введите сумму')

    month = models.DateField(verbose_name='Месяц',
                             help_text='Введите месяц')

    status = models.CharField(verbose_name='Статус выдачи',
                              help_text='Введите статус выдачи',
                              max_length=20)

    class Meta:
        verbose_name_plural = 'Зарплаты'

    def __str__(self):
        return str(self.month)


class PriceVisit(models.Model):
    service = models.ForeignKey('Service',
                                on_delete=models.CASCADE,
                                help_text='Выберите услугу',
                                verbose_name='Услуга')

    staff = models.ForeignKey('Staff',
                              on_delete=models.CASCADE,
                              help_text='Выберите персонал',
                              verbose_name='Персонал')

    price = models.IntegerField(help_text='Установить цену',
                                verbose_name='Цена')

    class Meta:
        verbose_name_plural = 'Цены'

    def __str__(self):
        return str(self.service)

