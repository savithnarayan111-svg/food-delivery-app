from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from userapp import views    


urlpatterns=[
    path("signup/",views.Signup,name="signup"),
    # path("Add_to_cart/<int:id>",views.Add_to_cart,name="Add_to_cart")
    path("user_signup",views.user_signup,name="user_signup"),
    # path("User_login",views.User_login,name="User_login"),
    path("user_login",views.user_login,name="Login"),
    path("dashboard",views.buy_food,name="dashboard"),
    # path("add_to_cart",views.add_to_cart,name="add_to_cart"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("token_login",views.token_login,name="token_login"),
    
    #CART

    path("add_to_cart",views.add_to_cart,name="add_to_cart"),
    path("view_cart",views.view_cart,name="view_cart"),
    path("delete_cart",views.delete_cart,name="delete_cart"),
    path("remove_cart",views.remove_cart,name="remove_cart"),
    path("update_quantity",views.update_quantity,name="update_quantity"),
    path("wishlist_to_cart",views.wishlist_to_cart,name="wishlist_to_cart"),


    

    #WISHLIST

    path("add_to_wishlist",views.add_to_wishlist,name="add_to_wishlist"),
    path("view_wishlist",views.view_wishlist,name="view_wishlist"),
    path("delete_wishlist",views.delete_wishlist,name="delete_wishlist"),
    
    #REVIEW

    path("add_review",views.add_review,name="add_review"),
    path("delete_review",views.delete_review,name="delete_review"),
    path("update_review",views.update_review,name="update_review"),
    path("view_review/<int:id>",views.view_review,name="view_review"),
    path("add_restaurant_review",views.add_restaurant_review,name="add_restaurant_review"),
    path("view_restaurant_review/<int:id>",views.view_restaurant_review,name="view_restaurant_review"),


    

    #PROFILE

    path("view_profile",views.view_profile,name="view_profile"),
    path("update_profile",views.update_profile,name="update_profile"),
    path("search_restaurants",views.search_restaurants,name="search_restaurants"),

    path("search_product",views.search_product,name="search_product"),
    path("filtering_Price/",views.filtering_Price,name="filtering_Price"),

#SORT RESTAURANT

    path("sort_restaurant",views.sort_restaurant,name="sort_restaurant"),
    path("average_rest_rating/<int:id>",views.average_rest_rating,name="average_rest_rating"),

    

]
