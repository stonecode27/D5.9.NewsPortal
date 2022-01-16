from django.forms import DateInput


class DateInputWidget(DateInput):
    input_type = 'date'