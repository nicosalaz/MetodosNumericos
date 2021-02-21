from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import math


def mostrar_calculadora_decimal(request):
    return render(request,'base_diez.html')

def mostrar_calculadora_binaria(request):
    return render(request,'base_binaria.html')

def mostrar_calculadora_hexadecimal(request):
    return render(request, 'base_hexa.html')

def mostrar_calculadora_octal(request):
    return render(request, 'base_octal.html')


def resultado_decimal(request):

    numero = float(request.POST['numero'])
    parte_decimal,parte_entero = math.modf(numero)
    binario = 0
    octal = 0
    hexa = 0
    aux = 0


    if parte_decimal == 0:
        binario = float(hallar_binario(numero))
        octal = hallar_octal(numero)
        hexa = hallar_hexadecimal(numero)
        return render(request, 'resultado_decimal.html', {'numero': numero, 'binario': binario,
                                                          'hexadecimal': hexa, 'octal': octal})
    else:
        binario = str(hallar_binario(parte_entero)) + '.' + str(hallar_binario_flotante(parte_decimal))
        hexa = str(hallar_hexadecimal(parte_entero))+'.'+str(hallar_hexa_octa_flotante(parte_decimal,16))
        octal = str(hallar_octal(parte_entero))+'.'+str(hallar_hexa_octa_flotante(parte_decimal,8))

        return render(request, 'resultado_decimal.html', {'numero': numero, 'binario': binario,
                                                          'hexadecimal': hexa, 'octal': octal})

def resultado_binario(request):
    binario = request.POST['binario']
    parte_decimal, parte_entero = math.modf(binario)
    decimal = 0
    octal = 0
    hexa = 0

    if '.' in binario:
        decimal = str(hallar_binario(parte_entero)+'.'+str(hallar_decimal_flotante(parte_decimal)))
        return render(request, 'resultado_binario.html', {'binario': binario, 'decimal': decimal,
                                                          'hexadecimal': hexa, 'octal': octal})
    else:
        decimal = hallar_decimal(binario)
        octal = hallar_octal(decimal)
        hexa = hallar_hexadecimal(decimal)
        return render(request, 'resultado_binario.html', {'binario': binario, 'decimal': decimal,
                                                          'hexadecimal': hexa, 'octal': octal})

def resultado_hexa_dec(request):
    numero = request.POST['hexa']
    aux = []
    decimal = 0
    for x in numero:
        aux.append(x)
    hexa = hallar_hexa_dec(aux)
    for h in range(0,len(hexa)):
        decimal += (16**h)*int(hexa[h])
    octal = hallar_octal(decimal)
    binario = hallar_binario(decimal)
    return render(request,'resultado_hexa_dec.html',{'numero':numero,'decimal':decimal,
                                                     'binario':binario,'octal':octal})

def resultado_octa_dec(request):
    numero = request.POST['octal']
    aux =[]
    octal = 0
    for x in numero:
        aux.append(x)
    aux.reverse()
    for y in range(len(aux)):
        octal+=(8**y)*int(aux[y])
    hexa = hallar_hexadecimal(octal)
    binario = hallar_binario(octal)
    return render(request,'resultado_octal_dec.html',{'numero':numero,'octal':octal,
                                                      'hexadecimal':hexa,'binario':binario})

def hallar_decimal(numero):
    entero = {}
    aux = []
    k = 1
    decimal = 0
    for b in numero:
        aux.append(b)

    aux.reverse()

    for a in aux:
        entero[k] = a
        print(k)
        k *= 2

    for clave in entero:
        if entero[clave] == '1':
            decimal += clave

    return decimal

def hallar_binario(numero):
    binario = ""
    for b in bin(int(numero)):
        binario +=b
        if binario == '0b':
            binario=""

    return binario


def hallar_hexadecimal(numero):
    hexa = ""
    for h in hex(int(numero)):
        hexa +=h
        if hexa == '0x':
            hexa=""

    return hexa

def hallar_octal(numero):
    octal=""
    for o in oct(int(numero)):
        octal +=o
        if octal == '0o':
            octal=""

    return octal

def hallar_hexa_dec(array_numeros):
    result = []
    letras={'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    for x in array_numeros:
        for y in letras:
            if x == y:
                result.append(letras[y])
                break
            elif (x in letras) == False:
                result.append(x)
                break
    result.reverse()
    return result

def hallar_binario_flotante(numero):
    result = ""
    for x in range(20):
        #print('numero1:', numero)
        aux = numero *2
        numero = aux
        #print('numero2:', numero)
        parte_decimal, parte_entero = math.modf(numero)
        result += str(int(parte_entero))
        #print(result)
        if aux > 1:
            numero-=1
        elif aux  == 1.0 :
            break

    return result

def hallar_hexa_octa_flotante(numero,base):
    flt = ""
    paso_hexa = 0
    aux = 0
    if base == 16:
        for x in range(20):
            aux = numero*16
            pd,pe =math.modf(aux)
            paso_hexa = hallar_hexadecimal(pe)
            flt+=paso_hexa.upper()
            if pd == 0.0:
                break
            numero = pd
    elif base == 8:
        for x in range(20):
            aux = numero*8
            pd,pe =math.modf(aux)
            flt+=str(int(pe))
            if pd == 0.0:
                break
            numero = pd

    return flt

def hallar_decimal_flotante(numero):
    print(int(numero))

    return 0