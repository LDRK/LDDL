from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db import models
from ...models.producto import Producto, MovimientoInventario
from ...models.categoria_producto import Categoria
from ...models.inventario import Inventario
from ...forms import CategoriaForm, ProductoForm, InventarioForm

@login_required
def inventario_dashboard(request):    
    context = {
        'total_productos': Producto.total_productos(),
        'total_stock': Inventario.total_stock(),
        'stock_bajo': Inventario.stock_bajo(),
    }
    return render(request, 'inventario/inventario_dashboard.html', context)


def mostrar_productos(request):
    producto = Producto.objects.all()  # Obtiene todos los Producto
    categoProducto = Categoria.objects.select_related('producto')  # Une con la tabla de categoria

    return render(request, "inventario/tablaProducto.html", {
        'productos': producto,
        'categorias': categoProducto
    })

#Vista para registar la categoria

def registar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'ok': True,
                'message': '¡Categoría registrada exitosamente!',
                'redirect_url': '/dashboard/inventario/productos/'
            })
        else:
            return JsonResponse({
                'ok': False,
                'errors': form.errors
            }, status=400)
    else:
        form = CategoriaForm()
        return render(request, "inventario/formCategoria.html", {"form": form})

#Vista para registar el producto
def registar_productos(request):
    categorias = Categoria.objects.all() # Obtenemos todo de la tabla categorias
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            
            # Registramos el historial
            MovimientoInventario.objects.create(
                producto=producto,
                tipo='registro',
                usuario=request.user,
                descripcion=f"Registro del producto: {producto.nombre}"
            )
            return JsonResponse({
                'ok': True,
                'message': '¡Producto registrado exitosamente!',
                'redirect_url': '/dashboard/inventario/productos/'
            })
        else:
            return JsonResponse({
                'ok': False,
                'errors': form.errors
            }, status=400)
    else:
        form = ProductoForm()
        return render(request, "inventario/formProducto.html",{'categorias': categorias})

# Vista Editar Productos
def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            #Registramos el historial
            MovimientoInventario.objects.create(
                producto=producto,
                tipo='actualizacion',
                usuario=request.user,
                descripcion=f"Producto actualizado: {producto.nombre}"
            )
            return JsonResponse({'ok': True, 'redirect_url': '/dashboard/inventario/productos/'})
        else:
            return JsonResponse({'ok': False, 'errores': form.errors})
    else:
        form = ProductoForm(instance=producto)
        categorias = Categoria.objects.all()
        return render(request, "inventario/formProducto.html", {
            'form': form,  # pasar el form para mostrarlo
            'producto': producto,
            'categorias': categorias
        })
    
# Vista Para mostrar el contenido de la tabla inventario
def mostrar_inventario(request):
    inventarios = Inventario.objects.all()
    producto = Producto.objects.all()
    return render(request, "inventario/tablaInventario.html",{'inventarios': inventarios,'producto': producto})

# Vista para registrar el Stock del Producto
def registrar_inventario(request):
    productos = Producto.objects.all()
    if request.method == "POST":
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'ok': True,
                'message': '¡Producto registrado exitosamente!',
                'redirect_url': '/dashboard/inventario/store/'
            })
        else:
            return JsonResponse({
                'ok': False,
                'errors': form.errors
            }, status=400)
    else:
        form = InventarioForm()
        return render(request, "inventario/formInventario.html",{'productos':productos})
        
# Vista Editar Stock
def editar_inventario(request, id_inventario):
    stock = get_object_or_404(Inventario, id=id_inventario)
    
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return JsonResponse({'ok': True, 'redirect_url': '/dashboard/inventario/store/'})
        else:
            return JsonResponse({'ok': False, 'errores': form.errors})
    else:
        form = InventarioForm(instance=stock)
        return render(request, "inventario/formInventario.html", {
            'form': form,  # pasar el form para mostrarlo
            'stock': stock,
        })
        

def eliminar_producto(request, producto_id):
    if request.method == "POST":
        try:
            producto = Producto.objects.get(id=producto_id)
            
        #     #Registramos el historial
        #     MovimientoInventario.objects.create(
        #     producto=producto,
        #     tipo='eliminacion',
        #     usuario=request.user,
        #     descripcion=f"Producto eliminado: {producto.nombre}"
        # )
            producto.delete()
            return JsonResponse({"ok": True})
        except Producto.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Producto no encontrado"})
    return JsonResponse({"ok": False, "error": "Método no permitido"})


# #Vista para ver el historial de movimientos
# def historial_movimientos(request, producto_id):
#     producto = get_object_or_404(Producto, pk=producto_id)
#     movimientos = MovimientoInventario.objects.filter(producto=producto).order_by('-fecha')
#     return render(request, 'inventario/historial.html', {'producto': producto, 'movimientos': movimientos})

#Vista para buscar productos 
def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query).select_related('categoria')

    resultados = []
    for producto in productos:
        resultados.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': str(producto.precio),
            'categoria': producto.categoria.nombre,
        })

    return JsonResponse({'productos': resultados})