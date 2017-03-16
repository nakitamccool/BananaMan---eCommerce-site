from django.contrib import messages, auth
from accounts.forms import UserLoginForm
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

