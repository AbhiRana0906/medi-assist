from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def product_interface(request):
    return render(request,"ProductInterface.html")

@xframe_options_exempt
def submit_Product(request):

    try:
        db,cmd=Pool.ConnectionPooling()

        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandid=request.POST['brandid']
        productname=request.POST['productname']
        price=request.POST['price']
        offerprice=request.POST['offerprice']
        packingtype=request.POST['packingtype']
        qty=request.POST['qty']
        rating=request.POST['rating']
        salestatus=request.POST['salestatus']
        status=request.POST['status']
        productimage=request.FILES['productimage']

        query="insert into products(categoryid,subcategoryid,brandid,productname,price,offerprice,packingtype,status,salestatus,productimage,quantity,rating) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(categoryid,subcategoryid,brandid,productname,price,offerprice,packingtype,status,salestatus,productimage,qty,rating)
        
        F=open("E:/medassist_ecom/assets/"+productimage.name,'wb')
        for chunk in productimage.chunks():
            F.write(chunk)
        F.close()
        cmd.execute(query)
        db.commit()
        db.close()
        return render(request,"ProductInterface.html",{'message':'Product added successfully'})
    except Exception as e:
        return render(request,"ProductInterface.html",{'message':'Something went wrong'})

@xframe_options_exempt
def fetch_all_brand_json(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        subcategoryid=request.GET['subcategoryid']
        categoryid=request.GET['categoryid']
        query = "select * from brands where categoryid={0} and subcategoryid={1}".format(categoryid,subcategoryid)
        cmd.execute(query)
        brands = cmd.fetchall()
        db.close()

        return JsonResponse({'data': brands}, safe=False)

    except Exception as e:
        print(Exception)
        return JsonResponse({'data': None}, safe=False)


@xframe_options_exempt
def display_all_products(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        query = "select p.*,(select c.categoryname from categories c where c.categoryid=p.categoryid) as cname,(select s.subcategoryname from subcategories s where p.subcategoryid=s.subcategoryid) as scname,(select b.brandname from brands b where p.brandid=b.brandid) as bname from products p"
        cmd.execute(query)
        products = cmd.fetchall()
        db.close()

        return render(request, "DisplayProducts.html", {'product': products})

    except Exception as e:

        return render(request, "DisplayProducts.html", {'product': None})


@xframe_options_exempt
def edit_productimage(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        productid = request.POST['productid']
        image = request.FILES['image']

        query = "update products set productimage='{0}' where productid={1}".format(image.name, productid)

        F = open("E:/medassist_ecom/assets/" + image.name, 'wb')
        for chunk in image.chunks():
            F.write(chunk)
        F.close()
        print(query)
        cmd.execute(query)
        db.commit()
        db.close()
        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        return JsonResponse({'result': False}, safe=False)


@xframe_options_exempt
def delete_product(request):
    try:
        db, cmd = Pool.ConnectionPooling()

        productid = request.GET['productid']
        print("hi")
        query = "delete from products where productid={0}".format(productid)
        print(query)
        cmd.execute(query)
        db.commit()
        db.close()
        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        return JsonResponse({'result': False}, safe=False)

@xframe_options_exempt
def edit_product(request):
    try:
                
        db, cmd = Pool.ConnectionPooling()

        categoryid=request.GET['categoryid']
        subcategoryid=request.GET['subcategoryid']
        brandid=request.GET['brandid']
        productname=request.GET['productname']
        price=request.GET['price']
        offerprice=request.GET['offerprice']
        packingtype=request.GET['packingtype']
        qty=request.GET['qty']
        rating=request.GET['rating']
        salestatus=request.GET['salestatus']
        status=request.GET['status']
        productid=request.GET['productid']
        print("got everything")
        query = "update products set categoryid={0},subcategoryid={1},brandid={2},productname='{3}',price={4},offerprice={5},packingtype='{6}',status='{7}',salestatus='{8}',quantity={9},rating={10} where productid={11}".format(categoryid,subcategoryid,brandid,productname,price,offerprice,packingtype,status,salestatus,qty,rating,productid)
        print(query)
        cmd.execute(query)
        db.commit()
        db.close()
        return JsonResponse({'result': True}, safe=False)
    except Exception as e:
        print("error:",Exception)
        return JsonResponse({'result': False}, safe=False)


@xframe_options_exempt
def images_interface(request):
    try:
        admin = request.session['ADMIN']
    except:
        return render(request, 'Login_Page.html')
    return render(request,"AddPictures.html")


@xframe_options_exempt
def Add_picture(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        brandid=request.POST['brandid']
        productid=request.POST['productid']
        productimage=request.FILES['productimage']
        query="insert into pictures(categoryid,subcategoryid,brandid,productid,image) values('{0}','{1}','{2}','{3}','{4}')".format(categoryid,subcategoryid,brandid,productid,productimage)
        F = open("E:/medassist_ecom/assets/" + productimage.name, 'wb')
        for chunk in productimage.chunks():
            F.write(chunk)
        F.close()
        cmd.execute(query)
        db.commit()
        db.close()
        return render(request,"AddPictures.html",{'message':'Picture added successfully'})
    except Exception as e:
        return render(request,"AddPictures.html",{'message':'Something went wrong'})



@xframe_options_exempt
def fetch_all_product_json(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        subcategoryid=request.GET['subcategoryid']
        categoryid=request.GET['categoryid']
        brandid=request.GET['brandid']
        query = "select * from products where categoryid={0} and subcategoryid={1} and brandid={2}".format(categoryid,subcategoryid,brandid)
        cmd.execute(query)
        brands = cmd.fetchall()
        db.close()
        return JsonResponse({'data': brands}, safe=False)
    except Exception as e:
        return JsonResponse({'data': None}, safe=False)



