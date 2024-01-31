from django.shortcuts import render


# Create your views here.
def index(re):
    return render(re,
                  'contact/index.html')
