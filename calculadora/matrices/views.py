from django.shortcuts import render, redirect
import numpy as np
from scipy import linalg

#################################### VARIABLES GLOBALES ####################################

datos = []
result = ""
fil = 0
col = 0


#################################### HTML ####################################

def mostrar_formulario_ecu_lineal(request):
    return render(request, 'Matrices/form_matrices.html')


def formulario_completo_matrices(request):
    global datos
    global result
    return render(request, 'Matrices/form_completo.html', {'datos': datos, 'result': result})


def resolver(request):
    global result
    boton = request.POST['calcular']
    operacion = request.POST['operacion']
    if boton == 'Guardar Matrices':
        guardar_matriz(request)
    elif boton == 'Borrar':
        limpiar_diccionario()
    elif boton == 'calculo':
        if '+' in operacion:
            result = sumar(operacion)
        elif '-' in operacion:
            result = restar(operacion)
        elif '*' in operacion:
            if buscar_numero(operacion):
                result = multi_por_escalar(operacion)
            else:
                result = multipliacion_matrices(operacion)
        elif 'det' in operacion:
            result = determinante(operacion)
        elif 'inv' in operacion:
            result = matriz_inversa(operacion)
    return redirect('mat')


def guardar_valores(m, name):
    global datos
    global fil
    global col
    mat = creadorDeMatrices(m)
    col, fil = saberDeCuantoPorCuantoEs(mat)
    mat_final = rellenarLosEspacios(mat)
    datos.append([name, np.array(mat_final), fil, col])
    print(datos)


def resolver_ecu_lineales(request):
    entrada = request.POST['mat_lin']
    mat, b = armar_sistema(entrada)
    x = solucionar_ecuacion_lineal(mat, b)
    return render(request, 'Matrices/form_matrices.html', {'x': x})


#################################### lOGICA ####################################
def creadorDeMatrices(valores):
    aux = list()
    auxDos = ""
    matriz = []
    for i in range(len(valores)):
        if valores[i] != "," and valores[i] != " ":
            auxDos += valores[i]
        if valores[i] == "," or i == len(valores) - 1 or valores[i] == " ":
            aux.append(float(auxDos))
            auxDos = ""
        if valores[i] == " " or i == len(valores) - 1:
            matriz.append(aux.copy())
            auxDos = ""
            aux.clear()

    return matriz


def saberDeCuantoPorCuantoEs(matriz):
    aux = 0
    filas = len(matriz)
    for i in range(0, len(matriz)):
        if aux < len(matriz[i]):
            aux = len(matriz[i])

    return aux, filas


def rellenarLosEspacios(matriz):
    numerosFaltan, filas = saberDeCuantoPorCuantoEs(matriz)
    for i in range(0, len(matriz)):
        if numerosFaltan > len(matriz[i]):
            matriz[i].append(0)
    return matriz


def limpiar_diccionario():
    global datos
    global result
    datos.clear()
    result = ""


def guardar_matriz(request):
    name = request.POST['nombre']
    matriz = request.POST['matriz']
    guardar_valores(matriz, name)


def sumar(valor):
    aux=[]
    dimension = 0
    suma = 0
    for x in valor:
        if x != '+':
            aux.append(x)
    dimension = get_pos_array(aux[0])
    for i in aux:
        if existe_matriz(i):
            if get_pos_array(i)[2] == dimension[2] and get_pos_array(i)[3] == dimension[3]:
                suma = suma + determinar_matriz(i)
            else:
                suma = 'las matrices deben tener las mismas dimensiones'
        else:
            suma = 'no existe la matriz '+i
            return suma
    return suma

