from django.shortcuts import render, redirect
from django.http import HttpResponse
from pmax.models import User, Movie
# Create your views here.
def Home(request):
    return render(request,"./pmax/home.html")

def Signup(request):
    if request.method=="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "./pmax/signup.html",{"error":"Username already exist"})
        else:
            User.objects.create(username=username, password=password, email=email)
            return redirect("Login")
    else: 
        return render(request, "./pmax/signup.html")
    
def Login(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username,password=password)
            request.session["user-id"] = user.id
            request.session["user-name"] = user.username
            return redirect("dashboard")
        except:
            return render("./pmax/login.html",{"error":"Invalid credentials"})
    else:
        return render(request,"./pmax/login.html")
    
def Dashboard(request):
    user_id = request.session.get("user-id")
    if not user_id:
        return redirect("Login")
    
    movies = Movie.objects.all()
    return render(request, "./pmax/dashboard.html",{"movies":movies})