from django.shortcuts import render
import sympy as sp
import numpy as np
import math
import random
from scipy import integrate

################################## variables globlales ##################################
datos=[]

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

def mostrar_form_integrales_montecarlo(request):
    return render(request, 'integrales/form_integrales_montecarlo.html')


################################## RESULTADOS ##################################

def resultado_integrales_rectangulos(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    a_2 = evaluar_entrada(a)
    b_2 = evaluar_entrada(b)
    graficar_funcion(func,a_2, b_2)
    izq = intregales_rectangulos_izq(func, a_2, b_2, n)
    der = intregales_rectangulos_der(func, a_2, b_2, n)
    med = intregales_rectangulos_med(func, a_2, b_2, n)
    return render(request, 'integrales/resultado_integrales_rectangulos.html'
                  , {'izq': izq, 'der': der, 'med': med, 'func': func,
                     'a':int(a_2),'b':int(b_2)})


def resultado_integrales_trapecios(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    a_2 = evaluar_entrada(a)
    b_2 = evaluar_entrada(b)
    graficar_funcion(func, a_2, b_2)
    calculo,error = integrales_trapecios(func, a_2, b_2, n)
    return render(request, 'integrales/resultado_integrales_trapecios.html', {'calculo': calculo, 'func': func,
                                                                            'a':int(a_2),'b':int(b_2),'error':error})


def resultado_integrales_simpson_1_3(request):
    global datos
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    a_2 =  evaluar_entrada(a)
    b_2 = evaluar_entrada(b)
    guardar_valores([a_2,b_2])
    graficar_funcion(func, a_2, b_2)
    calculo, error = integralSimpson_1_3(func, a_2, b_2, n)
    return render(request, 'integrales/resultado_integrales_simpson_1_3.html',
                  {'calculo': calculo, 'func': func, 'error': error,'a':int(a_2),'b':int(b_2)})


def resultado_integrales_simpson_3_8(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    a_2 =  evaluar_entrada(a)
    b_2 = evaluar_entrada(b)
    graficar_funcion(func, a_2, b_2)
    calculo, error = integralSimpson_3_8(func, a_2, b_2, n)
    return render(request, 'integrales/resultado_integrales_simpson_3_8.html',
                  {'calculo': calculo, 'func': func, 'error': error,'a':int(a_2),'b':int(b_2)})

def resultado_integrales_montecarlo(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    a_2 =  evaluar_entrada(a)
    b_2 = evaluar_entrada(b)
    graficar_funcion(func, a_2, b_2)
    result = metodo_motecarlo(func,a_2,b_2,n)
    return render(request,'integrales/resultado_integrales_montecarlo.html',{'result':result,'func':func
                                                                        ,'a_2':a_2,'b_2':b_2})

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
        xn.append(float(aux))
        aux += deltaX
    # print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion, x)
    # print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    # print('resultado: ','{:.5f}'.format(result))
    return '{:.8f}'.format(result)


def intregales_rectangulos_der(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a) + deltaX
    result = 0
    for i in range(int(n)):
        xn.append(float(aux))
        aux += deltaX
    # print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion, x)
    # print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    # print('resultado: ','{:.5f}'.format(result))
    return '{:.8f}'.format(result)


def intregales_rectangulos_med(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a)
    result = 0
    for i in range(int(n)+1):
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
    return '{:.8f}'.format(result)

def integrales_trapecios(funcion, a, b, n):
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a)
    result = 0
    imagen_a = determinar_func(funcion, a)
    imagen_b = determinar_func(funcion, b)
    randomico = random.uniform(0, 1)
    epsilon = float(a) + randomico * (float(b) - float(a))
    derivada = calcular_derivada(funcion,float(epsilon),2)
    error = -((deltaX**3)/12)*derivada

    for i in range(int(n)):
        xn.append(float(aux))
        aux += deltaX
    #print('xn: ',xn)
    for x in range(1,len(xn)):
        result += determinar_func(funcion,xn[x])*2
    result  += (float(determinar_func(funcion,a))+float(determinar_func(funcion,b)))
    result *= (deltaX/2)
    #     # print(determinar_func(funcion, x))
    # # print('resultado: ', '{:.5f}'.format(result))
    resultado_final =result
    # # print('resultado: ','{:.5f}'.format(resultado_final))

    return '{:.8f}'.format(resultado_final),error

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

def integral_3_8(funcion, a, b):
    m1 = (2 * float(a) + float(b)) / 3
    m2 = (float(a) + 2 * float(b)) / 3
    resultado = (float(b) - float(a)) / 8 * (determinar_func(funcion, float(a)) + (3 * determinar_func(funcion, m1)) + (
            3 * determinar_func(funcion, m2)) + determinar_func(funcion, float(b)))

    return resultado


def integralSimpson_3_8(funcion, a, b, n):
    aux = int(n)
    if (aux % 3 == 1):
        aux += 2
    elif (aux % 3 == 2):
        aux += 1

    valorA = float(a)
    valorB = float(b)
    valorN = aux
    randomico = random.uniform(0, 1)
    epsilon = valorA + randomico * (valorB - valorA)

    delta = (valorB - valorA) / valorN
    resultado = 0

    for i in range(valorN):
        valorB = valorA + delta
        area = integral_3_8(funcion, valorA, valorB)
        resultado = resultado + area
        valorA = valorB

    derivada4 = calcular_derivada(funcion, float(epsilon), 4)

    error = -((3 / 80) * (delta ** 5)) * derivada4

    return resultado, error

def metodo_motecarlo(funcion,a,b,n):
    inf = float(a)
    sup = float(b)
    N = int(n)
    integral = 0.0
    xrand = np.zeros(N)
    for i in range(len(xrand)):
        xrand[i] = random.uniform(inf, sup)
    for i in range(N):
        integral += determinar_func(funcion,xrand[i])
    answer = (sup - inf) / float(N) * integral
    return answer


def graficar_funcion(func, xi=-10, xf=10):
    ecu = sp.sympify(func)
    inf = int(xi)
    sup = int(xf)
    x = sp.symbols('x')
    sp.plot(ecu, (x, inf, sup))

def evaluar_entrada(numero):
    valor = numero
    if numero == 'pi':
        valor = math.pi
    elif numero == 'inf':
        valor = float(math.inf)

    return float(valor)

def guardar_valores(numeros):
    global datos
    for x in numeros:
        datos.append(x)
    print(datos)
