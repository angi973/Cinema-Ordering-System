from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import *
from django.conf import settings
from django.core.mail import send_mail


from .forms import CreateUserForm
from .models import Movie, Ticket, Order, Concession_stand, Transaction_receipt, Show_time, Customer
from .forms import TicketForm, CustomerInfoForm


# Create your views here.
def home(request):
	movie_list = Movie.objects.all()
	return render(request, 'index.html', {'movie_list':movie_list})

def test(request):
    return render(request, 'test.html', {})

def movie_showcase(request):
	movie_list = Movie.objects.all()
	all_show_times = Show_time.objects.all()
	return render(request, 'movie_showcase.html', {'movie_list':movie_list, 'all_show_times':all_show_times})

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'GET':
			form = CreateUserForm()		
			context = {'form':form}
			return render(request, 'register.html', context)
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				user_email = form.cleaned_data.get('email')
				messages.success(request, 'Account was created for ' + user)

				#create instance of customer
				customer_instance = Customer.objects.create(
					customer_account_number = user,
					customer_email = user_email
				)

				return redirect('customer_information')
			



def loginPage(request):
	if request.user.is_authenticated:
		return redirect('movie_showcase')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('movie_showcase')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def ticket_page(request):
	if request.method == "GET":
		form = TicketForm
		return render(request, 'ticket_page.html', {'form':form})
	if request.method == "POST":
		form = TicketForm(request.POST)
		if form.is_valid():
			form.save()
		#return render(request, 'concession_order.html', {})
		return redirect('concession_order')


@login_required(login_url='login')
def concession_order(request):
	#input_problem = request.POST.get("existing_boot_problem")
	#<select class="form-control" id="exampleFormControlSelect1" name="existing_boot_problem">
	if request.method == "GET":
		print("*************")
		return render(request, 'concession_order.html', {})
	if request.method == "POST":
		popcorn_amount = request.POST.get("popcorn_amount")
		soda_amount = request.POST.get("soda_amount")
		print("POPCORN:"+str(popcorn_amount))
		print("SODA:"+str(soda_amount))

		#add order to context {} and latest ticket
		lastest_ticket = Ticket.objects.last()
		Concession_stand_latest = Concession_stand.objects.last() 

		#make instance of order entry to databse
		#feet_instance = Feet_measurment.objects.create()
		#feet_instance.save()
		order_instance = Order.objects.create(
			customer_account_number = lastest_ticket.customer_account_number,
			order_number = Order.objects.last().order_number + 1,
			items_ordered = "popcorn: "+str(popcorn_amount)+" soda: "+str(soda_amount),
			pick_up_time = 15,
			concession_stand_number = Concession_stand_latest
		)
		order_instance.save()

		return redirect('order_summary')


		#return render(request, "order_summary.html", {'soda_amount':soda_amount, 'popcorn_amount':popcorn_amount, 'lastest_ticket':lastest_ticket})

@login_required(login_url='login')
def order_summary(request):
	popcorn_amount = 0
	soda_amount = 1
	#latest ticket
	lastest_ticket = Ticket.objects.last()
	if request.method == "GET":
		order_instance_latest = Order.objects.last()
		amount_popcorn = int(order_instance_latest.items_ordered.split()[1])
		amount_soda = int(order_instance_latest.items_ordered.split()[3])
		ticket_price = int(lastest_ticket.price)
		payment_due_popcorn = amount_popcorn*5
		payment_due_soda = amount_soda*3
		total = payment_due_popcorn + payment_due_soda  + ticket_price
		print(amount_popcorn)
		#create instance of transaction receipt
		transaction_receipt_instance = Transaction_receipt.objects.create(
			customer_account_number = lastest_ticket.customer_account_number,
			transaction_number = randint(1, 1000),
			receipt = Transaction_receipt.objects.last().receipt + 1,
			amount = total,
			items = order_instance_latest.items_ordered,
			date = "today"
		)
		return render(request, 'order_summary.html', {'payment_due_soda':payment_due_soda, 'payment_due_popcorn':payment_due_popcorn, 'total':total, 'soda_amount':amount_soda, 'popcorn_amount':amount_popcorn, 'lastest_ticket':lastest_ticket})

@login_required(login_url='login')
def thank_you_page(request):
	if request.method == "GET":
		return render(request, "thank_you_page.html", {})
	if request.method == "POST":
		transaction_receipt_instance = Transaction_receipt.objects.last()
		amount_spent = str(transaction_receipt_instance.amount)
		transaction_number_last = str(transaction_receipt_instance.transaction_number)
		message = 'Hi , thank you for buying a ticket at your local cinema. You purchase of $'+amount_spent+' in transaction #'+transaction_number_last+' will go to supporting a local business!'
		#get email of user 
		found_user_name = request.user
		customer_form_found = Customer.objects.get(pk=found_user_name)
		customer_email_found = str (customer_form_found.customer_email)
		send_mail(
            'Movie Project Group 8 CPSC 471', #subject
            message, # message
            'cpsc471project@gmail.com', #from email
            [customer_email_found], #to email
        )
		
		movie_list = Movie.objects.all()
		all_show_times = Show_time.objects.all()
		return render(request, 'movie_showcase.html', {'movie_list':movie_list, 'all_show_times':all_show_times})


@login_required(login_url='login')
def customer_information_inital(request):
	found_user_name = request.user
	customer_form_found = Customer.objects.get(pk=found_user_name)
	form = CustomerInfoForm(request.POST or None, instance=customer_form_found)
	if request.method == "GET":
		return render(request, "customer_information.html", {'form':form})
	if request.method == "POST":
		if form.is_valid():
			form.save()
		#return render(request, 'concession_order.html', {})
		return redirect('movie_showcase')