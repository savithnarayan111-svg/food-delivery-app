from django.urls import path

from adminapp import views

urlpatterns=[

    #RESTAURANT


    path("add_restaurant",views.Add_Restaurant,name="add_restaurant"),
    path("view_restaurant",views.View_restaurants,name="view_restaurant"),
    path("view_single_restaurant/<int:id>",views.view_single_restaurant,name="view_single_restaurant"),
    path("View_Single_restaurant/<int:id>",views.View_Single_restaurant,name="View_Single_restaurant"),
    path("Remove_restaurant/<int:id>",views.Remove_restaurant,name="Remove_restaurant"),
    path("update_restaurant/<int:id>",views.update_restaurant,name="update_restaurant"),
    path("view_users",views.view_users,name="view_users"),


    #PRODUCT

    path("Add_Product/<int:id>",views.Add_Product,name="Add_Product"),
    path("view_product",views.view_product,name="view_product"),
    path("remove_product/<int:id>",views.remove_product,name="remove_product"),
    path("view_single_product/<int:id>",views.view_single_product,name="view_single_product"),
    path("update_product/<int:id>",views.update_product,name="update_product"),

    #COUPON

    path("add_coupon",views.Add_coupon,name="Add_coupon"),
    path("view_coupon",views.View_coupon,name="View_coupon"),
    path("coupon_delete/<int:id>",views.Coupon_delete,name="Coupon_delete"),
    path("update_coupon/<int:id>",views.Update_coupon,name="Update_coupon"),

    #REVIEW

    path("view_review",views.view_review,name="view_review"),
    path("filtering_rating",views.filtering_rating,name="filtering_rating"),
    path("delete_product_review",views.delete_product_review,name="delete_product_review"),
    path("delete_restauarnt_review",views.delete_restauarnt_review,name="delete_restauarnt_review"),




    

]