import re

from django.shortcuts import render, redirect
import numpy as np
from scipy import linalg
import sympy as sp


#################################### VARIABLES GLOBALES ####################################

datos = dict()
result = []
resulado = []
resultado_a_c=[]
fil = 0
col = 0


#################################### HTML ####################################

def mostrar_formulario_ecu_lineal(request):
    return render(request, 'Matrices/form_matrices.html')

def mostrar_form_ajuste_de_curvas(request):
    global resultado_a_c
    return render(request,'Matrices/form_ajuste_curvas.html',{'result':resultado_a_c})


def formulario_completo_matrices(request):
    global datos
    global result
    global resulado
    return render(request, 'Matrices/form_completo.html', {'datos': datos, 'result': resulado,})


def resolver(request):
    global resulado
    global datos
    boton = request.POST['calcular']
    operacion = request.POST['operacion']
    if boton == 'Guardar Matrices':
        guardar_matriz_text_area(request)
    elif boton == 'Borrar':
        limpiar_diccionario()
    elif boton == 'calculo':
        try:
            result = ecuacionesMatrices(operacion,datos)
            resulado.append([operacion,result])
        except:
            result = 'Algo salio mal'
            resulado.append([operacion,result])
        # if '+' in operacion:
        #     #result.append([operacion,sumar(operacion)])
        #     resulado.append([operacion,sumar(operacion)])
        # elif '-' in operacion:
        #     result = restar(operacion)
        #     resulado.append([operacion,restar(operacion)])
        # elif '*' in operacion:
        #     if buscar_numero(operacion):
        #         result = multi_por_escalar(operacion)
        #         resulado.append([operacion,multi_por_escalar(operacion)])
        #     else:
        #         result = multipliacion_matrices(operacion)
        #         resulado.append([operacion,multipliacion_matrices(operacion)])
        # elif 'det' in operacion:
        #     result = determinante(operacion)
        #     resulado.append([operacion,determinante(operacion)])
        # elif 'inv' in operacion:
        #     result = matriz_inversa(operacion)
        #     resulado.append([operacion,matriz_inversa(operacion)])
        # elif 'transpuesta' in operacion:
        #     result = matriz_transpuesta(operacion)
        #     resulado.append([operacion,matriz_transpuesta(operacion)])
    resulado.reverse()
    return redirect('mat')


# def guardar_valores(m, name):
#     global datos
#     global fil
#     global col
#     mat = creadorDeMatrices(m)
#     col, fil = saberDeCuantoPorCuantoEs(mat)
#     mat_final = rellenarLosEspacios(mat)
#     datos.append([name, np.array(mat_final), fil, col])
#     print(datos)

def guardar_valores_area(m, name):
    global datos
    global fil
    global col
    mat = ordenar_2(m)
    a = to_matriz(mat)
    t = to_float(a)
    col, fil = saberDeCuantoPorCuantoEs(mat)
    mat_final = rellenarLosEspacios(t)
    datos[name] =np.array(mat_final)


def resolver_ecu_lineales(request):
    entrada_mat = request.POST['textarea']
    entrada_vec = request.POST['vec']
    m = ordenar_2(entrada_mat)
    a = to_matriz(m)
    t = to_float(a)
    mat = rellenarLosEspacios(t)
    b = ordenar_arreglo(entrada_vec)
    x = solucionar_ecuacion_lineal(mat, b)
    return render(request, 'Matrices/form_matrices.html', {'x': x})

def resolver_ajuste_curvas(request):
    boton  = request.POST['calcular']
    global resultado_a_c
    if boton == 'Borrar':
        limpiar_respuesta()
    elif boton == 'calcular':
        x =  request.POST['x']
        solx = ordenar_arreglo(x)
        print(solx)
        y = request.POST['y']
        soly = ordenar_arreglo(y)
        print(soly)
        n = len(solx)
        resultado_a_c = solucionar_ajuste_curvas(solx,soly,n)
    return redirect('ajuste_curvas')

#################################### lOGICA ####################################
# def creadorDeMatrices(valores):
#     aux = list()
#     auxDos = ""
#     matriz = []
#     for i in range(len(valores)):
#         if valores[i] != "," and valores[i] != " ":
#             auxDos += valores[i]
#         if valores[i] == "," or i == len(valores) - 1 or valores[i] == " ":
#             aux.append(float(auxDos))
#             auxDos = ""
#         if valores[i] == " " or i == len(valores) - 1:
#             matriz.append(aux.copy())
#             auxDos = ""
#             aux.clear()
#
#     return matriz

