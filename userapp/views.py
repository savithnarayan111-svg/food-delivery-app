from itertools import product
import json
from os import stat
from urllib import request, response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from adminapp.models import Product, Restaurant
from userapp.models import Cart, CartItem, Profile, Review, Wishlist, WishlistItem
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken



# CREATE YOUR VIEWS HERE.

@csrf_exempt
def Signup(request):
    if request.method=="POST":
        data = json.loads(request.body)
        rname=data.get("nme")
        rmail=data.get("mail")
        rage=data.get("age")
        rnum=data.get("num")
        rpass=data.get("pass")
        # Cpass=request.POST.get("cpass")
        Signup.objects.create(
            Name=rname,
            Email=rmail,
            Age=rage,
            Phone=rnum,
            Password=rpass,
            # ConPass=Cpass
            )
    return JsonResponse({'message':'added!'})

#SIGNUP

@csrf_exempt
def user_signup(request):
    if request.method=='POST':
        
        rfname=request.POST.get('fname')
        rlname=request.POST.get('lname')
        rpass=request.POST.get('pass')
        rmail=request.POST.get('mail')
        rphone=request.POST.get('phone')
        raddress=request.POST.get('address')
        rzipcode=request.POST.get('zipcode')
        if not rmail or not rphone or not raddress:
            return HttpResponse("This is mandatory")
        userr=User.objects.create_user(
            first_name=rfname,
            last_name=rlname,
            email=rmail,
            username=rmail, 
            password=rpass
        )
        Profile.objects.create(
            user=userr,
            Phone=rphone,
            Zipcode=rzipcode,
            Address=raddress,
            
        )
        # return JsonResponse({'message':'success'})
    return JsonResponse({'message':'successfully'})





#SESSION BASED AUTHENTICATION


# @csrf_exempt
# def user_login(request):
#     if request.method=='POST':
#             rmail=request.POST.get('mail')
#             rpass=request.POST.get('pass')
#             if not rmail or not rpass:
#                  return HttpResponse("This field is mandatory")
#             try:
#              user=User.objects.get(username=rmail)  #left--db
#              print(user)
#             except:
#                 if User.DoesNotExist:
#                     return JsonResponse({'message':'Invalid credentials'})
#             if not user.check_password(rpass):
#                 return JsonResponse({'message':'Not registered'})
#             login(request,user)                             #
#             return JsonResponse({'message':' registered'})


#AUTHENTICATE()

@csrf_exempt
def user_login(request):
    if request.method=='POST':
             rmail=request.POST.get('mail')
             rpass=request.POST.get('pass')
             user=authenticate(username=rmail,password=rpass)  #left-db
             if user is not None:   #None → if credentials are wrong
                  login(request,user)
                  return JsonResponse({'message':' registered'})
             else:
               return JsonResponse({'message':'Invalid credentials'})      

 
#ONLY ENTER WHEN LOGIN

#MANUALLY WITHOUT LOGIN REQUIRED

# def add_to_cart(request):
#     if request.user.is_authenticated:
#            return JsonResponse( {'message':'order created for'+" "+ request.user.username})  #request.user==It is the currently logged-in user,request.user.usernameIt is the username of the logged-in user
     
#     return JsonResponse({'message':'you are not AUTHENTICATED'},status=401)

#DJANGO SESSION BASED AUTHENTICATION

# @csrf_exempt
# def User_login(request):
#     if request.method=='POST':
#             rmail=request.POST.get('mail')
#             rpass=request.POST.get('pass')
#             user=authenticate(username=rmail,password=rpass)
#             if user is not None:   
#                 token,created=Token.objects.get_or_create(user=user)  #if there is user get token or else create new token 
#                 return JsonResponse({'message':'success'})  


 #DJANGO JWT  AUTHENTICATION





@csrf_exempt
def token_login(request):
     if request.method=="POST":
          remail=request.POST.get('mail')
          rpass=request.POST.get('pass')
          if not remail or not rpass:
               return HttpResponse("This is mandatory")
          user=authenticate(username=remail,password=rpass)
          if user is None:
               return JsonResponse({'message':'Invalid credentials'})
          else:
               refresh=RefreshToken.for_user(user)
               return JsonResponse(
                    {
                         "refresh":str(refresh),
                         "access":str(refresh.access_token),
                         "User":{"id":user.id,"username":user.username,"email":user.email}
                    }
               )


from rest_framework.decorators import permission_classes,api_view

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buy_food(request):
      return JsonResponse({'message':"ordere created",
                           "user": request.user.username})


#ADD TO CART
@api_view(['POST'])
@permission_classes([IsAuthenticated])  #This means only logged-in users can access this API.
def add_to_cart(request):
    item_id=request.POST.get('id')
    quantity=int(request.POST.get('quantity',1))
    data=Product.objects.get(id=item_id)
    cart,created=Cart.objects.get_or_create(user=request.user)      #dbfield=logged_in user
    CartItem.objects.get_or_create(
         product=data,
         cart=cart
    )

    return JsonResponse({
        "message": "Product added to cart",
          "product": data.Name,
          "price":data.price,
           "quantity": quantity
        })


#WISHLIST

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
     item=request.POST.get('id')
     data=Product.objects.get(id=item)
     wishlist,created=Wishlist.objects.get_or_create(user=request.user) 
     WishlistItem.objects.get_or_create(
          product=data,
          wishlist=wishlist
     )
     return JsonResponse({
          "message":"Item added to wishlist",
          "product":data.Name
     })

#ADD REVIEW
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_review(request):
#      rrating=request.POST.get("rating")
#      rreview=request.POST.get("review")
#      Review.objects.create(
#           Rating=rrating,
#           Review=rreview
#                              )
#      return JsonResponse({"message": "Success"}, status=201)# 


#..................................REVIEW...........................



# ADD REVIEW
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):

    rrating = request.data.get("rating")
    rreview = request.data.get("review")
    product_id = request.data.get("product_id")

    # if not product_id:
    #     return JsonResponse({"error": "product_id is required"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    Review.objects.create(
        user=request.user,
        product=product,
        Rating=int(rrating),
        Review=rreview
    )

    return JsonResponse({"message": "Success"}, status=201)

#DELETE REVIEW

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request):
    item_id = request.POST.get('item_id')
    try:
        review=Review.objects.get(user=request.user, product_id=item_id)#user=request.user → review must belong to the currently logged-in user.#product_id=item_id → review must be for the given product ID.
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"})

    review.delete()
    return JsonResponse({"message": "Review deleted successfully"})


# UPDATE REVIEW


@api_view(['GET']) 
def update_review(request):
    item_id = request.POST.get('item_id')
    try:
        review=Review.objects.get(user=request.user, product_id=item_id)#user=request.user → review must belong to the currently logged-in user.#product_id=item_id → review must be for the given product ID.
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"})
     

     
     













































# @api_view(['POST'])
# @permission_classes([IsAuthenticated])

# def add_to_cart(request):
#     item_id = request.POST.get('id')
#     quantity = int(request.POST.get('quantity', 1))

#     product = get_object_or_404(Product, id=item_id)

#     # get or create cart for logged-in user
#     cart, created = Cart.objects.get_or_create(user=request.user)

#     # get or create cart item
#     cart_item, created = CartItem.objects.get_or_create(
#         product=product,
#         cart=cart,
#         defaults={'quantity': quantity}
#     )

#     # if already exists → increase quantity
#     if not created:
#         cart_item.quantity += quantity
#         cart_item.save()

#     return JsonResponse({
#         "message": "Product added to cart",
#         "product": product.Name,
#         "quantity": cart_item.quantity
#     })
