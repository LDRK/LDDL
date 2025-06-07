from django.urls import path
#Vistas de Auth
from .views.landing_page.inicio import index
from .views.auth.login import login_view 
from .views.auth.logout import logout_view
#vistas admin 
from .views.admin.admin import superadmin_dashboard,register_users,editar_users,editar_profile,complete_profile,mostrar_users 
#vistas gerente
from .views.gerente.gerente import gerente_dashboard
#vistas inventario
from .views.inventario.inventario import inventario_dashboard,mostrar_productos,registar_productos, registar_categoria, mostrar_inventario, registrar_inventario, editar_producto, editar_inventario, eliminar_producto, buscar_productos
#vistas ventas
from .views.ventas.ventas import ventas_dashboard, mostrar_categorias, productos_por_categoria, carrito_view, registrar_venta, mostrar_facturas, view_factura

urlpatterns = [
    path('', index, name='inicio'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    #--------------------------------------------------------------------------------------------------------------
    #Inicio rutas Admin
    path('dashboard/admin/', superadmin_dashboard, name="admin"),
    path('dashboard/admin/users/', mostrar_users, name='users'),
    #Registrar
    path('dashboard/register/', register_users, name="registerUser"),
    path('completeProfile/', complete_profile, name='registerProfile'),
    #Editar
    path('dashboard/editar/<int:user_id>/', editar_users, name="editarUser"),
    path('dashboard/editar/profile/<int:user_id>/', editar_profile, name="editarPerfil"),
    #Fin rutas Admin
    #--------------------------------------------------------------------------------------------------------------
    #Inicio rutas Gerente
    path('dashboard/gerente/', gerente_dashboard, name="gerente"),
    #Fin rutas Gerente
    #--------------------------------------------------------------------------------------------------------------
    #Inicio rutas Inventario
    path('dashboard/inventario/', inventario_dashboard, name="inventario"),
    path('dashboard/inventario/productos/', mostrar_productos, name='productos'),
    path('dashboard/inventario/store/', mostrar_inventario, name='viewInventario'), 
    #Registrar
    path('dashboard/inventario/rCategoria/', registar_categoria, name='registerCategoria'), 
    path('dashboard/inventario/rProducto/', registar_productos, name='registerProductos'), 
    path('dashboard/inventario/rStore/', registrar_inventario, name='registerInventario'),
    #Editar 
    path('dashboard/inventario/editar/<int:id_producto>/', editar_producto, name='editarProducto'), 
    path('dashboard/inventario/editar/stock/<int:id_inventario>/', editar_inventario, name='editarInventario'),
    #eliminar
    path('dashboard/inventario/eliminar/<int:producto_id>/', eliminar_producto, name='eliminarProducto'),
    #Buscar
    path('dashboard/inventario/buscar-productos/', buscar_productos, name='buscar_productos'),
    #Fin rutas Inventario
    #--------------------------------------------------------------------------------------------------------------
    #Inicio rutas Ventas
    path('dashboard/ventas/', ventas_dashboard, name="ventas"),
    path('dashboard/ventas/categorias/', mostrar_categorias, name="mostrarCategorias"),
    path('dashboard/ventas/producto/categoria/<int:categoria_id>/', productos_por_categoria , name="mostrarTabla"),
    path('dashboard/ventas/facturas/', mostrar_facturas , name="listarFacturas"),
    path('dashboard/ventas/viewFactura/<int:factura_id>/', view_factura , name="mostrarFactura"),
    #Venta
    path('dashboard/ventas/carrito/', carrito_view, name='carrito' ),
    #Registrar
    path('dashboard/ventas/rVenta/', registrar_venta, name='registrarVenta' ),
    #Fin rutas Ventas
    
    
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


