from os import stat
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from adminapp.models import Coupon, Product, Restaurant
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes,api_view

from rest_framework.permissions import IsAuthenticated
from userapp.models import Profile, RestaurantReview, Review






#.......................................RESTAURANT.................................

#ADD RESTAURANT

@csrf_exempt      #This decorator allows POST requests from Postman, mobile apps, or frontend APIs.
def Add_Restaurant(request):
        if request.method=='POST':
                rname=request.POST.get('name')     #Gets the value of name from the POST request.
                rdescription=request.POST.get('description')
                rimage=request.POST.get('image')
                rlocation=request.POST.get('location')
                rrating=request.POST.get('rating')
                rtime=request.POST.get('time')
                rcontact=request.POST.get('contact')
                remail=request.POST.get('email')
                
                if not rname or  not rlocation or not rcontact:
                    return HttpResponse("This field is mandatory",status=400)     #BAD REQUEST::::The client sent invalid or incomplete data.
                
                try:
                    
                    Restaurant.objects.create(
                        Restaurant_name=rname,
                        Image=rimage,
                        Description=rdescription,
                        Location=rlocation,
                        Rating=rrating,
                        Time=rtime,
                        Contact=rcontact,
                        Email=remail 
                    )
            
                    return JsonResponse({"message": "Success"}, status=201)  #return HttpResponse("Success",status=201)
        
                except Exception as e:
                    return HttpResponse(str(e),status=500)     #The problem occurred on the server side:::::str(e).....Sends the actual error message for debugging.
        return HttpResponse("method not allowed",405)    #Method Not Allowed:::::This API only supports POST requests.


#VIEW RESTAURANT

@csrf_exempt
def View_restaurants(request):
    restaurants_list= Restaurant.objects.all()
    # print(restaurants_list)
    new_list=[]
    for i in restaurants_list:
         new_list.append({
            "name": i.Restaurant_name,
            # "image": i.Image,
            "description": i.Description,
            "location": i.Location,
            "rating": i.Rating,
            "time": i.Time,
            "contact": i.Contact,
            "email": i.Email,
        })
 
    # return HttpResponse(new_list)

    return JsonResponse(new_list, safe=False)  #to show as list


#VIEW SINGLE RESTAURANT


def view_single_restaurant(request,id):
    try:
        data=Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:   #the item does not in database it shows an error
         print("")
    item={
            "name": data.Restaurant_name,
            "description": data.Description,
            "location": data.Location,
            "rating": data.Rating,
            "time": data.Time,
            "contact": data.Contact,
            "email": data.Email,
    }
    return JsonResponse(item)    
    
          


#simple way....dont want try and exept

def View_Single_restaurant(request,id):
    new_data=get_object_or_404(Restaurant,id=id)
    new_item={
            "name": new_data.Restaurant_name,
            "description": new_data.Description,
            "location": new_data.Location,
            "rating": new_data.Rating,
            "time": new_data.Time,
            "contact": new_data.Contact,
            "email": new_data.Email,
    }
    return JsonResponse(new_item)      

#REMOVE RESTAURANT

@csrf_exempt
def Remove_restaurant(request,id):
     if request.method=="DELETE":
        remove=Restaurant.objects.get(id=id)
        remove.delete()
        return JsonResponse({'message':'successfully created'})

#uPDATE RESTAURANT

@csrf_exempt
def update_restaurant(request,id):
    try:
     temp=Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error':'item not found'},status=404)
    if request.method=="GET":
        update_item={
            "name": temp.Restaurant_name,
            "description":temp.Description,
            "location":temp.Location,
            "rating":temp.Rating,
            "time":temp.Time,
            "contact":temp.Contact,
            "email":temp.Email,
    }
        return JsonResponse(update_item,status=200)
    
    elif request.method=="POST":
        # temp=Restaurant.objects.get(id=id)
        temp.Restaurant_name=request.POST.get("name", temp.Restaurant_name)#("name", temp.Restaurant_name) ::::we cannot save form as an empty field.if there are no errors,the existing data wants to show.
        temp.Description=request.POST.get("description",temp.Description) 
        temp.Location=request.POST.get("location",temp.Location) 
        temp.Rating=request.POST.get("rating",temp.Rating) 
        temp.Time=request.POST.get("time",temp.Time) 
        temp.Contact=request.POST.get("contact",temp.Contact) 
        temp.Email=request.POST.get("email",temp.Email) 
        temp.save()
        return JsonResponse({'message':'successfully updated'},status=200)


#VIEW USERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_users(request):
    users = User.objects.all()
    data = []
    for u in users:
        try:
            phone = u.profile.Phone
            address = u.profile.Address
            zipcode = u.profile.Zipcode
        except Profile.DoesNotExist:
            phone = ""
            address = ""
            zipcode = ""

        data.append({
            "fname": u.first_name,
            "lname": u.last_name,
            "mail": u.email,
            "phone": phone,
            "address": address,
            "zipcode": zipcode,
        })

    return JsonResponse(data, safe=False)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_users(request):
#     user=User.objects.all()
#     # profile=Profile.objects.all()
#     data=[]
#     for i in user:
#          data.append({
#               "fname":i.first_name,
#               "lname":i.last_name,
#               "mail":i.email,
#               "phone":i.profile.phone,
#               "address":i.profile.address,
#               "zipcode":i.profile.zipcode,
#          })
#     return JsonResponse(data,safe=False)
     


#.................................PRODUCT..................................

#ADD PRODUCT

