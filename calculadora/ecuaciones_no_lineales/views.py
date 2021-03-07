import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from django.shortcuts import render



def mostar_form_biseccion(request):
    return render(request,'ENL/form_biseccion.html')

def mostar_form_falsa_pos(request):
    return render(request,'ENL/form_falsa_pos.html')

def mostar_form_derivada(request):
    return render(request,'ENL/Form_derivada.html')

def resultado_biseccion(request):
    funcion = str(request.POST['funcion'])
    xi = request.POST['lim_inf']
    xf = request.POST['lim_sup']
    et = request.POST['error']
    graficar_funcion(funcion,xi,xf)
    result,er = metodo_biseccion(funcion,xi,xf,et)
    return render(request,'ENL/resultado_biseccion.html',{'resultado':result,'error_relativo':er})

def resultado_falsa_pos(request):
    funcion = str(request.POST['funcion'])
    xi = request.POST['lim_inf']
    xf = request.POST['lim_sup']
    et = request.POST['error']
    graficar_funcion(funcion,xi,xf)
    result,er = metodo_falsa_posicion(funcion,xi,xf,et)
    return render(request,'ENL/resultado_biseccion.html',{'resultado':result,'error_relativo':er})

def determinar_func(func,valor):
    ecuacion = sp.sympify(func)
    simbolo = sp.symbols('x')
    result = ecuacion.evalf(subs={simbolo:float(valor)})
    return result

def metodo_biseccion(func,xi,xf,error=0.001,ite =50):
    ri = 0
    conta = 0
    error_calculado = 1
    if float(determinar_func(func,xi))*float(determinar_func(func,xf)) <= 0:
        while conta <= ite and float(error_calculado) >= float(error):
            print(float(determinar_func(func,xi))*float(determinar_func(func,xf)),conta)
            conta+=1
            ri = (float(xi)+float(xf))/2
            error_calculado = abs((float(ri)-float(xi))/float(ri))
            if float(determinar_func(func,xi)) * float(determinar_func(func,ri)) > 0:
                xi = ri
            else:
                xf = ri
        return '{:.5f}'.format(ri),'{:.5f}'.format(error_calculado)

    else:
        return False,False

def metodo_falsa_posicion(func,xi,xf,error=0.001,ite =50):
    ri = 0
    conta = 0
    error_calculado = 1
    if float(determinar_func(func,xi))*float(determinar_func(func,xf)) <= 0:
        while conta < ite and float(error_calculado) > float(error):
            conta+=1
            ri = float((float(xf))-((float(determinar_func(func,xf))*(float(xf)-float(xi)))/(float(determinar_func(func,xf))-float(determinar_func(func,xi)))))
            error_calculado = abs((float(ri) - float(xi)) / float(ri))
            if float(determinar_func(func,xi)) * float(determinar_func(func,ri)) > 0:
                xi = ri
            else:
                xf = ri
        return '{:.5f}'.format(ri), '{:.5f}'.format(error_calculado)

    else:
        return False, False

def graficar_funcion(func,xi,xf):
    ecu = sp.sympify(func)
    inf = int(xi)
    sup = int(xf)
    sim = sp.symbols('x')
    sp.plot(ecu,(sim,inf,sup))

def resultado_dev(request):
    funcion = request.POST['funcion']
    x = sp.symbols('x')
    numero = request.POST['num']
    p_d = sp.diff(funcion, x)
    s_d = sp.diff(funcion, x,2)
    r_pd = int(sp.diff(funcion, x).evalf(subs={x: numero}))
    r_sd = int(sp.diff(funcion, x,2).evalf(subs={x: numero}))
    print("Primera derivada ", sp.diff(funcion, x, 1))
    print("Segunda derivada ", sp.diff(funcion, x, 2))
    print("Resultado primera derivada ", sp.diff(funcion, x, 1).evalf(subs={x: numero}))
    print("Resultado segunda derivada ", sp.diff(funcion, x, 2).evalf(subs={x: numero}))

    return render(request,'ENL/resultado_dev.html',{'p_d':p_d,'s_d':s_d,'r_pd':r_pd,'r_sd':r_sd,})