def restar(valor):
    aux=[]
    dimension = 0
    resta = 0
    for x in valor:
        if x != '-':
            aux.append(x)
    dimension = get_pos_array(aux[0])
    for i in aux:
        if existe_matriz(i):
            if get_pos_array(i)[2] == dimension[2] and get_pos_array(i)[3] == dimension[3]:
                if i == aux[0]:
                    resta = determinar_matriz(i)
                else:
                    resta = resta - determinar_matriz(i)
            else:
                resta = 'las matrices deben tener las mismas dimensiones'
        else:
            resta = 'no existe la matriz '+i
            return  resta
    return resta

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
            res = i[1] * float(num)
            return res

    return 'no se encontró ninguna matriz con ese identificador'


def determinante(valor):
    est = False
    conta = 0
    res = 0
    while conta < (len(valor) - 1) and est == False:
        if valor[conta + 1] == ')':
            if existe_matriz(valor[conta]):
                if es_cuadrada(valor[conta]) == True:
                    res = np.linalg.det(determinar_matriz(valor[conta]))
                    est = True
                else:
                    res = 'la matriz no es cuadrada'
            else:
                res = 'la matriz no existe'
                return res
        conta += 1
    return res


def determinar_matriz(valor):
    global datos
    for x in datos:
        if x[0] == valor:
            return x[1]
    return 0


def buscar_numero(dato):
    estado = False
    for x in dato:
        if x.isnumeric() == True:
            estado = True
    return estado


def multipliacion_matrices(valor):
    res = 0
    aux = []
    global datos
    for y in valor:
        if y != '*':
            aux.append(determinar_matriz(y))
    if get_col(valor[0]) == get_fil(valor[2]):
        for x in range(len(aux) - 1):
            res = np.matmul(aux[x], aux[x + 1])
    else:
        res = 'recuerda que el numero de columbas de la matriz '+valor[0]+\
              ' deben ser igual al numero de filas de la matriz '+valor[2]
    return res


def es_cuadrada(valor):
    global datos
    conta = 0
    est = False
    while conta < len(datos) and est == False:
        if datos[conta][0] == valor:
            if datos[conta][2] == datos[conta][3]:
                est = True
        conta += 1
    return est

def armar_sistema(cadena):
    matriz = []
    aux = []
    aux2 = ""
    aux3 = ""
    b = []
    conta = 1000
    for x in range(len(cadena)):
        if cadena[x] != ',' and (cadena[x] == '-' or cadena[x].isnumeric() or cadena[x] == '.') and cadena[x] != '=' and x < conta:
            aux2 += cadena[x]
        elif cadena[x] == ',':
            aux.append(float(aux2))
            aux2 = ""
        elif cadena[x] == '=':
            matriz.append(aux.copy())
            aux.clear()
            conta = x
        elif x > conta:
            if cadena[x] != ' ':
                aux3 += cadena[x]
        if x == len(cadena) - 1 or cadena[x + 1] == ' ':
            b.append(float(aux3))
            aux3 = ""
            conta = 10000
    return matriz, b


def solucionar_ecuacion_lineal(mat, b):
    a = np.array(mat)
    v_sol = np.array(b)
    x = np.linalg.solve(a, v_sol)
    return x

def get_col(valor):
    global datos
    for x in datos:
        if valor == x[0]:
            return x[3]

def get_fil(valor):
    global datos
    for x in datos:
        if valor == x[0]:
            return x[2]

def matriz_inversa(valor):
    id_matriz =''
    matriz_aux = 0
    inversa = ''
    for x in range(len(valor)):
        if valor[x-1] == '(':
            id_matriz = valor[x]
    if es_cuadrada(id_matriz) == True:
        matriz_aux = determinar_matriz(id_matriz)
        inversa = np.linalg.inv(matriz_aux)
    else:
        inversa = 'la matriz debe ser cuadrada'

    return inversa

def get_pos_array(valor):
    global datos
    conta = 0
    est = False
    dato = 0
    while conta < len(datos) and est == False:
        if datos[conta][0] == valor:
            dato = datos[conta]
            est = True
        conta+=1
    return dato

def existe_matriz(valor):
    global datos
    for x in datos:
        if x[0] == valor:
            return True
    return False