from django.http import HttpResponseForbidden

from .models import *
from django.contrib.auth import authenticate


def create_client(first_name, last_name, last_last_name,
                  number, address, advert_status):
    object_client = Client()

    object_client.first_name = first_name
    object_client.last_name = last_name
    object_client.last_last_name = last_last_name
    object_client.number = number
    object_client.address = address
    object_client.advert_status = advert_status
    object_client.save()
    print('клиент создан')


def check_role_user(verified_user):
    verified_user = User.objects.get(username=verified_user)

    if verified_user == 'staff':
        return 'staff'
    elif verified_user == 'user':
        return 'user'
    else:
        return 'guest'


def get_info_user(username, field):
    info_user = User.objects.get(username=username)
    return info_user


def get_price_service(service_id, staff_id):
    object_price_visit = PriceVisit.objects.get(service=service_id, staff=staff_id)
    return object_price_visit.price


def get_data_now():
    date = datetime.datetime.now()
    day_of_the_week = datetime.datetime.isoweekday()
    week = date.day/7
    month = date.month

    return date, day_of_the_week, week, month


def create_calendar():
    date, weekday, week, month = get_data_now()

    date_list = [iter for iter in range(1,32)]

    return date, weekday, week, month, date_list


def authentication(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    return user


def test_services():
    services = Service.objects.all()
    return services


def get_info_main_form_user():
    try:
        services = Service.objects.all()
        staff_list = Staff.objects.filter(specialization='Врач')
        staff_bio = BioStaff.objects.all()
        return services, staff_list, staff_bio

    except Service.DoesNotExist:
        return False


def get_info_service_details(pk):
    try:
        object_service = Service.objects.get(id=pk)

        object_service_staff = Service.objects.get(id=pk).staff_list.all()

        staff_bio = BioStaff.objects.all()

        return object_service, object_service_staff, staff_bio

    except Service.DoesNotExist:
        return False

    except BioStaff.DoesNotExist:
        return False


def create_user(request):
    try:
        # POST с формы
        username = request.POST.get('login')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        last_last_name = request.POST.get('last_last_name')
        password = request.POST.get('password')
        number = request.POST.get('number')
        address = request.POST.get('address')
        advert_status = 'Active'
        data_joined = datetime.datetime.now()

        # Создание пользователя
        object_user = User()

        object_user.username = username
        object_user.last_name = last_name
        object_user.first_name = first_name
        object_user.date_joined = data_joined
        object_user.password = password
        object_user.is_superuser = True
        object_user.save()
        print('пользователь создан')
        # Создание клиента
        create_client(first_name, last_name, last_last_name,
                      number, address, advert_status)
        return True

    except Exception:
        return False


def get_info_for_appointment(ser_pk, s_pk):
    try:
        staff = Staff.objects.get(id=s_pk)
        services = Service.objects.get(id=ser_pk)
        return services, staff

    except Service.DoesNotExist:
        return False, True

    except Staff.DoesNotExist:
        return True, False


def split_date_and_time(date_and_time: str ):
    split_datetime = date_and_time.split(' ')
    date, time = split_datetime[0], split_datetime[1]

    return date, time


def get_info_user(id_user):
    pass


def set_appointment(request, ser_pk, s_pk):
    date_and_time = request.POST.get('date_and_time')

    object_user = User.objects.get(username=request.user.username)

    date, time = split_date_and_time(date_and_time)

    object_visit = Visit()






