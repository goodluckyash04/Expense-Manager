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
    path("undoDelEntries/<int:id>",undoDelEntries,name="undoDelEntries"),    
    path("getDeletedEntries/",getDeletedEntries,name="getDeletedEntries"),
    path("undoMultipleDelEntries/",undoMultipleDelEntries,name="undoMultipleDelEntries"),

# ..........................................Task Management..................................................

    path("addTask/",addTask,name="addTask"),
    path("currentMonthTaskReport/",currentMonthTaskReport,name="currentMonthTaskReport"),
    path("taskReports/",taskReports,name="taskReports"),
    path("editTask/<int:id>",editTask,name="editTask"),
    path("task/action/<int:id>/<str:action>/",taskAction,name="taskAction"),

    

# ..........................................Loan Management..................................................

    path("addloan/",addloan,name="addloan"),
    path("loanHome/",loanHome,name="loanHome"),
    path("loanReport/<int:id>",loanReport,name="loanReport"),
    path("searchLoan/",searchLoan,name="searchLoan"),
    path("updateLoanStatus/<int:id>",updateLoanStatus,name="updateLoanStatus"),
    path("addEMI/<int:id>",addEMI,name="addEMI"),
    path("editEmi/<int:id>",editEmi,name="editEmi"),
    path("deleteLoan/<int:id>",deleteLoan,name="deleteLoan"),
    path("deleteEmi/<int:id>",deleteEmi,name="deleteEmi"),
    path("undoEntries/<int:id>",undoEntries,name="undoEntries"),
    path("deletedEntries/",deletedEntries,name="deletedEntries"),

]
