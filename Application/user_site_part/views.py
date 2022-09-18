from django.contrib.auth import login, logout
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, HttpResponseNotModified, \
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseGone, HttpResponseServerError

from datetime import datetime
from .services import *

from .forms import *


def m304():
    return HttpResponseNotModified()


def m400():
    return HttpResponseBadRequest("<h2>Запрос задан некорректно</h2>")


def m403():
    return HttpResponseForbidden( "<h2>Доступ к странице запрещен</h2>")


def m404():
    return HttpResponseNotFound("<h2>Данные по запросу отсутсвуют</h2>")


def m405():
    return HttpResponseNotAllowed("<h2>Доступ запрещен</h2>")


def m410():
    return HttpResponseGone("<h2>Данная страница удалена</h2>")


def m500():
    return HttpResponseServerError("<h2>Что-то пошло не так</h2>")


def test(request):
    try:
        return render(request, 'application/123.html')
    except Service.DoesNotExist:
        return HttpResponseRedirect('/main/')


def main_user_form(request):
    services, staff_list, staff_bio = get_info_main_form_user()
    return render(request, 'application/main_form_user.html', {'services': services,
                                                               'object_staff': staff_list,
                                                               'staff_bio': staff_bio})


def staff_main_form(request):
    services = Service.objects.all()
    staff = Staff.objects.all()
    return render(request, 'application/main.html', {'services': services,
                                                     'staff': staff})


def staff_contract_form(request):
    if request.method == 'POST':
        pass
    else:
        list_non_processed = Contract.objects.filter(who_accept='')

        return render(request, 'application/staff_contract.html', {'non_process': list_non_processed})


def create_an_appointment(request, ser_pk, s_pk):
    if request.method == 'GET':
        services, staff = get_info_for_appointment(ser_pk, s_pk)

        if not services:
            return HttpResponseForbidden('<h2> Данное посещение сейчас недоступно </h2>')
        elif not staff:
            return HttpResponseForbidden('<h2> Данная услуга сейчас недоступна </h2>')

        return render(request, 'application/create_an_appointment.html', {'staff': staff,
                                                                          'services': services})

    if request.method == 'POST':
        set_appointment(request, ser_pk, s_pk)
        return render(request, 'application/create_an_appointment.html', {'staff': staff,
                                                                          'service': services})


def choose_main_form(request):
    if check_role_user(verified_user=request.user.username) == 'user':
        print('user')
        return main_user_form(request)
    elif check_role_user(verified_user=request.user.username) == 'staff':
        print('staff')
        return staff_main_form(request)
    else:
        return HttpResponse('<h2>Не сработало</h2>')


def create_contract(request):
    if check_role_user(verified_user=request.user.username) != 'user':
        try:
            if request.method == 'POST':
                object_contract = Contract()
                object_contract.type_contract = request.POST.get('type')
                object_contract.description_contract = request.POST.get('description')

                render(request, 'application/successfully_contract.html')

            return render(request, 'application/appointment.html', {'visits': visit,
                                                                    'services': services})
        except Service.DoesNotExist:
            return HttpResponseForbidden('<h2> Данный сервис недоступен на данный момент </h2>')

        except Visit.DoesNotExist:
            return HttpResponseForbidden('<h2> Данный посещение сейчас недоступно </h2>')


def registration(request):
    try:
        if request.method == 'POST':
            if create_user(request):
                return HttpResponseRedirect('/')
            else:
                return render(request, 'Register.html')
        else:
            return render(request, 'Register.html')

    except ValueError:
        return render(request, 'Register.html')


def authorization(request):
    try:
        if request.method == 'POST':
            user = authentication(request)

            if user:
                login(request, user)
                return HttpResponseRedirect('/main')
            else:
                return render(request, 'Authorizations.html')
        else:
            return render(request, 'Authorizations.html')

    except ValueError:
        return HttpResponseRedirect('')


def service_details(request, pk):
    try:
        object_service, object_service_staff, staff_bio = get_info_service_details(pk)
        return render(request, 'application/service_detail.html', {'service': object_service,
                                                                   'object_staff': object_service_staff,
                                                                   'objects_bio': staff_bio})

    except Service.DoesNotExist:
        return HttpResponseRedirect('main/')

    except ValueError:
        return HttpResponseRedirect('main/')


class Registr(CreateView):
    form_class = RegisterForm
    template_name = 'Register.html'
    success_url = reverse_lazy('authorization')


class ServiceDetailView(generic.DetailView):
    model = Service
    #template_name = 'service_detail.html'
    context_object_name = 'service'
    paginate_by = 1

