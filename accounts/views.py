from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from datetime import datetime
from itertools import chain
from django.db.models import Q
import random,string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# ...........................................Home Page..................................................


def home(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        print("wewef",datetime.today().strftime("%b'%y"))
        items = [
            {
                "title": "EXPENSE",
                "description": "Maintain Your Day to Day Expense",
                "modal_target": "#expensemodal",
                "modal_button_icon": 'fa-circle-plus',
                "report_url": "/currentMonthreports/",
                "report_button_icon":  datetime.today().strftime("%b'%y").upper(),
                "delete_url": "/reports/",
                "delete_button_icon": 'fa-solid fa-square-poll-horizontal',
                "class_suffix": " mb-3 mb-sm-0"
                
            },
            {
                "title": "TASK",
                "description": "Don't Stress Your Brain Add Your ToDos Here",
                "modal_target": "#taskmodal",
                "modal_button_icon": 'fa-circle-plus',
                "report_url": "/currentMonthTaskReport/",
                "report_button_icon": datetime.today().strftime("%b'%y").upper(),
                "delete_url": "/taskReports/",
                "delete_button_icon": 'fa-square-poll-horizontal',
                "class_suffix": " mb-3"
            },
            {
                "title": "LOAN",
                "description": "Create Your Virtual Loan To keep track of EMIS",
                "modal_target": "#loanmodal",
                "modal_button_icon": 'fa-circle-plus',
                "report_url": "/loanHome/",
                "report_button_icon": 'fa-square-poll-horizontal',
                "delete_url": "/deletedEntries/",
                "delete_button_icon": 'fa-trash-can',
                "class_suffix": ""
            },
        ]

        return render(request,"home.html",{"user":user,'items': items})
    else:
        return redirect('login')


# ...........................................User Management..................................................

def login(request):
    print(request)
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
    else:
        return redirect('login')



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

def get_current_month_name():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_date = datetime.now()
    current_month = months[current_date.month - 1]  # Python months are 1-based
    current_year = str(current_date.year)[-2:]  # Get the last two digits of the year
    return f"{current_month}'{current_year}"

# hashed_pwd = make_password("plain_text")
# check_password("plain_text",hashed_pwd)  # returns True

