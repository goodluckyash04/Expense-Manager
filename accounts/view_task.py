from django.shortcuts import render,redirect
from .models import *
from datetime import datetime
from django.db.models import Q


# ............................................Task Management...........................................

def addTask(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        taskData =Task.objects.filter(Q(created_by =user) & Q(complete_by__month= datetime.today().month) & Q(status = "Pending") ).order_by('-complete_by')
        # taskData =Task.objects.filter(created_by =user)
        print(taskData)
        if request.method == "GET":
            request.session["key"] = "dashboard"
            return render(request,"tasks.html",{"user":user,"taskData":taskData})
        elif request.method == "POST":
            Task.objects.create(
                priority = request.POST["priority"],
                task_title = request.POST["task_title"],
                complete_by = request.POST["complete_by"],
                task_detail = request.POST["task_detail"],
                status = "Pending",
                completed_on = request.POST["complete_by"],
                created_by = user
            )
            return render(request,"tasks.html",{"msg":"task added","user":user,"taskData":taskData})
    else:
        return redirect("login")


def updatetask(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Completed"
    current_task.save()
    return redirect('addTask')


def incomplete(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Pending"
    current_task.save()
    return redirect('taskReports')


def deletetask(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Deleted"
    current_task.save()
    return redirect('addTask')


def permdeletetask(request,id):
    current_task = Task.objects.get(id = id)
    print(current_task)
    current_task.delete()
    return redirect('taskReports')


def taskReports(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
    taskData = Task.objects.filter(created_by = user)
    return render(request,'taskReport.html',{'user':user,'taskData':taskData})
