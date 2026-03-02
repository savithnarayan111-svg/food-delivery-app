from itertools import product
import json
from os import stat
from urllib import request, response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from adminapp.models import Product, Restaurant
from userapp.models import Cart, CartItem, Profile, RestaurantReview, Review, Wishlist, WishlistItem
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Avg




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

#........................................PROFILE.......................................

#VIEW PROFILE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    user=request.user
    profile = user.profile
    phone = profile.Phone
    address = profile.Address
    zipcode = profile.Zipcode

    data = {
        "fname": user.first_name,
        "lname": user.last_name,
        "mail": user.email,
        "phone": phone,
        "address": address,
        "zipcode": zipcode,
    }

    return JsonResponse(data)
 
#UPDATE PROFILE

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user=request.user
    profile = user.profile
    user.first_name = request.data.get("fname", user.first_name)
    user.save()
    profile.Address = request.data.get("address", profile.Address)
    profile.save()
    return JsonResponse({"message":"updated succesfully"})




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




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buy_food(request):
      return JsonResponse({'message':"ordere created",
                           "user": request.user.username})


#.......................................CART..........................................

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


#VIEW CART

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart=Cart.objects.get(user=request.user)
    views=CartItem.objects.filter(cart=cart)
    data=[]

    for i in views:
            data.append({
            "product_name": i.product.Name,
            "price": i.product.price,
            "quantity":i.quantity
        }) 
    return JsonResponse(data, safe=False)
      

#REMOVE SINGLE ITEM

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart(request):
    item_id=request.POST.get('item_id')
    cart=CartItem.objects.get(id=item_id)
    cart.delete()
    return JsonResponse({"message":"deleted successfully"})

#DELETE CART ITEMS

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    cart=Cart.objects.get(user=request.user)
    newcart=CartItem.objects.filter(cart=cart)
    newcart.delete()
    return JsonResponse({"message":"deleted successfully"})

#UPDATE ITEM

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_quantity(request):
    item_id = request.data.get('item_id')
    new_quantity = request.data.get('quantity')
    cart_item = CartItem.objects.get(cart__user=request.user, id=item_id)
    cart_item.quantity = int(new_quantity)
    cart_item.save() 

    return JsonResponse({"message": "Updated successfully"})

#WISHLIST_TO_CART

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_to_cart(request):

    item_id=request.POST.get('item_id')
    try:
        wishlist=WishlistItem.objects.get(product_id=item_id,wishlist__user=request.user)
    except WishlistItem.DoesNotExist:
        return JsonResponse({"message":"Does not exist"})

    cartitem,created=CartItem.objects.get_or_create(
        cart__user=request.user,
        product=wishlist.product
    )

    wishlist.delete()

    return JsonResponse({
        "message": "Item moved to cart successfully",
        "product": cartitem.product.Name
    })






#...................................................WISHLIST...........................................

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
     if not created:
         return JsonResponse({"message": "Product already in wishlist"})
     return JsonResponse({
          "message":"Item added to wishlist",
          "product":data.Name 
     })

#VIEW WISHLIST

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)
    items = WishlistItem.objects.filter(wishlist=wishlist)

    data = []
    for i in items:
        data.append({
            "product_name": i.product.Name,
            "price": i.product.price
        })

    return JsonResponse(data, safe=False)

#DELETE WISHLIST


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_wishlist(request):
    item_id = request.data.get('item_id')
    try:
        wishlist=WishlistItem.objects.get(id=item_id)#user=request.user → review must belong to the currently logged-in user  #id = item_id
    except WishlistItem.DoesNotExist:
        return JsonResponse({"error": "Not found"})
    wishlist.delete()
    return JsonResponse({"message": "Wishlist deleted successfully"})





#.....................................................REVIEW..........................................



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
        Review=rreview,

    )

    return JsonResponse({"message": "Success"}, status=201)

#DELETE REVIEW

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request):
    item_id = request.POST.get('item_id')
    try:
        review=Review.objects.get(user=request.user, id=item_id)#user=request.user → review must belong to the currently logged-in user  #id = item_id
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"})

    review.delete()
    return JsonResponse({"message": "Review deleted successfully"})


