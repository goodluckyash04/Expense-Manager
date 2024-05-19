from django.urls import path

from .view_transaction import create_transaction, transaction_detail, update_transaction, delete_transaction, \
    fetch_deleted_transaction, undo_transaction, update_transaction_status
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

# ..........................................Transaction Management...............................................

    path("create-transaction/", create_transaction, name="create-transaction"),
    path("transaction-detail/", transaction_detail, name="transaction-detail"),
    path("deleted-transaction-detail/", fetch_deleted_transaction, name="deleted-transaction-detail"),
    path("update-transaction/<int:id>", update_transaction, name="update-transaction"),
    path("update-transaction-status/<int:id>", update_transaction_status, name="update-transaction-status"),
    path("delete-transaction/", delete_transaction,name="delete-transaction"),
    path("delete-transaction/<int:id>", delete_transaction ,name="delete-transaction"),
    path("undo-transaction/", undo_transaction, name="undo-transaction"),
    path("undo-transaction/<int:id>", undo_transaction, name="undo-transaction"),


# ..........................................Task Management..................................................

    path("addTask/",addTask,name="addTask"),
    path("currentMonthTaskReport/",currentMonthTaskReport,name="currentMonthTaskReport"),
    path("taskReports/",taskReports,name="taskReports"),
    path("editTask/<int:id>",editTask,name="editTask"),
    path("task/action/<int:id>/<str:action>/",taskAction,name="taskAction"),


# ..........................................Loan Management..................................................
#
#     path("addloan/",addloan,name="addloan"),
#     path("loanHome/",loanHome,name="loanHome"),
#     path("loanReport/<int:id>",loanReport,name="loanReport"),
#     path("searchLoan/",searchLoan,name="searchLoan"),
#     path("updateLoanStatus/<int:id>",updateLoanStatus,name="updateLoanStatus"),
#     path("addEMI/<int:id>",addEMI,name="addEMI"),
#     path("editEmi/<int:id>",editEmi,name="editEmi"),
#     path("deleteLoan/<int:id>",deleteLoan,name="deleteLoan"),
#     path("deleteEmi/<int:id>",deleteEmi,name="deleteEmi"),
#     path("undoEntries/<int:id>",undoEntries,name="undoEntries"),
#     path("deletedEntries/",deletedEntries,name="deletedEntries"),

]


