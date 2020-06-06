from django.shortcuts import render

# Create your views here.
def report_shift(request):

    return render(request, 'report_shift.html')