from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import F
from .models import Task
from .decorators import auth_user


def get_task_data_by_user(user):
    return Task.objects.filter(created_by=user).order_by(F('status').desc(), 'complete_by')

def get_task_by_id(id):
    return get_object_or_404(Task, id=id)

# ............................................Task Management...........................................

@auth_user
def addTask(request, user):
    task_data = request.POST
    
    Task.objects.create(
        priority=task_data["priority"],
        name=task_data["name"],
        complete_by_date=task_data["complete_by_date"],
        description=task_data["description"],
        status="Pending",
        created_by=user
    )
    
    return redirect('utilities')

@auth_user
def currentMonthTaskReport(request, user):
    current_month = timezone.now().month
    taskData = Task.objects.filter(
        created_by=user,
        complete_by_date__month=current_month,
        status="Pending",
        is_deleted=False
    ).order_by('complete_by_date')

    return render(request, "task/tasks.html", {"user": user, "taskData": taskData})

@auth_user
def taskReports(request, user):
    taskData = Task.objects.filter(created_by=user).order_by(F('status').desc(), 'complete_by_date')
    return render(request, 'task/taskReport.html', {'user': user, 'taskData': taskData})

@auth_user
def editTask(request, id):
    task_data = get_object_or_404(Task, id=id)
    if request.method == "GET":
        task_dict = {
            'id': task_data.id,
            'priority': task_data.priority,
            'name': task_data.name,
            'complete_by_date': task_data.complete_by_date,
            'description': task_data.description
        }
        return JsonResponse(task_dict)
    else:
        task_data.__dict__.update(**request.POST.dict())
        task_data.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@auth_user
def taskAction(request, id, action):
    current_task = get_task_by_id(id)

    if action == 'complete':
        current_task.completed_on = timezone.now()
        current_task.status = "Completed"
    elif action == 'incomplete':
        current_task.completed_on = None
        current_task.status = "Pending"
        current_task.is_deleted = False
        current_task.deleted_at = None
    elif action == 'delete':
        current_task.is_deleted = True
        current_task.deleted_at = timezone.now()

    current_task.save()

    if action == "permdeletetask":
        current_task.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
