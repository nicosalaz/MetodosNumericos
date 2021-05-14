from django.shortcuts import render,redirect
import numpy as np
from scipy import linalg

datos = {}
fil= 0
col = 0
num_mat = 0

def mostrar_formulario_inicial(request):
    return render(request,'Matrices/form_matrices.html')

def formulario_completo_matrices(request):
    global num_mat
    n = request.POST['n_matrices']
    num_mat = int(n)
    arreglo = []
    for x in range(int(n)):
        arreglo.append(x+1)
    return render(request,'Matrices/form_completo.html',{'arr':arreglo})

def resolver(request):
    valor = request.POST['calcular']
    if valor == 'Calcular':
        for x in range(num_mat):
            nom_mat = request.POST['nom_mat'+str((x+1))]
            matriz = request.POST['mat'+str((x+1))]
            guardar_valores(matriz,nom_mat)
    elif valor == 'Borrar':
        limpiar_diccionario()
    return redirect('mat_ini')

def guardar_valores(m,nombre):
    global datos
    global fil
    global col
    mat = creadorDeMatrices(m)
    col,fil =  saberDeCuantoPorCuantoEs(mat)
    mat_final = rellenarLosEspacios(mat)
    datos[nombre] = np.array(mat_final)
    print(datos)

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
    datos.clear()
    print(datos)