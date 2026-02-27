from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Producto, Venta
from .forms import ProductoForm, VentaForm, FiltroVentasForm

class VistasTest(TestCase):
    def setUp(self):
        # Crear un usuario para pruebas
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        
        # Crear datos de prueba
        self.producto = Producto.objects.create(nombre='Producto Test', precio=50.00)
        self.venta = Venta.objects.create(producto=self.producto, cantidad=1, total=50.00)

    def test_agregar_producto(self):
        response = self.client.get(reverse('agregar_producto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agregar_producto.html')

        response = self.client.post(reverse('agregar_producto'), {
            'nombre': 'Nuevo Producto',
            'precio': 100.00
        })
        self.assertEqual(response.status_code, 302)  # Redirige a 'lista_productos'
        self.assertTrue(Producto.objects.filter(nombre='Nuevo Producto').exists())

    def test_agregar_venta(self):
        response = self.client.get(reverse('agregar_venta'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agregar_venta.html')

        response = self.client.post(reverse('agregar_venta'), {
            'producto': self.producto.id,
            'cantidad': 2
        })
        self.assertEqual(response.status_code, 302)  # Redirige a 'lista_ventas'
        self.assertTrue(Venta.objects.filter(cantidad=2).exists())

    def test_graficos_ventas(self):
        response = self.client.get(reverse('graficos_ventas'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_estadisticas_ventas(self):
        response = self.client.get(reverse('estadisticas_ventas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'estadisticas.html')

    def test_ventas_filtradas(self):
        response = self.client.get(reverse('ventas_filtradas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ventas_filtradas.html')

    def test_graficos_interactivos(self):
        response = self.client.get(reverse('graficos_interactivos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'graficos_interactivos.html')

    def test_estadisticas_avanzadas(self):
        response = self.client.get(reverse('estadisticas_avanzadas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'estadisticas_avanzadas.html')

    def test_productos_mas_vendidos(self):
        response = self.client.get(reverse('productos_mas_vendidos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productos_mas_vendidos.html')

    def test_registro_usuario(self):
        response = self.client.get(reverse('registro_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')

        response = self.client.post(reverse('registro_usuario'), {
            'username': 'newuser',
            'password1': 'newpass',
            'password2': 'newpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirige a 'login'
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_usuario(self):
        response = self.client.get(reverse('login_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(reverse('login_usuario'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirige a 'inicio'
        self.assertRedirects(response, reverse('inicio'))

    def test_logout_usuario(self):
        response = self.client.get(reverse('logout_usuario'))
        self.assertEqual(response.status_code, 302)  # Redirige a 'login'
        self.assertRedirects(response, reverse('login'))

    def test_inicio(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicio.html')

    def test_lista_productos(self):
        response = self.client.get(reverse('lista_productos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_productos.html')

    def test_lista_ventas(self):
        response = self.client.get(reverse('lista_ventas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_ventas.html')

    def test_exportar_ventas_excel(self):
        response = self.client.get(reverse('exportar_ventas_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
