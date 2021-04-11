from django.shortcuts import render
import sympy as sp

# Create your views here.
################################## HTML ##################################
def mostrar_form_integrales_rectangulo(request):
    return render(request,'integrales/form_integrales_rectangulos.html')


################################## RESULTADOS ##################################

def resultado_integrales_rectangulos(request):
    func = request.POST['funcion']
    a = request.POST['ext_izq']
    b = request.POST['ext_der']
    n = request.POST['n']
    izq = intregales_rectangulos_izq(func,a,b,n)
    der = intregales_rectangulos_der(func,a,b,n)
    med = intregales_rectangulos_med(func,a,b,n)
    return render(request,'integrales/resultado_integrales_rectangulos.html',{'izq':izq,'der':der,'med':med})

################################## lOGICA ##################################

def determinar_func(func,valor):
    ecuacion = sp.sympify(func)
    simbolo = sp.symbols('x')
    result = ecuacion.evalf(subs={simbolo:float(valor)})
    return result

def intregales_rectangulos_izq(funcion,a,b,n):
    deltaX = (float(b)-float(a))/float(n)
    xn=[]
    aux = float(a)
    result = 0
    for i in range(int(n)):
        if aux >= float(b):
            break
        xn.append(float(aux))
        aux+=deltaX
    #print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion,x)
    #print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    #print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)

def intregales_rectangulos_der(funcion,a,b,n):
    deltaX = (float(b)-float(a))/float(n)
    xn=[]
    aux = float(a)+deltaX
    result = 0
    for i in range(int(n)):
        if aux > float(b):
            break
        xn.append(float(aux))
        aux+=deltaX
    #print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion,x)
    #print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    #print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)

def intregales_rectangulos_med(funcion,a,b,n):
    deltaX = (float(b)-float(a))/float(n)
    xn=[]
    aux = (float(a)+(float(a)+deltaX))/2
    result = 0
    for i in range(int(n)):
        if aux > float(b):
            break
        xn.append(float(aux))
        aux= (aux+(aux+deltaX))/2
    #print('delta: ',deltaX)
    print('xn: ',xn)
    for x in xn:
        result += determinar_func(funcion,x)
    #print('resultado: ', '{:.5f}'.format(result))
    result *= deltaX
    #print('resultado: ','{:.5f}'.format(result))
    return '{:.5f}'.format(result)