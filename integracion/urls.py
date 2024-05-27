from django.contrib import admin
from django.urls import path, re_path
from App import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('carrito/carrito/', views.carrito, name='carrito'),
    path('carrito/productos/', views.productos, name='productos'),
    path('webpay/commit/', views.webpay_commit, name='webpay_commit'),
    path('webpay/create/', views.webpay_create, name='webpay_create'),

    #Admin
    path('admin/', admin.site.urls)
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]
