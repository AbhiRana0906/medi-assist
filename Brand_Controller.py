from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def brand_interface(request):
    return render(request,"BrandInterface.html")
@xframe_options_exempt
def submit_brand(request):

    try:
        db,cmd=Pool.ConnectionPooling()

        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandname=request.POST['brandname']
        contactperson=request.POST['contactperson']
        mobile=request.POST['mobile']
        status = request.POST['status']
        brandicon=request.FILES['brandicon']

        query="insert into brands(categoryid,subcategoryid,brandname,contactperson,mobileno,logo,status) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(categoryid,subcategoryid,brandname,contactperson,mobile,brandicon.name,status)
        print(query)
        F=open("E:/medassist_ecom/assets/"+brandicon.name,'wb')
        for chunk in brandicon.chunks():
            F.write(chunk)
        F.close()
        cmd.execute(query)
        db.commit()
        db.close()
        return render(request,"BrandInterface.html",{'message':'Brand added successfully'})
    except Exception as e:
        return render(request,"BrandInterface.html",{'message':'Something went wrong'})


@xframe_options_exempt
def display_all_brands(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        query = "select b.*,(select c.categoryname from categories c where c.categoryid=b.categoryid) as cname,(select s.subcategoryname from subcategories s where b.subcategoryid=s.subcategoryid) as scname from brands b"
        cmd.execute(query)
        brands = cmd.fetchall()
        db.close()

        return render(request, "DisplayBrands.html", {'brand': brands})

    except Exception as e:

        return render(request, "DisplayBrands.html", {'brand': None})


@xframe_options_exempt
def edit_brand(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        categoryid=request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        brandname = request.GET['brandname']
        brandid=request.GET['brandid']
        contactperson=request.GET['contactperson']
        mobileno=request.GET['mobileno']

        query = "update brands set brandname='{0}',categoryid={1},subcategoryid={2},contactperson='{3}',mobileno={4} where brandid={5}".format(brandname,categoryid,subcategoryid,contactperson,mobileno,brandid)
        print(query)
        cmd.execute(query)
        db.commit()
        db.close()
        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        return JsonResponse({'result': False}, safe=False)
@xframe_options_exempt
def delete_brand(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        brandid = request.GET['brandid']

        query = "delete from brands where brandid={0}".format(brandid)
        cmd.execute(query)
        db.commit()
        db.close()
        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def edit_brandicon(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        brandid = request.POST['brandid']
        logo = request.FILES['logo']

        query = "update brands set logo='{0}' where brandid={1}".format(logo.name, brandid)

        F = open("E:/medassist_ecom/assets/" + logo.name, 'wb')
        for chunk in logo.chunks():
            F.write(chunk)
        F.close()
        print(query)
        cmd.execute(query)
        db.commit()
        db.close()
        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        return JsonResponse({'result': False}, safe=False)