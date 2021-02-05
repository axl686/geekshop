from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from geekshop import settings

import mainapp.views as mainapp


urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='ordersapp')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
   import debug_toolbar

   urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]