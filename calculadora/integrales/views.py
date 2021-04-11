from django.shortcuts import render
import sympy as sp
import math


# Create your views here.
################################## HTML ##################################
def mostrar_form_integrales_rectangulo(request):
    return render(request, 'integrales/form_integrales_rectangulos.html')


def mostrar_form_integrales_trapecio(request):
    return render(request, 'integrales/form_integrales_trapecio.html')


def mostrar_form_integrales_simpson_1_3(request):
    return render(request, 'integrales/form_integrales_simpson_1_3.html')


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
                  , {'izq': izq, 'der': der, 'med': med, 'func': func})


def resultado_integrales_trapecios(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    graficar_funcion(func, a, b)
    calculo = integrales_trapecios(func, a, b, n)
    return render(request, 'integrales/resultado_integrales_trapecios.html', {'calculo': calculo, 'func': func})


def resultado_integrales_simpson_1_3(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    graficar_funcion(func, a, b)
    calculo = integralSimpson_1_3(func, a, b, n)
    return render(request, 'integrales/resultado_integrales_simpson_1_3.html', {'calculo': calculo, 'func': func})


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
    aux = (float(a) + (float(a) + deltaX)) / 2
    result = 0
    for i in range(int(n)):
        if aux > float(b):
            break
        xn.append(float(aux))
        aux = (aux + (aux + deltaX)) / 2
    # print('delta: ',deltaX)
    # print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion, x)
    # print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    # print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)


def integrales_trapecios(funcion, a, b, n):
    imagen_a = 0
    imagen_b = 0
    deltaX = (float(b) - float(a)) / float(n)
    xn = []
    aux = float(a)
    result = 0

    imagen_a = determinar_func(funcion, a)
    imagen_b = determinar_func(funcion, b)

    for i in range(int(n)):
        if aux >= float(b):
            break
        xn.append(float(aux))
        aux += deltaX
    # print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion, x)
    # print('resultado: ', '{:.5f}'.format(result))

    # print('resultado: ','{:.5f}'.format(result))
    result *= 2
    result += imagen_a + imagen_b
    result *= (deltaX / 2)
    return '{:.5f}'.format(result)


def integralSimpson_1_3(funcion, a, b, n):
    valorA = float(a)
    valorB = float(b)
    valorN = int(n)
    sumatoria = 0
    delta = ((valorB - valorA) / valorN)

    for i in range(valorN + 1):
        xi = (valorA + (i * delta))
        valor = math.e ** (xi ** 2)
        if xi == valorA or xi == valorB:
            # sumatoria += determinar_func(funcion, i)
            sumatoria += valor
        elif i % 2 != 0:
            # ecu = 4 * determinar_func(funcion, i)
            # sumatoria += determinar_func(funcion, i)
            valor = 4 * valor
            sumatoria += valor
        elif i % 2 == 0:
            # ecu = 2 * determinar_func(funcion, i)
            # sumatoria += determinar_func(funcion, i)
            valor = 2 * valor
            sumatoria += valor

    resultado = (delta / 3) * sumatoria

    return resultado


def graficar_funcion(func, xi=-10, xf=10):
    ecu = sp.sympify(func)
    inf = int(xi)
    sup = int(xf)
    x = sp.symbols('x')
    sp.plot(ecu, (x, inf, sup))
