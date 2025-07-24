from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API juego.",
        default_version='v1',

        description="""API para un sistema de gestión de un juego multijugador con funcionalidades avanzadas. 
        Permite la administración de jugadores, partidas en tiempo real, economía virtual y análisis de estadísticas. 
        Incluye autenticación JWT, emparejamiento dinámico y soporte para WebSocket.
        Diseñada para escalabilidad y seguridad, ideal para experiencias multijugador competitivas.""",
        
        terms_of_service="https://www.tusitio.com/policies/terms/",
        contact=openapi.Contact(email="contact@tusitio.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('agregar_venta/', views.agregar_venta, name='agregar_venta'),
    path('graficos/', views.graficos_ventas, name='graficos_ventas'),
    path('estadisticas_ventas/', views.estadisticas_ventas, name='estadisticas_ventas'),
    path('ventas_filtradas/', views.ventas_filtradas, name='ventas_filtradas'),
    path('graficos_interactivos/', views.graficos_interactivos, name='graficos_interactivos'),
    path('estadisticas_avanzadas/', views.estadisticas_avanzadas, name='estadisticas_avanzadas'),
    path('productos_mas_vendidos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),
    path('registro_usuario/', views.registro_usuario, name='registro_usuario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('logout_usuario/', views.logout_usuario, name='logout_usuario'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('lista_ventas/', views.lista_ventas, name='lista_ventas'),
    path('exportar/ventas/excel/', views.exportar_ventas_excel, name='exportar_ventas_excel'),

    # Autenticación con JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Documentación con Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
