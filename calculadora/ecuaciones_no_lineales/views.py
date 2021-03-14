import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from django.shortcuts import render,redirect

################################################## HTML ##################################################

def mostar_form_biseccion(request):
    return render(request,'ENL/form_biseccion.html')

def mostar_form_falsa_pos(request):
    return render(request,'ENL/form_falsa_pos.html')

def mostar_form_derivada(request):
    return render(request,'ENL/Form_derivada.html')

def mostar_form_secante(request):
    return render(request,'ENL/form_secante.html')

def mostar_form_n_r(request):
    return render(request,'ENL/form_newton_raphson.html')

def mostar_form_r_polinomios(request):
    return render(request,'ENL/form_r_polinomios.html')

def mostar_form_graficador(request):
    return render(request,'ENL/form_graficador.html')

################################################## RESULTADOS ##################################################

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

def resultado_n_r(request):
    func = request.POST['funcion']
    numero = request.POST['pun_ini']
    error_tol = request.POST['error']
    graficar_funcion(func,0,numero)
    result,error = metodo_newton_raphson(func,numero,error_tol)

    return render(request,'ENL/resultado_n_r.html',{'raiz':result,'error':error})

def resultado_secante(request):
    funcion = request.POST['funcion']
    xi = request.POST['lim_inf']
    xf = request.POST['lim_sup']
    error_tol = request.POST['error']
    graficar_funcion(funcion,xi,xf)
    result,error = metodo_secante(funcion,xi,xf,error_tol)

    return render(request,'ENL/resultado_secante.html',{'raiz':result,'error':error})

def resultado_dev(request):
    funcion = request.POST['funcion']
    x = sp.symbols('x')
    numero = request.POST['num']
    p_d = sp.diff(funcion, x)
    s_d = sp.diff(funcion, x,2)
    r_pd = float(sp.diff(funcion, x).evalf(subs={x: numero}))
    r_sd = float(sp.diff(funcion, x,2).evalf(subs={x: numero}))
    # print("Primera derivada ", sp.diff(funcion, x, 1))
    # print("Segunda derivada ", sp.diff(funcion, x, 2))
    # print("Resultado primera derivada ", sp.diff(funcion, x, 1).evalf(subs={x: numero}))
    # print("Resultado segunda derivada ", sp.diff(funcion, x, 2).evalf(subs={x: numero}))

    return render(request,'ENL/resultado_dev.html',{'p_d':p_d,'s_d':s_d,'r_pd':r_pd,'r_sd':r_sd,})

def resultado_r_polinomios(request):
    func = request.POST['funcion']
    graficar_funcion(func)
    list_r,list_im = organizarRaices(raicesdepolinomios(func))
    return render(request,'ENL/resultado_r_polinomios.html',{'reales':list_r,'imaginarios':list_im})

def resultado_graficador(request):
    func = request.POST['funcion']
    graficar_funcion(func)
    return redirect('graficador')


################################################## LOGICA ##################################################

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
        return '{:.5f}'.format(ri),'{:.8f}'.format(error_calculado)

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
        return '{:.5f}'.format(ri), '{:.8f}'.format(error_calculado)

    else:
        return False, False

def metodo_newton_raphson(func,p_inical,error_tolerancia=0.0001):
    xi = p_inical
    xr = 0
    er = 100
    i = 0
    ite = []
    while er > float(error_tolerancia) and i <= 50:
        #print('i:',i)
        if float(calcular_derivada(func,xi)) == 0:
            return False,False
        xr = float(xi) - (float(determinar_func(func,xi))/float(calcular_derivada(func,xi)))
        #print('xr:',xr)
        er = abs(((float(xi) - float(xr))/float(xr)))
        #print('er:', er)
        xi = float(xr)
        i += 1
        ite.append((i,xr,er))

    return '{:.5f}'.format(xr),'{:.8f}'.format(er)

