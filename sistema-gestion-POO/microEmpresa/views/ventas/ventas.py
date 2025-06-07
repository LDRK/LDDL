from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ...models.categoria_producto import Categoria
from ...models.producto import Producto
from ...models.cliente import Cliente
from ...models.ventas import Venta,DetalleVenta
from ...forms import ProductoForm

@login_required
def ventas_dashboard(request):
    return render(request, 'ventas/dashboard_ventas.html')

def mostrar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "ventas/categorias.html",{'categorias': categorias})

def productos_por_categoria(request,categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, "ventas/tablaProductos.html",{
        'categoria': categoria,
        'productos': productos,
    })

def carrito_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            total_general = 0

            for producto in data:
                producto["subtotal"] = float(producto["precio"]) * int(producto["cantidad"])
                total_general += producto["subtotal"]

            return render(request, "ventas/carrito.html", {
                "carrito": data,
                "total_general": total_general
            })
        except Exception as e:
            return JsonResponse(f"Error: {e}", status=400)

    return render(request, "ventas/carrito.html", {
        "carrito": [],
        "total_general": 0
    })


def registrar_venta(request):
    if request.method == "GET":
        return render(request,'ventas/formVenta.html')
    if request.method == "POST":
        try:
            # Obtener y parsear JSON del body
            data = json.loads(request.body)
            cliente_data = data.get("cliente")
            carrito = data.get("carrito")
            print(cliente_data)
            print(carrito)

            if not cliente_data or not carrito:
                return JsonResponse({"ok": False, "error": "Faltan datos de cliente o carrito"}, status=400)

            # Crear o recuperar cliente (por ejemplo, por cédula o correo)
            cliente, created = Cliente.objects.get_or_create(
                cedula=cliente_data["cedula"],
                defaults={
                    "nombre": cliente_data["nombre"],
                    "apellido": cliente_data["apellido"],
                    "correo": cliente_data["correo"],
                    "celular": cliente_data["celular"]
                }
            )
            
             # Calcular total antes de registrar la venta
            total_venta = 0
            for item in carrito:
                cantidad = int(item["cantidad"])
                precio = float(item["precio"])
                subtotal = cantidad * precio
                total_venta += subtotal
                # Crear la venta
            venta = Venta.objects.create(
                cliente = cliente,
                usuario = request.user,  # usuario autenticado
                total = total_venta
            )

            # Registrar productos en detalle de venta
            for item in carrito:
                producto = Producto.objects.get(id=item["id"])
                cantidad = int(item["cantidad"])
                precio = float(item["precio"])
                subtotal = cantidad * precio

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal
                )

            return JsonResponse({"ok": True, "venta_id": venta.id})

        except Producto.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Producto no encontrado"}, status=404)

        except Exception as e:
            return JsonResponse({"ok": False, "error": str(e)}, status=500)

#Facturas
def mostrar_facturas(request):
    facturas = Venta.objects.select_related('cliente', 'usuario').order_by('-fecha')
    return render(request,"ventas/facturas.html",{'facturas': facturas})

def view_factura(request, factura_id):
    venta = get_object_or_404(Venta, id=factura_id)
    detalles = venta.obtener_detalles()  # usando el método del modelo

    context = {
        "venta": venta,
        "detalles": detalles,
        "total": venta.calcular_total()
    }
    return render(request, "ventas/modalFacturaContenido.html", context)

#PDF FACTURA
