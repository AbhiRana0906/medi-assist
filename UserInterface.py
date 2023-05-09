from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
import json
from urllib.parse import unquote
def AddToCart(request):
    try:
     product = request.GET['product']
     qty=request.GET['qty']
     product=product.replace("'","\"")
     product=json.loads(product)
     product['qty']=qty
     print('UPDATED PRODUCTS:',product)
     #create cart container using Session
     try:
       CART_CONTAINER=request.session['CART_CONTAINER']
       CART_CONTAINER[str(product['productid'])]=product
       request.session['CART_CONTAINER']=CART_CONTAINER

     except:
       CART_CONTAINER={}
       CART_CONTAINER[str(product['productid'])]=product
       request.session['CART_CONTAINER']=CART_CONTAINER

     print("CART_CONTAINER:",CART_CONTAINER)
     CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")

     return JsonResponse({'data': CART_CONTAINER}, safe=False)
    except Exception as err:
        print("ERRORRRRR:",err)
        return JsonResponse({'data': []}, safe=False)

def FetchCart(request):
    try:
     try:
       CART_CONTAINER=request.session['CART_CONTAINER']

     except:
       CART_CONTAINER={}

     print("CART_CONTAINER:",CART_CONTAINER)
     CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")

     return JsonResponse({'data': CART_CONTAINER}, safe=False)
    except Exception as err:
        print("ERRORRRRR:",err)
        return JsonResponse({'data': []}, safe=False)

def RemoveFromCart(request):
    try:
       productid = request.GET['productid']

       CART_CONTAINER=request.session['CART_CONTAINER']
       del CART_CONTAINER[productid]
       request.session['CART_CONTAINER']=CART_CONTAINER
       print("REMOVE CART_CONTAINER:",CART_CONTAINER)
       CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")
       return JsonResponse({'data': CART_CONTAINER}, safe=False)
    except Exception as err:
        print("ERRORRRRR:",err)
        return JsonResponse({'data': []}, safe=False)




def Index(request):
    return render(request,"index.html")

def MyShoppingCart(request):
    try:
        try:
            CART_CONTAINER = request.session['CART_CONTAINER']
            total=0
            totalprice=0
            totalsavings=0
            for key in CART_CONTAINER.keys():
                amt=(CART_CONTAINER[key]['price']-CART_CONTAINER[key]['offerprice'])
                CART_CONTAINER[key]['save']=amt*int(CART_CONTAINER[key]['qty'])
                totalsavings+=CART_CONTAINER[key]['save']
                CART_CONTAINER[key]['productprice'] = CART_CONTAINER[key]['offerprice']* int(CART_CONTAINER[key]['qty'])
                total+=CART_CONTAINER[key]['offerprice']*int(CART_CONTAINER[key]['qty'])
                totalprice += CART_CONTAINER[key]['price'] * int(CART_CONTAINER[key]['qty'])

        except Exception as err:
            CART_CONTAINER = {}
            print ("Errrrrrrr",err)

        print("My Shopping CART_CONTAINER:", CART_CONTAINER.values())
        #CART_CONTAINER = str(CART_CONTAINER).replace("'", "\"")

        return render(request, "MyCart.html",{'data': CART_CONTAINER.values(),'totalamount':total,'totalproducts':len(CART_CONTAINER.keys()),'totalprice':totalprice,'totalsavings':totalsavings})

    except Exception as err:
        print("ERRORRRRR:", err)
        return render(request, "MyCart.html", {'data':{}})


def Buy_Product(request):
    product=unquote(request.GET['product'])
    product=json.loads(product)
    print("zzzzzzzzzzzzz",product)
    db, cmd = Pool.ConnectionPooling()
    query = "select * from pictures where productid={0}".format(product['productid'])
    cmd.execute(query)
    pictures = cmd.fetchall()

    db.close()

    return render(request,"Buy_product.html",{'product':product,'pictures':pictures})