def ordenar_2(msj):
    lista = msj.split(sep='\r\n')
    lista_final = []
    for x in lista:
        lista_final.append(x)
    return lista_final

def to_matriz(msj):
    mat = []
    for x in msj:
        fila = x.split(sep=' ')
        mat.append(fila)
    return mat

def to_float(msj):
    mat = []
    aux = []
    for x in msj:
        for y in x:
            aux.append(float(y))
        mat.append(aux.copy())
        aux.clear()
    return mat


def ordenar_arreglo(msj):
    lista = msj.split(sep=',')
    lista_final = []
    for x in lista:
        lista_final.append(float(x))
    return lista_final

def creadorDeMatrices_area(valores):
    aux = list()
    auxDos = ""
    matriz = []
    for i in range(len(valores)):
        if valores[i] != "," and valores[i] != "\n" and valores[i] != " ":
            auxDos += valores[i]
        if valores[i] == "," or i == len(valores) - 1 or valores[i+2] == "\n":
            aux.append(float(auxDos))
            auxDos = ""
        if valores[i] == "\n" or i == len(valores) - 1:
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
    global resulado
    datos.clear()
    resulado.clear()
    result = ""


# def guardar_matriz(request):
#     name = request.POST['nombre']
#     matriz = request.POST['matriz']
#     guardar_valores(matriz, name)

def guardar_matriz_text_area(request):
    name = request.POST['nombre']
    matriz = request.POST['textarea']
    guardar_valores_area(matriz, name)


# def sumar(valor):
#     aux=[]
#     dimension = 0
#     suma = 0
#     for x in valor:
#         if x != '+':
#             aux.append(x)
#     dimension = get_pos_array(aux[0])
#     for i in aux:
#         if existe_matriz(i):
#             if get_pos_array(i)[2] == dimension[2] and get_pos_array(i)[3] == dimension[3]:
#                 suma = suma + determinar_matriz(i)
#             else:
#                 suma = 'las matrices deben tener las mismas dimensiones'
#         else:
#             suma = 'no existe la matriz '+i
#             return suma
#     return suma
#
# def restar(valor):
#     aux=[]
#     dimension = 0
#     resta = 0
#     for x in valor:
#         if x != '-':
#             aux.append(x)
#     dimension = get_pos_array(aux[0])
#     for i in aux:
#         if existe_matriz(i):
#             if get_pos_array(i)[2] == dimension[2] and get_pos_array(i)[3] == dimension[3]:
#                 if i == aux[0]:
#                     resta = determinar_matriz(i)
#                 else:
#                     resta = resta - determinar_matriz(i)
#             else:
#                 resta = 'las matrices deben tener las mismas dimensiones'
#         else:
#             resta = 'no existe la matriz '+i
#             return  resta
#     return resta

# def multi_por_escalar(escalar):
#     mat = ""
#     num = ""
#     res = ""
#     global datos
#     for x in range(len(escalar)):
#         if escalar[x].isnumeric():
#             num = escalar[x]
#         elif escalar[x] != '*':
#             mat = escalar[x]
#         else:
#             pass
#     for i in datos:
#         if i[0] == mat:
#             res = i[1] * float(num)
#             return res
#         else:
#             res ='no se encontró ninguna matriz con ese identificador'
#
#     return res


# def determinante(valor):
#     est = False
#     conta = 0
#     res = 0
#     while conta < (len(valor) - 1) and est == False:
#         if valor[conta + 1] == ')':
#             if existe_matriz(valor[conta]):
#                 if es_cuadrada(valor[conta]) == True:
#                     res = np.linalg.det(determinar_matriz(valor[conta]))
#                     est = True
#                 else:
#                     res = 'la matriz no es cuadrada'
#             else:
#                 res = 'la matriz no existe'
#                 return res
#         conta += 1
#     return res

def matrizElevada(elevado, matriz):
    aux = matriz
    for i in range(elevado - 1):
        aux = np.dot(aux, matriz)
    return aux