@csrf_exempt   
def Add_Product(request,id):
        Products=get_object_or_404(Restaurant,id=id)
        if request.method=='POST':
            rname=request.POST.get('name')
            rprice=request.POST.get('price')
            rdescription=request.POST.get('description')
            Product.objects.create(
                     Name=rname,
                     price=rprice,
                     Description=rdescription,
                     Restaurant=Products

                    )
            
            return JsonResponse({"message": "Success"}, status=201)  
        return HttpResponse("method not allowed",405) 


#VIEW PRODUCT

@csrf_exempt
def view_product(request):
     Product_list=Product.objects.all()
     empty_list=[]
     for i in Product_list:
          empty_list.append({
               "name":i.Name,
               "decsription":i.Description,
               "price":i.price,     
          })
     return JsonResponse(empty_list,safe=False)

#VIEW SINGLE PRODUCT

@csrf_exempt
def view_single_product(request,id):
     Product_list=get_object_or_404(Restaurant,id=id)
     products=Product.objects.filter(Restaurant=Product_list)  # Fetches multiple Product records from the database. → Filters products whose Restaurant foreign key matches Product_list.
     empty_list=[]
     for i in products:
          empty_list.append({
               "name":i.Name,
               "decsription":i.Description,
               "price":i.price,     
          })
     return JsonResponse(empty_list,safe=False)
     
#REMOVE PRODUCT  
     
@csrf_exempt
def remove_product(request,id):
     if request.method=="DELETE":
          remove_product=Product.objects.get(id=id)
          remove_product.delete()
     return JsonResponse({'message':'Successfully deleted'})

#UPDATE PRODUCT

@csrf_exempt
def update_product(request, id):
    try:
        temp = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'item not found'}, status=404)
    if request.method == "GET":
        update_item = {
            "name": temp.Name,
            "description": temp.Description,
            "price": temp.price,
        }
        return JsonResponse(update_item)
    elif request.method == "POST":
        temp.Name = request.POST.get("name", temp.Name)
        temp.Description = request.POST.get("description", temp.Description)
        temp.price = request.POST.get("price", temp.price)
        temp.save()
        return JsonResponse({'message': 'updated successfully'})



#coupon


@csrf_exempt
def  Add_coupon(request):
     if request.method=='POST':
          rcoupon=request.POST.get('name')
          rdescription=request.POST.get('description')
          rdiscount=request.POST.get('discount')

          Coupon.objects.create(
               Coupon_name=rcoupon,
               Description=rdescription,
               Discount=rdiscount,
          )

          return JsonResponse({'message':'coupon added succesfully'})
    
     return JsonResponse({'message':'coupon added succesfully'})

@csrf_exempt
def View_coupon(request):
    Coupon_list=Coupon.objects.all()
    empty_list=[]
    for i in Coupon_list:
        empty_list.append({
            "name":i.Coupon_name,
            "description":i.Description,
            "discount":i.Discount,
        })
    return JsonResponse(empty_list, safe=False)

@csrf_exempt
def Coupon_delete(request,id):
     if request.method=="DELETE":
          Delete_coupon=Coupon.objects.get(id=id)
          Delete_coupon.delete()
          return JsonResponse({'message':'Successfully deleted'})
     

@csrf_exempt
def Update_coupon(request,id):
     temp=Coupon.objects.get(id=id)
     if request.method=='GET':
          update_coupon={
               "name":temp.Coupon_name,
               "description":temp.Description,
               "discount":temp.Discount,
          }
          return JsonResponse(update_coupon)

     elif request.method=="POST":
          temp.Coupon_name=request.POST.get("name",temp.Coupon_name)
          temp.Description=request.POST.get("description",temp.Description)
          temp.Discount=request.POST.get("discount",temp.Discount)
          temp.save()
          return JsonResponse({'message':'updated successfully'})
     

#.........................................REVIEWS................................

#VIEW REVIEW

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_review(request):
    review=Review.objects.all()
    data=[]
    for i in review:
         data.append({
         "user":i.user.username,
          "product":i.product.id,
         "rating":i.Rating,
         "review":i.Review   
         })
    return JsonResponse(data,safe=False)

#FILTER REVIEWS

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filtering_rating(request):
    query=request.GET.get('q')
    min=request.GET.get('min')
    max=request.GET.get('max')
    try:
     restaurant=Restaurant.objects.get(id=query)
    except Restaurant.DoesNotExist:
        return JsonResponse({"message":"Restaurant not found"})
    
    reviews=RestaurantReview.objects.filter(restaurant=restaurant)

    if min:
        rating=reviews.filter(Rating__gte=min)
    if max:
        rating=reviews.filter(Rating__gte=max)
    if not reviews:
        return JsonResponse({"message":"Review not found"})
    data=[]
    for i in rating:
        data.append({
            "name":i.Review,
            "rating":i.Rating,
            "restaurant":i.restaurant.id,
            

        })
    return JsonResponse(data,safe=False)


#DELETE REVIEW

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_review(request):
    item_id = request.POST.get('item_id')
    try:
        review=Review.objects.get(user=request.user, id=item_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found"})

    review.delete()
    return JsonResponse({"message": "Review deleted successfully"})

#DELETE RESTAURANT REVIEW


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_restauarnt_review(request):
    restauarant_id = request.POST.get('restauarant_id')
    try:
        review=RestaurantReview.objects.get(user=request.user, id=restauarant_id)
    except RestaurantReview.DoesNotExist:
        return JsonResponse({"error": "Review not found"})

    review.delete()
    return JsonResponse({"message": "Review deleted successfully"})

            