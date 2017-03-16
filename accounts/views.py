from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth, messages

# Create your views here.
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('index'))

def profile(request):
    return render(request, 'profile.html')