from django.shortcuts import render
import sympy as sp
import math
import random
from scipy import integrate


# Create your views here.
################################## HTML ##################################
def mostrar_form_integrales_rectangulo(request):
    return render(request, 'integrales/form_integrales_rectangulos.html')


def mostrar_form_integrales_trapecio(request):
    return render(request, 'integrales/form_integrales_trapecio.html')


def mostrar_form_integrales_simpson_1_3(request):
    return render(request, 'integrales/form_integrales_simpson_1_3.html')


def mostrar_form_integrales_simpson_3_8(request):
    return render(request, 'integrales/form_integrales_simpson_3_8.html')


################################## RESULTADOS ##################################

def resultado_integrales_rectangulos(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    graficar_funcion(func, a, b)
    izq = intregales_rectangulos_izq(func, a, b, n)
    der = intregales_rectangulos_der(func, a, b, n)
    med = intregales_rectangulos_med(func, a, b, n)
    return render(request, 'integrales/resultado_integrales_rectangulos.html'
                  , {'izq': izq, 'der': der, 'med': med, 'func': func,
                     'a':a,'b':b})


def resultado_integrales_trapecios(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    graficar_funcion(func, a, b)
    calculo,error = integrales_trapecios(func, a, b, n)
    return render(request, 'integrales/resultado_integrales_trapecios.html', {'calculo': calculo, 'func': func,
                                                                              'a':a,'b':b,'error':error})


def resultado_integrales_simpson_1_3(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    graficar_funcion(func, a, b)
    calculo, error = integralSimpson_1_3(func, a, b, n)
    return render(request, 'integrales/resultado_integrales_simpson_1_3.html',
                  {'calculo': calculo, 'func': func, 'error': error,'a':a,'b':b})


def resultado_integrales_simpson_3_8(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    graficar_funcion(func, a, b)
    calculo, error = integralSimpson_3_8(func, a, b, n)
    return render(request, 'integrales/resultado_integrales_simpson_3_8.html',
                  {'calculo': calculo, 'func': func, 'error': error,'a':a,'b':b})


################################## lOGICA ##################################

def determinar_func(func, valor):
    ecuacion = sp.sympify(func)
    simbolo = sp.symbols('x')
    result = ecuacion.evalf(subs={simbolo: float(valor)})
    return result


def intregales_rectangulos_izq(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a)
    result = 0
    for i in range(int(n)):
        if aux >= float(b):
            break
        xn.append(float(aux))
        aux += deltaX
    # print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion, x)
    # print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    # print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)


def intregales_rectangulos_der(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a) + deltaX
    result = 0
    for i in range(int(n)):
        if aux > float(b):
            break
        xn.append(float(aux))
        aux += deltaX
    # print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion, x)
    # print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    # print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)


def intregales_rectangulos_med(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a)
    result = 0
    for i in range(int(n)+1):
        if aux > float(b):
            break
        xn.append(float(aux))
        aux = aux + deltaX
    #print('delta: ',deltaX)
    #print('xn: ',xn)
    for x in range(0,len(xn)-1):
        media = (float(xn[x]) + float(xn[x+1]))/2
        result += determinar_func(funcion, media)
    # print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    # print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)


def integrales_trapecios(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a)
    result = 0
    imagen_a = determinar_func(funcion, a)
    imagen_b = determinar_func(funcion, b)
    randomico = random.uniform(0, 1)
    epsilon = float(a) + randomico * (float(b) - float(b))
    derivada = calcular_derivada(funcion,float(epsilon),2)
    error = -((deltaX**3)/12)*derivada

    for i in range(int(n)):
        xn.append(float(aux))
        aux += deltaX
    #print('xn: ',xn)
    for x in range(1,len(xn)):
        result += determinar_func(funcion,xn[x])*2
    result+= (float(determinar_func(funcion,a))+float(determinar_func(funcion,b)))
    result *= (deltaX/2)
    #     # print(determinar_func(funcion, x))
    # # print('resultado: ', '{:.5f}'.format(result))
    resultado_final =result
    # # print('resultado: ','{:.5f}'.format(resultado_final))

    return '{:.5f}'.format(resultado_final),error

def calcular_derivada(func, valor,num_int):
    funcion = sp.sympify(func)
    x = sp.symbols('x')
    numero = valor
    r_pd = float(sp.diff(funcion, x, num_int).evalf(subs={x: numero}))

    return r_pd


def integralSimpson_1_3(funcion, a, b, n):
    aux = int(n)
    if (aux % 2 != 0):
        aux += 1
    valorA = float(a)
    valorB = float(b)
    valorN = aux
    sumatoria = 0
    randomico = random.uniform(0, 1)
    epsilon = float(a)+randomico*(float(b)-float(a))
    delta = ((valorB - valorA) / valorN)

    for i in range(valorN + 1):
        xi = (valorA + (i * delta))
        valor = determinar_func(funcion, xi)
        if xi == valorA or xi == valorB:
            sumatoria += valor
        elif i % 2 != 0:
            valor = 4 * valor
            sumatoria += valor
        elif i % 2 == 0:
            valor = 2 * valor
            sumatoria += valor

    resultado = (delta / 3) * sumatoria

    derivada4 = calcular_derivada(funcion, float(epsilon),4)

    error = -(((delta ** 5) / 90) * derivada4)

    return resultado, error


def integralSimpson_3_8(funcion, a, b, n):
    aux = int(n)
    if (aux % 3 == 1):
        aux += 2
    elif (aux % 3 == 2):
        aux += 1
    valorA = float(a)
    valorB = float(b)
    randomico = random.uniform(0, 1)
    epsilon =  float(a)+randomico*(float(b)-float(a))
    delta = ((valorB - valorA) / 3)
    resultado = 0


    x0 = valorA
    x1 = x0 + delta
    x2 = x1 + delta
    x3 = x2 + delta

    fx0 = determinar_func(funcion, x0)
    fx1 = determinar_func(funcion, x1)
    fx2 = determinar_func(funcion, x2)
    fx3 = determinar_func(funcion, x3)

    derivada4 = calcular_derivada(funcion, float(epsilon),4)

    error = -((3 / 80) * (delta ** 5)) * derivada4

    resultado = ((3 * delta) / 8) * (fx0 + (3 * fx1) + (3 * fx2) + fx3)

    return resultado, error

def graficar_funcion(func, xi=-10, xf=10):
    ecu = sp.sympify(func)
    inf = int(xi)
    sup = int(xf)
    x = sp.symbols('x')
    sp.plot(ecu, (x, inf, sup))
