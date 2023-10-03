from django.urls import path
from storeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('contact',views.contact),
    path('delete/<rid>',views.delete),
    path('edit/<rid>',views.edit),
    path('hello',views.greet),
    path('addproduct',views.addproduct),
    path('index',views.index),
    path('details/<id>',views.detail),
    path('catfilter/<cv>',views.catfilter),
    path('pricerange',views.pricerange),
    path('sort/<sv>',views.sort),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('addcart/<rid>',views.addcart),
    path('cart',views.viewcart),
    path('remove/<rid>',views.removecart),
    path('qty/<sig>/<pid>',views.cartqty),
    path('placeorder',views.place_order),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendmail),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)