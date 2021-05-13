from django.shortcuts import render,redirect

def mostrar_formulario_inicial(request):
    return render(request,'Matrices/form_matrices.html')

def formulario_completo_matrices(request):
    n = request.POST['n_matrices']
    arreglo = []
    for x in range(int(n)):
        arreglo.append(x+1)
    return render(request,'Matrices/form_completo.html',{'arr':arreglo})

def resolver(request):
    valor = request.POST['calcular']
    print(valor)
    return redirect('mat_ini')