"""medassist_ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import Category_Controller
from . import Subcategory_Controller
from . import Brand_Controller
from . import Product_Controller
from . import Admin_Controller
from . import UserInterface
urlpatterns = [
    path('admin/', admin.site.urls),
    path('categoryinterface/',Category_Controller.Category_Interface),
    path('submitcategory', Category_Controller.Submit_Category),
    path('displayallcategories/', Category_Controller.Display_All_Category),
    path('editcategory/', Category_Controller.Edit_Category),
    path('deletecategory/', Category_Controller.Delete_Category),
    path('editcategoryicon', Category_Controller.Edit_CategoryIcon),
    path('fetch_all_category_json', Category_Controller.Fetch_All_Category_JSON),

    path('subcategoryinterface/', Subcategory_Controller.Subcategory_Interface),
    path('submitsubcategory', Subcategory_Controller.Submit_Subcategory),
    path('displayallsubcategories', Subcategory_Controller.Display_All_Subcategory),
    path('editsubcategory/', Subcategory_Controller.Edit_Subcategory),
    path('deletesubcategory/', Subcategory_Controller.Delete_Subcategory),
    path('editsubcategoryicon', Subcategory_Controller.Edit_SubcategoryIcon),

    path('brandinterface',Brand_Controller.brand_interface),
    path('fetchallsubcategoriesjson/',Subcategory_Controller.fetch_all_subcategory_json),
    path('submitbrand',Brand_Controller.submit_brand),
    path('displayallbrands',Brand_Controller.display_all_brands),
    path('editbrand/',Brand_Controller.edit_brand),
    path('deletebrand/',Brand_Controller.delete_brand),
    path('editbrandicon',Brand_Controller.edit_brandicon),

    path('productinterface/',Product_Controller.product_interface),
    path('submitproduct',Product_Controller.submit_Product),
    path('fetchallbrandsjson/',Product_Controller.fetch_all_brand_json),
    path('displayallproducts/',Product_Controller.display_all_products),
    path('editproductimage',Product_Controller.edit_productimage),
    path('deleteproduct/',Product_Controller.delete_product),
    path('editproducts/',Product_Controller.edit_product),
    path('imagesinterface',Product_Controller.images_interface),
    path('fetchallproductsjson/',Product_Controller.fetch_all_product_json),
    path('submitimage',Product_Controller.Add_picture),

path('adminlogin/',Admin_Controller.Admin_Login),
path('adminlogout/',Admin_Controller.Admin_Logout),
path('checkadminlogin',Admin_Controller.Check_Admin_Login),
path('home/',UserInterface.Index),
path('fetch_all_user_category/',UserInterface.Fetch_All_Category_JSON),

path('fetch_all_products/',UserInterface.Fetch_All_Products),
path('fetch_all_subcategory_json/',UserInterface.Fetch_All_SubCategory_JSON),
path('buy_product/',UserInterface.Buy_Product),
path('add_to_cart/',UserInterface.AddToCart),
path('fetch_cart/',UserInterface.FetchCart),
path('remove_from_cart/',UserInterface.RemoveFromCart),
path('my_shopping_cart/',UserInterface.MyShoppingCart),
path('check_user_mobileno/',UserInterface.CheckUserMobileno),
path('insert_user/',UserInterface.InsertUser),
path('check_user_mobileno_for_address/',UserInterface.CheckUserMobilenoForAddress),
path('insert_user_address/',UserInterface.InsertUserAddress),


]
