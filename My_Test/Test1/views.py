from django.shortcuts import render
from django.http import HttpResponse
# from .models import Candidate
from .models import Card_Text
# Create your views here.
# def index(request):
#     candidates = Candidate.objects.all()
#     context={'candidates':candidates}
#     return render(request,"Test1/index.html",context)
    # return HttpResponse(str)
def index(request):
    card_texts = Card_Text.objects.all()
    context = {'card_texts': card_texts}
    return render(request,"Test1/index.html",context)