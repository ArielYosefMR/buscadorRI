from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

import json
import time

# Create your views here.
@csrf_exempt
def saludo(request):
    return HttpResponse("Hola ñero")
@csrf_exempt
def buscar(request):

    doc_externo=open("/home/ArielYosef/buscadorRI/buscadorRI/templates/busqueda.html")
    plt = Template(doc_externo.read())
    doc_externo.close()
    ctx = Context()
    documento = plt.render(ctx)

    return HttpResponse(documento)

@csrf_exempt
def programa(request):
    if request.method == 'POST':
        palabra_buscar = request.POST.get('entrada')
        nombre_archivo_diccionario1 = '/home/ArielYosef/buscadorRI/buscadorRI/indiceParte1.txt'
        nombre_archivo_diccionario2 = '/home/ArielYosef/buscadorRI/buscadorRI/indiceParte2.txt'

        msg = '<html><body><h2>Resultados</h2><form action="/busqueda/" method="POST"><Input type="submit" value="Regresar"></form></body></html>'
        try:
            with open(nombre_archivo_diccionario1, 'r') as archivo:
                diccionario_cargado = archivo.read()
            with open(nombre_archivo_diccionario2, 'r') as archivo:
                diccionario_cargado += archivo.read()
        except Exception as e:
            print(f'{e}')

        inicio = time.time()
        try:
            diccionario_cargado = json.loads(diccionario_cargado)

            if diccionario_cargado and palabra_buscar in diccionario_cargado:
                resultado_busqueda = sorted(diccionario_cargado[palabra_buscar], key=lambda x: x['Valor'], reverse=True)
                msg += f'Tiempo de carga: {time.time() - inicio} segundos<br>'
                msg += f'Resultado de "{palabra_buscar}":<br>'
                msg += '<br>'.join([str(res) for res in resultado_busqueda]) + '<br>'
            else:
                msg += f'La palabra "{palabra_buscar}" no fue encontrada en el diccionario.'

            return HttpResponse(msg)
        except FileNotFoundError:
            msg = f'Error: No se pudo cargar el diccionario desde el archivo {diccionario_cargado}.'
            return HttpResponse(msg)
    else:
        return HttpResponse("Viene vacío ñero")