def operar(ecuacion, diccionario):
    num = 0
    for i in diccionario.keys():
        num +=ecuacion.count(i)
    if "*" in ecuacion and "^" in ecuacion:
        i = ecuacion.index("^")
        iDos = ecuacion.index("*")
        if "(" in ecuacion:
            if i < iDos :
                matrizElevar = ecuacion[1:i]
                elevado = ecuacion[i+1:iDos]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado),diccionario[matrizElevar])
                    if elevado == "T" :
                        solucionUno =  diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd' :
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                solucionUno = np.array(solucionUno)
                multiplicado = ecuacion[iDos+1:len(ecuacion)-1]
                if multiplicado in diccionario.keys():
                    solucion = np.dot(solucionUno, diccionario[multiplicado])
                else:
                    solucion = solucionUno * float(multiplicado)
            if iDos < i :
                matrizElevar = ecuacion [iDos+1:i]
                elevado = ecuacion [i+1:len(ecuacion)-1]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado),diccionario[matrizElevar])
                    if elevado == "T" :
                        solucionUno =  diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd' :
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                solucionUno = np.array(solucionUno)
                multiplicado = ecuacion[1:iDos]
                if multiplicado in diccionario.keys():
                    solucion = np.dot(solucionUno, diccionario[multiplicado])
                else:
                    solucion = solucionUno * float(multiplicado)
        else:
            if i < iDos :
                matrizElevar = ecuacion[0:i]
                elevado = ecuacion[i+1:iDos]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado),diccionario[matrizElevar])
                    if elevado == "T" :
                        solucionUno =  diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd' :
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                solucionUno = np.array(solucionUno)
                multiplicado = ecuacion[iDos+1:len(ecuacion)]
                if multiplicado in diccionario.keys():
                    solucion = np.dot(solucionUno, diccionario[multiplicado])
                else:
                    solucion = solucionUno * float(multiplicado)
            if iDos < i :
                matrizElevar = ecuacion [iDos+1:i]
                elevado = ecuacion [i+1:len(ecuacion)]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado),diccionario[matrizElevar])
                    if elevado == "T" :
                        solucionUno =  diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd' :
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                solucionUno = np.array(solucionUno)
                multiplicado = ecuacion[0:iDos]

                if multiplicado in diccionario.keys():
                    solucion = np.dot(solucionUno, diccionario[multiplicado])
                else:
                    solucion = solucionUno * float(multiplicado)



    if ("+" in ecuacion or "-" in ecuacion) and "^" in ecuacion and num >= 2:
        if "(" in ecuacion and "-" in ecuacion:
            i = ecuacion.index("^")
            iDos = ecuacion.index("-")
            if i < iDos:
                matrizElevar = ecuacion[1:i]
                elevado = ecuacion[i + 1: iDos]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[iDos + 1:len(ecuacion) - 1]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno - diccionario[restar]
            if i > iDos:
                matrizElevar = ecuacion[iDos + 1:i]
                elevado = ecuacion[i + 1:len(ecuacion) - 1]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[1:iDos]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno - diccionario[restar]

        if "(" not in ecuacion and "-" in ecuacion:
            i = ecuacion.index("^")
            iDos = ecuacion.index("-")
            if i < iDos:
                matrizElevar = ecuacion[0:i]
                elevado = ecuacion[i + 1: iDos]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[iDos + 1:len(ecuacion)]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno - diccionario[restar]
            if i > iDos:
                matrizElevar = ecuacion[iDos + 1:i]
                elevado = ecuacion[i + 1:len(ecuacion)]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[0:iDos]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno - diccionario[restar]

        if "(" in ecuacion and "+" in ecuacion:
            i = ecuacion.index("^")
            iDos = ecuacion.index("+")
            if i < iDos:
                matrizElevar = ecuacion[1:i]
                elevado = ecuacion[i + 1: iDos]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[iDos + 1:len(ecuacion) - 1]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno + diccionario[restar]
            if i > iDos:
                matrizElevar = ecuacion[iDos + 1:i]
                elevado = ecuacion[i + 1:len(ecuacion) - 1]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[1:iDos]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno + diccionario[restar]

        if "(" not in ecuacion and "+" in ecuacion:
            i = ecuacion.index("^")
            iDos = ecuacion.index("+")
            if i < iDos:
                matrizElevar = ecuacion[0:i]
                elevado = ecuacion[i + 1: iDos]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[iDos + 1:len(ecuacion)]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno + diccionario[restar]
            if i > iDos:
                matrizElevar = ecuacion[iDos + 1:i]
                elevado = ecuacion[i + 1:len(ecuacion)]
                if matrizElevar in diccionario.keys():
                    if elevado.isdigit() and elevado != "-1" and elevado != "D" and elevado!='d':
                        solucionUno = matrizElevada(int(elevado), diccionario[matrizElevar])
                    if elevado == "T":
                        solucionUno = diccionario[matrizElevar].T
                    if elevado == "-1":
                        solucionUno = np.linalg.inv(diccionario[matrizElevar])
                    if elevado == "D" or elevado == 'd':
                        solucionUno = np.linalg.det(diccionario[matrizElevar])
                restar = ecuacion[0:iDos]
                solucionUno = np.array(solucionUno)
                solucion = solucionUno + diccionario[restar]

    if "+" in ecuacion and "-" not in ecuacion and "*" not in ecuacion and "^" not in ecuacion and "/" not in ecuacion:
        i = ecuacion.index("+")
        if "(" in ecuacion:
            if ecuacion[1:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion) - 1] in diccionario.keys():
                solucion = diccionario[ecuacion[1:i]] + diccionario[ecuacion[i + 1:len(ecuacion) - 1]]
        else:
            if ecuacion[0:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion)] in diccionario.keys():
                solucion = diccionario[ecuacion[0:i]] + diccionario[ecuacion[i + 1:len(ecuacion)]]
    if "-" in ecuacion and "+" not in ecuacion and "*" not in ecuacion and "^" not in ecuacion and "/" not in ecuacion:
        i = ecuacion.index("-")
        if "(" in ecuacion:
            if ecuacion[1:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion) - 1] in diccionario.keys():
                solucion = diccionario[ecuacion[1:i]] - diccionario[ecuacion[i + 1:len(ecuacion) - 1]]
        else:
            if ecuacion[0:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion)] in diccionario.keys():
                solucion = diccionario[ecuacion[0:i]] - diccionario[ecuacion[i + 1:len(ecuacion)]]
    if "^" in ecuacion and "+" not in ecuacion and "*" not in ecuacion and "/" not in ecuacion \
            and num <= 1:
        i = ecuacion.index("^")
        if "(" in ecuacion:
            if "-"in ecuacion[1:i]:
                numero = ecuacion[i + 1:len(ecuacion) - 1]
                if numero == "-1":
                    solucionUno = np.linalg.inv(diccionario[ecuacion[2:i]])
                    solucionUno = np.array(solucionUno)
                    solucion = solucionUno * (-1)
                if numero == "D" or numero == "d":
                    solucionUno = np.linalg.det(diccionario[ecuacion[2:i]])
                    solucionUno = np.array(solucionUno)
                    solucion = solucionUno * (-1)
                if numero == "T" or numero == "t":
                    solucionUno = diccionario[ecuacion[2:i]].T
                    solucionUno = np.array(solucionUno)
                    solucion = solucionUno * (-1)
                else:
                    if ecuacion[2:i] in diccionario.keys() and numero != "-1" and numero != "D" \
                            and numero != "d" and numero != "T" and numero != "t":
                        solucionUno = matrizElevada(int(numero), diccionario[ecuacion[2:i]])
                        solucionUno = np.array(solucionUno)
                        solucion = solucionUno * (-1)
            else:
                numero = ecuacion[i + 1:len(ecuacion) - 1]
                if numero == "-1":
                    solucion = np.linalg.inv(diccionario[ecuacion[1:i]])
                if numero == "D" or numero == "d":
                    solucion = np.linalg.det(diccionario[ecuacion[1:i]])
                if numero == "T" or numero == "t":
                    solucion = diccionario[ecuacion[1:i]].T
                else:
                    if ecuacion[1:i] in diccionario.keys() and numero != "-1" and numero != "D" \
                            and numero != "d" and numero != "T" and numero != "t":
                        solucion = matrizElevada(int(numero), diccionario[ecuacion[1:i]])
        else:
            if "-" in ecuacion[0:i]:
                numero = ecuacion[i + 1:len(ecuacion)]
                if numero == "-1":
                    solucionUno = np.linalg.inv(diccionario[ecuacion[1:i]])
                    solucionUno = np.array(solucionUno)
                    solucion = solucionUno * (-1)
                if numero == "D" or numero == "d":
                    solucionUno = np.linalg.det(diccionario[ecuacion[1:i]])
                    solucionUno = np.array(solucionUno)
                    solucion = solucionUno * (-1)
                if numero == "T" or numero == "t":
                    solucionUno = diccionario[ecuacion[1:i]].T
                    solucionUno = np.array(solucionUno)
                    solucion = solucionUno * (-1)
                else:
                    if ecuacion[0:i] in diccionario.keys() and numero != "-1" and numero != "D" \
                            and numero != "d" and numero != "T" and numero != "t":
                        solucionUno = matrizElevada(int(numero), diccionario[ecuacion[1:i]])
                        solucionUno = np.array(solucionUno)
                        solucion = solucionUno * (-1)
            else:
                numero = ecuacion[i + 1:len(ecuacion)]
                if numero == "-1":
                    solucion = np.linalg.inv(diccionario[ecuacion[0:i]])
                if numero == "D" or numero == "d":
                    solucion = np.linalg.det(diccionario[ecuacion[0:i]])
                if numero == "T" or numero == "t":
                    solucion = diccionario[ecuacion[0:i]].T
                else:
                    if ecuacion[0:i] in diccionario.keys() and numero != "-1" and numero != "D" \
                            and numero != "d" and numero != "T" and numero != "t":
                        solucion = matrizElevada(int(numero), diccionario[ecuacion[0:i]])
    if "*" in ecuacion and "+" not in ecuacion and "-" not in ecuacion and "^" not in ecuacion and "/" not in ecuacion:
        i = ecuacion.index("*")
        if "(" in ecuacion:
            if ecuacion[i + 1].isdigit():
                posU = i + 1
                posJ = len(ecuacion) - 1
                numero = float(ecuacion[posU:posJ])
                if ecuacion[1:i] in diccionario.keys() and numero != -1:
                    solucion = np.dot(numero, diccionario[ecuacion[1:i]])
            if ecuacion[1:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion) - 1] in diccionario.keys():
                solucion = np.dot(diccionario[ecuacion[1:i]], diccionario[ecuacion[i + 1:len(ecuacion) - 1]])
        else:
            if ecuacion[i + 1].isdigit():
                posU = i + 1
                posJ = len(ecuacion)
                numero = float(ecuacion[posU:posJ])
                if ecuacion[0:i] in diccionario.keys() and numero != -1:
                    solucion = np.dot(numero, diccionario[ecuacion[0:i]])
            if ecuacion[0:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion)] in diccionario.keys():
                solucion = np.dot(diccionario[ecuacion[0:i]], diccionario[ecuacion[i + 1:len(ecuacion)]])
    if "/" in ecuacion and "+" not in ecuacion and "-" not in ecuacion and "^" not in ecuacion and "*" not in ecuacion:
        i = ecuacion.index("/")
        if "(" in ecuacion:
            if ecuacion[i+1].isdigit():
                posU = i + 1
                posJ = len(ecuacion)-1
                numero = float(ecuacion[posU:posJ])
                if ecuacion[1:i] in diccionario.keys() and numero != -1:
                    solucion = diccionario[ecuacion[1:i]] / numero
            if ecuacion[1:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion) - 1] in diccionario.keys():
                solucion = diccionario[ecuacion[1:i]] / diccionario[ecuacion[i + 1:len(ecuacion) - 1]]
        else:
            if ecuacion[i + 1].isdigit():
                posU = i + 1
                posJ = len(ecuacion)
                numero = float(ecuacion[posU:posJ])
                if ecuacion[0:i] in diccionario.keys() and numero != -1:
                    solucion = diccionario[ecuacion[1:i]] / numero
            if ecuacion[0:i] in diccionario.keys() and ecuacion[i + 1:len(ecuacion) ] in diccionario.keys():
                solucion = diccionario[ecuacion[0:i]] / diccionario[ecuacion[i + 1:len(ecuacion) ]]
    return solucion


