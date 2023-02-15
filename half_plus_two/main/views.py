from django.views.generic.list import ListView
from django.shortcuts import redirect, render
from .forms import RequestsFormField
from django.utils import timezone
from .models import Request
import requests

def tf_api_request(payload: list):
    tf_request_data = {"instances": payload}

    url = 'http://tf:8501/v1/models/half_plus_two:predict'
    response = requests.post(url, json=tf_request_data)
    
    response_timestamp = timezone.now()
    tf_api_response = response.json()
    return {'response': tf_api_response, 'response_time': response_timestamp}


def half_plus_three(request):
    if request.method == 'POST':
        request_timestamp = timezone.now()
        form = RequestsFormField(request.POST)

        if form.is_valid():
            data = request.POST['request']
            payload = [float(x) for x in data.split(',')]
            tf_request = tf_api_request(payload)            

            reqInstance = Request(request=data, response=tf_request['response'], request_time=request_timestamp, response_time=tf_request['response_time'])
            reqInstance.save()


    form = RequestsFormField()
    context = {'form': form}
    return redirect('request-list')

class RequestListView(ListView):
    model = Request
    ordering = ['-request_time']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RequestsFormField()
        return context

