from django.contrib import admin
from .models import Employee, Customer, Movie, Cinema, Concession_stand, Show_time, Ticket, Order, Transaction_receipt
# Register your models here.

admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(Cinema)
admin.site.register(Concession_stand)
admin.site.register(Show_time)
admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(Transaction_receipt)
