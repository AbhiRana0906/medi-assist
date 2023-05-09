from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def Admin_Login(request):
    return render(request,"Login_Page.html")
def Admin_Logout(request):
    del request.session['ADMIN']
    return render(request,"Login_Page.html")

def Check_Admin_Login(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        emailid = request.POST['emailid']
        password = request.POST['password']
        query = "select * from adminlogin where emailid='{0}' and password='{1}'".format(emailid,password)
        print(query)
        cmd.execute(query)
        row=cmd.fetchone()
        if(row):
            request.session['ADMIN']=row
            return render(request, "DashBoard.html",{'AdminData':row})
        else:
            return render(request, "Login_Page.html",{'message':'Invalid Emailid/Password'})

        db.close()

    except Exception as e:
        return render(request, "AdminLogin", {'message': 'Something went wrong'})

