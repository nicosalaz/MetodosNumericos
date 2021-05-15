from django.shortcuts import render,redirect
import numpy as np
from scipy import linalg

#################################### VARIABLES GLOBALES ####################################

datos = []
result = ""
fil= 0
col = 0
#################################### HTML ####################################

def mostrar_formulario_inicial(request):
    return render(request,'Matrices/form_matrices.html')

def formulario_completo_matrices(request):
    global datos
    global result
    return render(request,'Matrices/form_completo.html',{'datos':datos,'result':result})

def resolver(request):
    global result
    valor = request.POST['calcular']
    escalar = request.POST['escalar']
    resta = request.POST['resta']
    suma = request.POST['suma']
    if valor == 'Guardar Matrices':
        guardar_matriz(request)
    elif valor == 'Borrar':
        limpiar_diccionario()
    elif valor == 'A+B':
        result = sumar(suma)
    elif valor == 'A-B':
        result = restar(resta)
    elif valor == 'escalar':
        result = multi_por_escalar(escalar)
    return redirect('mat')

def guardar_valores(m,name):
    global datos
    global fil
    global col
    mat = creadorDeMatrices(m)
    col,fil =  saberDeCuantoPorCuantoEs(mat)
    mat_final = rellenarLosEspacios(mat)
    datos.append([name,np.array(mat_final),fil,col])
    print(datos)

#################################### lOGICA ####################################
def creadorDeMatrices (valores) :
    aux = list()
    auxDos = ""
    matriz = []
    for i in range(len(valores)) :
        if valores[i] != "," and valores[i] !=" ":
            auxDos+= valores[i]
        if valores[i]== "," or i == len(valores)-1 or valores[i] == " ":
            aux.append(float(auxDos))
            auxDos = ""
        if valores[i] == " " or i == len(valores)-1:
            matriz.append(aux.copy())
            auxDos = ""
            aux.clear()


    return matriz

def saberDeCuantoPorCuantoEs (matriz):
    aux = 0
    filas = len(matriz)
    for i in range(0, len(matriz)):
        if aux < len(matriz[i]):
            aux = len(matriz[i])

    return aux,filas

def rellenarLosEspacios (matriz):
    numerosFaltan,filas = saberDeCuantoPorCuantoEs(matriz)
    for i in range(0, len(matriz)):
        if numerosFaltan > len(matriz[i]):
            matriz[i].append(0)
    return matriz

def limpiar_diccionario():
    global datos
    global result
    datos.clear()
    result=""
def guardar_matriz(request):
    name = request.POST['nombre']
    matriz = request.POST['matriz']
    guardar_valores(matriz,name)

def sumar(valor):
    if len(datos) > 1 and (len(valor)==0):
        result = datos[0][1]+datos[1][1]
        print(result)
        return str(datos[0][1])+' + '+str(datos[1][1])+' = '+str(result)
    elif len(valor) != 0:
        return sumar_por_prametro(valor)
    else:
        return 'No se puede realizar la operación'

def restar(valor):
    if len(datos) > 1 and (len(valor)==0):
        result = datos[0][1]-datos[1][1]
        print(result)
        return str(datos[0][1])+' - '+str(datos[1][1])+' = '+str(result)
    elif len(valor)!=0:
        return restar_por_prametro(valor)
    else:
        return 'No se puede realizar la operación'

def multi_por_escalar(escalar):
    mat = ""
    num = ""
    resultado = ""
    global datos
    for x in range(len(escalar)):
        if escalar[x].isnumeric():
            num = escalar[x]
        elif escalar[x] != '*':
            mat = escalar[x]
        else:
            pass
    for i in datos:
        if i[0] == mat:
            res = i[1]*float(num)
            return res

    return 'no se encontró ninguna matriz con ese identificador'

def determinante():
    pass

def restar_por_prametro(valor):
    identi=[]
    for x in valor:
        if x != '-':
           identi.append(x)
    resultado = determinar_matriz(identi[0]) - determinar_matriz(identi[1])
    return resultado

def sumar_por_prametro(valor):
    identi=[]
    for x in valor:
        if x != '+':
           identi.append(x)
    resultado = determinar_matriz(identi[0]) + determinar_matriz(identi[1])
    return resultado


def determinar_matriz(valor):
    global datos
    for x in datos:
        if x[0] == valor:
            return x[1]