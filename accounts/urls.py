from django.urls import path
from .views import *
from .view_expense import *
from .view_loan import *
from .view_task import *


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
    path("currentMonthreports/",currentMonthreports,name="currentMonthreports"),
    path("search/",search_report,name="search_report"),
    path("filter/",filter_report,name="filter_report"),
    path("delete_records/",delete_records,name="delete_records"),

# ..........................................Task Management..................................................

    path("addTask/",addTask,name="addTask"),
    path("currentMonthTaskReport/",currentMonthTaskReport,name="currentMonthTaskReport"),
    path("updatetask/<int:id>",updatetask,name="updatetask"),
    path("incomplete/<int:id>",incomplete,name="incomplete"),
    path("deletetask/<int:id>",deletetask,name="deletetask"),
    path("permdeletetask/<int:id>",permdeletetask,name="permdeletetask"),
    path("taskReports/",taskReports,name="taskReports"),

# ..........................................Loan Management..................................................

    path("loanHome/",loanHome,name="loanHome"),
    path("addloan/",addloan,name="addloan"),
    path("updateLoanStatus/<int:id>",updateLoanStatus,name="updateLoanStatus"),
    path("deleteLoan/<int:id>",deleteLoan,name="deleteLoan"),
    path("loanReport/<int:id>",loanReport,name="loanReport"),
    path("addEMI/<int:id>",addEMI,name="addEMI"),
    path("deleteEmi/<int:id>",deleteEmi,name="deleteEmi"),

]
