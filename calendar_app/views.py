from django.shortcuts import render

# Create your views here.


# First Page - App Install Prompt
def index(request):
    return render(request, 'index.html')

# Second Page - Calendar with Slider
def calendar_view(request):
    return render(request, 'calendar.html')

# def demo(request):
#     return render(request,'demo.html')