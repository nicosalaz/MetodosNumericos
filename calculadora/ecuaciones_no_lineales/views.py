from django.shortcuts import render


def mostar_form_biseccion(request):
    return render(request,'ENL/form_biseccion.html')

def resultado_biseccion(request):
    funcion = determinar_func(str(request.POST['funcion']))
    xi = request.POST['lim_inf']
    xf = request.POST['lim_sup']
    et = request.POST['error']
    result,er = metodo_biseccion(funcion,xi,xf,et)
    return render(request,'ENL/resultado_biseccion.html',{'resultado':result,'error_relativo':er})

def determinar_func(func):
    aux = ''
    for f in func:
        if f == '^':
            aux += '**'
        else:
            aux += f
    return aux

def metodo_biseccion(func,xi,xf,error=0.001,ite =100):
    f = lambda x :eval(str(func))
    ri = 0
    conta = 0
    error_calculado = 101
    if float(f(float(xi)))*float(f(float(xf))) <= 0:
        while conta <= ite and float(error_calculado) >= float(error):
            conta+=1
            ri = (float(xi)+float(xf))/2
            error_calculado = abs((float(ri)-float(xi))/float(ri))*100
            if float(f(float(xi))) * float(f(float(ri))) > 0:
                xi = ri
            else:
                xf = ri
        return '{:.3f}'.format(ri),'{:.2f}'.format(error_calculado)

    else:
        return False,False
