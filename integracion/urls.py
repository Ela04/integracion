from django.contrib import admin
from django.urls import path, re_path, include
from App import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/<int:producto_id>/', views.carrito, name='carrito'),
    path('productos/', views.productos, name='productos'),
    path('carrito/productos/', views.productos, name='productos'),
    path('webpay/commit/', views.webpay_commit, name='webpay_commit'),
    path('webpay/create/', views.webpay_create, name='webpay_create'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    

    #Admin
    path('admin/', admin.site.urls),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]
