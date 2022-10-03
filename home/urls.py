from django.urls import path # allows us make use of the path in urlpatterns so as to input the views
from . import views # connects the views to the urls





urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('detail/<str:id>/<slug:slug>', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.pay, name='pay'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    # path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('error_page/', views.error_page, name='error_page'),
    path('callback/', views.callback, name='callback'),
]