def Fetch_All_Products(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        query = "select p.*,(select c.categoryname from categories c where c.categoryid=p.categoryid) as cname,(select s.subcategoryname from subcategories s where p.subcategoryid=s.subcategoryid) as scname,(select b.brandname from brands b where p.brandid=b.brandid) as bname from products p"
        cmd.execute(query)
        products = cmd.fetchall()
        db.close()

        return JsonResponse({'data': products}, safe=False)

    except Exception as e:

        return JsonResponse({'data': []}, safe=False)

def Fetch_All_Category_JSON(request):
    try:
      DB, CMD = Pool.ConnectionPooling()
      Q = "select * from categories"
      CMD.execute(Q)
      records = CMD.fetchall()
      print('RECORDS:', records)
      DB.close()
      return JsonResponse({'data': records}, safe=False)
    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def Fetch_All_SubCategory_JSON(request):
    try:
      DB, CMD = Pool.ConnectionPooling()
      Q = "select * from subcategories"
      CMD.execute(Q)
      records = CMD.fetchall()
      print('RECORDS:', records)
      DB.close()
      return JsonResponse({'data': records}, safe=False)
    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)
def  CheckUserMobileno(request):
    mobileno=request.GET['mobileno']
    try:
      DB, CMD = Pool.ConnectionPooling()
      Q = "select * from  users where mobileno='{0}'".format(mobileno)
      CMD.execute(Q)
      record = CMD.fetchone()
      print('User:', record)
      if(record):
          return JsonResponse({'data': record,'status':True}, safe=False)
      else:
          return JsonResponse({'data':[], 'status': False}, safe=False)
      DB.close()

    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)

def  InsertUser(request):
    mobileno=request.GET['mobileno']
    emailid = request.GET['emailid']
    firstname = request.GET['firstname']
    lastname = request.GET['lastname']
    password = request.GET['password']
    try:
      DB, CMD = Pool.ConnectionPooling()
      Q = "insert into users values('{0}','{1}','{2}','{3}','{4}')".format(emailid,mobileno,firstname,lastname,password)
      CMD.execute(Q)
      DB.commit()
      DB.close()
      return JsonResponse({'status':True}, safe=False)


    except Exception as e:
      print('Error:', e)
      return JsonResponse({'status':False}, safe=False)

def  CheckUserMobilenoForAddress(request):
    mobileno=request.GET['mobileno']
    try:
      DB, CMD = Pool.ConnectionPooling()
      Q = "select UA.*,(select U.firstname from users U where U.mobileno=UA.mobileno) as firstname,(select U.lastname from users U where U.mobileno=UA.mobileno) as lastname  from  users_address UA where UA.mobileno='{0}'".format(mobileno)
      CMD.execute(Q)
      record = CMD.fetchone()
      print('User:', record)
      if(record):
          return JsonResponse({'data': record,'status':True}, safe=False)
      else:
          return JsonResponse({'data':[], 'status': False}, safe=False)
      DB.close()

    except Exception as e:
      print('Error:', e)
      return JsonResponse({'data': []}, safe=False)


def  InsertUserAddress(request):
    mobileno=request.GET['mobileno']
    emailid = request.GET['emailid']
    addressone = request.GET['addressone']
    addresstwo = request.GET['addresstwo']
    landmark = request.GET['landmark']
    city = request.GET['city']
    state = request.GET['state']
    zipcode = request.GET['zipcode']
    try:
      DB, CMD = Pool.ConnectionPooling()
      Q = "insert into users_address(mobileno, emailid, address1, address2, landmark, city, state, zipcode) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(mobileno,emailid,addressone,addresstwo,landmark,city,state,zipcode)
      print(Q)
      CMD.execute(Q)
      DB.commit()
      DB.close()
      return JsonResponse({'status':True}, safe=False)


    except Exception as e:
      print('Error:', e)
      return JsonResponse({'status':False}, safe=False)

