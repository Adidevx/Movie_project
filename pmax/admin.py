from django.contrib import admin
from pmax.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Movie)  
admin.site.register(Theater)
admin.site.register(Show)
admin.site.register(Review)
admin.site.register(Booking)