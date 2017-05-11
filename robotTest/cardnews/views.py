from .models import Cardnews
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm
from django.http import JsonResponse

import socket

# Create your views here.
def index(request):
    test = Cardnews(tendency=1, title="쿵짝쿵짝 도천 천곡", target="한겨례", article="best in the world", articleUrl="knq1130@naver.com",publish_time="9999-12-31 23:59:59", collecting_time="9999-12-31 23:59:59")
    test.save()
    news_datas = Cardnews.objects.all()
    return render(request,'cardnews/index.html',{'news_datas':news_datas})

def a(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #clientSocket()
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            keyword = form.cleaned_data['keyword']
            tendency = form.cleaned_data['tendency']
            dataSet = (keyword, tendency)

            clientSocket(dataSet)
            return HttpResponseRedirect('cardnews/a.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'cardnews/a.html', {'form': form})

def clientSocket(dataSet):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 8090

    # connection to hostname on the port.
    s.connect((host, port))

    # Receive no more than 1024 bytes
    # msg = 'Thank you for' + "\r\n"
    keyword, tendency = dataSet
    msg = keyword + ',' + tendency

    s.send(msg.encode('utf8'))
    # s.send(msg)

    s.close()





