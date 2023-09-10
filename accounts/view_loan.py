from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import JsonResponse


# ...............................................Loan Management...................................

def addloan(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("title") 

        if request.method == "GET":
            return render(request,'addLoan.html',{'user':user,"loanData":loanData})
        else:
            Loan.objects.create(
                title = request.POST['title'],
                amount = request.POST['amount'],
                started_on =  request.POST['started_on'],
                created_by =user
            )
        return redirect('home')
    else:
        return redirect("login")


def loanHome(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        loanData = Loan.objects.filter(created_by=user).order_by("-status","title") 
        return render(request,'loanHome.html',{"loanData":loanData})
    else:
        return redirect('login')    
    

def updateLoanStatus(request,id):
    if 'username' in request.session:
        loanData = Loan.objects.get(id=id)

        if loanData.status == "Open":
            loanData.status = "Closed"
        else:
            loanData.status = "Open"

        loanData.save()
        return redirect('loanHome')
    else:
        return redirect('login')    
    

def loanReport(request,id):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        
        if request.method == "GET":
            loanData = Loan.objects.get(id= id)
            emiData = EMI.objects.filter(loan_id = id ).order_by('-paid_on')
            
            total = loanData.amount
            for i in emiData:
                total += i.amount
        
            return render(request,'loanReport.html',{'user':user,"loanData":loanData,'emiData':emiData,'total':total})
    else:
        return redirect('login')    



def addEMI(request,id):
    if 'username' in request.session:
        loanData = Loan.objects.get(id= id)
        EMI.objects.create(
            loan = loanData,
            paid_on = request.POST['paid_on'],
            amount = -int(request.POST['amount']),
            note = request.POST['note'],
        )
        return redirect(f'/loanReport/{id}')
    else:
        return redirect('login')
    
def editEmi(request, id):
    if 'username' in request.session:
        emi_data = get_object_or_404(EMI, id=id)  # Use get_object_or_404 to handle 404 if the object is not found        
        loan = Loan.objects.get(id=emi_data.loan_id).title
        if request.method=="GET":
            # Serialize the model data into a dictionary
            emi_dict = {
                'id': emi_data.id,
                'loan':loan,
                'paid_on': emi_data.paid_on,  # Replace with your actual field names
                'amount': emi_data.amount,
                'note': emi_data.note,
                # Add more fields as needed
            }

            return JsonResponse(emi_dict)
        else:
            Loan.objects.filter(id=emi_data.loan_id).update(title=request.POST["loan"])

            emi_data.paid_on= request.POST['paid_on']  # Replace with your actual field names
            emi_data.amount = request.POST['amount']
            emi_data.note= request.POST['note']
            emi_data.save()
            print("ok")
            return redirect(f'/loanReport/{emi_data.loan_id}')

    else:
        return redirect('login')

def deleteLoan(request,id):
    if 'username' in request.session:
        emis = EMI.objects.filter(loan_id = id)
        if not emis:
            current_Loan = Loan.objects.get(id = id)
            current_Loan.delete()
        return redirect('loanHome')
    else:
        return redirect('login')

def deleteEmi(request,id):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])

        current_EMI = EMI.objects.get(id = id)
        loandata = Loan.objects.get(id=current_EMI.loan_id)
        DeletedEMI.objects.create(
            loan = loandata.title,
            paid_on =current_EMI.paid_on,
            amount = current_EMI.amount,
            note =current_EMI.note,
            created_by = user
        )
        current_EMI.delete()
        return redirect('loanReport',id=loandata.id)
    else:
        return redirect('login')
    

def deletedEntries(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])

        deleteEmi = DeletedEMI.objects.filter(created_by =user.id)
        return render(request,'deletedEntries.html',{"data":deleteEmi,"user":user})
    else:
        return redirect('login')
    
def undoEntries(request,id):
    if 'username' in request.session:
        user = User.objects.get(username = request.session["username"])
        deleteEmi = DeletedEMI.objects.get(id = id)
        loanData = Loan.objects.get(title = deleteEmi.loan ,created_by = user.id)
        if loanData:
            EMI.objects.create(
                loan = loanData,
                paid_on = deleteEmi.paid_on,
                amount = deleteEmi.amount,
                note = deleteEmi.note
            )
        deleteEmi.delete()
        return redirect('deletedEntries')
    else:
        return redirect('login')