# UPDATE REVIEW

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_review(request):
    item_id = request.POST.get('item_id')
    # updated_review = request.data.get('review')
    try:
        review=Review.objects.get(user=request.user, id=item_id)#user=request.user → review must belong to the currently logged-in user.#product_id=item_id → review must be for the given product ID.
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"})

    review.Review = request.data.get('review', review.Review)
    review.save()
    return JsonResponse({"message": "Updated successfully"})
    

#VIEW REVIEW

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_review(request,id):
    reviews=Review.objects.filter(product_id=id)
    data=[]
    for i in reviews:
        data.append({
            "rating":i.Rating,
            "review":i.Review,
            "user":i.user.username
        })
    return JsonResponse(data,safe=False)

#ADD RESTAURANT REVIEW

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_restaurant_review(request):

    item_id=request.POST.get('restaurant_id')
    rreview=request.POST.get('review')
    rrating=request.POST.get('rating')

    try:
        restaurant=Restaurant.objects.get(id=item_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({"message":"Restaurant not found"})
    
    RestaurantReview.objects.create(
        user=request.user,
        restaurant=restaurant,
        Rating=int(rrating),
        Review=rreview,
    )
    return JsonResponse({"message": "Success"}, status=201)

#VIEW RESTAURANT REVIEW

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_restaurant_review(request,id):
    reviews=RestaurantReview.objects.filter(restaurant_id=id)
    data=[]
    for i in reviews:
        data.append({
            "rating":i.Rating,
            "review":i.Review,
            "user":i.user.username
        })
    return JsonResponse(data,safe=False)

#VIEW AVERAGE RATING

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def average_rest_rating(request,id):
    average=RestaurantReview.objects.filter(restaurant_id=id).aggregate(avg=Avg('Rating'))['avg']

    return JsonResponse({
        "restaurant_id": id,
        "average_rating": average
    })

#....................................................SEARCH...............................................

#SEARCH RESTAURANT

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_restaurants(request):
    query=request.GET.get('q')

    restaurants=Restaurant.objects.filter(
        Q(Location__icontains=query)|
        Q(Restaurant_name__icontains=query)
    )
    if not  restaurants:
        return JsonResponse({"message":"Restaurant not found"})
    data=[]
    for i in restaurants:
        data.append({
            "location":i.Location,
            "name":i.Restaurant_name
        })
        return JsonResponse(data,safe=False)
    

#SEARCH PRODUCT

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_product(request):
    query=request.GET.get('q')
    restaurant_id=request.GET.get('r')

    try:
        restaurant=Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({"message":"Restaurant not found"})
    
    # product=Product.objects.filter(Restaurant=restaurant).filter(

    #     Q(Name__icontains=query)
    # )
    product = Product.objects.filter(
        Restaurant=restaurant,
         Name__icontains=query ,
        
    )
    if not product:
        return JsonResponse({"message":"Product not found"})
    data=[]
    for i in product:
        data.append({
            "name":i.Name,
            "price":i.price

        })
    return JsonResponse(data,safe=False)

#SEARCH PRODUCT_LIST

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_product_list(request):
    query=request.GET.get('q')
    search=Product.objects.filter


#>......................................FILTER..................................

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def filtering_Price(request):
    restaurant_id=request.GET.get('r')
    min=request.GET.get('min')
    max=request.GET.get('max')
    try:
        restaurant=Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return JsonResponse({"message":"Restaurant not found"})
    product = Product.objects.filter(Restaurant=restaurant)
    # products=product
    if min:
        products=product.filter(price__gte=min)
    if max:
        products=product.filter(price__lte=max)
    if not product:
        return JsonResponse({"message":"Product not found"})
    data=[]
    for i in products:
        data.append({
            "name":i.Name,  
            "price":i.price
 
        })
    return JsonResponse(data,safe=False)


#SORT RESTAURANT

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_restaurant(request):
    sort=request.GET.get('sort','Restaurant_name')
    restaurants=Restaurant.objects.all().order_by(sort)
    data=[]
    for i in restaurants:
        data.append({
            "name":i.Restaurant_name
        })
    return JsonResponse(data,safe=False)


