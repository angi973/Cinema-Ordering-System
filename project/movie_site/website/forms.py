from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Customer
from django import forms
from tkinter import Widget

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"

        price_option = (
            ('10','Adult Ticket $10.00'),
            ('5','Kid Ticket $5.00')
        )
        labels ={
			'show_time_movie_id':'what movie showtime do you want to see?',
    		'seat_number':'Seat numbers available are from 1 to 10. Input your selection:',
    		'row_letter':'Row letters available are from A to E. Input your selection',
    		'classification':'Are you a loyalty member?',
    		'price':'Select your ticket price.',
    		'date':'Input the movie date',
    		'customer_account_number':'What is your user name number?'
        }
        widgets = {
			#'show_time_movie_id':forms.MultipleChoiceField(),
			# 'seat_number':forms.TextInput(),
			# 'row_letter':forms.TextInput(),
			# 'classification':forms.TextInput(),
			# 'price':forms.Select(choices=price_option),
			# 'date':forms.TextInput(),
			#'customer_account_number':forms.MultiValueField()
        }

class CustomerInfoForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"

		labels ={
			'customer_account_number':'Enter your user name:',
    		'customer_email': 'What is your Email?',
    		'first_name':'What is your first name?',
    		'last_name':'What is your last name?',
    		'middle_name':'What is your middle name?',
    		'age' : 'What is your age?'
        }

