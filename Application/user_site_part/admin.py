import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *
# Register your models here.


#class EventAdmin(admin.ModelAdmin):
#    list_display = ['day', 'start_time', 'end_time', 'notes']
#    change_list_template = r'/admin/change_list.html'
#
#    def changelist_view(self, request, extra_context=None):
#        after_day = request.GET.get('day__gte', None)
#        extra_context = extra_context or {}
#
#        if not after_day:
#            d = datetime.datetime.today()
#
#        else:
#            try:
#                split_after_day = after_day.split('-')
#                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
#            except:
#                d = datetime.date.today()
#
#        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
#        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
#        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
#                                       day=1)  # find first day of previous month
#
#        last_day = calendar.monthrange(d.year, d.month, day=last_day[1])
#        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])
#        next_month = next_month + datetime.timedelta(days=1)
#        next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)
#
#        extra_context['previous_month'] = reverse('admin: events_events_changelist') \
#                                         + '?day__gte='+ str(previous_month)
#
#        extra_context['next_month'] = reverse('admin: events_event_changelist') \
#                                      + '?day__gte=' + str(next_month)
#
#        calendar = HTMLCalendar()
#
#        html_calendar = calendar.formatmonth(d.year, d.month, withyear=True)
#        html_calendar = html_calendar.replace('<td', '<td width="150" height="150"')
#
#        extra_context['calendar'] = mark_safe(html_calendar)
#
#        return super(EventAdmin, self).changelist_view(request, extra_context)


@admin.register(Visit)
class AdminVisit(admin.ModelAdmin):
    list_display = ('time_start_visit', 'time_end_visit', 'who_visit',
                    'who_accept', 'summ_visit', 'service',
                    'date')

    list_filter = ('time_start_visit', 'time_end_visit', 'who_visit',
                   'who_accept', 'summ_visit', 'service',
                   'date')


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'last_last_name',
                    'number', 'address', 'advert_status')

    list_filter = ('advert_status',)


@admin.register(Service)
class AdminService(admin.ModelAdmin):
    list_display = ('type_service', 'service_description', 'short_service_description')

    list_filter = ('type_service', 'service_description', 'staff_list', 'short_service_description')


@admin.register(Contract)
class AdminContact(admin.ModelAdmin):
    list_display = ('type_contract', 'who_accept', 'description_contract', 'client_side')

    list_filter = ('type_contract', 'who_accept', 'description_contract', 'client_side')


@admin.register(Staff)
class AdminStaff(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'last_last_name',
                    'number', 'address', 'specialization')

    list_filter = ('last_name', 'specialization')


@admin.register(BioStaff)
class AdminBioStaff(admin.ModelAdmin):
    list_display = ('staff', 'bio', 'root_to_image')
    list_filter = ('staff',)


@admin.register(PayrollPreparation)
class AdminPayrollPreparation(admin.ModelAdmin):
    list_display = ('staff', 'summ_payroll', 'month',
                    'status')

    list_filter = ('staff', 'month', 'status')


@admin.register(PriceVisit)
class AdminPriceVisit(admin.ModelAdmin):
    list_display = ('service', 'staff', 'price')

    list_filter = ('service', 'staff', 'price')