def ecuacionesMatrices(ecuacion, matriz):
    i = 0
    f = 0
    clave = ""
    auxiliar = ecuacion
    auxDos = ""
    diccionario = matriz.copy()
    while len(auxiliar) != 0:
        if "(" in auxiliar:

            if i + 1 < len(auxiliar) and auxiliar[i] != ")":
                if auxiliar[i] == "(" and auxiliar[i + 1] != "(":
                    posicionInicial = i
                if auxiliar[i + 1] == "(":
                    posicionInicial = i + 1
            if auxiliar[i] == ")":
                posicionFinal = i
                if posicionInicial != -1 and posicionFinal != -1:
                    auxDos = auxiliar[posicionInicial: posicionFinal + 1]
                    clave = "r" + str(f)
                    diccionario[str(clave)] = np.array(operar(auxDos, diccionario))
                    if len(auxDos) == len(auxiliar):
                        auxiliar = auxiliar.replace(auxDos, "")
                    else:
                        auxiliar = auxiliar.replace(auxDos, str(clave))
                    f = f + 1
                    i = 0
                    posicionInicial = 0
                    posicionFinal = 0
                    auxDos = ""
        i = i + 1

        if "(" not in auxiliar:
            if "^" in auxiliar:
                posicionInicial = 0
                posicionFinal = len(auxiliar)
                auxDos = auxiliar[posicionInicial:posicionFinal]
                clave = "r" + str(f)
                diccionario[str(clave)] = np.array(operar(auxDos, diccionario))
                if len(auxDos) == len(auxiliar):
                    auxiliar = auxiliar.replace(auxDos, "")
                else:
                    auxiliar = auxiliar.replace(auxDos, str(clave))
                f = f + 1
            if "*" in auxiliar:
                posicionInicial = 0
                posicionFinal = len(auxiliar)
                auxDos = auxiliar[posicionInicial:posicionFinal]
                clave = "r" + str(f)
                diccionario[str(clave)] = np.array(operar(auxDos, diccionario))
                if len(auxDos) == len(auxiliar):
                    auxiliar = auxiliar.replace(auxDos, "")
                else:
                    auxiliar = auxiliar.replace(auxDos, str(clave))
                f = f + 1
            if "/" in auxiliar:
                posicionInicial = 0
                posicionFinal = len(auxiliar)
                auxDos = auxiliar[posicionInicial:posicionFinal]
                clave = "r" + str(f)
                diccionario[str(clave)] = np.array(operar(auxDos, diccionario))
                if len(auxDos) == len(auxiliar):
                    auxiliar = auxiliar.replace(auxDos, "")
                else:
                    auxiliar = auxiliar.replace(auxDos, str(clave))
                f = f + 1
            if "-" in auxiliar:
                posicionInicial = 0
                posicionFinal = len(auxiliar)
                auxDos = auxiliar[posicionInicial:posicionFinal]
                clave = "r" + str(f)
                diccionario[str(clave)] = np.array(operar(auxDos, diccionario))
                if len(auxDos) == len(auxiliar):
                    auxiliar = auxiliar.replace(auxDos, "")
                else:
                    auxiliar = auxiliar.replace(auxDos, str(clave))
                f = f + 1
            if "+" in auxiliar:
                posicionInicial = 0
                posicionFinal = len(auxiliar)
                auxDos = auxiliar[posicionInicial:posicionFinal]
                clave = "r" + str(f)
                diccionario[str(clave)] = np.array(operar(auxDos, diccionario))
                if len(auxDos) == len(auxiliar):
                    auxiliar = auxiliar.replace(auxDos, "")
                else:
                    auxiliar = auxiliar.replace(auxDos, str(clave))
                f = f + 1
    return diccionario[clave]

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


