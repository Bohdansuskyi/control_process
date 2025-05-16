from django.shortcuts import render

def index(request):
    return render(request,"app/index.html")

def info(request):
    return render(request,"app/info.html")

def charts(request):
    return render(request,"app/charts.html")