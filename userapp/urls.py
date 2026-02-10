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
    # path("user_login",views.user_login,name="Login"),
    path("dashboard",views.buy_food,name="dashboard"),
    # path("add_to_cart",views.add_to_cart,name="add_to_cart"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("token_login",views.token_login,name="token_login"),
    path("add_to_cart",views.add_to_cart,name="add_to_cart"),
    path("add_to_wishlist",views.add_to_wishlist,name="add_to_wishlist"),
    path("add_review",views.add_review,name="add_review"),
    path("delete_review",views.delete_review,name="delete_review"),
    path("update_review",views.update_review,name="update_review"),


]