def metodo_secante(func,xi,xf,error_tol):
    funcion = str(func)
    x0 = float(xi)
    x1 = float(xf)
    tolerancia = float(error_tol)
    raiz = 0
    i = 0
    error = 1
    while float(error) > float(tolerancia) and i <= 50:
        raiz = float(float(x1) * float(determinar_func(funcion, x0)) - float(x0) *float(determinar_func(funcion, x1))) / (
            float(determinar_func(funcion, x0)) - float(determinar_func(funcion, x1)))
        error = abs((float(x1) - float(raiz)) / float(raiz))
        x0 = float(x1)
        x1 = float(raiz)
        i = i + 1

    return '{:.5f}'.format(raiz), '{:.10f}'.format(error)


def graficar_funcion(func):
    ecu = sp.sympify(func)
    inf = float(-10)
    sup = float(10)
    sim = sp.symbols('x')
    sp.plot(ecu,(sim,inf,sup))


def calcular_derivada(func,valor):
    funcion = sp.sympify(func)
    x = sp.symbols('x')
    numero = valor
    p_d = sp.diff(funcion, x)
    r_pd = float(sp.diff(funcion, x).evalf(subs={x: numero}))

    return r_pd

def sacarValoresDeFuncion(funcion):
    i=0
    aux=""
    lista= list()
    fin=len(funcion)-1
    while i<len(funcion):
        if funcion[i]=="+":
            lista.append(aux)
            aux=""
        if funcion[i]=="-" and i != 0:
            lista.append(aux)
            aux=""
        if i== fin:
            aux += funcion[fin]
            lista.append(aux)
            aux=""
        else:
                aux+=funcion[i]
        i+=1

    return lista

def sacarMayorCofeciente(lista):
    i=0
    aux=""
    listaDenumeroGrados= list()
    caracter ="^"
    guardarMenos=""
    while i<len(lista):
        for k in range(0,len(lista[i])):
            if caracter not in lista[i]:
                if lista[i][k] =="-":
                    guardarMenos = lista[i][k]
                if lista[i][k].isdigit() == True or lista[i][k] ==".":
                    aux+=lista[i][k]
                if lista[i][k] == "x":
                    if aux =="":
                        aux+="1"
                    if guardarMenos !="":
                        listaDenumeroGrados.append([float(1),-float(aux)])

                    else:
                        listaDenumeroGrados.append([float(1),float(aux)])
                    guardarMenos = ""
                    aux=""
                if k == len(lista[i])-1 and lista[i][len(lista[i])-1] != "x":
                    if guardarMenos != "":
                        listaDenumeroGrados.append([float(0),-float(aux)])
                    else:
                        listaDenumeroGrados.append([float(0),float(aux)])
                    aux=""
                    guardarMenos = ""

            if caracter in lista[i]:
                if lista[i][k] =="-":
                    guardarMenos = lista[i][k]
                if k == len(lista[i])-1:
                    if aux == "":
                        aux+="1"
                    auxDos=lista[i][len(lista[i])-1]
                    if guardarMenos !="":
                        listaDenumeroGrados.append([float(auxDos),-float(aux)])
                    else:
                        listaDenumeroGrados.append([float(auxDos),float(aux)])
                    aux=""
                    guardarMenos=""
                if (lista[i][k].isdigit() == True or  lista[i][k] =="." )and k != len(lista[i])-1 :
                    aux+=lista[i][k]
        i+=1
    return listaDenumeroGrados

def organizarLista(lista):
    retono=sorted(lista)

    return retono

def raicesdepolinomios(funcion):
    polinomio=organizarLista(sacarMayorCofeciente(sacarValoresDeFuncion(funcion)))
    polinomio.reverse()
    raicesAsacar=list()
    raicesDeUnpolinomio=list()
    for i in range(0,len(polinomio)):
        raicesAsacar.append(polinomio[i][1])
    raicesDeUnpolinomio= np.roots(raicesAsacar)

    return raicesDeUnpolinomio

def organizarRaices(lista):
    strj=""
    listaReales=list()
    listaImag=list()
    for i in lista:
        strj=str(i)
        if "j" in strj:
            listaImag.append(strj.replace('j','i'))
        else:
            listaReales.append(strj)
    return listaReales,listaImag


