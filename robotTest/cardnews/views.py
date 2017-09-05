from django.shortcuts import render
from .forms import SearchForm
from .models import cardnews
from urllib.request import urlretrieve

import socket

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            tendency = form.cleaned_data['tendency']
            dataSet = (keyword, tendency)
            received_newsdatas = clientSocketSendData(dataSet)
            newsdatas_list = received_newsdatas.split('*')
            cardnews_titles = newsdatas_list[0][2:].split('##')
            cardnews_articles = newsdatas_list[1][2:].split('##')
            cardnews_imgUrls = newsdatas_list[2][2:].split('##')

            for i in range(len(newsdatas_list)):
                news_data = cardnews(title=cardnews_titles[i], article=cardnews_articles[i], imgUrl=cardnews_imgUrls[i])
                news_data.save()


            cardnews_data = cardnews.objects.order_by('-publish_time')[:3]  # 최신순으로 정렬 3개만 뽑기
            count = len(newsdatas_list)-1

            for data in cardnews_data:
                    try:
                        urlretrieve(cardnews_imgUrls[count], "cardnews\static\img\img" + str(data.id) + ".jpg")
                        count -= 1
                    except:
                        print("저장 실패")

            return render(request, 'cardnews/index.html', {'news_datas':cardnews_data,'form': form})

    # # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
        form.fields['keyword'].widget.attrs['placeholder']='Enter keyword'
        form.fields['tendency'].widget.attrs['placeholder'] = 'Enter tendency'

    return render(request, 'cardnews/index.html', {'form': form})

def clientSocketSendData(dataSet):
    # create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # get local machine name
        host = socket.gethostname()
        port = 8084

        # connection to hostname on the port.
        s.connect((host, port))

        # Receive no more than 1024 bytes
        keyword, tendency = dataSet
        msg = keyword + ',' + tendency

        s.send(msg.encode('utf8'))
        received = s.recv(9096).decode('utf8')
        print(received)
        return received