# def multipliacion_matrices(valor):
#     res = 0
#     aux = []
#     global datos
#     for y in valor:
#         if y != '*':
#             aux.append(determinar_matriz(y))
#     if get_col(valor[0]) == get_fil(valor[2]):
#         for x in range(len(aux) - 1):
#             res = np.matmul(aux[x], aux[x + 1])
#     else:
#         res = 'recuerda que el numero de columbas de la matriz '+valor[0]+\
#               ' deben ser igual al numero de filas de la matriz '+valor[2]
#     return res


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
    final = retornar_impresion_ecu_lineal(x)
    return final

def retornar_impresion_ecu_lineal(arreglo):
    msj = []
    for x in range(len(arreglo)):
        msj.append('x'+str(x+1)+' = '+str(arreglo[x]))
    return msj


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

def get_id(valor):
    respuesta = ''
    for x in range(len(valor)):
        if valor[x-1] == '(':
            respuesta = valor[x]
    return respuesta

# def matriz_inversa(valor):
#     id_matriz =''
#     matriz_aux = 0
#     inversa = ''
#     for x in range(len(valor)):
#         if valor[x-1] == '(':
#             id_matriz = valor[x]
#     if es_cuadrada(id_matriz) == True:
#         matriz_aux = determinar_matriz(id_matriz)
#         inversa = np.linalg.inv(matriz_aux)
#     else:
#         inversa = 'la matriz debe ser cuadrada'
#
#     return inversa

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

