from django.shortcuts import render, redirect, get_object_or_404  # Importa la función render para renderizar plantillas HTML.
from django.urls import reverse  # Importa reverse para construir URLs dinámicamente.
from .models import Producto
from django.views.decorators.http import require_http_methods  # Importa para restringir los métodos HTTP permitidos.
from django.views.decorators.csrf import csrf_exempt  # Importa para exentar una vista de la protección CSRF.
from transbank.error.transbank_error import TransbankError  # Importa la excepción genérica de errores de Transbank.
from transbank.error.transaction_commit_error import TransactionCommitError  # Importa la excepción específica para errores al confirmar una transacción.
from transbank.webpay.webpay_plus.transaction import Transaction  # Importa la clase Transaction de Transbank para manejar transacciones.
import random  # Importa el módulo random para generar números aleatorios.

# Vistas básicas
def index(request):
    # Renderiza y retorna la plantilla 'index.html' cuando se accede a la vista 'index'.
    return render(request, 'index.html')



def productos(request):
    productos = Producto.objects.all()
    return render(request, 'carrito/productos.html', {'productos': productos})



def carrito(request, producto_id):
    # Convertir producto_id a string para evitar problemas de tipo
    producto_id_str = str(producto_id)
    producto = Producto.objects.get(pk=producto_id)
    
    # Verificar que el precio sea un número válido
    try:
        precio_producto = float(producto.precio)
    except ValueError:
        raise ValueError(f"El precio del producto con ID {producto_id} no es un número válido.")
    
    # Obtener o inicializar el carrito en la sesión
    carrito = request.session.get('carrito', {})

    # Verificar que el carrito sea un diccionario, no un float
    if not isinstance(carrito, dict):
        carrito = {}

    print(f"Producto ID: {producto_id_str}, Precio: {precio_producto}")
    print(f"Carrito antes de la actualización: {carrito}")


    if producto_id_str in carrito:
        # Si el producto ya está en el carrito, aumenta la cantidad
        carrito[producto_id_str]['cantidad'] += 1
        carrito[producto_id_str]['subtotal'] += float(producto.precio)

    else:
        # Si el producto no está en el carrito, agrégalo al carrito
        carrito[producto_id_str] = {
            
            'id': producto_id_str,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1,
            'subtotal': float(producto.precio),
        }

    # Calcular el total sumando todos los subtotales
    total = sum(item['subtotal'] for item in carrito.values())

    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    request.session['total'] = total

 

    print(f"Carrito después de la actualización: {carrito}")

    # Redirigir a la página de productos
    return redirect('productos')



from django.contrib import messages

def limpiar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        del request.session['total']
    
    # Redirigir a la página de productos u otra página
    return redirect('productos')  # Asegúrate de que 'productos' sea una URL válida en tu proyecto

# Transbank
@csrf_exempt  # Exenta la vista de la protección CSRF.
@require_http_methods(["POST"])  # Restringe la vista para que solo acepte solicitudes POST.
def webpay_create(request):
    print("Webpay Plus Transaction.create")
    
    # Genera un número aleatorio para el buy_order.
    buy_order = str(random.randrange(1000000, 99999999))
    
    # Genera un número aleatorio para el session_id.
    session_id = str(random.randrange(1000000, 99999999))
    
    # Obtiene el monto de la solicitud POST.
    amount = request.POST.get('amount')
    
    # Obtiene el tipo de suscripción de la solicitud POST.
    subscription_type = request.POST.get('subscription_type')
    
    # Construye la URL de retorno utilizando la función reverse para obtener la URL dinámica.
    return_url = request.build_absolute_uri(reverse('webpay_commit'))

    # Crea un diccionario con los datos de la solicitud.
    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    try:
        # Crea una transacción con Transbank utilizando los datos generados y obtenidos.
        response = Transaction().create(buy_order, session_id, amount, return_url)
        print(response)
    except TransbankError as e:
        # Si ocurre un error, se captura la excepción y se muestra un mensaje de error.
        print("Error en la creación de la transacción: {}".format(e))
        return render(request, 'webpay/error.html', {'message': str(e)})

    # Renderiza y retorna la plantilla 'create.html' con los datos de la solicitud y la respuesta de Transbank.
    return render(request, 'webpay/create.html', {
        'request': create_request,
        'response': response,
        'amount': amount,
        'subscription_type': subscription_type
    })

@csrf_exempt  # Exenta la vista de la protección CSRF.
@require_http_methods(["GET"])  # Restringe la vista para que solo acepte solicitudes GET.
def webpay_commit(request):
    # Obtiene el token de la solicitud GET (puede ser 'token_ws' o 'TBK_TOKEN').
    token = request.GET.get('token_ws') or request.GET.get('TBK_TOKEN')
    print("commit for token: {}".format(token))
    
    try:
        # Confirma la transacción con Transbank utilizando el token obtenido.
        response = Transaction().commit(token=token)
        print("response: {}".format(response))
        del request.session['carrito']
        del request.session['total']
    except TransactionCommitError as e:
        # Si ocurre un error al confirmar la transacción, se captura la excepción y se muestra un mensaje de error.
        print("Error al confirmar la transacción: {}".format(e))
        return render(request, 'webpay/error.html', {'message': str(e)})

    # Renderiza y retorna la plantilla 'commit.html' con el token y la respuesta de Transbank.
    
    return render(request, 'webpay/commit.html', {'token': token, 'response': response})
