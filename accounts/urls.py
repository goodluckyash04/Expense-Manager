from django.urls import path
from .views import *

urlpatterns = [

# ..........................................Home Page..................................................
    path("home/",home,name="home"),

# ..........................................User Management..................................................
    path("",login,name="login"),
    path("signup/",signup,name="signup"),
    path("logout/",logout,name="logout"),
    path("forgotPassword/",forgotPassword,name="forgotPassword"),
    path("changePassword/",changePassword,name="changePassword"),

# ..........................................Expense Management...............................................

    path("addexpense/",addexpense,name="addexpense"),
    path("editEntry/<int:id>",editEntry,name="editEntry"),    
    path("deleteentry/<int:id>",deleteentry,name="deleteentry"),    
    path("reports/",reports,name="reports"),
    path("search/",search_report,name="search_report"),
    path("filter/",filter_report,name="filter_report"),

# ..........................................Task Management..................................................

    path("addTask/",addTask,name="addTask"),
    path("updatetask/<int:id>",updatetask,name="updatetask"),
    path("incomplete/<int:id>",incomplete,name="incomplete"),
    path("deletetask/<int:id>",deletetask,name="deletetask"),
    path("permdeletetask/<int:id>",permdeletetask,name="permdeletetask"),
    path("taskReports/",taskReports,name="taskReports"),

# ..........................................Loan Management..................................................

    path("loan/",loan,name="loan"),
    path("loanReport/",loanReport,name="loanReport"),
    path("loanEMI/",loanEMI,name="loanEMI"),
    path("deleteEmi/<int:id>",deleteEmi,name="deleteEmi"),
    path("deleteLoan/<int:id>",deleteLoan,name="deleteLoan"),
    path("delete_records/",delete_records,name="delete_records"),


]