# def matriz_transpuesta(valor):
#     id_mat = get_id(valor)
#     mat = 0
#     trans = 0
#     if existe_matriz(id_mat):
#         mat = determinar_matriz(id_mat)
#         trans = trasponer(mat)
#     else:
#         trans = 'no existe una matriz con ese id'
#
#     return trans

def trasponer(m):
    return np.transpose(m)

def limpiar_respuesta():
    global resultado_a_c
    resultado_a_c.clear()

def determinar_func(func,valor):
    ecuacion = sp.sympify(func)
    simbolo = sp.symbols('x')
    result = ecuacion.evalf(subs={simbolo:float(valor)})
    return result

def hallar_media_y(y):
    suma = 0
    promedio = 0
    for x in y:
        suma += x
    promedio = int(suma/len(y))
    return promedio

def hallar_st(y):
    media = hallar_media_y(y)
    sumatoria = 0
    for i in y:
        sumatoria += pow((i-media),2)
    return sumatoria

def hallar_sr(funcion,x,y):
    sumatoria = 0
    for i in range(len(x)):
        sumatoria += pow(y[i]-determinar_func(funcion,x[i]),2)
    return sumatoria

def sumatoria(arreglo,exp):
    suma = 0
    for a in arreglo:
        suma = suma + pow(a,exp)

    return suma

