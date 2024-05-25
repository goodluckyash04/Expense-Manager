from django.urls import path

from .views import *
from .view_transaction import create_transaction, transaction_detail, update_transaction, delete_transaction, \
    fetch_deleted_transaction, undo_transaction, update_transaction_status
from .view_financial_instrument import create_finance, finance_details, fetch_financial_transaction, \
    update_instrument_status, update_finance_detail, remove_instrument
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
    path("create-finance/",create_finance,name="create-finance"),
    path("finance-details/",finance_details,name="finance-details"),
    path("update-finance-detail/<int:id>",update_finance_detail,name="update-finance-detail"),
    path("fetch-financial-transaction/<int:id>",fetch_financial_transaction,name="fetch-financial-transaction"),
    path("update-instrument-status/<int:id>",update_instrument_status,name="update-instrument-status"),
    path("remove-instrument/<int:id>",remove_instrument,name="remove-instrument"),


]


