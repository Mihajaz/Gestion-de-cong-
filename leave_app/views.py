from django.shortcuts import render




# Create your views here.
def home(request):
    return render(request, 'home.html')

def validation(request):
    return render(request,'validation.html')


