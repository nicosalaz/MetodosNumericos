import struct
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def decimal_binario32(request):
    return render(request, 'decimal_binario32.html')

def binario_decimal32(request):
    return render(request, 'binario_decimal32.html')

def decimal_binario64(request):
    return render(request, 'decimal_binario64.html')

def binario_decimal64(request):
    return render(request, 'binario_decimal64.html')

def float_to_bin32(num):
    bits, = struct.unpack('!I', struct.pack('!f', num))
    return "{:032b}".format(bits)

def float_to_bin64(num):
    bits, = struct.unpack('!I', struct.pack('!f', num))
    return "{:064b}".format(bits)

def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]


def decimalBinario32(request):
    numero = "El resultado es: %r" % float_to_bin32(float(request.POST["numero"]))
    return HttpResponse(numero)

def binarioDecimal32(request):
    numero = "El resultado es: %r" % bin_to_float(request.POST["numero"])
    return HttpResponse(numero)

def decimalBinario64(request):
    numero = "El resultado es: %r" % float_to_bin64(float(request.POST["numero"]))
    return HttpResponse(numero)

def binarioDecimal64(request):
    numero = "El resultado es: %r" % bin_to_float(request.POST["numero"])
    return HttpResponse(numero)