"""calculadora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.convertidor.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('convertidor/', include(('apps.convertidor.urls','convertidor'))),

    path('decimal_binario32/', decimal_binario32, name = 'decimal_binario32'),
    path('binario_decimal32/', binario_decimal32, name = 'binario_decimal32'),

    path('resultadoDB32/', decimalBinario32, name= 'resultadoDB32'),
    path('resultadoBD32/', binarioDecimal32, name= 'resultadoBD32'),

    path('decimal_binario64/', decimal_binario64, name = 'decimal_binario64'),
    path('binario_decimal64/', binario_decimal64, name = 'binario_decimal64'),

    path('resultadoDB64/', decimalBinario64, name='resultadoDB64'),
    path('resultadoBD64/', binarioDecimal64, name='resultadoBD64')
]
