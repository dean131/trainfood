from django.urls import path

from . import views

urlpatterns = [
    path('product_list/', views.product_list_view),
    path('recomended_product_list/', views.recomended_product_view),

    path('update_item/', views.update_item_view),
    path('cart/', views.cart_view),
    path('order/', views.order_view),
    path('my_order/', views.my_order_view),
    path('my_order_history/', views.my_order_history_view),
]
