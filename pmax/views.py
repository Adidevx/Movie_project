from django.shortcuts import render, redirect
from django.http import HttpResponse
from pmax.models import User, Movie,Show, Review, Booking
from django.views.decorators.cache import never_cache

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
            return render(request,"./pmax/login.html",{"error":"Invalid credentials"})
    else:
        return render(request,"./pmax/login.html")

@never_cache
def Dashboard(request):
    user_id = request.session.get("user-id")
    if not user_id:
        return redirect("Login")
    
    movies = Movie.objects.all()
    return render(request, "./pmax/dashboard.html",{"movies":movies})

@never_cache
def logout(request):
    request.session.flush()
    return redirect("Login")

@never_cache
def movie_detail(request,movie_id):
    user_id = request.session.get('user-id')
    if not user_id:
        return redirect("Login")

    movie = Movie.objects.get(id=movie_id)
    show = Show.objects.filter(movie=movie)
    review = Review.objects.filter(movie=movie)

    if request.method=="POST":
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        user= User.objects.get(id = user_id)
        Review.objects.create(
            movie = movie,
            user = user,
            comment = comment,
            rating = rating
        )
        return redirect(f"/movie_detail/{movie_id}")
    return render(request,"./pmax/movie_detail.html",{"movie":movie,"shows":show,"reviews":review})

@never_cache
def book_show(request,show_id):
    user_id = request.session.get('user-id')
    if not user_id:
        return redirect('login')
    show = Show.objects.get(id=show_id)

    rows= ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U',
          'V','W','X','Y','Z']
    seats = []
    seats_per_row = 10
    total_seats = show.available_seats
    count= 0

    for row in rows:
        for num in range(1,seats_per_row+1):
            if count>=total_seats:
                break
            seats.append(row+str(num))
            count = count+1
        if count>=total_seats:
            break

    #Available Slots
    bookings = Booking.objects.filter(show=show)
    booked_seats = []
    for b in bookings:
        booked_seats.extend(b.seats.split(","))
    
    if request.method == "POST":
        selected_seats = request.POST.get("selected_seats")

        if not selected_seats:
            return render(request,"./pmax/seat_selection.html", {'show':show,'booked_seats':booked_seats,
                                                        'seats':seats, 'error':'Please select atleast one seat'})
        seat_list = selected_seats.split(',')
        
        if len(seat_list)> show.available_seats:
            return render(request,'./pmax/seat_selection.html',{'show':show,'booked_seats':booked_seats,
                        'seats':seats, 'error':"Not enough seats"})
        
        totalprice = len(seat_list)*show.price
        user = User.objects.get(id=user_id)
        Booking.objects.create(
            user=user,
            show=show,
            seats=selected_seats,
            totalprice=totalprice
        )
        show.available_seats = show.available_seats - len(seat_list)
        show.save()
        return render(request,"./pmax/Success.html")
    return render(request, "./pmax/seat_selection.html",{'show':show ,'booked_seats': booked_seats, 'seats':seats})