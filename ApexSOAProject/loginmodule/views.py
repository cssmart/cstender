from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages


# Create your views here.
def login(request, pk):
	request.session['pk'] = pk
	if request.user.is_authenticated:
		messages.add_message(request, messages.INFO, 'You are already Logged in.')
		data = f'/detailpo/{pk}/'
		return HttpResponseRedirect(data)
	else:
		c = {}
		c.update(csrf(request))
		return render(request, 'loginmodule/login.html', c)


def auth_view(request):
	pk = request.session.get('pk')
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		messages.add_message(request, messages.INFO, 'Your are now Logged in.')
		return HttpResponseRedirect(f'/detailpo/{pk}/')
	else:
		messages.add_message(request, messages.WARNING, 'Invalid Login Credentials.')
		return HttpResponseRedirect('/login')


def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	messages.add_message(request, messages.INFO, 'You are Successfully Logged Out')
	messages.add_message(request, messages.INFO, 'Thanks for visiting.')
	return HttpResponseRedirect('/login')
