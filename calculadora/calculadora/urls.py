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
from django.urls import path
from calculadora_binaria.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mostrar_calculadora_decimal/', mostrar_calculadora_decimal,name='decimal'),
    path('resultado_decimal/', resultado_decimal),
    path('mostrar_calculadora_binaria/', mostrar_calculadora_binaria,name='binaria'),
    path('resultado_binario/', resultado_binario),
    path('mostrar_calculadora_hexadecimal/',mostrar_calculadora_hexadecimal, name='hexa_dec'),
    path('resultado_hexa_dec/', resultado_hexa_dec),
    path('mostrar_calculadora_octal',mostrar_calculadora_octal, name='octal_dec'),
    path('resultado_octa_dec/',resultado_octa_dec),

]
