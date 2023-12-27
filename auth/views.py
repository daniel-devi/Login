from django.shortcuts import render,redirect
from .forms import CreateUserForm 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from ecom import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    return render(request, "auth\home.html")



@csrf_exempt
def signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

    if form.is_valid():
        user =  form.cleaned_data.get("username")
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exist")
        
        """if User.objects.filter(email=email ):
            messages.error(request, "email Already Exist")
        """
    #   WELCOME EMAIL

        subject = "Welcome to Daniel's Project."
        message = "Hello" + str(username) ," Welcome to Daniel's Project \n Thank You For Creating and account \n  We have also sent you a Confirmation Email, open it to activate your Account "
        from_mail = settings.EMAIL_HOST_USER
        to_mail = [email]
        send_mail( subject, message, from_mail, to_mail, fail_silently=True )
        messages.success(request, "Account Created For " + str(username), "Was Succseful")
        form.save()
        return redirect(signin)
        
        
    context = {"form":form}
    return render(request, "auth\signup.html", context)



def signin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password Incorrect")
            return render(request, "auth\signin.html")

    context = {}
    return render(request, "auth\signin.html")



def signout(request):
    logout(request)
    return render(request,"auth\logout.html")