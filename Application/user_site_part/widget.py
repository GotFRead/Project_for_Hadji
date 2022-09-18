from django.forms import DateTimeInput


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'templates/application/xdsoft_datetimepicker.html'


