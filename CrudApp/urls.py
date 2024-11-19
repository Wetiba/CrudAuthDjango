from  django.urls import path


from . import views as user_views
from django.contrib.auth import views as auth_views





urlpatterns=[
    path('', user_views.index, name='home-page'),
    path('add-product/', user_views.add_product, name='add-product-page'),
    path('products/', user_views.products, name='all-products'),
    path('delete-product/<id>', user_views.delete_product, name='del-pr'),
    path('update-product/<id>', user_views.update_product, name='upd-product'),
    path('register/', user_views.register, name='user-registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='user-logout'),
    path('shop/', user_views.shop, name='shop'),
    path('pay/<id>', user_views.pay, name='pay')
]