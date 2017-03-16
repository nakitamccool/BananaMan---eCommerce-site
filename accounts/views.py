from django.contrib import messages, auth
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login?next=profile')
def profile(request):
    return render(request, 'profile.html')


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username_or_email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")

                if request.GET and 'next' in request.GET:
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your username or password was not recognised")

    else:
        # this handles the initial get request
        # return a blank form for user to login
        form = UserLoginForm()

    # prepare args to pass to render function
    #   form:   this is the form which will be rendered to html (UserLoginForm)
    #   next:   if the url of the request included a next query string '?next=' pass it to the form
    #           so that it can be included in the url when the form is resubmitted
    #           see handling of post method: next = request.GET['next']
    args = {'form': form, 'next': request.GET['next'] if request.GET and 'next' in request.GET else ''}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            #do an early save so that if user input is invalid/ unauthorised new form can be loaded with valide details previously entered
            form.save()

            #user has a valid username and password, if not a user then we will drop out of this code and reload form on line X
    #else:
        #form= UserRegistrationForm()
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))

            #if valid user, then return success msg and redirect to profile. Else provide error msg.
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered and are now logged into your account")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "Unable to log you in at this time.")

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))


    return render(request, 'register.html', args)






