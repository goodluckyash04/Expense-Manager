from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseServerError
from django.utils.crypto import get_random_string
from .models import User
from .decorators import auth_user



# ...........................................Home Page..................................................

@auth_user
def home(request,user):
    try:
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
    except Exception as e:
        messages.error(request, "An unexpected error occurred.")
        # Log the error for debugging purposes
        print(str(e))
        return HttpResponseServerError()


# ...........................................User Management..................................................

def login(request):

    if 'username' in request.session:
        return redirect("home")
    
    if request.method == "GET":
        msg = request.session.pop('forgot_password_msg', '')
        return render(request, "login.html", {"msg": msg})
    
    if not User.objects.filter(username=request.POST['username'].lower()).exists():
        return render(request,"login.html",{"msg":"user Does not exist"})
    

    user = User.objects.get(username=request.POST['username'].lower())
    if not check_password(request.POST['password'],user.password):
        return render(request,"login.html",{"msg":"Invalid Credential"})

    request.session["username"] = user.username
    return redirect("home")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    if request.method == "POST":
        username = request.POST.get('username', '').lower()
        password = request.POST.get('password', '')
        rpassword = request.POST.get('rpassword', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if not username or not password or not rpassword:
            return render(request, "signup.html", {"msg": "All fields are required."})

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"msg": "Username already exists."})

        if password != rpassword:
            return render(request, "signup.html", {"msg": "Passwords do not match."})

        try:
            User.objects.create(
                username=username,
                password=make_password(password),
                name=name,
                email=email,
            )
            return render(request, "login.html", {"msg": "User Created. Login to Continue"})
        except Exception as e:
            messages.error(request, "An unexpected error occurred.")
            # Log the error for debugging purposes
            print(str(e))
            return HttpResponseServerError()

    return render(request, "signup.html")



def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass  # 'username' key may not be present in the session

    return redirect('login')


def forgotPassword(request):
    if request.method == "GET":
        return render(request, "forgotPassword.html")

    if request.method == "POST":
        try:
            username = request.POST.get("username", "").lower()
            user = User.objects.get(username=username)

            new_password = get_random_string(8)
            sub = "Change in Account"
            message = f"Use This Password to Login to your account:\n{new_password}\n\n Do Not Share With anyone"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(sub, message, from_email, recipient_list)
            
            user.password = make_password(new_password)
            user.save()
            
            masked_email = hide_email(user.email)
            msg = f"Password sent to {masked_email}"
            request.session['forgot_password_msg'] = msg
            
            return redirect('login')
        except User.DoesNotExist:
            return render(request, "forgotPassword.html", {"msg": "User does not exist"})
        except Exception as e:
            # Handle other exceptions if necessary
            return render(request, "forgotPassword.html", {"msg": "An error occurred. Please try again."})

    return render(request, "forgotPassword.html")


@auth_user
def changePassword(request, user):
    if request.method == "GET":
        return render(request, "changePassword.html", {"user": user})

    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('password', '')
    confirm_password = request.POST.get('c_password', '')

    if not check_password(old_password, user.password):
        return render(request, "changePassword.html", {"user": user, "msg": "Old Password Incorrect"})

    if new_password != confirm_password:
        return render(request, "changePassword.html", {"user": user, "msg": "Confirm Password Should Match"})

    user.password = make_password(new_password)
    user.save()

    return redirect('home')



# .............................................EXTRAS................................................

    
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

