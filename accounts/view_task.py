from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse



# ............................................Task Management...........................................

def addTask(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        Task.objects.create(
            priority = request.POST["priority"],
            task_title = request.POST["task_title"],
            complete_by = request.POST["complete_by"],
            task_detail = request.POST["task_detail"],
            status = "Pending",
            completed_on = request.POST["complete_by"],
            created_by = user
        )
        return redirect('home')
    else:
        return redirect("login")
    

def currentMonthTaskReport(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        taskData =Task.objects.filter(Q(created_by =user) & Q(complete_by__month= datetime.today().month) & Q(status = "Pending") ).order_by('complete_by')
        request.session["key"] = "current_month"
        return render(request,"tasks.html",{"user":user,"taskData":taskData})
    else:
        return redirect("login")


def updatetask(request,id):
    current_task = Task.objects.get(id = id)
    current_task.completed_on = datetime.today()
    current_task.status = "Completed"
    current_task.save()
    if request.session['key'] == "current_month":
        return redirect('currentMonthTaskReport')
    else:
        return redirect('taskReports')

def editTask(request,id):
    task_data = get_object_or_404(Task, id=id)  # Use get_object_or_404 to handle 404 if the object is not found        
    if request.method=="GET":
        # Serialize the model data into a dictionary
        task_dict = {
            
            'id': task_data.id,
            'priority':task_data.priority,
            'task_title':task_data.task_title,
            'complete_by':task_data.complete_by, 
            'task_detail':task_data.task_detail  
            
        }

        return JsonResponse(task_dict)
    else:
        task_data.priority = request.POST["priority"]
        task_data.task_title = request.POST["task_title"]
        task_data.complete_by = request.POST["complete_by"]
        task_data.task_detail = request.POST["task_detail"]       
       
        task_data.save()
        return redirect('taskReports')

    #     return redirect('currentMonthTaskReport')
    # else:
    #     return redirect('taskReports')

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
    return redirect('currentMonthTaskReport')


def permdeletetask(request,id):
    current_task = Task.objects.get(id = id)
    print(current_task)
    current_task.delete()
    return redirect('taskReports')


def taskReports(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        taskData = Task.objects.filter(created_by = user).order_by("-status",'complete_by')
        request.session["key"] = "taskReport"
        return render(request,'taskReport.html',{'user':user,'taskData':taskData})
    else:
        return redirect('login')
