from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from datetime import datetime
from itertools import chain
from django.db.models import Q
import random,string
from django.core.mail import send_mail
from django.conf import settings

# ...........................................Home Page..................................................


def home(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        return render(request,"home.html",{"user":user})
    else:
        return redirect('login')


# ...........................................User Management..................................................

def login(request):
    if 'username' in request.session:
        return redirect("home")
    else:
        if request.method == "GET":
            msg = ""
            if 'forgot_password_msg' in request.session:
                msg = request.session.get('forgot_password_msg', None)
                del request.session['forgot_password_msg']
            return render(request,"login.html",{"msg":msg})
        else:
            if User.objects.filter(username=request.POST['username'].lower()).exists():
                user = User.objects.get(username=request.POST['username'].lower())
                if check_password(request.POST['password'],user.password):
                    request.session["username"] = user.username
                    return redirect("home")
                else:
                    return render(request,"login.html",{"msg":"Invalid Credential"})

            else:
                return render(request,"login.html",{"msg":"user Does not exist"})


def signup(request):
    if request.method == "GET":
        return render(request,"signup.html")
    else:
        if User.objects.filter(username=request.POST['username'].lower()).exists():
            return render(request,"signup.html",{"msg":"User Exist"})
        else:
            if request.POST['password'] == request.POST["rpassword"]:
                User.objects.create(
                    name = request.POST['name'],
                    username = request.POST['username'].lower(),
                    email = request.POST['email'],
                    password = make_password(request.POST['password'])
                )
                return render(request,"login.html",{"msg":"User Created.Login to Continue"})
            else:
                return render(request,"signup.html",{"msg":"Both Password Should be Same"})


def logout(request):
    del request.session['username']
    return redirect('login')


def forgotPassword(request):
    if request.method == "GET":
        return render(request,"forgotPassword.html")
    else:
        try:
            user = User.objects.get(username = request.POST["username"].lower())
            newPassword = get_random_string(8)
            sub = "Change in Account"
            message = f"Use This Password to Login to ypur account:\n{newPassword}\n\n Do Not Share With anyone"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(sub, message, from_email, recipient_list)
            user.password =  make_password(newPassword)
            user.save()
            maskedEmail =hide_email(user.email)
            msg = f"Password sent to {maskedEmail}"
            request.session['forgot_password_msg'] = msg
            return redirect('login')
        except:
            return render(request,"forgotPassword.html",{"msg":"User Does not exist"})


def changePassword(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        if request.method == "GET":
            return render(request,"changePassword.html",{"user":user})
        else:
            if check_password(request.POST['old_password'],user.password):
                if request.POST['password'] == request.POST['c_password']:
                    user.password =  make_password(request.POST['password'])
                    user.save()
                    return redirect('home')
                else:
                    return render(request,"changePassword.html",{"user":user,"msg":"confirm Password Should Match"})
            else:
                return render(request,"changePassword.html",{"user":user,"msg":"Old Password Incorrect"})



# .............................................EXTRAS................................................

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

    
def dateConvert(date_value):
    date_string = date_value
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    formatted_date = date_object.strftime("%d%b%y").upper()
    return formatted_date


def hide_email(value):
    parts = value.split('@')
    username = parts[0]
    domain = parts[1]
    username = username[:2] + '*' * 8 + username[-1:]  # Hide all characters except the first two and last
    return f"{username}@{domain}"



# hashed_pwd = make_password("plain_text")
# check_password("plain_text",hashed_pwd)  # returns True







def indexLogin(request):
    return render(request,'newlogin.html')