from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout




def i(request):
     return render(request, 'index.html')


def signup(request):

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    my_context = {}

    args = {}
    args['validation'] = 'please enter info'
    args['status'] = True

    if User.objects.filter(username=username).exists():
        args['validation'] = 'user already exist'
        args['status'] = False
    else:
        user = User()
        # user.email= email
        if username and password:
            user.username= username
            user.set_password(password)
            user.save()

            args = {}
            args['validation'] = 'signup done'
            args['status'] = True

            print 'signup request recieved'
            return HttpResponseRedirect('/')
    return render_to_response('signup.html',args)


def home(request):
    print 'request.user'
    return render(request, 'home.html')



def submit_login(request):
    print 'login request recieved'
    username = request.POST.get('username')
    password = request.POST.get('password')
    my_context = {}
    args = {}
    args['validation'] = 'Invalid Login detail'
    args['status'] = True

    user = authenticate(username=username, password=password)
    login(request, user)

    if user is not None:
        # the password verified for the user
        if user.is_active:
            print "User is valid, active and authenticated"
            return redirect('/home/', backend=my_context)


            # return render_to_response('home.html', my_context, context_instance=RequestContext(request))
        else:
            print "The password is valid, but the account has been disabled!"
            # return render_to_response('index.html', my_context, context_instance=RequestContext(request))
    else:
        # the authentication system was unable to verify the username and password
        print "The username and password were incorrect."
    return render_to_response('index.html',args)

    # return render_to_response('index.html', my_context, context_instance=RequestContext(request))


def logoutView(request):
   if request.user.is_authenticated():
       logout(request)
       return HttpResponseRedirect('/')
   else:
       return HttpResponse(json.dumps({"redirectUrl":"/","validation":"Invalid Login","status":False}), content_type="application/json")