def sumatoria_y(expo,x,y):
    suma = 0
    for i in range(len(x)):
        suma += pow(x[i],expo)*y[i]
    return suma

def resultado_y(x,y):
    sumar = []
    for d in range(7):
        sumar.append(sumatoria_y(d,x,y))
    return np.array(sumar)

def get_respuesta(vec,mat):
    res = []
    for c in range(len(mat)):
        res.append(vec[c])
    return np.array(res)

def retornar_func(num):
    msj = ''
    for n in range(len(num)):
        if n == 0:
            msj += str('{:.9f}'.format(num[n]))+' '
        else:
            if num[n] < 0:
                msj += str('{:.9f}'.format(num[n]))+'*x^'+str(n)+' '
            else:
                msj += ' + '+str('{:.9f}'.format(num[n]))+'*x^'+str(n)+' '
    return msj

def resolver_lineal(mat,vec):
    m = np.linalg.solve(mat,vec)
    return retornar_func(m)

def resolver_ecuaciones_lineales(mat,vec):
    aux1 =[]
    aux2 = []
    result =[]
    for x in range(6):
        for m in range(len(mat)):
            aux1.append([get_respuesta(vec,mat[m]),mat[m]])
        if np.linalg.det(aux1[x][1]) != 0:
            aux2.append([x+1,resolver_lineal(aux1[x][1],aux1[x][0])])
        else:
            aux2.append('el determinante de esta matriz es 0')
            return False
    return aux2

def solucionar_ajuste_curvas(x,y,n):
    respuestas = []
    vector = []
    aux = []
    result = []
    terminos_funcion = []
    conta = 8
    exponente = 0
    coeficiente = 0
    resultados = resultado_y(x,y)
    # me rellena todas las matrices.
    for i in range(2, conta):
        for f in range(i):
            for c in range(i):
                if c == 0 and f == 0:
                    aux.append(n)
                else:
                    aux.append(sumatoria(x, exponente))
                if c == i - 1:
                    respuestas.append(aux.copy())
                    aux.clear()
                    exponente = f
                exponente += 1

        vector.append(np.array(respuestas.copy()))
        respuestas.clear()
        exponente = 0

    final = resolver_ecuaciones_lineales(vector, resultados)
    print(final)
    if final != False:
        st = hallar_st(y)
        for t in range(len(final)):
            sr = hallar_sr(final[t][1],x,y)
            coeficiente = pow(((st - sr) / st), 0.5)
            print(coeficiente)
            final[t].append(coeficiente)

        return final
    else:
        return []


#6,-2.5,2.1,4.1,=12.5 12,-8,6,10,=34.75 0.5,-13,9,2.4,=27 -6,0.25,1.75,-18,=-38